from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_SOURCE = Path("work/json/source_sextractor.json")
DEFAULT_TRANS = Path("work/json/source_sextractor_trans.json")
DEFAULT_REPORT = Path("work/reports/translation_validation.json")

TAG_RE = re.compile(r"\[[^\]]*\]")
JP_RE = re.compile(r"[\u3040-\u30ff]")
WARNING_KINDS = {"source_residual", "untranslated_source_equal"}


def load_array(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise ValueError(f"{path} 顶层不是数组")
    return value


def tags(text: str) -> list[str]:
    return TAG_RE.findall(text)


def validate(source_path: Path, trans_path: Path) -> dict[str, Any]:
    source = load_array(source_path)
    trans = load_array(trans_path)
    issues: list[dict[str, Any]] = []
    if len(source) != len(trans):
        issues.append({"kind": "count_mismatch", "source": len(source), "translation": len(trans)})
    for idx, src in enumerate(source[: len(trans)]):
        dst = trans[idx]
        if not isinstance(src, dict) or not isinstance(dst, dict):
            issues.append({"index": idx, "kind": "record_type"})
            continue
        if not isinstance(src.get("message"), str) or not isinstance(dst.get("message"), str):
            issues.append({"index": idx, "kind": "message_type"})
            continue
        if ("name" in src) != ("name" in dst):
            issues.append({"index": idx, "kind": "name_field_mismatch"})
        if "name" in src and not isinstance(dst.get("name"), str):
            issues.append({"index": idx, "kind": "name_type"})
        if not dst["message"].strip():
            issues.append({"index": idx, "kind": "empty_message"})
        src_tags = tags(src["message"])
        dst_tags = tags(dst["message"])
        if src_tags != dst_tags:
            issues.append({
                "index": idx,
                "kind": "tag_mismatch",
                "source_tags": src_tags,
                "translation_tags": dst_tags,
                "source": src["message"],
                "translation": dst["message"],
            })
        visible_translation = TAG_RE.sub("", dst["message"])
        if dst["message"] == src["message"] and JP_RE.search(TAG_RE.sub("", src["message"])):
            issues.append({
                "index": idx,
                "kind": "untranslated_source_equal",
                "translation": dst["message"],
            })
        elif JP_RE.search(visible_translation):
            issues.append({
                "index": idx,
                "kind": "source_residual",
                "translation": dst["message"],
            })
    hard_issues = [issue for issue in issues if issue.get("kind") not in WARNING_KINDS]
    return {
        "source_count": len(source),
        "translation_count": len(trans),
        "issue_count": len(issues),
        "hard_issue_count": len(hard_issues),
        "issues": issues[:1000],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--translation", type=Path, default=DEFAULT_TRANS)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    report = validate(args.source, args.translation)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("source_count", "translation_count", "issue_count", "hard_issue_count")}, ensure_ascii=False, indent=2))
    return 0 if report["hard_issue_count"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
