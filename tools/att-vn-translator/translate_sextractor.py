from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI


DEFAULT_SOURCE = Path("work/json/source_sextractor.json")
DEFAULT_OUTPUT = Path("work/json/source_sextractor_trans.json")
DEFAULT_STATE = Path("work/reports/translation_state.json")
DEFAULT_REPORT = Path("work/reports/translation_report.md")
DEFAULT_SETTING = Path("setting.toml")

TAG_RE = re.compile(r"\[[^\]]*\]")
SOURCE_RE = re.compile(r"[\u3040-\u30ff]")


@dataclass(frozen=True)
class LlmConfig:
    base_url: str
    api_key: str
    model: str
    timeout: int
    worker_count: int
    rpm: int | None
    retry_count: int
    retry_delay: int


def parse_simple_toml(path: Path) -> dict[str, dict[str, Any]]:
    data: dict[str, dict[str, Any]] = {}
    section = ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line.strip("[]")
            data.setdefault(section, {})
            continue
        if "=" not in line or not section:
            continue
        key, value = [part.strip() for part in line.split("=", 1)]
        if value.startswith('"') and value.endswith('"'):
            parsed: Any = value[1:-1]
        elif value.lower() == "true":
            parsed = True
        elif value.lower() == "false":
            parsed = False
        elif re.fullmatch(r"-?\d+", value):
            parsed = int(value)
        elif re.fullmatch(r"-?\d+\.\d+", value):
            parsed = float(value)
        else:
            parsed = value
        data.setdefault(section, {})[key] = parsed
    return data


