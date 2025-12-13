from abc import abstractmethod, ABC

from utils.log_util import get_logger


class IRunnable(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

class IWithLogger:
    def __init__(self):
        self.logger = get_logger(f"{self.__class__.__module__}.{self.__class__.__name__}")