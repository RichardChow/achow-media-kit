# Adapter: Chinese & Multimodal Domestic Platforms (即梦 / 豆包 / Nano Banana)

**Target Engines:** 即梦 (Jimeng / Dreamina), 豆包 (Doubao), Nano Banana (Gemini Native Image Editing / Generation), and similar natural-language Chinese-first image platforms.

**Adapter ID:** `cn-platforms`

*(Adapted and expanded from community platform insights in `wenyachen/ai-wedding-photo-skill` with full Wedding Photo Studio proportion and bridal high-crown guardrails.)*

---

## Universal Principles Across All Three Platforms

1. **Always Prefer Natural Prose Over Foreign Parameter Syntax:** Do **NOT** append Midjourney flags (`--ar`, `--stylize`, `--no`, `--v`) or Stable Diffusion weight syntax (`(high crown:1.3)`). Express aspect ratio in the UI selector (default `3:4`) and state exclusions as direct Chinese natural-language sentences.
2. **One Self-Contained Prompt Per Frame (Recommended) or Explicit Panel Reset:** Repeat the core identity mapping, proportion/neck blending guardrail, bridal high-crown rule, unified luminous-fair skin tone rule, and locked wardrobe details in every single standalone prompt.
3. **Explicitly Bind Uploaded Reference Order:** Clearly identify which uploaded image corresponds to the bride, groom, and any pet (e.g., `图1为新娘与新郎真人参考照` or `图1为新娘、图2为新郎、图3为宠物`). Keep canonical original photos attached on every generation—never let an AI-generated preview silently replace original facial references.

---

## 1. 即梦 (Jimeng / Dreamina)

**Style Strength:** Excels at fluent Chinese cinematic descriptions, oriental & French lighting atmospheres, and fine hair/veil movement.

### Prompt Structure
```text
以参考图人物为唯一面部身份依据（图1为新人/图1新娘图2新郎），正面严格锁定原照两眼间距、眼鼻嘴相对位置、面颊真实宽度与饱满度、下颌转折、下巴形状及原有左右微差异，默认几何瘦脸为 0（严禁自动收窄面颊或拉尖下颌），斜角与侧颜按同一张脸保守透视推演，参考图仅锁身份不锁死单一表情。头、颈与肩身按原照原生体量自然协调，靠 85mm 透视与顺畅颈肩衔接优化比例，既杜绝大头小身或生硬贴脸感，也严禁为了纠偏画成粗颈、厚肩或上身显壮；新娘采用整体清透白皙精修，面部、下颌线、脖颈、锁骨与肩臂同步匀净白皙且保留自然皮肤微纹理与柔和阴影，无面颈色差。

画面内容（第{shot_index}张·{role}）：{framing}，{angle}，人物位于{micro_zone}（人像优先 85mm 浅景深奶油虚化背景聚焦五官）。
新娘造型：{bride_dress}，{bride_hairstyle}，高颅顶造型，头顶发根自然蓬松饱满、发丝顺滑整洁有空气感，无贴头皮扁塌感，也不要毛躁炸开碎发切碎脸颊轮廓；{bride_makeup}；{veil_or_accessories}。
新郎造型：{groom_outfit}；{groom_hairstyle}。
捧花与道具：{bouquet_and_props}。
互动动作与情绪：{pose}；新娘双手：{bride_hand_action}；新郎双手：{groom_hand_action}；手持物与动态：{handheld_prop_state}（彻底清除参考图原宣传册/手机等日常手持物，除非用户指定保留）；{contact_topology}；{expression_gaze}；整体氛围：{mood_tone}。
场景与光影：{aesthetic_tagline_zh}；{venue}，{atmosphere}，前景{foreground}；{body_and_lens}，{lighting}，{color_temperature}，{film_texture}。

画面要求：不要改变两人真实面部特征，不要出现扁塌贴头皮发顶、大头小身或面颈肤色割裂，不要生成多余手指、额外路人或水印文字。
```

### Usage Tips
- 在界面直接选择 **3:4 竖图**，逐张运行编号 1-8 提示词（如需先验证方向，可先用第 2 帧或第 5 帧试跑一张确认五官与头肩比）。
- 若用户明确选择在即梦生成 **8 宫格选片板**，在开头补充：`生成一张清晰独立的8宫格选片预览板，每格独立从原始参考图恢复人物真实五官，禁止跨格脸部漂移`。

