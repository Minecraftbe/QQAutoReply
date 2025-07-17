from tkinter import Tk
from ui.controllers import *
from utils.logger_util import get_logger
from pubsub import pub

logger = get_logger(__name__)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.ui_locked: bool = False
        self.vars: dict[str, StringVar | Button] = {}
        self.controls: list[Button] = []
        self.resizable(False, False)
        self.state: bool = False

        self._subscribe_events()

    # -----一种预设, 已自动开启-----
    def _init_layout(self):
        self.geometry("450x200+10+10")
        setup_controllers(self)

    # -----监听消息-----

    @staticmethod
    def _subscribe_events():
        pub.subscribe(update_state, "update_state")
        pub.subscribe(update_chat_box_pos, "update_chat_box_pos")
        pub.subscribe(update_message_pos, "update_message_pos")
        pub.subscribe(update_hint, "update_ui.hint")

    # -----不要忘记调用run()!!!!!!-----
    def run(self):
        self._init_layout()
        self._subscribe_events()
        self.mainloop()


if __name__ == '__main__':
    import core.picker

    logger.info("hello world")
    root = Window()
    root.run()
