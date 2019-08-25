# -*- coding: utf-8 -*-

# Chat_player クラス

import pygame
from pygame.locals import *

import pygame_utilities as pygu

import json

class Chat_player:
    def __init__(self, display_size):
        # display_size [横, 縦]

        setting = json.load(open('chat_setting.json', 'r'))

        self.display_size = display_size

        self.command_list = []
        self.niconico_line = 0
        self.niconico_line_max = 12
        self.plain_font_size = int(self.display_size[1] / self.niconico_line_max  *2/3)
        self.plain_font = pygame.font.Font(setting['plain_font_path'], self.plain_font_size)

        self.police_sound = pygame.mixer.Sound(setting['police_path'])
        self.medic_sound  = pygame.mixer.Sound(setting['medic_path'])
        self.w_sound      = pygame.mixer.Sound(setting['laughter_path'])
        self.police_sound.set_volume(setting['police_vol'])
        self.medic_sound.set_volume(setting['medic_vol'])
        self.w_sound.set_volume(setting['laughter_vol'])

        self.pre_commands = []

    
    def draw(self):
        if len(self.command_list) == 0:
            return None

        chat_renders        = [c.draw() for c in self.command_list]
        # draw() の返り値が Noneのやつを消したい
        self.command_list   = [c for c, r in zip(self.command_list, chat_renders) if not r == None]
        chat_renders        = [{"chat":c[0], "pos":c[1]} for c in chat_renders if not c == None]

        return chat_renders


    def command_process(self, command_request):
        # コマンドを処理する
        if '/police' in command_request[1]:
            self.police_sound.stop()
            return self.police_sound.play()

        elif '/medic' in command_request[1]:
            self.medic_sound.stop()
            return self.medic_sound.play()

        elif '/w' in command_request[1]:
            return self.w_sound.play()
            
        chat  = command_request[0] + ' : ' + command_request[1].split(' ')[-1]
        color = (255,255,255)
        # 横1280で 1 frame 4
        speed = self.display_size[0] / 320

        if '/unk' in command_request[1]:
            chat = command_request[1].split(' ')[-1]

        if '/fast' in command_request[1]:
            speed *= 2
        
        elif '/slow' in command_request[1]:
            speed = speed /4 * 1.5
        
        if '/red' in command_request[1]:
            color = (255,0,0)

        elif '/blue' in command_request[1]:
            color = (0,0,255)

        elif '/green' in command_request[1]:
            color = (0,255,0)
        
        elif '/bk' in command_request[1]:
            color = (0,0,0)

        self.command_list.append(
                Niconico(
                    chat,
                    self.plain_font,
                    self.niconico_line,
                    speed = speed,
                    color = color,
                    display_size=self.display_size,
                    line_max=self.niconico_line_max
                )
            )
        self.niconico_line += 1
        if self.niconico_line >= self.niconico_line_max:
            self.niconico_line = 0



class command:
    # コマンドを処理するクラスの雛形
    def __init__(self):
        pass
    def draw(self):
        # 毎回呼び出される関数
        return None

class Niconico(command):
    # 画面を16行にわる
    def __init__(self, comment:str, font_type, line:int, speed=4, color=(255,255,255),
                 display_size=(1920,1080), line_max=16, outline_color = (30,30,30), back_color=(0,255,0)):
        super(Niconico, self).__init__()
        self.comment    = comment
        self.font_type  = font_type
        self.line       = line
        self.speed      = speed
        self.pos        = [display_size[0]-speed, display_size[1]*line/line_max]
        self.display_size = display_size
        self.color      = color
        self.outline_color = outline_color
        self.render     = pygu.textOutline(self.font_type, self.comment, self.color, self.outline_color, outline_width=1, back_color=back_color).convert()

    def draw(self):
        self.pos[0] = self.pos[0] - self.speed
        if self.pos[0] + self.font_type.size(self.comment)[0] <= 0:
            return None
        return [self.render, tuple(self.pos)]

    def line(self):
        return line

    def pos(self):
        return tuple(self.pos)