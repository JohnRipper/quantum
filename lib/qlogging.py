import sys
from logging import getLoggerClass, addLevelName, setLoggerClass
import logging

logging.basicConfig(
    format="%(threadName)10s %(name)18s: %(message)s",
)


class HourFilter(logging.Filter):
    def filter(self, record):
        msg = record.msg
        if isinstance(msg, str):
            # TODO creates a filter that only returns records from the past hour
            # TODO Avoid intensive operations
            # 'created': 1550671851.660067
            # if record.created
            # returns True if passes checks
            return True
        return False


class QuantumLogger(getLoggerClass()):
    # custom levels
    CHAT = 50
    WEBSOCKET = 25
    WS_EVENT = 25
    WS_SENT = 25

    # logger levels
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    _choices = ((CHAT, "chat"),
                (WS_EVENT, "wsevent"),
                (WS_SENT, "wssent"),
                (DEBUG, "debug"),
                (INFO, "info"),
                (WARNING, "warning"),
                (ERROR, "error"))

    def __init__(self, name, level=20):
        super().__init__(name, level)
        addLevelName(self.CHAT, "CHAT")
        addLevelName(self.WS_EVENT, "WS_EVENT")
        addLevelName(self.WS_SENT, "WS_SENT")
        # default is info
        self.addFilter(HourFilter())

    def chat(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.CHAT):
            self._log(self.CHAT, msg, args, **kwargs)

    def ws_event(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.WS_EVENT):
            self._log(self.WS_EVENT, msg, args, **kwargs)

    def ws_send(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.WS_SENT):
            self._log(self.WS_SENT, msg, args, **kwargs)

    def remove_handlers(self):
        for handler in self.handlers:
            self.removeHandler(handler)

    def date_suffix(self):
        # TODO for use in log file names for better organization.
        # TODO seperated by Daily logs?
        return

    def add_chat_handler(self):
        # TODO better log file names. ^^ see above ^^
        if not self.level == self.CHAT:
            handler = logging.FileHandler(filename=f"/data/logs/chat.log")
            handler.setLevel(self.CHAT)
            self.addHandler(handler)

    def set_level(self, level: int):
        for item in self._choices:
            if level == item[0]:
                self.setLevel(level)
                handler = logging.FileHandler(filename=f"/data/logs/{item[0]}.log")
                self.addHandler(handler)
                # print chosen logging level to console.
                handler2 = logging.StreamHandler(sys.stderr)
                self.addHandler(handler2)
                return f"Logging level set to {item[1].upper()}"
        # level was not set
        return False


setLoggerClass(QuantumLogger)



