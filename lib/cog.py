import logging



class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot
        self.commands = []

    async def userlist(self, data):
        return

    async def join(self, data):
        return

    async def quit(self, data):
        return

    async def ping(self, data):
        return

    async def yut_stop(self, data):
        return

    async def msg(self, data):
        return

    async def captcha(self, data: dict):
        return

    def pvtmsg(self,data):
        return




