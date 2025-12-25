from os import mkdir, path
from threading import Thread

import cores as qar_core
import utils as qar_utils
from ui import window


def main():
    check()

    key_listening_thread = Thread(target=qar_utils.util.key_listener, daemon=True, name="KeyListeningThread")
    key_listening_thread.start()

    core_thread = qar_core.CoreThread(10)
    core_thread.start()

    ocr_thread = Thread(target=qar_core.OpticalCharacterRecognition, name="OCRThread", daemon=True)
    ocr_thread.start()
    # 最后初始化ui，要不然主线程任务无法继续执行
    ui = window.init()


def check():
    if not path.exists("messages"):
        mkdir("messages")
    if not path.exists("temp"):
        mkdir("temp")


if __name__ == '__main__':
    main()
