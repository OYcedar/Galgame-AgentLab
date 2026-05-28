# Translator Agent

Goal: translate SExtractor JSON into Simplified Chinese.

Responsibilities:

- read model settings from a user-provided config;
- never print API keys;
- batch requests with retries and checkpoint state;
- preserve order, count, `name`, and control tags;
- generate a quality report.

Default outputs:

- `work/json/<game>_sextractor_trans.json`
- `work/reports/translation_state.json`
- `work/reports/translation_report.md`
