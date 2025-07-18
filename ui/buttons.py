from tkinter import Frame, Button

from .events import *


def setup_buttons(_window: "Window"):
    setup_events(_window)

    frame_buttons = Frame(_window, padx=10, pady=10)  # 淡灰背景更现代
    frame_buttons.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    # 按钮统一样式
    button_config = {
        "fg": "#333333",
        "activebackground": "#cce6ff",
        "activeforeground": "#000000",
        "relief": "groove",
        "bd": 2
    }

    b_load_messages = Button(frame_buttons, text="📥 载入聊天消息", command=load_message, **button_config)
    b_start = Button(frame_buttons, text="▶ 开始/暂停", command=on_toggle_running, **button_config)
    b_set_pos = Button(frame_buttons, text="📍 选取坐标", command=set_coordinates, **button_config)
    b_new_message = Button(frame_buttons, text="📃 新建对话文件", command=new_message, **button_config)

    _window.vars["b_start"] = b_start

    for btn in (b_load_messages, b_start, b_set_pos, b_new_message):
        _window.controls.append(btn)
        btn.pack(side="left", expand=True, fill="x", padx=8, pady=6)
