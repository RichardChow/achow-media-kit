# Wedding Photo Studio Skill (`wedding-photo-studio-skill`)

一个面向 GitHub 开源与长期模块化扩展的 **高定 AI 婚纱照编排 Skill**。  
An extensible, modular AI wedding photography orchestrator Skill designed for **virtual couples** and **real couple (plus optional pet) reference photos**, combining structured multi-angle directing, strict identity & head-to-body proportion guardrails, unified luminous bridal complexion, pluggable style packs, multi-engine adapters, and lightweight workflow utilities.

---

## 核心特性 (Key Highlights)

- **身份一致性、头肩比融合与整体白皙统一 (`guardrails/identity-and-proportion.md`):**
  - 针对真人参考图常见的大头小身、极窄溜肩与面颈割裂问题，按人物真实脸型体量自适应匹配自然肩宽与脖颈粗细；
  - 默认提供 **`luminous-fair-unified`（自然清透白皙精修）**，在保留真实皮肤微纹理的前提下将**面部、下颌线、脖颈、锁骨与肩臂整体同步提亮**（同时支持切换 `studio-soft-glow` 或 `natural-authentic`）；
  - 实行 **Canonical Original Reference Lock**（最初上传原图永为默认人脸锚点，不被 AI 派生图静默顶替）、**表情去锁定**（只锁五官骨相，不锁死参考图单一表情）以及 **Face Readability Gate**（远景/回眸/倒影保持清晰人脸可读性）。
- **新娘高颅顶全局美学护栏 (`guardrails/bridal-aesthetics.md`):** 无论波浪卷、低盘发、赫本丸子、森系编发还是中式发髻，均强制锁定饱满高颅顶与头包脸空气感，并显式决策刘海、发缝与露耳露颈比例。
- **灵活可控的新郎发型与出图模式:**
  - **新郎发型可选：** 真人模式默认 `keep-original-groomed`（保持参考图原发型并自然整理），也可按需切换 `editorial-redesign`（按主题重塑造型）；
  - **出图形式可选：** 默认推荐 **独立 3:4 单图分批生成**（可配合 `scripts/make_contact_sheet.py` 拼出带编号选片板），同时支持 **先出 1 张代表图试拍确认**，或直接选择 **8 宫格预览板**（自动开启逐格 `PANEL IDENTITY RESET` 防漂移，选中编号后再放大独立单图）。
- **导演式量化防重复分镜 (`guardrails/set-continuity-qa.md` & `matrices/`):** 引入 8 栏导演分镜表、相邻帧 ≥4 维度差异、直视镜头 ≤2、并排站姿 ≤2、姿势家族语义去重、2-4 个景别可见力学点、情侣接触关系拓扑与场景微位点（Micro Zones）。
- **单变量局部 Remix (`scripts/remix_resolver.py`):** 成片后说“只换场地/只换礼服/只调光影”时精准冻结无关模块，避免整套重写。

---

## 内置 9 套开箱即用风格包 (`packs/`)

| Pack ID | 中文名称 | 核心场景与氛围 | 默认分镜矩阵 |
| --- | --- | --- | --- |
| `dali-cangshan-sunrise` *(默认)* | 大理苍山日照金山电影感 | 高原草坡、日照金山逆光、飘逸长头纱 | `8-angle-cinematic` |
| `korean-minimal-airy` | 韩系极简清透棚拍 | 纯白高定影棚、半透白纱帘、高调漫射窗光 | `8-angle-cinematic` |
| `french-vintage-garden` | 法式复古庄园花园 | 石灰岩古堡、雕花花廊、午后斑驳树影 | `8-angle-cinematic` |
| `sayram-lake-monet` | 赛里木湖莫奈油画感 | 湛蓝高原湖岸、雪峰野花、印象派柔美光色 | `8-angle-cinematic` |
| `japanese-film-natural` | 日系胶片自然生活流 | 复古木屋书房、老街窗光、35mm 非摆拍纪实 | `8-angle-cinematic` |
| `seaside-vacation-documentary` | 海边度假私奔纪实 | 阳光沙滩、海边木屋、复古单车与海风扬纱 | `8-angle-cinematic` |
| `road-trip-wedding` | 公路旅行电影感 | 旷野公路、停靠敞篷老爷车、落日与复古直闪 | `8-angle-cinematic` |
| `school-to-marriage` | 从校服到婚姻·跨时空叙事 | 大学校园记忆与婚礼当下同机位跨时空呼应 | `story-timeline-8` |
| `pet-family-wedding` | 有宠物家庭温馨婚纱照 | 居家/草坪温馨互动、锁定宠物参考品种花纹 | `8-angle-cinematic` |

---

## 目录架构 (Repository Structure)

