import emoji

from config import logger
from utils import load_json
from draw import PygameStrRender, PygameWindow
from commands import NicoNico, Rain, Sound

class ChatPlayer:
    def __init__(self, pg_window:PygameWindow, config_path:str):
        self.pg_window = pg_window

        try:
            config = load_json(config_path)

            self.taboo_words = [str(c) for c in config["taboo_words"]]
            self.oo_words = [str(c) for c in config["oo_words"]]

            # コマンド系
            font_name = str(config["font"]["name"])
            font_size = int(config["font"]["size"])

            PygameStrRender.set_font(font_name, font_size)
            PygameStrRender.set_screen(self.pg_window.screen)

            nn = NicoNico(
                PygameStrRender.screen_size, **config["niconico_commands"]
            )
            rain = Rain(
                PygameStrRender.screen_size, config["rain_commands"]
            )
            sound = Sound(
                config["sound_commands"]
            )
            self.commands = [sound, rain, nn]

        except:
            logger.error("failed at loading chat config")
            return None

    def process_comment(self, comment:[str,str]):

        comment[0] = ''.join(c for c in comment[0] if not c in emoji.UNICODE_EMOJI)
        comment[1] = ''.join(c for c in comment[1] if not c in emoji.UNICODE_EMOJI)

        if not comment[1]:
            return False

        # taboo_word を含んだコメントを許すな
        for taboo in self.taboo_words:
            if taboo in comment[0] or taboo in comment[1]:
                return False

        # oo_word は伏せる
        for oo in self.oo_words:
            comment[0] = comment[0].replace(oo, "〇〇")
            comment[1] = comment[1].replace(oo, "〇〇")


        for command in self.commands:
            render = command.process_comment(comment)
            if render is not None:
                self.pg_window.add_render(render)
                return True

        return False