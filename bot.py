"""
Quantum is a modular bot for Tinychat,
edit the .toml file to enable/disable modules
"""

import concurrent.futures
import argparse
import asyncio
import concurrent.futures
import json
import importlib
import re
import sys
import time
import tomlkit
import websockets

from lib import tinychat
from lib.account import Account
from lib.command import Command

from pathlib import Path
from importlib import reload
from lib.utils import get_current_sha1
from lib.constants import Limit
from lib.constants import SocketEvents as SE
from lib.qlogging import QuantumLogger

__version__ = get_current_sha1()


class QuantumBot:

    def __init__(self, args):
        self._ws = None
        self.accounts = {}
        self.log = QuantumLogger("quantum")
        self.settings = None
        self.version = __version__
        self.message_queue = []
        self.is_running = False
        self.handle = 0
        self.req = 0
        self.start_time = time.time()
        self.modules = []  # list of imports
        self.cogs = []  # list of classes

        if args.config:
            if args.config:
                self.load_config(args.config)
        if args.logging:
            if self.log.shortcodes.get(args.logging, False):
                self.log.set_level(self.log.shortcodes.get(args.logging, False))

    async def run(self):
        await self.load_cogs()
        await self.connect()

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

    async def load_cogs(self):
        for cog_name in self.settings["bot"]["modules"]:
            self.log.debug(f"adding cog: {cog_name}")
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
        self.log.info("attempting to connect to tinychat")
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

        if tiny_crap["tc"] == SE.PASSWORD:
            await self.password()

        found = False
        # runs cog events
        if tiny_crap["tc"] in SE.ALL:
            found = True
            for cog in self.cogs:
                event = getattr(cog, tiny_crap["tc"])
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

    async def send_message(self, message: str, clean: bool = True, limit: int = 0):
        if len(message) > Limit.CHARS:
            send_limit = self.settings["bot"]["message_limit"]
            if limit > 0 and limit <= send_limit:
                send_limit = limit
            if clean:
                message = re.sub("\n", " ", message)
            # re.DOTALL makes . match everything, including newline
            messages = re.findall("(.{1,400}[.,;:]|.{1,400})", message, re.DOTALL)
            for message in messages[:send_limit]:
                self.message_queue.append(message)
        elif len(message) <= Limit.CHARS:
            self.message_queue.append(message)

    async def pong(self):
        data = json.dumps({"tc": "pong", "req": self.get_req()})
        self.log.pong(data)
        await self._ws.send(data)

    async def wsend(self, message: str):
        """websocket send wrapper"""
        self.log.ws_send(message)
        await self._ws.send(message)

    def process_input(self):
        while True:
            if self.is_running:
                f = input()

    def process_message_queue(self):
        while True:
            if self.is_running:
                if len(self.message_queue) > 0:
                    asyncio.run(
                        self.wsend(json.dumps({"tc": "msg", "req": self.get_req(), "text": self.message_queue.pop(0)})))
                asyncio.run(asyncio.sleep(Limit.MSG_PER_SEC))


