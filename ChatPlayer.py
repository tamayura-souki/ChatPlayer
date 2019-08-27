# -*- coding: utf-8 -*-

# Chat_player クラス

import pygame
from pygame.locals import *

import pygame_utilities as pygu

import json

class Chat_player:
    def __init__(self, display_size):
        # display_size [横, 縦]

        setting = json.load(open("chat_setting.json", 'r'))

        self.display_size = display_size

        self.command_list = []
        self.niconico_line = 0
        self.niconico_line_max = 12
        self.plain_font_size = int(self.display_size[1] / self.niconico_line_max  *2/3)
        self.plain_font = pygame.font.Font(setting["plain_font_path"], self.plain_font_size)

        # 音声系のコマンドの読み込み
        self.sound_commands = []
        for sound_command in setting["sound_commands"]:
            try:
                command = sound_command["command"]
                if len(command) <= 0:
                    continue

                Sound = pygame.mixer.Sound(sound_command["path"])
                Sound.set_volume(sound_command["volume"])

                self.sound_commands.append({"command": command, "Sound": Sound})
            except:
                continue

        # 文字色コマンドの読み込み
        self.font_color_commands = []
        for color_command in setting["color_commands"]:
            try:
                if len(color_command["command"]) <= 0:
                    continue

                for i in range(3):
                    if color_command["font_color"][i] < 0 \
                            or color_command["font_color"][i] > 255:
                        raise ValueError
                    
                    if color_command["outline_color"][i] < 0 \
                            or color_command["outline_color"][i] > 255:
                        raise ValueError

                self.font_color_commands.append(color_command)

            except ValueError:
                print("fail color format")
                continue
                
            except:
                continue


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

        # 音声系コマンドを処理
        for sound_command in self.sound_commands:
            if sound_command["command"] in command_request[1]:
                sound_command["Sound"].stop()
                return sound_command["Sound"].play()

        chat  = command_request[0] + ' : ' + command_request[1].split(' ')[-1]
        color = (255,255,255)
        outline_color = (30,30,30)
        # 横1280で 1 frame 4
        speed = self.display_size[0] / 320

        if '/unk' in command_request[1]:
            chat = command_request[1].split(' ')[-1]

        if '/fast' in command_request[1]:
            speed *= 2
        
        elif '/slow' in command_request[1]:
            speed = speed /4 * 1.5
        
        # チャット色系のコマンドを処理
        for color_command in self.font_color_commands:
            if color_command["command"] in command_request[1]:
                color           = tuple(color_command["font_color"])
                outline_color   = tuple(color_command["outline_color"])
                break

        self.command_list.append(
                Niconico(
                    chat,
                    self.plain_font,
                    self.niconico_line,
                    speed = speed,
                    color = color,
                    outline_color = outline_color,
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
    def __init__(self, comment:str, font_type, line:int, speed=4, color=(255,255,255), outline_color = (30,30,30),
                 display_size=(1920,1080), line_max=16, back_color=(0,255,0)):
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