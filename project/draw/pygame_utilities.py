# -*- coding: utf-8 -*-
# https://www.pygame.org/pcr/hollow_outline/index.php

import pygame, pygame.font, pygame.image
from pygame.locals import *

# outline_width を 1以上にすると いけない
# CSS の 太文字作成を参考に改良すること

def textHollow(font, message, fontcolor, outline_width=1):
    notcolor = [c^0xFF for c in fontcolor]
    base = font.render(message, False, fontcolor, notcolor)
    size = base.get_width() + outline_width*2, base.get_height() + outline_width*2
    img = pygame.Surface(size, 16)
    img.fill(notcolor)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (outline_width*2, 0))
    img.blit(base, (0, outline_width*2))
    img.blit(base, (outline_width*2, outline_width*2))
    base.set_colorkey(0)
    base.set_palette_at(1, notcolor)
    img.blit(base, (outline_width, outline_width))
    img.set_colorkey(notcolor)
    return img

def textOutline(font, message, fontcolor, outlinecolor, outline_width=1, back_color=(0,255,0)):
    base = font.render(message, 0, fontcolor)
    outline = textHollow(font, message, outlinecolor, outline_width=outline_width)
    img = pygame.Surface(outline.get_size(), 16)
    img.fill(back_color)
    img.blit(base, (outline_width, outline_width))
    img.blit(outline, (0, 0))
    img.set_colorkey(back_color)
    return img