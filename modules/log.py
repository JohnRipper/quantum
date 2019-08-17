from lib.cog import Cog
import json

class Log(Cog):

    async def on_message(self, data: dict):
        print(f"{data['author']['id']}:{self.bot.user_id}")
