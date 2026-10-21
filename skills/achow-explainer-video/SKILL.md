---
name: achow-explainer-video
description: 知识讲解类视频。把一个后台/仪表盘/产品页面用模拟数据重建成 3D 倾斜页面，镜头一镜到底依次推到每个指标，高亮+点击，配卡通主讲人画中画、中文配音、字幕、BGM 闪避和音效，输出 1080x1920 竖版讲解视频。适用于"X 数据后台讲解""某工具界面逐项讲解"等知识类短视频。
---

# 知识讲解类视频（achow-explainer-video）

一份 `script.json`（每段一句讲解 + 要推到的元素）+ 一份 `page.html`（用模拟数据重建的页面）→ 一条 1080×1920、30fps、一镜到底的讲解视频。

## 原始需求（不要丢）
1. **重建页面，不用截图**：用 HTML 按真实后台的布局重做一页，所有数字都是**模拟数据**，页面上标 `simulated data`，讲稿里也说一句"数字是模拟的"。不要把用户真实数据或真实帖子文字放进去。
2. **3D 倾斜页面 + 一镜到底**：页面整体做透视倾斜，镜头在同一张页面上平移/推拉到下一个指标，过渡约 1s、中间轻微拉远，**不硬切**。
3. **逐项讲解**：每段 = 顶部标签（`> 01 曝光 Impressions` + 闪烁光标）+ 鼠标移入点击（波纹）+ 赤陶色高亮框 + 一句大白话解释。
4. **主讲人画中画**：左下角固定卡通形象，嘴型跟随配音。
5. **配音 + 字幕**：edge-tts 中文配音，字幕按标点切块、按字数分配时长。
6. **BGM + 音效**：BGM 全程连续，配音时自动闪避（约降到 40%）；段落切换 whoosh、点击 click、高亮 ding。
7. **开头概览、结尾总结**：开头一个全景镜头说"这一页回答什么问题"，结尾一句可执行结论 + 下期预告。

## 风格（用户已确认，默认就用）
- **不用渐变背景**。Claude Code / Anthropic 风：暖米白纯色底 `#F3EEE3` + 极淡纸纹；页面 `#FAF8F3`，1px 细线框 `#DDD5C6`，几乎无阴影。
- 强调色只用**低饱和赤陶 `#D97757`**，只点缀（高亮框、最近几根柱、光标、`>` 提示符）。**不要大面积橙色**（用户否过亮橙）。
- 字体：标题/字幕 Noto Serif CJK SC；数字/标签 JetBrains Mono（备选 DejaVu Sans Mono）；正文 Noto Sans CJK SC。
- 终端感细节：页面顶栏 `● ● ●  ~/x-analytics — claude`、`>` 提示符、闪烁光标块、`//` 系列名。
- 去掉大光晕/毛玻璃/强模糊。运动模糊最多 0.8px，最终版直接不用。

## 可选项（先问用户，没说就用默认）
| 项 | 选项 | 默认 |
|---|---|---|
| 配音 `voice` | zh-CN-YunxiNeural 云希（年轻男声）/ YunjianNeural 云健（浑厚）/ YunyangNeural 云扬（播音腔）/ YunxiaNeural 云夏（少年）/ XiaoxiaoNeural 晓晓（女声）/ XiaoyiNeural 晓伊（活泼女声） | 云希，`rate: +12%` |
| 主讲人 `presenter` | `A` 3D 卡通（泡泡玛特/皮克斯感）/ `B` / `C`，或自己的目录（含 `avatar.png` 张嘴、`avatar_closed.png` 闭嘴） | `A` |
| 署名 `name` + `tagline` | 例：`Engineer × AI 工具 × 创作` | 必填，别写城市等隐私 |
| 系列名 `series` | 例：`新号做 X 的学习笔记 · 01` | 必填 |
| 字幕强调词 `em` | `词1|词2`，用赤陶色标出 | — |

试听/预览：`assets/voices/*.mp3`，`assets/presenters/compare.jpg`。
更自然的声音需要 ElevenLabs / 火山引擎 / 克隆本人声音，这个 skill 不包含。

## 目录
```
templates/
  template.html   引擎：样式、镜头、标签、高亮、光标、字幕、嘴型（占位符 {{PAGE}} {{SERIES}} {{NAME}} {{TAGLINE}} /*{{CSS}}*/ /*{{INIT}}*/）
  audio.py        配音拼接、停顿压缩、字幕切分、嘴型序列、BGM 合成与闪避、音效 → mix.wav + timing.json
  cap.mjs         playwright-core 逐帧截图 + 每帧字幕/头像重叠检测
  build.py        一键：TTS → 音频 → 合成 html → 并行截帧 → 30fps 编码 → 检查 → 联系表
assets/presenters/{A,B,C}/  assets/voices/
examples/01-overview/  examples/02-audience/   （完整可跑的一期）
```

