import asyncio
import json
import aioice
from aiortc.contrib.media import MediaPlayer
from aiortc import (
    RTCPeerConnection,
    RTCSessionDescription,
)
from lib.cog import Cog
from lib.command import makeCommand, Command
from threading import Thread






class Webcam(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.candidates = []
        self.pc = RTCPeerConnection()
        self.connection = aioice.Connection(ice_controlling=True)
        self.stun_server = None
        self.cammed = False

        @self.pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print("ICE connection state is %s" % self.pc.iceConnectionState)

            if self.pc.iceConnectionState == "failed":
                await self.pc.close()
            if self.pc.iceGatheringState == 'complete':
                return

    #############################
    # Events
    #############################

    async def iceservers(self, data):
        # get ice servers
        # {"req":216,"servers":["stun:192.95.35.254:47089","stun:167.114.164.149:26178"],"success":true,"tc":"iceservers"}
        await self.offer(data)

    async def publish(self, data):
        await self.subscribe(data['handle'])

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
                    await self.connection.connect()

    async def stream_closed(self, data):
        await self.bot.ws.send(json.dumps({"tc": "subscribe", "req": 2, "handle": data['handle']}))

    async def stream_connected(self, data):
        return

    #############################
    # Commands
    #############################
    @makeCommand(name='cam' , description='attempts to cam up')
    async def cam(self, c: Command):
        # get ice servers
        await self.bot.ws.send(json.dumps({"tc": "getice", "req": 216}))

    #############################
    # class methods
    #############################

    async def close_stream(self, handle_id):
        self.bot.ws.send(json.dumps({"tc":"stream_close","req":215,"handle": handle_id}))

    async def subscribe(self, handle_id):
        await self.bot.ws.send(json.dumps({"tc":"subscribe","req":2,"handle": handle_id}))

    async def offer(self, data):
        s_server = data['servers'][0].split(":")
        STUN_SERVER = (s_server[1], int(s_server[2]))
        self.connection.stun_server = STUN_SERVER
        self.stun_server = STUN_SERVER
        await self.connection.gather_candidates()

        options = {"framerate": "30", "video_size": "1920x1080"}
        player = MediaPlayer("/dev/video0", format="v4l2", options=options)
        if player and player.audio:
            self.pc.addTrack(player.audio)
        if player and player.video:
            self.pc.addTrack(player.video)

        await self.pc.setLocalDescription(await self.pc.createOffer())
        data = {
            "tc": "sdp",
            "req": 420,
            "type": "offer",
            "sdp": self.pc.localDescription.sdp,
            "handle": 0
        }
        print(data)
        await self.bot.ws.send(json.dumps(data))
        for c in self.connection.local_candidates:
            data = {
                "tc": "trickle",
                "req": 420,
                "candidate": "candidate:" + aioice.Candidate.to_sdp(c),
                "handle": self.bot.handle
            }
            print(data)
            await self.bot.ws.send(json.dumps(data))

    async def get_ice(self):
        await self.bot.ws.send(json.dumps({'tc': 'getice', 'req':1}))



