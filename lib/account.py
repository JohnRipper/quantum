from lib.constants import AppData, Role
from lib.utils import append_string_in_file, string_in_file
from dataclasses import dataclass


@dataclass
class Account:
    # "userlist" and "join" events use the same user object.

    # tc object
    achievement_url: str
    avatar: str
    featured: bool
    giftpoints: int
    handle: int
    lurker: bool
    mod: bool
    nick: str
    owner: bool
    session_id: str
    subscription: bool
    username: str

    # custom fields
    role: (str, int) = Role.NONE
    tc: str = "None"

    def __post_init__(self):
        # check in order to ensure user gets highest available role assigned.
        if self.has_op_access():
            self.role = Role.OP
        if self.mod:
            self.role = Role.MOD
        if self.owner:
            self.role = Role.OWNER

        if self.role is Role.NONE:
            self.role = Role.GUEST

    def has_op_access(self):
        if self.role >= Role.OP:
            return True

    def is_banned(self):
        if string_in_file(file=AppData.BANNED_ACCOUNTs, search_term=self.username):
            return True
        return False

    def make_op(self):
        if self.role <= Role.OP:
            self.role = Role.OP
            return True
        else:
            # Role level is already higher.
            return False

    def make_banned(self):
        if not string_in_file(file=AppData.BANNED_ACCOUNTs, search_term=self.username):
            append_string_in_file(file=AppData.BANNED_ACCOUNTs, appended_string=self.username)
