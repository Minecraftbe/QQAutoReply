from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import TYPE_CHECKING

from pubsub import pub

from utils.event_util import TOPIC_LOAD_MESSAGE, TOPIC_NEW_MESSAGE, TOPIC_PAUSE, TOPIC_SET_COORDINATES, TOPIC_START

from ui.update import toggle_ui_lock_state, update_state
from utils.log_util import get_logger
from utils.path_util import get_project_dir

if TYPE_CHECKING:
    from window import Window
logger = get_logger(__name__)
window: "Window"


def setup_events(_window: "Window"):
    global window
    window = _window


# -----按钮对应指令-----


def load_message():
    file_: str = askopenfilename(
        initialdir=get_project_dir() + "\\messages",
        filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")),
    )
    if file_ != "":
        pub.sendMessage(TOPIC_LOAD_MESSAGE, file=file_)
        logger.info(f"对话文件已选取，文件为: {file_}")
    else:
        logger.warning("本次选取被取消！")


def on_toggle_running():
    if window.state:
        __reverse_and_update_state()
        toggle_ui_lock_state(False)
        pub.sendMessage(TOPIC_PAUSE)
    else:
        __reverse_and_update_state()
        if window.b_start_buffer is None:
            raise Exception("Button b_start is not initialized")
        toggle_ui_lock_state(True, window.b_start_buffer)
        pub.sendMessage(TOPIC_START)


def set_coordinates():
    toggle_ui_lock_state(True)
    pub.sendMessage(TOPIC_SET_COORDINATES)


def new_message():
    new_file: str = asksaveasfilename(
        initialdir=get_project_dir() + "\\messages",
        filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")),
    )
    if new_file != "":
        pub.sendMessage(TOPIC_NEW_MESSAGE, file=new_file)
        logger.info(f"新的对话文件已创建，文件为: {new_file}")
    else:
        logger.warning("本次选取被取消！")


# -----工具函数-----
def __reverse_and_update_state():
    window.state = not window.state
    update_state(window.state)
