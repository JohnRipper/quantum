
from lib.cog import Cog
import json

from lib.command import makeCommand, Command
from lib.utils import get_decorators

class Log(Cog):
    async def pvtmsg(self, data: dict):
        return None

    @makeCommand(name='test' , description='test')
    async def test(self, c: Command):
        print("test works")
        await self.bot.send_message('test works')
        return

    @makeCommand(name='test' , description='test')
    async def alsotest(self, c: Command):
        print(c.name)
        self.bot.send_message('test works')
        return