---

## 2. 豆包 (Doubao)

**Style Strength:** Strong instruction-following for conversational Chinese art direction, gentle portrait aesthetics, and family/pet storytelling.

### Prompt Structure
```text
请以我上传的真人照片作为人物面部身份参考（{reference_binding}），生成一张{aspect_ratio}竖版电影感婚纱照（第{shot_index}帧：{role}）。

人物与比例保护：严格保持参考图人物的真实脸型、五官比例与辨识度，同时按镜头情绪自然变化微表情与眼神，不要死板复制参考图原表情；按真实脸型大小自然匹配写实肩宽、脖颈粗细与舒展头身比，杜绝大头小身或贴脸感；整体肤色采用统一清透白皙精修，面部、脖颈、锁骨与裸露肩臂肤色纹理与受光过渡完全一致。

造型锁定：新娘穿{bride_dress}，{bride_hairstyle}（必须高颅顶造型，头顶发根自然蓬松饱满、头包脸修饰轮廓、无贴头皮扁塌），{bride_makeup}，佩戴{veil_or_accessories}；新郎穿{groom_outfit}，{groom_hairstyle}；道具锁定{bouquet_and_props}。

分镜与互动：{framing}，{angle}，位于{micro_zone}。两人动作：{pose}（{body_mechanics}），{expression_gaze}。
场景与质感：{venue}，{atmosphere}，前景为{foreground}。{body_and_lens}，{lighting}，{color_temperature}，{film_texture}。

禁忌：不要更换人物五官、不要改变宠物花纹品种（如有宠物）、不要出现扁塌贴头皮发型、不要出现塑料磨皮或脸白脖子黑、不要出现文字水印。
```

---

## 3. Nano Banana (Gemini Native Image Generation / Editing)

**Style Strength:** Exceptional multimodal spatial reasoning, faithful facial identity retention across multiple attached reference images, and crisp bilingual comprehension.

### Prompt Structure
- Prefer **Chinese + English hybrid or crisp English** with explicit reference-image binding at the very top (`Image 1 = bride & groom canonical reference`, optional `Image 2 = pet canonical reference`).
- State exclusions as clear affirmative + direct negative instructions (e.g., `Keep exact facial structure and likeness from Image 1; do not shrink shoulders into a frail tiny frame; do not flatten the bridal hair crown; do not leave any skin-tone seam between face, neck, and shoulders`).
- Follow the exact layered blueprint in `adapters/native-multimodal.md`—either **individual 3:4 frames in batches of 4** (recommended default) or **optional 8-panel selection preview with per-panel `PANEL IDENTITY RESET`**.

---

## 4. 二次微调防改坏双图提醒（即梦 / 豆包 / Nano Banana 通用）

当用户对第一版成片基本满意、只想微调 1–2 处细节（如发色、高颅顶、手部动作或色调）时，**必须主动提醒用户同时上传 2 张参考图**，禁止只传成片或只传原照：

- **图 1（最初上传的真人原照）**：仅负责锁定两人真实五官骨相，防止二次编辑越修越不像；
- **图 2（第一版基本满意的成片）**：作为底图锁定构图、站位、礼服、背景与光影。

### 中文双图微调模板
```text
请结合两张参考图进行最小化局部微调：
- 图 1（真人原照）：仅用于严格校准两位新人的真实五官、骨相与眼镜辨识度；
- 图 2（第一版成片）：作为严格锁定的底图。

【严格锁定不动（KEEP UNCHANGED）】
完全保持图 2 的整体构图、人物站位、婚纱蕾丝与头纱动态、新郎西装、手捧花、背景场景、光线方向与胶片色调，同时保持面部、下颌线、脖颈、锁骨与肩臂整体同步清透白皙无缝衔接。

【仅修改以下 1-2 处（CHANGE ONLY）】
1. {具体微调项，例如：仅将新娘发色调整为自然深黑并抬高颅顶蓬松度，同时按图 1 校准新娘五官相似度}
2. {可选第二处细微调整}
除上述明确指出的改动外，画面其余所有区域一律保持与图 2 一致，不要擅自改动。
```
