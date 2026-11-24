# Finding an Unlabeled UART Console

## 1. What is this?

A method for locating an undocumented UART interface on a board that has no helpful silkscreen labels — the common situation with consumer IoT devices.

## 2. Why does it matter?

Vendors frequently leave a debug UART connected to test points or an unpopulated header without documenting it. Finding it is usually the first practical step in understanding what a device is actually running.

## 3. How does it work?

A UART console idles HIGH (close to the supply voltage) when nothing is being sent, and toggles rapidly during boot. TX is usually the busiest line in the first second after power-on, because the bootloader is printing. GND is identifiable by continuity to the board's known ground (e.g., a shield can, a mounting screw, or the negative battery terminal). This lets you identify candidate pins with a multimeter and a logic analyzer alone, without guessing from a schematic.

## 4. What do you need?

- A multimeter (continuity and DC voltage mode).
- A basic 8-channel logic analyzer (e.g., a Saleae-compatible clone) and its software (such as `sigrok`/`PulseView`, which is free and open source).
- A USB-to-UART adapter, once candidate pins are identified (see [UART](../protocols/uart.md)).
- The target board, powered off until probing is complete.

## 5. How do you do it?

1. **Find GND** with the board powered off: use continuity mode between a point you can visually confirm is ground (a shield, a mounting hole, a battery negative terminal) and candidate header pins.
2. **Identify candidate signal pins**: look for 3–4 pin headers or exposed pads near the main SoC, often labeled only with silkscreen dots, or not labeled at all.
3. **Attach logic analyzer probes** to GND and each candidate pin.
4. **Power on the board** while capturing in `PulseView` (or equivalent), sampling at least 1 MHz (UART at 115200 baud needs roughly 10x oversampling to decode reliably).
5. **Look for toggling activity** in the first 1–2 seconds after power-on. A line with no bootloader will stay flat.
6. **Add the UART decoder** in your analyzer software to the busiest line and try common baud rates (9600, 57600, 115200) until the decoded bytes look like readable text.
7. Once TX is confirmed, connect your USB-to-UART adapter as described in the [UART guide](../protocols/uart.md).

## 6. What should happen?

The logic analyzer trace on the correct TX pin should show a burst of activity immediately after power-on, and the UART decoder should render recognizable ASCII (bootloader banners, memory addresses, log lines) once the baud rate is correct.

## 7. What can go wrong?

| Symptom | Likely cause | Fix |
|---|---|---|
| No activity on any candidate pin | UART physically disabled, fused off, or pins misidentified | Re-check continuity to ground; look for other candidate pads; consult the SoC datasheet for default UART pin assignments |
| Decoder shows only noise | Wrong baud rate or sample rate too low | Increase sample rate; sweep baud rates |
| Board does not power on while probing | A probe is shorting two pins together | Remove probes, re-check placement with the board off |

## 8. Safety and limitations

- Keep the board powered off while placing probes to avoid accidental shorts.
- Only perform this on hardware you own or are authorized to examine.
- Some devices use the exposed pins for something other than UART (e.g., SWD, or factory test signals that are not safe to drive externally) — observe passively first; do not drive a pin until you know its function.

## 9. Verification status

Hardware-tested on a consumer Wi-Fi smart plug (undisclosed model, owned by the author) using an 8-channel logic analyzer clone and `PulseView` 0.4, November 2026. Not tested against boards using 1.8V-only logic, which may fall below some analyzers' input-threshold range.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- `sigrok` / `PulseView` project documentation, UART protocol decoder.
- General hobbyist practice described in community teardown write-ups; no single authoritative source — treat this as an established technique rather than one invented here.
