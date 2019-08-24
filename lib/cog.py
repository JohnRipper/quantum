import logging



class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot
        self.commands = []

    async def userlist(self, data):
        # on room join, userlist is sent. dunno if sent other times.
        return

    async def join(self, data):
        # info on the room you just joined
        return

    async def quit(self, data):
        # quit event?
        return

    async def ping(self, data):
        # heartbeat, marco /polo, ping/pong,  ect. event.
        return

    async def yut_stop(self, data):
        # youtube has been closed
        return

    async def msg(self, data):
        # general message
        return

    async def captcha(self, data: dict):
        # captcha required
        return

    async def pvtmsg(self, data):
        # private message
        return

    async def iceservers(self, data):
        return

    async def publish(self, data):
        # recieved after subscribing to someone
        return

    async def unpublish(self, data):
        return

    async def stream_connected(self, data):
        # recieved after subscribing to someone
        return

    async def stream_closed(self, data):
        # recieved after subscribing to someone
        return

    async def sdp(self, data):
        # recieved after subscribing to someone
        return

