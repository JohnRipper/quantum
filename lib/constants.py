class SocketEvents:
    MSG = 'msg'
    CAPTCHA = 'captcha'
    USERLIST = 'userlist'
    JOIN = 'join'
    QUIT = 'quit'
    PING = 'ping'
    YUT_STOP = 'yut_stop'
    PVTMSG = 'pvtmsg'
    ICESERVERS = 'iceservers'
    PUBLISH = 'publish'
    UNPUBLISH = 'unpublish'
    STREAM_CONNECTED = 'stream_connected'
    STREAM_CLOSED = 'stream_closed'
    SDP = 'sdp'

    ALL = [MSG, CAPTCHA, USERLIST, JOIN, QUIT, PING, YUT_STOP,
           PVTMSG, ICESERVERS, PUBLISH, UNPUBLISH, STREAM_CONNECTED,
           STREAM_CLOSED, SDP]


class AppData:
    BADWORDS = "bad_words"
    OP = "bad_words"
    BANNED_ACCOUNTs = "banned_accounts"
    HELP_MESSAGE = "help_message"
    ALL = (BADWORDS, OP, BANNED_ACCOUNTs, HELP_MESSAGE)
