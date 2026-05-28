---
name: vn-runtime-test
description: 自动化测试 Windows 视觉小说补丁，包括点击、Ctrl 跳过、分支、截图、闪退和卡死检测。
---

# VN 实机测试

回填或封包后，使用这个 Skill 测试真实 Windows 游戏窗口。

## 原则

- 每次运行前记录准确 exe 路径和工作目录。
- 测试当前本体或当前发布包，不误开其他同名游戏。
- 截图和报告保存到当前游戏的 `work` 目录。
- 启动、载入、跳过和菜单操作都要设置超时。
- 破坏性测试前备份 `save`、`savedata` 等用户存档目录。

## 建议自动化栈

Windows 下 Python 自动化可使用：

- `subprocess.Popen`
- `win32gui.EnumWindows`
- `win32api`
- `PIL.ImageGrab`
- 已安装且合适时使用 `pywinauto`

优先使用项目内已经可用的栈。脚本保留在项目或游戏工作目录内。

## 标准测试路径

1. 启动 exe。
2. 等待窗口出现。
3. 截图第一屏。
4. 到达标题或主菜单。
5. 开始新游戏，并等待足够长时间进入正式对白。
6. 如果有存档，载入 1 号槽。
7. 打开 Save、Load、Log、Config。
8. 存在 Extra / Gallery / Scene / Music 时也测试。
9. 控制时长地按住 Ctrl 或触发 Skip。
10. 项目需要分支覆盖时遍历选项。

## 分支测试

对于选项较多的游戏：

- 每个选项画面都截图。
- 给每条路径分配 path ID。
- 测到结局、回到标题、已知重复状态、闪退或超时为止。
- 记录路径和结果。

## 需要记录的问题

- 前台窗口不出现。
- 黑屏超时。
- 长时间 `Accessing...` 或载入画面。
- 对白、菜单、存读档或错误弹窗乱码。
- 文本溢出或换行错误。
- 字体 hook 没生效。
- 崩溃弹窗。
- 语法错误。
- Gallery 或 Extra 菜单闪退。
- Skip 在 OP、影片、时间卡附近卡死。

## 输出

推荐输出：

- `work/reports/runtime_qa_<date>.md`
- `work/reports/screenshots_<date>/`
- 闪退或卡死截图
- 实际使用的命令和 exe 路径
