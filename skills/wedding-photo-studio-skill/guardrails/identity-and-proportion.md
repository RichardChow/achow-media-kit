# Guardrail: Identity Consistency and Head-to-Body Proportion Harmony

**Applies to:** Real Couple Reference Mode (Mandatory) and Virtual Couple Mode (Anatomical Realism Baseline).

## Problem Statement

When generating wedding photos from real couple reference images, image models often copy the uploaded face at its original visual weight while defaulting to an overly slim, narrow-shouldered fashion-model body template. This causes:

- Unnatural "big head / tiny body" (大头小身) head-to-shoulder distortion
- Overly thin, elongated, or misaligned necks
- Visible color temperature, skin-texture, or lighting seams between the jawline, neck, and collarbones ("pasted-on face" artifact)

## Mandatory Prompt Injection Rules

Always inject the following harmonized proportion and blending block into every shot when a reference photo is supplied:

### Chinese Prompt Block

`严格保留参考图人物真实五官、骨相与神态辨识度；根据人物真实脸型大小与头部体量，自适应匹配自然协调的写实身材骨架、肩宽与脖颈粗细，建立真实舒展的头肩比与头身比，严禁出现大头小身、极窄溜肩或生硬换头贴脸感；面部、下颌线、脖颈、锁骨与肩臂之间的肤色冷暖、皮肤微纹理、受光方向与阴影过渡保持高度统一与自然无缝衔接。`

### English Prompt Block

`Strictly preserve exact facial identity, bone structure, and recognizable likeness from the reference photo while dynamically adapting realistic, anatomically harmonious head-to-shoulder and head-to-body proportions suited to each subject's natural face scale; match authentic neck thickness, natural shoulder width, and balanced torso frame with zero oversized-head, overly narrow shoulders, or pasted-on face artifacts; ensure seamless anatomical and lighting continuity across face, jawline, neck, collarbones, and shoulders with unified skin tone, natural skin texture, and consistent light-and-shadow falloff.`

## Visual Composition and Styling Synergy (Soft Optimization Without Altering Identity)

Without modifying the couple's authentic facial features, leverage real studio photography techniques to make proportions look naturally flattering:

1. **Hair Framing Synergy:** Pair with `guardrails/bridal-aesthetics.md` (voluminous high crown + airy face-framing side strands) to balance facial width naturally.
2. **Neckline Guidance (Offer in Phase 2 Styling Menu):**
   - **Recommended for balanced head-to-shoulder ratio:** Off-the-shoulder (一字肩), French square neckline (法式方领), V-neck (V领), sweetheart strapless with natural shoulder line (抹胸心形领), draped sleeves (落肩袖) to visually broaden shoulders and elongate the neck gracefully.
   - **Use cautiously:** Tight high-collar/choker necklines that visually shorten the neck and emphasize head scale unless specifically requested.
3. **Lens and Angle Strategy:**
   - Favor 50mm-85mm medium-telephoto natural compression rather than wide-angle close-ups (which exaggerate head size).
   - Use 3/4 subtle body angles, natural posture turns, and soft translucent veil layering near the jawline/shoulders rather than rigid dead-center straight-on mugshot framing.
4. **Couple Height and Scale Harmony:** Ensure the groom's head scale and shoulder breadth stay anatomically proportional relative to the bride's head scale so neither partner appears artificially shrunken or enlarged in shared shots.
5. **Native Head-Neck-Body Harmony & Anti-Bulky Rollback (原生比例协调与防厚肩显壮回退):**
   - When a subject's face is naturally fuller or slightly larger, **preserve their true facial structure first** and check lens perspective (50mm-85mm compression) and head-to-torso depth position before changing body proportions.
   - Ground shoulder width and torso volume in the subject's **actual visible build from the reference photo**; refine only the smooth anatomical transition at the neck root and shoulder line.
   - **Rollback Trigger:** Never over-correct "big head / tiny body" into a **thick neck, overly broad shoulders, or bulky/stocky upper body (粗颈、厚肩、上身显壮)**. If an adjustment produces a bulky torso look, immediately roll back toward the subject's authentic build.

## Angle-Aware Facial Structure Lock & Optional Subtle Contour (按角度保脸结构规则)

1. **Front-Facing Default Lock (正面照默认锁定原脸结构 · 几何瘦脸 = 0):**
   - Anchored strictly to the canonical original photo, lock **inter-eye distance (两眼间距), relative eye-nose-mouth positions (眼鼻嘴相对位置), natural cheek fullness and width (面颊宽度与饱满度), jawline turn (下颌转折), chin shape (下巴形状), and natural left-right facial asymmetry (原有左右微差异)**.
   - Allow natural smiles/expressions, bridal makeup, and lighting changes, while keeping **default geometric face slimming = 0** (`face_contour_mode: "none-zero-slimming"`). Do NOT inject face-slimming keywords into prompts by default.
   - **ZH Lock Snippet:** `严格锁定原照两眼间距、眼鼻嘴相对位置、面颊真实宽度与饱满度、下颌转折、下巴形状及原有左右微差异，正面默认几何瘦脸为0，严禁自动收窄面颊或拉尖下颌。`
   - **EN Lock Snippet:** `Strictly preserve original inter-eye distance, relative eye-nose-mouth geometry, natural cheek width and fullness, jawline turn, chin shape, and natural left-right facial asymmetry with zero geometric face slimming or cheek narrowing.`
