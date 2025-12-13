from cores.ocr import OpticalCharacterRecognition
from cores.opencv import ImageProcessor
from utils.interfaces import IRunnable, IWithLogger


class Core(IRunnable, IWithLogger):
    def __init__(self):
        super().__init__()
        self.state: bool = False
        self.modules: dict[str:IRunnable] = {}
        self.ocr: OpticalCharacterRecognition = OpticalCharacterRecognition()
        self.opencv: ImageProcessor
        self.opencv = ImageProcessor()
        self.logger.info(f"{self.__class__.__name__} 已初始化")

    def run(self):
        self.opencv.run()


if __name__ == '__main__':
    core = Core()
    print(core.__class__.__name__)
    core.logger.info("hi")
