# Optional Workflow: Multi-Person Wedding Party, Family & Solo Roster (单人 / 伴郎伴娘 / 全家福多人模式)

**Trigger:** Automatically activates whenever the user requests a shoot with **1 person** (solo bridal/groom portrait) OR **3+ people** (couple + parents/family, bride & groom + bridesmaids/groomsmen 伴郎伴娘团, multi-generation family wedding portrait, or friends wedding party).
*(Standard 2-person couples default silently to `P01` Bride + `P02` Groom with zero extra questions.)*

*(Adapted in concept from `yang0/handraw-style` `kefu` / `paishe` multi-participant Detail Floor model.)*

---

## 1. Participant Structure Gate (For 3+ People Only)

Before outputting the Phase 2 3-column confirmation table for any group/family/wedding-party shoot (3+ participants), verify three essentials:
1. **Total participant count (`participant_count`)**
2. **Per-person gender & role label** (infer automatically from unambiguous titles like 爸爸/妈妈/伴娘/伴郎; ask ONLY for truly missing members in ONE compact turn—never turn into a long questionnaire)
3. **Relationship hierarchy (`relationship_description`)** (e.g., "新人 C 位为主角，两侧为父母长辈，后排错落为 2 位伴娘与 2 位伴郎")

Assign every person a permanent continuity ID for the entire session:
- `P01`: Bride (新娘)
- `P02`: Groom (新郎)
- `P03`, `P04`, ...: Named roles (e.g., `P03 新娘母亲`, `P04 伴娘A`, `P05 伴郎A`)

---

## 2. Non-Negotiable Multi-Person Detail Floor

Increasing headcount must **NEVER** degrade per-person specificity:

1. **Per-Person Identity Binding:** Map each uploaded reference photo explicitly to its `participant_id` (`P01 -> ref_1`, `P02 -> ref_2`, `P03 -> ref_3`, ...). Zero identity swapping, zero accidental duplicate faces, zero adding/dropping declared participants.
2. **Per-Person Complete Wardrobe & Hair:** Every participant gets an independent outfit, neckline/proportion note, and hairstyle specification.
   - **FORBIDDEN:** Never write "伴娘统一浅粉色礼服", "其他人穿类似西装", or "其余家人自然搭配". Shared color harmonies are great, but each individual's silhouette/cut/detail must still be written out explicitly.
   - All core guardrails apply to every visible person: **0% geometric face slimming** (`none-zero-slimming` default), native build anti-bulky rollback, unified face-neck-shoulder complexion, and mandatory sleek high-crown hair for the bride (`P01`).
3. **Per-Shot Explicit Roster & Choreography (`participants_present` + `participant_directions`):**
   - Every shot in `ShotPlan.shots[]` explicitly lists which IDs appear (`participants_present`) and gives ONE concrete direction per visible person (`participant_directions`: stance, hand placement, height level, gaze, interaction).
   - **FORBIDDEN:** Never write "其余人站在后面微笑互动".

---

## 3. Multi-Person Composition & 8-Shot Set Coverage Rules

- **Full-Roster Coverage:** Across an 8-shot set, the union of `participants_present` MUST include 100% of confirmed participants.
- **Complete Group Portrait:** Include at least **1–2 full-roster ceremonial portraits** with staggered depth, seated/standing height layering, and interconnected gaze/contact (never a stiff flat lineup!).
- **Subgroup & Couple Balance:** Mix full-group frames (Shots 1 & 7), couple-core hero frames (Shots 2, 4, 5), solo bride couture hero (Shot 6), candid bridal-party / parents warm interaction frames (Shot 3), and closing detail of rings/hands/bouquet (Shot 8).
- **Face Readability Gate for Groups:** For 4+ people in one frame, favor horizontal `16:9` / `3:2` or wider `3:4` architectural tiered arrangements (stairs, benches, foreground-midground-background triangles) so every face remains clear, well-lit, and fully recognizable.
