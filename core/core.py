from core.context import Context


class Core:
    def __init__(self, context:Context):
        self.context: Context = context
        self.state: bool = False

    def get_message_pos(self):
        pass

    def get_chat_box_pos(self):
        pass

    def get_state(self):
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def load_messages(self):
        pass

    def set_pos(self):
        pass

    def set_chat_box_pos(self):
        pass

    def set_messages_pos(self):
        pass

    def add_to_loop(self):

    def mainloop(self):



if __name__ == '__main__':
    core = Core(Context("aaa"))
    a = core.context
