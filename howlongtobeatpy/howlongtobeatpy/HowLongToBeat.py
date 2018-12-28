# ---------------------------------------------------------------------
# IMPORTS

import aiohttp
import requests

from .HTMLResultParser import HTMLResultParser

# ---------------------------------------------------------------------


class HowLongToBeat:
    """
    Main class that contain the base "search" function
    The search function is available using standard request or using an async request that MUST be awaited
    """

    BASE_URL = 'https://howlongtobeat.com/'
    SEARCH_URL = BASE_URL + "search_main.php"
    GAME_URL = BASE_URL + "game.php?id="

    async def async_search(self, game_name: str):
        """
        Function that search the game using an async request
        :param game_name: The original game name received as input
        :return: A list of possible games
        """
        if game_name is None or len(game_name) == 0:
            return None
        html_result = await self.send_async_web_request(game_name)
        if html_result is not None:
            return self.parse_web_result(game_name, html_result)
        else:
            return None

    def search(self, game_name: str):
        """
        Function that search the game using a normal request
        :param game_name: The original game name received as input
        :return: A list of possible games
        """
        if game_name is None or len(game_name) == 0:
            return None
        html_result = self.send_web_request(game_name)
        if html_result is not None:
            return self.parse_web_result(game_name, html_result)
        else:
            return None

    def send_web_request(self, game_name: str):
        """
        Function that search the game using an async request
        :param game_name: The original game name received as input
        :return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*'
        }
        payload = {
            'queryString': game_name,
            't': 'games',
            'sorthead': 'popular',
            'sortd': 'Normal Order',
            'plat': '',
            'length_type': 'main',
            'length_min': '',
            'length_max': '',
            'detail': '0'
        }
        # Make the post request and return the result if is valid
        r = requests.post(self.SEARCH_URL, data=payload, headers=headers)
        if r is not None and r.status_code == 200:
            return r.text
        else:
            return None

    async def send_async_web_request(self, game_name: str):
        """
        Function that search the game using an async request
        :param game_name: The original game name received as input
        :return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*'
        }
        payload = {
            'queryString': game_name,
            't': 'games',
            'sorthead': 'popular',
            'sortd': 'Normal Order',
            'plat': '',
            'length_type': 'main',
            'length_min': '',
            'length_max': '',
            'detail': '0'
        }
        # Make the post request and return the result if is valid
        async with aiohttp.ClientSession() as session:
            async with session.post(self.SEARCH_URL, data=payload, headers=headers) as resp:
                if resp is not None and str(resp.status) == "200":
                    return await resp.text()
                else:
                    return None

    def parse_web_result(self, game_name: str, html_result):
        """
        Function that call the HTML parser to get the data
        :param game_name: The original game name received as input
        :param html_result: The HTML received from the request
        :return: A list of possible games
        """
        parser = HTMLResultParser(game_name, self.GAME_URL)
        parser.feed(html_result)
        return parser.results
