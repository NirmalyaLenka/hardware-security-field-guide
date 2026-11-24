#!/usr/bin/env python3
"""
uart_logger.py

Purpose:
    Connects to a serial (UART) device and logs incoming lines to both the
    terminal and a timestamped file. Companion script to
    docs/protocols/uart.md and docs/practical-labs/lab-01-uart-console.md.

Required equipment / dependencies:
    - A device exposing a serial console (e.g., an ESP32 dev board over its
      onboard USB-to-UART chip), connected over USB.
    - Python 3.8+
    - pyserial >= 3.5  (pip install pyserial)

Configuration:
    Edit PORT and BAUD_RATE below, or pass them as command-line arguments:
        python3 uart_logger.py /dev/ttyUSB0 115200

How to run:
    python3 uart_logger.py [port] [baud_rate]

Expected output:
    Each received line is printed to stdout and appended to a file named
    uart_log_<ISO8601 timestamp>.txt in the current directory. Press Ctrl+C
    to stop; the script closes the serial port and the log file cleanly.

Limitations:
    - Assumes line-oriented, newline-terminated text output (typical of
      bootloader/console logs). Binary protocols are not handled here.
    - Does not send any data to the device; it is a passive logger only,
      intended to be safe to run against hardware you are just getting to
      know.

Recovery / cleanup:
    This script does not alter device state. No cleanup beyond closing the
    serial port (handled automatically) is required.
"""

import sys
import time
import datetime

try:
    import serial
except ImportError:
    print("This script requires pyserial. Install it with:")
    print("    pip install pyserial")
    sys.exit(1)

DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUD_RATE = 115200


def main():
    port = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PORT
    baud_rate = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_BAUD_RATE

    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    log_filename = f"uart_log_{timestamp}.txt"

    print(f"Opening {port} at {baud_rate} baud. Logging to {log_filename}.")
    print("Press Ctrl+C to stop.")

    try:
        with serial.Serial(port, baud_rate, timeout=1) as ser, \
                open(log_filename, "w", encoding="utf-8", errors="replace") as log_file:
            while True:
                try:
                    raw_line = ser.readline()
                except serial.SerialException as exc:
                    print(f"Serial error: {exc}")
                    break

                if not raw_line:
                    continue  # timeout with no data; loop and check again

                line = raw_line.decode("utf-8", errors="replace").rstrip("\r\n")
                stamped = f"[{time.strftime('%H:%M:%S')}] {line}"
                print(stamped)
                log_file.write(stamped + "\n")
                log_file.flush()

    except serial.SerialException as exc:
        print(f"Could not open {port}: {exc}")
        print("Check the port name and that no other program has it open.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nStopped by user. Log saved to", log_filename)


if __name__ == "__main__":
    main()
