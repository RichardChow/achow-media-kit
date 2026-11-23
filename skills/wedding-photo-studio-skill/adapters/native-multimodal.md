# Adapter: Native Multimodal Image Generators (Default)

**Target Engines:** Native multimodal image generation tools inside coding/chat agents (e.g., Gemini Image Generation / Nano Banana / Imagen, GPT Image, Seedream, and comparable instruction-following visual models).

**Adapter ID:** `native-multimodal`

---

## Flexible Delivery Modes (User-Selectable in Phase 2)

Support both delivery workflows cleanly—defaulting to **separate individual 3:4 images** for maximum facial sharpness while fully supporting **optional 8-panel previews** and **1-shot representative tests**:

1. **Individual 3:4 Single Images (`individual-images`, Recommended Default):**
   - Ideal for Real Couple Reference Mode so each face receives full pixel resolution with crisp likeness, natural head-to-shoulder proportions, airy high-crown hair strands, and seamless face-neck-shoulder skin blending.
   - **Batching Strategy for 8-Shot Sets:** Batch 1 = Shots 1-4; Batch 2 = Shots 5-8. Always attach the user's **canonical original reference photo(s)** on every single generation call and copy `continuity_anchors` verbatim across batches.
   - After rendering individual frames, optionally assemble a numbered 2x2 / 2x4 / 3x3 showcase sheet locally via `scripts/make_contact_sheet.py`.
2. **Optional 1-Shot Representative Test (`representative_first: true`):**
   - Generate 1 representative portrait first (typically Shot 2 or Shot 5) so the user can verify facial likeness, unified luminous-fair skin tone, head-to-shoulder proportions, and bridal high-crown volume before committing to the remaining frames.
3. **Optional Multi-Panel Storyboard Preview (`multi-panel-preview`):**
   - When the user explicitly prefers a fast 8-panel (or 4-panel) selection grid first before enlarging favorite frames:
     - Enforce crisp panel borders, exact panel count (8 distinct frames, zero narrow strips), and zero duplicated poses.
     - **Mandatory Identity Lock v2 (`PANEL IDENTITY RESET`):** Prepend an explicit instruction before each panel's shot block requiring the model to reconstruct facial identity directly from the canonical original uploaded reference(s) independently per panel (never copying Panel N-1's generated face into Panel N).
     - **Face Readability Gate:** Ensure faces in wide, motion, or over-the-shoulder panels remain clearly readable.
     - Once the user picks favorite panel numbers (e.g., "放大 2、5、6"), render standalone 3:4 single images still anchored to the **canonical original reference(s)** (using the selected grid cell only as a composition/pose hint, never as the face source).

---

## Bilingual Prompt Assembly Blueprint

Native multimodal models follow structured natural-language instructions best. Compile each shot from `ShotPlan` in the layered priority order below:

### 1. Chinese Prompt Structure (`prompt_zh`)

