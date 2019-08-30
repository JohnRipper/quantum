from lib.cog import Cog
from lib.command import makeCommand, Command


class Debug(Cog):

    @makeCommand(name="people", description="get the current userlist")
    async def people(self,  c: Command):
        await self.bot.send_message(self.bot.accounts.__str__())

    @makeCommand(name="reload", description="<cog_name> reloads a cog")
    async def reload(self,  c: Command):
        self.bot.remove_cog(c.message.rstrip())
        self.bot.add_cog(c.message.rstrip())
        self.logger.debug(f"Reloaded module: {c.message.rstrip()}")
        await self.bot.send_message(f"Reloaded module: {c.message.rstrip()}")
