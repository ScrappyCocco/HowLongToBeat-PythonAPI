# ---------------------------------------------------------------------
# IMPORTS

import aiohttp
import requests
import re
import html
from enum import Enum
from fake_useragent import UserAgent


# ---------------------------------------------------------------------

class SearchModifiers(Enum):
    NONE = ""
    # INCLUDE_DLC is left, but should NO LONGER make a difference. HowLongToBeat re-added DLC in standard requests
    INCLUDE_DLC = "show_dlc"
    # ISOLATE_DLC shows only DLC in the search result
    ISOLATE_DLC = "only_dlc"
    # HIDE_DLC hide DLCs in the search result
    HIDE_DLC = "hide_dlc"


class HTMLRequests:
    BASE_URL = 'https://howlongtobeat.com/'
    SEARCH_URL = BASE_URL + "search_results.php"
    GAME_URL = BASE_URL + "game.php?id="

    @staticmethod
    def send_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE):
        """
        Function that search the game using a normal request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        ua = UserAgent()
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'User-Agent': ua.random
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
            'detail': search_modifiers.value
        }
        # Make the post request and return the result if is valid
        r = requests.post(HTMLRequests.SEARCH_URL, data=payload, headers=headers)
        if r is not None and r.status_code == 200:
            return r.text
        else:
            return None

    @staticmethod
    async def send_async_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE):
        """
        Function that search the game using an async request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        ua = UserAgent()
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'User-Agent': ua.random
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
            'detail': search_modifiers.value
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
        @param game_title: The HowLongToBeat page title of the game
        (For example "How long is A Way Out? | HowLongToBeat")
        @return: The cut game-title, without howlongtobeat names and grammatical symbols
        (So, in this example: "A Way Out")
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
        @param game_id: id of the game to get the title
        @return: The game title from the given id
        """

        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }

        url_get = HTMLRequests.GAME_URL + str(game_id)

        # Request and extract title
        contents = requests.get(url_get, headers=headers)
        return HTMLRequests.__cut_game_title(contents.text)

    @staticmethod
    async def async_get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        @param game_id: id of the game to get the title
        @return: The game title from the given id
        """

        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }

        url_get = HTMLRequests.GAME_URL + str(game_id)

        # Request and extract title
        async with aiohttp.ClientSession() as session:
            async with session.post(url_get, headers=headers) as resp:
                if resp is not None and str(resp.status) == "200":
                    text = await resp.text()
                    return HTMLRequests.__cut_game_title(text)
                else:
                    return None
