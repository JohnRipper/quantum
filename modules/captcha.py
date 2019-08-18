from python_anticaptcha import NoCaptchaTaskProxylessTask, AnticatpchaException, AnticaptchaClient

from lib.cog import Cog
import json

class Captcha(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.captcha_client = AnticaptchaClient(self.bot.settings['captcha_key'])

    async def captcha(self, data: dict):
        await self.do_captcha(key=data['key'])

    async def do_captcha(self, key: str):
        print('captcha required, attempting to solve.')
        try:
            task = NoCaptchaTaskProxylessTask(
                'https://www.tinychat.com/room/%s' % self.bot.settings['room'], key)
            job = self.captcha_client.createTask(task)
            job.join()
            payload = {
                'tc': 'captcha',
                'req': 1,
                'token': job.get_solution_response()
            }
            await self.bot.ws.send(json.dumps(payload))
        except AnticatpchaException as e:
            raise
