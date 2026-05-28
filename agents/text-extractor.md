# 文本提取 Agent

目标：导出玩家可见文本，供外部翻译使用。

默认输出：

- `work/json/<game>_sextractor.json`
- `work/json/<game>_sextractor_map.json`
- `work/reports/extract_report.md`

规则：

- 外部 JSON 必须使用 SExtractor 格式。
- 文件名、行号、偏移、上下文等元数据保存在映射文件里。
- 不要把脚本命令、标签、变量、调试注释、文件名或引擎关键字当成普通文本。
- 保留控制符和标签。
- 报告被跳过和疑似异常的行。
