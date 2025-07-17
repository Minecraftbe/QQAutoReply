from constants import *
from .buttons import *
from .labels import *
from .update import *


def setup_controllers(windows: "Window"):
    setup_buttons(windows)
    setup_labels(windows)
    setup_updates(windows)


# -----监听消息-----
def subscribe_events():
    pub.subscribe(update_state, TOPIC_UPDATE_RUNNING_STATE)
    pub.subscribe(update_chat_box_pos, TOPIC_SET_CHAT_BOX_POS)
    pub.subscribe(update_message_pos, TOPIC_SET_MESSAGE_POS)
    pub.subscribe(update_hint, TOPIC_UPDATE_HINT)
    pub.subscribe(on_toggle_running, TOPIC_TOGGLE_RUNNING)
