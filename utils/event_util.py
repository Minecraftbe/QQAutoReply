from collections.abc import Callable
from typing import Any
from pubsub import pub


TOPIC_UPDATE_RUNNING_STATE = "update_state"
TOPIC_UPDATE_HINT = "ui.hint"

TOPIC_TOGGLE_RUNNING = "toggle_running"
TOPIC_PAUSE = "pause"
TOPIC_START = "start"
TOPIC_NEW_MESSAGE = "new_message"
TOPIC_LOAD_MESSAGE = "load_message"

TOPIC_SET_COORDINATES = "set_coordinates"
TOPIC_SET_CHAT_BOX_POS = "set_chat_box_pos"
TOPIC_SET_MESSAGE_POS = "set_message_pos"


def subscribe(fun: Callable[..., Any], topic: str):
    pub.subscribe(fun, topic)
