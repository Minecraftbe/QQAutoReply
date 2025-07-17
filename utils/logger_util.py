import logging
from sys import stdout
from utils.utils import get_project_dir
from os.path import exists


def setup_logger():
    log_dir: str = get_project_dir() + "\\latest.log"

    logger = logging.getLogger()
    if logger.handlers:
        return  # 已设置过，不重复添加

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "[%(asctime)s] [%(threadName)s/%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%H:%M:%S"
    )

    # 🔹 文件 Handler（写入日志文件）
    file_handler = logging.FileHandler(log_dir, mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)

    # 🔹 控制台 Handler（输出到终端）
    console_handler = logging.StreamHandler(stdout)
    console_handler.setFormatter(formatter)

    # 添加 Handler
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


def get_logger(name: str):
    setup_logger()
    return logging.getLogger(name)
