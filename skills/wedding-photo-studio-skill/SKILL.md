---
name: wedding-photo-studio
description: Orchestrate customizable, high-end wedding photography workflows, design structured multi-angle prompts, and directly generate wedding photo sets for both virtual couples and real couple (plus optional pet) reference photos with strict facial consistency, unified luminous complexion, bridal high-crown aesthetics, and natural head-to-body proportion blending. Use whenever the user asks to shoot wedding photos, create couple portraits, refine bridal prompts, customize wedding scenes/outfits/poses/camera specs, or apply style packs from the studio catalog.
---

# Wedding Photo Studio (Orchestrator)

An extensible, modular wedding photography orchestrator that separates workflow logic, reusable catalogs, pluggable style packs, proportion/aesthetic guardrails, rendering adapters, and lightweight helper scripts.

## Hard Execution Gate (MUST OBEY BEFORE ANY IMAGE GENERATION)

1. **NO IMAGE TOOL CALLS BEFORE PHASE 2 CONFIRMATION:** Do NOT call any image generation or image editing tool until you have presented the Phase 2 3-column confirmation table AND received the user's explicit confirmation in a subsequent turn.
2. **Action Verbs Are NOT Skip Permission:** Requests such as "帮我拍婚纱照", "帮我生成一张", "用这张合照出图", or "generate a wedding photo" do **NOT** authorize skipping Phase 2 or auto-running defaults.
3. **Only Valid Skip Triggers:** Skip Phase 2 ONLY if the user explicitly writes "按默认生成" / "全部使用默认配置" / "直接按默认出图" / "抽卡" (explicit blind draw), OR has already specified all 5 modules in one message.
4. **Strict Image Count Compliance:** Generate the exact number of images requested by the user (e.g., if the user asks for 1 test shot, generate exactly 1 image, NEVER 2 or more).

## Architecture Overview

Load files on demand instead of dumping everything into context at once:

- **Guardrails (`guardrails/`):** Always load `identity-and-proportion.md`, `bridal-aesthetics.md`, and `set-continuity-qa.md` before writing prompts or generating images.
- **Style Packs (`packs/`):** 19 installed themed presets across 4 categories:
  - Nature & Scenic: `dali-cangshan-sunrise.pack.yaml` (default), `sayram-lake-monet.pack.yaml`, `enchanted-forest-tyndall.pack.yaml`, `seaside-vacation-documentary.pack.yaml`, `iceland-black-sand-epic.pack.yaml`
  - Oriental & Chinese: `crimson-new-chinese.pack.yaml`, `imperial-crimson-xiuhe.pack.yaml`, `jiangnan-ink-garden.pack.yaml`
  - Studio & Ceremonial: `korean-minimal-airy.pack.yaml`, `white-chapel-ceremony.pack.yaml`, `editorial-noir-studio.pack.yaml`, `european-palace-staircase.pack.yaml`, `french-vintage-garden.pack.yaml`
  - Retro, Cinema & Story: `japanese-film-natural.pack.yaml`, `hongkong-retro-cinema.pack.yaml`, `shanghai-vintage-mansion.pack.yaml`, `road-trip-wedding.pack.yaml`, `school-to-marriage.pack.yaml`, `pet-family-wedding.pack.yaml`
  Each supplies cohesive defaults while allowing per-module overrides.
- **Atomic Catalogs (`catalogs/`):** Load relevant YAML files when browsing or customizing locations (plus micro-zones and global landmarks), styling (plus unified skin finish and pet locks), poses (plus contact topology and reactive expressions), or camera specs.
- **Shot Matrices (`matrices/`):** Load `8-angle-cinematic.yaml` (default), `4-angle-editorial.yaml`, or `story-timeline-8.yaml` to plan distinct, non-repetitive angles.
- **Adapters (`adapters/`):** Format final prompts for `native-multimodal.md` (default), `cn-platforms.md` (Jimeng / Doubao / Nano Banana), `midjourney.md`, or `flux-comfyui.md`.
- **Optional Workflows (`workflows/`):** Load strictly on demand: `wardrobe-board.md` (6-look outfit comparison), `reference-beauty-prep.md` (3-panel pre-shoot reference retouch), `multi-person-roster.md` (solo / family / bridesmaids & groomsmen groups).
- **Helper Scripts (`scripts/`):** `remix_resolver.py` (single-variable edits), `make_contact_sheet.py` (2x2 / 3x2 / 4x2 / 3x3 numbered boards), `workspace_manager.py` (optional local multi-theme `THEME-xxx` persistence), and `validate_repo.py`.
- **Contract Tests (`tests/`):** `test_skill_contracts.py` (automated stdlib `unittest` regression suite verifying guardrails, packs, taglines, and scripts).

