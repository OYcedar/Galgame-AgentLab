---
name: hsp-dpm-localization
description: Localize HSP/DPM games, including DPM extraction, GBK/GB18030 text handling, current-version exe patching, SExtractor repack, and runtime QA.
---

# HSP / DPM Localization

Use this skill for authorized games built on HSP or archives using DPM/DPMX.

## Engine Evidence

Common evidence:

- `*.dpm` or DPMX archives.
- `start.ax`.
- `hspcmp.dll`, `hspext.dll`, or HSP runtime DLLs.
- `DPMX` headers.
- `HSPHED` data in an executable.

## Workspace

Use a per-game workspace:

```text
games/<game>/
├─ original/
├─ old_body/
├─ old_patch/
├─ HSP-PACK/
├─ work/
│  ├─ extract/
│  ├─ json/
│  ├─ repack/
│  ├─ reports/
│  └─ tmp/
├─ patched/
└─ release/
```

All extracted files, temporary DLL/EXE copies, disassembly outputs, and test packages must stay inside the current game's `work` directory.

## Extraction

1. Extract from the current game body, not from an old patch.
2. Enumerate all `*.dpm` archives, including DLC and extra scenario archives.
3. Identify scenario text, system text, choices, replay titles, and prompt strings.
4. Export visible text as SExtractor JSON.
5. Keep an internal map for archive name, file name, offsets, command context, and target encoding.
6. Produce an extraction summary with total strings, skipped command strings, and encoding risks.

## Old Patch Reference

An old patch can be used to learn:

- How special punctuation was normalized.
- How Chinese archives were named.
- Whether the exe needed code page, font, or archive-name changes.
- Which runtime screens were known to work.

Do not reuse:

- Old-version DPM archives.
- Old-version executables.
- Old extracted scripts as the base for a new body.

## Reinsertion

1. Read `<game>_sextractor_trans.json`.
2. Validate count, order, names, line breaks, and target encoding.
3. Normalize visible punctuation according to the current engine behavior.
4. Rebuild archives from the current game extraction.
5. Re-extract the rebuilt product and confirm Chinese text was written.

GBK or GB18030 is common for Chinese HSP patches, but verify the current executable before committing to an encoding.

## Symbol Rules

- Convert visible ASCII punctuation to fullwidth or Chinese punctuation when the engine/font renders halfwidth badly.
- Visible halfwidth letters and digits may be converted to fullwidth according to project style.
- Keep file names, variables, archive names, and engine identifiers unchanged unless the exe is patched accordingly.
- Replace hearts, music notes, wave dashes, Japanese quotes, and special marks with target-encoding-safe characters.
- If scene names appear in save/load lists, test them separately because unsafe text can break save pages.

## Exe Work

If Chinese display requires exe changes:

1. Start from the current-version executable.
2. Compare old body, old patch, and current body only to identify the needed change.
3. Patch code page, font name, archive name, or embedded script references in the current exe.
4. Do not bypass DRM, activation, online checks, anti-tamper, or license checks.
5. Runtime-test the patched exe. File size similarity is not enough.

If the game hangs on a loading screen:

- Confirm the archive names match what the exe loads.
- Check DPM headers, entry sizes, checksums, and packing options.
- Confirm no old-version archive replaced a current-version archive.

## Runtime QA

Minimum QA:

- First launch.
- Title or main menu.
- Formal dialogue.
- Save page.
- Load page.
- Log page.
- Choices and branches.
- DLC or extra scenario entry points.

Save screenshots and logs under `games/<game>/work/reports`.

## Release

Release packages usually include:

- Current-version Chinese exe when needed.
- Current-version rebuilt Chinese DPM archives.
- Required fonts and configuration files.
- Usage instructions.

Do not include `_work`, saves, old patch files, or unmodified large CG/voice/BGM archives.
