---
name: game-engine-detect
description: Detect non-RPG Windows game engines for authorized localization before extraction, patching, or testing.
---

# Game Engine Detection

Detect the engine before extraction, translation, reinsertion, or patch packaging.

## Checklist

1. List top-level files, executables, DLLs, and archive extensions.
2. Inspect archive signatures and common script extensions.
3. Check whether the executable embeds resources or loads external archives.
4. Compare old patches only as references, not as source files.
5. Write `work/engine_report.md`.

## Supported Profiles

### Kirikiri / KAG / XP3

Evidence:

- `*.xp3`
- `*.ks`
- `*.tjs`
- `startup.tjs`
- KAG or TJS runtime errors

Recommended skill: `kirikiri-z-localization`.

### LiLiM / Le.Chocolat AOS

Evidence:

- `*.aos`
- extracted `*.scr`
- commands such as `^go(...)`, `^gsb(...)`, `var`, `fnt(...)`, `wnd(...)`
- GARbro or custom tools identify AOS resources

Recommended skill: `lilim-aos-localization`.

### HSP / DPM

Evidence:

- `*.dpm`
- `DPMX` headers
- `start.ax`
- `hspcmp.dll`, `hspext.dll`, or HSP runtime signatures
- `HSPHED` inside an executable

Recommended skill: `hsp-dpm-localization`.

## Explicitly Out Of Scope

- LiveMaker / LiveNovel.
- RPG Maker workflows.
- DRM, license checks, online activation, or anti-tamper bypass.

## Engine Report

`work/engine_report.md` should include:

- suspected engine
- confidence
- evidence files
- archives that need extraction
- text format and likely encoding
- whether an old patch can be used as reference
- files that must not be mixed from old versions
- recommended next skill or workflow
