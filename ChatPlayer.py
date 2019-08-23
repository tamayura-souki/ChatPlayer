# -*- coding: utf-8 -*-

# PyGameで配信に映すやつをつくる

import pygame
from pygame.locals import *
import sys

import time
import concurrent.futures

from ChatGetter import Chat_getter

DISPLAY_SIZE = (1280,720)
BACK_COLOR   = (0,255,0)

class Chat_player:
    def __init__(self):
        self.command_list = []
        self.plain_font_size = 40
        self.plain_font = pygame.font.Font("source/Koruri-Semibold.ttf", self.plain_font_size)
        self.niconico_line = 0
        self.niconico_line_max = 12
        self.pre_command = []
    
    def draw(self, command_requests=[]):
        # 受け取ったコマンドから、それぞれコマンドに対応したコマンドオブジェクトを生成する。        
        if (command_requests != []) and (command_requests != self.pre_command):
            [self.command_process(c) for c in command_requests]
            self.pre_command = command_requests

        if len(self.command_list) == 0:
            return None

        chat_renders        = [c.draw() for c in self.command_list]
        # draw() の返り値が Noneのやつを消したい
        self.command_list   = [c for c, r in zip(self.command_list, chat_renders) if not r == None]
        chat_renders        = [{"chat":c[0], "pos":c[1]} for c in chat_renders if not c == None]

        return chat_renders


    def command_process(self, command_request):
        '''
        command = command_request[1].split(' ')
        if len(command) < 2:
            return None
        
        if command[0] == '/nn':
            self.command_list.append(
                NicoNico(
                    command_request[0] + ' : ' + command[-1],
                    self.plain_font,
                    self.niconico_line
                )
            )
            self.niconico_line += 1
            if self.niconico_line >= 12:
                self.niconico_line = 0
        '''
        # めんどうなので、ニコニコ風をデフォにした
        # 時間のあるときに変えよう
        self.command_list.append(
                Niconico(
                    command_request[0] + ' : ' + command_request[1],
                    self.plain_font,
                    self.niconico_line,
                    display_size=DISPLAY_SIZE,
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
        pass

class Niconico(command):
    # 画面を12行にわって、上11行を使う
    def __init__(self, comment:str, font_type, line:int, speed=2.5,
                 display_size=(1920,1080), line_max=16, color=(255,255,255)):
        super(Niconico, self).__init__()
        self.comment    = comment
        self.font_type  = font_type
        self.line       = line
        self.speed      = speed
        self.pos        = [display_size[0]-speed, display_size[1]*line/line_max]
        self.display_size = display_size
        self.color  = color

    def draw(self):
        self.pos[0] = self.pos[0] - self.speed
        render = self.font_type.render(self.comment, True, self.color)
        if self.pos[0] + self.font_type.size(self.comment)[0] == 0:
            return None
        return [render, tuple(self.pos)]

    def line(self):
        return line

    def pos(self):
        return tuple(self.pos)

getter      = Chat_getter("https://www.youtube.com/live_chat?is_popout=1&v=Sflq-_arjDg")
chats       = []

def main():
    global getter, chats
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    pygame.display.set_caption("ChatPlayer")
    player = Chat_player()

    while True:
        screen.fill(BACK_COLOR)

        chat_renders = player.draw(chats)
        if (not chat_renders == None) and (not chat_renders == []):
            for chat_render in chat_renders:
                screen.blit(chat_render["chat"], chat_render["pos"])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                getter.quit()
                sys.exit()

def chat_get():
    global chats
    while True:
        chats = getter.get_chats()
        time.sleep(1)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
executor.submit(main)
executor.submit(chat_get)