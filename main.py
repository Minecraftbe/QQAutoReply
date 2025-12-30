from __future__ import annotations
from threading import Thread
from typing import TYPE_CHECKING
import os
import logging

from ui import Window
from core import Core, CoreThread, ImageProcessor
import utils

if TYPE_CHECKING:
    from pathlib import Path


def main() -> None:
    init()

    key_listening_thread = Thread(
        target=utils.key_listener, daemon=True, name="KeyListeningThread"
    )
    key_listening_thread.start()

    core = Core(ImageProcessor())
    core_thread = CoreThread(core)
    core_thread.start()

    ui = Window()


# TODO: 换用Pathlib
def init() -> None:
    os.environ.setdefault(
        "PADDLE_PDX_CACHE_HOME", str((utils.CWD / ".paddlex").absolute())
    )
    create_dir(utils.CWD / "messages")
    create_dir(utils.CWD / "temp")


def create_dir(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        path.mkdir()


if __name__ == "__main__":
    main()
