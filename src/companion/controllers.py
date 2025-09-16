"""
controllers.py
Contain high-level obstacle avoidance controllers that decide what velocity commands to send.
This is intentionally simple: when an obstacle is detected within threshold, step right.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


def simple_reactive_avoidance(distance_m: Optional[float], threshold: float):
    """
    Decide avoidance action based on a single forward-facing distance reading.
    Returns tuple (north, east, down, yaw_deg, duration)
    - north/east/down in m/s
    - yaw_deg in degrees
    - duration in seconds
    """
    if distance_m is None:
        logger.debug("Distance None: no action")
        return None

    if distance_m <= 0:
        logger.debug("Invalid distance: %s", distance_m)
        return None

    if distance_m < threshold:
        # simple action: strafe right at 1.0 m/s for 1.5s (tune for your aircraft)
        logger.info("Obstacle within threshold (%.2f m < %.2f m). Avoid to right.", distance_m, threshold)
        return (0.0, 1.0, 0.0, 0.0, 1.5)
    else:
        logger.debug("No avoidance needed (distance %.2f m)", distance_m)
        return None
