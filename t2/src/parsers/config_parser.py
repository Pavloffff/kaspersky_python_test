import json


def load_config(file_path) -> dict:
    with open(file_path, 'r') as file:
        return json.load(file)


def save_config(config, file_path) -> None:
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)
