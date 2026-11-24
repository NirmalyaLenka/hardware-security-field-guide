# Glossary

**Baud rate** — The number of signal changes per second on a UART line; both ends must agree on it for bytes to decode correctly.

**Bootloader** — The first code a device runs after power-on, responsible for loading and starting the main application firmware.

**Firmware** — The software stored in a device's non-volatile memory that controls its hardware.

**GPIO** — General Purpose Input/Output; a microcontroller pin that software can configure as a digital input or output.

**JTAG** — Joint Test Action Group; a standardized hardware debug interface allowing direct control of a chip's internals, including memory and registers.

**Logic analyzer** — A tool that records digital signal transitions on multiple channels over time, used to observe and decode protocols like UART, I²C, and SPI.

**Pull-up / pull-down resistor** — A resistor that holds a digital input at a known voltage (high or low) when nothing else is actively driving it.

**SPI** — Serial Peripheral Interface; a synchronous, clocked, multi-wire protocol commonly used to talk to flash memory chips and other peripherals.

**SWD** — Serial Wire Debug; a two-wire alternative to JTAG, common on ARM Cortex-M microcontrollers.

**Threat model** — A structured list of a system's assets, attack surfaces, and trust boundaries, used to prioritize what to test and why.

**UART** — Universal Asynchronous Receiver/Transmitter; a simple two-wire serial protocol with no shared clock, widely used for debug consoles.
