# AGENTS.md

## 项目目的

本仓库用于授权范围内的 Windows Galgame 与视觉小说本地化工作流。

项目采用 Agent 模型：

- `agents/` 描述职责分工；
- `.agents/skills/` 描述引擎专用知识；
- `workflows/` 描述端到端流程。

## 范围

支持：

- Kirikiri Z / KAG / XP3
- LiLiM / Le.Chocolat AOS
- Bruns / EENC / EENZ
- 未知非 RPG VN 引擎分析
- SExtractor JSON 提取、翻译、回填、封包和实机 QA

## 搜索

来源 Windows 机器上 `rg` 可能不可用或被拒绝。优先使用 PowerShell 原生命令：

```powershell
Get-ChildItem -Recurse -File | Select-String -Pattern "text"
```

## 外部翻译格式

所有外部翻译 JSON 默认使用 SExtractor 格式：

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1"
  }
]
```

文件名、偏移、行号、命令上下文和回填元数据必须放在单独的 map 文件里。

## 编码

- JSON、报告、文档和配置默认使用 UTF-8。
- 日文原脚本常见编码是 CP932 / Shift-JIS。
- 老引擎中文补丁可能需要 GBK 或 GB18030。
- 旧引擎脚本按实机确认的目标编码写入中文。
- 回填前必须验证目标编码。

## 文件纪律

- 临时文件放在对应游戏工作目录。
- 单个游戏临时文件放在 `games/<game>/_work` 或该工作流指定的 `work` 目录。
- 通用脚本放在 `tools`。
- 引擎 skill 放在 `.agents/skills`。
- 提交内容以项目规则、脚本、文档、示例和测试为主。

## 图片翻译

游戏内图片文字使用项目指定的图片翻译流程。
