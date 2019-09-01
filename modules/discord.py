import requests

from lib.cog import Cog


class Discord(Cog):

    def __init__(self, bot):
        super().__init__(bot)

    async def send_discord(self, data):
        headers = {"Authorization": "Bot {}".format(self.bot.settings["discord"]["channel"]),
                   "Content-Type": "application/x-www-form-urlencoded"}
        requests.post(url="https://discordapp.com/api/v6/channels/{}/messages%".format(self.discord_channel),
                      headers=headers,
                      data={"content": data})

    async def join(self, data):
        await self.send_discord(
            "{} has joined the room with account: {}".format(
                data["nick"],
                data["username"]))
