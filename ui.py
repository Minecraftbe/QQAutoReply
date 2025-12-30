from __future__ import annotations
from tkinter import Frame, LabelFrame, Tk, Button, StringVar, Label, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import Any, Literal
from pubsub import pub

from utils import (
    CWD,
    TOPIC_LOAD_MESSAGE,
    TOPIC_NEW_MESSAGE,
    TOPIC_PAUSE,
    TOPIC_SET_CHAT_BOX_POS,
    TOPIC_SET_MESSAGE_AREA,
    TOPIC_SET_POSITIONS,
    TOPIC_START,
    TOPIC_TOGGLE_RUNNING_STATE,
    TOPIC_UI_SIMPLE_MSGBOX,
    TOPIC_UI_UPDATE_HINT,
    TOPIC_UPDATE_RUNNING_STATE,
    subscribe,
    get_logger,
)

logger = get_logger(__name__)
window: Window


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.b_start_buffer: Button | None = None
        self.ui_locked: bool = False
        self.string_vars: dict[str, "StringVar"] = {}
        self.labels: dict[str, "Label"] = {}
        self.buttons: list["Button"] = []
        self.resizable(False, False)
        self.state: bool = False

        # 设置窗口样式
        self.title("聊天助手")
        self.configure(bg="#ecf0f1")
        self.option_add("*Font", "微软雅黑 9")  # type: ignore # 减小全局字体大小

        global window
        window = self

        self.geometry("500x280")  # 减小窗口尺寸
        self.update_idletasks()  # 确保窗口尺寸计算准确

        setup_buttons()
        setup_labels()

        self.mainloop()


