import math
from time import time, sleep as sl

from pubsub import pub
from utils.event_util import TOPIC_PAUSE, TOPIC_START, TOPIC_TOGGLE_RUNNING
from cores.ocr import OpticalCharacterRecognition
from cores.core import Core
from cores.opencv import ImageProcessor, ScreenCapturer
from utils.interfaces import IWithLogger
from utils.thread_util import ControllableThread


class CoreThread(ControllableThread, IWithLogger):
    def __init__(self, tps: int = 10):
        super().__init__(name="CoreThread")
        IWithLogger.__init__(self)

        self.core = Core()
        self._tick_duration: float = 1 / tps

        pub.subscribe(self.pause, TOPIC_PAUSE)
        pub.subscribe(self.resume, TOPIC_START)

    def run(self):
        warning: bool = False
        while not self._stop_event.is_set():
            self._running_event.wait()
            start = time()
            self.core.run()

            remaining = self._tick_duration + start - time()
            if remaining > 0:
                sl(remaining)
                # test
                # print(remaining)
            else:
                if not warning:
                    self.logger.warning(f"tps太高, 电脑无法胜任, 建议将tps设置低于 {math.floor(1 / -remaining)}")
                    warning = True

    def get_core(self):
        return self.core

    def resume(self):
        if self.core.opencv.scr.is_initialized:
            super().resume()
        else:
            from tkinter.messagebox import showwarning
            showwarning("未完成坐标选择", "未选择坐标，无法启动！")
            pub.sendMessage(TOPIC_PAUSE)
            pub.sendMessage(TOPIC_TOGGLE_RUNNING)
            self.logger.warning("未选择坐标，已回滚此次启动！")

