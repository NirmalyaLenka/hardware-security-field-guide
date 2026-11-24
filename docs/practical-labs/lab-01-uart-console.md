# Lab 01 — Capture and Read a Boot Console

**Level:** Beginner · **Hardware required:** Yes (no simulator substitute for this one) · **Estimated time:** 30–45 minutes

## 1. What is this?

A guided, hands-on exercise that combines the [Electronics Fundamentals](../electronics/fundamentals.md) and [UART](../protocols/uart.md) pages into one complete task: capture and read a real device's boot log.

## 2. Why does it matter?

This is the smallest possible end-to-end exercise that mirrors real hardware-security work: identify an interface, confirm it's safe to connect to, connect correctly, and interpret the result.

## 3. How does it work?

See the linked pages above for the underlying theory. This lab only sequences the steps and tells you what success looks like.

## 4. What do you need?

- An ESP32 or Arduino-family dev board (any model with an onboard USB-to-serial chip works, which keeps this lab accessible without a separate adapter).
- A USB cable and a computer with a terminal program installed.
- No logic analyzer is required for this lab (that is introduced in [Finding an Unlabeled UART Console](../debugging/uart-console-discovery.md), which builds on this one).

## 5. How do you do it?

1. Connect the board to your computer via USB.
2. Identify its serial device node (`/dev/ttyUSB0`, `/dev/ttyACM0`, or a Windows `COM` port — see the [UART guide](../protocols/uart.md) for exact commands).
3. Open a terminal session at 115200 baud.
4. Press the board's reset button (or unplug/replug USB) while the terminal session is open.
5. Record the first 10 lines of output in your own notes, including anything that looks like a version string or chip identifier.

## 6. What should happen?

You should see a bootloader banner (on ESP32 boards, typically beginning with `ets ` followed by a build date, then chip and flash information) immediately after reset.

## 7. What can go wrong?

See the troubleshooting table in the [UART guide](../protocols/uart.md) — the same failure modes apply here.

## 8. Safety and limitations

Low risk: this lab uses only a board's own USB port and does not require opening the device or connecting external probes.

## 9. Verification status

Hardware-tested on an ESP32 DevKitC, November 2026, using the exact steps above.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- See the reference lists in [Electronics Fundamentals](../electronics/fundamentals.md) and [UART](../protocols/uart.md).
