# Adapter: Flux & ComfyUI Pipeline

**Target Engines:** Flux.1 Dev / Flux.1 Pro / Flux.1 Kontext inside ComfyUI (optionally paired with PuLID-Flux, IP-Adapter, Redux, or ControlNet OpenPose/Depth).

**Adapter ID:** `flux-comfyui`

---

## Translation Principles

1. **Natural Descriptive Prose Over Tag Soup:** Flux uses a T5-XXL text encoder that understands nuanced anatomical, optical, and spatial relationships in natural sentences far better than comma-separated tag spam.
2. **Affirmative Proportion Framing:** Because Flux Guidance (distilled CFG) does not always apply traditional negative prompts unless true CFG is enabled, state all proportion and bridal high-crown guardrails as clear positive photographic truths inside the primary prompt.
3. **Explicit Left/Right Spatial Separation:** Clearly specify `on the left` and `on the right` (or `foreground` / `background`) so clothing, hair, and dual-subject identity adapters do not bleed across bride and groom.

---

## Recommended ComfyUI Parameters

| Setting | Recommended Value | Notes |
| --- | --- | --- |
| **Resolution (`3:4`)** | `896 x 1152` or `1024 x 1360` | Divisible by 16; crisp facial fidelity without OOM |
| **Resolution (`2:3`)** | `896 x 1344` | Full-frame vertical portrait ratio |
| **Resolution (`16:9`)** | `1344 x 768` | Widescreen cinematic establishing frames |
| **Sampler / Scheduler** | `euler` + `simple` (or `beta`) | Clean skin micro-texture and natural Kodak film grain |
| **Steps** | `24` - `30` | Sweet spot for lace embroidery and hair strand separation |
| **Flux Guidance** | `2.5` - `3.2` | Above `3.8` tends to over-sharpen skin and stiffen neck shadows |
| **CFG (if True CFG enabled)** | `1.0` (standard distilled) or `2.0` (with negative prompt) | Keep subtle to avoid waxy faces |

---

## Prompt Compilation Template (Flux Natural Prose)

```text
A candid 35mm film wedding photograph captured on {body_and_lens}. {framing_sentence} {angle_sentence}.

On the left/right, the bride wears {bride_dress_en}. Her hair is styled in {bride_hairstyle_en} featuring a voluminous high-crown silhouette with naturally lifted airy roots, flattering face-framing strands, and zero flatness on top. Her makeup is {bride_makeup_en}, accented by {veil_en}. Beside her, the groom wears {groom_outfit_en} with {groom_hairstyle_en}, holding {bouquet_en}.

Both subjects exhibit realistic, anatomically harmonious head-to-shoulder and head-to-body proportions suited to their natural facial scale, with authentic neck thickness, natural relaxed shoulder breadth, and completely seamless skin-tone, micro-texture, and shadow continuity across the face, jawline, neck, collarbones, and exposed shoulders.

Action and emotion: {pose_en}, radiating {mood_tone_en}.

Environment and lighting: Photographed at {venue_en}, surrounded by {atmosphere_en}, with {foreground_en} in the foreground. Illuminated by {lighting_en} at {color_temperature_en}, rendered with {film_texture_en}.
```

---

## Dual-Subject Real Couple Reference Wiring (ComfyUI)

To prevent identity mixing or "big head on frail body" distortion in ComfyUI:

1. **Identity Conditioning (Dual Masked PuLID-Flux / Flux Kontext):**
   - Route Bride reference photo (`weight: 0.75-0.85`, start step `0.05`, end step `0.85`) into the bride's attention mask.
   - Route Groom reference photo (`weight: 0.75-0.85`, start step `0.05`, end step `0.85`) into the groom's attention mask.
   - Delaying start step slightly (`0.05`) lets Flux establish natural anatomical shoulder-to-head proportions first before locking exact facial identity!
2. **Garment & Set Continuity Lock:**
   - Pass Shot 2 (classic medium full shot) into a low-weight **Flux Redux** (`strength: 0.25-0.35`) for Shots 3-8 to keep lace embroidery, bouquet roses, and golden sunrise tone coherent across all 8 angles.
3. **Optional Post-Pass:**
   - Run a gentle `0.20-0.28` denoise Detailer/Upscale pass focusing on eyes, lace filigree, and soft film grain—never push face-restore strength above `0.35` so neck-to-face skin texture remains unified.

---

## Negative Prompt Mapping (For True-CFG / SDXL Hybrid Workflows)

```text
flat pasted hair, deflated scalp, oversized head on tiny narrow body, frail distorted shoulders, pasted-on face, visible neck seam, mismatched face and neck skin color, plastic airbrushed skin, wide-angle facial distortion, extra fingers, duplicated couple poses, muddy lace texture, text, watermark
```
