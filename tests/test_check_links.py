"""Regression tests for scripts/check_links.py (standard library only)."""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.check_links import (  # noqa: E402
    check_links,
    extract_target,
    iter_markdown_files,
    resolve_local_target,
)


class ExtractTargetTests(unittest.TestCase):
    def test_plain_destination(self):
        self.assertEqual(extract_target("guide.md"), "guide.md")

    def test_destination_with_title(self):
        self.assertEqual(extract_target('guide.md "A title"'), "guide.md")

    def test_angle_bracket_destination_can_contain_spaces(self):
        self.assertEqual(extract_target("<folder/guide page.md> \"title\""), "folder/guide page.md")

    def test_empty_destination(self):
        self.assertEqual(extract_target("  "), "")


class RepositoryLinkCheckTests(unittest.TestCase):
    def test_detects_broken_link_but_accepts_valid_and_external_links(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[valid](docs/guide.md) [missing](docs/missing.md) "
                "[web](https://example.com) [anchor](#top)\n",
                encoding="utf-8",
            )

            files, broken = check_links(root)

            self.assertEqual(len(files), 2)
            self.assertEqual(broken, [("README.md", "docs/missing.md")])

    def test_handles_query_fragment_and_percent_encoded_spaces(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "docs" / "guide page.md").write_text("# Guide\n", encoding="utf-8")
            (root / "README.md").write_text(
                "[guide](docs/guide%20page.md?view=full#intro)\n", encoding="utf-8"
            )
            _, broken = check_links(root)
            self.assertEqual(broken, [])

    def test_ignores_generated_and_dependency_directories(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "docs").mkdir()
            (root / "site").mkdir()
            (root / ".git").mkdir()
            (root / ".venv").mkdir()
            (root / "docs" / "guide.md").write_text("# Guide\n", encoding="utf-8")
            (root / "site" / "generated.md").write_text("[bad](missing.md)\n", encoding="utf-8")
            (root / ".git" / "history.md").write_text("[bad](missing.md)\n", encoding="utf-8")
            (root / ".venv" / "metadata.md").write_text("[bad](missing.md)\n", encoding="utf-8")

            files = iter_markdown_files(root)
            self.assertEqual([path.relative_to(root).as_posix() for path in files], ["docs/guide.md"])


    def test_rejects_links_that_escape_repository_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            base = Path(temporary_directory)
            root = base / "repo"
            root.mkdir()
            outside = base / "outside.md"
            outside.write_text("# Outside\n", encoding="utf-8")
            (root / "README.md").write_text("[outside](../outside.md)\n", encoding="utf-8")

            _, broken = check_links(root)
            self.assertEqual(broken, [("README.md", "../outside.md")])

    def test_repository_root_relative_links(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            docs = root / "docs"
            docs.mkdir()
            target = root / "README.md"
            target.write_text("# Home\n", encoding="utf-8")
            source = docs / "guide.md"
            source.write_text("# Guide\n", encoding="utf-8")

            self.assertEqual(resolve_local_target(source, "/README.md", root), target.resolve())


if __name__ == "__main__":
    unittest.main()
