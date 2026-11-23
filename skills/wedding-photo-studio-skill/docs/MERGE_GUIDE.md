# External Repository & Asset Merge Guide (外部项目合入指南)

This guide defines the standard process for integrating wedding photography, couple portrait, or artistic portrait assets from external skills, prompt libraries, or open-source repositories into `wedding-photo-studio-skill/` cleanly—without breaking modular interfaces or weakening core aesthetic and proportion guardrails.

---

## 1. Architectural Mapping Rules (资产拆解映射表)

Never dump an external repository's raw prompt files or monolithic `SKILL.md` directly into this project. Instead, **decompose, sanitize, and map** each valuable component into its designated layer:

| External Asset Type (外部资产类型) | Target Destination (映射目标) | Cleaning & Adaptation Requirements (清洗适配要求) |
| --- | --- | --- |
| Complete themed wedding preset (e.g., vintage Hong Kong film, hand-drawn watercolor portrait, Icelandic glacier wedding) | `packs/<pack-id>.pack.yaml` | Copy `packs/_template.pack.yaml`, fill every field required by `schemas/style-pack.schema.json`, set `source.origin: adapted-external`, and populate `source.reference_url` & `source.license_note`. |
| New scenic locations, architectural venues, or studio backdrops | `catalogs/locations.yaml` | Add under the matching `group_id` / `category` with bilingual `name`, `venue`, `atmosphere`, and `foreground` fields. |
| New bridal dresses, Chinese attire, groom suits, hair/makeup styles, or props | `catalogs/styling-and-props.yaml` | MUST append `neckline_proportion_note` for dresses and `high_crown_adaptation` for any bridal hairstyle. |
| New mood presets or couple interaction poses | `catalogs/poses-and-moods.yaml` | Classify under `classic-ceremonial`, `dynamic-candid`, or `intimate-documentary` and add `proportion_friendly_tip`. |
| New lighting setups, film emulations, or lens presets | `catalogs/camera-and-lighting.yaml` | Specify Kelvin `color_temperature`, optical `proportion_note`, and bilingual prompt blocks. |
| Distinctive multi-shot storyboards (e.g., 6-angle editorial, 9-angle documentary, hand-drawn comic strip) | `matrices/<matrix-id>.yaml` | Follow the structure of `matrices/8-angle-cinematic.yaml` with `role`, `framing`, `angle`, `pose_guidance`, and `guardrail_focus` per shot. |
| Platform-specific prompt syntax (e.g., new diffusion model or API) | `adapters/<platform>.md` | Document how standard `ShotPlan` objects compile into target prompts without changing `SKILL.md` workflow logic. |

---

## 2. Non-Negotiable Guardrail Policy (全局底线保护条款)

When adapting ANY external style pack or workflow:

1. **Identity & Proportion Blending (`guardrails/identity-and-proportion.md`) MUST remain enabled by default (`enforce_proportion_blending: true`).**
   - Strip away any upstream phrasing that forces fragile/anorexic body templates (e.g., "ultra-skinny narrow shoulders", "tiny doll body") which cause oversized-head distortion on real couple reference photos.
   - Even for stylized packs (such as watercolor, oil painting, or hand-drawn editorial illustration), maintain realistic head-to-shoulder proportion harmony relative to the real couple's faces.
2. **Bridal High-Crown Aesthetics (`guardrails/bridal-aesthetics.md`) MUST remain enabled by default (`enforce_high_crown: true`).**
   - Strip upstream terms that imply flat, slicked-down, scalp-clinging hair unless explicitly requested by the end user during an active session.
3. **Set Continuity & Anti-Repetition (`guardrails/set-continuity-qa.md`) MUST apply across multi-shot packs.**
   - Ensure every pack points `defaults.shot_matrix` to a valid matrix in `matrices/` and defines locked garment, bouquet, and lighting descriptions.
4. **No External Pack May Override `SKILL.md` Phase 2 Questionnaire:**
   - Merged packs automatically register as selectable options in Phase 2 while still allowing users to override any of the 5 modules in one line.

---

## 3. Licensing & Attribution Hygiene (开源协议与出处规范)

Before merging inspiration or adapted presets from an external GitHub repo or community post:

1. **Verify License Compatibility:** Only adapt materials from permissively licensed projects (MIT, Apache-2.0, CC-BY-4.0, CC0) or rewrite original photography concepts cleanly in your own bilingual wording. Do not copy proprietary or All-Rights-Reserved text verbatim.
2. **Record Provenance in `source`:**
   ```yaml
   source:
     origin: adapted-external
     reference_url: "https://github.com/example-owner/example-repo"
     license_note: "Adapted from MIT-licensed concepts; restructured for WeddingStylePack v1 schema"
   ```
3. **Keep `SKILL.md` Lean:** Never inflate `SKILL.md` with pack-specific prose; keep `SKILL.md` under 500 lines and load newly merged packs on demand from `packs/`.

---

## 4. Step-by-Step Merge Checklist

1. [ ] Clone or inspect the external reference source and extract only reusable photography concepts (venue, styling, pose, lighting, shot matrix).
2. [ ] Map extracted entries into `packs/`, `catalogs/`, and/or `matrices/` with complete Chinese + English descriptions.
3. [ ] Confirm `guardrail_overrides.enforce_high_crown: true` and `guardrail_overrides.enforce_proportion_blending: true`.
4. [ ] Confirm `source.origin`, `source.reference_url`, and `source.license_note` are accurately filled.
5. [ ] Run repository validation and verify zero errors:
   ```bash
   python3 scripts/validate_repo.py
   ```
6. [ ] Smoke-test the merged pack in both **Virtual Couple Mode** and **Real Couple Reference Mode** (checking facial consistency, natural shoulder/neck transition, high-crown hair lift, and cross-frame garment continuity).
7. [ ] Commit cleanly with a descriptive Conventional Commit message (e.g., `feat(packs): add <pack-id> style pack adapted from <source>`).