```text
wedding-photo-studio-skill/
├── README.md
├── .gitignore
├── SKILL.md                               # 核心编排入口（按需加载模块）
├── schemas/
│   ├── session-state.schema.json          # 5 模块会话契约（含宠物/原图锚点/Remix 状态）
│   ├── style-pack.schema.json             # 可插拔风格包标准接口
│   └── shot-plan.schema.json              # 多角度分镜与分享卡输出契约
├── guardrails/
│   ├── identity-and-proportion.md         # 身份锚定、头肩比融合、整体白皙统一与可读性门槛
│   ├── bridal-aesthetics.md               # 新娘高颅顶强制规则、显式发型杠杆与肤质档位
│   └── set-continuity-qa.md               # 7 项连续性 QA + 8 栏导演表与量化防重复配额
├── catalogs/
│   ├── locations.yaml                     # 4 大类户内外场景 + 全球旅拍地标 + Micro Zones 微位点
│   ├── styling-and-props.yaml             # 礼服领型头肩比提示、白皙肤质档位、新郎可选发型、宠物锁
│   ├── poses-and-moods.yaml               # 5 大情绪 + 3 大动作库 + 反应式表情 + 接触拓扑与力学指南
│   └── camera-and-lighting.yaml           # 6 类光影氛围、焦段压缩指南、胶片影调与画幅比例
├── matrices/
│   ├── 8-angle-cinematic.yaml             # 8 角度电影感矩阵（默认，含量化防重复配额）
│   ├── 4-angle-editorial.yaml             # 4 角度高定精修矩阵
│   └── story-timeline-8.yaml              # 8 角度时间线跨时空呼应叙事矩阵
├── packs/
│   ├── _template.pack.yaml                # 新建/合入风格包注释模板
│   └── *.pack.yaml                        # 9 套开箱即用主题风格包
├── adapters/
│   ├── native-multimodal.md               # 原生多模态生图工具（默认，支持单图/代表图/8宫格）
│   ├── cn-platforms.md                    # 国内常用平台适配（即梦 / 豆包 / Nano Banana）
│   ├── midjourney.md                      # Midjourney v6.1 / v7 适配规范
│   └── flux-comfyui.md                    # Flux.1 + ComfyUI / PuLID 适配规范
├── scripts/
│   ├── validate_repo.py                   # 全仓库 Schema / YAML / 署名 / 脚本 / 路径校验
│   ├── make_contact_sheet.py              # 独立成片拼图展示板工具（支持 2x2 / 4x2 / 3x3 + 编号）
│   └── remix_resolver.py                  # 单变量局部 Remix 依赖解析器
└── docs/
    └── MERGE_GUIDE.md                     # 外部参考项目资产拆解与合入指南
```

---

## 快速开始与实用工具 (Quick Start & Utilities)

将本仓库挂载到支持 `SKILL.md` 的 AI Agent Skill 目录即可触发：

- **默认旗舰包：** 「帮我拍一套大理苍山日照金山婚纱照，按默认生成」
- **真人合照 + 一句话定制：** 上传合照并发送：「选韩系极简风，新郎发型按主题重塑，先出 1 张代表图确认再出独立 3:4 单图，其他默认」
- **灵感探索（按需触发）：** 还没想好风格时可说「给我 3 个方向」（生成 A/B 两个跨文化现实地标 + C 一个穿越时空方案，回复 `A/B/C` 直接拍），或直接说「抽卡」（全自动盲盒抽签并锁定底线护栏一步出图）
- **单变量局部改配：** 「只换场地到赛里木湖，其他全部冻结不变」

### 命令行辅助脚本

```bash
# 1. 全仓库结构、JSON Schema、YAML、署名与路径完整性校验
python scripts/validate_repo.py

# 2. 查询单变量 Remix 冻结与失效依赖（支持中英文）
python scripts/remix_resolver.py 场地

# 3. 将生成的独立 3:4 单图拼成带编号的 4x2 或 3x3 选片展示板（需安装 Pillow）
python scripts/make_contact_sheet.py ./outputs/session_01 ./outputs/preview_grid.jpg --layout auto
```

---

## 扩展与合入外部风格 (Extending & Merging)

1. 复制 `packs/_template.pack.yaml` 为 `packs/<your-pack-id>.pack.yaml`，按 `schemas/style-pack.schema.json` 填写完整配置并保持 `enforce_high_crown: true` 与 `enforce_proportion_blending: true`。
2. 如从外部开源项目吸收风格或编排机制，请严格遵循 [`docs/MERGE_GUIDE.md`](docs/MERGE_GUIDE.md) 并在 `source` 中如实注明出处与协议。
3. 提交前执行 `python scripts/validate_repo.py` 确保零报错。

---

## 致谢与开源署名 (Acknowledgements & Attribution)

本仓库在模块化设计、风格包扩充与防漂移编排机制演进过程中，参考并重构吸收了以下优秀开源项目的理念与公开文字规范（均已遵守对应开源协议，未拷贝第三方受肖像权保护的示例人像图片）：

- **[wenyachen/ai-wedding-photo-skill](https://github.com/wenyachen/ai-wedding-photo-skill)** *(MIT License)* — 启发了 8 套精选婚纱照细分风格包概念、导演式量化防重复配额、国内平台（即梦/豆包/Nano Banana）适配经验与成片拼图工具思路。
- **[yang0/handraw-style](https://github.com/yang0/handraw-style)** *(Author: **yang0**, MIT License with Attribution Requirement)* — 启发了 `couple-photo-orchestrator` 中的 Canonical 原图身份锁、表情去锁定、Face Readability Gate、多宫格 `PANEL IDENTITY RESET`、场景微位点（Micro Zones）、2-4 景别可见身体力学、情侣接触关系拓扑与单变量 Remix 依赖图设计。
