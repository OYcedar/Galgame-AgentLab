---
name: bruns-eenz-localization
description: 本地化 Bruns/BGI-like EENC/EENZ 视觉小说，包括 ams.cfg、scene BSO 脚本、SExtractor JSON、GB18030 回填、exe UI 字符串、VOICE 警告处理和实机 QA。
---

# Bruns / EENC / EENZ 本地化

用于授权范围内、使用 Bruns 风格加密资源和 Lisp-like `a3:` 脚本的视觉小说。

## 引擎证据

常见证据：

- 文件头为 `EENC` 或 `EENZ` 的加密文件。
- `ams.cfg` 引擎配置。
- `scene/*.bso` 剧本脚本。
- 解密脚本包含 `(a3:define-set ...)`、`(a3:call-user-func ...)`、`(a3:send-string ...)` 等结构。
- 运行标题或文件中出现 `Bruns`。

该引擎家族的流程形态可能类似 BGI/Ethornell；处理时以当前文件签名和本项目工具为准。

## 工作目录

推荐布局：

```text
games/<game>/
├─ original/
├─ work/
│  ├─ extract/
│  │  └─ scene_decrypted/
│  ├─ json/
│  ├─ patch_scene_decrypted/
│  ├─ patch_scene/
│  ├─ reports/
│  └─ tmp/
├─ patched/
└─ release/
```

一次性二进制副本、解密配置、截图和测试脚本都应放在当前游戏的 `work` 目录内。

## EEN 文件

已知行为：

- `EENC` 和 `EENZ` 是加密包装。
- `EENZ` 载荷可能还经过压缩。
- `ams.cfg`、`scene/*.bso` 和部分 `parts/*.png` 可能被包装。

流程：

1. 备份原始加密文件。
2. 解密 `ams.cfg` 和目标 `scene/*.bso`。
3. 只编辑解密后的工作副本。
4. 把变更文件重新加密回相同路径和文件名。
5. 重新解密最终产物，确认能看到预期中文。

## 文本提取

外部翻译交付必须使用 SExtractor JSON：

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

文件名、脚本偏移、调用上下文和原始字节范围保存在内部映射文件中。

只提取剧本和菜单/系统中的玩家可见文本。脚本结构类内容留在内部映射中：

- `a3:` 命令。
- 数字资源 ID。
- `(a3:idref-word ...)` 等变量引用。
- 文件路径和资源名。
- 调试注释。

## 翻译与编码

- 默认翻译为简体中文。
- 该引擎回填中文脚本时 GB18030 通常较安全，但仍需按作品验证。
- JSON、报告和说明保持 UTF-8。
- 替换字符串时保留命令结构和换行。
- 每条译文都要确认能编码到目标脚本编码。

## Ruby 与特殊文本

Bruns 脚本可能包含 ruby 标记：

```text
&RA<base>&RS<ruby>&RT
```

中文补丁优先把 ruby 扁平化为正文，除非已经实机确认中文 ruby 渲染安全。这样可以避免基线上的细小残字和日志显示破坏。

回填后扫描译文 JSON 和解密脚本中的 `&RA`、`&RS`、`&RT`，除非项目有意保留 ruby。

## Exe 工作

允许的 exe 修改仅限显示和本地化兼容：

- 窗口标题字符串。
- 系统/日志标签。
- 阻塞游玩的调试警告行为。

### VOICE 警告

有些 Bruns 构建会显示阻塞型调试警告：

```text
[WARN] VOICE制御は未対応です(%d)
```

处理警告时保留 `voice` 配置和语音播放调用。

如果实机确认这只是调试警告，且语音播放必须保留，优先做最小 exe 补丁，把日志等级字符串从 `WARN ` 降级为等长非阻塞等级，例如 `TRACE`。保留 `VOICE...` 消息和全部脚本语音调用。

必须测试：

- 首次启动。
- 标题菜单。
- 进入正式对白。
- 至少一条可用语音。

## 字体处理

字体处理要保守。

- 优先使用 `ams.cfg` 中已验证可用的系统字体。
- 不发布未经实机证明有效的字体注册启动器。
- 如果用户要求本地 `.ttf`，先确认真实 Windows 字体族名，再确认正式对白截图确实变化。
- 如果字体实验失败或没有改善显示，应还原启动器、`.ini`、用户字体注册和发布文件。

## 实机 QA

最低 QA：

- 首次启动没有阻塞型调试警告。
- 标题菜单和选项菜单。
- Start 进入正式对白。
- 日志/回想。
- 存读档页。
- Ctrl Skip 或 Auto。
- 如果存在 Scene Replay / CG / Gallery 页面，也要测试。
- 警告处理后语音播放仍然有效。

截图保存到 `games/<game>/work/reports`。

## 发布

只发布玩家需要的文件：

- 必要时的补丁 exe。
- 补丁 `ams.cfg`。
- 补丁 `scene/*.bso`。
- 必要 README。

发布目录只包含上方列出的玩家文件，工作产物保存在 `work`：

- `_work`。
- 存档。
- 解密脚本。
- 调试截图。
- 未修改的 CG、语音、BGM 或视频封包。
- QA 过程中的字体实验文件。
