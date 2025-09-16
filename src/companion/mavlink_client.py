"""
mavlink_client.py
Provides a MAVSDK wrapper to connect and send basic commands to Pixhawk.
"""

import asyncio
import logging
from mavsdk import System
from mavsdk.offboard import VelocityNedYaw, OffboardError
from mavsdk.action import ActionError
from typing import Optional

logger = logging.getLogger(__name__)


class MAVClient:
    def __init__(self, serial_url: str):
        self._serial_url = serial_url
        self._drone = System()
        self._connected = False

    async def connect(self):
        logger.info(f"Connecting to vehicle via {self._serial_url}")
        await self._drone.connect(system_address=self._serial_url)

        # Wait for connection
        async for state in self._drone.core.connection_state():
            if state.is_connected:
                logger.info(f"Connected to system with UUID: {state.uuid}")
                self._connected = True
                break

    async def arm(self):
        try:
            await self._drone.action.arm()
            logger.info("Armed vehicle")
        except ActionError as e:
            logger.exception("Failed to arm: %s", e)
            raise

    async def disarm(self):
        try:
            await self._drone.action.disarm()
            logger.info("Disarmed vehicle")
        except ActionError as e:
            logger.exception("Failed to disarm: %s", e)
            raise

    async def start_offboard_velocity(self, north: float, east: float, down: float, yaw_deg: float, duration: float):
        """
        Sends an offboard velocity setpoint for `duration` seconds.
        """
        logger.debug("Starting offboard velocity: N=%.2f E=%.2f D=%.2f Yaw=%.2f for %.2fs",
                     north, east, down, yaw_deg, duration)
        try:
            await self._drone.offboard.set_velocity_ned(VelocityNedYaw(north, east, down, yaw_deg))
            await self._drone.offboard.start()
            await asyncio.sleep(duration)
            await self._drone.offboard.stop()
            logger.debug("Offboard velocity command finished")
        except OffboardError as e:
            logger.exception("Offboard error: %s", e)
            # swallow or re-raise depending on design
        except Exception as e:
            logger.exception("Unexpected error in offboard: %s", e)

    def get_drone(self) -> System:
        return self._drone
