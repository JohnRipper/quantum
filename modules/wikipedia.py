import re

import wikipedia

from lib.cog import Cog
from lib.command import Command, makeCommand


class Wikipedia(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["wikipedia"]
        self.searches = []

    @makeCommand(name="wiki", description="query|none return a wikipedia summary")
    async def wiki(self, c: Command):
        wikipedia.set_lang(self.settings["language"])
        sentences = self.settings["sentences"]
        query = c.message
        # expected response for choosing a topic from `self.searches`
        if len(query) == 1 and query.isdigit():
            query = self.searches[int(query)]
        elif len(query) == 0:
            query = wikipedia.random(pages=1)
        try:
            page = wikipedia.page(query)
            summary =  wikipedia.summary(query, sentences=sentences)
        except wikipedia.exceptions.PageError as err:
            await self.send_message("PageError, FIXME")
        except wikipedia.exceptions.DisambiguationError as err:
            self.searches = err.options[:10]
            # iterate over self.searches to create a formated string,
            # ie "0) List Index 0\n1) List Index 1" etc
            fmtd = "\n".join([str(i)+") "+m for i,m in enumerate(self.searches)])
            await self.send_message("Select one with \"wiki #\"\n{}".format(fmtd), clean=False)
        else:
            url = page.url
            # wikipedia lib reformats headings? yuck.
            summary = re.sub("==.+==", " ", summary)
            summary = re.sub("\n", "", summary)
            # TODO maybe pull this limit from the settings
            await self.send_message("{}\n{}".format(url,summary), clean=False, limit=1)
