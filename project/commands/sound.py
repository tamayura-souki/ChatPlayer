from . import logger
from . import PygameSoundRender

from .command import Command
from .command_util import *


class Sound(Command):
    def __init__(self, commands, **kwargs):
        super().__init__(**kwargs)

        self.sound_commands = {}
        for sc in commands:
            try:
                command = get_command(sc)
                render  = PygameSoundRender(
                    str(sc["path"]),
                    float(sc["volume"])
                )
                self.sound_commands[command] = render

            except:
                logger.warning("loading skip a sound command")
                continue

    def process_comment(self, text):
        text = text[1]

        for command, render in self.sound_commands.items():
            if command not in text:
                continue
            return render

        return None