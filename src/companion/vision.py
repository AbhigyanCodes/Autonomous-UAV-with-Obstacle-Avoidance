"""
vision.py
Simple camera helper functions using OpenCV.
This module keeps things light; heavy inference is better run on Coral/EdgeTPU.
"""

import cv2
import logging
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


def open_camera(index: int = 0) -> Optional[cv2.VideoCapture]:
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        logger.warning("Camera index %s not opened", index)
        return None
    # set resolution if desired:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    return cap


def read_frame(cap: cv2.VideoCapture) -> Optional[Tuple[bool, any]]:
    if cap is None:
        return None
    ret, frame = cap.read()
    if not ret:
        logger.debug("Camera read returned empty frame")
        return None
    return (ret, frame)


def release_camera(cap: cv2.VideoCapture):
    if cap is not None:
        cap.release()
