# -*- coding: utf-8 -*-

# スパチャの命令をstream labs に送るやつ

import json
import time
import asyncio
import requests

import os
from os.path import join, dirname
from dotenv import load_dotenv

class SuperChatAir:
    def __init__(self):
        self.tokens_path = "tokens.json"

        # APIキーとか読み込む
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        try:
            with open(self.tokens_path, mode='r') as f:
                self.tokens = json.load(f)

        except:
            self.tokens = {}

    def send_alert(self, token,  price:str, user:str, messageText:str):
        return requests.post('https://streamlabs.com/api/v1.0/alerts', {
            "access_token": token,
            "type": "donation",
            "message": "SuperChat Air<br><span>{}</span> by <span>{}</span>".format(price, user),
            "user_message": messageText or " ",
            "duration": 5000,
            "special_text_color": "Orange"
        })

    def super_chat(self, user:str, price:str, message:str):
        try:
            self.send_alert(self.tokens["access_token"], price, user, message)
        
        except Exception as e:
            data = {
                "client_id": os.environ.get("CLIENT_ID"),
                "client_secret":os.environ.get("CLIENT_SECRET"),
                "redirect_uri":os.environ.get("REDIRECT_URI")
            }
            if "refresh_token" in self.tokens.keys():
                data["grant_type"] = "refresh_token"
                data["refresh_token"] = self.tokens["refresh_token"]
            else:
                data["grant_type"] = "authorization_code"
                data["code"]       = os.environ.get("CODE")

            self.tokens = requests.post('https://streamlabs.com/api/v1.0/token',data).json()
            with open(self.tokens_path, mode='w', encoding='utf-8') as f:
                json.dump(self.tokens, f)

            self.send_alert(self.tokens["access_token"], price, user, message)



if __name__ == "__main__":
    sa = SuperChatAir()
    sa.super_chat("珠響そうき", "5000兆円", "あばばばばば")