```text
[参考图与头肩比融合底线 — 真人模式必含]
严格保留原始参考图人物真实五官、骨相与神态辨识度：正面锁定两眼间距、眼鼻嘴相对位置、面颊真实宽度与饱满度、下颌转折、下巴形状及原有左右微差异，默认几何瘦脸为 0（严禁自动收窄面颊或拉尖下颌）；斜角与侧颜按同一张脸保守做真实透视推演（参考图仅锁定身份，不锁死单一静态表情、不沿用原图僵硬站姿）。按当前会话策略处理参考图原物品（默认彻底清除参考图中的日常服饰、背景杂物与一切非婚纱手持物，如宣传册、卡片、手机、提袋等，除非用户明确指定保留某件纪念物）。头、颈与身体按原照可见的原生体量自然协调，优先靠 85mm 透视与顺畅颈肩衔接优化比例，既杜绝大头小身或贴脸感，也严禁为了纠偏把女生画成粗颈、厚肩或上身显壮。肤色采用统一清透白皙精修（或用户指定肤质档位），面部、下颌线、脖颈、锁骨与肩臂之间的肤色冷暖、白皙度、皮肤微纹理、受光方向与自然阴影过渡保持高度统一与无缝衔接。

[本帧分镜、微位点与视角 — 来自 ShotPlan.shots[i]]
第 {shot_index} 帧（{role}）：场景微位点为 {micro_zone}；{framing}，{angle}（人像近中景优先 85mm 柔和奶油散景虚化背景，将清晰度与视觉焦点聚焦在两人真实五官上）。

[情侣主体与高颅顶妆造锁定 — 来自 continuity_anchors + bridal-aesthetics.md]
新娘：{bride_dress}，{bride_hairstyle}（{hair_design_details}），高颅顶造型，头顶发根自然蓬松饱满、发丝顺滑整洁有空气感，无贴头皮扁塌感，也避免毛躁炸开碎发切碎脸颊轮廓；{bride_makeup}；{bride_skin_finish}；{bride_veil_or_accessories}。
新郎：{groom_outfit}；{groom_hairstyle}。
手捧花与道具：{bouquet_and_props}（如有宠物，严格保留宠物参考照品种与毛色花纹）。

[双手动作、手持物指定、头纱动态与反应式情绪]
互动姿态：{pose}；新娘双手：{bride_hand_action}；新郎双手：{groom_hand_action}；手持物与动态：{handheld_prop_state}（例如头纱随风飘动具动态感、严禁残留参考图原日常手持物）；画面可见关键力学：{body_mechanics}；接触关系：{contact_topology}；表情与视线：{expression_gaze}；整体情绪氛围：{mood_tone}。

[场景、分场景摄影美学口号与光影质感锁定]
摄影美学定调：{aesthetic_tagline_zh}（按当前风格包从 catalogs/camera-and-lighting.yaml 自动匹配，而非一刀切强插）。
拍摄场地：{venue}；环境氛围：{atmosphere}；前景构图：{foreground}。
器材光影：{body_and_lens}；{lighting}；{color_temperature}；{film_texture}。画幅比例：{aspect_ratio}。

[规避项]
避免：{negative_prompt}。
```

### 2. English Prompt Structure (`prompt_en`)

```text
[Canonical Identity, Angle-Aware Facial Lock, Native Proportion & Unified Complexion Guardrail — Mandatory in Reference Mode]
Strictly preserve exact facial identity, inter-eye distance, relative eye-nose-mouth geometry, natural cheek width and fullness, jawline turn, chin shape, and natural left-right facial asymmetry directly from the original uploaded reference photo with zero geometric face slimming by default (conservatively project the same 3D facial structure for angled/profile turns; lock identity only, NOT the static reference expression, casual clothing, stiff stance, or everyday handheld items). Per session policy (default `replace-with-bridal-poses`), completely remove all casual clothes, background clutter, and non-wedding handheld items from the reference photo (brochures, pamphlets, cards, phones, bags) unless a specific keepsake was explicitly requested. Keep head, neck, shoulders, and torso naturally proportional to each subject's real visible build from the reference photo—using 85mm optical perspective and clean neck-root-to-shoulder blending with zero oversized-head distortion AND zero over-widened thick neck or bulky shoulders. Apply the selected skin finish (default unified luminous fair complexion preserving natural micro skin texture) seamlessly across face, jawline, neck, collarbones, and exposed shoulders with unified lighting and natural shadows.

[Frame Role, Micro-Zone, Framing & Camera Angle]
Frame {shot_index} ({role}) at micro-zone {micro_zone}: {framing}. Camera angle and optics: {angle} (favor creamy 85mm shallow depth-of-field bokeh on portrait frames so full clarity stays on the couple's authentic faces). Keep visible faces clearly readable (Face Readability Gate).

[Subject Styling & High-Crown Hair Continuity Lock]
Bride: {bride_dress}; {bride_hairstyle} ({hair_design_details}), voluminous high-crown hairstyle, naturally lifted roots with sleek, smooth, neatly groomed airy volume on top and clean face-framing curls (avoid messy frizzy flyaways cutting across cheeks), lush hairline without flat roots; {bride_makeup}; {bride_veil_or_accessories}.
Groom: {groom_outfit}; {groom_hairstyle}.
Bouquet & Props: {bouquet_and_props}.

[Pose, Explicit Hand Actions, Handheld Props, Veil Dynamics & Reactive Expression]
{pose}. Bride hands: {bride_hand_action}. Groom hands: {groom_hand_action}. Handheld prop & motion state: {handheld_prop_state} (e.g., wind-swept flowing veil dynamics; zero leftover reference-photo everyday objects). Key visible body mechanics: {body_mechanics}. Contact topology: {contact_topology}. Expression and gaze: {expression_gaze}. Emotional mood: {mood_tone}.

[Location, Scene-Matched Aesthetic Direction Tagline, Lighting & Film Grade Lock]
Aesthetic direction tagline: {aesthetic_tagline_en} (automatically matched to the active style family in catalogs/camera-and-lighting.yaml).
Location: {venue}. Atmosphere: {atmosphere}. Foreground: {foreground}.
Photography specs: {body_and_lens}, {lighting}, {color_temperature}, {film_texture}. Aspect ratio {aspect_ratio}.

[Avoid]
{negative_prompt}.
```

