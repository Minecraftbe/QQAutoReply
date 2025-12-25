from cv2.typing import MatLike
from mss import mss
from pubsub import pub
from skimage.metrics import structural_similarity as ssim  # type: ignore

import cv2
import numpy as np

from utils.event_util import TOPIC_SET_MESSAGE_AREA
from utils.interfaces import IRunnable, IWithLogger


class ImageProcessor(IRunnable, IWithLogger):
    def __init__(self):
        super().__init__()
        self.is_changed: bool = False
        self._is_initialized = False
        self.scr = ScreenCapturer()

    def run(self):
        self.is_changed = False
        if not self._is_initialized:
            self.scr.run()
        self.scr.run()

        if self.is_chat_changed(self.scr.get_images()):
            self.is_changed = True
            print("aaa")

    @staticmethod
    def is_chat_changed(images: tuple[MatLike | None, MatLike | None]) -> bool:
        this = images[0]
        last = images[1]

        if this == last:
            return True
        similarity, _ = ssim(this, last, full=True)  # type: ignore
        if similarity < 0.95:
            return True
        else:
            return False

    @staticmethod
    def split_image(image: MatLike):
        pass


class ScreenCapturer(IRunnable):
    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.width: int = 0
        self.height: int = 0
        self.is_initialized: bool = False
        self._this_image = None
        self._last_image = None
        pub.subscribe(self.set_coordinates, TOPIC_SET_MESSAGE_AREA)

    def set_coordinates(self, pos: tuple[int, int, int, int]):
        self.x = pos[0]
        self.y = pos[1]
        self.width = pos[2] - self.x
        self.height = pos[3] - self.y
        self.is_initialized = True

    def run(self):
        if not self.is_initialized:
            raise RuntimeError("未初始化")
        self._last_image = self._this_image
        with mss() as sct:
            monitor = {
                "left": self.x,
                "top": self.y,
                "width": self.width,
                "height": self.height,
            }
            self._this_image = cv2.cvtColor(
                np.array(sct.grab(monitor)), cv2.COLOR_BGR2GRAY
            )

    def get_images(self):
        if not self.is_initialized:
            raise RuntimeError("未初始化")
        return self._this_image, self._last_image
