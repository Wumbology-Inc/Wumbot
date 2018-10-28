import logging
import typing

import aiohttp
import requests


class SpaceXAPI:
    @staticmethod
    async def async_get(
        endpoint: str = "", method: str = "", query: typing.Dict = {}
    ) -> typing.Tuple:
        """Asynchronous GET request to the SpaceX API
        Parameters
        ----------
            endpoint : str
                The endpoint for the request
            method : str
                The method used for the request
            query : dict
                A dictionary representation of query string options
        Returns
        -------
            tuple
                returns the response body and headers, both as `dict`
        """
        requestURL = SpaceXAPI._buildURL(endpoint, method)

        logging.info(f"Making query to: {requestURL}")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                requestURL, params=query, raise_for_status=True
            ) as resp:
                logging.info("Successful response received")
                return await resp.json(), resp.headers

    @staticmethod
    def get(
        endpoint: str = "", method: str = "", query: typing.Dict = {}
    ) -> typing.Tuple:
        """GET request to the SpaceX API
        Parameters
        ----------
            endpoint : str
                The endpoint for the request
            method : str
                The method used for the request
            query : dict
                A dictionary representation of query string options
        Returns
        -------
            tuple
                returns the response body and headers, both as `dict`
        """
        requestURL = SpaceXAPI._buildURL(endpoint, method)

        logging.info(f"Making query to: {requestURL}")
        r = requests.get(requestURL, params=query)

        if not r.ok:
            r.raise_for_status()

        logging.info("Successful response received")
        return r.json(), r.headers

    @staticmethod
    def _buildURL(
        endpoint: str, method: str, baseURL: str = "https://api.spacexdata.com/v3"
    ) -> str:
        """Build the SpaceX API Query URL, as :class:`str`

        Parameters
        ----------
        endpoint : str
            The endpoint for the request
        method : str
            The method for the request
        baseURL : str
            Base SpaceX API URL

            Defaults to the V3 URL: https://api.spacexdata.com/v3/
        """
        return f"{baseURL}/{endpoint}/{method}"
