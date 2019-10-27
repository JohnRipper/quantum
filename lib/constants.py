class SocketEvents:
    BANLIST = "banlist"
    CAPTCHA = "captcha"
    CLOSED = "closed"
    ICESERVERS = "iceservers"
    JOIN = "join"
    JOINED = "joined"
    MSG = "msg"
    NICK = "nick"
    PASSWORD = "password"
    PENDING_MODERATION = "pending_moderation"
    PING = "ping"
    PUBLISH = "publish"
    PVTMSG = "pvtmsg"
    QUIT = "quit"
    SDP = "sdp"
    STREAM_CLOSED = "stream_closed"
    STREAM_CONNECTED = "stream_connected"
    SYSMSG = "sysmsg"
    USERLIST = "userlist"
    UNPUBLISH = "unpublish"
    YUT_PAUSE = "yut_pause"
    YUT_PLAY = "yut_play"
    YUT_STOP = "yut_stop"

    ALL = [
        BANLIST, CAPTCHA, CLOSED, ICESERVERS, JOIN, JOINED, MSG, NICK, PASSWORD,
        PENDING_MODERATION, PING, PUBLISH, PVTMSG, QUIT, SDP, STREAM_CLOSED,
        STREAM_CONNECTED, SYSMSG, USERLIST, UNPUBLISH, YUT_PAUSE, YUT_PLAY,
        YUT_STOP,
    ]


class Limit:
    CHARS = 400
    MSG_PER_SEC = 0.5


class AppData:
    BADWORDS = "bad_words"
    OP = "op"
    BANNED_ACCOUNTs = "banned_accounts"
    HELP_MESSAGE = "help_message"
    ALL = (BADWORDS, OP, BANNED_ACCOUNTs, HELP_MESSAGE)


class Role:
    NONE = ("none", -1)
    NO_ACCOUNT = ("no_account", 0)
    # guest is logged in
    GUEST = ("account", 10)
    OP = ("op", 50)
    MOD = ("mod", 75)
    OWNER = ("owner", 100)
    ALL_VALID = (NO_ACCOUNT, GUEST, OP, MOD, OWNER)

