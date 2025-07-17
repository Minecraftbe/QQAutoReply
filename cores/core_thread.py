from threading import Thread, Event
from pubsub import pub
from constants import *
from cores.core import Core
from time import sleep as sl


class CoreThread(Thread):
    def __init__(self, tps: int = 10):
        super().__init__(name="CoreThread", daemon=True)

        self.core = Core()
        self._tick_duration: float = 1 / tps
        self._running_event = Event()
        self._stop_event = Event()

        pub.subscribe(self.pause, TOPIC_PAUSE)
        pub.subscribe(self.resume, TOPIC_START)

    def run(self):
        while not self._stop_event.is_set():
            self._running_event.wait()
            self.core.run()
            sl(self._tick_duration)

    def pause(self):
        self._running_event.clear()

    def resume(self):
        self._running_event.set()

    def stop(self):
        self._running_event.set()
        self._stop_event.set()

    def get_core(self):
        return self.core

    def is_running(self):
        return self._running_event.is_set()
