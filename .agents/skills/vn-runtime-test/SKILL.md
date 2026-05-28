---
name: vn-runtime-test
description: Automate runtime QA for Windows visual novel patches with clicks, Ctrl skip, branching, screenshots, crash and hang detection.
---

# VN Runtime Test

Use this skill after reinsertion or packaging to test the real Windows game window.

## Principles

- Record the exact exe path and working directory before each run.
- Test the current body or current release package, not another same-named game elsewhere.
- Save screenshots and reports under the current game's `work` directory.
- Use timeouts for launch, loading, skip, and menu operations.
- Preserve user saves by backing up `save`, `savedata`, or similar folders before destructive tests.

## Suggested Automation Stack

On Windows, Python automation can use:

- `subprocess.Popen`
- `win32gui.EnumWindows`
- `win32api`
- `PIL.ImageGrab`
- `pywinauto` when installed and useful

Use whichever stack is already available in the project. Keep scripts project-local.

## Standard Test Path

1. Launch the exe.
2. Wait for the window.
3. Screenshot the first visible screen.
4. Reach the title or main menu.
5. Start a new game and wait long enough for formal dialogue.
6. Load slot 1 if available.
7. Open save, load, log, and config screens.
8. Test extra/gallery/scene/music screens when present.
9. Hold Ctrl or trigger skip for a controlled interval.
10. Traverse choices if the project needs branch coverage.

## Branch Testing

For choice-heavy games:

- screenshot each choice screen
- assign a path ID to each branch
- test until ending, title return, known repeated state, crash, or timeout
- record the path and outcome

## Issues To Record

- foreground window never appears
- black screen timeout
- long `Accessing...` or loading screen
- mojibake in dialogue, menus, save/load, or errors
- text overflow or broken wrapping
- font hook not applied
- crash dialogs
- syntax errors
- gallery or extra menu crashes
- skip hangs around OP/movie/time-card transitions

## Output

Recommended outputs:

- `work/reports/runtime_qa_<date>.md`
- `work/reports/screenshots_<date>/`
- crash or hang screenshots
- exact command and exe path used
