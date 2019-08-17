import logging


class Cog:

    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot

    async def userlist(self, data):
        return

    async def join(self, data):
        return

    async def quit(self, data):
        return

    async def ping(self, data):
        return

    async def yut_stop(self, data):
        return

    async def msg(self, data):
        await self.process_message(data['text'], self.bot.accounts[data['handle']])

    async def captcha(self, data: dict):
        return

    # a simple message processor, doesnt matter which one you override with your cog. user preference.
    async def process_message(self, m, username):
        for prefix in self.bot.settings['prefixes']:
            if m.startswith(prefix):
                command, message = f'{m}{" "}'.split(' ', 1)
                command = command[1:]
                if command == 'eyes':
                    await self.bot.send_message('o.o 0.0 O.O o.O O.o O.0')
                if command == 'echo':
                    await self.bot.send_message(message)
                if command == 'yt':
                    await self.bot.play_youtube(message)
            # await self.send_discord({"{}:{}".format(username, m)})
