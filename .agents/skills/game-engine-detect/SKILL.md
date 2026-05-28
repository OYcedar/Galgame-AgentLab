---
name: game-engine-detect
description: 在授权本地化项目中识别非 RPG Windows 游戏引擎，再决定提取、回填、封包和测试方式。
---

# 游戏引擎识别

在提取、翻译、回填或制作补丁前，必须先识别引擎。

## 检查清单

1. 列出顶层文件、可执行文件、DLL 和封包扩展名。
2. 检查封包签名和常见脚本扩展名。
3. 判断 exe 是加载外部封包，还是内嵌资源。
4. 旧补丁只能作为参考，不作为新版本文件来源。
5. 生成 `work/engine_report.md`。

## 支持画像

### Kirikiri / KAG / XP3

证据：

- `*.xp3`
- `*.ks`
- `*.tjs`
- `startup.tjs`
- KAG 或 TJS 运行时报错

推荐 Skill：`kirikiri-z-localization`。

### LiLiM / Le.Chocolat AOS

证据：

- `*.aos`
- 解包后的 `*.scr`
- `^go(...)`、`^gsb(...)`、`var`、`fnt(...)`、`wnd(...)` 等命令
- GARbro 或自定义工具识别到 AOS 资源

推荐 Skill：`lilim-aos-localization`。

### Bruns / EENC / EENZ

证据：

- 文件头为 `EENC` 或 `EENZ`
- `ams.cfg`
- `scene/*.bso`
- 解密后脚本包含 `(a3:...)` 结构
- 运行时或文件中出现 `Bruns`

推荐 Skill：`bruns-eenz-localization`。

## 明确排除

- LiveMaker / LiveNovel。
- RPG Maker 工作流。
- DRM、授权校验、在线激活或反篡改绕过。

## 引擎报告

`work/engine_report.md` 应包含：

- 疑似引擎。
- 置信度。
- 证据文件。
- 需要解包的封包。
- 文本格式和可能编码。
- 旧补丁是否只能作为参考。
- 不能从旧版本混用的文件。
- 推荐的下一步 Skill 或 Workflow。
