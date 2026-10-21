# cardkit 视觉规范（深色科技风 + 亮色教程风）

源码：`scripts/cardkit.py`（`cover()`、`compare_card()`），示例：`examples/build_demo.py`。
两个函数都有 `theme='dark'|'light'`，默认 dark，深色输出跟加主题前逐像素一致。

## 选哪套
- 深色 `theme='dark'`：硬核技术、跑分、额度/价格实测、模型对比、命令行和 agent 操作。
- 亮色 `theme='light'`：教程、新手向、一步步搭建、清单、经验和职场随记这类软话题。
- 同一个系列（比如一篇长文的封面和配图）只用一套，不混搭。

## 尺寸
- 封面 `cover()`：2000×800（5:2），X 长文封面和单图帖都能用。左侧文字区 x=140 起，右侧终端窗口 x≈1200 到 W-110，上下各留 175。
- 数据卡 `compare_card()`：宽 1200，高按内容自动算（约 4:5 到 1:1）；需要固定高度就传 `H`。左右边距 80。

## 颜色
| 用途 | 值 |
|---|---|
| 背景渐变 | 左上 #06090C → 右下 #0B1D1F，叠一层 40px 点阵 #1C282C |
| 主强调（默认） | 薄荷绿 #3DFFB4（kicker、光标、终端光晕） |
| 标题 | #FFFFFF |
| 次要文字 | #C8D0D4 |
| 副标题 / 账号 / 脚注 | #7C868A |
| 面板 / 终端底 | #081115，标题栏 #141C1F |
| 品牌：Claude | #D97757 |
| 品牌：Codex/OpenAI | #4A90FF |

对比图里左右两方各用自己的品牌色，标题里的品牌名也染同色，"vs" 用灰色。

## 字体
- 中文和正文：Noto Sans CJK SC（ttc index 2），标题用 Bold，正文用 Regular。
- 代码、kicker：JetBrains Mono；字符串里的中文会自动换成 Noto CJK（`text_mixed`），不会出现豆腐块。
- 字号：封面标题 110–130，副标题 44，kicker 32，账号 28；数据卡标题 64，小节标题 48，标签和数值 30，备注和脚注 26。

## 版式
- 封面：kicker（`> ...` 等宽字体，强调色）→ 1 到 2 行大标题 → 一句副标题 → 左下角放账号。右边放一个带光晕的终端窗口，3 到 5 行内容，最后一行用 `$_` 画出闪烁光标。
- 数据卡：kicker → 标题 → 左右两个条件卡（品牌色描边加左侧色条）→ 若干小节，每个小节下面是若干横条 → 底部一条分隔线，左边脚注，右边账号。
- 横条只表示同一个指标（比如「占 5 小时额度」），一个小节里别混用不同单位。区间值用 `pct=(lo, hi)`，深色是下限、浅色是上限。

## Do
- 只写真实、能溯源的数字；文字里写不清的，在 `note` 里补一句原话。
- 一张图只讲一件事，每个小节最多 3 到 4 条横条。
- 脚注写清楚测试的局限，比如「个人实测，方法不严谨」。
- 出图后打开 PNG 看一遍：有没有豆腐块、有没有溢出、留白是否均匀。

## Don't
- 不用 emoji，不放外链和二维码。
- 不编数字、不画没有数据支撑的比例条。
- 每张图除了品牌色，最多再加一种强调色；不用纯黑 #000 或浅色背景（浅色请用 light 主题）。

## 亮色主题（theme='light'）
| 用途 | 常量 | 值 |
|---|---|---|
| 背景（纯色，无渐变无点阵） | `L_BG` | #F6F4EF 米白 |
| 主强调 | `L_ACCENT` | #FF5A1F 橙（标签胶囊、标题高亮词、服务器指示灯、光标） |
| 标题 / 描边 / 实心节点 | `L_INK` | #111111 |
| 副标题 / 标签 | `L_TEXT2` | #444444 |
| 底部技术栈 / 账号 / 脚注 | `L_MUTED` | #888888 |
| 服务器框 / 卡片 / 终端底 | `L_PANEL` | #FFFFFF |
| 横条空槽 | `L_TRACK` | #E8E4DA |
| 分隔线 | `L_RULE` | #DDD9CF |
| 品牌色 | `CLAUDE` / `CODEX` | 沿用 #D97757 / #4A90FF |

- 自动映射：亮色主题下，build 脚本里的 `WHITE→L_INK`、`TEXT2→L_TEXT2`、`MUTED/FAINT→L_MUTED`、`ACCENT→L_ACCENT`，同一份 build 脚本只改 `theme` 就能出两套。
- 封面版式（2000×800）：kicker 变成橙色描边胶囊（4px 描边、高 62，开头的 `> ` 自动去掉，Noto Bold 31）→ 间隔 59 → 标题（单行默认 168，两行默认 118，Noto Bold）→ 间隔 45 → 副标题 46 #444 → 左下 y≈702 一行 `footer=[...]` 技术栈，用「 · 」连接，#888 28 号；账号放右下（距右边 122）。整块文字以 y≈336 为中心垂直居中。
- 右侧插画 `illustration=`：`'servers'`（默认）是三台扁平服务器，304×92 圆角 20、5px 墨色描边，中间那台实心墨色，左侧橙色指示灯，右侧短横线；虚线连到三个节点：橙色实心、白底空心、墨色实心，半径 26。`'terminal'` 是扁平白色终端（5px 墨色描边，配 `term_lines`）。`None` 不画。
- 数据卡：米白底；kicker 橙色胶囊；条件卡白底、4px 墨色描边、内侧品牌色竖条；横条空槽 #E8E4DA，区间浅色段是品牌色和底色 45/55 混合；数值默认墨色，落在色条上时自动变白。
- 亮色主题不加光晕、不加渐变，靠粗描边和留白出层次。

## 用法
```python
import sys; sys.path.insert(0, 'scripts')
from cardkit import *
cover('out.png', [[('Codex 100刀', CODEX)], [('vs ', MUTED), ('Claude 20刀', CLAUDE)]],
      '副标题', kicker='> ...', term_lines=[('$ cmd', TEXT2), ('结果', ACCENT), ('$_', TEXT2)])
compare_card('card.png', [('A', CODEX), (' vs ', MUTED), ('B', CLAUDE)], '> kicker',
             sides=[{'name': 'A', 'color': CODEX, 'spec': ['...', '...']}, {...}],
             sections=[{'title': '...', 'subtitle': '...', 'rows': [{'side': 0, 'label': '...', 'value': '50%', 'pct': 50, 'note': '...'}]}],
             footnote='个人实测，方法不严谨')
# 亮色：同样的参数加 theme='light'；封面可加 footer 和 illustration
cover('out-light.png', [[('$5 ', ACCENT), ('自建代理', WHITE)]], '从注册到能用，新手一篇搞定',
      kicker='VPS 自建教程', footer=['Vultr', 'sing-box', 'VLESS + Reality'], theme='light')
```
亮色示例：`demo_light.py` → `demo-light-cover.png`、`demo-light-compare.png`。
