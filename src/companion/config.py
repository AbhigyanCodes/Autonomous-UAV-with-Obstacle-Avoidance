"""
Configuration constants for the companion computer.
Edit these values to match your hardware.
"""

# Serial / MAVLink
SERIAL_PORT = "/dev/serial0"  # or '/dev/ttyUSB0' if using USB adapter
BAUDRATE = 57600             # or 921600 depending on Pixhawk setting

# HC-SR04 (BCM numbering)
HC_SR04_TRIG = 23
HC_SR04_ECHO = 24
DISTANCE_THRESHOLD_M = 1.0  # meters

# Camera
CAMERA_INDEX = 0

# Logging & runtime
LOG_LEVEL = "INFO"
LOG_DIR = "/var/log/companion"  # requires write permission for service user

# MAVSDK Offboard params
OFFBOARD_VELOCITY_DURATION = 1.5  # seconds for avoidance velocity command
