#!/usr/bin/env python3
"""Check local Markdown links without requiring third-party packages.

The checker validates that relative and repository-root-relative Markdown
links (including image links) point to an existing file or directory. It
skips URLs with a scheme/netloc and fragment-only links. Fragment target IDs
and external URL reachability are intentionally not checked.

Run from any directory with:
    python scripts/check_links.py

Compatible with Python 3.8+ and Windows, macOS, and Linux.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple
from urllib.parse import unquote, urlsplit

REPO_ROOT = Path(__file__).resolve().parent.parent
# Includes Markdown images. This intentionally targets ordinary inline links;
# reference-style Markdown links are outside this lightweight checker's scope.
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
IGNORED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "site",
}


def extract_target(raw_target: str) -> str:
    """Extract a Markdown destination, including destinations with titles.

    Angle-bracket destinations may contain spaces. For ordinary destinations,
    the first whitespace-delimited token is the URL/path; an optional Markdown
    title follows it.
    """
    target = raw_target.strip()
    if target.startswith("<"):
        closing_angle = target.find(">")
        if closing_angle >= 0:
            return target[1:closing_angle].strip()
    return target.split(None, 1)[0] if target else ""


def iter_markdown_files(repo_root: Path) -> List[Path]:
    """Return Markdown files while excluding generated and dependency trees."""
    files = []
    for path in repo_root.rglob("*.md"):
        try:
            relative_parts = path.relative_to(repo_root).parts
        except ValueError:
            continue
        if any(part in IGNORED_DIRECTORY_NAMES for part in relative_parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def resolve_local_target(source_file: Path, target: str, repo_root: Path):
    """Resolve a local Markdown destination, or return None for non-local links."""
    parts = urlsplit(target)
    # Skip web URLs, mailto:, protocol-relative URLs, and other URI schemes.
    if parts.scheme or parts.netloc:
        return None
    if not parts.path:  # Empty target or fragment-only target, e.g. #section
        return None

    decoded_path = unquote(parts.path)
    if decoded_path.startswith("/"):
        # A leading slash is treated as repository-root-relative.
        return (repo_root / decoded_path.lstrip("/")).resolve()
    return (source_file.parent / decoded_path).resolve()


def check_links(repo_root: Path = REPO_ROOT) -> Tuple[List[Path], List[Tuple[str, str]]]:
    """Return (Markdown files checked, broken local links)."""
    root = repo_root.resolve()
    markdown_files = iter_markdown_files(root)
    broken = []

    for markdown_file in markdown_files:
        try:
            content = markdown_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            broken.append((str(markdown_file.relative_to(root)), "<cannot read file: {}>".format(exc)))
            continue

        for match in LINK_PATTERN.finditer(content):
            target = extract_target(match.group(1))
            resolved = resolve_local_target(markdown_file, target, root)
            if resolved is None:
                continue
            try:
                resolved.relative_to(root)
            except ValueError:
                broken.append((str(markdown_file.relative_to(root)), target))
                continue
            if not resolved.exists():
                broken.append((str(markdown_file.relative_to(root)), target))

    return markdown_files, broken


def main() -> int:
    markdown_files, broken = check_links()
    if broken:
        print("Found {} broken internal link(s):\n".format(len(broken)))
        for file_path, target in broken:
            print("  {} -> {}".format(file_path, target))
        print("Checked {} Markdown files; validation FAILED.".format(len(markdown_files)))
        return 1

    print("Checked {} Markdown files. 0 broken internal links. PASS.".format(len(markdown_files)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
