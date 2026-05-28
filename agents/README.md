# Agents

Agents are role definitions. They are engine-neutral by default.

Use skills for engine details, and workflows for sequencing.

## Agent List

- `engine-detector`: classify the engine and choose a safe toolchain.
- `text-extractor`: export text as SExtractor JSON plus an internal map.
- `translator`: translate SExtractor JSON with model or external workflow.
- `reinsertor`: write translations back into scripts or archives.
- `font-fixer`: handle font registration, real font family names, encoding, and wrapping.
- `packager`: rebuild archives or patch files.
- `runtime-tester`: run the actual game and capture regressions.
- `release-builder`: create clean player-facing patch folders and archives.
