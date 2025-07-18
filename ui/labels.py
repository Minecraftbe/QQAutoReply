from tkinter import StringVar, Frame, Label, LabelFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window import Window


def setup_labels(_window: "Window"):
    frame_labels = LabelFrame(_window, text="状态面板🖥", padx=10, pady=10, font=("微软雅黑", 13, "bold"), labelanchor="n")
    frame_labels.pack(side="top", fill="x", padx=10, pady=10)

    # 创建 StringVar 状态变量
    state = StringVar(value="运行状态: False")
    chat_box_pos = StringVar(value="输入框位置: 未确定")
    message_pos = StringVar(value="消息位置: 未确定")
    hint = StringVar(value="提示: 当选取坐标时请看这里")

    # 注册变量
    _window.vars["hint"] = hint
    _window.vars["state"] = state
    _window.vars["chat_box_pos"] = chat_box_pos
    _window.vars["message_pos"] = message_pos

    # 样式统一参数
    label_config = {
        "relief": "flat",
        "anchor": "w",
        "font": ("Consolas", 11),
        "padx": 6,
    }

    # 创建标签组件
    l_state = Label(frame_labels, textvariable=state, **label_config)
    l_chat_box_pos = Label(frame_labels, textvariable=chat_box_pos, **label_config)
    l_messages_pos = Label(frame_labels, textvariable=message_pos, **label_config)
    l_hint = Label(frame_labels, textvariable=hint, **label_config)

    # 高亮警告
    l_warn = Label(
        frame_labels,
        text="⚠️ 警告：请不要遮挡聊天窗口！",
        relief="groove",
        anchor="center",
        padx=8,
        pady=4,
        fg="white",
        bg="#c0392b",
        font=("微软雅黑", 13, "bold")
    )

    # 按顺序排列
    for widget in (l_state, l_chat_box_pos, l_messages_pos, l_hint, l_warn):
        widget.pack(fill="x", pady=3)
