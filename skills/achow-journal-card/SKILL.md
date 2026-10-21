---
name: achow-journal-card
description: 生成「手帐笔记风（方格纸、胶带标签、彩色描边色块、硬阴影、划重点）」的 3:4 中文数据/知识卡片（1080x1440 PNG）。当用户要做小红书/X 图文卡片、后台数据复盘卡、学习笔记封面、单页数据总结卡，并希望用这种风格时使用。输入一个 JSON，输出 PNG。
---

# achow-journal-card

风格：手帐笔记风（方格纸、胶带标签、彩色描边色块、硬阴影、划重点）。尺寸固定 1080×1440（3:4），适合 X、小红书、视频号图文。

## 1. 填内容
复制 `examples/issue01.json` 改成你的数据。字段：
- `series` 系列名，`handle` 账号，`issue` 期号，`topic` 小标题，`tags` 标签数组（手帐风用）
- `title_line1` / `title_line2` 两行标题，每行 ≤ 8 个汉字
- `hero_label` / `hero_value` / `hero_unit` 主数字（如 曝光 / 19.2 / K），主数字 ≤ 5 个字符
- `stat1_*` / `stat2_*` 主数字旁的两个辅助数字
- `metrics` 恰好 4 项：`label` `value`，可选 `sub`+`sub_sep`（如 “/ 545”），`pct` 进度条百分比（毛玻璃风，0 = 不画），`emoji` `color`（手帐风）
- `footnote` 次要数据一行；`takeaway_prefix` + `takeaway_highlights` 组成结论，高亮词会上强调色，结论 ≤ 16 字
- 字段值可含简单 HTML（如 `&gt;`）。只用真实数据，不编数字。

## 2. 版式规则
- 一张卡只讲 1 个主数字 + 4 个次级指标 + 1 句结论；内容多就拆成多张，不要缩字号硬塞。
- 最小字号 24px（1080 宽画布），标题 ≥ 80px。
- 字体：Noto Sans CJK SC / Noto Serif CJK SC（本地字体，无需联网）。Linux 安装：`sudo apt install fonts-noto-cjk`；macOS 可装 Noto Sans/Serif SC 或接受系统回退。

## 3. 渲染
```bash
npm install            # 只装 playwright-core，不下载浏览器
node scripts/render.mjs examples/issue01.json out/issue01.png
```
脚本会依次找 `CHROME_PATH`、系统 Chrome/Chromium/Edge；都没有时执行 `npx playwright install chromium` 并改依赖为 `playwright`。

## 4. QA（每次必做）
渲染后**打开 PNG 用眼睛看**，逐条检查：
- [ ] 没有文字溢出画布、被裁切或挤成两行把卡片撑破
- [ ] 没有小于 24px 的字，手机上能读
- [ ] 中文无豆腐块/方框（缺字体就装 Noto CJK）
- [ ] 数字和原始数据逐个对得上
- [ ] 底部结论条与上方内容不重叠，留白均衡
有问题就缩短文字或拆卡，再重新渲染。
