#!/usr/bin/env python3
"""
Calibration script for HC-SR04. Reads distances and prints them in a loop.
Place a known distance object and record readings.
"""

import time
import argparse
import logging

from companion.sensors import HCSR04

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("calibrate_hcsr04")

def main(trig, echo):
    sensor = HCSR04(trig_pin=trig, echo_pin=echo)
    try:
        while True:
            dist = sensor.read_distance()
            logger.info("Distance: %s m", dist)
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Stopping calibration.")
    finally:
        sensor.cleanup()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trig", type=int, default=23)
    parser.add_argument("--echo", type=int, default=24)
    args = parser.parse_args()
    main(args.trig, args.echo)
