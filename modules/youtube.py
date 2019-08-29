import random

import isodate
import requests

from lib.cog import Cog
import json

from lib.command import makeCommand, Command


class Youtube(Cog):
    song_playing = False
    queue = []

    @makeCommand(name="stop", description= "<name/url/id> - plays a song")
    async def stop(self, c: Command):
        # todo send youtube command.
        return

    @makeCommand(name="skip", description="<name/url/id> - plays a song")
    async def skip(self, c: Command):
        # todo next song
        return

    @makeCommand(name="play", description= "<name/url/id> - plays a song")
    async def play(self, c: Command):
        # TODO check that this triggers on empty command
        if c.message is None or c.message == '':
            await self.bot.send_message("No url, id, or song name given.")

        url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=' + c.message + '&maxResults=1&key=AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg'
        headers = {'referer': 'https://tinychat.com'}
        search_request = requests.get(url=url, headers=headers)
        search_result = json.loads(search_request.text)
        video_id = search_result['items'][0]['id']['videoId']
        details = requests.get(
            url='https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id=' + video_id + '&key=AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg',
            headers=headers)
        d = json.loads(details.text)
        dur = isodate.parse_duration(d['items'][0]['contentDetails']['duration'])
        # add a few seconds to duration to help fight premature ejaculation.
        data = {"tc":"yut_play",
                "req":36,
                "item":{
                    "id":video_id,
                    "duration":int(dur.total_seconds()) + 3,
                    "offset":0,
                    "title":"test"}}
        await self.play_song(data=data)

    async def yut_stop(self, data: dict):
        self.song_playing = False
        if self.queue:
            await self.play_song(data=self.queue.pop())

    async def yut_play(self, data: dict):
        self.song_playing = True

    async def play_song(self, data):
        if self.song_playing:
            self.queue.append(data)
        else:
            await self.bot.ws.send(json.dumps(data))

    async def play_next(self):
        next_song = self.queue.pop()
        await self.bot.ws.send(json.dumps(next_song))
