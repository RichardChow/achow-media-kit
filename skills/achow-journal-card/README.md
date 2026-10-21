# achow-journal-card

手帐笔记风（方格纸、胶带标签、彩色描边色块、硬阴影、划重点）的 3:4 中文数据卡片 Skill，可用于 Claude Code / Codex 等能读取 SKILL.md 的 Agent，也能单独用命令行跑。

![预览](examples/issue01.png)

## 安装
```bash
git clone https://github.com/RichardChow/achow-journal-card ~/.claude/skills/achow-journal-card && cd ~/.claude/skills/achow-journal-card && npm install
```

## 使用
1. 复制 `examples/issue01.json`，改成你的数据（字段说明见 SKILL.md）。
2. 渲染：`node scripts/render.mjs my.json out/my.png`
3. 打开 PNG 检查有没有溢出、小字、缺字。

在 Agent 里直接说：「用 achow-journal-card 把这些数据做成卡片」。

## 依赖
Node 18+、本机 Chrome/Chromium（自动探测，可用 `CHROME_PATH` 指定）、Noto CJK 字体。

## 致谢
视觉参考 [atian-create/knowledge-card-journal-skill](https://github.com/atian-create/knowledge-card-journal-skill)（MIT），详见 [CREDITS](CREDITS/README.md)。

## License
MIT © aChow_hz
