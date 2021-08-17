def get_command(config):
    command = str(config.get("command", ""))
    if not command:
        Exception
    return command

def normalize_color(color):
    def norm_one(c):
        c = c if c >= 0 else 0
        return c if c <= 255 else 255

    return [norm_one(c) for c in color]