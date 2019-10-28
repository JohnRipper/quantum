import logging
import os
import sys
from logging import LogRecord, addLevelName, getLoggerClass, setLoggerClass

dir_path = os.path.dirname(os.path.realpath(__file__))


class ChatFilter(logging.Filter):
    def filter(self, record: LogRecord):
        msg = record.msg
        if isinstance(msg, str):
            if record.levelno == QuantumLogger.CHAT:
                return True
        return False


class QuantumLogger(getLoggerClass()):
    # custom levels
    CHAT = 75
    WEBSOCKET = 24
    WS_EVENT = 25
    WS_SENT = 26

    PING = 27
    PONG = 28
    # logger levels
    NOTSET = 0
    DEBUG = 10
    INFO = 20
    WARNING = 30
    ERROR = 40
    CRITICAL = 50

    _choices = ((CHAT, "chat"),
                (WEBSOCKET, "websocket"),
                (DEBUG, "debug"),
                (PING, "ping"),
                (PONG, "pong"),
                (INFO, "info"),
                (WARNING, "warning"),
                (ERROR, "error"))

    shortcodes = {
        "i": INFO,
        "c": CHAT,
        "ws": WEBSOCKET,
        "d": DEBUG,
        "w": WARNING,
        "e": ERROR
    }

    def __init__(self, name, level=20, chat_handler=True):
        super().__init__(name, level)
        addLevelName(self.CHAT, "CHAT")
        addLevelName(self.WS_EVENT, "WS_EVENT")
        addLevelName(self.WS_SENT, "WS_SENT")
        addLevelName(self.PING, "PING")
        addLevelName(self.PONG, "PONG")
        self.chat_handler_enabled = chat_handler

        # default is info
        self.set_level(level)

    def ping(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PING):
            self._log(self.PING, msg, args, **kwargs)

    def pong(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.PONG):
            self._log(self.PONG, msg, args, **kwargs)

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
        # TODO better log file names. ^^ see above ^^ Also apply filter
        file_name = f"data/logs/chat.log"
        # create if doesnt exist
        open(os.path.join(dir_path, "..", f'{file_name}'), 'a').close()
        handler = logging.FileHandler(filename=file_name)
        # apply filter
        handler.addFilter(ChatFilter())
        self.addHandler(handler)

    def set_level(self, level: int):
        for chosen_level in self._choices:
            self.setLevel(level)
            if level == chosen_level[0]:
                # reset handlers
                self.remove_handlers()
                # set formatter
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

                # secondary log file that contains only messages.
                if self.level == self.CHAT:
                    self.add_chat_handler()
                else:
                    if self.chat_handler_enabled:
                        self.add_chat_handler()

                    # log to file
                    file_name = f"data/logs/{chosen_level[1]}.log"
                    # create if doesnt exist
                    open(os.path.join(dir_path, "..", f'{file_name}'), 'a').close()

                    handler = logging.FileHandler(filename=file_name)
                    handler.setLevel(level)
                    handler.setFormatter(formatter)
                    self.addHandler(handler)

                # log to the terminal.
                handler2 = logging.StreamHandler(sys.stdout)
                handler2.setLevel(level)
                handler2.setFormatter(formatter)
                self.addHandler(handler2)
                self.debug(f"Logging level set to {chosen_level[1].upper()}")
                return True
        # level was not set
        return False


setLoggerClass(QuantumLogger)
