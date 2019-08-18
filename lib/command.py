def makeCommand(name, description, cls=None, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f._command = True
        return f
    return wrap


class Command:
    def __init__(self, data):
        self.raw_data = data
        self.command, self.message = f'{data["text"]}{" "}'.split(' ', 1)
        self.command = self.command[1:]






