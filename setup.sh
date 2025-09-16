#!/usr/bin/env bash
set -euo pipefail

# Convenience setup script for Raspberry Pi (Bullseye / Bookworm)
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing system packages..."
sudo apt install -y python3-pip python3-opencv python3-rpi.gpio git build-essential libatlas-base-dev libjpeg-dev

echo "Upgrading pip..."
python3 -m pip install --upgrade pip setuptools wheel

echo "Installing Python packages from requirements..."
python3 -m pip install -r requirements.txt

echo "Disabling serial console (manual prompt will be shown)."
echo "Run: sudo raspi-config -> Interfacing Options -> Serial -> Disable login shell -> Enable serial port"
read -p "Press ENTER to continue after making the raspi-config changes (or Ctrl+C to abort)"

echo "If you are using Raspberry Pi 3 and want to free the hardware UART, adding 'dtoverlay=disable-bt' to /boot/config.txt is recommended."
echo "You can run:"
echo "  sudo bash -c \"echo 'dtoverlay=disable-bt' >> /boot/config.txt\""
echo "  sudo systemctl disable hciuart"
echo "Then reboot."

echo "Setup complete. Please verify /dev/serial0 exists and your Pixhawk TELEM2 baud matches SERIAL_PORT settings."
