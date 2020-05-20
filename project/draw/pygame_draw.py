import sys
import os
import traceback
from typing import Tuple

import pygame
from pygame.locals import *

sys.path.append(os.pardir)
from config import logger
from .draw import Render, DrawWindow
from .pygame_utilities import textOutline

def get_quit_event():
    return any(e.type == QUIT for e in pygame.event.get())

class PygameStrRender(Render):
    screen = None
    font = None

    @classmethod
    def set_screen(cls, screen:pygame.Surface):
        cls.screen = screen

    @classmethod
    def set_font(cls, font_name:str, font_size:int):
        cls.font = pygame.font.SysFont(font_name, font_size)

    def __init__(self):
        self.pos = (255,255)
        self.render = textOutline(
            PygameStrRender.font,
            "testテキストです☆",
            (255,255,255),
            (0,0,0)
        )

        self.size = (0,0)

    def is_draw(self):
        # 画面内外判定
        return True

    def draw(self):
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

