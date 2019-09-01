class SocketEvents:
    MSG = "msg"
    CAPTCHA = "captcha"
    CLOSED = "closed"
    USERLIST = "userlist"
    JOIN = "join"
    JOINED = "joined"
    QUIT = "quit"
    PING = "ping"
    YUT_STOP = "yut_stop"
    PVTMSG = "pvtmsg"
    ICESERVERS = "iceservers"
    PUBLISH = "publish"
    UNPUBLISH = "unpublish"
    STREAM_CONNECTED = "stream_connected"
    STREAM_CLOSED = "stream_closed"
    SDP = "sdp"

    ALL = [MSG, CAPTCHA, USERLIST, JOIN, JOINED, QUIT, PING, YUT_STOP,
           PVTMSG, ICESERVERS, PUBLISH, UNPUBLISH, STREAM_CONNECTED,
           STREAM_CLOSED, SDP, CLOSED]


class AppData:
    BADWORDS = "bad_words"
    OP = "op"
    BANNED_ACCOUNTs = "banned_accounts"
    HELP_MESSAGE = "help_message"
    ALL = (BADWORDS, OP, BANNED_ACCOUNTs, HELP_MESSAGE)


class Role:
    NONE = -1
    NO_ACCOUNT = 0
    GUEST = 10
    OP = 50
    MOD = 75
    OWNER = 100
