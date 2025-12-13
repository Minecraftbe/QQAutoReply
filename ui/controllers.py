from typing import TYPE_CHECKING

from pubsub import pub

from ui.events import on_toggle_running
from utils.event_util import TOPIC_SET_CHAT_BOX_POS, TOPIC_SET_MESSAGE_POS, TOPIC_TOGGLE_RUNNING, TOPIC_UPDATE_HINT, TOPIC_UPDATE_RUNNING_STATE
from .buttons import setup_buttons  # Replace with actual names of the items being imported
from .labels import setup_labels  # Replace with actual names of the items being imported
from .update import setup_updates, update_state, update_chat_box_pos, update_message_pos, update_hint

if TYPE_CHECKING:
    from window import Window

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
