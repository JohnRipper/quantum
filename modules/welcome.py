from python_anticaptcha import NoCaptchaTaskProxylessTask, AnticatpchaException, AnticaptchaClient

from lib.cog import Cog
import json

from lib.command import makeCommand, Command


class Welcome(Cog):
    def __init__(self, bot):
        super().__init__(bot)

    async def joined(self, data):
        # {"achievement_url":"","avatar": ""
        # ,"featured":false,
        # "giftpoints":0,"handle":2704504,
        # "lurker":false,"mod":false,"nick":"j"
        # ,"owner":false,"session_id":"6a66866"
        # ,"subscription":0,"username":""}
        if data["owner"]:
            self.bot.send_message("Welcome back boss")
        else:
            message = str(self.bot.settings["welcome_message"])
            message = message.replace("{nick}", data["nick"])
            message = message.replace("{username}", data["username"])
            message = message.replace("{id}", data["handle"])
            message = message.replace("{nick}", data["nick"])
            self.bot.send_message(message)

    async def quit(self, data):
        # self.bot.send_message("has left the building")
        return
