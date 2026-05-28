# LiLiM / Le.Chocolat AOS 补丁流程

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

- 先确认脚本封包是 AOS 系列，例如 `scr.aos`。
- 文本提取聚焦可见对白、菜单、选项和系统文字，脚本命令、变量、跳转标签和注释保存在内部映射中。
- 外部翻译文本导出为 SExtractor JSON。
- 中文回填通常需要 GBK 或 GB18030，必须实机验证。
- 重点检查 Shift-JIS 残留符号、半角英文数字、时间文本、存档摘要和日志页面。
- 如果 exe 是 EVB 或类似封装，只能基于当前版本 exe 做显示兼容修改。
- 新补丁基于当前版本本体重建，旧补丁作为风格参考。

校验门槛：

- `scr.aos` 能重新封包并被当前 exe 加载。
- Start 正式流程无乱码。
- Load No.01、日志、存档页和 CG/Scene/Music 菜单均通过。
- 字号变更后自动换行没有溢出。
