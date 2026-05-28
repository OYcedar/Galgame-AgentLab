# Bruns / EENC / EENZ 补丁流程

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

- 编辑前先确认封包类型是 `EENC` 或 `EENZ`。
- 从当前版本本体解出 `ams.cfg` 和 `scene/*.bso`，旧补丁只能作为参考。
- 外部翻译文本导出为 SExtractor JSON，回填映射单独保存。
- 中文回填默认使用 GB18030，除非实机证明该作品需要其他编码。
- Bruns ruby 标记如 `&RA...&RS...&RT` 默认扁平化为正文，除非已经确认中文 ruby 渲染安全。
- 保留 `voice` 配置和语音播放调用。
- 如果 `[WARN] VOICE制御は未対応です(%d)` 阻塞启动，优先用最小 exe 补丁降级调试警告，并保留语音播放。
- 不发布未经过实机验证的外部字体启动器。
- 发布包只包含修改后的 exe、配置、脚本封包、必要字体和 README。

校验门槛：

- 源 JSON 与译文 JSON 都能解析，条数和顺序一致。
- 修改后的 `*.bso` 能重新解密，并能看到预期中文。
- `ams.cfg` 能重新解密，配置结构有效。
- 首次启动能进入标题菜单，没有阻塞型调试警告。
- Start 能进入正式对白。
- 语音播放没有被刻意关闭。
- 发布目录不包含 `_work`、存档、截图、解密脚本或未修改的大体积媒体封包。
