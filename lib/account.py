from lib.constants import AppData, Role
from lib.utils import append_string_in_file, string_in_file


class Account:
    role: (str, int)

    def __init__(self, data):
        # "userlist" and "join" events use the same user object.
        self.raw_data = data
        # convert raw data to class objects
        self.achievement_url = data["achievement_url"]
        self.avatar = data["avatar"]
        self.featured = data["featured"]
        self.giftpoints = data["giftpoints"]
        self.handle = data["handle"]
        self.lurker = data["lurker"]
        self.mod = data["mod"]
        self.nick = data["nick"]
        self.owner = data["owner"]
        self.session_id = data["session_id"]
        self.subscription = data["subscription"]

        self.username = data["username"]

        self.role = Role.NONE
        # check in order to ensure user gets highest available role assigned.
        if self.is_op():
            self.role = Role.OP
        if self.mod:
            self.role = Role.MOD
        if self.owner:
            self.role = Role.OWNER

        # how to detect people who are not logged in

    def is_op(self):
        if string_in_file(file=AppData.OP, search_term=self.username):
            return True
        return False

    def is_banned(self):
        if string_in_file(file=AppData.BANNED_ACCOUNTs, search_term=self.username):
            return True
        return False

    def make_op(self):
        if not string_in_file(file=AppData.OP, search_term=self.username):
            append_string_in_file(file=AppData.OP, appended_string=self.username)

    def make_banned(self):
        if not string_in_file(file=AppData.BANNED_ACCOUNTs, search_term=self.username):
            append_string_in_file(file=AppData.BANNED_ACCOUNTs, appended_string=self.username)
