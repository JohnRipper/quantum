import requests

from lib.cog import Cog
from lib.command import makeCommand, Command


class Movie(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.settings = self.bot.settings["module"]["movie"]
        # set base url for each query for brevity
        self.search_url = "https://api.themoviedb.org/3/search/multi?api_key={apikey}&query={query}"
        self.movie_url = ""
        self.tv_url = ""
        # works abit like youtube, general search then another request using an ID
        self.id_url = "https://api.themoviedb.org/3/{media_type}/{id}/{apikey}"

    @makeCommand(name="imdb", description="<query> search The Movie Db for TV and movies")
    async def search(self, query):
        # TODO handle years in query
        query = requests.utils.quote(query)
        response = await self.apiget(
            self.search_url.format(self.settings["key"], query)
        )
        if response is None or "results" not in response:
            await self.bot.send_message("Couldn't find that m8")
        elif len(response["results"]) == 0:
            await self.bot.send_message("Couldn't find that m8")
        else:
            info = await self.apiget(
                self.id_url.format(**query["results"][0])
            )
            if query["results"][0]["media_type"] == "movie":
                await self.bot.send_message(
                    self.formatresponse(info, is_movie=True)
                )
            else:
                await self.bot.send_message(
                    self.formatresponse(info, is_movie=False)
                )
    # TODO
    @makeCommand(name="movie", description="<query> search The Movie Db for Movies")
    async def movie_search(self, query):
        pass
    # TODO
    @makeCommand(name="tv", description="<query> search The Movie Db for TV shows")
    async def tv_search(self, query):
        pass

    async def apiget(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        else:
            # pretty sure tmdb only returns empty results{}, never a proper status code
            # unless the URL is malformed, which shouldn't happen after query=
            self.bot.warning(f"themoviedb {r.status_code}")
            return None

    def formatresponse(self, info: dict, is_movie: bool):
        if is_movie:
            response = """
            {original_title} ({}release_date})\n
            Rating: {vote_average}\n
            —https://imdb.com/title/{imdb_id}\n
            —{overview}
            """.format(**info)
        else:
            response = """
            {original_name} ({first_air_date}\n
            Rating: {vote_average})\n
            Episodes: {episode_run_time[0]}\n
            —{overview}
            """.format(**info)
        return response

