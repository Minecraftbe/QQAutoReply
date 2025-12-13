from tkinter import StringVar, Frame, Label, LabelFrame
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from window import Window


def setup_labels(_window: "Window"):
    frame_labels = LabelFrame(
        _window,
        text="状态面板",
        padx=10,
        pady=8,
        font=("微软雅黑", 10, "bold"),
        labelanchor="n",
        bg="#f5f7fa",
        fg="#34495e",
        relief="flat",
    )
    frame_labels.pack(side="top", fill="x", padx=10, pady=8)

    # 创建 StringVar 状态变量
    state = StringVar(value="运行状态: 暂停")
    chat_box_pos = StringVar(value="输入框位置: 未设置")
    message_pos = StringVar(value="消息位置: 未设置")
    hint = StringVar(value="提示: 点击'选取坐标'设置位置")

    # 注册变量
    _window.string_vars["hint"] = hint
    _window.string_vars["state"] = state
    _window.string_vars["chat_box_pos"] = chat_box_pos
    _window.string_vars["message_pos"] = message_pos

    # 优化标签样式
    label_config: dict[str, Any] = {
        "anchor": "w",
        "font": ("微软雅黑", 9),
        "padx": 8,
        "pady": 2,
        "bg": "#f5f7fa",
        "fg": "#2c3e50",
    }

    # 创建状态行框架 - 将状态文本和指示器放在同一行
    frame_state = Frame(frame_labels, bg="#f5f7fa")
    frame_state.pack(fill="x", pady=2)

    # 状态文本标签
    l_state = Label(frame_state, textvariable=state, **label_config)
    l_state.pack(side="left", fill="x", expand=True)

    # 状态指示器 - 现在与状态文本在同一行
    status_indicator = Label(
        frame_state, text="🔴", fg="#e74c3c", bg="#f5f7fa", font=("Arial", 12), padx=8
    )
    _window.labels["status_indicator"] = status_indicator
    status_indicator.pack(side="right", anchor="e")

    # 其他标签组件
    l_chat_box_pos = Label(frame_labels, textvariable=chat_box_pos, **label_config)
    l_messages_pos = Label(frame_labels, textvariable=message_pos, **label_config)
    l_hint = Label(frame_labels, textvariable=hint, **label_config)

    # 优化警告样式
    l_warn = Label(
        frame_labels,
        text="⚠️ 警告：不要遮挡聊天窗口！",
        relief="flat",
        anchor="center",
        padx=6,
        pady=4,
        fg="#ffffff",
        bg="#e74c3c",
        font=("微软雅黑", 9, "bold"),
        borderwidth=0,
    )

    # 按顺序排列
    for widget in (l_chat_box_pos, l_messages_pos, l_hint, l_warn):
        widget.pack(fill="x", pady=2)
