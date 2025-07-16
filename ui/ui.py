from tkinter import Tk, Button, Label, StringVar
from utils.logger_util import get_logger
from context import Context

logger = get_logger(__name__)

class Window(Tk):
    def __init__(self, context):
        super().__init__()
        self.context = context

        self.state = StringVar()
        self.state.set("状态: False")
        self.chat_box_pos = StringVar()
        self.chat_box_pos.set("输入框位置: 未确定")
        self.message_pos = StringVar()
        self.message_pos.set("消息位置: 未确定")

        self.geometry("200x100+10+10")

    def use_preset(self):
        b_load_messages = Button(self, text="载入存放的聊天消息", relief="groove")
        # b_load_messages = Button(self, text="载入存放的聊天消息", relief="groove", command=self.context.core.load)
        b_start = Button(self, text="开始", relief="groove")
        # b_start = Button(self, text="开始", relief="groove", command=self.context.core.start)
        b_set_pos = Button(self, text="选取坐标", relief="groove", command=self.test)

        l_state = Label(self, textvariable=self.state, relief="groove")
        l_chat_box_pos = Label(self, textvariable=self.chat_box_pos, relief="groove")
        l_messages_pos = Label(self, textvariable=self.message_pos, relief="groove")

        b_load_messages.pack()
        b_start.pack()
        b_set_pos.pack()
        l_chat_box_pos.pack()
        l_messages_pos.pack()
        l_state.pack()

    def run(self):
        self.mainloop()

    def update_state(self, state: bool):
        self.state.set(f"状态: {state}")

    def update_chat_box_pos(self, pos: tuple):
        self.chat_box_pos.set(f"输入框位置: {pos}")

    def update_message_pos(self, pos: tuple):
        self.message_pos.set(f"消息位置: {pos}")


if __name__ == '__main__':
    logger.info("hello world")
    root = Window(Context("A"))
    root.use_preset()
    root.run()