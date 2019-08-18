import logging



class Cog:
    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot
        self.commands = []


    async def check_commands(self):
        method_list = [func for func in dir(self) if callable(getattr(self, func))]
        print(method_list)
        for method in method_list:
            m = getattr(self, method)
            print(m.__name__)
            print(m.__dict__)
            if m.__name__ == 'test':
                print(m)
            if hasattr(m, 'test'):
                s = getattr(m, 'test')
                dir(s)
                print(s)

                # breaks here getting wrong  item because shit is wrapped
                print(getattr(s, '_command'))

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
        return

    async def captcha(self, data: dict):
        return

    def add_command(self, data:dict):
        self.commands.append(data)

    def pvtmsg(self,data):
        return




