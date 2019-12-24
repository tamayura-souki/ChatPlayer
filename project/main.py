# -*- coding: utf-8 -*-

# PyGameで配信に映すやつをつくる

import sys
import traceback
import time
import json

import tkinter as tk

import pygame
from pygame.locals import *

from pytchat    import LiveChat
from ChatPlayer import Chat_player

class ChatPlayerApp():
    def __init__(self, json_file):
        self.json_file = json_file
        self.setting   = json.load(open(json_file, 'r', encoding='utf-8', errors='ignore'))

        self.make_livechat()

        self.end_f     = False

    # callback func
    def command_get(self, data):
        for c in data.items:
            self.player.command_process([c.author.name, c.message])
            data.tick()

    def setting_window(self):
        root = tk.Tk()
        root.title("配信のIDを入力")
        root.geometry("200x50")

        def ok():
            self.setting["chat_id"] = txt.get()
            root.destroy()

        def end():
            self.end_f = True
            root.destroy()
            sys.exit(0)

        lbl = tk.Label(text='ID')
        lbl.place(x=10, y=10)

        txt = tk.Entry()
        txt.place(x=30, y=10)
        txt.insert(tk.END, self.setting["chat_id"])

        enter_btn = tk.Button(text="Ok", command=ok)
        enter_btn.place(x=160, y=5)

        root.protocol("WM_DELETE_WINDOW", end)
        root.mainloop()

    def make_livechat(self):
        try:
            self.setting_window()
            self.getter = LiveChat(self.setting["chat_id"], callback = self.command_get)

            with open(self.json_file, "w", encoding='utf-8', errors='ignore') as f:
                json.dump(self.setting, f)

        except:
            print("Error Live Chat")
            sys.exit(-1)    

    def init_pygame(self):
        try:
            pygame.init()
            self.screen = pygame.display.set_mode(self.setting["win_size"])
            pygame.display.set_caption("ChatPlayer")
            self.clock = pygame.time.Clock()

        except:
            print("Error Pygame initialize")
            traceback.print_exc()
            sys.exit(-1)


    def main(self):
        
        self.init_pygame()

        try:
            self.player = Chat_player(self.setting["win_size"])

        except:
            print("Error ChatPlayer")
            pygame.quit()
            sys.exit(-1)

        print("boot chatplayer")

        while not self.end_f:
            if not self.getter.is_alive():
                print("live is none")
                pygame.quit()
                self.make_livechat()
                self.init_pygame()

            try:
                self.clock.tick(30)
                self.screen.fill(self.setting["back_color"])

                chat_renders = self.player.draw()
                if (not chat_renders == None) and (not chat_renders == []):
                    [self.screen.blit(chat_render["chat"], chat_render["pos"]) for chat_render in chat_renders]

                pygame.display.update()

            except:
                print("error mainloop")
                traceback.print_exc()
                sys.exit(-1)
        
            # 終了処理
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    self.getter.terminate()
                    sys.exit(0)

        pygame.quit()
        self.getter.terminate()
        sys.exit(0)

if __name__ == "__main__":
    chatplayer = ChatPlayerApp("setting.json")
    chatplayer.main()