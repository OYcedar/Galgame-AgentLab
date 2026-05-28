# LiLiM / Le.Chocolat AOS Patch Workflow

Agents:

1. engine-detector
2. text-extractor
3. translator
4. reinsertor
5. font-fixer
6. packager
7. runtime-tester
8. release-builder

Core rules:

- extract `scr.aos` from the current body;
- export player text as SExtractor JSON;
- filter out commands such as `^gsb(VAR)`, `%route`, `^go(TITLE)`, and comments;
- normalize GBK-sensitive Shift-JIS symbols;
- keep standalone time lines and visible halfwidth symbols engine-safe;
- rebuild the AOS archive and test start/load/OP/extra menus.
