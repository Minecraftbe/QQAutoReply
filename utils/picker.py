import collections
from pyautogui import position
from time import sleep
from pubsub import pub

from utils.event_util import TOPIC_SET_CHAT_BOX_POS, TOPIC_SET_POSITIONS, TOPIC_SET_MESSAGE_AREA, TOPIC_UPDATE_HINT
from utils.log_util import get_logger
from threading import Thread

logger = get_logger(__name__)

type pos = tuple[int, int]
type area = tuple[int, int, int, int]

def chat_box_picker() -> pos:
    delay: int = 2
    hint: str = f"🖱 现在选取输入框位置，请将鼠标移动到目标位置，{delay} 秒后将获取坐标..."
    pub.sendMessage(TOPIC_UPDATE_HINT, text=hint)
    sleep(delay)
    x, y = position()
    logger.info(f"📍 当前坐标：({x}, {y})")
    pub.sendMessage(TOPIC_SET_CHAT_BOX_POS, pos=(x, y))
    return x, y


def messages_picker() -> area:
    delay: int = 3
    pub.sendMessage(TOPIC_UPDATE_HINT, text=f"❗ 现在选取聊天界面位置，请移动鼠标到聊天界面框左上角，{delay} 秒后获取坐标")
    sleep(delay)
    x1, y1 = position()

    
    pub.sendMessage(TOPIC_UPDATE_HINT, text=f"🖱 移动鼠标到右下角，{delay} 秒后获取坐标")
    sleep(delay)
    x2, y2 = position()

    # width = x2 - x1
    # height = y2 - y1
    logger.info(f"📍 左上角：({x1}, {y1})")
    logger.info(f"📍 右下角：({x2}, {y2})")
    logger.info(f"✅ 截图区域: ({x1}, {y1}, {x2}, {y2})")

    if x2 <= x1 or y2 <= y1:
        logger.warning("❌ 坐标选择错误, 正在对坐标进行调整")
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        logger.info(f"✅ 已调整截图区域: ({x1}, {y1}, {x2}, {y2})")

    pub.sendMessage(TOPIC_UPDATE_HINT, text="坐标选取已完成！")
    pub.sendMessage(TOPIC_SET_MESSAGE_AREA, pos=(x1, y1, x2, y2))
    return x1, y1, x2, y2


def set_positions():
    chat_box_picker()
    messages_picker()


def init():
    Thread(target=set_positions, daemon=True, name="PositionPickerThread").start()


pub.subscribe(init, TOPIC_SET_POSITIONS)
