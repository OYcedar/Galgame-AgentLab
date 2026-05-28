# Engine Detector Agent

Goal: identify the game engine before extraction or patching.

Responsibilities:

- inspect folder structure and file signatures;
- distinguish archive formats and script formats;
- decide which engine skill applies;
- stop if the target appears to require DRM, activation, or anti-tamper bypass;
- produce an `engine_report.md`.

Output should include:

- suspected engine;
- confidence level;
- evidence files;
- recommended tools;
- supported or unsupported status.

This project excludes LiveMaker / LiveNovel even if detected.
