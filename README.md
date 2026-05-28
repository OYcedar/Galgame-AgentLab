# Galgame-AgentLab

Galgame-AgentLab 是一套面向授权范围内 Windows Galgame / 视觉小说本地化的 Agent 工作流项目。

它把汉化补丁制作拆成一组可协作的角色：

- 引擎识别
- 文本提取
- SExtractor JSON 翻译
- 译文回填
- 字体与编码修复
- 封包与补丁整理
- 实机 QA
- 发布包制作

本项目只处理非 RPG 的 Galgame / 视觉小说引擎。LiveMaker / LiveNovel、RPG Maker、HSP / DPM 不属于本项目范围。

## 已支持的引擎

当前支持：

- Kirikiri Z / KAG / XP3
- LiLiM / Le.Chocolat AOS
- Bruns / EENC / EENZ
- 未知非 RPG VN 引擎初筛

明确排除：

- LiveMaker / LiveNovel
- RPG Maker 工作流
- HSP / DPM
- DRM、授权校验、在线激活、反篡改绕过

## 项目模型

Agent 表示一种职责，Skill 表示某类引擎的专用知识，Workflow 表示端到端流程。

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
  bruns-eenz-localization/
  kirikiri-z-localization/
  lilim-aos-localization/
  vn-sextractor-json/
  vn-runtime-test/
  vn-release-packaging/
```

## 默认文本格式

外部翻译交付统一使用 SExtractor JSON：

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

回填所需的文件名、偏移、行号、命令上下文等元数据必须保存在单独的内部映射文件中。

## 工具

通用工具放在 `tools/`。

`tools/att-vn-translator` 是一个 ATT-MZ 风格的 VN 翻译适配器：复用模型配置、批量翻译、断点续跑和校验思路，但输入输出使用 SExtractor JSON。

常用翻译命令：

```powershell
python tools/att-vn-translator/translate_sextractor.py --source work/json/source_sextractor.json --output work/json/source_sextractor_trans.json --setting setting.toml
python tools/att-vn-translator/validate_sextractor_translation.py --source work/json/source_sextractor.json --translation work/json/source_sextractor_trans.json
```

Kirikiri XP3 常用封包命令：

```powershell
& tools/att-vn-translator/pack_kirikiri_xp3.ps1 -SourceDir work/patch_src -OutputXp3 work/dist/patch_chs.xp3 -GarbroDir tools/GARbro -Scheme "your diary + [English]"
```

## 仓库规则

- 只处理用户拥有或获授权本地化的游戏与素材。
- 不绕过 DRM、激活、授权校验或反篡改保护。
- 不分发原始版权素材，除非补丁流程确实需要修改后的封包且分发许可允许。
- 不提交游戏本体、存档、解包 CG/语音/视频、API Key 或生成的发布压缩包。
- 单个游戏的临时文件必须放在该游戏的 `work` 目录下。

## 许可证

当前尚未选择许可证。若要公开分发，请先补充合适的许可证。
