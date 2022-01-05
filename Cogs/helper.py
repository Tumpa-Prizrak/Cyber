import json
import nextcord

class params:
    def __init__(self, filename: str) -> None:
        g = json.load(open(filename))
        self.token = g["token"]
        self.prefix = g["prefix"]
        self.owners = g['owners']
        self.apikey = g['apikey']
        self.limit = g['limit']

def embed_builder(title: str, *, desc: str = None, color: nextcord.Colour = nextcord.Colour.green()): return nextcord.Embed(title=title, description=desc, color=color)