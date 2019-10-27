from datetime import timedelta
import time

from lib.utils import get_latest_sha1
from lib.cog import Cog
from lib.command import makeCommand, Command

class Builtins(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        #self.settings = self.bot.settings["modules"]["builtins"]

    @makeCommand(name="uptime", description="return uptime")
    async def uptime(self, c: Command):
        start = round(self.bot.start_time)
        current = round(time.time())
        delta = timedelta(seconds=current - start)
        await self.send_message(str(delta))

    @makeCommand(name="version", description="return version")
    async def version(self, c: Command):
        current = self.bot.version
        head = get_latest_sha1()
        msg = f"Current: {current}\nLatest: {head}"
        await self.send_message(msg, clean=False)





