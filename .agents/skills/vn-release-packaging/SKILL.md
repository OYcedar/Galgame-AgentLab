---
name: vn-release-packaging
description: 为非 RPG 视觉小说项目构建干净的中文补丁发布目录。
---

# VN 发布打包

准备面向玩家的中文补丁发布目录时使用。

## 打包前确认

打包前确认：

- 补丁游戏能从干净的当前版本本体启动。
- 如果包含发布 exe，该 exe 基于当前版本 exe。
- 脚本封包由当前版本文件重建。
- 必需字体和配置文件存在。
- `.ini` 和 readme 文件为 UTF-8。
- 不包含 `_work`、存档、截图、解包素材或临时工具。

## 只包含玩家需要的内容

常见发布内容：

- 中文显示需要时的补丁 exe。
- 修改后的脚本或文本封包。
- 必需时的字体启动器或辅助 DLL。
- 补丁所需字体文件。
- UTF-8 配置文件。
- 使用说明。

不要包含：

- 未修改的 CG 封包。
- 未修改的语音封包。
- 未修改的 BGM 封包。
- 未实际修改或不可分发的视频。
- 解包原始素材。
- 测试截图。
- 存档文件夹。
- 其他游戏版本的旧补丁文件。
- 临时分析文件。

## 通用布局

Kirikiri / XP3：

```text
<game>_CHS_patch/
├─ patch_chs.xp3
├─ fonts/
│  └─ <font>.ttf
└─ README.txt
```

LiLiM / AOS：

```text
<game>_CHS_patch/
├─ <game>_chs.exe
├─ <font_launcher>.exe
├─ <font_launcher>.ini
├─ <font>.ttf
└─ README.txt
```

Bruns / EENC / EENZ：

```text
<game>_CHS_patch/
├─ <game>_chs.exe
├─ ams.cfg
├─ scene/
│  └─ <patched>.bso
└─ README.txt
```

## 自测

打包后：

1. 把发布文件复制到干净的当前版本本体。
2. 从该本体启动游戏。
3. 进入正式对白。
4. 打开 Save、Load、Log、Config 和 Extra。
5. 检查字体、换行、乱码和闪退行为。
6. QA 截图保存在项目工作目录，不放进发布目录。

## 压缩

只从发布目录创建 `.7z` 或 `.zip`，不要压缩父级工作目录。
