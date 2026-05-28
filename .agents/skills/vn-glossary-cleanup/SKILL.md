---
name: vn-glossary-cleanup
description: 清理游戏文本提取生成的术语表，输入通常为 output.json 和 output_detail.txt。
---

# VN 术语表清理

当文本提取生成 `output` 之类术语表目录时使用。

## 输入

- `output/output.json`
- `output/output_detail.txt`

## 保留

优先保留：

- 角色名
- 地名
- 组织名
- 作品专有名词
- 系统术语
- UI 术语
- 具有稳定含义的重复短语

## 删除

删除不适合作为术语的条目：

- 乱码
- 脚本命令
- 变量
- 资源 ID
- 纯标点
- 不稳定单字
- 分词错误碎片
- 只出现在命令或调试行里的字符串
- 对一致性帮助不大的泛用词

## 流程

1. 备份术语表文件。
2. 查看每个术语的明细来源。
3. 删除含义不明或不安全条目。
4. 保持 `output.json` 和 `output_detail.txt` 同步。
5. 写出清理报告。

## 项目脚本

需要自动化时，单游戏脚本放在：

```text
games/<game>/work/scripts/
```

运行前检查路径常量。
