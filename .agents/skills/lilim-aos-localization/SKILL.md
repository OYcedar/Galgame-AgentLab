---
name: lilim-aos-localization
description: Localize LiLiM / Le.Chocolat AOS visual novels, including scr.aos extraction, SExtractor JSON, GBK-safe script repair, AOSv2 repacking, embedded exe patching, font config, and runtime QA.
---

# LiLiM / AOS Localization

Use this skill for authorized LiLiM, Le.Chocolat, and related AOS visual novel projects.

## Engine Evidence

Common evidence:

- `*.aos` archives.
- Extracted `*.scr` scripts.
- Script commands such as `var`, `^go(...)`, `^gsb(...)`, `bgmoff`, `fnt(...)`, `wnd(...)`, or `wbl(...)`.
- Old Windows VN executables that may embed `scr.aos` inside a wrapper.

## Workspace

Use a per-game workspace:

```text
games/<game>/
├─ original/
├─ old_patch/
├─ work/
│  ├─ aos/
│  ├─ decoded/
│  ├─ json/
│  ├─ reports/
│  └─ scripts/
├─ patched/
└─ release/
```

Do not put temporary exe, dll, extracted script dumps, or one-off analysis files in the repository root.

## Extraction

1. Confirm the AOS archive layout before decoding.
2. Extract script files into `work/decoded`.
3. Export SExtractor JSON for external translation.
4. Store file names, line positions, script contexts, and encodings in an internal map.
5. Do not export script commands, labels, variable declarations, comments, or debug parameters as dialogue.

Known non-dialogue examples:

- `^gsb(VAR)`
- `%route`
- `^go(TITLE)`
- `var %temp`
- Comment lines beginning with `#`

## Script Reinsertion

- Old AOS engines commonly require GBK or GB18030 output for Chinese patches.
- Do not write UTF-8 Chinese into scripts unless the current executable has been verified to support it.
- Only visible dialogue, names, menu text, time cards, and choices should be localized.
- Keep engine commands in halfwidth ASCII.
- Never fullwidth-convert command lines, labels, variable names, or function calls.

After reinsertion, scan command-like lines by NFKC normalization. If a normalized line matches a known script command shape, restore it to the original command form.

## Character Rules

GBK-targeted AOS projects often show mojibake when Shift-JIS punctuation or Japanese symbols remain in visible text. Fix visible text conservatively:

- Convert visible halfwidth English and digits to the old-patch style only when they are ordinary displayed prose.
- Keep script syntax and command arguments halfwidth.
- Standalone time cards should follow the old patch's known safe fullwidth style.
- Replace Shift-JIS residue, hearts, music notes, wave dashes, Japanese quote marks, and special punctuation with characters the target encoding and font can render.
- Treat choice delimiters as syntax. Only edit the visible choice text inside the delimiter.
- If the archive grows too large for an embedded slot, shrink comments first. Do not shorten visible text or commands just to fit.

When an old patch exists, use it as a style reference, not as a base file. Never mix an old-version full archive into a new-version body.

## AOSv2 Repacking

Some AOSv2 entries are stored as:

```text
uint32 unpacked_size
custom compressed body
```

When rebuilding an index, the entry size must include the four-byte unpacked size header plus the compressed body length.

Recommended flow:

1. Use the original archive as the file-order template.
2. Rebuild each modified `.scr`.
3. Preserve the original file order and unmodified entries.
4. Verify that each index `offset + size` matches the next entry offset.
5. Re-extract the rebuilt archive and inspect boot scripts, title scripts, variable scripts, and several scenario files.

The helper scripts in this skill's `scripts/` directory are meant to be called with project-local paths, for example:

```powershell
python .agents\skills\lilim-aos-localization\scripts\pack_aosv2_entrysize.py `
  --scr-dir games\<game>\work\decoded\patched `
  --template games\<game>\work\aos\scr_original.aos `
  --output games\<game>\work\aos\scr_chs.aos
```

## Embedded Exe Patching

Some Chinese patches embed `scr.aos` inside a modified executable.

Safe approach:

1. Keep the current-version executable as the base.
2. Compare old patch behavior only for clues.
3. Locate the embedded archive slot by exact old archive bytes or verified offset metadata.
4. Ensure the new archive fits the slot.
5. Write the new archive into the slot and zero-fill the remaining bytes.
6. Avoid modifying wrapper metadata unless you have verified the resulting exe enters the foreground and reaches the title menu.

## Font And Wrapping

Font launchers usually handle one or more of these tasks:

- Temporarily register a TTF file.
- Read a UTF-8 `.ini` configuration.
- Patch save/system data or script font settings.

Dialogue size and wrapping are often controlled by scripts:

- `fnt(...)` controls font size and style.
- `wnd(...)` can control message window line width.
- `wbl(...)` can control backlog line width.

When increasing font size, reduce line width and test the formal dialogue flow. Do not rely on a launcher setting if the packed scripts still set a smaller font.

## Runtime QA

Minimum QA:

- First launch reaches the title menu.
- Start reaches formal dialogue.
- Load slot 1 reaches visible dialogue.
- Save, load, and backlog pages show readable Chinese.
- Extra, CG, scene replay, and music pages do not crash.
- Ctrl skip does not hang around movies, OP cards, or time cards.
- No visible command text such as `var %temp`, `%route`, or `^go(...)`.
- No GBK mojibake remains in visible text.
- Font launcher is verified in formal dialogue, not just the title menu.

Save screenshots and reports under the current game's `work/reports` folder.
