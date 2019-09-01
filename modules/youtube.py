import random

import isodate
import requests

from lib.cog import Cog
import json

from lib.command import makeCommand, Command


class Youtube(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.apikey = "AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg"
        self.headers = {"referer": "https://tinychat.com"}
        self.settings = self.bot.settings["modules"]["youtube"]
        if len(self.settings["key"]) > 0:
            self.apikey = self.settings["key"]
            self.headers = None
        self.song_playing = False
        self.queue = False

        # url parts
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        # videoSyndicated = Show results that can be played outside youtube (embedded?)
        # fields = shorten the json response, gotta go fast https://youtu.be/PX7zPlQjAr8
        self.search_url = "{}search?part=snippet&type=video&q={}&maxResults=1&"\
            "fields=items(id%2FvideoId)&videoSyndicated=true&key={}"
        self.detail_url = "{}videos?part=contentDetails,snippet&id={}&"\
            "fields=items(contentDetails%2Fduration%2Csnippet(channelTitle%2Ctitle))&key={}"


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
        # TODO it doesn't
        if c.message is None or c.message == '':
            await self.bot.send_message("No url, id, or song name given.")

        query = requests.utils.quote(c.message)
        search_requests = requests.get(
            url = self.search_url.format(self.base_url, query, self.apikey),
            headers = self.headers
        )
        video_id = search_request.json()["items"][0]["id"]["videoId"]
        details = requests.get(
            url = self.detail_url.format(self.base_url, video_id, self.apikey),
            headers = self.headers
        )
        duration = isodate.parse_duration(
            details.json()["items"][0]["contentDetails"]["duration"]
        )
        title = details.json()["items"][0]["snippet"]["title"]
        channel = details.json()["items"][0]["snippet"]["channelTitle"]
        # add a few seconds to duration to help fight premature ejaculation.
        data = {
            "tc":"yut_play",
            "req":36,
            "item": {
                "id":video_id,
                "duration":int(dur.total_seconds()) + 3,
                "offset":0,
                "title": "{} — [{}]".format(title,channeltitle)
            }
        }
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

