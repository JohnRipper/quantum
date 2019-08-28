import json

from lib.cog import Cog
from lib.command import makeCommand, Command
from lib.constants import AppData


class Admin(Cog):

    @makeCommand(name='cam', description='attempts to cam up')
    async def make_op(self, c: Command):
        # TODO
        return

    @makeCommand(name='cam', description='attempts to cam up')
    async def check_op(self, c: Command):
        # TODO
        return

    @makeCommand(name='cam', description='attempts to cam up')
    async def make_ban_account(self, c: Command):
        # TODO
        return

    @makeCommand(name='cam', description='attempts to cam up')
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
