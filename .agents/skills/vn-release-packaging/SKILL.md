---
name: vn-release-packaging
description: Build a clean Chinese patch release folder for non-RPG visual novel projects.
---

# VN Release Packaging

Use this skill when preparing a player-facing Chinese patch release folder.

## Preflight

Confirm before packaging:

- The patched game launches from a clean current-version body.
- The release exe, if included, is based on the current-version exe.
- Script archives were rebuilt from current-version files.
- Required fonts and configuration files are present.
- `.ini` files and readme files are UTF-8.
- No `_work`, save data, screenshots, extracted assets, or temporary tools are included.

## Include Only What Players Need

Common release contents:

- Patched exe when needed for Chinese display.
- Modified script or text archive.
- Font launcher or helper DLL when required.
- Font files required by the patch.
- UTF-8 configuration files.
- Usage instructions.

Do not include:

- Unmodified CG archives.
- Unmodified voice archives.
- Unmodified BGM archives.
- Movies unless actually patched and redistributable.
- Extracted raw assets.
- Test screenshots.
- Save folders.
- Old patch files for a different game version.
- Temporary analysis files.

## Generic Layouts

Kirikiri / XP3:

```text
<game>_CHS_patch/
├─ patch_chs.xp3
├─ fonts/
│  └─ <font>.ttf
└─ README.txt
```

LiLiM / AOS:

```text
<game>_CHS_patch/
├─ <game>_chs.exe
├─ <font_launcher>.exe
├─ <font_launcher>.ini
├─ <font>.ttf
└─ README.txt
```

HSP / DPM:

```text
<game>_CHS_patch/
├─ <game>_chs.exe
├─ <text_archive>.dpm
├─ <extra_text_archive>.dpm
└─ README.txt
```

## Self Test

After packaging:

1. Copy the release files onto a clean current-version game body.
2. Launch the game from that clean body.
3. Enter formal dialogue.
4. Open save, load, log, config, and extra screens.
5. Verify font, wrapping, mojibake, and crash behavior.
6. Store QA screenshots in the project work folder, not in the release folder.

## Archive

Create a `.7z` or `.zip` from the release folder only. Do not archive the parent work folder.
