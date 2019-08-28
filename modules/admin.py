from lib.cog import Cog
from lib.command import makeCommand, Command
from lib.constants import AppData


class Admin(Cog):

    @makeCommand(name='op', description='Remakes help file using file descriptions')
    async def make_help(self, c: Command):
        help = ""
        help.join("Quantum bot help file\n")
        help.join("\n")
        # TODO remake help file and post somewhere
        for module in self.bot.cogs:
            help.join(f"{module.__name__}\n")
            method_list = [func for func in dir(module) if callable(getattr(module, func))]
            for method in method_list:
                if hasattr(method, "_description"):
                    print(getattr(module, "_description"))
                    # todo get method name and aliases
                    help.join(f"{getattr(module, '_name')} - {getattr(module, '_description')}\n")

    @makeCommand(name='op', description='<account_name> makes op')
    async def make_op(self, c: Command):
        # TODO
        return

    @makeCommand(name='check_op', description='<account_name> check if has op status')
    async def check_op(self, c: Command):
        # TODO
        return

    @makeCommand(name='ban', description='<account> attempts to ban')
    async def make_ban_account(self, c: Command):
        # TODO
        return

    @makeCommand(name='check_ban', description='<account> checks ban')
    async def check_ban_account(self, c: Command):
        # TODO
        return

    def check_app_data(self, search_term: str, data_type: str):
        """returns true if search term exists in file"""
        if data_type not in AppData.ALL:
            self.logger.error("Not a valid app data type!")
            return False
        # todo read file.
        return False

    def append_app_data(self, to_append: str, data_type: str):
        """returns true if search term exists in file"""
        if data_type not in AppData.ALL:
            self.logger.error("Not a valid app data type!")
            return False
        # todo append to file.
        return False
