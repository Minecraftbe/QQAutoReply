from mss.screenshot import ScreenShot
from pubsub import pub
from mss import mss
import numpy as np
from constants import *
import cv2
from utils.interfaces import IRunnable, IWithLogger
from utils.log_util import get_logger


class ImageProcessor(IRunnable, IWithLogger):
    def __init__(self):
        super().__init__()


    def run(self):
        pass


class ScreenCapturer(IRunnable):
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.width: int = 0
        self.height: int = 0
        self._is_initialized: bool = False
        self.this_image = None
        self.last_image = None
        pub.subscribe(self.set_coordinates, TOPIC_SET_MESSAGE_POS)

    def set_coordinates(self, pos: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.width = pos[2] - self.x
        self.height = pos[3] - self.y
        self._is_initialized = True

    def run(self):
        if not self._is_initialized:
            raise RuntimeError("未初始化")
        self.last_image = self.this_image
        with mss() as sct:
            monitor = {
                "left": self.x,
                "top": self.y,
                "width": self.width,
                "height": self.height
            }
            self.this_image = cv2.cvtColor(np.array(sct.grab(monitor)), cv2.COLOR_BGR2GRAY)

    def get_images(self):
        if not self._is_initialized:
            raise RuntimeError("未初始化")
        return self.this_image, self.last_image
