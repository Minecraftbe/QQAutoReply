from ui.ui import Window
from core.core import Core
from utils.logger_util import get_logger

logger = get_logger(__name__)


class Context:
    def __init__(self, config):
        self.config = config
        self._checked: bool = False
        self.ui: Window | None = None
        self.core: Core | None = None

    def bind_core(self, core):
        if self.core is not None:
            logger.warning("不能重复绑定 Core")
            return
        self.core = core
        logger.info(f"Core 已绑定, Core: {self.core}")

    def bind_ui(self, ui):
        if self.ui is not None:
            logger.warning("不能重复绑定 UI")
            return
        self.ui = ui
        logger.info(f"UI 已绑定, UI: {self.ui}")

    def update_ui(self):
        self.check_at_first()
        self.ui.update_state(self.core.get_state())
        self.ui.update_chat_box_pos(self.core.get_chat_box_pos())
        self.ui.update_message_pos(self.core.get_message_pos())

    def get_message_pos(self):
        self.check_at_first()
        return self.core.get_message_pos()

    def get_chat_box_pos(self):
        self.check_at_first()
        return self.core.get_chat_box_pos()

    def get_state(self):
        self.check_at_first()
        return self.core.get_state()

    def start_core(self):
        self.check_at_first()
        self.core.start()

    def pause_core(self):
        self.check_at_first()
        self.core.pause()

    def load_messages(self):
        self.check_at_first()
        self.core.load_messages()

    def set_pos(self):
        self.check_at_first()
        self.core.set_chat_box_pos()
        self.core.set_messages_pos()

    def check_at_first(self):
        if not self._checked:
            self.checks()

    def checks(self):
        if self.core is None and self.ui is None:
            raise RuntimeError("Core 和 UI 未设置")
        if self.core is None:
            raise RuntimeError("Core 未设置")
        if self.ui is None:
            raise RuntimeError("UI 未设置")
        self._checked = True
        logger.info("所有检测已通过")
