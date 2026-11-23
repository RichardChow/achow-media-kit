# Guardrail: Bridal Aesthetics and Mandatory High-Crown Hair Volume

**Applies to:** ALL Modes (Real Couple Reference Mode and Virtual Couple Mode), across every bridal hairstyle and every style pack.

## Problem Statement

Image generation models frequently render Asian and bridal hairstyles with flat, pasted-down crown roots—especially in backlit outdoor scenes, wind-swept shots, or tight updos. Flat crown hair:

- Visualizes the face as wider or heavier than it naturally is
- Weakens the "head-framing-face" (头包脸) sculptural contour prized in high-end bridal styling
- Degrades the premium couture finish of both modern minimalist and traditional Chinese bridal portraits

## Mandatory Global Injection Rule

Regardless of whether the bride chooses wavy curls (浪漫波浪卷), a low chignon (法式低盘发), a Hepburn high bun (赫本高丸子), woodland braids (森系编发), or a traditional Chinese bridal updo (中式发髻), **ALWAYS** inject the following high-crown block into every shot unless the user explicitly disables it in the current session:

### Chinese Prompt Block

`高颅顶造型，头顶发根自然蓬松饱满，头包脸修饰脸型轮廓，发丝轻盈有空气感，无贴头皮扁塌感`

### English Prompt Block

`voluminous high-crown hairstyle, naturally lifted roots with airy hair volume on top, flattering face-framing silhouette, lush hairline without flat roots`

## Hairstyle-Specific Adaptation Guide

Adapt how the high-crown lift is visually sculpted so it looks authentically styled by a master bridal hairstylist rather than exaggerated or wig-like:

| Hairstyle Category (发型类型) | High-Crown Execution (高颅顶落地细节) |
| --- | --- |
| **Romantic Wavy Curls (浪漫波浪大卷)** | Lifted crown roots with soft S-curve temple bangs (八字刘海/龙须碎发) framing the cheekbones; sunlit airy hair strands catching rim light. |
| **French Low Chignon / Bun (法式慵懒低盘发)** | Sculpted rounded volume at the top crown and back skull (饱满后脑勺), loose textured tendrils near ears, pearls or veil anchored cleanly beneath the crown swell. |
| **Hepburn High Bun (赫本高丸子/芭蕾盘发)** | Elevated smooth-yet-airy crown silhouette (avoiding slick-flat scalp), paired with delicate tiara/pearl comb positioned just forward of the high bun for regal proportion. |
| **Woodland / Fairy Braids (森系编发/半扎公主头)** | Softly teased crown roots with airy braided crown halo and delicate baby's-breath or silk ribbon woven through loose strands. |
| **Chinese Bridal Updo (中式发髻/秀禾盘发)** | Full, rounded high-crown base supporting phoenix coronet (凤冠) or gold hairpins (步摇) gracefully without flattening the hairline; soft sculpted side edges (微弧度鬓角) framing the jawline. |
| **Minimalist Sleek / Half-Up (韩系极简半扎/清透直卷)** | Invisible inner-root lift at the top and temples for natural "head-envelops-face" softness while keeping the surface clean and refined. |

## Synergy With Identity and Proportion Guardrail

- Always pair this rule with `guardrails/identity-and-proportion.md`.
- **Do NOT alter facial bone structure** to fake a smaller face; instead, let natural high-crown hair volume, softly curved hairline density, and airy side strands visually balance head-to-shoulder proportions naturally.
- Ensure veil attachment points sit naturally behind or beneath the high crown without crushing the top volume flat.

## Explicit Hair Styling Decisions (高颅顶之上的显式细节决策)

To prevent the generator from passively copying messy or theme-mismatched hair from a casual reference photo, explicitly specify three levers alongside the mandatory high crown:

1. **Fringe / Bangs Strategy (刘海策略):** Airy curtain bangs (八字空气刘海), soft cheekbone tendrils (龙须碎发), light French fringe, or clean lifted open forehead.
2. **Parting (发缝方式):** Soft off-center invisible zigzag part, gentle middle part, or clean swept-back crown volume.
3. **Ear & Neck Exposure (露耳露颈度):** Revealing pearl earrings and an elongated neck line (recommended for optimizing head-to-shoulder proportion) vs. sleek curls framing the collarbone transition.
4. **Sleek, Neat Airy Finish (发丝顺滑整洁 · 防毛躁炸发破坏脸颊辨识度):** Keep high-crown volume softly lifted yet **smooth, silky, and neatly groomed**. Avoid messy, frizzy, backlit flyaway strands cutting haphazardly across the cheeks (which visually break up authentic cheek contours and lower facial likeness).

## Unified Luminous-Fair Bridal Skin Finish (默认清透白皙精修)

- Default bridal finish is **`luminous-fair-unified` (自然清透白皙精修)**: bright, clean, healthy fair radiance with gentle blemish/dark-circle softening while preserving real fine skin texture—applied **identically across face, jawline, neck, collarbones, and exposed shoulders** to guarantee zero face-neck color seam.
- Optional overrides in Phase 2: `studio-soft-glow` (影楼柔焦白皙高定精修，面颈肩同步匀亮) or `natural-authentic` (原生肤色微整理).

## QA Rejection Criteria

Flag and regenerate any frame that exhibits:

- Hair glued tightly to the scalp with zero crown lift
- Unnatural helmet-like or oversized wig distortion
- Frizzy, messy flyaway hair cutting across the cheeks and distorting authentic facial contours
- Missing hair strand translucency in backlit shots
- Inconsistent hairstyle or veil placement between shots in the same set
