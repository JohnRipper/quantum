"""
Quantum is a modular bot for Tinychat,
edit the .toml file to enable/disable modules
"""
import re

import websockets
import concurrent.futures
import asyncio
import requests
import json
import re as regex
import sys
import importlib
import argparse
from pathlib import Path

import tomlkit

from lib import tinychat
from lib.qlogging import QuantumLogger
from lib.constants import SocketEvents as SE, CHARACTER_LIMIT
from lib.command import Command
from lib.account import Account

from importlib import reload
from lib.utils import get_current_sha1, split_string
import time

__version__ = get_current_sha1()

class QuantumBot:

    def __init__(self):
        self._ws = None
        self.accounts = {}
        self.log = QuantumLogger("quantum")
        self.settings = None
        self.version = __version__
        self.rate_limit_seconds = 0.5
        self.message_queue = []
        self.is_running = False
        self.handle = 0
        self.req = 0

        # todo recheck the load, unload, reload methods
        # list of imports
        self.modules = []
        # list of classes
        self.cogs = []

    def init(self):
        self.load_cogs()

    async def attempt_command(self, cmd: Command):
        for cog in self.cogs:
            for method in cog.methods:
                if getattr(method, "name") == cmd.command:
                    # commands only run if they were given the _command meta data from the @command decorator
                    # check the role attribute
                    if cmd.account.role[1] >= method.role[1]:
                        asyncio.create_task(method(cmd))
                    else:
                        await self.send_message("Insufficient Permission to access this command")

    def get_req(self):
        self.req += 1
        return self.req

    def load_config(self, config):
        config = Path(config)
        if config.exists():
            self.settings = tomlkit.loads(config.read_text())
        else:
            sys.exit("Configuration not found, exiting.")

    def load_cogs(self):
        for cog_name in self.settings["bot"]["modules"]:
            self.log.info(f"adding cog: {cog_name}")
            self.add_cog(cog_name)

    def login(self):
        self.log.info("Beginning login")
        csrf = tinychat.getcsrf()
        if csrf is None:
            self.log.error("Couldn't get CSRF token, exiting...")
            sys.exit(1)
        logged_in = tinychat.login(
            self.settings["account"]["username"],
            self.settings["account"]["password"],
            csrf
        )
        if logged_in != None:
            self.log.error(logged_in)
            sys.exit(1)

    async def connect(self):
        self.log.info("starting")
        self.login()
        token = tinychat.token(self.settings["room"]["roomname"])
        if token is None:
            self.log.error("Couldn't get room token, exiting...")
            sys.exit(1)
        rtcversion = tinychat.rtcversion(self.settings["room"]["roomname"])
        if rtcversion is None:
            self.log.error("Couldn't get RTC version, exiting...")
            sys.exit(1)

        payload = {
            "tc": "join",
            "req": self.get_req(),
            "useragent": "tinychat-client-webrtc-chrome_linux x86_64-" + rtcversion,
            "token": token["result"],
            "room": self.settings["room"]["roomname"],
            "nick": self.settings["room"]["nickname"]}
        async with websockets.connect(
                uri=token["endpoint"],
                subprotocols=["tc"],
                extra_headers=tinychat.HEADERS,
                timeout=600,
                origin="https://tinychat.com"
        ) as self._ws:
            await self.wsend(json.dumps(payload))
            self.is_running = True
            async for message in self._ws:
                await self.consumer(message)

    def load_module(self, cog_name):
        for module in self.modules:
            if module.__name__ == f"modules.{cog_name.lower()}":
                module = reload(module)
                return module
        m = importlib.import_module(f"modules.{cog_name.lower()}")
        self.modules.append(m)
        return m

    def add_cog(self, cog_name: str):
        m = self.load_module(cog_name)
        cog = getattr(m, cog_name)
        self.cogs.append(cog(self))
        self.log.debug(f"added {cog_name} to the bot coglist")

    def remove_cog(self, cog_name: str):
        for cog in self.cogs:
            if cog.name == cog_name:
                self.cogs.remove(cog)
                self.log.debug(f"unloaded {cog_name}")
                break

    async def password(self):
        # do not log.
        await self._ws.send(
            json.dumps({"tc": "password", "req": self.get_req(), "password": self.settings["room"]["password"]}))

    async def consumer(self, message: str):
        tiny_crap = json.loads(message)
        if tiny_crap["tc"] == SE.PING:
            self.log.ping(tiny_crap)
            await self.pong()
        else:
            self.log.ws_event(message)
        if tiny_crap["tc"] == SE.NICK:
            self.accounts[tiny_crap["handle"]].nick = tiny_crap["nick"]
        if tiny_crap["tc"] == SE.CAPTCHA:
            self.log.warning(f"Captcha needed {tiny_crap}")
        if tiny_crap["tc"] == SE.USERLIST:
            for user in tiny_crap["users"]:
                self.accounts.update({user["handle"]: Account(**user)})
        if tiny_crap["tc"] == SE.JOINED:
            self.handle = tiny_crap["self"]["handle"]
        if tiny_crap["tc"] == SE.JOIN:
            self.accounts.update({tiny_crap["handle"]: Account(**tiny_crap)})
        if tiny_crap["tc"] == SE.QUIT:
            self.accounts.pop(tiny_crap["handle"])
        if tiny_crap["tc"] == SE.MSG:
            self.log.chat(f"{self.accounts[tiny_crap['handle']].username}: {tiny_crap['text']}")
            # check for a command, decorators are optional you can do it manually overriding msg in cog
            for prefix in self.settings["bot"]["prefixes"]:
                # if prefix match continue
                if tiny_crap["text"].startswith(prefix):
                    await self.attempt_command(
                        Command(prefix=prefix, data=tiny_crap, sender=self.handle_to_username(tiny_crap["handle"]),
                                account=self.accounts[tiny_crap["handle"]]))
                if prefix + "version" in tiny_crap["text"]:
                    await self.send_message(f"Quantum version: {self.version}")

        if tiny_crap["tc"] == SE.PASSWORD:
            await self.password()

        found = False
        # runs cog events
        for t in SE.ALL:
            if tiny_crap["tc"] == t:
                found = True
                for cog in self.cogs:
                    event = getattr(cog, t.lower())
                    if not hasattr(event, "command"):
                        await event(tiny_crap)

        # check for unknown events
        if not found:
            self.log.debug(f"Unknown websocket event: {tiny_crap}")

    def handle_to_nick(self, handle: int):
        return self.accounts[handle].nick

    def handle_to_username(self, handle: int):
        return self.accounts[handle].username

    def username_to_handle(self, username: str):
        for account in self.accounts:
            if account.username == username:
                return account.handle

    async def send_message(self, message: str):
        # 128 characters, 255 bytes
        if len(message) > CHARACTER_LIMIT:
            send_limit = self.settings["bot"]["message_limit"]
            message = re.sub("\n", " ", message)
            messages = re.findall("(.{1,128}[ .,;:]|.{1,128})", message.strip())
            for message in messages[:send_limit]:
                self.message_queue.append(message.strip())
        elif len(message) <= CHARACTER_LIMIT:
            self.message_queue.append(message.strip())

    async def pong(self):
        data = json.dumps({"tc": "pong", "req": self.get_req()})
        self.log.pong(data)
        await self._ws.send(data)

    async def wsend(self, message: str):
        """websocket send wrapper"""
        self.log.ws_send(message)
        await self._ws.send(message)

    def bot_loop(self):
        while True:
            if self.is_running:
                self.process_message_queue()
                # possible to add a loop to modules? idk what ppl would use it for.

    def process_message_queue(self):
        if len(self.message_queue) > 0:
            asyncio.run(self.wsend(json.dumps({"tc": "msg", "req": self.get_req(), "text": self.message_queue.pop(0)})))
        asyncio.run(asyncio.sleep(self.rate_limit_seconds))


