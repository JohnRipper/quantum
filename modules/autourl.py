import re

import requests
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog

class AutoUrl(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.pattern = "http.\S+"
        self.exclusion_char = self.bot.settings["module"]["autourl"]["exclusion_char"]

    async def msg(self, data):
        msg = data["text"]
        match = re.findall(self.pattern, msg)
        if msg.startswith(self.exclusion_char) or len(match) == 0:
            pass
        else:
            res = requests.get(match[0])
            soup = bs4(requests.get(match[0]).text, "html.parser")
            if soup != None:
                # TODO maybe split at "/" to do like [URL Title] - site.url
                # maybe handle 404, meh
                try:
                    title = soup.title.string
                except AttributeError:
                    pass
                else:
                    await self.bot.send_message(f"[{soup.title.string}]")

