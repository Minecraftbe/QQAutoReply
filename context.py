class Context:
    def __init__(self, config):
        self.config = config
        self.ui = None
        self.core = None

    def set_core(self, core):
        self.core = core

    def set_ui(self, ui):
        self.ui = ui

    def update_ui(self):
        self.ui.update_label(self.core.get_state())

