#!/usr/bin/env python3
"""Single-variable Remix dependency resolver for wedding-photo-studio-skill.

When a user asks to change only ONE dimension (e.g. '只换场地' or '只换礼服'),
this script determines which SessionState / ShotPlan modules must be recomputed
and which remain strictly frozen—while ALWAYS preserving canonical identity
references and core aesthetic/proportion guardrails.

Adapted in concept from yang0/handraw-style (MIT License with Attribution).
"""

from __future__ import annotations

import argparse
import json
import sys

ALL_MODULES = (
    "location",
    "micro_zones",
    "dress",
    "hairstyle",
    "groom_hair",
    "makeup",
    "skin_finish",
    "props",
    "mood",
    "lighting",
    "shot_plan",
    "render",
)

DEPENDENCY_GRAPH: dict[str, dict[str, list[str]]] = {
    "location": {
        "always_invalidate": ["location", "micro_zones", "lighting", "shot_plan", "render"],
        "conditional_invalidate": ["props", "dress", "hairstyle"],
    },
    "dress": {
        "always_invalidate": ["dress", "shot_plan", "render"],
        "conditional_invalidate": ["hairstyle", "makeup", "props"],
    },
    "hairstyle": {
        "always_invalidate": ["hairstyle", "shot_plan", "render"],
        "conditional_invalidate": ["makeup"],
    },
    "groom_hair": {
        "always_invalidate": ["groom_hair", "shot_plan", "render"],
        "conditional_invalidate": [],
    },
    "makeup": {
        "always_invalidate": ["makeup", "shot_plan", "render"],
        "conditional_invalidate": ["skin_finish"],
    },
    "skin_finish": {
        "always_invalidate": ["skin_finish", "shot_plan", "render"],
        "conditional_invalidate": ["makeup"],
    },
    "mood": {
        "always_invalidate": ["mood", "shot_plan", "render"],
        "conditional_invalidate": ["lighting"],
    },
    "lighting": {
        "always_invalidate": ["lighting", "shot_plan", "render"],
        "conditional_invalidate": ["makeup"],
    },
    "color_palette": {
        "always_invalidate": ["lighting", "props", "shot_plan", "render"],
        "conditional_invalidate": ["dress", "makeup"],
    },
    "shot_matrix": {
        "always_invalidate": ["micro_zones", "shot_plan", "render"],
        "conditional_invalidate": [],
    },
}

ALIASES: dict[str, str] = {
    "场地": "location",
    "地点": "location",
    "场景": "location",
    "礼服": "dress",
    "婚纱": "dress",
    "服装": "dress",
    "发型": "hairstyle",
    "新娘发型": "hairstyle",
    "新郎发型": "groom_hair",
    "妆容": "makeup",
    "肤质": "skin_finish",
    "白皙度": "skin_finish",
    "情绪": "mood",
    "互动": "mood",
    "动作": "mood",
    "光影": "lighting",
    "光线": "lighting",
    "色调": "color_palette",
    "色彩": "color_palette",
    "分镜": "shot_matrix",
    "角度": "shot_matrix",
}

PERMANENT_LOCKS = [
    "canonical_original_references",
    "guardrails/identity-and-proportion.md",
    "guardrails/bridal-aesthetics.md",
    "guardrails/set-continuity-qa.md",
]


def resolve_remix(target: str) -> dict[str, object]:
    normalized = ALIASES.get(target.strip(), target.strip().lower())
    if normalized not in DEPENDENCY_GRAPH:
        supported = ", ".join(sorted(DEPENDENCY_GRAPH.keys()))
        raise KeyError(f"Unknown remix target {target!r}. Supported: {supported}")

    entry = DEPENDENCY_GRAPH[normalized]
    always_inv = entry["always_invalidate"]
    cond_inv = entry["conditional_invalidate"]
    frozen = [m for m in ALL_MODULES if m not in always_inv and m not in cond_inv]

    return {
        "target_dimension": normalized,
        "always_invalidate": always_inv,
        "conditional_invalidate": cond_inv,
        "frozen_modules": frozen,
        "permanent_locks": PERMANENT_LOCKS,
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    parser = argparse.ArgumentParser(
        description="Resolve frozen vs. invalidated modules for a single-variable wedding remix."
    )
    parser.add_argument(
        "target",
        help="Dimension to remix (e.g. location/场地, dress/礼服, hairstyle/发型, groom_hair/新郎发型, skin_finish/肤质, lighting/光影, shot_matrix/分镜).",
    )
    args = parser.parse_args()

    try:
        plan = resolve_remix(args.target)
    except KeyError as exc:
        print(f"[FAIL] {exc}", file=sys.stderr)
        return 1

    print(json.dumps(plan, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
