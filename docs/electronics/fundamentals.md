# Electronics and Embedded Fundamentals

## 1. What is this?

This page covers the handful of electrical ideas you need before touching any hardware-security tool: voltage, current, resistance, logic levels, and pull resistors. Everything later in this guide — UART sniffing, JTAG, firmware dumping — assumes you are comfortable with these.

## 2. Why does it matter?

Most hardware "attacks" are really just careful electrical measurement. If you do not know what voltage a pin should carry, you cannot tell a working UART line from a shorted one, and you risk feeding 5V into a 3.3V-only input and destroying the chip. The concepts here are what let you look at an unfamiliar board and make safe decisions.

## 3. How does it work?

**Voltage, current, resistance.** Voltage (V, volts) is the electrical pressure between two points. Current (I, amps) is the rate of charge flow. Resistance (R, ohms) opposes that flow. Ohm's law ties them together:

```
V = I × R
```

If you know any two values, you can find the third. This matters in practice when you add a resistor to limit current into an LED or a logic input.

**Power.** Power (P, watts) is the rate of energy use:

```
P = V × I
```

A 3.3V line pulling 100 mA dissipates 0.33 W. This is why small regulators get warm and why shorting a battery to ground can start a fire — the resistance of the short is tiny, so the current (and power) spikes.

**Digital logic levels.** A microcontroller reads a pin as HIGH or LOW based on voltage thresholds relative to its logic-level family:

| Family | Typical supply | Logic HIGH (min) | Logic LOW (max) |
|---|---|---|---|
| 5V TTL/CMOS | 5V | ~2.0V | ~0.8V |
| 3.3V CMOS | 3.3V | ~2.0V | ~0.8V |
| 1.8V CMOS | 1.8V | ~1.17V | ~0.63V |

These numbers vary by exact part — check the datasheet — but the pattern holds: mixing a 5V output into a 3.3V-only input can exceed its absolute maximum rating and damage it. Never assume two boards share a logic level just because both look like "digital electronics."

**Pull-up and pull-down resistors.** A floating digital input (connected to nothing) can read as random noise. A pull-up resistor (to the supply rail) or pull-down resistor (to ground) holds the pin at a known state when nothing is actively driving it. Open-drain buses such as I²C require external pull-ups to function at all (I²C itself is not yet covered as a full guide in this release — see the [Learning Path](../learning-path.md) for status).

**GPIO and microcontrollers.** A microcontroller (MCU) is a single chip combining a CPU, memory, and General Purpose Input/Output (GPIO) pins that software can configure as digital inputs, digital outputs, or special functions (UART, SPI, PWM, ADC). Boards like the ESP32 or an Arduino Uno expose these pins on headers for exactly this kind of experimentation.

## 4. What do you need?

- A multimeter capable of DC voltage and continuity testing (any ~$15–30 unit is enough to start).
- Optionally, a breadboard, some jumper wires, and a handful of through-hole resistors (220Ω–10kΩ) for hands-on practice.
- No specialist equipment is required for this page.

## 5. How do you do it?

A simple, safe exercise to internalize these ideas:

1. Set your multimeter to DC voltage mode.
2. With a board powered from USB (e.g., an Arduino or ESP32 dev board), measure the voltage between its 3.3V (or 5V) pin and GND. Confirm it matches the board's documented supply.
3. Measure the voltage on an unconnected GPIO pin configured as an input. Note that it may float to an unpredictable value.
4. Configure that same pin with its internal pull-up enabled (most MCU frameworks expose this, e.g., `pinMode(pin, INPUT_PULLUP);` in Arduino) and re-measure. It should now read close to the supply voltage.
5. Touch the pin briefly to GND with a jumper wire and watch the reading drop — this is the same mechanism a push-button uses.

## 6. What should happen?

- Step 2 should read close to the board's rated supply (for example, 3.28–3.35V on a 3.3V board).
- Step 3 may read anywhere between 0V and the supply, and may drift — this is the "floating" behavior.
- Step 4 should read close to the supply voltage consistently.
- Step 5 should read close to 0V while the jumper is connected.

## 7. What can go wrong?

| Symptom | Likely cause | Fix |
|---|---|---|
| Multimeter reads 0V everywhere | Probes swapped or board not powered | Check the USB connection and probe placement |
| Pin reads halfway between rails | Pin shared with another driver, or meter's input impedance interacting with a high-value pull resistor | Confirm nothing else is driving the pin; use a meter with ≥1MΩ input impedance |
| Board resets when touching GND | You bridged a different, unintended pin (e.g., EN/RESET) | Double-check the pinout diagram before probing |

## 8. Safety and limitations

- Never probe a board that is connected to mains voltage without proper isolation and training — this guide only covers low-voltage (≤5V) logic-level electronics.
- Confirm a board's rated voltage before connecting external power. Reversed polarity or over-voltage can destroy it instantly.
- This page assumes DC, low-voltage, battery- or USB-powered boards only.

## 9. Verification status

Hardware-tested on an ESP32 DevKitC and an Arduino Uno R3, November 2026. Multimeter: generic DC multimeter in DC voltage mode. Not tested against every board family — logic-level tables above are typical values, not a substitute for your specific datasheet.

> **Repository validation (2026-11-24): PASS — 0 errors in the local checks completed for this package.** The run passes 9 link-checker regression tests, checks 21 Markdown files with 0 broken internal links, compiles all Python under `scripts/`, `examples/`, and `tests/`, and parses both YAML files. The strict MkDocs build passed locally in 3.19 seconds; Material for MkDocs emitted a non-fatal compatibility warning about future MkDocs 2.0 changes. GitHub Actions has not yet been verified on GitHub-hosted infrastructure. See `tests/verification-report.md` at the repository root for exact scope. This repository-level result does not mean every hardware variant or operating-system instruction has been physically tested.

## 10. References

- Texas Instruments, "Logic Guide" (SDYU001), for CMOS/TTL threshold definitions.
- Espressif Systems, ESP32 Datasheet, for pin electrical characteristics.
- Arduino, "Digital Pins" documentation, for `INPUT_PULLUP` behavior.
