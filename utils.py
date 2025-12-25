from collections.abc import Callable
from os.path import dirname, abspath
from sys import stdout
from time import sleep
from typing import Any
from pubsub import pub
from keyboard import add_hotkey
from threading import Thread, current_thread
from pyautogui import position

import logging

TOPIC_UPDATE_RUNNING_STATE = "update_state"
TOPIC_UPDATE_HINT = "ui.hint"

TOPIC_TOGGLE_RUNNING_STATE = "toggle_running"
TOPIC_PAUSE = "pause"
TOPIC_START = "start"
TOPIC_NEW_MESSAGE = "new_message"
TOPIC_LOAD_MESSAGE = "load_message"

TOPIC_SET_POSITIONS = "set_coordinates"
TOPIC_SET_CHAT_BOX_POS = "set_chat_box_pos"
TOPIC_SET_MESSAGE_AREA = "set_message_pos"


def subscribe(topic: str):
    """该装饰器只能用于函数而非方法."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        pub.subscribe(func, topic)
        return func

    return decorator


# TODO: 换用Pathlib， 并改进逻辑直到找到pyproject.toml
def get_project_dir():
    current_path = dirname(abspath(__file__))
    # 获取当前脚本所在的项目根目录
    root_path = dirname(current_path)
    # print("项目根目录路径：", root_path)
    return root_path


# TODO:换pathlib
def setup_logger():
    log_dir: str = get_project_dir() + "\\latest.log"

    logger = logging.getLogger()
    if logger.handlers:
        return  # 已设置过，不重复添加

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(threadName)s/%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%H:%M:%S",
    )

    # 🔹 文件 Handler（写入日志文件）
    file_handler = logging.FileHandler(log_dir, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 🔹 控制台 Handler（输出到终端）
    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)

    # 添加 Handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_logger(name: str):
    setup_logger()
    return logging.getLogger(name)


logger = get_logger(__name__)


# TODO: 移动这段代码到更合适的位置
def key_listener(hotkey: str | None = None):
    logger = get_logger(f"{__name__}.{key_listener.__name__}")
    if current_thread().name == "MainThread":
        raise RuntimeError("请不要把监听设在主线程")

    if isinstance(hotkey, str) and len(hotkey) == 1:
        add_hotkey(hotkey, lambda: pub.sendMessage(TOPIC_TOGGLE_RUNNING_STATE))
        logger.info(f'发现自定义按键，开始监听 "{hotkey}" 键')
        return

    add_hotkey("p", lambda: pub.sendMessage(TOPIC_TOGGLE_RUNNING_STATE))
    logger.info('未发现自定义按键，默认监听 "P" 键')


type pos = tuple[int, int]
type area = tuple[int, int, int, int]


def chat_box_pos_picker() -> pos:
    delay: int = 2
    hint: str = (
        f"🖱 现在选取输入框位置，请将鼠标移动到目标位置，{delay} 秒后将获取坐标..."
    )
    pub.sendMessage(TOPIC_UPDATE_HINT, text=hint)
    sleep(delay)
    x, y = position()
    logger.info(f"📍 当前坐标：({x}, {y})")
    pub.sendMessage(TOPIC_SET_CHAT_BOX_POS, pos=(x, y))
    return x, y


def messages_area_picker() -> area:
    delay: int = 3
    pub.sendMessage(
        TOPIC_UPDATE_HINT,
        text=f"❗ 现在选取聊天界面位置，请移动鼠标到聊天界面框左上角，{delay} 秒后获取坐标",
    )
    sleep(delay)
    x1, y1 = position()

    pub.sendMessage(TOPIC_UPDATE_HINT, text=f"🖱 移动鼠标到右下角，{delay} 秒后获取坐标")
    sleep(delay)
    x2, y2 = position()

    # width = x2 - x1
    # height = y2 - y1
    logger.info(f"📍 左上角：({x1}, {y1})")
    logger.info(f"📍 右下角：({x2}, {y2})")
    logger.info(f"✅ 截图区域: ({x1}, {y1}) 到 ({x2}, {y2})")

    if x2 <= x1 or y2 <= y1:
        logger.warning("❌ 坐标选择错误, 正在对坐标进行调整")
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        logger.info(f"✅ 已调整截图区域: ({x1}, {y1}, {x2}, {y2})")

    pub.sendMessage(TOPIC_UPDATE_HINT, text="坐标选取已完成！")
    pub.sendMessage(TOPIC_SET_MESSAGE_AREA, pos=(x1, y1, x2, y2))
    return x1, y1, x2, y2


def set_positions():
    chat_box_pos_picker()
    messages_area_picker()


@subscribe(TOPIC_SET_POSITIONS)
def picker_init():
    Thread(target=set_positions, daemon=True, name="PositionPickerThread").start()


if __name__ == "__main__":
    key_listener()
