from ui.buttons import *
from ui.labels import *
from ui.update import *
from window import Window


def setup_controllers(windows: Window):
    setup_buttons(windows)
    setup_labels(windows)
    setup_updates(windows)
