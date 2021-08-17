import sys
import re
import tkinter as tk

from config import logger
from utils import load_json, save_json

def main(config_path):
    config = load_json(config_path)

    root = tk.Tk()
    root.title("配信のURLを入力")
    root.geometry("200x50")

    def ok():
        config["chat_id"] = txt.get()
        if '/' in config["chat_id"]:
            config["chat_id"] = re.search(r"[\?\&]v=([^&]+)", config["chat_id"])
            if config["chat_id"] is None:
                logger.error("Invalid video id")
                return None

            config["chat_id"] = config["chat_id"].group(1)
        root.destroy()

    def end():
        root.destroy()
        sys.exit(0)

    lbl = tk.Label(text='URL')
    lbl.place(x=10, y=10)

    txt = tk.Entry()
    txt.place(x=40, y=10)
    txt.insert(tk.END, config["chat_id"])

    enter_btn = tk.Button(text="Ok", command=ok)
    enter_btn.place(x=170, y=5)

    root.protocol("WM_DELETE_WINDOW", end)
    root.mainloop()

    save_json(config_path, config)
    return config