from abc import ABC, abstractmethod
from collections.abc import Callable
import math
from threading import Event, Thread
from time import sleep, time
from typing import Any
from utils import (
    TOPIC_PAUSE,
    TOPIC_SET_MESSAGE_AREA,
    TOPIC_START,
    TOPIC_TOGGLE_RUNNING_STATE,
    get_logger,
)
from cv2.typing import MatLike
from mss import mss
from pubsub import pub
from skimage.metrics import structural_similarity as ssim  # type: ignore

import cv2
import numpy as np


class ControllableThread(Thread, ABC):
    def __init__(
        self, name: str | None = None, target: Callable[..., Any] | None = None
    ):
        super().__init__(name=name, target=target, daemon=True)
        self._running_event = Event()
        self._stop_event = Event()

    # TODO: 优化逻辑，给一个默认检查然后直接调用super().run()，在函数开头就检查，派生类只需要注重于while检查后内容
    @abstractmethod
    def run(self):
        """
        派生类必须实现此方法, 变量都摆好了只需要用while+wait对两个实例特性进行检测
        代码演示::
            while not self._stop_event.is_set():
                self._running_event.wait()
                self.the_instance.run()
        """
        pass

    def pause(self):
        self._running_event.clear()

    def resume(self):
        self._running_event.set()

    def stop(self):
        self._running_event.set()
        self._stop_event.set()

    def is_running(self):
        return self._running_event.is_set()


class CoreThread(ControllableThread):
    def __init__(self, tps: int = 10):
        super().__init__(name="CoreThread")
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.core = Core()
        self._tick_duration: float = 1 / tps

        pub.subscribe(self.pause, TOPIC_PAUSE)
        pub.subscribe(self.resume, TOPIC_START)

    # TODO: 优化逻辑
    def run(self):
        warned: bool = False
        while not self._stop_event.is_set():
            self._running_event.wait()
            start = time()
            self.core.run()

            remaining = self._tick_duration + start - time()
            if remaining > 0:
                sleep(remaining)
                # test
                # print(remaining)
            else:
                if not warned:
                    self.logger.warning(
                        f"tps太高, 电脑无法胜任, 建议将tps设置低于 {math.floor(1 / -remaining)}"
                    )
                    warned = True

    def get_core(self):
        return self.core

    def resume(self):
        if self.core.image_processor.is_initialized:
            super().resume()
        else:
            from tkinter.messagebox import showwarning

            showwarning("未完成坐标选择", "未选择坐标，无法启动！")
            pub.sendMessage(TOPIC_PAUSE)
            pub.sendMessage(TOPIC_TOGGLE_RUNNING_STATE)
            self.logger.warning("未选择坐标，已回滚此次启动！")


class Core:
    def __init__(self):
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

        self.state: bool = False
        # self.modules: dict[str, IRunnable] = {}
        self.image_processor = ImageProcessor()
        # TODO: 做一个ocr调用
        self.logger.info("Core 已初始化")

    def run(self):
        self.image_processor.tick()


if __name__ == "__main__":
    core = Core()
    print(core.__class__.__name__)
    core.logger.info("hi")


class ImageProcessor:
    def __init__(self):
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.is_changed: bool = False
        self._is_initialized = False
        self.monitor = {"left": -1, "top": -1, "width": -1, "height": -1}
        self.is_initialized: bool = False
        self.this_image: None | MatLike = None
        self.last_image: None | MatLike = None
        pub.subscribe(self.set_monitor, TOPIC_SET_MESSAGE_AREA)

    # TODO: 完善聊天截图变化检测逻辑
    def tick(self):
        self.is_changed = False
        if not self._is_initialized:
            self.make_screenshot()
        self.make_screenshot()

        if self.is_screenshot_changed():
            self.is_changed = True
            print("aaa")

    def set_monitor(self, pos: tuple[int, int, int, int]):
        self.monitor["left"] = pos[0]
        self.monitor["top"] = pos[1]
        self.monitor["width"] = pos[2] - pos[0]
        self.monitor["height"] = pos[3] - pos[1]
        self.is_initialized = True

    def make_screenshot(self) -> MatLike:
        self.last_image = self.this_image
        with mss() as sct:
            self.this_image = cv2.cvtColor(
                np.array(sct.grab(self.monitor)), cv2.COLOR_BGR2GRAY
            )
        return self.this_image

    def get_newer_screenshot(self) -> MatLike | None:
        if not self.is_initialized:
            raise RuntimeError("未初始化")

        self.make_screenshot()
        if self.is_screenshot_changed():
            return self.this_image
        return None

    def is_screenshot_changed(self) -> bool:
        if self.this_image is None:
            raise RuntimeError("当前截图为空")

        if self.last_image is None:
            return True
        if self.this_image.shape == self.last_image.shape and np.array_equal(
            self.this_image, self.last_image
        ):
            return False

        similarity: float = ssim(self.this_image, self.last_image)  # type: ignore
        return similarity < 0.95


# TODO: 完善自动回复
class AutoReply:
    def __init__(self, chatbox_pos: tuple[int, int, int, int]):
        self.chatbox = chatbox_pos
