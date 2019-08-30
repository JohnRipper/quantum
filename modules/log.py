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

    #############################
    # websocket events
    #############################
    async def userlist(self, data):
        self.logger.info(data)

    async def join(self, data):
        self.logger.info(data)

    async def quit(self, data):
        self.logger.info(data)

    async def ping(self, data):
        # NO
        # self.logger.debug(data)
        return

    async def yut_stop(self, data):
        self.logger.info(data)

    async def msg(self, data):
        self.logger.chat(data)

    async def captcha(self, data: dict):
        self.logger.info(data)

    async def pvtmsg(self, data):
        self.logger.info(data)

    async def publish(self, data):
        self.logger.info(data)

    async def unpublish(self, data):
        self.logger.info(data)

    async def iceservers(self, data):
        self.logger.info(data)

    async def stream_connected(self, data):
        self.logger.info(data)

    async def stream_closed(self, data):
        self.logger.info(data)

    async def sdp(self, data):
        self.logger.info(data)

    async def closed(self, data):
        self.logger.info(data)
