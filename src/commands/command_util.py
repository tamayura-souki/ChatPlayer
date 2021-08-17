from typing import Any

def get_command(config:dict[str, Any]) -> str:
    """
    設定からコマンド名を取り出す関数
    """
    command = str(config.get("command", ""))
    if not command:
        Exception("command not found")
    return command

def normalize_color(color):
    def norm_one(c):
        c = c if c >= 0 else 0
        return c if c <= 255 else 255

    return [norm_one(c) for c in color]