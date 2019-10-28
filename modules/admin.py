from lib.cog import Cog
from lib.command import Command, makeCommand
from lib.utils import append_string_in_file, string_in_file


class Admin(Cog):

    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["admin"]

    async def join(self, data):
        # VIP mode, only op users cn use the room
        if self.settings['vip_enabled']:
            if self.settings['vip_kickasban']:
                return
            else:
                # do ban
                self.bot.ban()


    @makeCommand(name='makeHelp', description='Remakes help file using file descriptions')
    async def make_help(self, c: Command):
        lines = ["Quantum bot help file"]
        for cog in self.bot.cogs:
            lines.append(f"******************************")
            lines.append(f"{cog.name}:")
            for method in cog.methods:
                if hasattr(method, "name") & hasattr(method, "description"):
                    lines.append(f"{getattr(method, 'name')} - {getattr(method, 'description')}")
        help = "\n".join(lines)
        append_string_in_file(file="help.txt", appended_string=help)


        # use an api to post help file somewhere. pastebin/gist
        # send results through socket.

    @makeCommand(name='nick', description='<nickname> set bots nickname ')
    async def change_nick(self, c: Command):
        await self.change_nick(c.message)
        await self.send_message(f"You may now call me{c.message}.")

    @makeCommand(name='op', description='<account> makes op')
    async def make_op(self, c: Command):
        return

    @makeCommand(name='check_op', description='<account> check if has op status')
    async def check_op(self, c: Command):
        return

    @makeCommand(name='ban', description='<account> attempts to ban')
    async def make_ban_account(self, c: Command):
        if append_string_in_file(file="banned_accounts", appended_string=c.message):
            await self.send_message(f"{c.message} has been given banned status")
        else:
            self.logger.debug(f"Could not add {c.message} banned list")
            await self.send_message("Command failed.")

    @makeCommand(name='check_ban', description='<account> checks ban')
    async def check_ban_account(self, c: Command):
        if string_in_file("banned_accounts", c.message):
            return True
        return False
