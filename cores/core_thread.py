import math
from threading import Event
from time import time, sleep as sl

from pubsub import pub

from constants import *
from cores.core import Core
from utils.controllable_thread import ControllableThread
from utils.interfaces import IWithLogger


class CoreThread(ControllableThread, IWithLogger):
    def __init__(self, tps: int = 10):
        super().__init__(name="CoreThread")
        IWithLogger.__init__(self)

        self.core = Core()
        self._tick_duration: float = 1 / tps
        self._running_event = Event()
        self._stop_event = Event()

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
                print(remaining)
            else:
                if not warning:
                    self.logger.warning(f"tps太高，电脑无法胜任，建议将tps设置低于 {math.floor(1 / -remaining)}")
                    warning = True

    def get_core(self):
        return self.core