## 一期视频的输入
`<issue>/config.json`
```json
{"series":"新号做 X 的学习笔记 · 02","name":"YourName","tagline":"Engineer × AI 工具 × 创作",
 "voice":"zh-CN-YunxiNeural","rate":"+12%","presenter":"A","em":"受众|活跃时段","out":"./out/02.mp4"}
```
`<issue>/script.json`：每段 `[id, 中文标签, 英文标签, 讲解词, 目标元素id 或 null, 推近倍数]`。
- 第一段与最后一段目标为 `null` = 全景。
- 推近倍数参考：单个小卡片 2.4–2.6，半宽卡片 1.6–1.9，整行/整表 1.05–1.2。

`<issue>/page.html`（只写页面内部）+ 可选 `page.css`、`init.js`：
- 要被讲到的元素加 `id`，并带 `class="box"`（会参与入场动画）。
- `init.js` 可定义 `window.ANIM=(t,seg)=>{}` 做逐帧动画（柱子生长、数字滚动、表格重排），必须是 t 的纯函数。
- 元素位置会被动画改变时（例如排序后的行），定义 `window.RECT=id=>({x,y,w,h})` 返回最终位置，否则高亮会框错地方。

## 运行
```bash
cd templates && npm install            # playwright-core；本机需 Chrome（或设 CHROME_PATH）
pip install numpy edge-tts pillow; apt install ffmpeg fonts-noto-cjk   # JetBrains Mono 另装
python3 build.py ../examples/02-audience --keyframes-only   # 先出 12 帧联系表 kf_sheet.jpg，人眼看
python3 build.py ../examples/02-audience                    # 出片 + 检查报告
```
输出末行是 JSON：时长、帧数、`freezes>=0.8s`、`overlap_frames`、`voice_gaps>0.6s`。三项都应为空/0（结尾 2s 淡出除外）。

## 踩过的坑（全部已在模板里修好，改模板时别改回去）
1. **"卡顿"多半不是掉帧**：是镜头在一个指标上停 6–7 秒几乎不动 + 配音句间停顿叠加。修法：每段停留期间镜头**持续缓推 7%** + 较大幅度漂移/摇摆；用 `freezedetect=n=0.003` 严格检测。
2. **配音停顿**：edge-tts 句号停顿 0.6–0.8s。`audio.py` 把段内静音压到 ≤0.32s，段间 0.22s，整片除开头 1s/结尾 2s 外**无 >0.6s 的空档**。
3. **帧率**：每帧按帧号只渲染一次（`render(f/30)`），并行 worker 按帧号区间切，图片序列 `-framerate 30 … -r 30` 编码。不要用实时录屏，不要一帧渲染两次。用 `ffprobe -count_frames` 核对帧数 = 时长×30。
4. **嘴型**：别按原始音量逐帧开合（太快像抽搐）。用 3 帧平滑包络 + 开/闭双阈值 + 每个状态至少保持 3 帧，长音中间插一次闭嘴，约 ≤5Hz，停顿时闭嘴。
5. **字幕与头像不能重叠**：头像 250px 固定左下，字幕走头像上方的独立通道（底边 y≈1520）。`cap.mjs` 每帧检测两者包围盒，`overlap.log` 必须为空。
6. **系列名被挡**：`// 系列名` 放在带底色的小签上、z-index 高于页面；顶部标签放在它下面。
7. **全景镜头字太小**：全景倍数按页面高度自动算（`min(1, 1250/页面高)`），倾斜减小到 -4°；卡片字号加大（标签 18px、数值 34px）。页面越长全景越小，所以一页别塞太多。
8. **高亮框跟着元素动**：元素会被动画移动时一定要给 `RECT`。
9. **事实**：讲解里只说有出处的定义。平台口径用官方帮助页或引用官方的报道核实；自己算的比例（如 有效占比、关注转化）要说明"自己算的"，页面上把公式写出来；不确定的词用"一般""可能"并在交付说明里标出。
10. **不写城市/真实数据/真实帖子**；示例帖子用中性的虚构内容，账号用 `@demo`。

## QA 清单（交付前逐项过）
- [ ] 联系表 12 帧人眼看过：无元素出框、无标签压字、高亮框位置对
- [ ] `overlap_frames = 0`，`voice_gaps` 为空，`freezes>=0.8s` 只有结尾淡出
- [ ] 时长符合要求（单期 60–110s 为宜）
- [ ] 讲稿每个定义都有来源，需要标注的已标注
- [ ] 全片无大面积橙色、无渐变背景
