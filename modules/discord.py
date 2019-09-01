import json

import requests
from lib.cog import Cog

# https://birdie0.github.io/discord-webhooks-guide/other/slack_formatting.html
WEBHOOK_FMT = {
    "username": "",
    "icon_url": "",
    "attachments": [{
        "text": "",
        "image_url": ""
    }]
}

# TODO add handling for needed values
class Discord(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self.discord = self.bot.settings["discord"]
        self.webhook_url = self.discord["webhook_url"]

    async def send_webhook(self, nick, username, avatar):
        msg = WEBHOOK_FMT
        if self.discord["include_avatar"] is False:
            avatar = None
        for key,_ in self.discord["bot"].items():
            # should be able to map this
            msg[key] = self.discord["bot"][key]
        # format the message from config
        tosend = self.discord["bot"]["message"].format(username=username, nick=nick)
        msg["attachments"][0]["text"] = tosend
        msg["attachements"][0]["image_url"] = avatar
        # people forget this shit all the time
        if "/slack" not in self.webhook_url:
            self.webhook_url += "/slack"
        requests.post(self.webhook_url, json.dumps(msg))

    async def send_discord(self, data):
        if len(self.discord["channel"]) > 0:
            headers = {"Authorization": "Bot {}".format(self.discord["channel"]),
                    "Content-Type": "application/x-www-form-urlencoded"}
            requests.post(url="https://discordapp.com/api/v6/channels/{}/messages%".format(self.discord_channel),
                        headers=headers,
                        data={"content": data})

    async def join(self, data):
        if self.discord["use_webhook"] is False:
            await self.send_discord(
                "{} has joined the room with account: {}".format(
                    data["nick"],
                    data["username"]))
        else:
            await self.send_webhook(
                nick=data["nick"],
                username=data["username"],
                avatar=data["avatar"]
            )