def setup_labels():
    frame_labels = LabelFrame(
        window,
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
    state = StringVar(value="运行状态: 停止")
    chat_box_pos = StringVar(value="输入框位置: 未设置")
    message_pos = StringVar(value="消息区域: 未设置")
    hint = StringVar(value="提示: 点击'选取坐标'设置位置")

    # 注册变量
    window.string_vars["hint"] = hint
    window.string_vars["state"] = state
    window.string_vars["chat_box_pos"] = chat_box_pos
    window.string_vars["message_pos"] = message_pos

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
    window.labels["status_indicator"] = status_indicator
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

    logger.info("Labels initialized successfully.")


def setup_buttons():
    frame_buttons = Frame(window, padx=10, pady=5, bg="#f5f7fa")
    frame_buttons.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    # 优化按钮样式 - 更合适的字体大小和间距
    button_config: dict[str, Any] = {
        "font": ("微软雅黑", 9, "bold"),  # 减小字体大小
        "fg": "#ffffff",
        "borderwidth": 0,
        "highlightthickness": 0,
        "padx": 6,  # 减小水平内边距
        "pady": 4,  # 减小垂直内边距
        "cursor": "hand2",
    }

    # 按钮颜色方案
    b_load_messages = Button(
        frame_buttons,
        text="📥 载入消息",  # 缩短文本
        command=load_message,
        bg="#3498db",
        activebackground="#2980b9",
        **button_config,
    )

    b_start = Button(
        frame_buttons,
        text="▶ 开始/暂停",
        command=on_toggle_running_state,
        bg="#2ecc71",
        activebackground="#27ae60",
        **button_config,
    )
    window.b_start_buffer = b_start

    b_set_pos = Button(
        frame_buttons,
        text="📍 选取坐标",
        command=set_coordinates,
        bg="#9b59b6",
        activebackground="#8e44ad",
        **button_config,
    )

    b_new_message = Button(
        frame_buttons,
        text="📃 新建对话",  # 缩短文本
        command=new_message,
        bg="#e67e22",
        activebackground="#d35400",
        **button_config,
    )

    # 使用网格布局
    b_load_messages.grid(row=0, column=0, padx=5, pady=4, sticky="ew")  # 减小间距
    b_start.grid(row=0, column=1, padx=5, pady=4, sticky="ew")
    b_set_pos.grid(row=0, column=2, padx=5, pady=4, sticky="ew")
    b_new_message.grid(row=0, column=3, padx=5, pady=4, sticky="ew")

    # 平均分配列宽
    for i in range(4):
        frame_buttons.columnconfigure(i, weight=1)

    for btn in (b_load_messages, b_start, b_set_pos, b_new_message):
        window.buttons.append(btn)
    logger.info("Buttons initialized successfully.")


def load_message():
    file_: str = askopenfilename(
        initialdir=CWD / "messages",
        filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")),
    )
    if file_ != "":
        pub.sendMessage(TOPIC_LOAD_MESSAGE, file=file_)
        logger.info(f"对话文件已选取，文件为: {file_}")
    else:
        logger.warning("本次选取被取消！")


@subscribe(TOPIC_TOGGLE_RUNNING_STATE)
def on_toggle_running_state():
    temp = window.state
    window.state = not window.state
    update_state(window.state)
    if temp:
        toggle_ui_lock_state(False)
        pub.sendMessage(TOPIC_PAUSE)
    else:
        if window.b_start_buffer is None:
            raise Exception("Button b_start is not initialized")
        toggle_ui_lock_state(True, window.b_start_buffer)
        pub.sendMessage(TOPIC_START)


def set_coordinates():
    toggle_ui_lock_state(True)
    pub.sendMessage(TOPIC_SET_POSITIONS)


def new_message():
    new_file: str = asksaveasfilename(
        initialdir=CWD / "messages",
        filetypes=(("对话文件", "*.json"), ("所有文件", "*.*")),
    )
    if new_file != "":
        pub.sendMessage(TOPIC_NEW_MESSAGE, file=new_file)
        logger.info(f"新的对话文件已创建，文件为: {new_file}")
    else:
        logger.warning("本次选取被取消！")


# -----更新显示内容或状态-----
@subscribe(TOPIC_UPDATE_RUNNING_STATE)
def update_state(state: bool):
    window.state = state
    if state:
        window.string_vars["state"].set("运行状态: 运行中...")
        window.labels["status_indicator"].config(fg="#2ecc71")
    else:
        window.string_vars["state"].set("运行状态: 停止")
        window.labels["status_indicator"].config(fg="#e74c3c")


@subscribe(TOPIC_SET_CHAT_BOX_POS)
def update_chat_box_pos(pos: tuple[int, int]):
    window.string_vars["chat_box_pos"].set(f"输入框位置: {pos}")


@subscribe(TOPIC_SET_MESSAGE_AREA)
def update_message_pos(pos: tuple[int, int]):
    window.string_vars["message_pos"].set(value=f"消息区域: {pos}")
    toggle_ui_lock_state(False)


@subscribe(TOPIC_UI_UPDATE_HINT)
def update_hint(text: str):
    window.string_vars["hint"].set(f"提示: {text}")


available_msgbox_mapping = {
    messagebox.INFO: messagebox.showinfo,
    messagebox.WARNING: messagebox.showwarning,
}


@subscribe(TOPIC_UI_SIMPLE_MSGBOX)
def show_simple_messagebox(
    icon: Literal["info", "warning"],
    title: str | None = None,
    message: str | None = None,
):
    available_msgbox_mapping[icon](title, message)


# -----更新按钮状态(锁定或正常)-----
def toggle_ui_lock_state(locked: bool, *target: Button) -> None:
    """更新按钮状态(锁定或正常)

    Args:
        locked (bool): 是否锁定按钮, True为锁定, False为正常
        target (Button | list[Button] | None, optional): _description_. Defaults to None.
    """
    window.ui_locked = locked

    for ctrl in window.buttons:
        ctrl.config(
            state="normal" if ctrl in target else ("disabled" if locked else "normal")
        )


if __name__ == "__main__":
    ui = Window()
    logger.info("启动聊天助手")
