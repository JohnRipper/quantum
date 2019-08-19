from lib.cog import Cog
from lib.command import makeCommand, Command


class Log(Cog):

    #############################
    # Commands
    #############################
    @makeCommand(name='printlog' , description='<-c> <-d> creates a copy of a Chat/debug log ')
    async def log_to_pastebin(self, c: Command):
        # TODO
        if c.message.startswith("-c"):
            await self.bot.send_message('not implemented for chat logs yet')

        if c.message.startswith("-c"):
            await self.bot.send_message('not implemented for debug logs yet')
        return

    #############################
    # websocket events
    #############################
    # TODO make pretty.

    async def userlist(self, data):
        self.logger.info(data)
        return

    async def join(self, data):
        self.logger.info(data)
        return

    async def quit(self, data):
        self.logger.info(data)
        return

    async def ping(self, data):
        # NO
        # self.logger.debug(data)
        return

    async def yut_stop(self, data):
        self.logger.info(data)
        return

    async def msg(self, data):
        self.logger.info(data)
        return

    async def captcha(self, data: dict):
        self.logger.info(data)
        return

    def pvtmsg(self, data):
        self.logger.info(data)
        return

