from pubsub import pub
from keyboard import add_hotkey
from threading import current_thread
from constants import *
from .log_util import get_logger


def key_listener(hotkey: str | None = None):
    logger = get_logger(f"{__name__}.{key_listener.__name__}")
    if current_thread().name == "MainThread":
        raise RuntimeError("请不要把监听设在主线程")

    if isinstance(hotkey, str) and len(hotkey) == 1:
        add_hotkey(hotkey, lambda: pub.sendMessage(TOPIC_TOGGLE_RUNNING))
        logger.info(f"发现自定义按键，开始监听 {hotkey} 键")
        return

    add_hotkey("p", lambda: pub.sendMessage(TOPIC_TOGGLE_RUNNING))
    logger.info("未发现自定义按键，默认监听 P 键")


if __name__ == '__main__':
    key_listener()
