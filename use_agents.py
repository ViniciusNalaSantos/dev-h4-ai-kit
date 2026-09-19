#!/usr/bin/env python3
"""Install this repository's agent skills into another repository.

The script has no third-party dependencies and can be invoked from any working
directory. By default it copies every skill into ``<target>/.agents/skills``.
"""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any


KIT_ROOT = Path(__file__).resolve().parent
SOURCE_SKILLS = KIT_ROOT / ".agents" / "skills"
SOURCE_LOCK = KIT_ROOT / "skills-lock.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install dev-h4-ai-kit skills into any repository."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=Path.cwd(),
        type=Path,
        help="target repository (default: current directory)",
    )
    parser.add_argument(
        "--mode",
        choices=("copy", "symlink"),
        default="copy",
        help="copy skills or link them back to this kit (default: copy)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace conflicting skills with the versions from this kit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show the changes without writing anything",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list the available skills and exit",
    )
    return parser.parse_args()


def skill_names() -> list[str]:
    if not SOURCE_SKILLS.is_dir():
        raise RuntimeError(f"Skills directory was not found: {SOURCE_SKILLS}")
    return sorted(
        path.name
        for path in SOURCE_SKILLS.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )


def directories_match(left: Path, right: Path) -> bool:
    """Recursively compare two real directories without following links blindly."""
    if not left.is_dir() or not right.is_dir():
        return False
    comparison = filecmp.dircmp(left, right)
    if comparison.left_only or comparison.right_only or comparison.funny_files:
        return False
    if any(not filecmp.cmp(left / name, right / name, shallow=False)
           for name in comparison.common_files):
        return False
    return all(
        directories_match(left / name, right / name)
        for name in comparison.common_dirs
    )


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Cannot read valid JSON from {path}: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"Expected a JSON object in {path}")
    return value


def merge_lock_file(target_root: Path, names: list[str], dry_run: bool) -> None:
    if not SOURCE_LOCK.is_file():
        return

    source_data = read_json(SOURCE_LOCK, {})
    source_entries = source_data.get("skills", {})
    if not isinstance(source_entries, dict):
        raise RuntimeError(f"Invalid skills map in {SOURCE_LOCK}")

    target_lock = target_root / "skills-lock.json"
    target_data = read_json(target_lock, {"version": 1, "skills": {}})
    target_entries = target_data.setdefault("skills", {})
    if not isinstance(target_entries, dict):
        raise RuntimeError(f"Invalid skills map in {target_lock}")

    for name in names:
        if name in source_entries:
            target_entries[name] = source_entries[name]
    target_data["version"] = max(int(target_data.get("version", 1)), 1)

    if not dry_run:
        target_lock.write_text(
            json.dumps(target_data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(f"{'Would update' if dry_run else 'Updated'} {target_lock}")


def install(args: argparse.Namespace) -> int:
    names = skill_names()
    if args.list:
        print("\n".join(names))
        return 0

    target_root = args.target.expanduser().resolve()
    if not target_root.is_dir():
        raise RuntimeError(f"Target directory does not exist: {target_root}")

    destination = target_root / ".agents" / "skills"
    conflicts: list[str] = []
    unchanged: list[str] = []

    for name in names:
        source = SOURCE_SKILLS / name
        target = destination / name
        if target.is_symlink() and target.resolve() == source.resolve():
            unchanged.append(name)
        elif target.exists() and directories_match(source, target):
            unchanged.append(name)
        elif target.exists() or target.is_symlink():
            conflicts.append(name)

    if conflicts and not args.force:
        joined = ", ".join(conflicts)
        raise RuntimeError(
            f"Conflicting skills already exist: {joined}. "
            "Re-run with --force to replace them."
        )

    if not args.dry_run:
        destination.mkdir(parents=True, exist_ok=True)

    changed = 0
    for name in names:
        if name in unchanged:
            print(f"Unchanged {name}")
            continue

        source = SOURCE_SKILLS / name
        target = destination / name
        action = "Link" if args.mode == "symlink" else "Copy"
        print(f"{'Would ' if args.dry_run else ''}{action} {name} -> {target}")
        changed += 1
        if args.dry_run:
            continue
        if target.exists() or target.is_symlink():
            remove_existing(target)
        if args.mode == "symlink":
            target.symlink_to(source, target_is_directory=True)
        else:
            shutil.copytree(source, target)

    merge_lock_file(target_root, names, args.dry_run)
    print(
        f"Done: {changed} skill(s) {'would be installed' if args.dry_run else 'installed'}, "
        f"{len(unchanged)} unchanged."
    )
    return 0


def main() -> int:
    try:
        return install(parse_args())
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        if os.name == "nt" and "symbolic link" in str(error).lower():
            print(
                "hint: use --mode copy, or enable Windows Developer Mode for symlinks",
                file=sys.stderr,
            )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
