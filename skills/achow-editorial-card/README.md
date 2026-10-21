# achow-editorial-card

杂志风（暖灰纸底、宋体大标题、橙色点缀、细线网格、黑色结论条）的 3:4 中文数据卡片 Skill，可用于 Claude Code / Codex 等能读取 SKILL.md 的 Agent，也能单独用命令行跑。

![预览](examples/issue01.png)

## 安装
```bash
git clone https://github.com/RichardChow/achow-editorial-card ~/.claude/skills/achow-editorial-card && cd ~/.claude/skills/achow-editorial-card && npm install
```

## 使用
1. 复制 `examples/issue01.json`，改成你的数据（字段说明见 SKILL.md）。
2. 渲染：`node scripts/render.mjs my.json out/my.png`
3. 打开 PNG 检查有没有溢出、小字、缺字。

在 Agent 里直接说：「用 achow-editorial-card 把这些数据做成卡片」。

## 依赖
Node 18+、本机 Chrome/Chromium（自动探测，可用 `CHROME_PATH` 指定）、Noto CJK 字体。

## 致谢
视觉参考 [FoundDream/editorial-card-generator-skill](https://github.com/FoundDream/editorial-card-generator-skill)（MIT），详见 [CREDITS](CREDITS/README.md)。

## License
MIT © aChow_hz
