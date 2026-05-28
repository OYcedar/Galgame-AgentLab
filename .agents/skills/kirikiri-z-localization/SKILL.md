---
name: kirikiri-z-localization
description: Build authorized Kirikiri Z / KAG / XP3 Chinese patches with SExtractor JSON, script reinsertion, font handling, XP3 packaging, and runtime QA.
---

# Kirikiri Z / KAG / XP3 Localization

Use this skill for authorized Kirikiri Z, Kirikiri 2, KAG, and XP3 visual novel projects.

## Engine Evidence

Common evidence:

- `*.xp3` archives.
- `.ks` KAG scenario scripts.
- `.tjs` scripts.
- `startup.tjs`, `Config.tjs`, `first.ks`, `title.ks`, or similar boot scripts.
- Error dialogs mentioning KAG tags, TJS, or `script`.

Do not assume every XP3 project has the same packing priority or patch naming. Inspect the current game first.

## Workspace

Recommended layout:

```text
games/<game>/
├─ original/
├─ work/
│  ├─ extract/
│  ├─ json/
│  ├─ patch_src/
│  ├─ reports/
│  └─ tmp/
├─ patched/
└─ release/
```

Keep the external translation JSON in SExtractor format:

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

Keep file paths, script positions, encodings, and reinsertion metadata in a separate internal map.

## Extraction

1. Extract XP3 archives from the current game version.
2. Identify scenario `.ks` and relevant `.tjs` files.
3. Export player-visible text only.
4. Preserve KAG tags in the message text when they affect display.
5. Do not translate script commands, labels, variable names, file names, macro definitions, or tag attributes unless they are visibly displayed.

Important tags and structures to protect:

- `[r]`, `[lr]`, `[p]`, `[l]`, `[cm]`, `[ct]`
- `[ruby ...]`, `[font ...]`, `[style ...]`
- `[iscript]... [endscript]`
- Macro calls and labels such as `*label`
- Storage/file attributes such as `storage=...`

If a file contains large `[iscript]` blocks, the safest reinsertion approach is to restore the original script block and only replace extracted display strings.

## Translation

- Translate into Simplified Chinese unless the project says otherwise.
- Keep the JSON order and item count unchanged.
- Keep `name` when present.
- Preserve all KAG tags and ruby tag counts.
- Normalize punctuation for the target engine after translation.
- Do not leave raw Japanese in visible text unless it is a name, title, or intentionally retained term.

## Reinsertion

1. Validate source JSON, translated JSON, and mapping.
2. Reinsert only into current-version extracted scripts.
3. Keep control tags and script code byte-for-byte where possible.
4. Encode output according to the engine behavior. Common choices are UTF-16 LE with BOM, CP932, or UTF-8, but this must be confirmed per title.
5. Re-extract or inspect the patched script files to confirm the Chinese text is really present.

If a syntax error appears at runtime, inspect the reported file and line first. Common causes:

- A translated line broke a KAG tag.
- A quote or bracket was translated inside tag attributes.
- A `[iscript]` block was accidentally modified.
- A newline was inserted where KAG expects a single command.

## Font Handling

Prefer script-level font changes before binary changes:

1. Identify the font family actually used by the game.
2. Register the required `.ttf` through the game, launcher, or an included helper DLL when available.
3. Patch KAG/TJS font declarations to use the real font family name.
4. If a dynamic placeholder such as `face=user` does not work, use the real family name directly.
5. Test inside the formal dialogue flow, not only the title screen.

When increasing font size, rewrap Chinese lines. Avoid relying on runtime wrapping because many VN message windows produce short orphan lines or overflow.

## XP3 Packaging

1. Pack only changed scripts, font registration files, and required patch metadata.
2. Do not include unmodified CG, voice, BGM, or movie archives.
3. Use a patch name that the game actually loads, such as `patch_chs.xp3`, `patch.xp3`, or a higher-priority numbered patch.
4. Re-extract the final XP3 to verify paths and encodings.
5. Test the patch against a clean copy of the current game version.

## Runtime QA

Minimum QA:

- First launch.
- Title screen.
- Start into formal dialogue.
- Load page and log page.
- Config and text speed dialogs.
- Auto/skip/Ctrl skip.
- Choice branches.
- Extra, gallery, scene, and music pages when present.
- Font rendering and line wrapping.
- Crash dialogs and syntax error dialogs.

Save screenshots and reports under `games/<game>/work/reports` or the project-specific QA folder.
