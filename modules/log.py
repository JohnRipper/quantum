from lib.cog import Cog
from lib.command import makeCommand, Command

class Log(Cog):

    #############################
    # Commands
    #############################
    @makeCommand(name='printlog' , description='<-c> <-d> creates a copy of a Chat/debug log ')
    async def log_to_pastebin(self, c: Command):
        if c.message.startswith("-c"):

            await self.bot.send_message('not implemented for chat logs yet')

        if c.message.startswith("-d"):
            await self.bot.send_message('not implemented for debug logs yet')
        return
