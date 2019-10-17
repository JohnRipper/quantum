from lib.qlogging import QuantumLogger
import json
from lib.constants import SocketEvents


class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = QuantumLogger(self.name)
        self.bot = bot

    #############################
    # Helper methods
    #############################
    async def send_message(self, message: str):
        await self.bot.send_message(message)

    async def send_private_message(self, message: str):
        await self.bot.send_private(message)

    async def send_ws(self, data: dict):
        await self.bot.wsend(json.dumps(data))

    def get_req(self):
        return self.bot.get_req()

    async def do_ban(self, username):
        # look at ban command, does it use handle or username?
        return

    async def do_kick(self, username):
        return

    async def change_nick(self, nickname: str):
        data = {"nick": nickname,
                "req": self.get_req(),
                "tc": SocketEvents.NICK}
        return self.send_ws(data)

    async def get_account(self, handle):
        return self.bot.accounts[handle]

    #############################
    # Events
    #############################

    async def closed(self, data):
        # tc closed the connnection
        return

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

    async def yut_pause(self, data):
        # Youtube video paused

        # data example
        # {"handle": 3468338,
        #  "item": {"duration": 315,
        #           "id": "B-oU2xlViRQ",
        #           "image": "",
        #           "offset": 77.243339538574219,
        #           "playlist": False,
        #           "title": "Megadeth - Hangar 18 (HD) — [MegaHermansen]"}, "req": 425,
        #  "success": True, "tc": "yut_pause"}
        return

    async def yut_play(self, data):
        # youtube has been played, or seeked

        # data examples

        # play
        # {"handle": 3468338,
        #  "item": {"duration": 315,
        #           "id": "B-oU2xlViRQ",
        #           "image": "",
        #           "offset": 31.102100372314453,
        #           "playlist": False,
        #           "title": "Megadeth - Hangar 18 (HD) — [MegaHermansen]"},
        #  "req": 422,
        #  "success": True,
        #  "tc": "yut_play"}

        #  seek
        # {"tc": "yut_play",
        #  "req": 426,
        #  "item": {"id": "B-oU2xlViRQ",
        #           "duration": 311.021,
        #           "offset": 77.24333953857422,
        #           "seek": True}}
        return

    async def nick(self, data):
        # nickname changed for specified user.

        # data example

        # {"handle": 3468338,
        #  "nick": "_johan_muted",
        #  "req": 484,
        #  "success": True,
        #  "tc": "nick"}
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
