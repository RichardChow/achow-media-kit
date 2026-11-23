---
name: wedding-photo-studio
description: Orchestrate customizable, high-end wedding photography workflows, design structured multi-angle prompts, and directly generate wedding photo sets for both virtual couples and real couple (plus optional pet) reference photos with strict facial consistency, unified luminous complexion, bridal high-crown aesthetics, and natural head-to-body proportion blending. Use whenever the user asks to shoot wedding photos, create couple portraits, refine bridal prompts, customize wedding scenes/outfits/poses/camera specs, or apply style packs from the studio catalog.
---

# Wedding Photo Studio (Orchestrator)

An extensible, modular wedding photography orchestrator that separates workflow logic, reusable catalogs, pluggable style packs, proportion/aesthetic guardrails, rendering adapters, and lightweight helper scripts.

## Architecture Overview

Load files on demand instead of dumping everything into context at once:

- **Guardrails (`guardrails/`):** Always load `identity-and-proportion.md`, `bridal-aesthetics.md`, and `set-continuity-qa.md` before writing prompts or generating images.
- **Style Packs (`packs/`):** 9 installed themed presets (`dali-cangshan-sunrise.pack.yaml` default, `korean-minimal-airy.pack.yaml`, `french-vintage-garden.pack.yaml`, `sayram-lake-monet.pack.yaml`, `japanese-film-natural.pack.yaml`, `seaside-vacation-documentary.pack.yaml`, `road-trip-wedding.pack.yaml`, `school-to-marriage.pack.yaml`, `pet-family-wedding.pack.yaml`). Each supplies cohesive defaults while allowing per-module overrides.
- **Atomic Catalogs (`catalogs/`):** Load relevant YAML files when browsing or customizing locations (plus micro-zones and global landmarks), styling (plus unified skin finish and pet locks), poses (plus contact topology and reactive expressions), or camera specs.
- **Shot Matrices (`matrices/`):** Load `8-angle-cinematic.yaml` (default), `4-angle-editorial.yaml`, or `story-timeline-8.yaml` to plan distinct, non-repetitive angles.
- **Adapters (`adapters/`):** Format final prompts for `native-multimodal.md` (default), `cn-platforms.md` (Jimeng / Doubao / Nano Banana), `midjourney.md`, or `flux-comfyui.md`.
- **Helper Scripts (`scripts/`):** Use `remix_resolver.py` for single-variable partial edits and `make_contact_sheet.py` to stitch individual high-res frames into a numbered preview board.

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

### Phase 2: Mandatory 3-Column Confirmation Menu (Single-Turn With Smart Defaults)

Never skip customization unless the user explicitly says to run all defaults or has already specified every module. Never silently alter pack/guardrail defaults (such as keeping casual reference brochures, freezing the static reference stance, or overriding `luminous-fair-unified`) unless the user asks for it.

Present ONE compact **3-column Markdown table (`模块 | 默认推荐 | 其余可选项`)** derived from the active pack (defaulting to `packs/dali-cangshan-sunrise.pack.yaml`). Always surface ALL core toggles and all 9 installed packs in column 3 so the user immediately sees every available capability:

| 模块 | 默认推荐 | 其余可选项（支持直接回关键词或自由人话） |
| --- | --- | --- |
| **1. 主体与原图处理** | 真人模式锁五官与眼镜; **清除原图宣传册等杂物与僵硬站姿** (`replace-with-bridal-poses`) | `保留原图动作仅去杂物` (`keep-reference-pose-only`) / `保留原图指定纪念物` (`keep-reference-keepsake`) / `加入宠物参考照` |
| **2. 风格包 / 场地** | **`dali-cangshan-sunrise`（大理苍山日照金山）** | 其余 8 套包: `韩系极简棚拍` / `法式复古庄园` / `赛里木湖莫奈` / `日系胶片自然` / `海边度假纪实` / `公路旅行` / `从校服到婚姻` / `宠物家庭`; 或自定室内外/全球地标（`catalogs/locations.yaml`, 回「展开场地菜单」看全部） |
| **3. 妆造、肤质与道具** | **心形抹胸蕾丝主纱** + **顺滑高颅顶波浪卷** + **默认 0 瘦脸保真脸型 (`none-zero-slimming`)** + **整体清透白皙统一 (`luminous-fair-unified`)** + **新郎黑西装（留原发型）** + **15朵浅粉玫瑰与刺绣长头纱** | 礼服领型: `一字肩锻面` / `法式方领` / `V领轻纱` / `中式秀禾`; 脸型修饰: `极轻微颊侧软组织修饰 (验收上限<=2%, 降辨识度即回退0)`; 肤质: `影楼柔焦白皙` / `原生肤色`; 新郎发型: `按主题重塑`;（`catalogs/styling-and-props.yaml`, 回「展开礼服/妆造菜单」看全部） |
| **4. 情绪、手部动作与分镜** | **浪漫深情电影感**; **主镜头按原图朝向（锁脸最稳）+ 新娘单手轻撩飘动头纱 + 新郎持捧花**; **`8 角度电影全套`** (`matrices/8-angle-cinematic.yaml`) | 朝向/视线: `两人深情对视` / `单向温柔凝望` / `同望远方`; 情绪: `松弛俏皮大笑` / `杂志高级冷艳` / `中式端庄`; 分镜: `4 张高定精修` (`matrices/4-angle-editorial.yaml`) / `时间线 8 镜` (`matrices/story-timeline-8.yaml`);（`catalogs/poses-and-moods.yaml`, 回「展开动作菜单」看全部） |
| **5. 光影、画幅与出图** | **5500K 黄金逆光 · 85mm 胶片质感 · `3:4` 竖版 · 独立单图分批（4+4）** | 出图: `先出 1 张代表图试拍` / `先出 8 宫格选片板`; 画幅: `2:3` / `9:16` / `16:9`; 平台: `即梦/豆包/Nano Banana` / `Midjourney` / `Flux`; 附加: `加社媒分享文案` |

