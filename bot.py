"""
Quantum is a modular bot for Tinychat,
edit the .toml file to enable/disable modules
"""
import websockets
import concurrent.futures
import asyncio
import requests
import json
import re as regex
import sys
import time
import importlib
import argparse
from pathlib import Path

import tomlkit

from lib.qlogging import QuantumLogger
from lib.constants import SocketEvents
from lib.command import Command
from lib.account import Account


class QuantumBot:
    def __init__(self):
        self.ws = None
        self.accounts = {}
        self.log = QuantumLogger("quantum")
        self.settings = None
        self.rate_limit_seconds = 1
        self.message_queue = []
        self.is_running = False
        self.cogs = []
        self.handle = 0

    async def attempt_command(self, cmd: Command):
        for cog in self.cogs:
            # todo make it work for aliases
            if hasattr(cog, cmd.command):
                f = getattr(cog, cmd.command)
                # commands only run if they were given the _command meta data from the @command decorator
                if hasattr(f, "_command"):
                    if f._command:
                        asyncio.ensure_future(getattr(cog, cmd.command)(cmd), loop=asyncio.get_event_loop())
                        # await getattr(cog, cmd.command)(cmd)

    def load_config(self, config):
        config = Path(config)
        print(config)
        if config.exists():
            self.settings = tomlkit.loads(config.read_text())
            self.load_cogs()
        else:
            sys.exit("Configuration not found, exiting.")

    def load_cogs(self):
        for cog_name in self.settings["bot"]["modules"]:
            self.add_cog(cog_name)

    async def connect(self):
        self.log.info("starting")
        r = requests.session()
        data = r.get(url="https://tinychat.com/start?#signin")
        csrf = regex.search(string=data.text,
                            pattern=r'<meta name="csrf-token" id="csrf-token" content="[a-zA-Z0-9]*').group(0)[49:]
        s_data = {
            "login_username": self.settings["account"]["username"],
            "login_password": self.settings["account"]["password"],
            "remember": "1",
            "_token": csrf
        }
        r.post(url="https://tinychat.com/login", data=s_data)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
        }
        token = r.get(url="https://tinychat.com/api/v1.0/room/token/" + self.settings["room"]["roomname"])
        rtc_version_data = r.get(url="https://tinychat.com/room/" + self.settings["room"]["roomname"])
        rtc_version = regex.search(string=rtc_version_data.text, pattern=r'href="/webrtc/[0-9-.]*').group(0)[13:]

        payload = {
            "tc": "join",
            "req": 1,
            "useragent": "tinychat-client-webrtc-chrome_linux x86_64-" + rtc_version,
            "token": token.json()["result"],
            "room": self.settings["room"]["roomname"],
            "nick": self.settings["room"]["nickname"]
        }

        r.close()
        async with websockets.connect(uri=token.json()["endpoint"], subprotocols=["tc"],
                                      extra_headers=headers, timeout=600, origin="https://tinychat.com") as self.ws:
            await self.ws.send(json.dumps(payload))
            self.is_running = True
            async for message in self.ws:
                await self.consumer(message)

    def add_cog(self, cog_name: str):
        m = importlib.import_module(f"modules.{cog_name.lower()}")
        cog_class = getattr(m, cog_name)
        cog = cog_class(bot=self)
        self.cogs.append(cog)

    def remove_cog(self, cog_name: str):
        for cog in self.cogs:
            if cog.name == cog_name:
                self.cogs.remove(cog)

    async def password(self):
        await self.ws.send(json.dumps({"tc": "password", "req": 2, "password": self.settings["room"]["password"]}))

    async def consumer(self, message: str):
        self.log.ws_event(message)
        tiny_crap = json.loads(message)
        if tiny_crap["tc"] == "captcha":
            self.log.error(f"Captcha needed {tiny_crap}")
        if tiny_crap["tc"] == "userlist":
            for user in tiny_crap["users"]:
                self.accounts.update({user["handle"]: Account(user)})
        if tiny_crap["tc"] == "joined":
            self.handle = tiny_crap["self"]["handle"]
        if tiny_crap["tc"] == "join":
            self.accounts.update({tiny_crap["handle"]: Account(tiny_crap)})
        if tiny_crap["tc"] == "quit":
            self.accounts.pop(tiny_crap["handle"])
        if tiny_crap["tc"] == "ping":
            await self.pong()
        if tiny_crap["tc"] == "msg":
            self.log.chat(str(self.handle_to_name(tiny_crap["handle"])) + ": " + str(tiny_crap["text"]))
            # check for a command, decorators are optional you can do it manually overriding msg in cog
            for prefix in self.settings["bot"]["prefixes"]:
                # if prefix match continue
                if tiny_crap["text"].startswith(prefix):
                    await self.attempt_command(Command(data=tiny_crap))
        if tiny_crap["tc"] == "password":
            await self.password()

        found = False
        # runs cog events
        for t in SocketEvents.ALL:
            if tiny_crap["tc"] == t:
                found = True
                for cog in self.cogs:
                    await getattr(cog, t.lower())(tiny_crap)
        # check for unknown events
        if not found:
            self.log.debug(f"Unknown websocket event: {tiny_crap}")
            print(f"Unknown websocket event: {tiny_crap}")

    def handle_to_name(self, handle):
        return self.accounts[handle].username

    async def send_message(self, message):
        if len(self.message_queue) > 0:
            self.message_queue.append(message)
        else:
            await self.ws.send(json.dumps({"tc": "msg", "req": 1, "text": message}))

    async def pong(self):
        await self.ws.send(json.dumps({"tc": "pong", "req": 1}))

    async def wsend(self, message: str):
        """websocket send wrapper"""
        self.log.ws_send(message)
        await self.ws.send(message)

    def bot_loop(self):
        while self.is_running:
            self.process_message_queue()

    def process_message_queue(self):
        while self.is_running:
            if len(self.message_queue) > 0:
                self.send_message(message=self.message_queue.pop(0))
                time.sleep(self.rate_limit_seconds)


def process_arg(b: QuantumBot):
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="It's reommended you copy the default.toml and rename before adding changing"
    )
    # Define args
    # TODO maybe add a few for more for roomname etc
    parser.add_argument(
        "--config", "-c",
        help="path to configuation file",
        default="default.toml"
    )
    parser.add_argument(
        "--logging", "-l",
        choices=["i","c","ws","d","w","e"],
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
            sys.exit()


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.bot_loop),
    await bot.connect()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=3, )
bot = QuantumBot()
process_arg(bot)
asyncio.get_event_loop().run_until_complete(start(executor, bot))
