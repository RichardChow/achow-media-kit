# Guardrail: Multi-Angle Set Continuity and Quality Assurance

**Applies to:** All multi-shot sets (8-angle cinematic default, 4-angle editorial, or custom N-shot sequences), both during Phase 3 prompt compilation and Phase 4 post-render QA.

## Objective

A commercial-grade wedding photo set must look like it was photographed in a single real session by one photographer on one day—meaning **subjects, garments, accessories, props, and atmosphere stay 100% locked**, while **framing, camera angle, lens perspective, and micro-interactions vary distinctly** across every shot.

## 7-Point Mandatory Continuity Checklist

Validate every compiled `ShotPlan` and every generated image batch against these seven checkpoints:

### 1. Facial Identity Consistency (人脸一致性)
- [ ] Both the bride and groom remain unmistakably the same individuals across all shots (especially in Real Couple Reference Mode).
- [ ] Micro-expressions change naturally (candid laugh, gentle gaze, serene closed-eye smile) without drifting facial geometry, nose bridge, eye spacing, or age.
- [ ] Groom's hairstyle matches the locked session setting (original groomed reference hairstyle in Real Photo Mode unless explicitly changed).

### 2. Head-to-Shoulder Ratio & Neck Blending Naturalness (头肩比与脖颈衔接自然度)
- [ ] Verify against `guardrails/identity-and-proportion.md` on every shot, especially medium close-ups and full-body frames.
- [ ] Zero "oversized head on tiny frail shoulders" (大头小身) distortion.
- [ ] Face, jawline, neck, collarbones, and exposed shoulders share unified skin tone, temperature, fine skin texture, and light-shadow falloff with zero pasted-on seam.
- [ ] Couple height difference and relative head scale stay anatomically consistent across all two-person shots.

### 3. Bridal High-Crown Consistency (新娘高颅顶与发式统一)
- [ ] Verify against `guardrails/bridal-aesthetics.md` on every shot featuring the bride.
- [ ] Every angle (front, 3/4, side profile, low angle, high angle) preserves lifted, airy crown volume and face-framing strands.
- [ ] Hair color, curl texture, hair accessories, and veil anchor position do not randomly morph between shots.

### 4. Dress Lace, Cut & Veil Embroidery Consistency (礼服蕾丝与头纱刺绣一致)
- [ ] Wedding dress silhouette, neckline cut, bodice texture (e.g., 3D floral lace vs. clean French satin), sleeve structure, and skirt volume remain identical across frames.
- [ ] Veil length, translucency, and edge embroidery pattern match across wide, medium, and close-up shots.
- [ ] Groom's suit color, lapel style, shirt collar, and bow tie / necktie stay locked.

### 5. Bouquet Floral Species & Count Consistency (捧花花材与数量一致)
- [ ] Bouquet flower variety, color palette, stem wrap, and approximate bloom count (e.g., 15 blush pink roses with fresh greenery) stay identical whenever visible.
- [ ] Props (umbrella, vintage camera, silk fan, champagne glasses, etc.) do not appear or disappear illogically or change material mid-set.

### 6. Color Temperature, Lighting & Atmosphere Consistency (色温光影与环境一致)
- [ ] Sun direction / primary key light side remains physically coherent across the sequence (e.g., warm 5500K golden sunrise backlight throughout a sunrise pack).
- [ ] Sky tone, terrain foreground, architectural details, and film grain profile (e.g., Kodak Portra 400 soft contrast) stay unified across the entire set.

### 7. Zero Duplicated Angles or Poses (机位角度与动作零重复)
- [ ] No two frames share the same shot scale + camera angle + body orientation.
- [ ] Every frame fulfills its distinct narrative slot from the active shot matrix (e.g., `matrices/8-angle-cinematic.yaml`).
- [ ] Hand placement, gaze direction, veil movement, and body orientation progress naturally like a cinema storyboard.

## 8-Column Directing Table & Quantitative Diversity Quotas

Before writing final frame prompts for a 6-9 shot set, verify the sequence against this 8-column directing table (absorbing best practices from `ai-wedding-photo-skill` and `couple-photo-orchestrator`):

| Frame | Story Beat | Micro-Zone | Shot Size & Angle | Visible Body Mechanics (2-4 pts) | Couple Contact Topology | Expression & Gaze | Prop / Light Continuity |
| --- | --- | --- | --- | --- | --- | --- | --- |

