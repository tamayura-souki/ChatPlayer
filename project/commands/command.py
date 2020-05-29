from abc import ABCMeta, abstractmethod
from . import Render

class Command(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def process_comment(self, text:[str,str]) -> Render:
        # コメントから コマンド処理
        pass