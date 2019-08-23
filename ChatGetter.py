# -*- coding: utf-8 -*-

# YoutubeChatで遊ぶためのコード
# Chat取得部分をつくる

import codecs
from selenium import webdriver

# 取得したコマンドコメント一覧と
# すでに持っているコマンドコメント一覧を比較して、
# 取得したコメントが、すでにある一覧にあれば、実行しない
# 実行済みのコメントが、取得コメントの中になければ、削除し、
# 再び実行出来るようにする。

class Chat_getter:
    def __init__(self, chat_url:str, not_chat=None):
        if not_chat == None:
            self.not_chat_list = ['上位チャット', 'チャット', '詳細', 'チャットへようこそ！ご自身のプライバシーを守るとともに、YouTube のコミュニティ ガイドラインを遵守することを忘れないでください。',
                                    'メッセージを入力...', '0/200']
        else:
            self.not_chat_list = not_chat

        self.url        = chat_url
        options         = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver     = webdriver.Chrome(options=options)
        self.sent_chat  = [['','']]

    def get_chats(self, chat_selector:str = 'yt-live-chat-renderer'):
        self.driver.get(self.url)

        # チャット欄のテキスト取得、チャット以外を消す
        elements  = self.driver.find_element_by_css_selector(chat_selector)
        words     = [e for e in elements.text.split('\n')]
        words     = [w for w in words if not w in self.not_chat_list]

        # ['ユーザ名', 'チャット']でリストつくる
        get_chats = [words[0::2], words[1::2]]
        get_chats = [list(c) for c in zip(*get_chats)]

        # 実行済みチャットからタイムアウトしたチャットを消す(再び使用可能に)
        self.sent_chat = [c for c in self.sent_chat if c in get_chats]

        # 実行済みチャット消す
        get_chats = [c for c in get_chats if not c in self.sent_chat]
        
        # listの重複消したい setじゃ二次元配列無理だった
        seen = []
        self.sent_chat = [x for x in (self.sent_chat+get_chats) if x not in seen and not seen.append(x)]

        return get_chats

    def quit(self):
        self.driver.quit()
#    def __del__(self):
#        self.driver.quit()

'''
getter = Chat_getter('https://www.youtube.com/live_chat?is_popout=1&v=Sflq-_arjDg')

def chat_get():
    return getter.get()

def quit():
    return getter.quit()




options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

print('start')

driver.get('https://www.youtube.com/live_chat?is_popout=1&v=Sflq-_arjDg')

for body in [driver.find_element_by_css_selector('yt-live-chat-renderer')]:
    print(type(body.text))
    print(body.text)

#print(codecs.encode(driver.page_source, 'utf-8', 'ignore'))

driver.save_screenshot('search_results.png')
driver.quit()
'''