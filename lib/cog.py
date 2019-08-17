import logging


class Cog:

    def __init__(self, bot):
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.bot = bot

    async def on_message(self, data: dict):
        self.logger.info(f"on_message: {data}")

    async def on_ready(self, data: dict):
        self.logger.info(f"on_ready: {data}")
