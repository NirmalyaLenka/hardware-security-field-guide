# Contributing

Thank you for considering a contribution. This project prioritizes depth and verification over coverage — a short, correct, tested guide is more valuable than a long, unverified one.

## Before you start

- Check the [Learning Path](docs/learning-path.md) "planned, not yet written" notes for topics that are already scoped and welcome.
- Open an issue first for anything substantial, so the approach can be discussed before you invest time writing.

## Guide format

Every substantial guide must follow the ten-section template used throughout `docs/`:

1. What is this?
2. Why does it matter?
3. How does it work?
4. What do you need?
5. How do you do it?
6. What should happen?
7. What can go wrong?
8. Safety and limitations
9. Verification status
10. References

See [docs/protocols/uart.md](docs/protocols/uart.md) for a worked example.

## Verification status is mandatory and must be honest

Every guide must state whether it is hardware-tested, simulator-tested, reviewed-but-not-executed, or unverified, including the date and environment for anything actually tested. Do not mark something as tested if it was not. Reviewers will check this against the actual PR contents.

## Writing style

- Explain a term the first time it appears.
- Prefer concrete examples over abstract claims.
- Do not copy text, diagrams, or structure from other hardware-security references, including the project that inspired this one ([swisskyrepo/HardwareAllTheThings](https://github.com/swisskyrepo/HardwareAllTheThings)). Write original explanations.
- Cite real sources for factual claims (datasheets, standards, official vendor documentation). Do not invent dates, specifications, or history.

## Code examples

- State purpose, requirements, configuration, how to run, expected output, limitations, and any recovery/cleanup steps needed, as a header docstring/comment (see [`examples/protocol-demos/uart_logger.py`](examples/protocol-demos/uart_logger.py) for the expected format).
- Python examples must pass `python3 -m py_compile` at minimum; add a real test under `tests/` where practical.
- Do not hard-code credentials or secrets.

## Safety content

Any procedure capable of damaging hardware, or any procedure involving another party's device, must include an explicit "Safety and limitations" section covering voltage/compatibility risk and the authorization boundary from [docs/safety/index.md](docs/safety/index.md).

## Submitting

1. Fork the repository and create a branch for your change.
2. Follow the format above.
3. Run the checks described in [tests/README.md](tests/README.md) locally before opening a pull request.
4. Open a pull request describing what you verified and how.

## Code of conduct

Participation in this project is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
