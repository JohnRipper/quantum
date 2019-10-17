from lib.account import Account

def makeCommand(name, description, cls=None, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f._command = True
        f._name = name
        f._description = description
        return f
    return wrap


def restrictTo(role: (str, int), cls=None, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already an instance.')
        f.role = role
        return f
    return wrap


class Command:
    def __init__(self, data, bot, account: Account):
        self._bot = bot
        self.raw_data = data
        self.command, self.message = f'{data["text"]}{" "}'.split(' ', 1)
        self.prefix = self.command[0]
        self.command = self.command[1:]
        self.account = account
        # depreciating in favor of lib.Account.
        self.sender = bot.handle_to_name(data["handle"])

    async def send_message(self, message: str):
        await self._bot.send_message(message)

    def send_private_message(self, message: str):
        return
