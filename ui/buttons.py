from tkinter import Frame, Button
from .events import *


def setup_buttons(_window: "Window"):
    setup_events(_window)
    frame_buttons = Frame(_window, padx=10, pady=10)
    frame_buttons.pack(side="bottom", fill="x")

    b_load_messages = Button(frame_buttons, text="📥 载入聊天消息", width=10,
                             command=load_message)
    b_start = Button(frame_buttons, text="▶ 开始/暂停", width=10,
                     command=on_toggle_running)
    b_set_pos = Button(frame_buttons, text="📍 选取坐标", width=10,
                       command=set_coordinates)
    b_new_message = Button(frame_buttons, text="📃 创建新对话文件", width=10,
                           command=new_message)
    _window.vars["b_start"] = b_start

    for btn in (b_load_messages, b_start, b_set_pos, b_new_message):
        _window.controls.append(btn)
        btn.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        btn.config(relief="groove")
