---
name: vn-glossary-cleanup
description: Clean glossary files generated from game text extraction, using output.json and output_detail.txt.
---

# VN Glossary Cleanup

Use this skill when a text-extraction pass creates a glossary folder such as `output`.

## Inputs

- `output/output.json`
- `output/output_detail.txt`

## Keep

Prefer keeping:

- character names
- place names
- organization names
- title-specific proper nouns
- system terms
- UI terms
- repeated phrases with stable meaning

## Remove

Remove entries that are not useful terminology:

- mojibake
- script commands
- variables
- resource IDs
- pure punctuation
- unstable single characters
- bad segmentation artifacts
- strings that only appear in command or debug lines
- generic words that do not help translation consistency

## Workflow

1. Back up the glossary files.
2. Read detail sources for each term.
3. Remove unclear or unsafe entries.
4. Keep `output.json` and `output_detail.txt` synchronized.
5. Write a cleanup report.

## Project Script

If automation is needed, place game-specific scripts under:

```text
games/<game>/work/scripts/
```

Check path constants before running a cleanup script.
