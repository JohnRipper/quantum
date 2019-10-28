import datetime
from lib.cog import Cog
from lib.command import makeCommand, Command
import asyncio

from lib.constants import Role


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["tokes"]
        self.is_running_hourly = self.bot.settings["module"]["tokes"]["hourly_420"]
        # auto start?
        if self.settings["hourly_420"]:
            asyncio.create_task(self.it_is_420())

    async def it_is_420(self):
        while self.bot.is_running & self.is_running_hourly:
            minutes = datetime.datetime.now().strftime("%M")
            if minutes == ("20"):
                await self.send_message("it is 420 somewhere")
            await asyncio.sleep(60)
            pass

    @makeCommand(name="420hour", description="enables/disables call for tokes hourly. ", role=Role.MOD)
    async def hour420(self, c: Command):
        self.is_running_hourly = not self.is_running_hourly

    @makeCommand(name="timer", description="a seconds timer ", role=Role.GUEST)
    async def timer(self, c: Command):
        if c.message.isdigit():
            await self.send_message(f"{c.account.nick} Just set a timer set for {c.message}")
            await asyncio.sleep(int(c.message))
            await self.send_message(f"{c.account.nick}'s timer set for {c.message}")

    @makeCommand(name="tokes", description="<int> calls for tokes")
    async def tokes(self, c: Command):
        if c.message.isdigit():
            total_seconds = int(c.message)
            minutes = int(total_seconds / 60)
            seconds = int(total_seconds % 60)
            # starting message
            if minutes != 0:
                await self.send_message(
                    f"{c.account.nick} is calling for tokes in {minutes} minutes {seconds} seconds!")
            else:
                await self.send_message(f"{c.account.nick} is calling for tokes in {seconds}!")
            # start counting down.
            for i in range(0, minutes):
                await asyncio.sleep(60)
                if minutes - i <= 5 & minutes - i != 0:
                    await self.send_message(f"{minutes} left before tokes. called by {c.account.nick}")
            await asyncio.sleep(seconds)
            await self.send_message(f"Time for tokes! called by {c.account.nick}")
        else:
            await self.send_message(f"Time for tokes! called by {c.account.nick}")
