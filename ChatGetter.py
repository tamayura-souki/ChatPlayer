# -*- coding: utf-8 -*-

# YoutubeChatで遊ぶためのコード
# Chat取得部分をつくる

import codecs
import emoji
from selenium import webdriver

class Chat_getter:
    def __init__(self, chat_url:str, driver_path=None):
        self.url        = chat_url
        options         = webdriver.ChromeOptions()
        options.add_argument('--headless')
        if driver_path == None:
            self.driver = webdriver.Chrome(options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=driver_path, options=options)
        self.sent_author_names  = []
        self.sent_messages      = []

        self.driver.get(self.url)

    def get_chats(self, author_selector='#author-name.yt-live-chat-author-chip', 
                        message_selector='#message.yt-live-chat-text-message-renderer'):
        # チャット欄の取得
        author_names  = self.driver.find_elements_by_css_selector(author_selector)
        messages      = self.driver.find_elements_by_css_selector(message_selector)

        names = [name.text for name in author_names if not name in self.sent_author_names]
        # 絵文字消す
        chats = [''.join(c for c in chat.text if not c in emoji.UNICODE_EMOJI) 
                    for chat in messages if not chat in self.sent_messages]

        self.sent_author_names  = author_names
        self.sent_messages      = messages

        # ['ユーザ名', 'チャット']でリストつくる
        get_chats = [[name, chat] for name, chat in zip(names, chats) if name != '' and chat != '']

        return get_chats

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    getter = Chat_getter('https://www.youtube.com/live_chat?is_popout=1&v=Sflq-_arjDg')

    print(getter.get_chats())

    getter.quit()