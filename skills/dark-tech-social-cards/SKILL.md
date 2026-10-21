---
name: dark-tech-social-cards
description: 给 X/社交平台帖子做封面或数据对比图时使用。两套主题：深色科技风（深青渐变+薄荷绿+发光终端）和亮色教程风（奶油底+橙色）。产出 2000x800（5:2）封面和 1200 宽的 A vs B 柱状对比卡。Python + Pillow。
---

# 封面 / 数据对比卡（深色 + 亮色）

工具：`scripts/cardkit.py`（`cover()`、`compare_card()`，都接受 `theme='dark'|'light'`，默认 dark）。完整视觉规范见 `STYLE.md`，示例见 `examples/build_demo.py`。

依赖：Python 3.9+、`pip install pillow numpy`、Noto Sans CJK 字体（Linux `apt install fonts-noto-cjk`），可选 JetBrains Mono。字体路径可用环境变量 `CARDKIT_CJK_BOLD` / `CARDKIT_CJK_REGULAR` / `CARDKIT_MONO` 覆盖。

## 选主题
- 深色（#06090C→#0B1D1F 渐变，薄荷绿 #3DFFB4，发光终端）：技术、跑分、额度实测、模型对比。
- 亮色（奶油 #F6F4EF，橙 #FF5A1F，墨色 #111111，白色面板，服务器节点插画）：教程、新手向、软话题。
- 一个系列只用一套。品牌色两套都固定：Claude #D97757，Codex/OpenAI #4A90FF。

## 步骤
1. 先读 `STYLE.md` 的尺寸、配色、字体和禁忌。
2. 只用真实、有出处的数字，不编数据、不画没有数据的柱子；两个来源冲突先问清楚。
3. 新建 `<日期>_<主题>/build.py`，`sys.path.insert(0, '<本 skill 目录>/scripts')` 后 `from cardkit import *`。
4. 封面：`cover()` 2000x800。kicker、1-2 行标题（品牌词用品牌色，vs 用灰色）、一行副标题、`handle='@你的账号'`。深色：右侧 3-5 行终端，写真实数值，以 `$_` 结尾。亮色：`footer=[...]` 技术栈行，`illustration='servers'|'terminal'|None`。
5. 数据卡：`compare_card()` 宽 1200。两张条件卡；每个 section 内的柱子共用同一指标；区间用 `pct=(lo,hi)`；脚注写清测试局限。
6. 渲染后逐张打开 PNG，检查缺字、溢出、间距。
7. 不用 emoji、不放外链和二维码，品牌色之外最多一个强调色。
