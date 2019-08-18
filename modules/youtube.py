import random

import isodate
import requests

from lib.cog import Cog
import json


class Youtube(Cog):

    song_playing = False
    queue = []

    async def yut_stop(self, data: dict):
            self.song_playing = False
            if self.queue:
                await self.play_song(data=self.queue.pop())

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
                    "title":"test"}}
        await self.play_song(data=data)

    async def play_song(self, data):
        if self.song_playing:
            self.queue.append(data)
        else:
            await self.bot.ws.send(json.dumps(data))