def load_config(path: Path) -> LlmConfig:
    data = parse_simple_toml(path)
    llm = data.get("llm", {})
    text = data.get("text_translation", {})
    base_url = str(
        llm.get("base_url")
        or os.environ.get("LLM_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or os.environ.get("DEEPSEEK_BASE_URL")
        or ("https://api.deepseek.com" if os.environ.get("DEEPSEEK_API_KEY") else "")
    )
    api_key = str(
        llm.get("api_key")
        or os.environ.get("LLM_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or os.environ.get("DEEPSEEK_API_KEY")
        or ""
    )
    model = str(
        llm.get("model")
        or os.environ.get("LLM_MODEL")
        or os.environ.get("OPENAI_MODEL")
        or os.environ.get("DEEPSEEK_MODEL")
        or ("deepseek-chat" if os.environ.get("DEEPSEEK_API_KEY") else "")
    )
    missing = [name for name, value in (("base_url", base_url), ("api_key", api_key), ("model", model)) if not value]
    if missing:
        raise ValueError(f"setting.toml or environment is missing llm config: {', '.join(missing)}")
        raise ValueError(f"setting.toml 缺少 llm 配置: {', '.join(missing)}")
    return LlmConfig(
        base_url=base_url,
        api_key=api_key,
        model=model,
        timeout=int(llm.get("timeout", 600)),
        worker_count=max(1, int(text.get("worker_count", 4))),
        rpm=int(text["rpm"]) if text.get("rpm") else None,
        retry_count=max(0, int(text.get("retry_count", 3))),
        retry_delay=max(0, int(text.get("retry_delay", 2))),
    )


def load_json_array(path: Path) -> list[dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, list):
        raise ValueError(f"{path} 顶层不是数组")
    for i, item in enumerate(value):
        if not isinstance(item, dict) or not isinstance(item.get("message"), str):
            raise ValueError(f"{path} 第 {i} 条不是 SExtractor message 记录")
    return value


def extract_tags(text: str) -> list[str]:
    return TAG_RE.findall(text)


def protect_tags(text: str) -> tuple[str, list[str]]:
    tags: list[str] = []

    def repl(match: re.Match[str]) -> str:
        tags.append(match.group(0))
        return f"@@TAG{len(tags) - 1:03d}@@"

    return TAG_RE.sub(repl, text), tags


def restore_tags(text: str, tags: list[str]) -> str:
    restored = text
    for i, tag in enumerate(tags):
        restored = restored.replace(f"@@TAG{i:03d}@@", tag)
    return restored


def repair_simple_tag_layout(source: str, translated: str) -> str | None:
    """Repair lines whose KAG tags are only quote/newline tags at the edges."""
    source_tags = extract_tags(source)
    if not source_tags:
        return translated
    if any(tag.lower().startswith("[ruby") or tag.lower().startswith("[font") or tag.lower().startswith("[style") for tag in source_tags):
        return None

    leading: list[str] = []
    rest = source
    while True:
        match = TAG_RE.match(rest)
        if not match:
            break
        leading.append(match.group(0))
        rest = rest[match.end() :]

    trailing: list[str] = []
    rest = rest.rstrip()
    while True:
        matches = list(TAG_RE.finditer(rest))
        if not matches:
            break
        last = matches[-1]
        if last.end() != len(rest):
            break
        trailing.insert(0, last.group(0))
        rest = rest[: last.start()].rstrip()

    if len(leading) + len(trailing) != len(source_tags):
        return None

    text_only = TAG_RE.sub("", translated).strip()
    repaired = "".join(leading) + text_only + "".join(trailing)
    if extract_tags(repaired) == source_tags:
        return repaired
    return None


def split_batches(records: list[dict[str, Any]], pending: list[int], max_items: int, max_chars: int) -> list[list[int]]:
    batches: list[list[int]] = []
    current: list[int] = []
    chars = 0
    for idx in pending:
        size = len(records[idx]["message"]) + len(records[idx].get("name", ""))
        if current and (len(current) >= max_items or chars + size > max_chars):
            batches.append(current)
            current = []
            chars = 0
        current.append(idx)
        chars += size
    if current:
        batches.append(current)
    return batches


def parse_model_json(text: str) -> list[dict[str, Any]]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    candidates = [stripped]
    left = stripped.find("[")
    right = stripped.rfind("]")
    if left != -1 and right > left:
        candidates.append(stripped[left : right + 1])
    last_error: Exception | None = None
    value: Any = None
    for candidate in candidates:
        try:
            value = json.loads(candidate)
            break
        except json.JSONDecodeError as exc:
            last_error = exc
    else:
        preview = stripped[:600].replace("\r", "\\r").replace("\n", "\\n")
        raise ValueError(f"model did not return parseable JSON: {last_error}; preview={preview!r}") from last_error
    if isinstance(value, dict):
        for key in ("items", "translations", "results"):
            if isinstance(value.get(key), list):
                value = value[key]
                break
    if not isinstance(value, list):
        raise ValueError("模型返回顶层不是数组，且没有 items/translations/results 数组")
    return value


def valid_existing_translation(src: dict[str, Any], dst: dict[str, Any] | None) -> bool:
    if not isinstance(dst, dict) or not isinstance(dst.get("message"), str):
        return False
    if ("name" in src) != ("name" in dst):
        return False
    if "name" in src and not isinstance(dst.get("name"), str):
        return False
    if not dst["message"].strip():
        return False
    if dst["message"] == src["message"]:
        return False
    return extract_tags(src["message"]) == extract_tags(dst["message"])


class RateLimiter:
    def __init__(self, rpm: int | None) -> None:
        self.interval = 60.0 / rpm if rpm else 0.0
        self._lock = asyncio.Lock()
        self._next_at = 0.0

    async def wait(self) -> None:
        if self.interval <= 0:
            return
        async with self._lock:
            now = time.monotonic()
            if now < self._next_at:
                await asyncio.sleep(self._next_at - now)
            self._next_at = max(now, self._next_at) + self.interval


def build_prompt(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    system = (
        "你是专业日文视觉小说汉化译者。把玩家可见日文翻译成自然、通顺的简体中文。"
        "严格保护所有形如 @@TAG000@@ 的占位符，不能删除、改名、重排。"
        "不要翻译文件名、变量名或代码；如果文本主要是控制符，只翻译可见文字。"
        "只返回 JSON，不要解释。优先返回 {\"items\":[{\"id\":数字,\"message\":\"译文\"}]}。"
    )
    user = {
        "task": "translate_ja_visual_novel_to_zh_cn",
        "rules": [
            "保留 @@TAGxxx@@ 占位符。",
            "中文使用简体。",
            "语气贴近 Galgame 对白，避免机器翻译腔。",
            "不要输出 Markdown。",
        ],
        "items": items,
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
    ]


async def translate_batch(
    *,
    client: AsyncOpenAI,
    config: LlmConfig,
    limiter: RateLimiter,
    records: list[dict[str, Any]],
    batch: list[int],
) -> dict[int, str]:
    protected_by_id: dict[int, tuple[str, list[str]]] = {}
    payload: list[dict[str, Any]] = []
    for idx in batch:
        protected, tags = protect_tags(records[idx]["message"])
        protected_by_id[idx] = (protected, tags)
        item: dict[str, Any] = {"id": idx, "message": protected}
        if records[idx].get("name"):
            item["name"] = records[idx]["name"]
        payload.append(item)

    last_error: Exception | None = None
    for attempt in range(config.retry_count + 1):
        try:
            await limiter.wait()
            request = {
                "model": config.model,
                "messages": build_prompt(payload),
                "temperature": 0.2,
            }
            try:
                response = await client.chat.completions.create(
                    **request,
                    response_format={"type": "json_object"},
                )
            except Exception as exc:
                if "response_format" not in str(exc):
                    raise
                response = await client.chat.completions.create(**request)
            content = response.choices[0].message.content or ""
            translated = parse_model_json(content)
            result: dict[int, str] = {}
            for item in translated:
                idx = int(item["id"])
                message = str(item["message"])
                if idx not in protected_by_id:
                    raise ValueError(f"模型返回未知 id: {idx}")
                _, tags = protected_by_id[idx]
                restored = restore_tags(message, tags)
                if extract_tags(records[idx]["message"]) != extract_tags(restored):
                    repaired = repair_simple_tag_layout(records[idx]["message"], restored)
                    if repaired is None:
                        raise ValueError(f"第 {idx} 条控制符不一致")
                    restored = repaired
                result[idx] = restored
            missing = set(batch) - set(result)
            if missing:
                raise ValueError(f"模型漏翻 id: {sorted(missing)[:5]}")
            return result
        except Exception as exc:
            last_error = exc
            if attempt >= config.retry_count:
                break
            await asyncio.sleep(config.retry_delay * (attempt + 1))
    raise RuntimeError(f"批次 {batch[0]}-{batch[-1]} 翻译失败: {last_error}") from last_error


def save_outputs(
    *,
    source: list[dict[str, Any]],
    output: list[dict[str, Any] | None],
    output_path: Path,
    state_path: Path,
    failures: list[str],
) -> None:
    complete_output: list[dict[str, Any]] = []
    completed = 0
    for src, dst in zip(source, output):
        if isinstance(dst, dict):
            complete_output.append(dst)
            completed += 1
        else:
            complete_output.append({"name": src.get("name"), "message": src["message"]} if "name" in src else {"message": src["message"]})
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(complete_output, ensure_ascii=False, indent=2), encoding="utf-8")
    state = {
        "total": len(source),
        "completed": completed,
        "remaining": len(source) - completed,
        "failures": failures[-20:],
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


async def run(args: argparse.Namespace) -> int:
    config = load_config(args.setting)
    client = AsyncOpenAI(api_key=config.api_key, base_url=config.base_url, timeout=config.timeout)
    records = load_json_array(args.source)

    existing: list[dict[str, Any]] = []
    if args.output.exists():
        try:
            existing = load_json_array(args.output)
        except Exception:
            existing = []
    output: list[dict[str, Any] | None] = [None] * len(records)
    if len(existing) == len(records):
        for i, (src, dst) in enumerate(zip(records, existing)):
            if valid_existing_translation(src, dst):
                output[i] = dst

    pending = [i for i, item in enumerate(output) if item is None]
    if args.limit:
        pending = pending[: args.limit]
    batches = split_batches(records, pending, args.batch_size, args.max_chars)
    workers = max(1, min(args.workers or config.worker_count, args.worker_cap))
    limiter = RateLimiter(config.rpm)
    failures: list[str] = []
    lock = asyncio.Lock()
    queue: asyncio.Queue[list[int]] = asyncio.Queue()
    for batch in batches:
        queue.put_nowait(batch)

    async def worker(worker_id: int) -> None:
        while not queue.empty():
            batch = await queue.get()
            try:
                translated = await translate_batch(
                    client=client,
                    config=config,
                    limiter=limiter,
                    records=records,
                    batch=batch,
                )
                async with lock:
                    for idx, message in translated.items():
                        dst: dict[str, Any] = {"message": message}
                        if "name" in records[idx]:
                            dst["name"] = records[idx]["name"]
                        output[idx] = dst
                    save_outputs(
                        source=records,
                        output=output,
                        output_path=args.output,
                        state_path=args.state,
                        failures=failures,
                    )
                    done = sum(1 for item in output if item is not None)
                    print(f"[worker {worker_id}] 完成 {done}/{len(records)}")
            except Exception as exc:
                async with lock:
                    failures.append(str(exc))
                    save_outputs(
                        source=records,
                        output=output,
                        output_path=args.output,
                        state_path=args.state,
                        failures=failures,
                    )
                raise
            finally:
                queue.task_done()

    await asyncio.gather(*(worker(i + 1) for i in range(workers)))
    completed = sum(1 for item in output if item is not None)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        "\n".join(
            [
                "# VN 翻译报告",
                "",
                f"- 总条数: {len(records)}",
                f"- 已完成: {completed}",
                f"- 未完成: {len(records) - completed}",
                f"- 模型: {config.model}",
                f"- 服务: {config.base_url}",
                f"- 失败数: {len(failures)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return 0 if completed == len(records) else 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--setting", type=Path, default=DEFAULT_SETTING)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--max-chars", type=int, default=4500)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--worker-cap", type=int, default=16)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
