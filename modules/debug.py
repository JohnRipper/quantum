from lib.cog import Cog
from lib.command import Command, makeCommand


class Debug(Cog):

    #############################
    # Commands
    #############################
    @makeCommand(name="people", description="get the current userlist")
    async def people(self,  c: Command):
        await self.bot.send_message(self.bot.accounts.__str__())

    @makeCommand(name="reload", description="<cog_name> reloads a cog")
    async def reload(self,  c: Command):
        module = c.message.rstrip()
        self.bot.remove_cog(module)
        self.bot.load_module(module)
        self.bot.add_cog(module)
        self.logger.debug(f"Reloaded module: {module}")
        await self.send_message(f"Reloaded module: {module}")

    @makeCommand(name="load", description="<cog_name> reloads a cog")
    async def load(self, c: Command):
        module = self.bot.load_module(c.message)
        self.bot.add_cog(c.message)
        botmsg = f"loaded module: {module}"
        self.logger.debug(botmsg)
        await self.send_message(botmsg)

    @makeCommand(name="unload", description="<cog_name> reloads a cog")
    async def unload(self, c: Command):
        # Not working, use reload.
        module = self.bot.load_module(c.message)
        if module in self.bot.modules:
            self.bot.modules.remove(module)
            self.bot.remove_cog(c.message)
            self.logger.debug(f"unloaded module: {module}")
            await self.send_message(f"unloaded module: {module}")

    @makeCommand(name="modules", description="prints a list of modules")
    async def modules(self, c: Command):
        await self.send_message(str(self.bot.modules))

    @makeCommand(name="cogs", description="prints a list of modules")
    async def cogs(self, c: Command):
        await self.send_message(str(self.bot.cogs.__repr__()))
