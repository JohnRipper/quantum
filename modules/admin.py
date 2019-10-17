from lib.cog import Cog
from lib.command import makeCommand, Command
from lib.constants import AppData
from lib.utils import string_in_file, append_string_in_file


class Admin(Cog):

    def join(self, data):
        # VIP mode, only op users cn use the room
        if self.bot.settings['admin']['vip_enabled']:
            if self.bot.settings['admin']['vip_kickasban']:
                return
            else:
                # do ban
                self.bot.ban()

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

        # use an api to post help file somewhere. pastebin/gist
        # send results through socket.

    @makeCommand(name='op', description='<account> makes op')
    async def make_op(self, c: Command):
        if append_string_in_file(file="op", appended_string=c.message):
            self.bot.send_message(f"{c.message} has been given op status")
        else:
            self.logger.debug(f"Could not make {c.message} an op")
            self.bot.send_message("Command failed.")

    @makeCommand(name='check_op', description='<account> check if has op status')
    async def check_op(self, c: Command):
        if string_in_file("op", c.message):
            return True
        return False

    @makeCommand(name='ban', description='<account> attempts to ban')
    async def make_ban_account(self, c: Command):
        if append_string_in_file(file="banned_accounts", appended_string=c.message):
            self.bot.send_message(f"{c.message} has been given banned status")
        else:
            self.logger.debug(f"Could not add {c.message} banned list")
            self.bot.send_message("Command failed.")

    @makeCommand(name='check_ban', description='<account> checks ban')
    async def check_ban_account(self, c: Command):
        if string_in_file("banned_accounts", c.message):
            return True
        return False
