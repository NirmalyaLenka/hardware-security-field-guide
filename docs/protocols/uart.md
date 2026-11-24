# UART (Universal Asynchronous Receiver/Transmitter)

## 1. What is this?

UART is a simple, two-wire, asynchronous serial protocol for sending bytes between two devices. No shared clock line is used — both sides agree in advance on a speed (baud rate) and timing format.

## 2. Why does it matter?

UART is the single most common "debug door" left open on embedded and IoT devices. Manufacturers use it during development to print boot logs and reach a shell, and frequently forget to disable it before shipping. Finding and reading a UART console is often the fastest way to understand what firmware a device is running.

## 3. How does it work?

Two devices connect TX (transmit) on one to RX (receive) on the other, and share a common ground:

```
Device A TX ----> Device B RX
Device A RX <---- Device B TX
Device A GND ---- Device B GND
```

Each byte is framed as: a start bit (line pulled low), the data bits (usually 8, least-significant-bit first), an optional parity bit, and one or more stop bits (line returns high). Both ends must agree on the baud rate (bits per second) — common values are 9600, 57600, and 115200 — or the receiver will misinterpret the bit timing and produce garbage characters.

UART has no addressing and no clock recovery beyond the agreed baud rate, which is why it only works point-to-point between exactly two devices.

## 4. What do you need?

- A USB-to-UART (often called USB-to-serial or USB-to-TTL) adapter using a chip such as the CP2102, CH340, or FT232. Confirm it supports your target's voltage (3.3V and 5V variants exist, and some are switchable).
- Jumper wires.
- A terminal program: `minicom` or `screen` on Linux/macOS, or PuTTY on Windows.
- A target board with an exposed UART header or test points (an ESP32 or Arduino dev board exposes this intentionally, which is ideal for learning before looking at unlabeled hardware).

## 5. How do you do it?

**Wiring (adapter to target), matching logic levels — see [Electronics Fundamentals](../electronics/fundamentals.md) before mixing voltages:**

| Adapter pin | Target pin |
|---|---|
| GND | GND |
| TX | RX |
| RX | TX |

Note the cross-over: TX always connects to RX, never TX-to-TX.

**Linux/macOS, using `screen`:**

```bash
# Identify the device node (varies by OS/driver)
ls /dev/tty.* /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# Connect at a common baud rate
screen /dev/ttyUSB0 115200
```

Exit `screen` with Ctrl-A then K, then confirm.

**Windows, using PuTTY:**

1. Open Device Manager and note the COM port number under "Ports (COM & LPT)".
2. In PuTTY, select connection type "Serial", enter the COM port and the baud rate (start with 115200), then click Open.

**If you see only garbled characters:** the baud rate is wrong. Try the other common values (9600, 57600, 230400) one at a time — most consumer boot loaders use one of these.

## 6. What should happen?

On a device actively printing to UART, you should see readable boot-log text (bootloader version, memory sizes, partition tables) scroll by immediately after power-on, possibly followed by an interactive shell prompt.

## 7. What can go wrong?

| Symptom | Likely cause | Fix |
|---|---|---|
| Nothing at all appears | Wrong baud rate, TX/RX not crossed, or UART disabled in firmware | Re-check wiring cross-over; try other baud rates; confirm with a logic analyzer that the line is toggling at all |
| Garbled text | Baud rate mismatch | Try the common values listed above |
| Device resets repeatedly | Adapter is back-powering the board through its 5V/3.3V pin while USB power is also connected | Connect only GND/TX/RX, not the power pin, unless you intend to power the board from the adapter |
| No shell, only logs | Console output is often present even when interactive input is disabled | This is common and expected on production firmware; do not assume a shell exists |

## 8. Safety and limitations

- Only connect TX/RX/GND between devices that share a known logic level, or use a level-shifter. Connecting a 5V TX into a 3.3V-only RX can damage the receiving pin.
- Only probe hardware you own or are explicitly authorized to examine.
- A UART console, if present, may expose credentials, keys, or an unauthenticated root shell. Treat anything you recover from a device you don't own as sensitive and handle it according to the device owner's policy and responsible disclosure norms — see [Hardware Security: Threat Modeling](../hardware-security/threat-modeling.md).

## 9. Verification status

Hardware-tested with a CP2102-based USB-UART adapter against an ESP32 DevKitC's factory boot log, November 2026, on Linux using `screen` at 115200 baud. Windows/PuTTY steps are reviewed but not independently executed in this verification pass.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- Espressif Systems, "ESP32 Series Datasheet", UART section.
- Silicon Labs, CP2102 USB-to-UART Bridge datasheet.
