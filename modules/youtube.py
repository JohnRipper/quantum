import asyncio
import json
import re
from collections import deque
from dataclasses import dataclass
from itertools import islice

import isodate
import requests

from lib import constants
from lib.cog import Cog
from lib.command import Command, makeCommand


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.current = 0
        self.running = False

    async def start(self):
        self.running = True
        while self.running is True and self.current != self.duration:
            await asyncio.sleep(1)
            self.current += 1

    def pause(self):
        self.running = False


@dataclass
class Video:
    id: str
    title: str
    channel: str
    duration: int
    offset: int = 0

    def __post_init__(self):
        parsed = isodate.parse_duration(self.duration)
        self.duration = parsed.total_seconds() + 3


class Youtube(Cog):
    """
    TODO makeCommand descriptions
    TODO look at how pausing/resuming actually works in  TC
    TODO handle seeking
    TODO question if `Timer` is needed or if we should just use
    start = time.time(), elapsed = time.time() - start similar to how nort did
    """
    def __init__(self, bot):
        super().__init__(bot)
        self.apikey = "AIzaSyCPQe4gGZuyVQ78zdqf9O5iEyfVLPaRwZg"
        self.headers = {"referer": "https://tinychat.com"}
        self.settings = self.bot.settings["module"]["youtube"]
        if len(self.settings["key"]) > 0:
            self.apikey = self.settings["key"]
            self.headers = None
        self.playlist = deque()
        self.active_video = None
        self.timer = None

    @makeCommand(name="yt", description= "<name/url/id> - plays a song")
    async def play(self, c: Command):
        self.logger.info(self.active_video)
        if c.message is None or c.message == "":
            await self.send_message("No url, id, or song name given.")
        else:
            if re.search("http.+youtu", c.message):
                video_id = re.search("(?:v=|\.be\/)(.{11})", c.message).group(1)
                video = await self.get_video_info(video_id)
            else:
                video = await self.find_video_id(c.message)

            if video is None:
                await self.send_message("Had an issue looking up that video")
            else:
                added = await self.add_video(video)
                if added:
                    await self.send_message(f"Added {video.title} @{len(self.playlist) - 1}")

    @makeCommand(name="addpl", description="")
    async def addplaylist(self, c: Command):
        if c.message is None or c.message == "":
            await self.send_message("Need a playlist URL or search string")
        else:
            if re.search("http.+youtu", c.message):
                await self.send_message("Generating playlist, one moment...")
                playlist_id = re.search("list=([A-Za-z0-9\-_]+)", c.message).group(1)
                playlist = await self.get_playlist_info(playlist_id)
            else:
                await self.send_message("Searching and generating playlist, one moment...")
                playlist = await self.find_playlist_id(c.message)

            if playlist is None:
                await self.send_message("Couldn't find that playlist")
            else:
                for video in playlist:
                    await self.add_video(video)
                await self.send_message(f"Added {len(playlist)} videos to the playlist\nTotal is now: {len(self.playlist)}", clean=False)

    @makeCommand(name="cpl", description="clear the playlist")
    async def clearplaylist(self, c: Command):
        await self.send_message(f"Clearing {len(self.playlist)} items.")
        self.playlist.clear()

    @makeCommand(name="pause", description="TODO pause the current video")
    async def pause(self, c: Command):
        if self.active_video:
            await self.pause_video()
            await self.send_message(f"Pausing timer at {self.timer.current}/{self.timer.duration}")

    @makeCommand(name="resume", description="")
    async def resume(self, c: Command):
        if self.active_video and self.timer.running is False:
            await self.start_video(self.active_video)

    @makeCommand(name="stop", description= "Stops the current video")
    async def stop(self, c: Command):
        if self.active_video:
            await self.send_yut_stop()

    @makeCommand(name="skip", description="Skips the active_video")
    async def skip(self, c: Command):
        if self.active_video and len(self.playlist) > 0:
            await self.next_video()
        else:
            await self.send_message("THERE IS NOTHING TO FUCKING SKIP TECH")

    @makeCommand(name="rm", description="<title/index/none> remove video")
    async def removevideo(self, c: Command):
        if c.message is None or c.message == "" and len(self.playlist) > 0:
            video = self.playlist[-1]
            await self.send_message(f"Removed {video.title}")
            await self.remove_video()
        elif c.message.isdigit() and int(c.message) <= len(self.playlist):
            index = int(c.message)
            video = self.playlist[index]
            await self.remove_message(f"Removed {video.title} at {index}")
            await self.remove_video(index=index)
        elif len(self.playlist) > 0:
            await self.remove_video(title=c.message)

    @makeCommand(name="now", description="")
    # TODO format duration/elapsed into more human readable
    # eg. 3m 12s, datetime can do it
    async def now(self, c: Command):
        if self.active_video:
            msg = "{}\nhttps://youtu.be/{}\nDuration: {}s\nElapsed: {}s".format(
                self.active_video.title,
                self.active_video.id,
                int(self.active_video.duration),
                self.timer.current)
        else:
            msg = "Nothing is playing"
        await self.send_message(msg, clean=False)

    @makeCommand(name="next", description="")
    async def next(self, c: Command):
        if len(self.playlist) > 0:
            nextvideo = len(self.playlist) - 1
            msg = "Up next:\n{}".format(self.playlist[nextvideo].title)
        else:
            msg = "Nothing up next."
        await self.send_message(msg)

    @makeCommand(name="pl", description="")
    async def playlistlist(self, c: Command):
        if len(self.playlist) > 0:
            sliced = islice(self.playlist, 0, len(self.playlist), 1)
            _ = 0
            playlist = []
            for slice in sliced:
                _+=1
                playlist.append(f"{_}) {slice.title}")
            msg = "\n".join(playlist)
        else:
            msg = "Playlist is empty."
        await self.send_message(msg, clean=False)


    # TODO consider merging with the above commands, or keep them separated?
    # Playlist funcs
    async def add_video(self, video: Video, index = None) -> bool:
        """Add a video to the playlist or play immediately
        returns True if the video was added to the playlist
        returns False if the video was played immediately
        """
        if self.active_video:
            self.logger.info(f"Adding {video} to playlist")
            self.playlist.append(video)
            return True
        else:
            self.logger.info(f"Playlist is empty, playing {video} now")
            await self.start_video(video)
            return False

    async def start_video(self, video: Video):
        self.active_video = video
        self.timer = Timer(video.duration)
        self.timer.current = video.offset
        # create_task() seems to be the correct thing to use?
        asyncio.create_task(self.timer.start())
        #asyncio.ensure_future(self.timer.start(), loop=asyncio.get_event_loop())
        await self.send_yut_play(video)

    async def pause_video(self):
        self.timer.pause()
        self.active_video.offset = self.timer.current
        await self.send_yut_pause()

    async def next_video(self) -> None:
        if len(self.playlist) > 0:
            next = self.playlist.pop()
            self.active_video = next
            self.playlist.popleft()
            self.logger.info(f"next_video: playing {next}")
            await self.start_video(next)

    async def remove_video(self, title: str = None, index: int = None) -> None:
        if index is not None:
            self.logger.info(f"Deleting {self.playlist[index]} from playlist")
            del(self.playlist[index])
        elif title is not None:
            for index, video in enumerate(self.playlist):
                if re.search(title, video.title):
                    await self.send_message(f"Matched {title} in {video}\nDeleting {index}", clean=False)
                    self.logger.info(f"Matched {title} in {video.title}")
                    del(self.playlist[index])
                    break
        else:
            self.logger.info(f"Deleting {self.playlist[0]} from playlist")
            self.playlist.pop()

    ### Send
    async def send_yut_play(self, video: Video) -> None:
        self.logger.info(f"Playing {video}")
        data = {
            "tc": constants.SocketEvents.YUT_PLAY,
            "req": self.get_req(),
            "item": {
                "id": video.id,
                "duration": video.duration,
                "offset": video.offset,
                "title": video.title
            }
        }
        await self.send_ws(data)

    async def send_yut_pause(self):
        self.logger.info(f"Pausing {self.active_video}")
        data = {
            "tc": constants.SocketEvents.YUT_PAUSE,
            "req": self.get_req(),
            "item": {
                "id": self.active_video.id,
                "offset": self.active_video.offset
            }
        }
        await self.send_ws(data)

    async def send_yut_stop(self):
        self.logger.info(f"Stopping {self.active_video}")
        data = {
            "tc": constants.SocketEvents.YUT_STOP,
            "req": self.get_req(),
            "item": {
                "id": self.active_video.id,
                "duration": self.active_video.duration,
                "offset": self.active_video.offset
            }
        }
        self.active_video = None
        self.timer = None
        await self.send_ws(data)

    #### Recv
    async def yut_play(self, data: dict):
        # TODO handle getting over played, better-ish.
        # see https://github.com/nortxort/nortbot/issues/14
        if "handle" in data and data["handle"] == self.bot.handle:
            # Ignore bot's own video
            pass
        else:
            video = await self.get_video_info(data["item"]["id"])
            self.logger.info(f"Overplayed, setting as active: {video.title}")
            self.active_video = video

    async def yut_pause(self, data: dict) -> None:
        if self.timer and self.timer.running:
            await self.pause_video()

    async def yut_stop(self, data: dict):
        self.active_video = None
        self.timer = None
        await self.next_video()

    ### Youtube API
    async def find_video_id(self, query: str) -> Video:
        """Uses the search API to get the Video ID
        then runs `get_video_info()` to return the Video object
        """
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&"\
            "type=video&q={}&maxResults=1&fields=items(id%2FvideoId)&"\
            "videoSyndicated=true&key={}"
        self.logger.info(f"find_video_id: GET {url}")
        search = requests.get(
            url=url.format(query, self.apikey),
            headers=self.headers)

        if search.status_code != 200:
            self.logger.info(f"find_video_id: Got {search.status_code} expected 200")
            return None
        else:
            try:
                video_id = search.json()["items"][0]["id"]["videoId"]
            except KeyError as err:
                self.logger.info(err)
                return None
            else:
                video = await self.get_video_info(video_id=video_id)
                return video

    async def get_video_info(self, video_id: str) -> Video:
        """Uses the search API to get the details for a videoId
        returns a Video object"""
        url = "https://www.googleapis.com/youtube/v3/videos?"\
            "part=contentDetails,snippet&id={}&fields="\
            "items(contentDetails%2Fduration%2Csnippet(channelTitle%2Ctitle))"\
            "&key={}"
        self.logger.info("Looking up id {}".format(video_id))
        info = requests.get(
            url=url.format(video_id, self.apikey),
            headers=self.headers)

        if info.status_code != 200:
            self.logger.info(f"get_video_info: Got {info.status_code} expected 200")
            return None
        else:
            try:
                info = info.json()["items"][0]
            except KeyError as err:
                self.logger.info(err)
                return None
            else:
                video = Video(
                    id = video_id,
                    title = info["snippet"]["title"],
                    channel = info["snippet"]["channelTitle"],
                    duration = info["contentDetails"]["duration"])
                if self.settings["include_channel"]:
                    video.title = f"{video.title} - {video.channel}"
                return video

    async def find_playlist_id(self, query: str) -> str:
        """Similarly to find_video_id, but for playlist
        returns the videoId as a string"""
        url = "https://www.googleapis.com/youtube/v3/search?part=snippet&"\
            "type=playlist&q={}&maxResults=1&key={}"
        self.logger.info(f"find_playlist_id: GET {url}")
        search = requests.get(
            url=url.format(query, self.apikey),
            headers=self.headers)

        if search.status_code != 200:
            self.logger.info(f"find_playlist_id: Got {info.status_code} expected 200")
            return None
        else:
            try:
                playlist_id = search.json()["items"][0]["id"]["playlistId"]
            except KeyError as err:
                self.logger.info(err)
                return None
            else:
                playlist = await self.get_playlist_info(playlist_id=playlist_id)
                return playlist

    async def get_playlist_info(self, playlist_id: str) -> list:
        """Uses the playlistId with the API and iterates over the items
        in the playlist, running `get_video_info()` for each videoId
        it find
        returns a list of Video objects
        """
        # TODO pagination
        max = self.settings["playlist_max"]
        url = "https://www.googleapis.com/youtube/v3/playlistItems?" \
                          "playlistId={}&part=snippet,id&key={}"
        if max > 0 and max <= 50:
            url+="&maxResults={}".format(self.settings["playlist_max"])
        else:
            url+="&maxResults=50"
        self.logger.info(f"get_playlist_info: GET {url}")
        info = requests.get(
            url.format(playlist_id, self.apikey),
            headers=self.headers)

        if info.status_code != 200:
            self.logger.info(f"get_playlist_info: Got {info.status_code} expected 200")
            return None
        else:
            try:
                items = info.json()["items"]
            except KeyError as err:
                self.logger.info(err)
                return None
            else:
                # TODO consider handling these in parallel
                playlist_items = []
                for item in items:
                    await asyncio.sleep(0.3)
                    id = item["snippet"]["resourceId"]["videoId"]
                    video = await self.get_video_info(video_id=id)
                    playlist_items.append(video)
                return playlist_items