## Core Workflow

### Phase 1: Input Detection and Mode Routing

Inspect the user's message and attachments to initialize `SessionState` (following `schemas/session-state.schema.json`):

1. **Real Couple Reference Mode (Image-to-Image):** Triggered when the user uploads one or more real couple (and optional pet) photos.
   - Lock `guardrails/identity-and-proportion.md` as **MANDATORY**.
   - Enforce **Canonical Original Reference Lock**: initially uploaded photos remain the default facial identity anchors across all batches and turns (never silently replaced by AI-derived frames unless explicitly promoted by the user), while **de-locking static reference expressions, casual clothes, stiff poses, and everyday handheld items** (brochures, phones, cards, bags).
   - Reference pose & handheld-object policy defaults to `replace-with-bridal-poses` (completely remove everyday objects and static stance from the reference photo and replace with fresh bridal hand actions, bouquet holding, and wind-swept veil motion), and is **optionally switchable** to `keep-reference-pose-only` or `keep-reference-keepsake` (retain a user-named meaningful keepsake).
   - Groom hairstyle defaults to `keep-original-groomed` (original hairstyle cleanly groomed) and is **optionally switchable** to `editorial-redesign` if the user wants a theme-matched redesign.
   - Apply `guardrails/bridal-aesthetics.md` (voluminous high-crown hair + explicit fringe/parting/ear-neck choices) and default `luminous-fair-unified` skin finish (naturally luminous fair tone applied uniformly across face, jawline, neck, collarbones, and shoulders with zero seam).
   - Recommend **individual 3:4 photos** as default for sharp faces, while keeping **8-panel preview** (with `PANEL IDENTITY RESET`) and **1-shot representative preview first** cleanly selectable.
2. **Virtual Couple Mode (Text-to-Image):** Triggered when no reference photo is provided.
   - Default to a 25-30-year-old Chinese young couple with natural, authentic chemistry unless otherwise specified.
3. **Solo & Multi-Person Group Routing (`workflows/multi-person-roster.md`):**
   - Couples default silently to 2 people (`P01` bride + `P02` groom) with no extra headcount question.
   - If the user requests a solo portrait (1 person) or a family / bridesmaids & groomsmen group shoot (3+ people), load `workflows/multi-person-roster.md`: run the compact Participant Structure Gate for missing count/gender/relationship hierarchy first, then enforce per-person Detail Floor (`P01..Pn`) across wardrobe and every shot.
4. **Chat-First Default (No Mandatory Project Directory):** Run directly in chat without asking for a workspace path. Only invoke `scripts/workspace_manager.py` (`init` / `new-theme`) if the user explicitly asks to persist and isolate multiple local `THEME-xxx` shooting projects.

### Phase 2: Mandatory 3-Column Confirmation Menu (Single-Turn With Smart Defaults)

Never skip customization unless the user explicitly says to run all defaults or has already specified every module. Never silently alter pack/guardrail defaults (such as keeping casual reference brochures, freezing the static reference stance, or overriding `luminous-fair-unified`) unless the user asks for it.

Present ONE compact **3-column Markdown table (`模块 | 默认推荐 | 其余可选项`)** derived from the active pack (defaulting to `packs/dali-cangshan-sunrise.pack.yaml`). Always surface ALL core toggles and all 19 installed packs (grouped cleanly into 4 categories) in column 3 so the user immediately sees every available capability:

