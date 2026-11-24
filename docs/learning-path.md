# Learning Path

Work through these in order. Each level builds on the skills and vocabulary of the one before it.

## Level 1 — Electronics and embedded fundamentals
- [Electronics Fundamentals](electronics/fundamentals.md) — voltage, current, logic levels, pull resistors. *(Available now.)*
- Multimeter and logic-analyzer basics, datasheet reading — *planned, not yet written.*

## Level 2 — Communication protocols
- [UART](protocols/uart.md) — the most common debug interface. *(Available now.)*
- I²C, SPI, Wi-Fi/BLE, RFID/NFC, LoRa, Modbus — *planned, not yet written.*

## Level 3 — Debugging and hardware inspection
- [Finding an Unlabeled UART Console](debugging/uart-console-discovery.md) *(Available now.)*
- JTAG/SWD discovery, chip identification — *planned, not yet written.*

## Level 4 — Firmware and boot processes
- [Firmware Basics: Acquiring and Inspecting an Image](firmware/firmware-basics.md) *(Available now.)*
- Filesystem extraction, boot log analysis, secure boot concepts — *planned, not yet written.*

## Level 5 — Hardware and IoT security
- [Threat Modeling](hardware-security/threat-modeling.md) *(Available now.)*
- Default credentials, secrets-in-firmware, secure update mechanisms, responsible disclosure — *planned, not yet written.*

## Level 6 — Practical labs
- [Lab 01: Capture and Read a Boot Console](practical-labs/lab-01-uart-console.md) *(Available now.)*
- Further labs building on Levels 2–5 — *planned, not yet written.*

## Honest status

This first release implements one complete, verified guide per level so the structure, the writing template, and the verification process are all demonstrated end-to-end. The remaining topics listed in each level are real gaps, not hidden ones — see `CHANGELOG.md` and `tests/verification-report.md` at the repository root for the current verification scope and known limitations.
