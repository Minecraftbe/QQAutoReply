from abc import ABC, abstractmethod
from collections.abc import Callable
from threading import Event, Thread
from time import sleep, time
from typing import Any, Protocol, override
from utils import (
    TOPIC_PAUSE,
    TOPIC_SET_MESSAGE_AREA,
    TOPIC_START,
    TOPIC_TOGGLE_RUNNING_STATE,
    TOPIC_UI_SIMPLE_MSGBOX,
    get_logger,
)
from cv2.typing import MatLike
from mss import mss
from pubsub import pub

import math
import cv2
import numpy as np
from tool import process_image, text_recognition


class Tickable(Protocol):
    def tick(self) -> None: ...


class NeedInitialize(ABC):
    @abstractmethod
    def is_initialized(self) -> bool: ...


class ControllableThread(Thread, ABC):
    def __init__(
        self, name: str | None = None, target: Callable[..., Any] | None = None
    ):
        super().__init__(name=name, target=target, daemon=True)
        self._running_event = Event()
        self._stop_event = Event()

    @abstractmethod
    def tick(self):
        pass

    @override
    def run(self):
        while not self._stop_event.is_set():
            self._running_event.wait()
            self.tick()

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
    def __init__(self, core: Tickable, tps: int = 10):
        super().__init__(name="CoreThread")
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.core = core
        self._tick_duration: float = 1 / tps
        self.warned = False
        self.is_initialized = False

        pub.subscribe(self.pause, TOPIC_PAUSE)
        pub.subscribe(self.resume, TOPIC_START)

    @override
    def tick(self):
        start = time()
        self.core.tick()

        remaining = self._tick_duration + start - time()
        if remaining > 0:
            sleep(remaining)
            # test
            # print(remaining)
        else:
            if not self.warned:
                self.logger.warning(
                    f"tps太高, 电脑无法胜任, 建议将tps设置低于 {math.floor(1 / -remaining)}"
                )
                self.warned = True

    def get_core(self):
        return self.core

    @override
    def resume(self):
        if not self.is_initialized:
            if isinstance(self.core, NeedInitialize):
                self.is_initialized = self.core.is_initialized()
            else:
                self.is_initialized = True

        if self.is_initialized:
            super().resume()
        else:
            pub.sendMessage(
                TOPIC_UI_SIMPLE_MSGBOX,
                icon="warning",
                title="未完成坐标选择",
                message="未选择坐标，无法启动！",
            )
            pub.sendMessage(TOPIC_PAUSE)
            pub.sendMessage(TOPIC_TOGGLE_RUNNING_STATE)
            self.logger.warning("未选择坐标，已回滚此次启动！")


class Core(NeedInitialize):
    def __init__(self, *components: Tickable):
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )

        self.state: bool = False
        self.components = components
        self.need_initialize = tuple(
            c for c in components if isinstance(c, NeedInitialize)
        )

    def tick(self):
        for component in self.components:
            component.tick()

    @override
    def is_initialized(self):
        return all(c.is_initialized() for c in self.need_initialize)


# 优化合并代码带来的屎山
class ImageProcessor(NeedInitialize):
    def __init__(self):
        self.logger = get_logger(
            f"{self.__class__.__module__}.{self.__class__.__name__}"
        )
        self.is_changed: bool = False
        self.monitor = {"left": -1, "top": -1, "width": -1, "height": -1}
        self.initialized = False
        self.this_image: None | MatLike = None
        self.last_image: None | MatLike = None
        pub.subscribe(self.set_monitor, TOPIC_SET_MESSAGE_AREA)

    # TODO: 完善聊天截图变化检测逻辑
    def tick(self):
        self.is_changed = False
        if img := self.get_newer_screenshot():
            roi, img = process_image(img)
            ...

    def set_monitor(self, pos: tuple[int, int, int, int]):
        self.monitor["left"] = pos[0]
        self.monitor["top"] = pos[1]
        self.monitor["width"] = pos[2] - pos[0]
        self.monitor["height"] = pos[3] - pos[1]
        self.initialized = True

    def get_newer_screenshot(self) -> MatLike | None:
        if not self.initialized:
            raise RuntimeError("未初始化")

        self.last_image = self.this_image
        with mss() as sct:
            self.this_image = cv2.cvtColor(
                np.array(sct.grab(self.monitor)), cv2.COLOR_BGR2GRAY
            )

        if self.is_screenshot_changed():
            return self.this_image
        return None

    # TODO: 删掉scikit-image, 并改进该方法
    def is_screenshot_changed(self) -> bool:
        if self.this_image is None:
            raise RuntimeError("当前截图为空")

        if self.last_image is None:
            return True

        return not np.array_equal(self.this_image, self.last_image)

    @override
    def is_initialized(self) -> bool:
        return self.initialized


# TODO: 完善自动回复
class AutoReply:
    def __init__(self, chatbox_pos: tuple[int, int, int, int]):
        self.chatbox = chatbox_pos