| 模块 | 默认推荐 | 其余可选项（支持直接回关键词或自由人话） |
| --- | --- | --- |
| **1. 主体与原图处理** | 真人模式锁五官与眼镜; **清除原图宣传册等杂物与僵硬站姿** (`replace-with-bridal-poses`) | `保留原图动作仅去杂物` / `保留原图指定纪念物` / `加入宠物参考照` / `多人伴郎伴娘或全家福` (`workflows/multi-person-roster.md`) / `先做三宫格参考图美化` (`workflows/reference-beauty-prep.md`, 仅用户主动提出) |
| **2. 风格包 / 场地** | **`dali-cangshan-sunrise`（大理苍山日照金山）** | **东方中式**: `海派深红新中式` / `故宫红墙秀禾` / `江南园林水墨`; **棚拍仪式**: `韩系极简棚拍` / `纯白教堂仪式堂` / `高级黑灰情绪棚` / `欧式古堡旋转楼梯` / `法式复古庄园`; **自然风光**: `赛里木湖莫奈` / `原始森林丁达尔` / `海边度假纪实` / `冰岛黑沙滩史诗`; **复古纪实**: `日系胶片自然` / `港风霓虹夜景` / `海派民国老洋房` / `公路旅行` / `从校服到婚姻` / `宠物家庭`; 或自定场地（`catalogs/locations.yaml`, 回「展开场地菜单」看全部） |
| **3. 妆造、肤质与道具** | **心形抹胸蕾丝主纱** + **顺滑高颅顶波浪卷** + **默认 0 瘦脸保真脸型 (`none-zero-slimming`)** + **整体清透白皙统一 (`luminous-fair-unified`)** + **新郎黑西装（留原发型）** + **15朵浅粉玫瑰与刺绣长头纱** | 礼服领型: `一字肩锻面` / `法式方领` / `V领轻纱` / `中式秀禾` / `先看 6 套换装对比` (`workflows/wardrobe-board.md`); 脸型修饰: `极轻微颊侧软组织修饰 (验收上限<=2%, 降辨识度即回退0)`; 肤质: `影楼柔焦白皙` / `原生肤色`; 新郎发型: `按主题重塑`;（`catalogs/styling-and-props.yaml`, 回「展开礼服/妆造菜单」看全部） |
| **4. 情绪、手部动作与分镜** | **浪漫深情电影感**; **主镜头按原图朝向（锁脸最稳）+ 新娘单手轻撩飘动头纱 + 新郎持捧花**; **`8 角度电影全套`** (`matrices/8-angle-cinematic.yaml`) | 朝向/视线: `两人深情对视` / `单向温柔凝望` / `同望远方`; 情绪: `松弛俏皮大笑` / `杂志高级冷艳` / `中式端庄`; 分镜: `4 张高定精修` (`matrices/4-angle-editorial.yaml`) / `时间线 8 镜` (`matrices/story-timeline-8.yaml`);（`catalogs/poses-and-moods.yaml`, 回「展开动作菜单」看全部） |
| **5. 光影、画幅与出图** | **5500K 黄金逆光 · 85mm 胶片质感 · 自动匹配分场景摄影美学口号 · `3:4` 竖版 · 独立单图分批（4+4）** | 出图: `先出 1 张代表图试拍` / `先出 8 宫格选片板`; 画幅: `2:3` / `9:16` / `16:9`; 摄影口号: `戏剧高定` / `清透极简` / `纪实故事` / `东方复古` / `自定义或关闭`; 平台: `即梦/豆包/Nano Banana` / `Midjourney` / `Flux`; 附加: `加社媒分享文案` / `本地多主题归档` |

Always include ONE concise instruction line below the table: tell the user they can reply "按默认生成", freely mix natural-language ideas or custom requests without memorizing module names (for example: "换海派深红新中式，先看6套换装，其他默认"), ask to expand any long menu ("展开场地/礼服/动作/光影菜单"), or trigger optional workflows ("给我3个方向" / "抽卡" / "先看6套换装" / "先美化参考图").

**STOP HERE:** End your turn immediately after presenting the Phase 2 table and wait for the user's next message before compiling final prompts or calling any image generation tool.

#### Optional On-Demand Workflow Extensions (Never Interrupt Normal Flow)

Activate ONLY when explicitly triggered by the user:

