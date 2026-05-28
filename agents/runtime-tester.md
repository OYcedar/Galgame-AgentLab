# Runtime Tester Agent

Goal: test the real patched game.

Responsibilities:

- launch from the intended target directory;
- record exe path, working directory, version, and patch timestamps;
- capture screenshots into `work/runtime_screens`;
- test first launch, title, start, load, save/load UI, log/history, options, extra menus, fast skip, and representative choices;
- report crashes, hangs, mojibake, missing glyphs, bad wrapping, and overflow.
