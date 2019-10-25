from lib.cog import Cog
from lib.command import Command, makeCommand

import wikipedia


class Wikipedia(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["wikipedia"]

    @makeCommand(name="wiki", description="query|none return a wikipedia summary")
    async def wiki(self, c: Command):
        wikipedia.set_lang(self.settings["language"])
        sentences = self.settings["sentences"]
        query = c.message
        if len(query) == 0:
            query = wikipedia.random(pages=1)
        try:
            page = wikipedia.page(query)
            summary = wikipedia.summary(query, sentences=sentences)
        except wikipedia.exceptions.PageError as err:
            msg = err
        else:
            if self.settings["url"] is True:
                msg = "{}\n{}".format(summary, page.url)
            else:
                msg = summary
        await self.send_message(msg)

