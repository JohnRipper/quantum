from python_anticaptcha import NoCaptchaTaskProxylessTask, AnticatpchaException, AnticaptchaClient

from lib.cog import Cog
import json

from lib.command import makeCommand, Command


class Debug(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @makeCommand(name="people", description="get the current userlist")
    async def people(self,  c: Command):
        await self.bot.send_message(self.bot.accounts.__str__())

    @makeCommand(name="reload", description="<cog_name> reloads a cog")
    async def reload(self,  c: Command):
        self.bot.remove_cog(c.message)
        self.bot.add_cog(c.message)
        await self.bot.send_message(f"reloaded {c.message} Cog")
