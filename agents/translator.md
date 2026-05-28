# 翻译 Agent

目标：把 SExtractor JSON 翻译为简体中文。

职责：

- 从用户提供的配置读取模型设置。
- 不打印 API Key。
- 按批次请求，支持重试和断点状态。
- 保留顺序、条数、`name` 字段和控制标签。
- 生成质量报告。

默认输出：

- `work/json/<game>_sextractor_trans.json`
- `work/reports/translation_state.json`
- `work/reports/translation_report.md`
