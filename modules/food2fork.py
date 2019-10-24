import random
import requests

from lib.cog import Cog
from lib.command import makeCommand, Command


class Food2fork(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["food2fork"]
        self.base_url = "https://food2fork.com/api/search?key={apikey}&q={search}"


    @makeCommand(name="food", description="<query> return random recipe related to the search")
    async def food(self, c: Command):
        if len(c.message) >= 3:
            res = await self.food_search(c.message)
            if res != None:
                await self.send_message("{} {} ({}/{})".format(*res[0]))
            else:
                await self.send_message("Couldn't find anything for {}".format(c.message))

    async def food_search(self, search):
        results = []
        search = requests.utils.quote(search)
        query = requests.get(
            self.base_url.format(apikey=self.settings["key"], search=search)
        )
        print(query)
        if query.status_code == 200:
            query = query.json()
            try:
                total = len(query["recipes"])
                num = random.randint(0, total)
                results.append([
                    query["recipes"][num]["title"],
                    query["recipes"][num]["f2f_url"],
                    num,
                    total
                ])
                return results
            except (IndexError, KeyError) as error:
                self.bot.log.warning(error)
