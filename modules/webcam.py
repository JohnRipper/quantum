import asyncio
import json
from dataclasses import dataclass

import aioice
from aiortc.contrib.media import MediaPlayer
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
)
from lib.cog import Cog
from lib.command import makeCommand, Command
import ffmpeg
from enum import Enum


class SupportedFormats(Enum):
    NONE = 0
    HTTPS = 1
    MP4 = 2
    DESKTOP = 3


class Types(Enum):
    NONE = 0
    HTTPS = 1
    MP4 = 2
    DESKTOP = 3


@dataclass
class Video:
    type: Types = 0
    frame_rate: int = 30
    threads: int = 0
    is_playing: bool = False

    # http type
    url: str = ""

    # local movie type
    name: str = ""

    # desktop
    # todo expirement with getting available displays
    x_display: str = ":0.0"
    width: int = 10
    height: int = 10
    x_offset: int = 0
    y_offset: int = 0
    out_location: str = "/dev/video2"


class Webcam(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.candidates = []
        self.pc = None
        self.connection = None
        self.stun_server = None
        self.ffmpeg_process = None
        self.video = Video()
        self.player = None

    #############################
    # Events
    #############################

    async def iceservers(self, data):
        # get ice servers
        # {"req":216,"servers":["stun:192.95.35.254:47089","stun:167.114.164.149:26178"],"success":true,"tc":"iceservers"}
        await self.offer(data)

    async def publish(self, data):
        # await self.subscribe(data['handle'])
        return

    async def unpublish(self, data):
        return

    async def sdp(self, data):
        if data["type"] == "offer":
            # other people cammed up and sent offers
            return

        if data["type"] == "answer":
            if data["success"]:
                d = RTCSessionDescription(type="answer", sdp=data["sdp"])
                await self.pc.setRemoteDescription(d)
                self.connection.remote_password = ""
                self.connection.remote_username = ""
                asyncio.ensure_future(self.connection.connect(), loop=asyncio.get_event_loop())

    async def stream_closed(self, data):
        # await self.bot.wsend(json.dumps({"tc": "subscribe", "req": 2, "handle": data['handle']}))
        if data["handle"] == self.bot.handle:
            await self.connection.close()
            await self.pc.close()
            await self.get_ffmpeg_ready()
            self.player = None

    async def stream_connected(self, data):
        return

    #############################
    # Commands
    #############################

    @makeCommand(name='camlink', description='attempts to cam up')
    async def camlink(self, c: Command):
        self.video.type = Types.HTTPS
        if c.message == "":
            await self.send_message("link required bro/bronette.")
            return
        self.video.url = c.message
        await self.start_camming_process()

    @makeCommand(name='camd', description='attempts to cam up from a linux desktop')
    async def camDesktop(self, c: Command):
        # only works on linux.
        self.video.type = Types.HTTPS
        await self.get_ffmpeg_ready()
        if c.message != "":
            # todo setup arg parse
            self.video.x_offset = c.message
        else:
            # ffmpeg -f x11grab -r 15 -s 140x70 -i :0.0+1920,0 -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video2
            self.ffmpeg_process = (
                ffmpeg.input(f":0.0+{self.video.x_offset},{self.video.y_offset}", format='x11grab',
                             s=f"{self.video.height}x{self.video.width}")
                    .output('/dev/video2', format='v4l2', pix_fmt='yuv420p')
                    .overwrite_output()
                    .run_async(pipe_stdin=True)
            )

        await self.start_camming_process()

    @makeCommand(name='cam', description='attempts to cam up')
    async def cam(self, c: Command):
        # get ice servers
        await self.get_ffmpeg_ready()
        await self.bot.wsend(json.dumps({"tc": "getice", "req": self.get_req()}))

    @makeCommand(name='endcam', description='cams down')
    async def endcam(self, c: Command):
        # get ice servers
        await self.close_stream(self.bot.handle)

    #############################
    # class methods
    #############################
    async def get_ffmpeg_ready(self):
        if not self.video.is_playing:
            # no video is playing but process is alive. kill it.
            if self.ffmpeg_process:
                self.ffmpeg_process.kill()

    async def start_camming_process(self):
        await self.bot.wsend(json.dumps({"tc": "getice", "req": self.get_req()}))

    async def close_stream(self, handle_id):
        await self.bot.wsend(json.dumps({"tc": "stream_close", "req": self.get_req(), "handle": handle_id}))

    async def subscribe(self, handle_id):
        if handle_id != self.bot.handle:
            await self.bot.wsend(json.dumps({"tc": "subscribe", "req": self.get_req(), "handle": handle_id}))

    async def offer(self, data):
        s_server = data['servers'][0].split(":")
        self.pc = RTCPeerConnection()
        self.connection = aioice.Connection(ice_controlling=True, )
        # todo play with other extensions

        if self.video.type == Types.HTTPS:
            options = {"volume": "33", "video_size": "640x480"}
            self.player = MediaPlayer(self.video.url, format="mp4", options=options)

        elif self.video.type == Types.DESKTOP:
            options = {"volume": "33", "video_size": f"{self.video.height}x{self.video.width}"}
            self.player = MediaPlayer(self.video.out_location, format="v4l2", options=options)

        if self.player and self.player.audio:
            self.pc.addTrack(self.player.audio)
        if self.player and self.player.video:
            self.pc.addTrack(self.player.video)

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % self.pc.iceConnectionState)

            if self.pc.iceConnectionState == "failed":
                await self.pc.close()
                await self.connection.close()

            if self.pc.iceConnectionState == 'completed':
                print("completed")

        STUN_SERVER = (s_server[1], int(s_server[2]))
        self.connection.stun_server = STUN_SERVER
        self.stun_server = STUN_SERVER
        await self.connection.gather_candidates()

        await self.pc.setLocalDescription(await self.pc.createOffer())
        data = {
            "tc": "sdp",
            "req": self.get_req(),
            "type": "offer",
            "sdp": self.pc.localDescription.sdp,
            "handle": 0
        }
        await self.bot.wsend(json.dumps(data))
        for c in self.connection.local_candidates:
            data = {
                "tc": "trickle",
                "req": self.get_req(),
                "candidate": "candidate:" + aioice.Candidate.to_sdp(c),
                "handle": self.bot.handle
            }
            await self.bot.wsend(json.dumps(data))

    async def get_ice(self):
        await self.bot.wsend(json.dumps({'tc': 'getice', 'req': self.get_req()}))
