from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from . import Render

@dataclass
class CommentData:
    author_name: str
    message: str

class Command(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def process_comment(self, comment:CommentData) -> Render:
        # コメントから コマンド処理
        pass