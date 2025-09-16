# Sensors — Notes & Wiring

This document explains supported sensors and wiring notes.

## HC-SR04 Ultrasonic
- VCC: 5V
- GND: GND (common with Raspberry Pi & Pixhawk)
- TRIG: GPIO output (e.g., BCM 23)
- ECHO: GPIO input (e.g., BCM 24) — **use a 1k / 2k resistor divider or level shifter** to bring 5V ECHO down to 3.3V.

### Characteristics
- Range: ~2 cm – 400 cm (practical useful: 3 cm – 300 cm)
- Beam width: wide; mount with cone-shaped shroud for better directionality
- Slow (~40 Hz max)

## RPLIDAR A1/A2
- Connect via USB or UART adaptor.
- If using UART, ensure voltage levels match (3.3V vs 5V).
- Use `rplidar` Python package to read scans.

## Camera
- Either Raspberry Pi Camera (CSI) or USB webcam.
- For Pi Camera use libcamera / picamera2 (newer Pi OS); for USB camera use OpenCV `cv2.VideoCapture(0)`.

## Mounting tips
- Place ultrasonic sensor at the front with clear FOV
- Place LIDAR near center for 360-degree scans (if available)
- Camera mounting height influences perspective; consider tilt for horizon balancing
