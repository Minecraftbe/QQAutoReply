from tkinter import Button
from ui.window import Window

window: Window


def setup_updates(_window: Window):
    global window
    window = _window


# -----更新显示内容或状态-----

def update_state(state: bool):
    window.state = state
    window.vars.get("state").set(f"运行状态: {window.state}")


def update_chat_box_pos(pos: tuple):
    window.vars.get("chat_box_pos").set(f"输入框位置: {pos}")


def update_message_pos(pos: tuple):
    window.vars.get("message_pos").set(f"消息位置: {pos}")
    update_ui_lock_state(False)


def update_hint(text: str):
    window.vars.get("hint").set(f"提示: {text}")


# -----更新按钮状态(锁定或正常)-----
def update_ui_lock_state(locked: bool, exception: Button | None = None):
    window.ui_locked = locked
    for ctrl in window.controls:
        if ctrl == exception:
            ctrl.config(state="normal")
        else:
            ctrl.config(state="disabled" if locked else "normal")
