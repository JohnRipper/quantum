import json
from lib.utils import append_string_in_file, string_in_file

class Account:
    def __init__(self, data):

        # "userlist" and "join" events use the same user object.
        # join has an additional tc key that can be ignored.
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

    def is_op(self):
        if string_in_file("op", self.username):
            return True
        return False

    def is_banned(self):
        if string_in_file("banned_accounts", self.username):
            return True
        return False

    def make_op(self):
        append_string_in_file(file="op", appended_string=self.username)

    def make_banned(self):
        append_string_in_file(file="banned_accounts", appended_string=self.username)
