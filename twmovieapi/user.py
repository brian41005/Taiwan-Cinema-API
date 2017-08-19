import json


class User(object):
    def __init__(self, name='config.json'):
        with open(name) as f:
            config = json.load(f)
            for k, v in config.items():
                setattr(self, k, v)
