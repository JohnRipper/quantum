import re
import requests

from lib.cog import Cog
from lib.command import makeCommand, Command


class Urban(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.base_url = "http://api.urbandictionary.com/v0/define?term={}"

    @makeCommand(name="urb", description= "<query> search urban dictionary")
    async def urb(self, c: Command):
        if len(c.message) >= 3:
            res = await self.urban_search(c.message)
            if res != None:
                await self.send_message("{term} — {definition}".format(**res))
            else:
                await self.send_message("Couldn't find that m8")

    async def urban_search(self, term):
        # TODO blacklist or handle toxic respones, see: "spam"
        query = requests.utils.quote(term)
        r = requests.get(self.base_url.format(query))
        if r.status_code == 200:
            try:
                # NANI?!
                _definition = r.json()["list"][0]["definition"].strip().replace("  ", " ")
                definition = re.sub(r"\[*\]*", "", _definition)
                return {"term": term, "definition": definition}
            except (IndexError, KeyError) as error:
                return None

