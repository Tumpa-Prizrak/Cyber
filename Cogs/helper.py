import json

class params:
    def __init__(self, filename: str) -> None:
        g = json.load(open(filename))
        self.token = g["token"]
        self.prefix = g["prefix"]
        self.owners = g['owners']
        self.apikey = g['apikey']
        self.limit = g['limit']
