#!/usr/bin/env python3
"""Repository validator for wedding-photo-studio-skill.

Uses Python standard library only. When PyYAML is available, performs full YAML
parsing and strict Style Pack / Shot Matrix schema verification; otherwise
gracefully falls back to lightweight structural YAML checks with a clear notice.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore

    HAS_PYYAML = True
except ImportError:
    yaml = None
    HAS_PYYAML = False


REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PACK_TOP_KEYS = (
    "id",
    "name",
    "version",
    "source",
    "defaults",
    "prompt_modifiers",
)

REQUIRED_DEFAULTS_KEYS = (
    "location",
    "bride",
    "groom",
    "props",
    "mood",
    "camera",
    "shot_matrix",
)

REQUIRED_NESTED_DEFAULTS = {
    "location": ("venue", "atmosphere", "foreground"),
    "bride": ("dress", "hairstyle", "makeup", "veil_or_accessories"),
    "groom": ("outfit", "hairstyle_virtual", "hairstyle_reference_mode"),
    "mood": ("tone", "signature_poses"),
    "camera": (
        "body_and_lens",
        "lighting",
        "color_temperature",
        "film_texture",
        "aspect_ratio",
    ),
}

REQUIRED_PROMPT_MODIFIERS = (
    "zh_style_keywords",
    "en_style_keywords",
    "negative_hints",
)

PACK_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
KNOWN_ROOT_DIRS = (
    "schemas",
    "guardrails",
    "catalogs",
    "matrices",
    "packs",
    "adapters",
    "scripts",
    "docs",
)


class ValidationResult:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []

    def ok(self, message: str) -> None:
        self.passed.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def fail(self, message: str) -> None:
        self.errors.append(message)


def _fallback_parse_top_level_yaml(text: str, rel_path: str, result: ValidationResult) -> dict[str, Any]:
    """Lightweight fallback parser when PyYAML is not installed."""
    data: dict[str, Any] = {}
    section_stack: str | None = None
    nested: dict[str, dict[str, Any]] = {}

    for lineno, raw_line in enumerate(text.splitlines(), start=1):
        if "\t" in raw_line:
            result.fail(f"{rel_path}:{lineno}: tabs are not allowed in YAML indentation")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if indent == 0:
            section_stack = None
            match = re.match(r"^([A-Za-z0-9_-]+)\s*:(.*)$", stripped)
            if not match:
                result.fail(f"{rel_path}:{lineno}: invalid top-level YAML syntax: {stripped}")
                continue
            key, val = match.group(1), match.group(2).strip().strip("\"'")
            data[key] = val if val else {}
            if not val:
                section_stack = key
                nested[key] = {}
        elif section_stack and indent == 2:
            match = re.match(r"^([A-Za-z0-9_-]+)\s*:(.*)$", stripped)
            if match:
                key, val = match.group(1), match.group(2).strip().strip("\"'")
                nested[section_stack][key] = val if val else {}

    for sec, sec_data in nested.items():
        if sec_data:
            data[sec] = sec_data
    return data


def load_yaml_file(path: Path, result: ValidationResult) -> dict[str, Any] | None:
    rel_path = path.relative_to(REPO_ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        result.fail(f"{rel_path}: YAML file is empty")
        return None

    if HAS_PYYAML:
        try:
            parsed = yaml.safe_load(text)
        except Exception as exc:  # noqa: BLE001
            result.fail(f"{rel_path}: YAML syntax error: {exc}")
            return None
        if not isinstance(parsed, dict):
            result.fail(f"{rel_path}: top-level YAML structure must be a mapping")
            return None
        return parsed

    return _fallback_parse_top_level_yaml(text, rel_path, result)


def validate_schemas(result: ValidationResult) -> None:
    schema_files = sorted((REPO_ROOT / "schemas").glob("*.json"))
    if not schema_files:
        result.fail("schemas/: no JSON schema files found")
        return

    for path in schema_files:
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        try:
            content = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            result.fail(f"{rel_path}: invalid JSON ({exc})")
            continue

        if not isinstance(content, dict):
            result.fail(f"{rel_path}: JSON schema root must be an object")
            continue

        schema_uri = content.get("$schema", "")
        if not isinstance(schema_uri, str) or not schema_uri.startswith("https://"):
            result.fail(f"{rel_path}: '$schema' must be a valid https:// URI")
            continue

        result.ok(f"JSON schema valid: {rel_path}")


def validate_yaml_directories(result: ValidationResult) -> None:
    yaml_dirs = ("catalogs", "matrices", "packs")
    for dirname in yaml_dirs:
        files = sorted((REPO_ROOT / dirname).glob("*.yaml"))
        if not files:
            result.fail(f"{dirname}/: no YAML files found")
            continue
        for path in files:
            rel_path = path.relative_to(REPO_ROOT).as_posix()
            parsed = load_yaml_file(path, result)
            if parsed is not None:
                result.ok(f"YAML syntax valid: {rel_path}")


def validate_matrices(result: ValidationResult) -> None:
    matrix_files = sorted((REPO_ROOT / "matrices").glob("*.yaml"))
    if not matrix_files:
        result.fail("matrices/: no matrix YAML files found")
        return

    for path in matrix_files:
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        data = load_yaml_file(path, result)
        if data is None or not HAS_PYYAML:
            continue

        matrix_id = data.get("id")
        shot_count = data.get("shot_count")
        shots = data.get("shots")
        if not isinstance(matrix_id, str) or not PACK_ID_PATTERN.match(matrix_id):
            result.fail(f"{rel_path}: 'id' must match ^[a-z0-9-]+$")
            continue
        if not isinstance(shot_count, int) or not isinstance(shots, list) or len(shots) != shot_count:
            result.fail(
                f"{rel_path}: 'shots' length ({len(shots) if isinstance(shots, list) else 'invalid'}) "
                f"must equal 'shot_count' ({shot_count!r})"
            )
            continue

        result.ok(f"Shot matrix structure valid: {rel_path} ({shot_count} shots)")


def validate_style_packs(result: ValidationResult) -> None:
    pack_files = sorted((REPO_ROOT / "packs").glob("*.pack.yaml"))
    active_packs = [p for p in pack_files if p.name != "_template.pack.yaml"]

    if not active_packs:
        result.fail("packs/: no active *.pack.yaml files found")
        return

    seen_ids: set[str] = set()
    for path in active_packs:
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        data = load_yaml_file(path, result)
        if data is None:
            continue

        missing_top = [k for k in REQUIRED_PACK_TOP_KEYS if k not in data]
        if missing_top:
            result.fail(f"{rel_path}: missing required top-level keys: {', '.join(missing_top)}")
            continue

        pack_id = data.get("id")
        if not isinstance(pack_id, str) or not PACK_ID_PATTERN.match(pack_id):
            result.fail(f"{rel_path}: 'id' must match ^[a-z0-9-]+$, got {pack_id!r}")
        elif pack_id in seen_ids:
            result.fail(f"{rel_path}: duplicate pack id {pack_id!r}")
        else:
            seen_ids.add(pack_id)

        if HAS_PYYAML:
            name = data.get("name")
            if not isinstance(name, dict) or not name.get("zh") or not name.get("en"):
                result.fail(f"{rel_path}: 'name' must contain non-empty 'zh' and 'en' strings")

            source = data.get("source")
            if not isinstance(source, dict) or source.get("origin") not in (
                "native",
                "adapted-external",
            ):
                result.fail(
                    f"{rel_path}: 'source.origin' must be 'native' or 'adapted-external'"
                )
            elif source.get("origin") == "adapted-external":
                if not str(source.get("reference_url", "")).strip():
                    result.fail(
                        f"{rel_path}: adapted-external pack must specify non-empty 'source.reference_url'"
                    )
                if not str(source.get("license_note", "")).strip():
                    result.fail(
                        f"{rel_path}: adapted-external pack must specify non-empty 'source.license_note'"
                    )

            defaults = data.get("defaults")
            if not isinstance(defaults, dict):
                result.fail(f"{rel_path}: 'defaults' must be a mapping")
                continue

            missing_defaults = [k for k in REQUIRED_DEFAULTS_KEYS if k not in defaults]
            if missing_defaults:
                result.fail(
                    f"{rel_path}: 'defaults' missing required keys: {', '.join(missing_defaults)}"
                )

            for section, req_keys in REQUIRED_NESTED_DEFAULTS.items():
                section_val = defaults.get(section)
                if not isinstance(section_val, dict):
                    result.fail(f"{rel_path}: 'defaults.{section}' must be a mapping")
                    continue
                missing_sub = [k for k in req_keys if not section_val.get(k)]
                if missing_sub:
                    result.fail(
                        f"{rel_path}: 'defaults.{section}' missing keys: {', '.join(missing_sub)}"
                    )

            props = defaults.get("props")
            if not isinstance(props, list) or not props:
                result.fail(f"{rel_path}: 'defaults.props' must be a non-empty list")

            prompt_mods = data.get("prompt_modifiers")
            if not isinstance(prompt_mods, dict):
                result.fail(f"{rel_path}: 'prompt_modifiers' must be a mapping")
            else:
                missing_mods = [k for k in REQUIRED_PROMPT_MODIFIERS if not prompt_mods.get(k)]
                if missing_mods:
                    result.fail(
                        f"{rel_path}: 'prompt_modifiers' missing keys: {', '.join(missing_mods)}"
                    )

            overrides = data.get("guardrail_overrides", {})
            if isinstance(overrides, dict):
                if overrides.get("enforce_high_crown") is False:
                    result.fail(
                        f"{rel_path}: shared packs must not disable 'enforce_high_crown'"
                    )
                if overrides.get("enforce_proportion_blending") is False:
                    result.fail(
                        f"{rel_path}: shared packs must not disable 'enforce_proportion_blending'"
                    )

        shot_matrix = None
        defaults_obj = data.get("defaults")
        if isinstance(defaults_obj, dict):
            shot_matrix = defaults_obj.get("shot_matrix")

        if not isinstance(shot_matrix, str) or not shot_matrix.strip():
            result.fail(f"{rel_path}: 'defaults.shot_matrix' must be a non-empty relative path")
        else:
            matrix_path = REPO_ROOT / shot_matrix
            if not matrix_path.is_file():
                result.fail(
                    f"{rel_path}: 'defaults.shot_matrix' target does not exist: {shot_matrix}"
                )
            else:
                result.ok(f"Style pack schema & shot_matrix valid: {rel_path} -> {shot_matrix}")


def validate_adapters_and_scripts(result: ValidationResult) -> None:
    adapter_files = sorted((REPO_ROOT / "adapters").glob("*.md"))
    if not adapter_files:
        result.fail("adapters/: no adapter markdown files found")
    else:
        for path in adapter_files:
            rel_path = path.relative_to(REPO_ROOT).as_posix()
            if not path.read_text(encoding="utf-8").strip():
                result.fail(f"{rel_path}: adapter file is empty")
            else:
                result.ok(f"Adapter present: {rel_path}")

    script_files = sorted((REPO_ROOT / "scripts").glob("*.py"))
    if not script_files:
        result.fail("scripts/: no Python scripts found")
    else:
        for path in script_files:
            rel_path = path.relative_to(REPO_ROOT).as_posix()
            try:
                source = path.read_text(encoding="utf-8")
                compile(source, rel_path, "exec")
            except SyntaxError as exc:
                result.fail(f"{rel_path}: Python syntax error ({exc})")
            else:
                result.ok(f"Python script compiles: {rel_path}")


def validate_skill_md(result: ValidationResult) -> None:
    skill_path = REPO_ROOT / "SKILL.md"
    if not skill_path.is_file():
        result.fail("SKILL.md: file does not exist")
        return

    text = skill_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if len(lines) >= 500:
        result.fail(f"SKILL.md: line count is {len(lines)}, must be < 500")
    else:
        result.ok(f"SKILL.md line count valid: {len(lines)} lines (< 500)")

    em_dash = "\u2014"
    en_dash = "\u2013"
    dash_issues: list[str] = []
    for idx, line in enumerate(lines, start=1):
        if em_dash in line:
            dash_issues.append(f"line {idx} contains em-dash (U+2014)")
        if en_dash in line:
            dash_issues.append(f"line {idx} contains en-dash (U+2013)")

    if dash_issues:
        for issue in dash_issues:
            result.fail(f"SKILL.md: {issue}")
    else:
        result.ok("SKILL.md typography valid: zero em-dash / en-dash characters")

    # Collect all local relative paths referenced inside backticks in SKILL.md.
    referenced_paths: set[str] = set()
    code_span_pattern = re.compile(r"`([^`]+)`")

    for line in lines:
        spans = code_span_pattern.findall(line)
        line_dir_context: str | None = None

        for span in spans:
            token = span.strip()
            if not token:
                continue

            if token.endswith("/") and token.rstrip("/") in KNOWN_ROOT_DIRS:
                line_dir_context = token.rstrip("/")
                referenced_paths.add(token)
                continue

            if "/" in token and not token.startswith(("http://", "https://")):
                first_segment = token.split("/", 1)[0]
                if first_segment in KNOWN_ROOT_DIRS:
                    referenced_paths.add(token)
                continue

            if line_dir_context and token.endswith((".md", ".yaml", ".yml", ".json", ".py")):
                referenced_paths.add(f"{line_dir_context}/{token}")

    if not referenced_paths:
        result.warn("SKILL.md: no local relative paths detected")
        return

    missing_refs: list[str] = []
    for ref in sorted(referenced_paths):
        target = REPO_ROOT / ref.rstrip("/")
        if ref.endswith("/"):
            if not target.is_dir():
                missing_refs.append(ref)
        else:
            if not target.is_file():
                missing_refs.append(ref)

    if missing_refs:
        for missing in missing_refs:
            result.fail(f"SKILL.md: referenced local path does not exist: {missing}")
    else:
        result.ok(
            f"SKILL.md local path references valid: all {len(referenced_paths)} referenced paths exist"
        )


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass

    result = ValidationResult()

    if HAS_PYYAML:
        result.ok(f"YAML engine: PyYAML {getattr(yaml, '__version__', 'installed')} (full parsing enabled)")
    else:
        result.warn(
            "PyYAML is not installed; running in standard-library fallback mode. "
            "Install PyYAML (`pip install pyyaml`) for full YAML AST validation."
        )

    validate_schemas(result)
    validate_yaml_directories(result)
    validate_matrices(result)
    validate_style_packs(result)
    validate_adapters_and_scripts(result)
    validate_skill_md(result)

    print("=== wedding-photo-studio-skill Repository Validation ===")
    for msg in result.passed:
        print(f"[OK]   {msg}")
    for msg in result.warnings:
        print(f"[WARN] {msg}")
    for msg in result.errors:
        print(f"[FAIL] {msg}")

    print(
        f"\nSummary: {len(result.passed)} passed, "
        f"{len(result.warnings)} warning(s), {len(result.errors)} error(s)."
    )
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
