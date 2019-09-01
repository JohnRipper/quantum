from python_anticaptcha import NoCaptchaTaskProxylessTask, AnticatpchaException, AnticaptchaClient

from lib.cog import Cog
import json

from lib.command import makeCommand, Command


class Welcome(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    async def joined(self, data):
        if data["self"]["owner"]:
            await self.bot.send_message("I am the boss and im back")
        else:
            message = f"Hello everybody I am back. {data['self']['handle']}"
            await self.bot.send_message(message)

    async def join(self, data):
        if data["owner"]:
            await self.bot.send_message("Welcome back boss")
        else:
            message = self.bot.settings["bot"]["welcome_message"]
            if len(message) >= 1: # account for a blank space
                message = message.format(**data)
                if "{room}" in message:
                    message = message.format(room=self.bot.settings["room"]["roomname"])
                await self.bot.send_message(message)
            else:
                pass

    async def quit(self, data):
        # username = self.bot.handle_to_name["handle"]
        # self.bot.send_message("{username}has left the building")
        return
