from tkinter import Frame, Button
from tkinter.filedialog import askopenfilename

from pubsub import pub
from ui.window import Window, logger
from ui.update import update_ui_lock_state, update_state
from utils.utils import get_project_dir

window: Window


def setup_buttons(_window: Window):
    global window
    window = _window
    frame_buttons = Frame(_window, padx=10, pady=10)
    frame_buttons.pack(side="bottom", fill="x")
    b_load_messages = Button(frame_buttons, text="📥 载入聊天消息", width=10,
                             command=load_message)
    b_start = Button(frame_buttons, text="▶️ 开始/暂停", width=10,
                     command=start_or_pause)
    b_set_pos = Button(frame_buttons, text="📍 选取坐标", width=10,
                       command=set_coordinates)
    _window.vars["b_start"] = b_start

    for btn in (b_load_messages, b_start, b_set_pos):
        _window.controls.append(btn)
        btn.pack(side="left", expand=True, fill="x", padx=5, pady=5)


# -----按钮对应指令-----

def load_message():
    file: str = askopenfilename(initialdir=get_project_dir() + "\\messages",
                                filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")))
    pub.sendMessage("load_message", file=file)
    logger.debug(file)


def start_or_pause():
    if window.state:
        pub.sendMessage("pause")
        update_ui_lock_state(False)
        # test
        window.state = False
        update_state(window.state)
    else:
        pub.sendMessage("start")
        update_ui_lock_state(True, window.vars.get("b_start"))
        # test
        window.state = True
        update_state(window.state)


def set_coordinates():
    update_ui_lock_state(True)
    pub.sendMessage("set_coordinates")
