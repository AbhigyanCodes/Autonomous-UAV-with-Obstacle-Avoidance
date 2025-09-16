# Wiring Guide

This file gives step-by-step wiring instructions and safety notes.

## Pixhawk ↔ Raspberry Pi (TELEM2)
- Pixhawk TELEM2 TX -> Raspberry Pi RX (GPIO15, physical pin 10)
- Pixhawk TELEM2 RX -> Raspberry Pi TX (GPIO14, physical pin 8)
- Pixhawk GND -> Raspberry Pi GND (physical pin 6)

**Important**
- Cross TX↔RX (TX from pixhawk to RX on Pi).
- Ensure common ground.
- Confirm Pixhawk TELEM2 baud rate parameter (e.g., SER_TEL2_BAUD or SERIALx_BAUD) matches Pi side (57600/921600).

![Pixhawk ↔ Pi wiring](wiring/pixhawk-pi-telemetry.png)

## Powering options
See `power-diagram.png` for recommended power distribution choices:
- Option A: Separate 5V power supply for Pi (recommended)
- Option B: Use Pixhawk BEC to power Pi (only if BEC can supply stable 5V and enough current)
- Never power Pi from Pixhawk USB in-flight; ensure proper regulation.

## Sensor wiring examples
- HC-SR04 TRIG -> Pi GPIO (e.g., BCM23)
- HC-SR04 ECHO -> Pi GPIO (e.g., BCM24) through resistor divider

Refer to `docs/sensors.md` for sensor-specific details.
