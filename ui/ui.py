from tkinter import Tk, Button, Label, StringVar

from context import Context


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
        b_load = Button(self, text="载入", relief="groove")
        # b_load = Button(self, text="载入", relief="groove", command=self.context.core.load)
        b_start = Button(self, text="开始", relief="groove")
        # b_start = Button(self, text="开始", relief="groove", command=self.context.core.start)
        b_set_pos = Button(self, text="选取坐标", relief="groove", command=self.test)
        l_state = Label(self, textvariable=self.state, relief="groove")
        l_chat_box_pos = Label(self, textvariable=self.chat_box_pos, relief="groove")
        l_message_pos = Label(self, textvariable=self.message_pos, relief="groove")
        b_load.pack()
        b_start.pack()
        b_set_pos.pack()
        l_chat_box_pos.pack()
        l_message_pos.pack()
        l_state.pack()

    def run(self):
        self.mainloop()

    def update_state(self, state: bool):
        self.state.set(f"状态: {state}")

    def update_chat_box_pos(self, pos: tuple):
        self.chat_box_pos.set(f"输入框位置: {pos}")

    def update_message_pos(self, pos: tuple):
        self.message_pos.set(f"消息位置: {pos}")

    def test(self):
        self.update_chat_box_pos((100, 1990))

if __name__ == '__main__':
    root = Window(Context("A"))
    root.use_preset()
    root.run()