Always include ONE concise instruction line below the table: tell the user they can reply "按默认生成", freely mix natural-language ideas or custom requests without memorizing module names (for example: "换韩系极简风，新郎按主题重塑发型，捧花换向日葵，先出1张代表图，其他默认"), ask to expand any long menu ("展开场地/礼服/动作/光影菜单"), or use optional discovery shortcuts ("给我3个方向" or "抽卡") if undecided.

#### Optional Discovery Shortcuts (On-Demand Only)

Never force an upfront mode-selection menu. Activate these two shortcuts only when the user explicitly triggers them or asks for inspiration:

1. **A/B/C 3-Direction Inspiration Cards (`给我3个方向` / undecided theme):**
   - Generate exactly 3 compact, visually contrasting direction cards labeled `A / B / C`:
     - **A & B (Contemporary Real-World Landmarks):** 2 distinct, recognizable real-world destinations across different climates, architecture, and cultural aesthetics (drawing from `catalogs/locations.yaml`; never auto-lock locations by perceived nationality unless the user specifies a region).
     - **C (Time-Travel / Cross-Era Direction):** 1 concrete historical era + real landmark, futuristic version of a real landmark, or well-known film/literary world adapted for couple photography (never vague generic labels).
   - Each card lists distinct per-person bride & groom outfits, high-crown hairstyle + unified luminous-fair skin finish, lighting/palette, and key scene micro-zones.
   - When the user replies `A`, `B`, or `C` (case-insensitive), lock that direction immediately and move straight to Phase 3 and Phase 4 without redundant Look confirmation.
2. **Blind-Box Auto-Draw (`抽卡`):**
   - Triggered ONLY by explicit "抽卡" (or clear equivalent) intent.
   - Skip the questionnaire and A/B/C selection: randomly pick 1 fresh, non-repetitive direction across installed `packs/`, global contemporary landmarks, and time-travel themes (tracking `used_spacetime_anchors` to avoid repeats), keep all mandatory guardrails (`guardrails/identity-and-proportion.md`, `guardrails/bridal-aesthetics.md`, `guardrails/set-continuity-qa.md`) strictly active, and run directly through Phase 3 and Phase 4 in the user's preferred delivery mode (default individual 3:4 shots, or 8-panel preview if requested).

### Phase 3: Prompt Compilation and Guardrail Injection

Compile a structured `ShotPlan` (following `schemas/shot-plan.schema.json`) and inject ALL active guardrails into every frame:

1. **Identity, Angle-Aware Facial Structure Lock, Native Proportion & Unified Complexion Guardrail (`guardrails/identity-and-proportion.md`):**
   - Lock front-facing facial structure from the canonical original photo (inter-eye distance, eye-nose-mouth positions, cheek fullness/width, jawline turn, chin shape, natural asymmetry) with **default geometric slimming = 0** (optional `subtle-soft-contour` strictly QA-capped at `<= 2%` bilateral cheek width with instant rollback to 0 if likeness drops); conservatively project the same 3D facial volume on angled/profile shots (preferring same-angle originals when supplied).
   - De-lock static reference expressions and enforce the chosen `reference_pose_and_props_policy` (by default removing casual clothes and everyday reference handheld objects like brochures/phones and injecting explicit `bride_hand_action`, `groom_hand_action`, `handheld_prop_state`, and flowing veil dynamics).
   - Coordinate head, neck, shoulders, and torso naturally using the subject's visible reference build plus 85mm optical perspective: prevent both "big head / tiny shoulders" AND over-corrected thick neck / bulky shoulders (roll back immediately if bulky).
   - Apply the chosen skin finish (default unified luminous fair) identically across face, jawline, neck, collarbones, and exposed shoulders with natural shadows; enforce Face Readability Gate and per-panel `PANEL IDENTITY RESET` in multi-panel previews.
2. **Mandatory Bridal High-Crown Hair Guardrail (`guardrails/bridal-aesthetics.md`):**
   - Inject voluminous high-crown lifted roots with **sleek, smooth, neatly groomed airy volume** (avoid frizzy flyaway strands cutting across cheeks) and explicit fringe/parting/ear-neck decisions into every bridal frame.
3. **Directing Table, Quantitative Diversity & 4-Step Structural QA (`guardrails/set-continuity-qa.md`):**
   - Assign distinct venue micro-zones, 2-4 framing-visible body mechanics, and couple contact topology per shot.
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
