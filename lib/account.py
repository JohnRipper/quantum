import json


class Account:
    def __init__(self, data):
        data = json.loads(data)
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
        # TODO check /data/app_data/op
        return False

    def is_banned(self):
        # TODO check /data/app_data/banned_accounts
        return False

    def make_op(self):
        # TODO check /data/app_data/op
        return False

    def make_banned(self):
        # TODO check /data/app_data/banned_accounts
        return False
