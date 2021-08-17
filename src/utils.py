import json

def load_json(path):
    return json.load(open(path, 'r', encoding='utf-8', errors='ignore'))

def save_json(path, dict_data):
    return json.dump( dict_data,
        open(path, "w", encoding='utf-8', errors='ignore'),
        ensure_ascii=False,
        indent=4,
        separators=(',', ': ')
    )