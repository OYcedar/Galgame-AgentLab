from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any


DEFAULT_EXTRACT_ROOT = Path("work/extract/data")
DEFAULT_PATCH_ROOT = Path("work/patch_src")
DEFAULT_MAP = Path("work/json/source_sextractor_map.json")
DEFAULT_TRANS = Path("work/json/source_sextractor_trans.json")
DEFAULT_REPORT = Path("work/reports/reinsert_report.json")

SCRIPT_EXTS = {".ks", ".tjs"}
ATTR_TEMPLATE = r'(?P<prefix>{attr}\s*=\s*")(?P<value>[^"]*)(?P<suffix>")'


def load_array(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"{path} top-level value is not an array")
    return value


def copy_script_tree(src: Path, dst: Path) -> int:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    copied = 0
    for file in src.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in SCRIPT_EXTS:
            continue
        rel = file.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, target)
        copied += 1
    return copied


def read_lines(path: Path) -> tuple[list[str], str]:
    text = path.read_text(encoding="utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    return text.splitlines(), newline


def write_lines(path: Path, lines: list[str], newline: str) -> None:
    path.write_text(newline.join(lines) + newline, encoding="utf-8")


def replace_attribute(line: str, attr: str, original: str, translated: str) -> tuple[str, bool]:
    pattern = re.compile(ATTR_TEMPLATE.format(attr=re.escape(attr)))
    for match in pattern.finditer(line):
        if match.group("value") == original:
            return line[: match.start("value")] + translated + line[match.end("value") :], True
    return line, False


def replace_label(line: str, original: str, translated: str) -> tuple[str, bool]:
    if not line.startswith("*") or "|" not in line:
        return line, False
    left, right = line.split("|", 1)
    if right.strip() != original:
        return line, False
    prefix = right[: len(right) - len(right.lstrip())]
    suffix = right[len(right.rstrip()) :]
    return f"{left}|{prefix}{translated}{suffix}", True


def apply_font_face(patch_root: Path, font_face: str | None) -> int:
    if not font_face:
        return 0
    changed = 0
    face_re = re.compile(r'(face\s*=\s*")([^"]*)(")')
    for file in patch_root.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in SCRIPT_EXTS:
            continue
        text = file.read_text(encoding="utf-8")
        new_text = face_re.sub(lambda m: m.group(1) + font_face + m.group(3), text)
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def reinsert(
    extract_root: Path,
    patch_root: Path,
    map_path: Path,
    trans_path: Path,
    report_path: Path,
    font_face: str | None,
) -> dict[str, Any]:
    mapping = load_array(map_path)
    trans = load_array(trans_path)
    if len(mapping) != len(trans):
        raise ValueError(f"map/translation count mismatch: {len(mapping)} != {len(trans)}")

    copied = copy_script_tree(extract_root, patch_root)
    by_file: dict[str, list[tuple[int, dict[str, Any], dict[str, Any]]]] = defaultdict(list)
    line_record_keys: set[tuple[str, int]] = set()
    for meta in mapping:
        if meta.get("kind") == "line":
            line_record_keys.add((str(meta["file"]), int(meta["line"])))

    skipped_shadow_attributes = 0
    for idx, (meta, record) in enumerate(zip(mapping, trans)):
        if not isinstance(record.get("message"), str):
            raise ValueError(f"translation record {idx} has no message")
        key = (str(meta["file"]), int(meta["line"]))
        if meta.get("kind") == "attribute" and key in line_record_keys:
            skipped_shadow_attributes += 1
            continue
        by_file[str(meta["file"])].append((idx, meta, record))

    issues: list[dict[str, Any]] = []
    applied = 0
    touched_files = 0

    for rel, changes in sorted(by_file.items()):
        path = patch_root / rel
        if not path.exists():
            issues.append({"kind": "missing_file", "file": rel})
            continue
        lines, newline = read_lines(path)
        changed = False
        for idx, meta, record in changes:
            line_no = int(meta["line"])
            if line_no < 1 or line_no > len(lines):
                issues.append({"index": idx, "kind": "line_out_of_range", "file": rel, "line": line_no})
                continue
            pos = line_no - 1
            kind = meta.get("kind")
            original = str(meta.get("original", ""))
            translated = str(record["message"])

            if kind == "line":
                if lines[pos] != original:
                    issues.append({
                        "index": idx,
                        "kind": "original_mismatch",
                        "file": rel,
                        "line": line_no,
                        "expected": original,
                        "actual": lines[pos],
                    })
                    continue
                lines[pos] = translated
                applied += 1
                changed = True
            elif kind == "attribute":
                new_line, ok = replace_attribute(lines[pos], str(meta.get("attr", "")), original, translated)
                if not ok:
                    issues.append({"index": idx, "kind": "attribute_mismatch", "file": rel, "line": line_no})
                    continue
                lines[pos] = new_line
                applied += 1
                changed = True
            elif kind == "label":
                new_line, ok = replace_label(lines[pos], original, translated)
                if not ok:
                    issues.append({"index": idx, "kind": "label_mismatch", "file": rel, "line": line_no})
                    continue
                lines[pos] = new_line
                applied += 1
                changed = True
            else:
                issues.append({"index": idx, "kind": "unknown_mapping_kind", "file": rel, "line": line_no, "mapping_kind": kind})

        if changed:
            write_lines(path, lines, newline)
            touched_files += 1

    font_files = apply_font_face(patch_root, font_face)
    report = {
        "script_files_copied": copied,
        "translation_records": len(trans),
        "applied_records": applied,
        "touched_files": touched_files,
        "font_face": font_face,
        "font_files_changed": font_files,
        "skipped_shadow_attributes": skipped_shadow_attributes,
        "issue_count": len(issues),
        "issues": issues[:1000],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extract-root", type=Path, default=DEFAULT_EXTRACT_ROOT)
    parser.add_argument("--patch-root", type=Path, default=DEFAULT_PATCH_ROOT)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP)
    parser.add_argument("--translation", type=Path, default=DEFAULT_TRANS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--font-face", default="Microsoft YaHei")
    args = parser.parse_args()
    report = reinsert(args.extract_root, args.patch_root, args.map, args.translation, args.report, args.font_face)
    print(json.dumps({k: report[k] for k in ("script_files_copied", "applied_records", "issue_count", "font_files_changed")}, ensure_ascii=False, indent=2))
    return 0 if report["issue_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
