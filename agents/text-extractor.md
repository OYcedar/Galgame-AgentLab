# Text Extractor Agent

Goal: export player-visible text for external translation.

Default output:

- `work/json/<game>_sextractor.json`
- `work/json/<game>_sextractor_map.json`
- `work/reports/extract_report.md`

Rules:

- external JSON must be SExtractor format;
- keep metadata in the map file;
- do not extract script commands, labels, variables, debug comments, file names, or engine keywords as normal text;
- preserve control codes and tags;
- report skipped and suspicious lines.
