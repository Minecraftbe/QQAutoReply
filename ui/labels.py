from tkinter import StringVar, Frame, Label
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window import Window


def setup_labels(_window: "Window"):
    frame_labels = Frame(_window, padx=10, pady=10)
    frame_labels.pack(side="top", fill="x")

    state = StringVar()
    state.set("运行状态: False")
    chat_box_pos = StringVar()
    chat_box_pos.set("输入框位置: 未确定")
    message_pos = StringVar()
    message_pos.set("消息位置: 未确定")
    hint = StringVar()
    hint.set("提示: 当选取坐标时请看这里")
    _window.vars["hint"] = hint
    _window.vars["state"] = state
    _window.vars["chat_box_pos"] = chat_box_pos
    _window.vars["message_pos"] = message_pos

    l_state = Label(frame_labels, textvariable=state, relief="flat", anchor="w", padx=5)
    l_chat_box_pos = Label(frame_labels, textvariable=chat_box_pos, relief="flat", anchor="w", padx=5)
    l_messages_pos = Label(frame_labels, textvariable=message_pos, relief="flat", anchor="w", padx=5)
    l_hint = Label(frame_labels, textvariable=hint, relief="flat", anchor="w", padx=5)

    l_state.pack(fill="x", pady=3)
    l_chat_box_pos.pack(fill="x", pady=3)
    l_messages_pos.pack(fill="x", pady=3)
    l_hint.pack(fill="x", pady=3)
