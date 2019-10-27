from lib.qlogging import QuantumLogger
import json
from lib.constants import SocketEvents


class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = QuantumLogger(self.name)
        self.bot = bot

        # see default.toml for available settings.
        self.settings = bot.settings

        # list of references to @makeCommand methods
        self.methods = [getattr(self, name)  # what gets stored.
                        for name in dir(self)  # loop
                        if "__" not in name  # ignore builtins
                        and callable(getattr(self, name))  # is callable
                        and hasattr(getattr(self, name), "command")  # @makeCommand used
                        ]

    #############################
    # Helper methods
    #############################

    async def send_message(self, message: str, clean: bool = True, limit: int = 0):
        await self.bot.send_message(message, clean=clean)

    async def send_private_message(self, message: str):
        await self.bot.send_private(message)

    async def send_ws(self, data: dict):
        await self.bot.wsend(json.dumps(data))

    def get_req(self):
        # bot side request counter.
        return self.bot.get_req()

    async def do_ban_by_id(self, handle: int):
        data = {"tc": "ban", "req": 420, "handle": handle}
        await self.send_ws(data=data)

    async def do_ban_by_username(self, username: str):
        await self.do_ban_by_id(self.bot.username_to_handle(username))

    async def get_banlist(self):
        # asks the bot to trigger then banlist event.
        # Recomended use is to create a flag in your cogs __init__ that you triggered the banlist event
        # Then override the banlist event with the flag in mind.
        data = {"tc": "banlist", "req": self.get_req()}
        await self.send_ws(data=data)

    async def do_kick_by_id(self, handle_id: int):
        data = {"tc": "kick", "req": self.get_req(), "handle": handle_id}
        await self.send_ws(data=data)

    async def do_kick_by_username(self, username: str):
        await self.do_kick_by_id(self.bot.username_to_handle(username))

    async def change_nick(self, nickname: str):
        if nickname or nickname != "":
            data = {"nick": nickname,
                    "req": self.get_req(),
                    "tc": SocketEvents.NICK}
            await self.send_ws(data)
        else:
            await self.send_message("invalid nickname")

    async def get_account(self, handle):
        return self.bot.accounts[handle]

    #############################
    # Events
    #############################
    async def sysmsg(self, data):
        return

    async def banlist(self, data):
        # gets the current ban list.
        return

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
