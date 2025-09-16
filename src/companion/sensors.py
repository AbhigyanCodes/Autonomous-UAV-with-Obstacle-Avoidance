"""
sensors.py
Provides simple wrappers for HC-SR04 ultrasonic sensor and (optional) RPLIDAR.
HC-SR04 uses RPi.GPIO and software pulses to measure distance.
"""

import time
import logging

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO  # type: ignore
    GPIO_AVAILABLE = True
except (RuntimeError, ModuleNotFoundError):
    GPIO_AVAILABLE = False
    # In CI or non-Pi environments, this will fall back to a stub for testing.


class HCSR04:
    def __init__(self, trig_pin: int, echo_pin: int, gpio_mode=GPIO.BCM):
        if not GPIO_AVAILABLE:
            logger.warning("RPi.GPIO not available; HCSR04 will not work on this platform.")
        self.trig = trig_pin
        self.echo = echo_pin
        self._setup(gpio_mode)

    def _setup(self, gpio_mode):
        if not GPIO_AVAILABLE:
            return
        GPIO.setmode(gpio_mode)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(0.2)

    def read_distance(self, timeout=0.02):
        """Returns distance in meters, or None if timed out / cannot read."""
        if not GPIO_AVAILABLE:
            logger.debug("GPIO not available; returning None for distance.")
            return None

        # Send trigger pulse
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)

        start = time.time()
        # Wait for echo to go high
        while GPIO.input(self.echo) == 0:
            start = time.time()
            if start + timeout < time.time():
                logger.debug("Timeout waiting for echo start")
                return None

        stop = time.time()
        while GPIO.input(self.echo) == 1:
            stop = time.time()
            if stop - start > timeout:
                logger.debug("Timeout waiting for echo end")
                return None

        pulse_duration = stop - start
        distance_m = (pulse_duration * 34300.0) / 2.0 / 100.0
        logger.debug("Pulse duration: %.6f s, distance: %.3f m", pulse_duration, distance_m)
        return distance_m

    def cleanup(self):
        if GPIO_AVAILABLE:
            GPIO.cleanup([self.trig, self.echo])
