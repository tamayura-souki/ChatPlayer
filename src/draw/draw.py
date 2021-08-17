from abc import ABCMeta, abstractmethod

from typing import Tuple

from . import logger
class Render(metaclass=ABCMeta):
    """
    draw window で描画するオブジェクト
    """
    @abstractmethod
    def draw(self):
        # 描画しなくてよくなったら None を返す
        return None

class DrawWindow(metaclass=ABCMeta):
    """
    描画ライブラリで絶対に必要な処理をまとめる
    """
    def __init__(self,
        window_size:Tuple[int, int]=(1280, 720),
        window_caption:str="ChatPlayer",
        fps:int=30,
        bg_color:Tuple[int,int]=(0,255,0)
        ):

        self.window_size = window_size
        self.window_caption = window_caption
        self.fps = fps
        self.bg_color=bg_color

        self.renders = []

        self.framework_init()

    def add_render(self, render:Render):
        if not isinstance(render, Render):
            logger.warning("cannot add render except Render object")
            logger.warning(f"you tried to add {type(render)} object")
            return False

        self.renders.append(render)
        return True

    @abstractmethod
    def framework_init(self):
        """
        framework 別に はじめにやるべき処理を書く
        """
        pass

    @abstractmethod
    def loop_first(self):
        """
        main loop のはじめにやるべき処理
        """
        pass

    @abstractmethod
    def loop_end(self):
        """
        main loop の最後にやるべき処理
        """
        pass

    def main(self, func):
        def inner(*args, **kwargs):
            # 最初に絶対やる処理
            self.loop_first()
            func(*args, **kwargs)
            self.renders = [r for r in self.renders if r.draw() is not None]
            # 最後に絶対やる処理
            self.loop_end()

        return inner

    @abstractmethod
    def quit(self):
        """
        終了処理
        """
        pass