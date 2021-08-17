from . import logger
from . import PygameStrRender, GroupRender

from .command import Command, CommentData
from .command_util import *

import random as rnd

class Rain(Command):
    def __init__(self, screen_size, commands, n_per_s=30.0, **kwargs):
        super().__init__(**kwargs)
        self.screen_size = screen_size

        self.rain_commands = {}
        for c in commands:
            try:
                command = get_command(c)
                time = float(c["time"])
                if time <= 0:
                    raise Exception

                n = int(time * n_per_s)
                interval = 1.0 / n_per_s

                v0 = float(c["v0"])
                a  = float(c["accel"])
                if v0 == 0 and a == 0:
                    raise Exception

                drops = str(c["drops"])
                font_color = normalize_color(c["color"])

                renders = [
                    PygameStrRender.font.render(d, False, font_color)
                    for d in drops
                ]

                self.rain_commands[command] = [n, interval, v0, a, renders]

            except:
                logger.warning("loading skip a rain command")
                continue

    def process_comment(self, comment:CommentData):
        text = comment.message

        def get_render():
            r   = rnd.choice(values[4])
            pos = [ float(rnd.randrange(0,self.screen_size[0])),
                    float(-r.get_height())]
            return PygameStrRender(
                render = r,
                pos    = pos,
                v      = [0.0,values[2]],
                a      = [0.0,values[3]]
            )

        for command, values in self.rain_commands.items():
            if command not in text:
                continue

            return GroupRender(
                values[1],
                [get_render() for _ in range(values[0])]
            )

        return None