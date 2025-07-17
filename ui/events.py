from tkinter.filedialog import askopenfilename, asksaveasfilename
from pubsub import pub
from ui.update import toggle_ui_lock_state, update_state
from utils.log_util import get_logger
from utils.path_util import get_project_dir
from typing import TYPE_CHECKING
from constants import *

if TYPE_CHECKING:
    from window import Window
logger = get_logger(__name__)
window: "Window"


def setup_events(_window: "Window"):
    global window
    window = _window


# -----按钮对应指令-----

def load_message():
    file: str = askopenfilename(initialdir=get_project_dir() + "\\messages",
                                filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")))
    if file != "":
        pub.sendMessage(TOPIC_LOAD_MESSAGE, file=file)
        logger.info(f"对话文件已选取，文件为: {file}")
    else:
        logger.warning("本次选取被取消！")


def on_toggle_running():
    if window.state:
        pub.sendMessage(TOPIC_PAUSE)
        toggle_ui_lock_state(False)
    else:
        pub.sendMessage(TOPIC_START)
        toggle_ui_lock_state(True, window.vars.get("b_start"))

    window.state = not window.state
    update_state(window.state)


def set_coordinates():
    toggle_ui_lock_state(True)
    pub.sendMessage(TOPIC_SET_COORDINATES)


def new_message():
    new_file: str = asksaveasfilename(initialdir=get_project_dir() + "\\messages",
                                      filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")))
    if new_file != "":
        pub.sendMessage(TOPIC_NEW_MESSAGE, file=new_file)
        logger.info(f"新的对话文件已创建，文件为: {new_file}")
    else:
        logger.warning("本次选取被取消！")
