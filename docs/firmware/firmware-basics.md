# Firmware Basics: Acquiring and Inspecting an Image

## 1. What is this?

An introduction to what a firmware image actually is, how to get a copy of one from a device you own, and how to take a first look inside it safely — without flashing anything back.

## 2. Why does it matter?

Before you can analyze a device's security, you need a firmware image and you need to know you have an unmodified copy of it. Hashing and preserving your original dump is what makes every later step reproducible and trustworthy.

## 3. How does it work?

Firmware is simply the binary content of a device's flash memory: bootloader, application code, and often a filesystem holding configuration and web assets. On many IoT boards this is a SPI NOR flash chip (common sizes: 1MB–16MB) that can be read either in-circuit (while still soldered to the board, via its SPI pins) or off-circuit (removed and read in a dedicated chip clip/programmer). Once read, the raw image is just bytes — tools like `binwalk` can recognize common signatures inside it (filesystem headers, compression magic numbers) to help you find where each component starts.

## 4. What do you need?

- A SPI flash programmer (e.g., a CH341A-based USB programmer, inexpensive and widely available) or an in-circuit SPI connection from a microcontroller/logic-level adapter.
- `flashrom` (open source) for reading the chip, or the vendor tool that ships with your programmer.
- `binwalk` for inspecting the resulting image.
- A device you own, with its flash chip identified (check the markings against its datasheet before connecting anything).

## 5. How do you do it?

**Read the chip (example using `flashrom` with a CH341A-style programmer, Linux):**

```bash
# Identify the chip (do this before writing anything)
flashrom -p ch341a_spi

# Read a full copy, twice, to a file each time
flashrom -p ch341a_spi -r dump1.bin
flashrom -p ch341a_spi -r dump2.bin
```

**Verify the two reads match before trusting either one:**

```bash
sha256sum dump1.bin dump2.bin
```

If the hashes differ, the chip was likely being written to during one of the reads (e.g., the device was powered and actively running) — power the board down fully, or isolate the chip, and read again.

**Inspect the image:**

```bash
binwalk dump1.bin
```

This prints a list of offsets where `binwalk` recognizes known structures (e.g., a `squashfs` filesystem, a U-Boot header, gzip-compressed data).

**Extract recognized filesystems:**

```bash
binwalk -e dump1.bin
```

## 6. What should happen?

Two independent reads should produce identical SHA-256 hashes. `binwalk` should report at least a bootloader signature and, on most consumer devices, a Linux filesystem (SquashFS, JFFS2, or similar) starting at some non-zero offset.

## 7. What can go wrong?

| Symptom | Likely cause | Fix |
|---|---|---|
| `flashrom` reports no chip found | Programmer not connected to all required SPI lines (CS, CLK, MOSI, MISO, VCC, GND) or chip not isolated from board power | Re-check the pinout against the chip's datasheet; for in-circuit reads, some designs require isolating the chip's VCC pin while the programmer supplies its own |
| Two reads don't match | Chip was live/being written during read | Power down fully, or desolder for an off-circuit read |
| `binwalk` finds nothing recognizable | Image is encrypted, or offsets are non-standard | Note this as a finding rather than forcing an extraction; encrypted firmware is a legitimate and increasingly common outcome |

## 8. Safety and limitations

- Confirm the chip's supply voltage (1.8V, 3V, or 3.3V are all common) before connecting a programmer — over-voltage can destroy the chip.
- Reading flash in-circuit can fail or produce corrupted data if the board's own processor is also trying to access the bus. Some boards require isolating a supply or signal connection, but the correct pin and method are device-specific: identify the exact chip, read its datasheet and the board design before making any change. Never infer a pin function from its number or lift/tape a pin based on a generic guide.
- Only dump firmware from hardware you own or are explicitly authorized to analyze. Firmware often contains vendor-proprietary code; redistributing it may violate the vendor's license even when the analysis itself is legitimate.

## 9. Verification status

Hardware-tested with a CH341A USB programmer and `flashrom` 1.2 against a desoldered Winbond W25Q32 SPI NOR chip from a decommissioned router (owned by the author), November 2026. In-circuit reads without desoldering were reviewed but not independently verified in this pass — see the repository-level limitations in `tests/verification-report.md`.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- `flashrom` project documentation and supported-programmer list.
- `binwalk` project documentation.
- Winbond W25Q32 datasheet, for pinout and voltage range.
