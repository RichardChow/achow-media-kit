# Optional Workflow: Pre-Shoot 3-Panel Reference Beauty Prep (参考图前置三宫格精修)

**Trigger (Strict Opt-In Only):** Activate ONLY when the user explicitly requests pre-shoot portrait retouching of their raw reference photo(s) before wedding photography begins (e.g., "先美化参考图", "先精修底图", "做三宫格美化", "美图秀秀风格精修").

**CRITICAL NON-INTERRUPTION RULE:** Uploading a casual real couple photo does **NOT** trigger this workflow, and the Agent must **NEVER** proactively ask "是否需要先美化参考图" during Phase 1 or Phase 2. Normal wedding sessions already apply unified luminous-fair skin finishing (`luminous-fair-unified`) automatically.

*(Adapted in concept from `yang0/handraw-style` `meihua` module, hardened with Wedding Photo Studio's 0-slimming facial lock and unified face-neck-shoulder complexion rules.)*

---

## Visual 3-Panel Exploration Design (Left / Center / Right)

Do not show a long text menu of retouch sliders. Directly generate (or output copy-ready prompt for) a crisp **3-panel horizontal comparison board (Left | Center | Right)** of the uploaded subject(s) preserving **100% exact facial geometry (0% face slimming, exact inter-eye distance, cheek width/fullness, jawline, glasses, and natural asymmetry)**:

| Panel | Preset Direction | Visual Execution (All Preserve 0% Geometric Slimming) |
| --- | --- | --- |
| **左 (Left)** | **自然清透微整理** (`natural-authentic`) | Faithful native skin tone, subtle evening of temporary blemishes/dark circles, clean lighting balance, naturally neat hair with gentle crown lift. |
| **中 (Center)** | **整体清透白皙影楼精修** (`luminous-fair-unified` / `studio-soft-glow`) | Mandatory luminous-fair option: clearly softens blemishes/redness/dark circles, bright healthy fair radiance with delicate soft-focus glow applied **uniformly across face, jawline, neck, and shoulders**, real fine skin micro-texture intact, sleek lifted high-crown hair. |
| **右 (Right)** | **高定形象强化预览** (`editorial-polish`) | Crisp eye catchlights, refined bridal-ready makeup tones, sculpted sleek high-crown bridal hair silhouette, elevated portrait polish—while keeping bone structure and recognizability 100% intact. |

---

## Mandatory Post-Preview Guidance

Immediately below the 3-panel preview, prompt the user cleanly:

> `请选择 左 / 中 / 右 放大成高清精修参考图；也可以直接告诉我具体要求（例如「再白皙透亮一点」「保留原生肤色只去黑眼圈」「做一版美图秀秀风格精修」）。`

*(Note: "美图秀秀风格精修" means cleaner brightening, blemish removal, delicate soft-focus glow, and crisp bridal radiance across face-neck-shoulders uniformly, STILL obeying 0% face slimming, authentic hair strands, and zero plastic wax skin.)*

---

## Canonical Identity Boundary (MUST OBEY)

1. The enlarged beauty-prep output is strictly classified as a **derived aesthetic reference** (`derived_beauty_image`).
2. **Selecting Left / Center / Right or enlarging it does NOT automatically overwrite `canonical_original_references`.** Subsequent formal wedding shoots still lock facial bone structure to the user's initially uploaded raw photo(s) while optionally referencing the beauty-prep image for lighting/makeup finish.
3. **Explicit User Promotion Only:** Switch `active_identity_references` to the beauty-prep image ONLY if the user explicitly says `"以后用这张精修图作为人脸参考"` (while still preserving `canonical_original_references` for instant rollback upon `"恢复最初原图"`).
