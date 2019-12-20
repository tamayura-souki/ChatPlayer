# -*- coding: utf-8 -*-

# PyGameで配信に映すやつをつくる

import pygame
from pygame.locals import *
import sys
import time

from pytchat    import LiveChat
from ChatPlayer import Chat_player

import json
import traceback


def command_get(data):
    global player

    for c in data.items:
        player.command_process([c.author.name, c.message])
        data.tick()

setting  = json.load(open("setting.json", 'r'))

DISPLAY_SIZE = tuple(setting["win_size"])
BACK_COLOR   = tuple(setting["back_color"])
CHAT_ID      = setting["chat_id"]

print("complete loding json")
try:
    getter = LiveChat(CHAT_ID, callback = command_get)

except:
    sys.exit()
    
player = None

def main():
    global player, getter

    try:
        pygame.init()
        screen = pygame.display.set_mode(DISPLAY_SIZE)
        pygame.display.set_caption("ChatPlayer")
        clock = pygame.time.Clock()

    except:
        print("Error Pygame initialize")
        traceback.print_exc()
        sys.exit(0)

    try:
        player = Chat_player(DISPLAY_SIZE)

    except:
        print("Error ChatPlayer")
        pygame.quit()
        sys.exit(0)

    print("boot chatplayer")


    while getter.is_alive():
        try:
            clock.tick(30)
            screen.fill(BACK_COLOR)

            chat_renders = player.draw()
            if (not chat_renders == None) and (not chat_renders == []):
                [screen.blit(chat_render["chat"], chat_render["pos"]) for chat_render in chat_renders]

            pygame.display.update()

        except:
            traceback.print_exc()
            sys.exit(0)
        
        # 終了処理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                getter.terminate()
                sys.exit(0)

    pygame.quit()
    getter.terminate()
    sys.exit(0)                


if __name__ == "__main__":
    main()