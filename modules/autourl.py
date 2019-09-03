import re

import requests
from bs4 import BeautifulSoup as bs4

from lib.cog import Cog

class AutoUrl(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["autourl"]
        self.pattern = self.settings["pattern"]
        self.exclusion_char = self.settings["exclusion_char"]

    async def msg(self, data):
        msg = data["text"]
        match = re.findall(self.pattern, msg)
        # workaround for youtube playing
        print(self.settings["ignores"])
        if data["handle"] == self.bot.handle or re.match("\A.?play", msg):
            pass
        elif msg.startswith(self.exclusion_char) or len(match) == 0:
            pass
        else:
            if self.ignore_msg(match[0]) is False:
                await self.bot.send_message(await self.get_title(match[0]))

    def ignore_msg(self, msg):
        print(msg)
        if len(self.settings["ignores"]) >= 1:
            for ignore in self.settings["ignores"]:
                if bool(re.findall(ignore, msg)):
                    return True
            else:
                return False
        else:
            return False

    async def get_title(self, url):
        res = requests.get(url)
        soup = bs4(res.text, "html.parser")
        if soup != None:
            try:
                title = soup.title.string
            except AttributeError as error:
                self.bot.warning(erro)
            else:
                return title.strip()

