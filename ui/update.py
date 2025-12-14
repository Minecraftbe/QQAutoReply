from tkinter import Button
from typing import TYPE_CHECKING

from utils.event_util import (
    TOPIC_SET_CHAT_BOX_POS,
    TOPIC_SET_MESSAGE_AREA,
    TOPIC_UPDATE_HINT,
    TOPIC_UPDATE_RUNNING_STATE,
    subscribe,
)

if TYPE_CHECKING:
    from window import Window
window: "Window"


def setup_updates(_window: "Window"):
    global window
    window = _window


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
    window.string_vars["message_pos"].set(f"消息区域: {pos}")
    toggle_ui_lock_state(False)


@subscribe(TOPIC_UPDATE_HINT)
def update_hint(text: str):
    window.string_vars["hint"].set(f"提示: {text}")


# -----更新按钮状态(锁定或正常)-----
def toggle_ui_lock_state(
    locked: bool, target: Button | list[Button] | None = None
) -> None:
    """更新按钮状态(锁定或正常)

    Args:
        locked (bool): 是否锁定按钮, True为锁定, False为正常
        target (Button | list[Button] | None, optional): _description_. Defaults to None.
    """
    window.ui_locked = locked
    if target is None:
        target = []
    elif isinstance(target, list):
        target = target
    else:
        target = [target]

    for ctrl in window.buttons:
        ctrl.config(
            state="normal" if ctrl in target else ("disabled" if locked else "normal")
        )
