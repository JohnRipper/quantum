from lib.account import Account
from lib.constants import Role


def makeCommand(name: str, description: str, role: (str, int) = Role.GUEST, cls=None, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f._command = True
        f._name = name
        f._description = description
        f.role = role
        return f
    return wrap


class Command:
    def __init__(self, prefix: str, data, sender: str, account: Account):
        self.raw_data = data

        # requires a trailing space to prevent split from breaking on empty message field.
        self.command, self.message = f'{data["text"]}{" "}'.split(' ', 1)
        # clean up the trailing spaces.
        self.message = self.message.strip()

        self.prefix = self.command[0]
        self.command = self.command[1:]
        self.account = account
        # depreciating in favor of lib.account.Account
        self.sender = sender
