import re
import requests

from lib.cog import Cog
from lib.command import makeCommand, Command
import asyncio


class Tokes(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    @makeCommand(name="tokes", description="<int> calls for tokes")
    async def tokes(self, c: Command):
        if c.message.isdigit():
            total_seconds = int(c.message)
            minutes = int(total_seconds / 60)
            seconds = int(total_seconds % 60)
            # starting message
            if minutes != 0:
                await self.send_message(
                    f"{c.account.username} is calling for tokes in {minutes} minutes {seconds} seconds!")
            else:
                await self.send_message(f"{c.account.username} is calling for tokes in {seconds}!")
            # start counting down.
            for i in range(0, minutes):
                await asyncio.sleep(60)
                if minutes - i <= 5 & minutes - i != 0:
                    await self.send_message(f"{minutes} left before tokes. called by {c.account.nick}")
            await asyncio.sleep(seconds)
            await self.send_message(f"Time for tokes! called by {c.account.username}")
        else:
            await self.send_message(f"Time for tokes! called by {c.account.username}")
