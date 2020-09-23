import sys
import traceback
from typing import Tuple

import pygame
from pygame.locals import *
from pygame.time   import get_ticks

from . import logger
from .draw import Render, DrawWindow
from .pygame_utilities import textOutline

def get_quit_event():
    return any(e.type == QUIT for e in pygame.event.get())

def get_test_event():
    key_states = pygame.key.get_pressed()
    return all([key_states[K_LCTRL], key_states[K_t]])

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
        if ".ttf" not in font_name:
            font_name = pygame.font.match_font(font_name)
        cls.font = pygame.font.Font(font_name, font_size)

    def __init__(self,
        text:str=None,
        color = (255,255,255),
        outline_color = (0,0,0),
        font=None,
        render=None,

        pos = [0.0,0.0],
        v   = [0.0,0.0],
        a   = [0.0,0.0]
    ):

        self.pos = pos
        self.v   = v
        self.a   = a

        if render is not None:
            self.render = render
            self.size = self.render.get_size()
            return

        font = PygameStrRender.font if font is None else font

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
            self.pos[1] > PygameStrRender.screen_size[1],
            self.pos[1] < -self.size[1]
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
    def __init__(self, path, volume):
        self.sound = pygame.mixer.Sound(path)
        self.sound.set_volume(volume)

    def draw(self):
        self.sound.stop()
        self.sound.play()
        return None

class GroupRender(Render):
    def __init__(self, interval, renders):
        self.interval = interval
        self.n_renders = renders
        self.renders  = []
        self.old_time = get_ticks()

        self.renders.append(self.n_renders.pop(0))

    def draw(self):
        if get_ticks() - self.old_time > self.interval:
            if self.n_renders:
                self.renders.append(self.n_renders.pop(0))
                self.old_time = get_ticks()

        self.renders = [r for r in self.renders if r.draw() is not None]

        if not len(self.renders):
            return None
        return True

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
            logger.error("Error during pygame initialize")
            traceback.print_exc()
            sys.exit(-1)

    def loop_first(self):
        self.clock.tick(self.fps)
        self.screen.fill(self.bg_color)

    def loop_end(self):
        pygame.display.update()

    def quit(self):
        pygame.quit()

