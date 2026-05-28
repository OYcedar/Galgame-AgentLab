# HSP / DPM Patch Workflow

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

- extract DPM archives from the current body;
- include DLC archives when present;
- target GBK or GB18030 if the engine requires it;
- compare old patches for executable string/resource changes, but do not copy old full archives into a new body;
- rebuild DPM files with the current-version base.
