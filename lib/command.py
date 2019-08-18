def makeCommand(name, description, cls=None, **attrs):
    def wrap(f):
        if isinstance(f, Command):
            raise TypeError('Callback is already a command.')
        f._command = True
        f._name = name
        f._description = description
        return f
    return wrap


class Command:
    def __init__(self, data):
        self.raw_data = data
        self.command, self.message = f'{data["text"]}{" "}'.split(' ', 1)
        self.command = self.command[1:]






