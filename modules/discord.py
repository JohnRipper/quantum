from python_anticaptcha import NoCaptchaTaskProxylessTask, AnticatpchaException, AnticaptchaClient

from lib.cog import Cog
import json

class Captcha(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.captcha_client = AnticaptchaClient(self.bot.settings['captcha_key'])

    async def send_discord(self, data):
        headers = {"Authorization": "Bot {}".format(self.discord_key),
                   "Content-Type": "application/x-www-form-urlencoded"}
        requests.post(url='https://discordapp.com/api/v6/channels/{}/messages'.format(self.discord_channel),
                      headers=headers,
                      data={'content': data})

    async def join(self, data):
        await self.send_discord(
            '{} has joined the room with account: {}'.format(
                data['nick'],
                data['username']))