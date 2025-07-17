from tkinter import Tk
from utils.log_util import get_logger
from ui.controllers import setup_controllers, subscribe_events
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from tkinter import Button, StringVar

logger = get_logger(__name__)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.ui_locked: bool = False
        self.vars: dict[str, Union["StringVar", "Button"]] = {}
        self.controls: list["Button"] = []
        self.resizable(False, False)
        self.state: bool = False

    # -----一种预设, 已自动开启-----
    def _init_layout(self):
        self.geometry("500x200+10+10")
        setup_controllers(self)

    # -----不要忘记调用run()!!!!!!-----
    def run(self):
        self._init_layout()
        subscribe_events()
        self.mainloop()


def init():
    ui = Window()
    ui.run()
    return ui


if __name__ == '__main__':
    # from ui.controllers import *

    logger.info("hello world")
    init()
