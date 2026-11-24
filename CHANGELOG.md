# Changelog

All notable changes to this project are documented here. The repository does not yet follow a formal release/versioning scheme; no tagged releases exist.

## [Unreleased] — Verification and maintainability fixes — 2026-11-24

### Updated
- Reconciled the README, changelog, tests guide, and verification report so their test claims match the checks actually run for this package.
- Replaced the README's placeholder clone command with the repository URL configured in `mkdocs.yml`.
- Made the internal Markdown link checker portable across Windows, macOS, and Linux; it now handles link titles, angle-bracket destinations, URL-encoded spaces, query strings, and repository-root-relative links, and excludes generated/dependency directories by path components.
- Added 9 standard-library regression tests for the link checker and wired them into GitHub Actions.
- Expanded `.gitignore` for generated site output, Python caches, build artefacts, virtual environments, local environment files, logs, and OS noise.
- Corrected firmware guidance that ambiguously described pin 1 as potentially VCC or CS. Chip pin functions must be taken from the exact datasheet and board design.
- Added a consistent repository-validation note to each of the six learning-level guides, while keeping hardware-specific verification boundaries explicit.

### Verification snapshot

The local checks passed: 9/9 link-checker regression tests, 21 Markdown files scanned with 0 broken internal links, Python compilation for `scripts/`, `examples/`, and `tests/`, YAML parsing for `mkdocs.yml` and `.github/workflows/docs-ci.yml`, and `mkdocs build --strict` (completed in 3.19 seconds).

Material for MkDocs emitted an upstream warning about future MkDocs 2.0 compatibility. It was informational: the strict build completed successfully. The GitHub Actions workflow has not yet run on GitHub-hosted infrastructure and must be checked after the initial push.

### Known scope limitations

- Only one representative complete guide per learning level is implemented; the remaining topics in `docs/learning-path.md` remain planned work.
- Windows/PuTTY instructions have not been independently executed on a Windows machine.
- The in-circuit SPI flash workflow has not been independently hardware-verified; the guide's hardware-tested claim is limited to its described desoldered-chip workflow.
- External URLs are not live-checked by the offline link checker.
- No animated GIF is included; the project uses its original animated SVG plus a static social-preview PNG.
