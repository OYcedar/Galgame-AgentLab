# Kirikiri Z / KAG / XP3 Patch Workflow

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

- start from the current game archive;
- use SExtractor JSON for external translation;
- keep KAG tags such as `[r]`, `[lr]`, `[phr]`, `[ruby ...]`, `[font ...]`;
- restore `.ks` files containing `[iscript]` unless targeted edits are proven safe;
- re-extract the built XP3 and inspect the changed scripts.

Font note:

Some Kirikiri/KAG games need static real family names in scripts. If dynamic font aliases fail, register the font externally and write the actual family name into KAG/TJS.
