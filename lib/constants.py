CHARACTER_LIMIT = 128


class SocketEvents:
    MSG = "msg"
    CAPTCHA = "captcha"
    CLOSED = "closed"
    USERLIST = "userlist"
    JOIN = "join"
    JOINED = "joined"
    QUIT = "quit"
    BANLIST = "banlist"
    PING = "ping"
    YUT_STOP = "yut_stop"
    YUT_PLAY = "yut_play"
    YUT_PAUSE = "yut_pause"
    PVTMSG = "pvtmsg"
    ICESERVERS = "iceservers"
    NICK = "nick"
    PUBLISH = "publish"
    UNPUBLISH = "unpublish"
    STREAM_CONNECTED = "stream_connected"
    STREAM_CLOSED = "stream_closed"
    SDP = "sdp"
    SYSMSG = "sysmsg"
    PASSWORD = "password"

    ALL = [
        PVTMSG, MSG, NICK,
        PUBLISH, UNPUBLISH,
        CAPTCHA, PASSWORD, QUIT, PING,
        YUT_STOP, YUT_PLAY, YUT_PAUSE,
        BANLIST, USERLIST, JOIN, JOINED, SYSMSG,
        ICESERVERS, STREAM_CONNECTED, STREAM_CLOSED, SDP, CLOSED]


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