1. **A/B/C 3-Direction Inspiration Cards (`给我3个方向` / undecided theme):**
   - Generate exactly 3 compact, visually contrasting direction cards labeled `A / B / C`: **A & B** = 2 distinct contemporary real-world landmarks across different climates/cultures (`catalogs/locations.yaml`, never auto-locked by perceived nationality); **C** = 1 concrete time-travel or known-work creative world. Each card specifies separate per-person bride & groom outfits, sleek high-crown hair + unified skin finish, lighting, and micro-zones. When the user replies `A`/`B`/`C` (case-insensitive), lock immediately and jump straight to Phase 3-4.
2. **Blind-Box Auto-Draw (`抽卡`):**
   - Triggered ONLY by explicit "抽卡" intent. Skip Phase 2; randomly draw 1 fresh, non-repetitive direction across installed `packs/`, global landmarks, and time-travel themes (tracking `used_spacetime_anchors`), enforce all core guardrails, and run directly through Phase 3-4.
3. **6-Look Wardrobe Comparison Board (`先看6套换装` / `礼服对比`):** Load `workflows/wardrobe-board.md` to produce 6 distinct per-person outfit combinations (optional 6-panel or `3x2` numbered preview via `scripts/make_contact_sheet.py` with `--layout 3x2`), then lock the user's chosen Look into Phase 3-4.
4. **Pre-Shoot 3-Panel Reference Beauty Prep (`先美化参考图` / `三宫格美化`):** Load `workflows/reference-beauty-prep.md` ONLY on explicit request (never proactively prompt upon photo upload). Generates Left/Center/Right 3-panel retouch options with 0% geometric slimming; enlarged output remains a derived reference and never silently replaces `canonical_original_references`.
5. **Local Persistent Multi-Theme Workspace (`建本地项目` / `多主题归档`):** Use `scripts/workspace_manager.py` (`init` / `new-theme` / `list`) to isolate `THEME-001`, `THEME-002`... while sharing `canonical_refs/`.

### Phase 3: Prompt Compilation and Guardrail Injection

Compile a structured `ShotPlan` (following `schemas/shot-plan.schema.json`) and inject ALL active guardrails into every frame:

1. **Identity, Angle-Aware Facial Structure Lock, Native Proportion & Unified Complexion Guardrail (`guardrails/identity-and-proportion.md`):**
   - Lock front-facing facial structure from the canonical original photo (inter-eye distance, eye-nose-mouth positions, cheek fullness/width, jawline turn, chin shape, natural asymmetry) with **default geometric slimming = 0** (optional `subtle-soft-contour` strictly QA-capped at `<= 2%` bilateral cheek width with instant rollback to 0 if likeness drops); conservatively project the same 3D facial volume on angled/profile shots (preferring same-angle originals when supplied).
   - De-lock static reference expressions and enforce the chosen `reference_pose_and_props_policy` (by default removing casual clothes and everyday reference handheld objects like brochures/phones and injecting explicit `bride_hand_action`, `groom_hand_action`, `handheld_prop_state`, and flowing veil dynamics).
   - Coordinate head, neck, shoulders, and torso naturally using the subject's visible reference build plus 85mm optical perspective: prevent both "big head / tiny shoulders" AND over-corrected thick neck / bulky shoulders (roll back immediately if bulky).
   - Apply the chosen skin finish (default unified luminous fair) identically across face, jawline, neck, collarbones, and exposed shoulders with natural shadows; enforce Face Readability Gate and per-panel `PANEL IDENTITY RESET` in multi-panel previews.
2. **Mandatory Bridal High-Crown Hair Guardrail (`guardrails/bridal-aesthetics.md`):**
   - Inject voluminous high-crown lifted roots with **sleek, smooth, neatly groomed airy volume** (avoid frizzy flyaway strands cutting across cheeks) and explicit fringe/parting/ear-neck decisions into every bridal frame.
3. **Directing Table, Scene-Matched Aesthetic Taglines & 4-Step Structural QA (`guardrails/set-continuity-qa.md`):**
   - Auto-select the matching scene aesthetic direction tagline (`dramatic-couture`, `airy-minimal-grace`, `candid-film-story`, or `oriental-vintage-poetry`) from `catalogs/camera-and-lighting.yaml` instead of forcing a single dramatic slogan across gentle/airy styles (respecting user overrides or `none`).
   - Assign distinct venue micro-zones, 2-4 framing-visible body mechanics, and couple contact topology (or full per-person `participants_present` + `participant_directions` for 3+ people).
   - Enforce quantitative quotas for 6-9 shot sets (adjacent frames differ in >= 4 directing fields, direct-to-camera <= 2, formal side-by-side standing <= 2, pose-family semantic dedupe) and audit outputs via the 4-step structural QA (eye-level facial alignment -> neck/shoulder anti-bulky check -> angled perspective check -> unified jawline/neck/clavicle lighting & neat hair).

