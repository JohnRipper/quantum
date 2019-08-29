import logging

from lib.qlogging import QuantumLogger


class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = QuantumLogger(self.name)
        self.bot = bot
        self.commands = []

    async def userlist(self, data):
        # on room join, userlist is sent. dunno if sent other times.
        return

    async def join(self, data):
        # info on the room you just joined
        return

    async def joined(self, data):
        # someone joined
        return

    async def quit(self, data):
        # quit event?
        return

    async def ping(self, data):
        # heartbeat, marco /polo, ping/pong,  ect.
        return

    async def yut_stop(self, data):
        # youtube has been closed
        return

    async def yut_start(self, data):
        # youtube has been started
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
        # ice servers have been retrieved
        return

    async def publish(self, data):
        # received after subscribing to someone through ws
        return

    async def unpublish(self, data):
        return

    async def stream_connected(self, data):
        # tc thinks the connection process completed.
        return

    async def stream_closed(self, data):
        # received after subscribing to someone
        return

    async def sdp(self, data):
        # sdp comes in two types

        # offer:
        # - Someone else trying to cam
        # - can be ignored
        # - if used, set to remote_description
        #   then create/send local_description as answer

        # answer:
        # - a response to your own offer.
        # - cannot be ignored.
        #   incomplete cam process will disconnect ws
        # - set to remote description

        return