---

## Dual-Anchor Delta Refinement Protocol & Proactive User Reminder (Phase 4)

Whenever the user wants to make subtle edits to a v1 generated frame without breaking parts they already love (e.g., fixing hair color, raising crown height, tweaking hand placement, or warming lighting), **ALWAYS**:

1. **Proactively Remind the User (Mandatory Notice):**
   > **微调防改坏提醒**：为避免二次修改把五官修漂移（只传第一版成片）或把满意的构图/背景改丢（只传原照），微调必须采用 **双图锚定 + 最小改动**：同时传入 **图 1（最初的真人原照，仅锁五官骨相）** 与 **图 2（第一版基本满意的成片，作为构图/服装/场景/光影底图）**，并在提示词中明确区分 `KEEP UNCHANGED` 与 `CHANGE ONLY`。*(若追求 99% 像素级局部不动，可改用 ComfyUI 局部重绘遮罩或 Midjourney Vary Region。)*
   - If the user uploads only a v1 image in a new conversation without their original photo, pause and ask them to also attach the original real photo before running the edit.
2. **Pass BOTH Images to the Generator Tool** (`Image 1 = canonical original photo`, `Image 2 = selected v1 frame`) and format the delta prompt explicitly:

```text
[Dual-Anchor Binding / 双图锚定]
Image 1 (图1): Canonical original real couple photo — use STRICTLY for exact facial identity, bone structure, glasses, and recognizable likeness.
Image 2 (图2): Selected v1 wedding frame — use as the locked base image for composition, framing, pose, wedding gown lace, tuxedo, bouquet, background scenery, lighting direction, and color tone.

[KEEP UNCHANGED / 严格锁定不动清单]
Keep identical to Image 2: camera framing, background architecture/scenery, lighting direction and 35mm film grain, groom's posture and tuxedo, bride's gown silhouette/lace/veil flow, bouquet, and seamless unified luminous-fair skin tone across face, neck, collarbones, and shoulders.

[CHANGE ONLY / 唯一允许改动的 1-2 处细节]
1. {specific_delta_1, e.g., Change bride's hair color to natural deep black and restore voluminous high-crown wavy hair with airy cheekbone tendrils, calibrating facial likeness tightly to Image 1}
2. {optional_delta_2}
Do NOT alter any other element outside the CHANGE ONLY list.
```

3. **Single-Variable Set Remix:** When the user asks to swap one macro dimension across the set (e.g., "只换场地" or "只换礼服"), follow `scripts/remix_resolver.py` to freeze unaffected modules verbatim instead of rewriting the whole session.
4. **Optional Social Share Card (`emit_share_card: true`):** When requested, output a clean 5-part share block (`《短标题》`, 1-2 sentence mood hook, copyable short invocation prompt, 4-7 `#hashtags`, and a natural invitation CTA) without internal workflow jargon.
