# -*- coding: utf-8 -*-

# Chat_player クラス

import pygame
from pygame.locals import *

<<<<<<< Updated upstream
import pygame_utilities as pygu
=======
from SuperChat import SuperChatAir
from ChatCommands import *
>>>>>>> Stashed changes

import json

class Chat_player:
    def __init__(self, display_size):
        # display_size [横, 縦]
        setting = json.load(open("chat_setting.json", 'r', encoding='utf-8', errors='ignore'))

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

        # 文字速度コマンドの読み込み
        self.speed_commands = []
        for speed_command in setting["speed_commands"]:
            try:
                if len(speed_command["command"]) <= 0:
                    continue

                self.speed_commands.append(speed_command)

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
        
        # 文字降らしコマンドの読み込み
        self.rain_commands = []
        for rain_command in setting["rain_commands"]:
            try:
                if len(rain_command["command"]) <= 0:
                    continue

                for i in range(3):
                    if rain_command["color"][i] < 0 \
                        or rain_command["color"][i] > 255:
                        raise ValueError

                self.rain_commands.append(rain_command)

            except ValueError:
                print("fail rain format")
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
        chat_renders        = [r for r in chat_renders if not r == None]
        chat_renders        = [{"chat":c[0], "pos":c[1]} for chats in chat_renders
                                    for c in chats if not c == None]

        return chat_renders


    def command_process(self, command_request):
        # コマンドを処理する
        # 音声系コマンドを処理
        for sound_command in self.sound_commands:
            if sound_command["command"] in command_request[1]:
                sound_command["Sound"].stop()
                return sound_command["Sound"].play()
        
        for rain_command in self.rain_commands:
            if rain_command["command"] in command_request[1]:
                return self.command_list.append(
                    Rain(
                        rain_command["drops"],
                        self.plain_font,
                        rain_command["time"],
                        v=rain_command["v0"],
                        accel=rain_command["accel"],
                        color=tuple(rain_command["color"]),
                        display_size=self.display_size
                    )
                )
        
        chat  = command_request[0] + ' : ' + command_request[1].split(' ')[-1]
        color = (255,255,255)
        outline_color = (30,30,30)
        # 横1280で 1 frame 4
        speed = self.display_size[0] / 270

        if '/unk' in command_request[1]:
            chat = command_request[1].split(' ')[-1]

<<<<<<< Updated upstream
=======
        # エアスパチャ
        if '/superchat' in command_request[1] or '/sc' in command_request[1]:
            superchat = command_request[1].split(' ')
            if len(superchat) > 1:
                return self.SuperChat.super_chat(command_request[0], superchat[-1], superchat[-2] if len(superchat) > 2 else "")
        
>>>>>>> Stashed changes
        # 速度系のコマンドを処理
        for speed_command in self.speed_commands:
            if speed_command["command"] in command_request[1]:
                speed *= speed_command["speed"]
                break

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
                    display_size = self.display_size,
                    line_max = self.niconico_line_max
                )
            )
        self.niconico_line += 1
        if self.niconico_line >= self.niconico_line_max:
            self.niconico_line = 0