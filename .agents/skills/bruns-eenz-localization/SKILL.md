---
name: bruns-eenz-localization
description: Localize Bruns/BGI-like EENC/EENZ visual novels, including ams.cfg, scene BSO scripts, SExtractor JSON, GB18030 reinsertion, exe UI strings, VOICE warning suppression, and runtime QA.
---

# Bruns / EENC / EENZ Localization

Use this skill for authorized visual novels that use Bruns-style encrypted resources and Lisp-like `a3:` scripts.

## Engine Evidence

Common evidence:

- Encrypted files beginning with `EENC` or `EENZ`.
- `ams.cfg` engine configuration.
- `scene/*.bso` scenario scripts.
- Decrypted script text contains Lisp-like forms such as:
  - `(a3:define-set ...)`
  - `(a3:call-user-func ...)`
  - `(a3:send-string ...)`
- Runtime title or files mention `Bruns`.

This engine family may resemble BGI/Ethornell in workflow shape, but do not assume BGI tools can directly unpack it.

## Workspace

Recommended layout:

```text
games/<game>/
├─ original/
├─ work/
│  ├─ extract/
│  │  └─ scene_decrypted/
│  ├─ json/
│  ├─ patch_scene_decrypted/
│  ├─ patch_scene/
│  ├─ reports/
│  └─ tmp/
├─ patched/
└─ release/
```

Keep all one-off binary copies, decrypted config files, screenshots, and test scripts inside the current game's `work` directory.

## EEN Files

Observed file behavior:

- `EENC` and `EENZ` are encrypted wrappers.
- `EENZ` payloads may also be compressed.
- `ams.cfg`, `scene/*.bso`, and some `parts/*.png` can be wrapped.

Workflow:

1. Back up original encrypted files.
2. Decrypt `ams.cfg` and all target `scene/*.bso`.
3. Edit only decrypted working copies.
4. Re-encrypt changed files back to the same paths and names.
5. Re-decrypt the final output and confirm expected Chinese text is present.

## Text Extraction

External translation handoff must use SExtractor JSON:

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

Keep file names, script offsets, call contexts, and original byte spans in an internal map file.

Extract player-visible text from scenario scripts and menu/system strings. Do not extract:

- `a3:` commands.
- Numeric resource IDs.
- Variable references such as `(a3:idref-word ...)`.
- File paths and resource names.
- Debug comments.

## Translation And Encoding

- Target Simplified Chinese unless the project says otherwise.
- GB18030 is a safe target encoding for Chinese script reinsertion in this engine; verify per title.
- JSON, reports, and docs stay UTF-8.
- Preserve command structure and line endings around replaced strings.
- Validate that every translated string can encode to the target script encoding.

## Ruby And Special Text

Bruns scripts may contain ruby markers such as:

```text
&RA<base>&RS<ruby>&RT
```

For Chinese patches, prefer flattening ruby to the base text unless the engine rendering is explicitly verified for Chinese. This avoids small stray text above the baseline and broken log display.

After reinsertion, scan the translated JSON and decrypted scripts for leftover `&RA`, `&RS`, and `&RT` unless the project intentionally keeps ruby.

## Exe Work

Allowed exe changes are display/localization compatibility only:

- Window title strings.
- System/log labels.
- Debug warning behavior that blocks gameplay.

Do not bypass DRM, activation, online checks, anti-tamper, or license checks.

### VOICE Warning

Some Bruns builds show a modal debug warning:

```text
[WARN] VOICE制御は未対応です(%d)
```

Do not disable `voice` configuration or remove voice playback calls just to hide the warning.

If runtime confirms this is only a debug warning and voice playback must remain intact, prefer a minimal exe patch that downgrades the log level string from `WARN ` to an equal-length non-modal level such as `TRACE`. Keep the `VOICE...` message and all script voice calls intact.

Always test:

- first launch;
- title menu;
- entering formal dialogue;
- at least one voiced line if available.

## Font Handling

Be conservative with fonts.

- Prefer known working system fonts in `ams.cfg`.
- Do not ship a launcher that registers fonts unless runtime proves the engine uses that registered font.
- If a local `.ttf` is requested, first verify the real Windows font family name and confirm a formal dialogue screenshot changes.
- If font experiments fail or do not improve rendering, revert the launcher, `.ini`, user-font registration, and release files.

## Runtime QA

Minimum QA:

- First launch without modal debug warnings.
- Title menu and choice menu.
- Start into formal dialogue.
- Log/backlog.
- Save/load page.
- Ctrl skip or auto mode.
- Scene replay / CG / gallery pages if present.
- Voice playback remains functional after any warning suppression.

Save screenshots under `games/<game>/work/reports`.

## Release

Release only files players need:

- Patched exe if needed.
- Patched `ams.cfg`.
- Patched `scene/*.bso`.
- Required README.

Do not include:

- `_work`.
- save data.
- decrypted scripts.
- debug screenshots.
- unmodified CG, voice, BGM, or movie archives.
- failed font launcher files or unverified external fonts.