### Phase 4: Deliver Structured Prompts, Generate Images & Single-Variable Remix

1. Output a concise **Configuration Summary**, the compact **Directing Table**, and **Reusable Bilingual Prompts (Chinese + English)** formatted via the active adapter (`adapters/native-multimodal.md` by default, or `adapters/cn-platforms.md` / `adapters/midjourney.md` / `adapters/flux-comfyui.md`).
2. Generate images according to the user's chosen delivery mode:
   - **Individual 3:4 shots (Recommended Default):** Generate in clean batches (e.g., 4 frames per batch) with canonical original reference photo(s) attached on every call and locked `continuity_anchors` across batches; optionally stitch rendered singles into a numbered showcase grid using `scripts/make_contact_sheet.py`.
   - **1-Shot Representative First (Optional):** Render Shot 2 or Shot 5 first to confirm likeness, proportion harmony, and tone before completing the rest.
   - **Multi-Panel Preview (Optional):** Render a crisp 8-panel selection board with `PANEL IDENTITY RESET` per panel; when the user selects favorite numbers to enlarge, render standalone 3:4 frames still anchored to the canonical original photo(s).
3. If `emit_share_card` is requested, include a clean 5-part social share card (title, hook, copyable short invocation, 4-7 `#hashtags`, invitation CTA) free of internal workflow jargon.
4. **Dual-Anchor Delta Refinement, Explicit Triggers, Post-Delivery Tip & Single-Variable Remix:**
   - **Mandatory Post-Delivery Tip (ALWAYS append at the bottom of EVERY reply that delivers generated images or copy-ready prompts):**
     > **成片微调指南 (防改坏变量控制):**
     > 如对成片基本满意、只需局部微调 (如发色、高颅顶、手部动作、头纱或光影), 直接回复 `微调第X张: 只改___` (或说「我需要修改 / 局部微调 / 改一下...」) 即可触发防改坏微调。
     > 系统会自动采用 **双图锚定 (图1最初真人原照仅锁五官 + 图2当前成片锁构图/礼服/背景/光影)** + `KEEP UNCHANGED / CHANGE ONLY` 最小改动策略, 防止五官修漂移或把满意部分改坏。*(如在新对话微调, 请同时附上原照与成片; 整套换大项如场地/礼服可直接说「只换场地到___」。)*
   - **Automatic Trigger Rules:** Activate **Dual-Anchor Delta Refinement** whenever the user expresses edit intent on an existing output (e.g., "我需要修改", "微调", "局部修改", "改一下第X张", "只改...", "别动其他", "refine/tweak/edit only"). Always remind the user why both images are needed, attach **Image 1 = Canonical Original Real Photo** + **Image 2 = Selected v1 Frame**, and compile explicit `KEEP UNCHANGED` and `CHANGE ONLY` (1-2 targeted edits) blocks (see `adapters/native-multimodal.md` and `adapters/cn-platforms.md`). If the original real photo is missing in a fresh conversation, pause and ask the user to attach it first.
   - **Single-Variable Set Remix:** For set-level single-dimension swaps (e.g., "只换场地" / "只换礼服" / "只改光影"), follow `scripts/remix_resolver.py` to freeze unaffected modules verbatim rather than rewriting the whole session.

## Extension Hook for Future Merged Packs

When new style packs are added to `packs/` (including adapted packs merged from external repositories per `docs/MERGE_GUIDE.md`):

- Validate them against `schemas/style-pack.schema.json` using `scripts/validate_repo.py`.
- Register the pack ID in the Phase 2 menu automatically.
- Never allow an external pack to disable `guardrails/identity-and-proportion.md` or `guardrails/bridal-aesthetics.md` unless the user explicitly overrides them in the current session.
