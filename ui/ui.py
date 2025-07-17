from tkinter import Tk, Button, Label, StringVar, messagebox, Frame
from tkinter.filedialog import askopenfilename
from utils.logger_util import get_logger
from utils.utils import get_project_dir
from pubsub import pub
import os

logger = get_logger(__name__)


class Window(Tk):
    def __init__(self):
        super().__init__()
        self.ui_locked: bool = False
        self.vars: dict[str, StringVar | Button] = {}
        self.controls: list[Button] = []
        self.resizable(False, False)
        self.state: bool = False

        self._subscribe_events()

    # -----一种预设, 请手动开启-----
    def use_preset(self):
        frame_top = Frame(self, padx=10, pady=10)
        frame_bottom = Frame(self, padx=10, pady=10)
        frame_top.pack(side="top", fill="x")
        frame_bottom.pack(side="bottom", fill="x")

        state = StringVar()
        state.set("运行状态: False")
        chat_box_pos = StringVar()
        chat_box_pos.set("输入框位置: 未确定")
        message_pos = StringVar()
        message_pos.set("消息位置: 未确定")
        hint = StringVar()
        hint.set("提示: 当选取坐标时请看这里")
        self.vars["hint"] = hint
        self.vars["state"] = state
        self.vars["chat_box_pos"] = chat_box_pos
        self.vars["message_pos"] = message_pos
        self.geometry("450x200+10+10")

        l_state = Label(frame_top, textvariable=state, relief="groove", anchor="w", padx=5)
        l_chat_box_pos = Label(frame_top, textvariable=chat_box_pos, relief="groove", anchor="w", padx=5)
        l_messages_pos = Label(frame_top, textvariable=message_pos, relief="groove", anchor="w", padx=5)
        l_hint = Label(frame_top, textvariable=hint, relief="groove", anchor="w", padx=5)

        l_state.pack(fill="x", pady=3)
        l_chat_box_pos.pack(fill="x", pady=3)
        l_messages_pos.pack(fill="x", pady=3)
        l_hint.pack(fill="x", pady=3)

        # 🔘 控制按钮
        b_load_messages = Button(frame_bottom, text="📥 载入聊天消息", width=10,
                                 command=self.load_message)
        b_start = Button(frame_bottom, text="▶️ 开始/暂停", width=10,
                         command=self.start_or_pause)
        b_set_pos = Button(frame_bottom, text="📍 选取坐标", width=10,
                           command=self.set_coordinates)
        self.vars["b_start"] = b_start

        for btn in (b_load_messages, b_start, b_set_pos):
            self.controls.append(btn)
            btn.pack(side="left", expand=True, fill="x", padx=5, pady=5)

    # -----更新显示内容或状态-----

    def update_state(self, state: bool):
        self.state = state
        self.vars.get("state").set(f"运行状态: {self.state}")

    def update_chat_box_pos(self, pos: tuple):
        self.vars.get("chat_box_pos").set(f"输入框位置: {pos}")

    def update_message_pos(self, pos: tuple):
        self.vars.get("message_pos").set(f"消息位置: {pos}")
        self.update_ui_lock_state(False)

    def update_hint(self, text: str):
        self.vars.get("hint").set(f"提示: {text}")

    # -----更新按钮状态(锁定或正常)-----
    def update_ui_lock_state(self, locked: bool, exception: Button | None = None):
        self.ui_locked = locked
        for ctrl in self.controls:
            if ctrl == exception:
                ctrl.config(state="normal")
            else:
                ctrl.config(state="disabled" if locked else "normal")

    # -----按钮对应指令-----

    @staticmethod
    def load_message():
        file: str = askopenfilename(initialdir=get_project_dir()+"\\messages", filetypes=(("对话文件","*.json"), ("所有文件", "*.*")))
        pub.sendMessage("load_message", file=file)
        logger.debug(file)

    def start_or_pause(self):
        if self.state:
            pub.sendMessage("pause")
            self.update_ui_lock_state(False)
            # test
            self.state = False
            self.update_state(self.state)
        else:
            pub.sendMessage("start")
            self.update_ui_lock_state(True, self.vars.get("b_start"))
            # test
            self.state = True
            self.update_state(self.state)

    def set_coordinates(self):
        self.update_ui_lock_state(True)
        pub.sendMessage("set_coordinates")

    # -----监听消息-----

    def _subscribe_events(self):
        pub.subscribe(self.update_state, "update_state")
        pub.subscribe(self.update_chat_box_pos, "update_chat_box_pos")
        pub.subscribe(self.update_message_pos, "update_message_pos")
        pub.subscribe(self.update_hint, "update_ui.hint")

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    import core.picker

    logger.info("hello world")
    root = Window()
    root.use_preset()
    root.run()
