# Adapter: Midjourney (v6.1 / v7)

**Target Engine:** Midjourney Web / Discord (`--v 6.1` or `--v 7`)

**Adapter ID:** `midjourney`

---

## Translation Principles

Midjourney responds best to concise, visually vivid English photography clauses rather than lengthy meta-instructions. When compiling a `ShotPlan` for Midjourney:

1. **Front-Load Framing, Subject, and Lighting:** Place shot scale, angle, couple styling, and high-crown hair volume in the first 40 words where attention weights are highest.
2. **Translate Guardrails Into Visual Photography Language:**
   - Replace abstract instructions like "do not paste face" with affirmative optical descriptions (`anatomically natural head-to-shoulder proportions, realistic neck thickness and natural shoulder width, unified sunlit skin tone across face, neck, and collarbones, 85mm portrait compression`) plus concise `--no` exclusions.
   - Always keep `voluminous high-crown bridal hairstyle with naturally lifted airy roots and face-framing strands` explicitly near the bride's description.
3. **Use `--style raw` for Documentary Realism:** Reduces synthetic plastic skin gloss and improves authentic film texture.

---

## Prompt Compilation Template

```text
{framing}, {angle}, {couple_description}, bride wearing {bride_dress_en}, {bride_hairstyle_en}, voluminous high-crown hairstyle with naturally lifted roots and airy face-framing strands, {bride_makeup_en}, {veil_en}, groom wearing {groom_outfit_en}, holding {bouquet_en}, {pose_en}, natural anatomically harmonious head-to-shoulder proportions and realistic neck-to-shoulder seamless skin lighting, set at {venue_en}, {atmosphere_en}, {foreground_en}, {lighting_en}, {color_temperature_en}, {film_texture_en}, {en_style_keywords} --ar {aspect_ratio} --style raw --stylize 180 --no flat pasted hair, oversized head, tiny narrow shoulders, stiff neck seam, plastic skin, duplicate faces, deformed hands, watermark, text
```

---

## Parameter Reference Table

| Parameter | Recommended Value | Notes |
| --- | --- | --- |
| `--ar` | `3:4` (default), `2:3`, `9:16`, `16:9` | Match `SessionState.camera_and_delivery.aspect_ratio` |
| `--style raw` | Always enabled for photorealism | Prevents overly polished CGI/illustration look |
| `--stylize` (`--s`) | `150` - `220` | Higher stylize drifts outfits/faces; keep moderate for set continuity |
| `--sref <url>` | Style anchor URL (optional) | Feed Shot 1 or Shot 2 URL into Shots 3-8 with `--sw 150` to lock lighting & film palette |
| `--cref <url>` | Character reference URL | Effective for solo portraits (e.g., Shot 6 Bride Solo Hero) with `--cw 80` to keep face while allowing outfit adaptation |
| `--no` | Concise negative terms | Keep under 12 crisp visual phrases (do not use punctuation-heavy sentences inside `--no`) |

---

## Real Couple Reference Mode Caveat in Midjourney

- Standard single `--cref` works cleanly on solo portraits (such as Shot 6) but can blend features across two people in a shared couple frame.
- For two-person real couple sessions in Midjourney:
  1. Generate clean base compositions with consistent `--sref` and locked wardrobe descriptions.
  2. Apply Midjourney **Editor / Vary (Region)** or **Omni Reference** per individual face/bust where supported, preserving exact lighting temperature and natural neck-to-shoulder continuity.
  3. If strict dual-face likeness in one pass is critical, recommend switching back to `adapters/native-multimodal.md` or `adapters/flux-comfyui.md` with regional dual-PuLID conditioning.
