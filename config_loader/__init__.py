import json


def load(json_src_path: str) -> map:
    with open(json_src_path) as json_src:
        return json.load(json_src)
