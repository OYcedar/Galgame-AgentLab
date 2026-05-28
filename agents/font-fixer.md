# Font Fixer Agent

Goal: make Chinese text render correctly in the target engine.

Responsibilities:

- identify the actual font path used by the engine;
- identify real font family names, not just file names;
- patch script font tags or engine config where appropriate;
- handle GBK / GB18030 / Shift-JIS symbol issues;
- test formal dialogue, history/log, menus, save/load, and confirmation dialogs.

Known lesson:

- Some Kirikiri/KAG games ignore dynamic `user` font aliases in formal dialogue. For those, register the external font and write the real family name directly into KAG/TJS.
