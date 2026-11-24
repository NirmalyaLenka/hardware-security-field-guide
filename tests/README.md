# Tests and Validation

This project's "tests" are lightweight, fast, offline checks appropriate to a documentation-and-examples repository — not a software test suite with full coverage targets.

## What exists today

| Check | Command | What it catches |
|---|---|---|
| Internal link check | `python -m scripts.check_links` or `python scripts/check_links.py` | Local Markdown links pointing at files that do not exist; ignores generated and dependency directories on Windows/macOS/Linux |
| Link-checker regression tests | `python -m unittest discover -s tests -p "test_*.py" -v` | Regressions in destination parsing, broken-link detection, encoded paths, root-relative links, and generated-directory exclusions |
| MkDocs strict build | `mkdocs build --strict` | Broken nav entries, unresolved relative links within `docs/`, config errors |
| Python syntax check | `python3 -m py_compile examples/protocol-demos/uart_logger.py` | Syntax errors in example scripts |

## Running everything locally

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -p "test_*.py" -v
python -m scripts.check_links
mkdocs build --strict
python -m compileall -q scripts examples tests
```

## Interpreting a clean result

A passing run means the automated checks listed above reported no errors in the current checkout. It validates documented file links, the checker regression tests, strict site generation, and Python syntax. It does not prove that every hardware instruction works on every device, that external URLs remain reachable, or that the workflow has passed on GitHub-hosted runners.

## What this does NOT verify

- That wiring instructions are electrically correct — that can only be confirmed by the hardware-testing claims in each guide's own "Verification status" section.
- That external (http/https) links are still live — the link checker is offline-only by design; a periodic manual or separate automated check would be needed for that.
- Markdown style/lint rules (no `markdownlint` config is included yet — see the project's `CHANGELOG.md` known-gaps list).

## Results from the most recent run

See [`verification-report.md`](verification-report.md) for the latest dated run, exact counts, environment, and limitations.
