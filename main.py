from os import mkdir, path
from threading import Thread

import core
from ui import Window
import utils


def main():
    check()

    key_listening_thread = Thread(
        target=utils.key_listener, daemon=True, name="KeyListeningThread"
    )
    key_listening_thread.start()

    core_thread = core.CoreThread(10)
    core_thread.start()

    # ocr_thread = Thread(target=core.OCR, name="OCRThread", daemon=True)
    # ocr_thread.start()

    # 最后初始化ui，要不然主线程任务无法继续执行
    ui = Window()


# TODO: 换用Pathlib
def check():
    if not path.exists("messages"):
        mkdir("messages")
    # if not path.exists("temp"):
    #     mkdir("temp")


if __name__ == "__main__":
    main()
