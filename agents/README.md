# Agents

Agent 是项目里的角色定义，默认不绑定具体引擎。

具体引擎细节放在 Skill 中，执行顺序放在 Workflow 中。

## Agent 列表

- `engine-detector`：识别引擎并选择安全工具链。
- `text-extractor`：导出 SExtractor JSON，并生成内部回填映射。
- `translator`：用模型或外部流程翻译 SExtractor JSON。
- `reinsertor`：把译文写回脚本或封包。
- `font-fixer`：处理字体注册、真实字体族名、编码和换行。
- `packager`：重建封包或补丁文件。
- `runtime-tester`：运行真实游戏并记录回归问题。
- `release-builder`：创建干净的玩家发布目录和压缩包。
