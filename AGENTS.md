# AGENTS.md

## Purpose

This repository is for authorized Galgame and visual novel localization workflows on Windows.

It uses an agent model:

- agents describe responsibilities;
- skills describe engine-specific knowledge;
- workflows describe end-to-end procedures.

## Scope

Supported:

- Kirikiri Z / KAG / XP3
- LiLiM / Le.Chocolat AOS
- HSP / DPM
- Bruns / EENC / EENZ
- unknown non-RPG VN engine analysis
- SExtractor JSON extraction, translation, reinsertion, packaging, and runtime QA

Out of scope:

- LiveMaker / LiveNovel
- RPG Maker
- DRM bypass, activation bypass, anti-tamper bypass, or license circumvention

## Search

On the originating Windows machine, `rg` may be unavailable or refused. Prefer PowerShell-native search:

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "text"
```

## External Translation Format

All external translation JSON should use SExtractor format by default:

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1"
  }
]
```

Keep file names, offsets, line numbers, command context, and reinsertion metadata in a separate map file.

## Encoding

- JSON, reports, docs, and configs default to UTF-8.
- Original Japanese scripts often use CP932 / Shift-JIS.
- Old Chinese patches may need GBK or GB18030.
- Do not write UTF-8 Chinese into old engines that require GBK.
- Validate target encoding before repacking.

## File Discipline

- Do not place temporary files in the repository root.
- Per-game temporary files belong under `games/<game>/_work`.
- Common reusable scripts belong under `tools`.
- Engine skills belong under `.agents/skills`.
- Do not commit game bodies, unpacked original assets, saves, debug screenshots, generated 7z archives, API keys, or local model settings.

## Image Translation

When translating image-based game text, use the project's image translation workflow only. Do not silently substitute a different OCR or image editing workflow.
