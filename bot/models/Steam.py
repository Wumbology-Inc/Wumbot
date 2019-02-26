import re
import typing
from datetime import datetime

import aiohttp
import requests
from yarl import URL


class SteamNewsPost:
    def __init__(
        self,
        gid: str = None,
        title: str = None,
        url: str = None,
        is_external_url: bool = None,
        author: str = None,
        contents: str = None,
        feedlabel: str = None,
        date: int = None,
        feedname: str = None,
        feed_type: int = None,
        appid: int = None,
    ):
        """
        Helper object to represent a Steam news post

        URLs are stripped from the contents string on instantiation
        """
        self.gid = gid
        self.title = title
        self.url = URL(url)
        self.is_external_url = is_external_url
        self.author = author
        self.contents = self._stripURL(contents)
        self.feedlabel = feedlabel
        self.date = datetime.fromtimestamp(date)
        self.feedname = feedname
        self.feed_type = feed_type
        self.appid = appid

    def __repr__(self):
        return (
            f"<SteamNews> \"{self.title}\" Posted {datetime.strftime(self.date, '%Y-%m-%d')} "
            f"by {self.author}"
        )

    @staticmethod
    async def asyncgetnewsforapp(
        appID: int = 582_010,
        count: int = 10,
        maxlength: int = 300,
        format: str = "json",
        **kwargs,
    ) -> typing.List:
        """
        This function is a coroutine

        Retrieve Steam news posts for the input appID

        Additional keyword arguments are accepted but not used to generate the API query

        Results are returned as a list of SteamNewsPost objects
        """
        apiURL = URL("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/")

        paramdict = {
            "appID": appID,
            "count": count,
            "maxlength": maxlength,
            "format": format,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(apiURL.with_query(paramdict)) as resp:
                rawdict = await resp.json()

        if rawdict["appnews"] and rawdict["appnews"]["newsitems"]:
            return [SteamNewsPost(**item) for item in rawdict["appnews"]["newsitems"]]

    @staticmethod
    def getnewsforapp(
        appID: int = 582_010,
        count: int = 10,
        maxlength: int = 300,
        format: str = "json",
        **kwargs,
    ) -> typing.List:
        """
        Retrieve Steam news posts for the input appID

        Additional keyword arguments are accepted but not used to generate the API query

        Results are returned as a list of SteamNewsPost objects
        """
        apiURL = URL("https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/")

        paramdict = {
            "appID": appID,
            "count": count,
            "maxlength": maxlength,
            "format": format,
        }
        r = requests.get(apiURL.with_query(paramdict))
        rawdict = r.json()

        if rawdict["appnews"] and rawdict["appnews"]["newsitems"]:
            return [SteamNewsPost(**item) for item in rawdict["appnews"]["newsitems"]]

    @staticmethod
    def _stripURL(instr: str) -> str:
        """
        Strip URLs out of instr using a basic regex
        """
        exp = r"https?:\/\/[\w\-\.\/]+\s?"
        return re.sub(exp, "", instr)
