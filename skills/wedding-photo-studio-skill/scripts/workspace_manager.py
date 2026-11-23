#!/usr/bin/env python3
"""Optional local multi-theme persistent workspace manager for wedding-photo-studio-skill.

Chat-first by default: never required for normal chat sessions. Activate only
when the user wants to organize multiple wedding themes (THEME-001, THEME-002...)
under one local project directory while sharing canonical original references
and isolating outfits, shot plans, wardrobe boards, and rendered outputs per theme.

Pure Python standard library only. Adapted in concept from yang0/handraw-style
(MIT License with Attribution Requirement).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANIFEST_NAME = "studio-manifest.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_manifest(project_dir: Path) -> dict[str, Any]:
    manifest_path = project_dir / MANIFEST_NAME
    if not manifest_path.is_file():
        raise SystemExit(
            f"Workspace not initialized at {project_dir}. Run `init` first."
        )
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def _write_manifest(project_dir: Path, data: dict[str, Any]) -> Path:
    manifest_path = project_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def init_workspace(project_dir: Path, couple_label: str = "Couple") -> dict[str, Any]:
    project_dir = project_dir.resolve()
    (project_dir / "canonical_refs").mkdir(parents=True, exist_ok=True)
    (project_dir / "beauty_prep").mkdir(parents=True, exist_ok=True)
    (project_dir / "themes").mkdir(parents=True, exist_ok=True)

    manifest_path = project_dir / MANIFEST_NAME
    if manifest_path.is_file():
        return _read_manifest(project_dir)

    manifest: dict[str, Any] = {
        "schema_version": "1.0.0",
        "couple_label": couple_label,
        "created_at": _utc_now(),
        "canonical_original_references": [],
        "active_identity_references": [],
        "used_spacetime_anchors": [],
        "themes": [],
    }
    _write_manifest(project_dir, manifest)
    return manifest


def create_theme(
    project_dir: Path,
    pack_id: str,
    title: str,
    participants: int = 2,
) -> dict[str, Any]:
    project_dir = project_dir.resolve()
    manifest = _read_manifest(project_dir)

    next_index = len(manifest.get("themes", [])) + 1
    theme_id = f"THEME-{next_index:03d}"
    theme_dir = project_dir / "themes" / theme_id
    for sub in ("prompts", "wardrobe_boards", "outputs", "refinements"):
        (theme_dir / sub).mkdir(parents=True, exist_ok=True)

    theme_meta: dict[str, Any] = {
        "theme_id": theme_id,
        "title": title,
        "pack_id": pack_id,
        "participant_count": participants,
        "status": "initialized",
        "created_at": _utc_now(),
        "isolated_dir": f"themes/{theme_id}",
    }

    (theme_dir / "theme-state.json").write_text(
        json.dumps(theme_meta, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest.setdefault("themes", []).append(theme_meta)
    _write_manifest(project_dir, manifest)
    return theme_meta


def list_themes(project_dir: Path) -> list[dict[str, Any]]:
    manifest = _read_manifest(project_dir.resolve())
    return list(manifest.get("themes", []))


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    parser = argparse.ArgumentParser(
        description="Manage optional persistent multi-theme wedding studio workspaces."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize a local multi-theme studio workspace.")
    p_init.add_argument("project_dir", type=Path)
    p_init.add_argument("--couple-label", default="Couple")

    p_new = sub.add_parser("new-theme", help="Create an isolated THEME-xxx directory.")
    p_new.add_argument("project_dir", type=Path)
    p_new.add_argument("--pack", required=True, help="Pack ID (e.g. crimson-new-chinese) or 'custom'.")
    p_new.add_argument("--title", required=True, help="Human-readable theme title.")
    p_new.add_argument("--participants", type=int, default=2, help="Participant count (default: 2).")

    p_list = sub.add_parser("list", help="List all themes in a workspace.")
    p_list.add_argument("project_dir", type=Path)

    args = parser.parse_args()

    if args.cmd == "init":
        data = init_workspace(args.project_dir, args.couple_label)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "new-theme":
        theme = create_theme(args.project_dir, args.pack, args.title, args.participants)
        print(json.dumps(theme, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "list":
        themes = list_themes(args.project_dir)
        print(json.dumps(themes, ensure_ascii=False, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
