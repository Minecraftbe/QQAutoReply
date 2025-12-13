from abc import ABC, abstractmethod
from collections.abc import Callable
from threading import Thread, Event
from typing import Any


class ControllableThread(Thread, ABC):
    def __init__(self, name: str | None = None, target: Callable[..., Any] | None = None):
        super().__init__(name=name, target=target, daemon=True)
        self._running_event = Event()
        self._stop_event = Event()

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
