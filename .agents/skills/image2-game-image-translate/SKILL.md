---
name: image2-game-image-translate
description: Mandatory workflow for translating game images, UI textures, CG text, buttons, map labels, and image-based text using image2 only when image translation is needed.
---

# Game Image Translation

Use this skill when a localization task requires translating image-based text.

## Scope

This applies to:

- UI images
- menu images
- button images
- CG text
- map labels
- tutorial screenshots
- textures with visible text
- any player-visible text baked into an image

## Rule

Use `image2` for game image translation.

Do not use OCR-to-manual-redraw, alternate image translation tools, Photoshop automation, or hand-recreated textures unless the user explicitly overrides this rule in the current task.

## Workflow

1. Identify the source image.
2. Back up the original.
3. Translate with `image2`.
4. Save output under the current game's work folder.
5. Check dimensions, transparency, format, and file name.
6. Runtime-test that the game reads the translated image correctly.
7. Only then include it in the patch archive or release folder.