2. **Side-Profile & Angled Shots (侧脸与斜角照保守透视推演):**
   - If the user supplied a matching-angle reference photo, prioritize that reference for that angle.
   - When only a front-facing reference photo exists, conservatively project the same 3D facial volume into the turn angle—preserving physically consistent near/far occlusion, cheek fullness curve, and nose-bridge-to-chin geometry so the angled face unmistakably reads as the same person.
3. **Optional Subtle Cheek Soft-Contour (`face_contour_mode: "subtle-soft-contour"`):**
   - Default styling relies strictly on sleek hair framing, soft lighting, and 85mm lens perspective (`none-zero-slimming`).
   - Only when the user explicitly opts into subtle slimming: permit minimal cheek soft-tissue refinement while strictly preserving jawline turn, chin shape, and feature spacing.
   - **Prompt vs. QA Separation:** Do NOT write literal percentages (like "2%") into image generation prompts (diffusion models misinterpret slimming keywords). Enforce the trial QA cap during visual review in `guardrails/set-continuity-qa.md`: **after aligning original and output at eye level, total bilateral cheek width reduction must not exceed 2% (use less whenever possible), and immediately roll back to 0 if recognizability drops.**

## Unified Luminous-Fair Complexion Harmony (整体同步白皙与面颈统一规则)

Bridal photography commonly favors a bright, luminous fair complexion (**默认清透白皙精修**). **Uniformity—not avoiding fairness—is the core anti-seam principle:**

- Apply the exact same skin brightness, color temperature, gentle blemish softening, natural fine skin texture, and light-shadow falloff **simultaneously across the face, jawline, neck, collarbones, shoulders, and exposed arms**.
- Never brighten or smooth only the face while leaving the neck or shoulders darker/redder (which creates a visible "mask/pasted head" boundary).
- Users may switch between `luminous-fair-unified` (default recommended), `studio-soft-glow` (soft-focus couture fair glow, uniformly synced across face-neck-shoulders), or `natural-authentic` (original skin tone with subtle lighting polish) in Phase 2.

## Canonical Identity Lock, Expression De-Locking & Face Readability

Adapted from battle-tested real-couple orchestration safeguards (with credit to `yang0/handraw-style`):

1. **Canonical Original Identity Reference Lock:**
   - The user's **initially uploaded real couple (and pet) photo(s)** remain the canonical identity anchor across all batches, remixes, enlargements, and follow-up turns.
   - AI-generated derived frames (earlier shots, contact sheets, or previews) may ONLY assist scene/garment/composition continuity and must **never** silently replace the original uploaded photo as the facial identity reference unless the user explicitly promotes a derived image.
2. **Expression De-Locking (只锁身份，不锁表情):**
   - Preserve bone structure, eye spacing, nose bridge, jawline, and recognizable likeness from the reference photo, **NOT** its single static smile, mouth shape, or gaze direction. Vary genuine reactive expressions across shots per the shot plan.
3. **Face Readability Gate (高风险镜头人脸可读性门槛):**
   - In wide establishing shots, walking motion, over-the-shoulder turns, or mirror/water reflections where faces are intended to be visible, maintain enough facial scale and natural head angle so both identities stay clearly recognizable rather than shrinking or twisting into blurry blurs.
4. **Multi-Panel `PANEL IDENTITY RESET` (When User Selects Optional Multi-Panel Preview):**
   - Whenever the user opts for an 8-panel / multi-panel storyboard preview, instruct the generator to reset facial identity directly from the canonical reference photo(s) **independently in every panel** so Panel N never drifts by copying Panel N-1.
5. **Reference Pose, Hands & Handheld-Object Cleanup Policy (参考图原姿态、手部与原手持物清理/保留可选项):**
   - Image-editing models (especially GPT Image / multimodal edit models) often lazily copy-paste casual clothes, stiff straight-on standing poses, and everyday handheld items (tourist brochures, pamphlets, phones, drinks, bags) directly from the uploaded reference photo into the generated wedding photo.
   - Always apply the session's `reference_pose_and_props_policy` (user-selectable in Phase 2):
     - **`replace-with-bridal-poses` (Default Recommended):** Extract facial identity ONLY; **completely remove casual clothing, background clutter, and all everyday handheld items from the reference photo (pamphlets, brochures, phones, cards, bags)**; discard the static reference pose and explicitly assign **bride's hands, groom's hands, bridal bouquet/props, and dynamic flowing veil** for every shot.
     - **`keep-reference-pose-only` (Optional):** Keep the couple's original gesture/stance from the reference photo, but remove casual everyday objects and replace them with empty clasped hands or bridal bouquet/veil.
     - **`keep-reference-keepsake` (Optional):** Keep a specific meaningful keepsake named by the user from the reference photo (e.g., marriage certificate, concert ticket, plushie), while upgrading everything else into bridal styling and scenery.
   - **Default Cleanup Injection Block (ZH):** `参考图仅用于提取人物真实五官身份；彻底清除参考图中的日常服饰、背景杂物与一切非婚纱手持物（如宣传册、纸张、手机、提袋等），不得沿用原图僵硬持物站姿；严格按本帧设计重新安排新娘双手动作、新郎双手动作、手捧花持握方式与头纱随风飘动动态。`
   - **Default Cleanup Injection Block (EN):** `Use the reference photo strictly for facial identity only; completely remove all casual clothing, background clutter, and non-wedding handheld objects from the reference photo (such as brochures, pamphlets, cards, phones, or bags) and discard the reference photo's static pose; explicitly render fresh natural bridal hand placement, bouquet holding, couple eye contact, and wind-swept flowing veil dynamics as directed for this frame.`
