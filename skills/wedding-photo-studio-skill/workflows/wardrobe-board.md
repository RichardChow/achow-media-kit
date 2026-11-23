# Optional Workflow: 6-Look Wardrobe Comparison Board (6 宫格换装预演板)

**Trigger (On-Demand Only):** Activate ONLY when the user has a theme/venue direction (or selected pack) and explicitly asks to compare multiple outfits before shooting (e.g., "先看 6 套换装", "先对比 6 套礼服搭配", "纠结穿哪套婚纱", "换装板"). Never force this step in normal shooting sessions.

*(Adapted in concept from `yang0/handraw-style` `huanzhuang` module, tailored for Wedding Photo Studio's proportion & high-crown guardrails.)*

---

## Non-Negotiable Rules

1. **Inherit Locked Context:** Keep the active venue/style pack, participant roster (2-person couple OR multi-person group via `workflows/multi-person-roster.md`), canonical original facial references, and core guardrails (`guardrails/identity-and-proportion.md` + `guardrails/bridal-aesthetics.md`) locked.
2. **Strict Per-Person Detail Floor:** Every single one of the 6 looks MUST write a complete independent outfit description for EVERY participant (`P01` Bride, `P02` Groom, and `P03...` if group shoot).
   - **FORBIDDEN:** Never compress outfits into vague summaries like "其他人类似", "情侣协调穿搭", or "伴娘统一浅色系".
   - Every bridal look MUST include its `neckline_proportion_note` (e.g., off-the-shoulder, French square neck, sweetheart strapless, V-neck, or wide-cloud-collar Xiuhe) to ensure flattering native head-to-shoulder proportions without bulky shoulders.
3. **Genuine Visual Differentiation:** Across Looks 1-6, each look must differ from the others in at least **two** dimensions: silhouette (ballgown / A-line / mermaid / Chinese Xiuhe / mini editorial), fabric (heavy silk satin / 3D floral lace / airy tulle / silk jacquard), neckline, or groom formality/palette.
4. **Wardrobe Preview Does Not Override Final Locks Automatically:** Hair/makeup inside the 6-look preview is for holistic visual cohesion only. Once the user picks their favorite Look number(s), lock the selected garment(s) into `SessionState.styling` and proceed directly to Phase 3-4 with full bridal high-crown, 0-slimming facial lock, and unified skin finish!

---

## Execution Procedure

1. **Present 6 Compact Look Cards (Text Review):**
   Output a clean numbered table (`Look 1` to `Look 6`) showing:
   - Look Name & Style Vibe
   - Bride Outfit + Neckline Proportion Note + Veil/Accessories
   - Groom Outfit (and any `P03+` outfits)
   - Matching Bouquet / Key Prop
2. **Ask User Preference:**
   - Pick directly from text (e.g., `"选 Look 2 开拍"` or `"Look 1 和 Look 4 各拍 4 张"`), OR
   - Request a **6-Panel Visual Wardrobe Preview Board** (`"先出 6 宫格换装预览图"`):
     - Either generate 1 clean 6-panel adaptive comparison grid with `PANEL IDENTITY RESET` per cell (no generated text numbers; clean grid dividers), OR generate 6 individual 3:4 frames and stitch them into a numbered `3x2` board via:
       ```bash
       python scripts/make_contact_sheet.py <wardrobe_dir> <output_3x2.jpg> --layout 3x2 --cell-ratio 3:4
       ```
3. **Selection & Handoff to Phase 3:**
   - When the user picks Look #N, update `SessionState.styling` (and run `scripts/remix_resolver.py dress` if replacing an earlier session's outfits), then compile the formal `ShotPlan` and execute Phase 4.
   - If the user says `"换装再来一版"`, generate 6 fresh non-overlapping combinations continuing numbering (`Look 7` to `Look 12`).
