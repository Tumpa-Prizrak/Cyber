import discord
import sqlite3
from random import randint
import json
import requests
from Cogs import config as c
from discord.ext import commands
conn = sqlite3.connect("mydb.db")
curor = conn.cursor()


class ReactionsCommand(commands.Cog):
    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(ReactionsCommand(client))
