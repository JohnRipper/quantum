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
    def __init__(self, prefix: str, data, sender: str, account: Account):
        self.raw_data = data
        self.command, self.message = f'{data["text"]}{" "}'.split(' ', 1)
        self.prefix = self.command[0]
        self.command = self.command[1:]
        self.account = account
        # depreciating in favor of lib.account.Account
        self.sender = sender
