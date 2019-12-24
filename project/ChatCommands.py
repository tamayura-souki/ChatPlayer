import pygame
from pygame.locals import *

import pygame_utilities as pygu

import time   as std_t
import random as rnd

class command:
    # コマンドを処理するクラスの雛形
    def __init__(self):
        pass
    def draw(self):
        # 毎回呼び出される関数
        # return [[self.render, tuple(self.pos)]]
        return None

class Rain(command):
    def __init__(self, drops_str:str, font_type, time, v=0, accel=0.2, color=(255,255,255),
                 display_size=(1920,1080)):
        super(Rain, self).__init__()
        self.font_type  = font_type
        self.v0         = v
        self.accel      = accel
        self.time       = time
        self.color      = color
        self.renders    = [self.font_type.render(c, False, self.color) for c in drops_str]
        self.display_size = display_size

        # drops = [{"x":, "y":, "v":, "render_type":}]
        self.drops   = []
        self.start_t = std_t.time()

    def draw(self):
        if not  std_t.time() - self.start_t > self.time:
            self.drops.append({"x": rnd.randrange(int(self.display_size[0])), "y":-self.renders[0].get_height(), "v":self.v0,
                                "render_type": rnd.randrange(len(self.renders))})

        drop_n = len(self.drops)
        for i in range(drop_n):
            self.drops[i]["y"] += self.drops[i]["v"]
            self.drops[i]["v"] += self.accel
            if self.drops[i]["y"] > self.display_size[1]:
                self.drops[i] = None

        self.drops = [d for d in self.drops if not d == None]
        if len(self.drops) == 0:
            return None
        return [[self.renders[d["render_type"]], tuple([d["x"], d["y"]])] for d in self.drops]

class Niconico(command):
    # 画面を16行にわる
    def __init__(self, comment:str, font_type, line:int, speed=4, color=(255,255,255), outline_color = (30,30,30),
                 display_size=(1920,1080), line_max=16, back_color=(0,255,0)):
        super(Niconico, self).__init__()
        self.comment    = comment
        self.font_type  = font_type
        self.line       = line
        self.speed      = speed
        self.display_size = display_size
        self.color      = color
        self.outline_color = outline_color
        self.render     = pygu.textOutline(self.font_type, self.comment, self.color, self.outline_color, outline_width=1, back_color=back_color).convert()

        self.pos        = [display_size[0]-speed if speed > 0 else -self.render.get_width(),
                            display_size[1]*line/line_max]

    def draw(self):
        self.pos[0] -= self.speed
        if self.pos[0] + self.render.get_width() < 0 \
            or self.pos[0] > self.display_size[0]:
            return None
        return [[self.render, tuple(self.pos)]]

    def line(self):
        return self.line

    def pos(self):
        return tuple(self.pos)