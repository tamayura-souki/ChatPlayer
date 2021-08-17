from config_main import main as config_main
from chatplayer_main import main as chatplayer_main

if __name__ == "__main__":
    while True:
        config = config_main("config.json")
        if not chatplayer_main(config, "chat_config.json"):
            break