from lib.account import Role
from lib.cog import Cog
from lib.command import Command, makeCommand


class Template(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        # do something

    #############################
    # Class methods
    #############################
    def add(self, num1: int, num2: int):
        self.logger.info(f"Adding {num1} + {num2}")
        return num1 + num2

    def reverse_string(self, message: str):
        reverse = message[::-1]
        self.logger.info(f"Reverse {message}:{reverse}")

        return reverse
    #############################
    # Commands
    #############################
    @makeCommand(name="whereami", description="displays the room name and url. )")
    async def whereami(self, c: Command):
        # refer too default.toml
        room_name = self.bot.settings["room_name"]

        # module level settings.
        string_example = self.settings["string_example"]
        string = f"{room_name} \n {string_example}"
        await self.send_message(string)

    @makeCommand(name="echo", description="<message> echos a message)")
    async def echo(self, c: Command):
        # how to access the raw data from webocket
        # print(c.raw_data)
        # how to use logger
        self.logger.info(f"Echo: {c.message}")
        # how to send a message
        await self.send_message(f"Echo {c.message}")

    @makeCommand(name="amiop", description="<cog_name> reloads a cog", restrict_to=Role.OP)
    async def amiop(self, c: Command):
        # Will not execute if not op.
        await self.send_message(f"Yes have access sir. you are {c.account.role[0]}.")

    @makeCommand(name="reverse", description="<message> reverses a message")
    async def reverse(self, c: Command):
        rm = self.reverse_string(c.message)
        if rm:
            await self.send_message(f"{rm}")

    #############################
    # Events
    #############################
    # You may delete what you are not going to use.

    async def closed(self, data):
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
        # - cannot be ignored.( u must send ice command and offer first)
        #   incomplete cam process will disconnect websocket
        # - set to remote description

        return
