# Autonomous UAV — Raspberry Pi 3 + Pixhawk (Obstacle Avoidance)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)]
[![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)]
[![Build](https://img.shields.io/badge/build-manual-orange.svg)]

> Companion-computer architecture for an autonomous multirotor using **Raspberry Pi 3** as companion computer and **Pixhawk** as flight controller. Provides obstacle avoidance using onboard sensors (HC-SR04 / LiDAR / Camera) and MAVLink commands via MAVSDK / pymavlink.

---

## Table of contents
- [Overview](#overview)  
- [Features](#features)  
- [Repository structure](#repository-structure)  
- [Hardware required](#hardware-required)  
- [Software & dependencies](#software--dependencies)  
- [Wiring (quick)](#wiring-quick)  
- [Quick start (Pi preparation)](#quick-start-pi-preparation)  
- [Running the companion program](#running-the-companion-program)  
- [Configuration](#configuration)  
- [Testing & safety checklist](#testing--safety-checklist)  
- [Logging & debugging](#logging--debugging)  
- [Troubleshooting](#troubleshooting)  
- [Contributing](#contributing)  
- [License](#license)  
- [Acknowledgements](#acknowledgements)

---

## Overview
This repository contains the companion-computer software, wiring diagrams, documentation and helper scripts to integrate a Raspberry Pi 3 with a Pixhawk flight controller to implement onboard obstacle detection and simple avoidance maneuvers. The Pi runs sensor drivers and a MAVLink client (MAVSDK / pymavlink) and issues velocity / position commands to Pixhawk.

This project focuses on a modular design so you can swap sensors (ultrasonic, RPLIDAR, LiDAR-Lite, camera) and algorithms (reactive vs. planner-based) without changing the flight controller firmware.

---

## Features
- Serial MAVLink link between Raspberry Pi and Pixhawk (TELEM2)  
- Basic obstacle-detection pipeline for HC-SR04 ultrasonic and RPLIDAR (extensible)  
- Camera capture (OpenCV) hooks for future vision-based avoidance (TFLite examples in `src/vision.py`)  
- Example Offboard velocity commands using MAVSDK-Python  
- `systemd` service example to auto-start on boot  
- SITL examples for safe algorithm testing before hardware flights  
- Documentation and wiring diagrams for safe assembly

---

## Repository structure
```
autonomous-uav-obstacle-avoidance/
├── .github/
│   ├── ISSUE_TEMPLATE.md
│   └── workflows/
│       └── python-ci.yml
├── docs/
│   ├── wiring/
│   │   ├── pixhawk-pi-telemetry.png
│   │   └── power-diagram.png
│   ├── sensors.md
│   ├── wiring.md
│   └── testing-checklist.md
├── hardware/
│   ├── bill_of_materials.md
│   ├── 3d-print-files/        # (optional) mechanical mounts, STL
│   └── schematics/            # png / svg wiring schematics
├── src/
│   ├── companion/             # companion computer code (python package)
│   │   ├── _init_.py
│   │   ├── main.py            # entrypoint (the script we discussed)
│   │   ├── sensors.py         # ultrasonic / lidar wrappers
│   │   ├── vision.py          # OpenCV / TFLite helpers (optional)
│   │   ├── mavlink_client.py  # MAVSDK wrapper + connection logic
│   │   ├── controllers.py     # avoidance / maneuver functions
│   │   └── config.py          # configurable constants (baud, pins, thresholds)
│   └── tools/
│       ├── calibrate_hcsr04.py
│       └── parse_logs.py
├── examples/
│   ├── start_companion.sh
│   ├── companion.service      # systemd service file (for /etc/systemd/system/)
│   └── sitl/                  # SITL launch scripts & examples
│       └── sitl_launch.sh
├── requirements.txt
├── setup.sh                   # convenience script to prep a Pi (installs deps)
├── README.md
├── LICENSE
├── .gitignore
└── CHANGELOG.md 
```

---

## Hardware required
Minimum:
- Pixhawk (PX4 or ArduPilot-compatible)  
- Raspberry Pi 3 (with power supply, recommended 5V 2.5–3A)  
- HC-SR04 ultrasonic sensor *or* RPLIDAR A1/A2 (optional)  
- Raspberry Pi Camera or USB camera  
- Level-shift / TTL-compatible connections or wiring harness for TELEM2  
- Common ground between Pi and Pixhawk, appropriate BECs/regulators  
- Propellers removed for bench-testing (mandatory)

See `hardware/bill_of_materials.md` for manufacturer parts and approximate pricing.

---

## Software & dependencies
- Raspberry Pi OS (Bullseye/Bookworm recommended)  
- Python 3.8+  
- Key Python packages (example pinned versions in `requirements.txt`):
  - `mavsdk` or `pymavlink`
  - `opencv-python`
  - `RPi.GPIO`
  - `rplidar` (if using RPLIDAR)
  - `grpcio` (for MAVSDK)
- System tools: `git`, `screen` / `minicom` (for debugging)

Full install commands are in `setup.sh`.

---

## Wiring (quick)
1. **Pixhawk TELEM2 ↔ Raspberry Pi UART**
   - Pixhawk TELEM2 TX → Raspberry Pi **RX (GPIO15, physical pin 10)**  
   - Pixhawk TELEM2 RX → Raspberry Pi **TX (GPIO14, physical pin 8)**  
   - Pixhawk GND → Raspberry Pi **GND (physical pin 6)**

2. **Sensor wiring**
   - HC-SR04: TRIG → Pi GPIO (configurable e.g., GPIO23), ECHO → Pi GPIO (GPIO24). Use level-shifter or correct resistor divider if necessary.  
   - RPLIDAR: usually USB or UART adapter; ensure correct 5V/3.3V levels.  

![Pixhawk ↔ Pi wiring](docs/wiring/pixhawk-pi-telemetry.png)
*Figure: Pixhawk TELEM2 ↔ Raspberry Pi UART wiring (TX↔RX, GND common).*

---

## Quick start (Pi preparation)
**On the Pi:**
```bash
# update
sudo apt update && sudo apt upgrade -y

# install system deps
sudo apt install -y python3-pip python3-opencv python3-rpi.gpio git

# clone repo (example)
git clone https://github.com/your-username/autonomous-uav-obstacle-avoidance.git
cd autonomous-uav-obstacle-avoidance

# run setup script (installs pip deps)
chmod +x setup.sh
./setup.sh

# (Optional) Disable serial console and free /dev/serial0 via raspi-config
sudo raspi-config
# Interfacing Options -> Serial -> No login shell over serial, Yes enable serial port
```

**Enable hardware UART (if using Pi3 and you want to free the serial bus from Bluetooth):**
Add `dtoverlay=disable-bt` to `/boot/config.txt` and run:
```bash
sudo systemctl disable hciuart
sudo reboot
```

---

## Running the companion program
1. Edit `src/companion/config.py` to set serial port (`/dev/serial0`), baud (e.g., `57600`), and sensor GPIO pins.  
2. Start manually (for testing):
```bash
python3 src/companion/main.py
```
3. Install service for auto-start:
```bash
sudo cp examples/companion.service /etc/systemd/system/companion.service
sudo systemctl daemon-reload
sudo systemctl enable companion.service
sudo systemctl start companion.service
sudo journalctl -u companion.service -f
```

> Always test while **props are removed**. Confirm communication in QGroundControl or MAVProxy.

---

## Configuration
Edit `src/companion/config.py`. Typical settings:
```py
SERIAL_PORT = "/dev/serial0"
BAUDRATE = 57600    # or 921600 depending on Pixhawk settings
HC_SR04_TRIG = 23
HC_SR04_ECHO = 24
DISTANCE_THRESHOLD_M = 1.0  # avoidance distance
CAMERA_INDEX = 0
LOG_LEVEL = "INFO"
```

---

## Testing & safety checklist
- [ ] Props removed during bench tests  
- [ ] Confirm /dev/serial0 exists and connects to Pixhawk  
- [ ] Check QGroundControl shows MAVLink messages from TELEM2  
- [ ] Run `python3 src/companion/main.py` with `LOG_LEVEL=DEBUG` and validate sensor readings  
- [ ] Validate avoidance command by watching values in QGC or MAVProxy (no motors attached)  
- [ ] SITL test before hardware flights (see `examples/sitl/`)

Full testing checklist in `docs/testing-checklist.md`.

---

## Logging & debugging
- Logs are printed to stdout and saved (if `LOG_DIR` configured).  
- Use `sudo journalctl -u companion.service -f` to view logs when running as systemd service.  
- For raw MAVLink inspection: `mavproxy.py --master=/dev/serial0 --baudrate 57600`

---

## Troubleshooting
**Common problems**
- *No connection to Pixhawk*: verify TELEM2 baud and that serial console disabled on Pi.  
- *HC-SR04 reports garbage or zero*: check wiring and that ECHO uses safe 3.3V level.  
- *Camera not found*: try `ls /dev/video*` and ensure `vcgencmd` / `libcamera` setup for Pi camera.

If stuck, open an issue with: Pi OS version, Python version, hardware photos, log snippet.

---

## Contributing
Contributions are welcome. Please:
1. Fork the repo  
2. Create a feature branch (`feature/<name>`)  
3. Open a PR and include testing steps / hardware used

See `.github/ISSUE_TEMPLATE.md` for issue reporting guidelines.

---

## License
This project is released under the **MIT License** — see `LICENSE` for details.

---

## Acknowledgements
- MAVSDK and pymavlink projects for MAVLink connectivity.  
- Pixhawk / PX4 / ArduPilot communities for documentation and examples.
