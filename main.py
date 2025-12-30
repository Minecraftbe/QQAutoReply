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
    core_thread = CoreThread(core, 2)
    core_thread.start()
    del core  # 同时删除主线程对image processor的引用, 由于我目前没搜到的原因, 保留这个引用mss会报错

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
