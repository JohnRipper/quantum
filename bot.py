from python_anticaptcha import AnticaptchaClient, NoCaptchaTaskProxylessTask, AnticatpchaException
import websockets
import concurrent.futures
import asyncio
import requests
import json
import re as regex
import isodate
import random
import sys
import time
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(threadName)10s : %(message)s',
    stream=sys.stderr,
)


class QuantumBot:
    def __init__(self, room: str):
        self.room = room
        self.nick = 'REEEEEEEEEEEE'
        self.username = 'johnjripper'
        self.password = '6`$3rH\'s_FYg*y\\A'
        self.captcha_client = AnticaptchaClient('13c1c8affe937213c92618735865340a')
        self.discord_key = ''
        self.ws = None
        self.accounts = {}
        self.log = logging.getLogger('tc_bot')
        self.queue = []
        self.song_playing = False
        if self.room == 'tech':
            self.prefixes = ('#')
            self.discord_channel = 571874368679051265
        elif self.room == 'ramblr':
            self.prefixes = ('/', '!', '#')
            self.discord_channel = 571875024064217089
        elif self.room == 'templeofvape':
            self.prefixes = ('/', '!', '#')
            self.discord_channel = 571875094264152064
        else:
            self.prefixes = ('/', '!', '#')
            self.discord_channel = 322662397359816714
        self.titles = ["my great experience voting for trump", "build the wall!!!!", "another reason to vote for trump", "top 10 reasons to vote for trump"]


    async def connect(self):
        self.log.info('starting')
        r = requests.session()
        data = r.get(url='https://tinychat.com/start?#signin')
        csrf = regex.search(string=data.text,
                            pattern=r'<meta name="csrf-token" id="csrf-token" content="[a-zA-Z0-9]*').group(0)[49:]
        s_data = {
            'login_username': self.username,
            'login_password': self.password,
            'remember': '1',
            '_token': csrf
        }
        r.post(url='https://tinychat.com/login', data=s_data)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        }
        token = r.get(url='https://tinychat.com/api/v1.0/room/token/' + self.room)
        rtc_version_data = r.get(url='https://tinychat.com/room/' + self.room)
        rtc_version = regex.search(string=rtc_version_data.text, pattern=r'href="/webrtc/[0-9-.]*').group(0)[13:]

        payload = {
            'tc': 'join',
            'req': 1,
            'useragent': 'tinychat-client-webrtc-chrome_linux x86_64-' + rtc_version,
            'token': token.json()['result'],
            'room': self.room,
            'nick': self.nick
        }
        print(payload)
        r.close()
        async with websockets.connect(uri=token.json()['endpoint'], subprotocols=['tc'], extra_headers=headers, origin='https://tinychat.com') as self.ws:
            await self.ws.send(json.dumps(payload))
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

    async def process_message(self, m, username):
        if m.startswith(self.prefixes):
            command, message = f'{m}{" "}'.split(' ', 1)
            command = command[1:]
            if command == 'eyes':
                await self.send_message('o.o 0.0 O.O o.O O.o O.0')
            if command == 'echo':
                await self.send_message(message)
            if command == 'yt':
                await self.play_youtube(message)
        await self.send_discord({"{}:{}".format(username, m)})

    async def consumer(self, message: str):
        tiny_crap = json.loads(message)
        print(message)
        if tiny_crap['tc'] == 'captcha':
           await self.do_captcha(key=tiny_crap['key'])
        if tiny_crap['tc'] == 'userlist':
            for user in tiny_crap['users']:
                self.accounts.update({user['handle']: user['nick']})
        if tiny_crap['tc'] == 'join':
            self.accounts.update({tiny_crap['handle']: tiny_crap['nick']})
            await self.send_discord(
                '{} has joined the room with account: {}'.format(
                    tiny_crap['nick'],
                    tiny_crap['username']))
        if tiny_crap['tc'] == 'quit':
            self.accounts.pop(tiny_crap['handle'])
        if tiny_crap['tc'] == 'ping':
            await self.pong()
        if tiny_crap['tc'] == 'msg':
            await self.process_message(tiny_crap['text'], self.accounts[tiny_crap['handle']])
        #"item":{"duration":196,"id":"hiFGxAOtGNw","image":"","offset":0,"playlist":false,"title":"my great experience voting for trump"},"success":true,"tc":"yut_stop"}
        if tiny_crap['tc'] == 'yut_stop':
            self.song_playing = False
            if self.queue:
                await self.play_song(data=self.queue.pop())


    async def do_captcha(self, key: str):
        print('captcha required, attempting to solve.')
        try:
            task = NoCaptchaTaskProxylessTask(
                'https://www.tinychat.com/room/%s' % self.room, key)
            job = self.captcha_client.createTask(task)
            job.join()
            payload = {
                'tc': 'captcha',
                'req': 1,
                'token': job.get_solution_response()
            }
            await self.ws.send(json.dumps(payload))
        except AnticatpchaException as e:
            raise

    async def send_message(self, message):
        await self.ws.send(json.dumps({'tc': 'msg', 'req':1, 'text':message}))

    async def send_discord(self, data):
        headers = {"Authorization": "Bot {}".format(self.discord_key),
                   "Content-Type": "application/x-www-form-urlencoded"}
        requests.post(url='https://discordapp.com/api/v6/channels/{}/messages'.format(self.discord_channel),
                      headers=headers,
                      data={'content': data})

    async def play_youtube(self, message):
        if message is None or message == '':
            return
        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=' + message + '&maxResults=1&key=AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg'
        headers = {'referer': 'https://tinychat.com'}
        search_request = requests.get(url=url, headers=headers)
        search_result = json.loads(search_request.text)
        video_id = search_result['items'][0]['id']['videoId']
        details = requests.get(
            url='https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=' + video_id + '&key=AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg',
            headers=headers)
        d = json.loads(details.text)
        print(details.text)
        dur = isodate.parse_duration(d['items'][0]['contentDetails']['duration'])
        # add a few seconds to duration to help fight premature ejeculation.
        data = {"tc":"yut_play",
                "req":36,
                "item":{
                    "id":video_id,
                    "duration":int(dur.total_seconds()) + 3,
                    "offset":0,
                    "title":random.choice(self.titles)}}
        await self.play_song(data=data)

    async def play_song(self, data):
        if self.song_playing:
            self.queue.append(data)
        else:
            await self.ws.send(json.dumps(data))

    async def pong(self):
        await self.ws.send(json.dumps({'tc': 'pong', 'req': 1}))


async def start(executor, bot):
    await bot.connect()

executor = concurrent.futures.ThreadPoolExecutor(max_workers=1,)
bot = QuantumBot(room=sys.argv[1])
asyncio.get_event_loop().run_until_complete(start(executor, bot))

