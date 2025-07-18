from tkinter import Button
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from window import Window
window: "Window"


def setup_updates(_window):
    global window
    window = _window


# -----更新显示内容或状态-----

def update_state(state: bool):
    window.state = state
    if state:
        window.vars.get("state").set(f"运行状态: 运行中...")
        window.vars.get("status_indicator").config(fg="#2ecc71")
    else:
        window.vars.get("state").set(f"运行状态: 停止")
        window.vars.get("status_indicator").config(fg="#e74c3c")


def update_chat_box_pos(pos: tuple):
    window.vars.get("chat_box_pos").set(f"输入框位置: {pos}")


def update_message_pos(pos: tuple):
    window.vars.get("message_pos").set(f"消息位置: {pos}")
    toggle_ui_lock_state(False)


def update_hint(text: str):
    window.vars.get("hint").set(f"提示: {text}")


# -----更新按钮状态(锁定或正常)-----
def toggle_ui_lock_state(locked: bool, exception: Button | list[Button] | None = None):
    window.ui_locked = locked
    if exception is None:
        exceptions = []
    elif isinstance(exception, list):
        exceptions = exception
    else:
        exceptions = [exception]

    for ctrl in window.controls:
        ctrl.config(state="normal" if ctrl in exceptions else ("disabled" if locked else "normal"))
