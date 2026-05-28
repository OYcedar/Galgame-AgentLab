# Galgame-AgentLab

Galgame-AgentLab is an agent-oriented workflow project for authorized Windows visual novel localization.

It organizes translation patch work as cooperating agents:

- engine detection
- text extraction
- SExtractor JSON translation
- reinsertion
- font and encoding fixes
- archive packaging
- runtime QA
- release building

The project is designed for non-RPG Galgame / visual novel engines. LiveMaker / LiveNovel is intentionally out of scope.

## Supported Engine Profiles

Current profiles:

- Kirikiri Z / KAG / XP3
- LiLiM / Le.Chocolat AOS
- HSP / DPM
- generic unknown VN engine detection

Explicitly excluded:

- LiveMaker / LiveNovel
- RPG Maker workflows
- DRM, license checks, online activation, anti-tamper bypass

## Project Model

Agent = a role that does one kind of work.

Skill = engine-specific knowledge and constraints.

Workflow = a sequence of agents plus one or more skills.

```text
agents/
  engine-detector.md
  text-extractor.md
  translator.md
  reinsertor.md
  font-fixer.md
  packager.md
  runtime-tester.md
  release-builder.md

.agents/skills/
  game-engine-detect/
  kirikiri-z-localization/
  lilim-aos-localization/
  hsp-dpm-localization/
  vn-sextractor-json/
  vn-runtime-test/
  vn-release-packaging/
```

## Default Text Format

External translation handoff uses SExtractor JSON:

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1。"
  }
]
```

Metadata for reinsertion belongs in a separate internal map file.

## Tooling

Reusable tools live in `tools/`.

The current `tools/att-vn-translator` adapter uses ATT-MZ-style model configuration and batch translation ideas, but reads and writes SExtractor JSON for visual novels.

Typical translation commands:

```powershell
python tools/att-vn-translator/translate_sextractor.py --source work/json/source_sextractor.json --output work/json/source_sextractor_trans.json --setting setting.toml
python tools/att-vn-translator/validate_sextractor_translation.py --source work/json/source_sextractor.json --translation work/json/source_sextractor_trans.json
```

Typical Kirikiri XP3 packing command:

```powershell
& tools/att-vn-translator/pack_kirikiri_xp3.ps1 -SourceDir work/patch_src -OutputXp3 work/dist/patch_chs.xp3 -GarbroDir tools/GARbro -Scheme "your diary + [English]"
```

## Repository Rules

- Work only on games and assets the user owns or is authorized to localize.
- Do not bypass DRM, activation, license checks, or anti-tamper protections.
- Do not redistribute original game assets unless the patch workflow explicitly requires a modified archive and distribution is permitted.
- Do not commit game bodies, save data, extracted CG/audio/video assets, API keys, or generated release archives.
- Keep per-game temporary files under that game's `work` folder.

## License

No license is selected yet. Add one before public distribution if needed.
