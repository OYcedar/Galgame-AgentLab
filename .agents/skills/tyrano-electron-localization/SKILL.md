---
name: tyrano-electron-localization
description: Localize TyranoScript / TyranoBuilder games packaged with Electron or NW.js, including scenario KS extraction, SExtractor JSON translation, source-aware quote and address QA, Electron HDR fixes, runtime testing, and release packaging.
---

# TyranoScript / Electron 本地化流程

适用于类似 `夏の照明` 的 TyranoScript / TyranoBuilder 游戏，常见结构是 `resources/app/main.js`、`resources/app/package.json`、`resources/app/data/scenario/*.ks`、`tyrano/`。

## 引擎识别

证据：

- `resources/app/package.json` 的 `main` 指向 `main.js`。
- `resources/app/main.js` 创建 `BrowserWindow` 或 NW.js 窗口。
- `resources/app/data/scenario/*.ks` 是 Tyrano/KAG 风格脚本。
- `resources/app/data/system/Config.tjs` 存在 `System.title`、`userFace` 等配置。
- `tyrano/`、`tyrano/libs.js`、`tyrano/plugins/kag/` 等目录存在。

不要把它按 Kirikiri XP3 处理；`.ks` 相似但封包、启动器和回填方式不同。

## 文本提取

1. 基准目录使用当前游戏本体，例如 `game/<游戏名>/resources/app`。
2. 从 `data/scenario/*.ks` 提取玩家可见文本，导出 SExtractor JSON。
3. map 文件保存脚本路径、行号、命令上下文和字段位置；不要交给翻译方。
4. 提取范围通常包括：
   - 纯对白行。
   - `#说话人` 行。
   - 选项文本。
   - 可见系统提示。
5. 不要提取：
   - 标签行。
   - `[jump]`、`[bg]`、`[chara_show]` 等命令属性。
   - 文件名、资源 ID、变量表达式。
   - 注释和调试行。

外部翻译文件仍使用 SExtractor JSON：

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

## 译后校对

这些处理只在翻译完成后执行，不作为翻译前全局替换：

- 人称与称呼校对：对照源文中的 `さん`、`ちゃん`、`くん`、`先輩`、`先生`、亲属称谓和角色关系，清理模型生成的 `桑`、`酱`、`君`、错误的 `阿姨/妈妈/老师/前辈/您`。
- 引号校对：逐条查看源文符号体系并对齐译文。源文外层是 `「」` 时译文保留 `「」`；源文使用或嵌套 `『』` 时译文对应保留 `『』`；清理模型生成的 `“”`、`‘’`、`｢｣`、`《》`。
- 标点校对：省略号、波浪线、括号、全半角标点要参考源文和实机显示，不做无条件替换。
- 保留 Tyrano 标签和控制符，尤其是 `[r]`、`[p]`、`[l]`、`[ruby]`、`[font]`、`[style]`。

## 回填

1. 回填前备份 `resources/app/data/scenario` 到 `_work/backup/scenario_original`。
2. 按 map 写回 `.ks`，保持原脚本结构和换行。
3. 修改窗口标题时同步检查：
   - `resources/app/package.json` 的 `window.title`。
   - `resources/app/data/system/Config.tjs` 的 `;System.title`。
4. 字体优先通过 `Config.tjs` 的 `;userFace` 指定系统字体，例如 `Microsoft YaHei`；不要为了字体问题先改 exe。

## HDR / 色彩修复

Electron 版在 HDR 显示器上可能发灰、过曝或颜色异常。优先在 `resources/app/main.js` 的 `app.on('ready')` 之前加入 Chromium 参数：

```js
app.commandLine.appendSwitch('force-color-profile', 'srgb');
app.commandLine.appendSwitch('force-raster-color-profile', 'srgb');
app.commandLine.appendSwitch('disable-features', 'UseHDRTransferFunction,EnableExternalDisplayHDR10Mode');
```

操作要求：

- 修改前把 `main.js` 备份到当前游戏 `_work/backup/hdr_fix`。
- 插入位置必须早于 `BrowserWindow` 创建。
- 修改后运行 `node --check resources/app/main.js`。
- HDR 修复文件要进入发布包，否则玩家覆盖后仍是旧启动器。

## 实机测试

至少测试：

- 启动到标题页。
- 点击 Start 后进入第一句正文。
- Load 页面和 No.01 存档。
- Log / Save / Config 菜单。
- 文本是否中文、无乱码、无明显溢出。
- HDR 修复后画面没有异常发灰或过曝。

截图保存到当前游戏 `_work/reports/runtime_screens` 或 `_work/ui_tests`。

## 发布

发布包通常只包含：

- `resources/app/main.js`，如果做过 HDR 或启动修复。
- `resources/app/package.json`，如果修改了窗口标题。
- `resources/app/data/system/Config.tjs`，如果修改了标题或字体。
- 修改过的 `resources/app/data/scenario/*.ks`。
- `README.txt`。

不要发布 `node_modules`、CG、BGM、语音、`save`、`_work` 或未修改的大体积素材。

发布前验证：

- 译文 JSON 条数一致且硬错误为 0。
- `node --check main.js` 通过。
- 压缩包 `7z t` 通过。
- 实机启动通过。
