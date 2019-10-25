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



class Webcam(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.candidates = []
        self.pc = RTCPeerConnection()
        self.connection = aioice.Connection(ice_controlling=True, )
        self.stun_server = None
        self.cammed = False

        # using a physical cam, almost no lag.
        # options = {"volume": "33"}
        # player = MediaPlayer("/dev/video0", format="v4l2", options=options)

        # screen grab. laggy.

        self.options = {"volume": "33", "video_size": "640x480"}
        self.player = MediaPlayer("/dev/video2", format="v4l2", options=self.options)

        if self.player and self.player.audio:
            self.pc.addTrack(self.player.audio)
        if self.player and self.player.video:
            self.pc.addTrack(self.player.video)

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % self.pc.iceConnectionState)

            if self.pc.iceConnectionState == "failed":
                await self.pc.close()

            if self.pc.iceConnectionState == 'completed':
                print("completed")



    #############################
    # Events
    #############################

    async def iceservers(self, data):
        # get ice servers
        # {"req":216,"servers":["stun:192.95.35.254:47089","stun:167.114.164.149:26178"],"success":true,"tc":"iceservers"}
        await self.offer(data)

    async def publish(self, data):
        # cawe dont await self.subscribe(data['handle'])
        return

    async def unpublish(self, data):
        return

    async def sdp(self, data):
        if data["type"] == "offer":
            # other people cam up and sendoffers
            return

        if data["type"] == "answer":
                print(data)
                if data["success"]:

                    d = RTCSessionDescription(type="answer", sdp=data["sdp"])
                    await self.pc.setRemoteDescription(d)
                    self.connection.remote_password = ""
                    self.connection.remote_username = ""
                    asyncio.ensure_future(self.connection.connect(), loop=asyncio.get_event_loop())



    async def stream_closed(self, data):
        # await self.bot.wsend(json.dumps({"tc": "subscribe", "req": 2, "handle": data['handle']}))
        return

    async def stream_connected(self, data):
        return

    #############################
    # Commands
    #############################
    @makeCommand(name='cam' , description='attempts to cam up')
    async def cam(self, c: Command):
        # get ice servers
        await self.bot.wsend(json.dumps({"tc": "getice", "req": self.get_req()}))

    @makeCommand(name='endcam', description='cams down')
    async def endcam(self, c: Command):
        # get ice servers
        await self.bot.wsend(json.dumps({"handle": self.bot.handle, "tc": "unpublish"}))

    #############################
    # class methods
    #############################

    async def close_stream(self, handle_id):
        self.bot.wsend(json.dumps({"tc": "stream_close", "req": self.get_req(), "handle": handle_id}))

    async def subscribe(self, handle_id):
        if handle_id != self.bot.handle:
            await self.bot.wsend(json.dumps({"tc": "subscribe", "req": self.get_req(), "handle": handle_id}))

    async def offer(self, data):
        s_server = data['servers'][0].split(":")

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
            print(data)
            await self.bot.wsend(json.dumps(data))

    async def get_ice(self):
        await self.bot.wsend(json.dumps({'tc': 'getice', 'req': self.get_req()}))
