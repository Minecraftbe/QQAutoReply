import cores as mypkg_core
from cores.core_thread import CoreThread
from ui import window
import utils as mypkg_utils
from threading import Thread
from os import mkdir, path


def main():
    check()

    key_listening_thread = Thread(target=mypkg_utils.utils.key_listener, daemon=True, name="KeyListeningThread")
    key_listening_thread.start()

    core_thread = CoreThread()
    core_thread.get_core().logger.info("aaaa")

    # 最后初始化ui，要不然主线程任务无法继续执行
    ui = window.init()


def check():
    if not path.exists("messages"):
        mkdir("messages")
    if not path.exists("temp"):
        mkdir("temp")


if __name__ == '__main__':
    main()