### Hard Diversity & Anti-Repetition Quotas (6-9 Shot Sets)
- **Adjacent Frame Delta:** Every consecutive pair of frames must differ in at least **4 columns** of the directing table.
- **Direct-to-Camera Cap:** At most **2 frames** looking directly into the camera; favor mutual eye contact, candid laughter, quiet glances, and absorbed interaction.
- **Formal Side-by-Side Standing Cap:** At most **2 frames** in formal side-by-side standing posture.
- **Breadth Minimums:** At least **5 distinct concrete actions**, **4 distinct expression/gaze patterns** (expression de-locked from reference photo), and **3 distinct camera heights/viewpoints** (eye-level, low angle, high/overhead, or framed foreground).
- **Pose-Family Semantic Dedupe:** Swapping only a prop or surface (e.g., leaning on a wall vs. leaning on a railing with the exact same weight distribution and torso axis) still counts as the same pose family and must be redesigned.
- **Framing-Adapted Body Mechanics Only:** Write only **2-4 key mechanics visible inside the frame** (full-body = stride/weight/skirt flow; waist-up = shoulder drop/torso twist/hands/neck line; close-up = head tilt/jawline/gaze/visible fingers). Never describe unseen feet in a close-up.
- **Face Readability Gate:** Confirm wide, motion, over-the-shoulder, and reflection frames still preserve readable, recognizable facial likeness.

## Cross-Batch Continuity Locking Protocol

When generating an 8-shot set in batches (recommended: Batch 1 = Shots 1-4, Batch 2 = Shots 5-8):

1. Copy the exact `continuity_anchors` block from `ShotPlan` verbatim into every shot prompt in both batches.
2. When supported by the image generation tool, pass the original couple reference photo(s) on **every single call** (and optionally pass the cleanest Shot 2 or Shot 5 output as a garment/environment anchor without overriding original facial identity).
3. Never paraphrase dress lace details, bouquet counts, or lighting Kelvin temperature differently between Batch 1 and Batch 2.

## Post-Render 4-Step Structural Diagnostic Audit (4 步结构化脸型与比例验收法)

Before blaming framing or crop size when a generated portrait feels slightly "off," run this exact 4-step diagnostic audit to pinpoint whether the issue is **facial geometry**, **body over-broadening**, **angle perspective**, or **lighting/hair**:

1. **Step 1 — Front Eye-Level Alignment & Facial Geometry Check (正面照按眼位对齐复核):**
   - Align the canonical original photo and output frame at eye level.
   - Verify exact preservation of **inter-eye distance, eye-nose-mouth positions, cheek fullness/width, jawline turn, chin shape, and natural left-right asymmetry**.
   - Default mode (`none-zero-slimming`): **0% geometric face slimming**.
   - Optional `subtle-soft-contour` mode: verify **total bilateral cheek width reduction <= 2% trial ceiling** (use less whenever possible) with zero bone/jaw/eye-spacing shift; if likeness drops at all, **roll back immediately to 0%**.
2. **Step 2 — Neck & Shoulder Over-Broadening Check (颈肩原生比例双向检查):**
   - Check BOTH failure directions: zero "oversized head on tiny frail shoulders" **AND** zero over-corrected "thick neck, widened shoulders, or stocky/bulky upper body (粗颈/厚肩/显壮)". Torso volume must stay faithful to the reference photo's visible build.
3. **Step 3 — Angled & Side-Profile Perspective Check (斜角/侧脸透视与遮挡检查):**
   - Verify near/far facial occlusion, cheek contour turn, and nose-to-chin geometry are physically explained by head rotation and still clearly read as the exact same person.
4. **Step 4 — Unified Jawline-Neck-Clavicle Lighting & Neat Hair Check (下颌/颈侧/锁骨光影与顺滑发丝检查):**
   - Verify jawline, side of neck, collarbones, and shoulders share one coherent lighting direction, unified skin tone, and natural soft shadows—and bridal high-crown hair stays smooth/neat rather than frizzy flyaways cutting across the cheeks.

## Post-Render Remediation Actions

If any generated shot fails a checkpoint:

- **Identity or proportion drift:** Re-shoot only the failed shot index using a slightly narrower focal perspective (`85mm` natural compression), reinforcing `guardrails/identity-and-proportion.md`, and shifting from straight-on to a 3/4 subtle body angle.
- **Flat hair crown:** Re-shoot with reinforced high-crown hair prompt block and backlit hair-rim highlights.
- **Duplicate framing:** Re-shoot by explicitly contrasting camera elevation (low angle vs. high angle) and distance (wide vs. tight detail).
