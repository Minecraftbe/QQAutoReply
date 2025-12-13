from tkinter import Tk
from typing import TYPE_CHECKING, Union

from ui.controllers import setup_controllers, subscribe_events
from utils.interfaces import IRunnable
from utils.log_util import get_logger

if TYPE_CHECKING:
    from tkinter import Button, StringVar, Label

logger = get_logger(__name__)


class Window(Tk, IRunnable):
    b_start_buffer: Union["Button", None] = None
    def __init__(self):
        super().__init__()
        self.ui_locked: bool = False
        self.string_vars: dict[str, "StringVar"] = {}
        self.labels: dict[str, "Label"] = {}
        self.buttons: list["Button"] = []
        self.resizable(False, False)
        self.state: bool = False

        # 设置窗口样式
        self.title("聊天助手")
        self.configure(bg="#ecf0f1")
        self.option_add("*Font", "微软雅黑 9")  # type: ignore # 减小全局字体大小

    # 初始化布局
    def _init_layout(self):
        self.geometry("500x280")  # 减小窗口尺寸
        self.update_idletasks()  # 确保窗口尺寸计算准确
        setup_controllers(self)

    def run(self):
        self._init_layout()
        subscribe_events()
        self.mainloop()


def init():
    ui = Window()
    ui.run()
    return ui


if __name__ == "__main__":
    logger.info("启动聊天助手")
    init()
