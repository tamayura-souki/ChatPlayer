import sys
import traceback
from typing import Tuple

import pygame
from pygame.locals import *

from . import logger
from .draw import Render, DrawWindow
from .pygame_utilities import textOutline

def get_quit_event():
    return any(e.type == QUIT for e in pygame.event.get())

class PygameStrRender(Render):
    screen = None
    screen_size = (0,0)
    font = None
    back_color = (0,255,0)

    @classmethod
    def set_screen(cls, screen:pygame.Surface):
        cls.screen = screen
        cls.screen_size = cls.screen.get_size()

    @classmethod
    def set_font(cls, font_name:str, font_size:int):
        cls.font = pygame.font.SysFont(font_name, font_size)

    def __init__(self,
        text:str,
        color = (255,255,255),
        outline_color = (0,0,0),
        font=None
    ):

        font = PygameStrRender.font if font is None else font

        self.pos = [0,0]
        self.v   = [0,0]
        self.a   = [0,0]
        self.render = textOutline(
            font,
            text,
            color,
            outline_color,
            back_color=PygameStrRender.back_color
        ).convert()

        self.size = self.render.get_size()

    def is_draw(self):
        # 画面内外判定
        judge = (
            self.pos[0] > PygameStrRender.screen_size[0],
            self.pos[0] < -self.size[0],
            self.pos[1] > PygameStrRender.screen_size[0],
            self.pos[1] < -self.size[0]
        )
        if any(judge):
            return False

        return True

    def draw(self):
        self.pos[0] += self.v[0]
        self.pos[1] += self.v[1]
        self.v[0] += self.a[0]
        self.v[1] += self.a[1]

        if not self.is_draw():
            return None

        PygameStrRender.screen.blit(self.render, self.pos)
        return True

class PygameSoundRender(Render):
    def __init__(self):
        pass

    def draw(self):
        self.sound
        return None

class PygameWindow(DrawWindow):
    """
    pygame の必要な処理まとめる
    """
    def framework_init(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode(self.window_size)
            pygame.display.set_caption(self.window_caption)
            self.clock = pygame.time.Clock()

        except:
            logger.exception("Error during pygame initialize")
            traceback.print_exc()
            sys.exit(-1)

    def loop_first(self):
        self.clock.tick(self.fps)
        self.screen.fill(self.bg_color)

    def loop_end(self):
        pygame.display.update()

    def quit(self):
        pygame.quit()

