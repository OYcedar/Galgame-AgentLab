# Kirikiri Z / KAG / XP3 补丁流程

参与 Agent：

1. `engine-detector`
2. `text-extractor`
3. `translator`
4. `reinsertor`
5. `font-fixer`
6. `packager`
7. `runtime-tester`
8. `release-builder`

核心规则：

- 从当前版本游戏本体解包 XP3。
- 识别 `.ks`、`.tjs`、字体文件和补丁加载顺序。
- 外部翻译文本导出为 SExtractor JSON。
- 保护 KAG 标签、TJS 代码、宏、标签名和文件名。
- 回填时只替换确认可见的文本，不改脚本控制逻辑。
- 封包名必须符合游戏实际加载规则，例如 `patch_chs.xp3`、`patch.xp3` 或更高优先级编号补丁。

字体规则：

- 优先修改 KAG/TJS 字体声明。
- 如果使用外部字体，必须确认真实字体族名。
- 字号或字体变更后要重测正式对白、日志页和选项页。

校验门槛：

- 游戏能首次启动。
- 标题、Start、Load、Config、Log、Extra 页面能打开。
- 没有 KAG/TJS 语法错误。
- 回填后重新解包 XP3，确认路径、编码和中文文本正确。
