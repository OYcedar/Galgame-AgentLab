---
name: vn-sextractor-json
description: 为所有非 RPG 游戏项目提取并校验 SExtractor 格式的外部翻译 JSON。
---

# SExtractor JSON

除非项目明确要求其他格式，所有外部翻译交付文件都应使用 SExtractor JSON。

## 格式

```json
[
  {
    "message": "Text0"
  },
  {
    "name": "Name1",
    "message": "Text1。"
  },
  {
    "name": "MaybeName2",
    "message": "「Text2」"
  }
]
```

规则：

- JSON 使用 UTF-8。
- 顶层值是数组。
- 每条都有 `message`。
- 只有存在说话人时才写 `name`。
- 顺序与原脚本出现顺序一致。
- 回填元数据放在单独映射文件中。

## 提取

只导出玩家可见文本：

- 对白
- 说话人名字
- 选项
- 菜单文本
- 系统提示
- 可见场景标题

以下脚本结构类内容保存在内部映射中：

- 标签
- 变量名
- 调试参数
- 命令名
- 文件名
- 资源 ID
- 注释
- 只用于脚本控制的行

已知非对白示例：

```text
^gsb(VAR)
%route
^go(TITLE)
var %temp
```

## 校验

回填前检查：

- 源文和译文都能作为 JSON 解析。
- 顶层值都是数组。
- 条数一致。
- 每条都有 `message`。
- 除非有意修改，`name` 出现情况与源文一致。
- 控制标签和占位符被保留。
- `message` 能编码到目标引擎编码。
- 空译文被报告。
- 明显源语言残留被报告供复核。
- 人称、敬称和角色称呼经过 `vn-address-audit` 复核。

## 命名

推荐文件名：

- 源文：`<game>_sextractor.json`
- 译文：`<game>_sextractor_trans.json`
- 内部映射：`<game>_sextractor_map.json`
- 校验报告：`<game>_sextractor_validation.json`

## 回填前清理

根据引擎行为规范化：

- ASCII 标点
- 可见正文中的半角英文和数字
- 引号：中文译文外层统一使用 `「」`，嵌套引号、作品名或原文已有强调层级使用 `『』`；不要混用 `“”`、`‘’`、`｢｣`、`《》`
- 省略号和波浪线
- 心形、音符、汗滴等特殊符号
- 固定宽度对白换行
