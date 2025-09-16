#!/usr/bin/env python3
"""
main.py
Entrypoint for the companion computer. Connects to Pixhawk via MAVSDK and
runs a simple obstacle avoidance loop using HC-SR04 and optional camera.
"""

import asyncio
import logging
import os
import signal

from mavsdk import System
from mavsdk.offboard import OffboardError
from datetime import datetime

from .config import SERIAL_PORT, BAUDRATE, HC_SR04_TRIG, HC_SR04_ECHO, DISTANCE_THRESHOLD_M, CAMERA_INDEX, LOG_DIR, LOG_LEVEL, OFFBOARD_VELOCITY_DURATION
from .sensors import HCSR04
from .vision import open_camera, read_frame, release_camera
from .mavlink_client import MAVClient
from .controllers import simple_reactive_avoidance

# Setup logging
log_level = os.getenv("LOG_LEVEL", LOG_LEVEL).upper()
logging.basicConfig(level=getattr(logging, log_level), format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger("companion.main")

# Ensure log dir exists if configured
if LOG_DIR:
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except Exception:
        logger.debug("Could not create LOG_DIR: %s", LOG_DIR)


stop_signal = False


def _signal_handler(sig, frame):
    global stop_signal
    logger.info("Caught signal %s, exiting...", sig)
    stop_signal = True


async def main_loop():
    serial_url = f"serial://{SERIAL_PORT}:{BAUDRATE}"
    mav = MAVClient(serial_url)
    await mav.connect()

    # Sensors
    hcsr = HCSR04(trig_pin=HC_SR04_TRIG, echo_pin=HC_SR04_ECHO)

    # Camera
    cap = open_camera(CAMERA_INDEX)

    try:
        while not stop_signal:
            # Read sensor
            dist = hcsr.read_distance()
            logger.info("Distance: %s m", dist)

            # Camera read (non-blocking)
            if cap:
                frame_info = read_frame(cap)
                if frame_info:
                    ret, frame = frame_info
                    # For now, only log frame shape
                    logger.debug("Camera frame: %s", frame.shape)

            # Decide avoidance
            action = simple_reactive_avoidance(dist, DISTANCE_THRESHOLD_M)
            if action:
                north, east, down, yaw_deg, duration = action
                # Use MAVSDK offboard to send velocity setpoint
                try:
                    await mav.start_offboard_velocity(north, east, down, yaw_deg, duration)
                except Exception as e:
                    logger.exception("Failed to execute offboard velocity: %s", e)

            await asyncio.sleep(0.5)

    finally:
        if cap:
            release_camera(cap)
        hcsr.cleanup()
        logger.info("Cleaned up sensors and exiting.")


def main():
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    logger.info("Starting companion main")
    try:
        asyncio.run(main_loop())
    except Exception as e:
        logger.exception("Fatal error in companion main: %s", e)


if __name__ == "__main__":
    main()
