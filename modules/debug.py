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
        # Not working, use reload.
        module = c.message.rstrip()
        if module in self.bot.modules:
            await self.send_message("Already loaded")
            return
        self.bot.remove_cog(module)
        botmsg = f"Reloaded module: {module}"
        self.logger.debug(botmsg)
        await self.send_message(botmsg)

    @makeCommand(name="unload", description="<cog_name> reloads a cog")
    async def unload(self, c: Command):
        # Not working, use reload.
        module = c.message.rstrip()
        if module not in self.bot.modules:
            await self.send_message(f"{module} cannot be unloaded")
            return
        self.bot.add_cog(module)
        self.logger.debug(f"unloaded module: {module}")
        await self.send_message(f"unloaded module: {module}")

    @makeCommand(name="modules", description="prints a list of modules")
    async def modules(self, c: Command):
        await self.send_message(str(self.bot.settings["bot"]["modules"]))