def process_arg(b: QuantumBot):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=f"Quantum {__version__}"
    )
    parser.add_argument(
        "--version", "-v",
        action="version", version=f"Quantum {__version__}"
    )
    parser.add_argument(
        "--config", "-c",
        help="path to configuation file",
        default="default.toml"
    )
    parser.add_argument(
        "--logging", "-l",
        choices=["i", "c", "ws", "d", "w", "e"],
        help="set logging to Info, Chat, WebSocket, Debug, Warn, Error; respectively",
        default="i"
    )
    args = parser.parse_args()
    if args.config:
        b.load_config(args.config)
    if args.logging:
        switcher = {
            "i": QuantumLogger.INFO,
            "c": QuantumLogger.CHAT,
            "ws": QuantumLogger.WEBSOCKET,
            "d": QuantumLogger.DEBUG,
            "w": QuantumLogger.WARNING,
            "e": QuantumLogger.ERROR
        }
        if switcher.get(args.logging, False):
            bot.log.set_level(switcher.get(args.logging, False))


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.bot_loop)
    run_or_try_again = True
    attempts = 5
    restart_time = 30
    while run_or_try_again:
        try:
            run_or_try_again = False
            bot.init()
            await bot.connect()
        except websockets.WebSocketException:
            bot.log.error("websocket crashed, Restarting in {}")
            if attempts != 0:
                run_or_try_again = True
                attempts -= 1
            time.sleep(restart_time)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumBot()
process_arg(bot)
asyncio.get_event_loop().run_until_complete(start(executor, bot))
print("completed??? ")
