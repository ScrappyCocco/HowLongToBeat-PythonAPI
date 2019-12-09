# ---------------------------------------------------------------------
# IMPORTS

import aiohttp
import requests
import re
import html


# ---------------------------------------------------------------------


class HTMLRequests:
    BASE_URL = 'https://howlongtobeat.com/'
    SEARCH_URL = BASE_URL + "search_results.php"
    GAME_URL = BASE_URL + "game.php?id="

    @staticmethod
    def send_web_request(game_name: str):
        """
        Function that search the game using a normal request
        :param game_name: The original game name received as input
        :return The HTML code of the research if the request returned 200(OK), None otherwise
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
        r = requests.post(HTMLRequests.SEARCH_URL, data=payload, headers=headers)
        if r is not None and r.status_code == 200:
            return r.text
        else:
            return None

    @staticmethod
    async def send_async_web_request(game_name: str):
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
            async with session.post(HTMLRequests.SEARCH_URL, data=payload, headers=headers) as resp:
                if resp is not None and str(resp.status) == "200":
                    return await resp.text()
                else:
                    return None

    @staticmethod
    def __cut_game_title(game_title: str):
        """
        Function that extract the game title from the html title of the howlongtobeat page
        :param game_title: The HowLongToBeat page title of the game
        For example "How long is A Way Out? | HowLongToBeat"
        :return The cut game-title, without howlongtobeat names and grammatical symbols
        So, in this example: "A Way Out"
        """

        if game_title is None or len(game_title) == 0:
            return None

        title = re.search("<title>([\w\W]*)<\/title>", game_title)
        # The position of start and end of this method may change if the website change
        cut_title = str(html.unescape(title.group(1)[12:-17]))
        return cut_title

    @staticmethod
    def get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        :param game_id: id of the game to get the title
        :return The game title from the given id
        """

        url_get = HTMLRequests.GAME_URL + str(game_id)

        # Request and extract title
        contents = requests.get(url_get)
        return HTMLRequests.__cut_game_title(contents.text)

    @staticmethod
    async def async_get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        :param game_id: id of the game to get the title
        :return The game title from the given id
        """

        url_get = HTMLRequests.GAME_URL + str(game_id)

        # Request and extract title
        async with aiohttp.ClientSession() as session:
            async with session.post(url_get) as resp:
                if resp is not None and str(resp.status) == "200":
                    text = await resp.text()
                    return HTMLRequests.__cut_game_title(text)
                else:
                    return None
