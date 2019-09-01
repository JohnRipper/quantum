import pytz
from datetime import datetime

import requests

from lib.cog import Cog
from lib.command import makeCommand, Command

# shamelessly stolen
"""
MIT License

Copyright (c) 2018 Jotham Read

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
# https://github.com/jotham/sopel-wundertime/blob/master/wundertime.py


class WunderTime(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.base_url = "http://autocomplete.wunderground.com/aq?query={}"

    @makeCommand(name="time", description= "<location> show local time for search")
    async def time(self, c: Command):
        if len(c.message) >= 3:
            results = await self.find_time(c.message.strip())
            if results:
                await self.bot.send_message("Time for {} is {} ({})".format(*results[0]))

    async def find_time(self, location):
        location = requests.utils.quote(location)
        query = requests.get(self.base_url.format(location)).json()
        results = []
        for location in query['RESULTS']:
            try:
                local_tz = pytz.timezone(location['tz'])
            except pytz.exceptions.UnknownTimeZoneError:
                # Couldn't find the location
                next
            else:
                results.append([
                    location['name'],
                    datetime.now(local_tz).strftime('%c'),
                    location['tzs']
                ])
            return results

