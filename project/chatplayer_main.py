import sys
import traceback

from pytchat import LiveChat

from config import logger
from draw import PygameWindow, get_quit_event, get_test_event
from ChatPlayer import ChatPlayer

def main(config, chat_config_path):
    try:
        chat_id = str(config["chat_id"])
        pg_window = PygameWindow(
            window_size = config["window_size"],
            bg_color = config["background_color"]
        )
    except KeyError or TypeError:
        logger.error("Error invalid config.json format")
        sys.exit(-1)

    chat_player = ChatPlayer(pg_window, chat_config_path)
    def process_comment(data):
        for c in data.items:
            chat_player.process_comment([c.author.name, c.message])
            data.tick()

    try:
        chat_getter = LiveChat(chat_id, callback=process_comment)

    except:
        logger.error("Error during LiveChat initialize")
        traceback.print_exc()
        pg_window.quit()
        return True

    @pg_window.main
    def loop():
        if not chat_getter.is_alive() or get_quit_event():
            chat_getter.terminate()
            pg_window.quit()
            sys.exit(0)

        chat_player.test(get_test_event())

    while True:
        loop()


if __name__ == "__main__":
    from utils import load_json

    config = load_json("config.json")
    main(config, "chat_config.json")