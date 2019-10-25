from lib.cog import Cog
from lib.command import makeCommand, Command
from lib.constants import AppData
from lib.utils import string_in_file, append_string_in_file


class Admin(Cog):

    def join(self, data):
        # VIP mode, only op users cn use the room
        if self.bot.settings['module.admin']['vip_enabled']:
            if self.bot.settings['module.admin']['vip_kickasban']:
                return
            else:
                # do ban
                self.bot.ban()

    @makeCommand(name='makeHelp', description='Remakes help file using file descriptions')
    async def make_help(self, c: Command):
        help = ""
        help.join("Quantum bot help file\n")
        help.join("\n")
        for cog in self.bot.cogs:
            help.join(f"******************************\n")
            help.join(f"{cog.__name__}:\n")
            for method in cog.methods:
                if hasattr(method, "command"):
                    if hasattr(method, "name"):
                        if hasattr(method, "description"):
                            help.join(f"{getattr(method, 'name')} - {getattr(method, 'description')}\n")

        # use an api to post help file somewhere. pastebin/gist
        # send results through socket.

    @makeCommand(name='nick', description='<nickname> set bots nickname ')
    async def change_nick(self, c: Command):
        await self.change_nick(c.message)
        await self.send_message(f"You may now call me{c.message}.")

    @makeCommand(name='op', description='<account> makes op')
    async def make_op(self, c: Command):
        if append_string_in_file(file="op", appended_string=c.message):
            self.send_message(f"{c.message} has been given op status")
        else:
            self.logger.debug(f"Could not make {c.message} an op")
            self.send_message("Command failed.")

    @makeCommand(name='check_op', description='<account> check if has op status')
    async def check_op(self, c: Command):
        if string_in_file("op", c.message):
            return True
        return False

    @makeCommand(name='ban', description='<account> attempts to ban')
    async def make_ban_account(self, c: Command):
        if append_string_in_file(file="banned_accounts", appended_string=c.message):
            self.send_message(f"{c.message} has been given banned status")
        else:
            self.logger.debug(f"Could not add {c.message} banned list")
            self.send_message("Command failed.")

    @makeCommand(name='check_ban', description='<account> checks ban')
    async def check_ban_account(self, c: Command):
        if string_in_file("banned_accounts", c.message):
            return True
        return False
