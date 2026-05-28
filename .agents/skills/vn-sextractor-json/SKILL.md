---
name: vn-sextractor-json
description: Extract and validate external translation JSON in SExtractor format for all non-RPG game projects.
---

# SExtractor JSON

All external translation handoff files should use SExtractor JSON unless the project explicitly requires another format.

## Format

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1。"
  },
  {
    "name": "MaybeName2",
    "message": "「Text2」"
  }
]
```

Rules:

- UTF-8 JSON.
- Top-level value is an array.
- Every item has `message`.
- `name` appears only when a speaker exists.
- Order matches the original script order.
- Metadata for reinsertion goes in a separate map file.

## Extract

Export only player-visible text:

- dialogue
- speaker names
- choices
- menu text
- system prompts
- scene titles when visibly shown

Do not export:

- labels
- variable names
- debug parameters
- command names
- file names
- resource IDs
- comments
- script-only control lines

Known non-dialogue examples:

```text
^gsb(VAR)
%route
^go(TITLE)
var %temp
```

## Validate

Before reinsertion:

- source and translation parse as JSON
- both top-level values are arrays
- item counts match
- every item has `message`
- `name` presence matches the source unless intentionally changed
- control tags and placeholders are preserved
- messages are encodable in the target engine encoding
- empty translations are reported
- obvious source-language residue is reported for review

## Naming

Recommended names:

- source: `<game>_sextractor.json`
- translation: `<game>_sextractor_trans.json`
- internal map: `<game>_sextractor_map.json`
- validation report: `<game>_sextractor_validation.json`

## Pre-Reinsertion Cleanup

Depending on engine behavior, normalize:

- ASCII punctuation
- halfwidth English and digits in visible prose
- Japanese quotes
- ellipses and wave dashes
- hearts, music notes, sweat marks, and other symbols
- fixed-width dialogue wrapping
