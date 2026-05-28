---
name: kirikiri-z-localization
description: 制作授权 Kirikiri Z / KAG / XP3 中文补丁，包括 SExtractor JSON、脚本回填、字体处理、XP3 封包和实机 QA。
---

# Kirikiri Z / KAG / XP3 本地化

用于授权范围内的 Kirikiri Z、Kirikiri 2、KAG 和 XP3 视觉小说项目。

## 引擎证据

常见证据：

- `*.xp3` 封包。
- `.ks` KAG 剧本。
- `.tjs` 脚本。
- `startup.tjs`、`Config.tjs`、`first.ks`、`title.ks` 等启动脚本。
- 报错窗口提到 KAG 标签、TJS 或 `script`。

先检查当前游戏的封包优先级和补丁命名规则。

## 工作目录

推荐布局：

```text
games/<game>/
├─ original/
├─ work/
│  ├─ extract/
│  ├─ json/
│  ├─ patch_src/
│  ├─ reports/
│  └─ tmp/
├─ patched/
└─ release/
```

外部翻译 JSON 使用 SExtractor 格式：

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

文件路径、脚本位置、编码和回填元数据保存在单独内部映射里。

## 提取

1. 从当前游戏版本解出 XP3。
2. 识别剧本 `.ks` 和相关 `.tjs`。
3. 只导出玩家可见文本。
4. 对影响显示的 KAG 标签，保留在 `message` 中。
5. 脚本命令、标签、变量名、文件名、宏定义和非显示标签属性保留在内部映射中。

需要保护的重要标签和结构：

- `[r]`、`[lr]`、`[p]`、`[l]`、`[cm]`、`[ct]`
- `[ruby ...]`、`[font ...]`、`[style ...]`
- `[iscript]... [endscript]`
- 宏调用和 `*label` 等标签
- `storage=...` 等文件属性

如果文件包含大段 `[iscript]`，最安全的回填方式是恢复原始脚本块，只替换已经提取出的显示字符串。

## 翻译

- 默认翻译为简体中文。
- JSON 顺序和条数必须不变。
- 源文有 `name` 时译文也保留。
- 保留全部 KAG 标签和 ruby 标签数量。
- 翻译后按目标引擎规范化标点。
- 除非是名字、标题或有意保留术语，不应在可见文本中残留日文。

## 回填

1. 校验源 JSON、译文 JSON 和映射。
2. 只回填到当前版本解包脚本。
3. 尽量逐字节保留控制标签和脚本代码。
4. 按引擎实际行为选择输出编码。常见选择有 UTF-16 LE with BOM、CP932、UTF-8，但必须按作品确认。
5. 回填后重新解包或检查脚本，确认中文确实存在。

如果运行时报语法错误，优先检查报错文件和行号。常见原因：

- 译文破坏 KAG 标签。
- 标签属性中的引号或括号被翻译。
- `[iscript]` 块被误改。
- 在 KAG 期望单行命令的位置插入了换行。

## 字体处理

优先使用脚本层修改，再考虑二进制修改：

1. 找到游戏实际使用的字体族名。
2. 通过游戏、启动器或已有辅助 DLL 注册所需 `.ttf`。
3. 修改 KAG/TJS 字体声明为真实字体族名。
4. 如果 `face=user` 等动态占位无效，直接使用真实字体族名。
5. 在标题菜单和正式对白中同时测试。

字号增大时同步整理中文换行，并用实机截图确认显示效果。

## XP3 封包

1. 只封修改脚本、字体注册文件和必要补丁元数据。
2. 封包内容聚焦修改脚本、字体注册文件和必要补丁元数据。
3. 使用游戏实际会加载的补丁名，如 `patch_chs.xp3`、`patch.xp3` 或更高优先级编号补丁。
4. 重新解包最终 XP3，验证路径和编码。
5. 在干净的当前版本本体上测试补丁。

## 实机 QA

最低 QA：

- 首次启动。
- 标题页。
- Start 进入正式对白。
- Load 页和 Log 页。
- Config 和文本速度弹窗。
- Auto / Skip / Ctrl Skip。
- 选项分支。
- 存在 Extra、Gallery、Scene、Music 页时也要测试。
- 字体渲染和换行。
- 崩溃弹窗和语法错误弹窗。

截图和报告保存到 `games/<game>/work/reports` 或项目专用 QA 目录。
