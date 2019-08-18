import getopt
import websockets
import concurrent.futures
import asyncio
import requests
import json
import re as regex
import sys
import time
import logging
import importlib
from lib import constants
from lib.command import Command

logging.basicConfig(
    level=logging.INFO,
    format='%(threadName)10s : %(message)s',
    stream=sys.stderr,
)

class QuantumBot:
    def __init__(self):
        self.ws = None
        self.accounts = {}
        self.log = logging.getLogger('tc_bot')
        self.settings = None
        self.rate_limit_seconds = 1
        self.message_queue = []
        self.is_running = False
        self.cogs = []

    async def attempt_command(self, cmd:Command):
        for cog in self.cogs:
            #todo make it work for aliases
            if hasattr(cog, cmd.command):
                f = getattr(cog, cmd.command)
                # commands only run if they were given the _command meta data from the @command decorator
                if f._command:
                    await getattr(cog, cmd.command)(cmd)

    def load_config(self, config=None):
        if config is None:
            config = 'config'
        with open(f'./data/config/{config}.json') as data_file:
            self.settings = json.load(data_file)
        self.load_cogs()

    def load_cogs(self):
        for cog_name in self.settings['modules']:
            self.add_cog(cog_name)


    async def connect(self):
        self.log.info('starting')
        r = requests.session()
        data = r.get(url='https://tinychat.com/start?#signin')
        csrf = regex.search(string=data.text,
                            pattern=r'<meta name="csrf-token" id="csrf-token" content="[a-zA-Z0-9]*').group(0)[49:]
        s_data = {
            'login_username': self.settings['username'],
            'login_password': self.settings['password'],
            'remember': '1',
            '_token': csrf
        }
        r.post(url='https://tinychat.com/login', data=s_data)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        token = r.get(url='https://tinychat.com/api/v1.0/room/token/' + self.settings['room'])
        rtc_version_data = r.get(url='https://tinychat.com/room/' + self.settings['room'])
        rtc_version = regex.search(string=rtc_version_data.text, pattern=r'href="/webrtc/[0-9-.]*').group(0)[13:]

        payload = {
            'tc': 'join',
            'req': 1,
            'useragent': 'tinychat-client-webrtc-chrome_linux x86_64-' + rtc_version,
            'token': token.json()['result'],
            'room': self.settings['room'],
            'nick': self.settings['nickname']
        }

        r.close()
        async with websockets.connect(uri=token.json()['endpoint'], subprotocols=['tc'], extra_headers=headers, origin='https://tinychat.com') as self.ws:
            await self.ws.send(json.dumps(payload))
            self.is_running = True
            async for message in self.ws:
                await self.consumer(message)

    def add_cog(self, cog_name: str):
        m = importlib.import_module(f'modules.{cog_name.lower()}')
        cog_class = getattr(m, cog_name)
        cog = cog_class(bot=self)
        self.cogs.append(cog)

    def remove_cog(self, cog_name: str):
        for cog in self.cogs:
            if cog.name == cog_name:
                self.cogs.remove(cog)

    async def password(self):
       await self.ws.send(json.dumps({"tc":"password","req":2,"password":self.settings['room_password']}))

    async def consumer(self, message: str):
        print(message)

        tiny_crap = json.loads(message)
        if tiny_crap['tc'] == 'userlist':
            for user in tiny_crap['users']:
                self.accounts.update({user['handle']: user['nick']})
        if tiny_crap['tc'] == 'join':
            self.accounts.update({tiny_crap['handle']: tiny_crap['nick']})
        if tiny_crap['tc'] == 'quit':
            self.accounts.pop(tiny_crap['handle'])
        if tiny_crap['tc'] == 'ping':
            await self.pong()
        if tiny_crap['tc'] == 'msg':
            # run command helpers eveents in cogs
            for prefix in self.settings['prefixes']:
                # if prefix match continue
                if tiny_crap['text'].startswith(prefix):
                    await self.attempt_command(Command(data=tiny_crap))

        if tiny_crap['tc'] == 'password':
            await self.password()
        # runs cog events
        for type in constants.T_OBJECTS:
            if tiny_crap['tc'] == type:
                for cog in self.cogs:
                    await getattr(cog, type.lower())(tiny_crap)

                    # a simple message processor, doesnt matter which one you override with your cog. user preference.

    def handle_to_name(self, handle):
        return self.accounts[handle]

    async def send_message(self, message):
        if len(self.message_queue) > 0:
            self.message_queue.append(message)
        else:
            await self.ws.send(json.dumps({'tc': 'msg', 'req':1, 'text':message}))

    async def pong(self):
        await self.ws.send(json.dumps({'tc': 'pong', 'req': 1}))

    def process_message_queue(self):
        while self.is_running:
            if len(self.message_queue) > 0:
                self.send_message(message= self.message_queue.pop(0))
                time.sleep(self.rate_limit_seconds)


def process_arg(arg, b: QuantumBot):
    try:
        opts, args = getopt.getopt(arg, "c:", ["config="])
    except getopt.GetoptError:
        print('Bot.py -c <configfile>')
        sys.exit(2)
    # load default config if one is not specified.
    if not opts:
        b.load_config()

    for opt, arg in opts:
        if opt == '-c':
            b.load_config(arg)


async def start(executor, bot):
    asyncio.get_event_loop().run_in_executor(executor, bot.process_message_queue),
    await bot.connect()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1,)
bot = QuantumBot()
process_arg(sys.argv[1:], bot)
asyncio.get_event_loop().run_until_complete(start(executor, bot))

