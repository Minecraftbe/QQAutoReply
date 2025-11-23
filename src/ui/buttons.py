from tkinter import Frame, Button
from .events import *

def setup_buttons(_window: "Window"):
    setup_events(_window)

    frame_buttons = Frame(_window, padx=10, pady=5, bg="#f5f7fa")
    frame_buttons.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    # 优化按钮样式 - 更合适的字体大小和间距
    button_config = {
        "font": ("微软雅黑", 9, "bold"),  # 减小字体大小
        "fg": "#ffffff",
        "borderwidth": 0,
        "highlightthickness": 0,
        "padx": 6,  # 减小水平内边距
        "pady": 4,  # 减小垂直内边距
        "cursor": "hand2"
    }

    # 按钮颜色方案
    b_load_messages = Button(frame_buttons, text="📥 载入消息",  # 缩短文本
                             command=load_message,
                             bg="#3498db", activebackground="#2980b9",
                             **button_config)

    b_start = Button(frame_buttons, text="▶ 开始/暂停",
                     command=on_toggle_running,
                     bg="#2ecc71", activebackground="#27ae60",
                     **button_config)

    b_set_pos = Button(frame_buttons, text="📍 选取坐标",
                       command=set_coordinates,
                       bg="#9b59b6", activebackground="#8e44ad",
                       **button_config)

    b_new_message = Button(frame_buttons, text="📃 新建对话",  # 缩短文本
                           command=new_message,
                           bg="#e67e22", activebackground="#d35400",
                           **button_config)

    _window.vars["b_start"] = b_start

    # 使用网格布局
    b_load_messages.grid(row=0, column=0, padx=5, pady=4, sticky="ew")  # 减小间距
    b_start.grid(row=0, column=1, padx=5, pady=4, sticky="ew")
    b_set_pos.grid(row=0, column=2, padx=5, pady=4, sticky="ew")
    b_new_message.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

    # 平均分配列宽
    for i in range(4):
        frame_buttons.columnconfigure(i, weight=1)

    for btn in (b_load_messages, b_start, b_set_pos, b_new_message):
        _window.controls.append(btn)