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
    ORIGIN_HEADER = 'https://howlongtobeat.com'
    REFERER_HEADER = BASE_URL
    SEARCH_URL = BASE_URL + "search_results"
    GAME_URL = BASE_URL + "game"

    @staticmethod
    def get_search_request_parameters(page: int):
        """
        Generate the parameters for the search request
        @param page: The page to search
        @return: The parameters object for the request
        """
        params = {
            'page': str(page)
        }
        return params

    @staticmethod
    def get_search_request_headers():
        """
        Generate the headers for the search request
        @return: The headers object for the request
        """
        ua = UserAgent()
        headers = {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'User-Agent': ua.random,
            'origin': HTMLRequests.ORIGIN_HEADER,
            'referer': HTMLRequests.REFERER_HEADER
        }
        return headers

    @staticmethod
    def get_search_request_data(game_name: str, search_modifiers: SearchModifiers):
        """
        Generate the data payload for the search request
        @param game_name: The name of the game to search
        @param search_modifiers: The search modifiers to use in the search
        @return: The request (data) payload object for the request
        """
        payload = {
            'queryString': game_name,
            't': 'games',
            'sorthead': 'popular',
            'sortd': 'Normal Order',
            'plat': '',
            'length_type': 'main',
            'length_min': '',
            'length_max': '',
            'detail': search_modifiers.value,
            'v': '',
            'f': '',
            'g': '',
            'randomize': '0'
        }
        return payload

    @staticmethod
    def send_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE, page: int = 1):
        """
        Function that search the game using a normal request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param page: The page to explore of the research, unknown if this is actually used
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        params = HTMLRequests.get_search_request_parameters(page)
        headers = HTMLRequests.get_search_request_headers()
        payload = HTMLRequests.get_search_request_data(game_name, search_modifiers)
        # Make the post request and return the result if is valid
        resp = requests.post(HTMLRequests.SEARCH_URL, params=params, headers=headers, data=payload)
        if resp.status_code == 200:
            return resp.text
        else:
            return None

    @staticmethod
    async def send_async_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE, page: int = 1):
        """
        Function that search the game using an async request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param page: The page to explore of the research, unknown if this is actually used
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        params = HTMLRequests.get_search_request_parameters(page)
        headers = HTMLRequests.get_search_request_headers()
        payload = HTMLRequests.get_search_request_data(game_name, search_modifiers)
        # Make the post request and return the result if is valid
        async with aiohttp.ClientSession() as session:
            async with session.post(HTMLRequests.SEARCH_URL, params=params, headers=headers, data=payload) as resp:
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

        title = re.search("<title>(.*)<\/title>", game_title)
        # The position of start and end of this method may change if the website change
        cut_title = str(html.unescape(title.group(1)[12:-17]))
        return cut_title

    @staticmethod
    def get_title_request_parameters(game_id: int):
        """
        enerate the parameters for the search request
        @param game_id: The game id to search in HLTB
        @return: The parameters object for the request
        """
        params = {
            'id': str(game_id)
        }
        return params

    @staticmethod
    def get_title_request_headers():
        """
        Generate the headers for the search request
        @return: The headers object for the request
        """
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random,
            'referer': HTMLRequests.REFERER_HEADER
        }
        return headers

    @staticmethod
    def get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        @param game_id: id of the game to get the title
        @return: The game title from the given id
        """

        params = HTMLRequests.get_title_request_parameters(game_id)
        headers = HTMLRequests.get_title_request_headers()

        # Request and extract title
        contents = requests.get(HTMLRequests.GAME_URL, params=params, headers=headers)
        return HTMLRequests.__cut_game_title(contents.text)

    @staticmethod
    async def async_get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        @param game_id: id of the game to get the title
        @return: The game title from the given id
        """

        params = HTMLRequests.get_title_request_parameters(game_id)
        headers = HTMLRequests.get_title_request_headers()

        # Request and extract title
        async with aiohttp.ClientSession() as session:
            async with session.post(HTMLRequests.GAME_URL, params=params, headers=headers) as resp:
                if resp is not None and str(resp.status) == "200":
                    text = await resp.text()
                    return HTMLRequests.__cut_game_title(text)
                else:
                    return None
