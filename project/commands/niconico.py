from . import logger
from . import PygameStrRender, PygameWindow

from .command import Command
from .command_util import *

class NicoNico(Command):
    def __init__(self, screen_size, **kwargs):
        super().__init__(**kwargs)

        # ニコニココマンド全体の設定
        self.screen_size = screen_size
        self.line_n = kwargs.get("line_n", 12)
        self.now_line = 0
        self.speed  = kwargs.get("speed",  4)

        self.default_color = {
            "font_color":[255,255,255],
            "outline_color":[0,0,0]
        }
        try:
            dc = kwargs["default_color"]
            fc = normalize_color(dc["font_color"])
            oc = normalize_color(oc["outline_color"])
            self.default_color = {"font_color":fc, "outline_color":oc}
        except:
            pass

        # 匿名化コマンド
        try:
            self.unk_command = str(kwargs["unkown_command"])
            if not self.unk_command:
                raise Exception
        except:
            self.unk_command = "/unk"
            logger.info(f"set unkown command is {self.unk_command}")

        # 文字速度コマンド読み込み
        self.speed_commands = {}
        speed_commands = kwargs.get("speed_commands", [])
        for sc in speed_commands:
            try:
                command = get_command(sc)

                speed   = float(sc["speed"])
                if not speed:
                    logger.warning(f"{command} cannot have speed 0")
                    raise Exception

                self.speed_commands[command]

            except:
                logger.warning("loading skip a speed command")
                continue

        # 文字色コマンド読み込み
        self.color_commands = {}
        color_commands = kwargs.get("color_commands", [])
        for cc in color_commands:
            try:
                command = get_command(cc)
                font_color = normalize_color(cc["font_color"])
                outline_color = normalize_color(cc["outline_color"])

                self.color_commands[command] = [font_color, outline_color]

            except:
                logger.warning("loading skip a color command")
                continue

    def process_comment(self, text):

        name = text[0] + " : "
        text = text[1]
        text_len = len(text)
        speed = self.speed
        color = self.default_color["font_color"]
        outline_color = self.default_color["outline_color"]

        # command find func

        # 速度系コマンドの処理
        for command, speed_ratio in self.speed_commands.items():
            text = text.replace(command, "")
            if len(text) != text_len:
                speed *= speed_ratio
                text_len = len(text)
                break

        # チャット色系のコマンドを処理
        for command, changed_color in self.color_commands.items():
            text = text.replace(command, "")
            if len(text) != text_len:
                color = changed_color[0]
                outline_color = changed_color[1]
                text_len = len(text)
                break

        # 匿名化
        text = text.replace(self.unk_command, "")
        if len(text) != text_len:
            name = ""
            text_len = len(text)

        render = PygameStrRender(
            name+text,
            color=color,
            outline_color=outline_color
        )

        render.v[0] = -speed
        render.pos[0] = self.screen_size[0]
        render.pos[1] = self.screen_size[1] / self.line_n * self.now_line

        self.now_line += 1
        if self.now_line >= self.line_n:
            self.now_line = 0

        return render