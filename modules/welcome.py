from lib.cog import Cog


class Welcome(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.room_name = self.bot.settings["room"]["room_name"]
        self.welcome_message = self.settings["message"]

    async def joined(self, data):
        if self.settings["self_message"]:
            if data["self"]["owner"]:
                await self.send_message("I am the boss and im back")
            else:
                message = f"Hello everybody I am back. {data['self']['handle']}"
                await self.send_message(message)

    # todo terrible.
    async def join(self, data):
        if data["owner"]:
            await self.send_message("Welcome back boss")
        else:
            message = self.welcome_message
            if len(message) >= 1:
                message = message.format(**data)
                if "{room}" in message:
                    message = message.format(room=self.room_name)
                    await self.send_message(message)
            else:
                pass

    async def quit(self, data):
        # username = self.bot.handle_to_name["handle"]
        # self.send_message("{username}has left the building")
        return
