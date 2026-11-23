#!/usr/bin/env python3
"""Automated contract regression tests for wedding-photo-studio-skill.

Uses Python standard library unittest (and optionally runs under pytest).
Run via:
  python -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    import yaml  # type: ignore

    HAS_PYYAML = True
except ImportError:
    yaml = None
    HAS_PYYAML = False


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import remix_resolver  # noqa: E402
import workspace_manager  # noqa: E402


class SkillContractTests(unittest.TestCase):
    def test_validate_repo_script_passes(self) -> None:
        proc = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_repo.py")],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stdout + proc.stderr)
        self.assertIn("0 error(s)", proc.stdout)

    def test_skill_md_hard_gates_and_hygiene(self) -> None:
        text = (REPO_ROOT / "SKILL.md").read_text(encoding="utf-8")
        lines = text.splitlines()
        self.assertLess(len(lines), 500)
        self.assertNotIn("\u2014", text, "SKILL.md must not contain em-dash")
        self.assertNotIn("\u2013", text, "SKILL.md must not contain en-dash")
        self.assertIn("Hard Execution Gate", text)
        self.assertIn("STOP HERE", text)
        self.assertIn("成片微调指南", text)
        self.assertIn("workflows/wardrobe-board.md", text)
        self.assertIn("workflows/reference-beauty-prep.md", text)
        self.assertIn("workflows/multi-person-roster.md", text)

    def test_all_19_style_packs_enforce_guardrails(self) -> None:
        packs = sorted(
            p for p in (REPO_ROOT / "packs").glob("*.pack.yaml")
            if p.name != "_template.pack.yaml"
        )
        self.assertGreaterEqual(len(packs), 19)
        if not HAS_PYYAML:
            return
        seen_ids: set[str] = set()
        for pack_path in packs:
            data = yaml.safe_load(pack_path.read_text(encoding="utf-8"))
            self.assertNotIn(data["id"], seen_ids)
            seen_ids.add(data["id"])
            overrides = data.get("guardrail_overrides", {})
            self.assertTrue(overrides.get("enforce_high_crown", True), pack_path.name)
            self.assertTrue(overrides.get("enforce_proportion_blending", True), pack_path.name)
            matrix_rel = data["defaults"]["shot_matrix"]
            self.assertTrue((REPO_ROOT / matrix_rel).is_file(), f"{pack_path.name} -> {matrix_rel}")

    def test_core_guardrail_invariants(self) -> None:
        id_guard = (REPO_ROOT / "guardrails" / "identity-and-proportion.md").read_text(encoding="utf-8")
        self.assertIn("none-zero-slimming", id_guard)
        self.assertIn("replace-with-bridal-poses", id_guard)
        self.assertIn("PANEL IDENTITY RESET", id_guard)
        self.assertIn("粗颈、厚肩、上身显壮", id_guard)

        bridal_guard = (REPO_ROOT / "guardrails" / "bridal-aesthetics.md").read_text(encoding="utf-8")
        self.assertIn("高颅顶造型，头顶发根自然蓬松饱满", bridal_guard)
        self.assertIn("voluminous high-crown hairstyle", bridal_guard)
        self.assertIn("luminous-fair-unified", bridal_guard)

        qa_guard = (REPO_ROOT / "guardrails" / "set-continuity-qa.md").read_text(encoding="utf-8")
        self.assertIn("4 步结构化脸型与比例验收法", qa_guard)
        self.assertIn("<= 2%", qa_guard)

    def test_scene_matched_aesthetic_taglines_cover_all_packs(self) -> None:
        if not HAS_PYYAML:
            self.skipTest("PyYAML not installed")
        cam_data = yaml.safe_load(
            (REPO_ROOT / "catalogs" / "camera-and-lighting.yaml").read_text(encoding="utf-8")
        )
        taglines = cam_data.get("aesthetic_direction_taglines", [])
        self.assertEqual(len(taglines), 4)
        covered_packs: set[str] = set()
        for item in taglines:
            self.assertTrue(item.get("tagline_zh"))
            self.assertTrue(item.get("tagline_en"))
            covered_packs.update(item.get("matched_packs", []))

        all_pack_ids = {
            yaml.safe_load(p.read_text(encoding="utf-8"))["id"]
            for p in (REPO_ROOT / "packs").glob("*.pack.yaml")
            if p.name != "_template.pack.yaml"
        }
        missing = all_pack_ids - covered_packs
        self.assertEqual(missing, set(), f"Packs missing aesthetic tagline mapping: {missing}")

    def test_schemas_support_new_fields(self) -> None:
        session_schema = json.loads(
            (REPO_ROOT / "schemas" / "session-state.schema.json").read_text(encoding="utf-8")
        )
        props = session_schema["properties"]
        self.assertIn("participants", props)
        self.assertIn("workspace_theme_id", props)
        self.assertIn("face_contour_mode", props["styling"]["properties"]["bride"]["properties"])
        self.assertIn("aesthetic_tagline_id", props["camera_and_delivery"]["properties"])

        shot_schema = json.loads(
            (REPO_ROOT / "schemas" / "shot-plan.schema.json").read_text(encoding="utf-8")
        )
        self.assertIn("aesthetic_tagline_zh", shot_schema["properties"])
        shot_item_props = shot_schema["properties"]["shots"]["items"]["properties"]
        self.assertIn("bride_hand_action", shot_item_props)
        self.assertIn("participants_present", shot_item_props)

    def test_remix_resolver_chinese_and_english(self) -> None:
        res_zh = remix_resolver.resolve_remix("场地")
        res_en = remix_resolver.resolve_remix("location")
        self.assertEqual(res_zh["target_dimension"], "location")
        self.assertEqual(res_zh, res_en)
        self.assertIn("canonical_original_references", res_zh["permanent_locks"])
        self.assertIn("makeup", res_zh["frozen_modules"])

    def test_workspace_manager_isolated_themes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "my-wedding-project"
            manifest = workspace_manager.init_workspace(root, couple_label="TestCouple")
            self.assertEqual(manifest["couple_label"], "TestCouple")
            self.assertTrue((root / "canonical_refs").is_dir())
            self.assertTrue((root / "beauty_prep").is_dir())

            t1 = workspace_manager.create_theme(root, "dali-cangshan-sunrise", "大理苍山", 2)
            t2 = workspace_manager.create_theme(root, "crimson-new-chinese", "海派深红新中式", 4)
            self.assertEqual(t1["theme_id"], "THEME-001")
            self.assertEqual(t2["theme_id"], "THEME-002")
            self.assertTrue((root / "themes" / "THEME-001" / "wardrobe_boards").is_dir())
            self.assertTrue((root / "themes" / "THEME-002" / "outputs").is_dir())
            self.assertEqual(len(workspace_manager.list_themes(root)), 2)


if __name__ == "__main__":
    unittest.main()
