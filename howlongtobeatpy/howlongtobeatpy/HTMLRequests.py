# ---------------------------------------------------------------------
# IMPORTS

import json
import re
import time
from enum import Enum

import aiohttp
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# ---------------------------------------------------------------------


class SearchModifiers(Enum):
    NONE = ""
    # ISOLATE_DLC shows only DLC in the search result
    ISOLATE_DLC = "only_dlc"
    # ISOLATE_MODS shows only MODs
    ISOLATE_MODS = "only_mods"
    # ISOLATE_HACKS shows only Hacks
    ISOLATE_HACKS = "only_hacks"
    # HIDE_DLC hide DLCs/MODs in the search result
    HIDE_DLC = "hide_dlc"


class SearchInformations:
    search_url = None

    def __init__(self, script_content: str):
        self.search_url = self.__extract_search_url_script(script_content)
        if HTMLRequests.BASE_URL.endswith("/") and self.search_url is not None:
            self.search_url = self.search_url.lstrip("/")
    
    def __extract_search_url_script(self, script_content: str):
        """
        Function that finds the 'fetch' call using 'method: "POST"', 
        extracts the base endpoint path, and returns the full '/api/path' 
        string (e.g., "/api/search" or "/api/finder").
        
        This avoids relying on the exact string by confirming 
        the use of the POST method, which identifies the actual search endpoint.
        
        @return: The full API endpoint string (e.g., "/api/search") or None.
        """
        # Pattern explanation:
        # 1. Capture Group 1: Matches the path suffix (e.g., "search", "find", "finder").
        # 2. Ensures the request options contain 'method: "POST"' to filter out the GET init call.
        pattern = re.compile(
            # Capture Group 1: The path suffix after /api/ (e.g., "search", "find", "finder")
            r'fetch\s*\(\s*["\']/api/([a-zA-Z0-9_/]+)[^"\']*["\']\s*,\s*{[^}]*method:\s*["\']POST["\'][^}]*}',
            re.DOTALL | re.IGNORECASE
        )
        
        match = pattern.search(script_content)
        
        if match:
            # Example captured string: "search", "find", "finder", or "find/v2"
            path_suffix = match.group(1)
            
            # Determine the root path (e.g., "search" from "search/v2")
            # This ensures we get the base endpoint name even if sub-paths are used.
            if '/' in path_suffix:
                base_path = path_suffix.split('/')[0]
            else:
                base_path = path_suffix
            
            # Accept any endpoint variant (search, find, finder, etc.)
            full_endpoint = f"/api/{base_path}"
            return full_endpoint
                
        return None


class SearchAuthToken:
    search_url = "api/s"
    search_url_endpoint = "/init"
    auth_token = None
    auth_key = None
    auth_value = None

    def extract_auth_token_from_response(self, response_content: requests.Response):
        """
        Extract the auth token from the request
        @return: The auth token in the response json if present, also assigned to self.auth_token
        """
        data = response_content.json()
        return self.extract_auth_token_from_json(data)
    
    def extract_auth_token_from_json(self, json_content):
        self.auth_token = json_content.get('token')

        for field_name, field_value in json_content.items():
            lower = field_name.lower()
            if re.search(r'key', lower):
                self.auth_key = field_value
            elif re.search(r'val', lower):
                self.auth_value = field_value

        return self

class HTMLRequests:
    BASE_URL = 'https://howlongtobeat.com/'
    REFERER_HEADER = BASE_URL
    GAME_URL = BASE_URL + "game"
    # Static search url to use in case it can't be extracted from JS code
    SEARCH_URL = BASE_URL + "api/s/"

    @staticmethod
    def get_search_request_headers(auth_struct, user_agent):
        """
        Generate the headers for the search request
        @return: The headers object for the request
        """
        headers = {
            'content-type': 'application/json',
            'accept': '*/*',
            'User-Agent': user_agent,
            'Referer': HTMLRequests.REFERER_HEADER,
            'Origin': HTMLRequests.REFERER_HEADER
        }

        if auth_struct is not None:
            headers['x-auth-token'] = str(auth_struct.auth_token)
            headers['x-hp-key'] = str(auth_struct.auth_key)
            headers['x-hp-val'] = str(auth_struct.auth_value)

        return headers

    @staticmethod
    def get_search_request_data(game_name: str, search_modifiers: SearchModifiers, page: int, auth_struct):
        """
        Generate the data payload for the search request
        @param game_name: The name of the game to search
        @param search_modifiers: The search modifiers to use in the search
        @param page: The page to search
        @return: The request (data) payload object for the request
        """
        payload = {
            'searchType': "games",
            'searchTerms': game_name.split(),
            'searchPage': page,
            'size': 20,
            'searchOptions': {
                'games': {
                    'userId': 0,
                    'platform': "",
                    'sortCategory': "popular",
                    'rangeCategory': "main",
                    'rangeTime': {
                        'min': 0,
                        'max': 0
                    },
                    'gameplay': {
                        'perspective': "",
                        'flow': "",
                        'genre': "",
                        "difficulty": ""
                    },
                    'rangeYear':
                    {
                        'max': "",
                        'min': ""
                    },
                    'modifier': search_modifiers.value,
                },
                'users': {
                    'sortCategory': "postcount"
                },
                'lists': {
                    'sortCategory': "follows"
                },
                'filter': "",
                'sort': 0,
                'randomizer': 0
            },
            'useCache': True
        }

        if auth_struct is not None:
            payload[auth_struct.auth_key] = auth_struct.auth_value

        return json.dumps(payload)

    @staticmethod
    def send_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE,
                         page: int = 1):
        """
        Function that search the game using a normal request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param page: The page to explore of the research, unknown if this is actually used
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        # Generate a single user agent to use for the whole request
        ua = UserAgent()
        request_user_agent = ua.random.strip()
        # Retrieve the updated URL
        search_info_data = HTMLRequests.send_website_request_getcode(False, request_user_agent)
        if search_info_data is None or search_info_data.search_url is None:
            search_info_data = HTMLRequests.send_website_request_getcode(True, request_user_agent)
        # Retrieve the request auth token
        auth_struct = None
        if search_info_data is not None and search_info_data.search_url is not None:
            auth_struct = HTMLRequests.send_website_get_auth_token(search_info_data.search_url, request_user_agent)
        else:
            auth_struct = HTMLRequests.send_website_get_auth_token(None, request_user_agent)
        # Make the request
        headers = HTMLRequests.get_search_request_headers(auth_struct, request_user_agent)
        if search_info_data is not None and search_info_data.search_url is not None:
            HTMLRequests.SEARCH_URL = HTMLRequests.BASE_URL + search_info_data.search_url
        payload = HTMLRequests.get_search_request_data(game_name, search_modifiers, page, auth_struct)
        resp = requests.post(HTMLRequests.SEARCH_URL, headers=headers, data=payload, timeout=60)
        if resp.status_code == 200:
            return resp.text
        return None

    @staticmethod
    async def send_async_web_request(game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE,
                                     page: int = 1):
        """
        Function that search the game using an async request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param page: The page to explore of the research, unknown if this is actually used
        @return: The HTML code of the research if the request returned 200(OK), None otherwise
        """
        # Generate a single user agent to use for the whole request
        ua = UserAgent()
        request_user_agent = ua.random.strip()
        # Retrieve the updated URL
        search_info_data = HTMLRequests.send_website_request_getcode(False, request_user_agent)
        if search_info_data is None or search_info_data.search_url is None:
            search_info_data = HTMLRequests.send_website_request_getcode(True, request_user_agent)
        # Retrieve the request auth token
        auth_struct = None
        if search_info_data is not None and search_info_data.search_url is not None:
            auth_struct = await HTMLRequests.async_send_website_get_auth_token(search_info_data.search_url, request_user_agent)
        else:
            auth_struct = await HTMLRequests.async_send_website_get_auth_token(None, request_user_agent)
        # Make the request
        headers = HTMLRequests.get_search_request_headers(auth_struct, request_user_agent)
        if search_info_data is not None and search_info_data.search_url is not None:
            HTMLRequests.SEARCH_URL = HTMLRequests.BASE_URL + search_info_data.search_url
        payload = HTMLRequests.get_search_request_data(game_name, search_modifiers, page, auth_struct)
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession() as session:
            async with session.post(HTMLRequests.SEARCH_URL, headers=headers, data=payload, timeout=timeout) as resp_with_key:
                if resp_with_key is not None and resp_with_key.status == 200:
                    return await resp_with_key.text()
                else:
                    return None

    @staticmethod
    def __cut_game_title(page_source: str):
        """
        Function that extract the game title from the html title of the howlongtobeat page
        @param game_title: The HowLongToBeat page title of the game
        (For example "How long is A Way Out? | HowLongToBeat")
        @return: The cut game-title, without howlongtobeat names and grammatical symbols
        (So, in this example: "A Way Out")
        """

        if page_source is None or len(page_source) == 0:
            return None

        soup = BeautifulSoup(page_source, 'html.parser')
        title_tag = soup.title
        title_text = title_tag.string

        # The position of start and end of this method may change if the website change
        cut_title = title_text[12:-17].strip()
        return cut_title

    @staticmethod
    def get_title_request_parameters(game_id: int):
        """
        Generate the parameters for the search request
        @param game_id: The game id to search in HLTB
        @return: The parameters object for the request
        """
        params = {
            'id': str(game_id)
        }
        return params

    @staticmethod
    def get_title_request_headers(user_agent):
        """
        Generate the headers for the search request
        @return: The headers object for the request
        """
        headers = {
            'User-Agent': user_agent,
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

        # This is a request to get the game title so we can generate a UserAgent
        ua = UserAgent()
        request_user_agent = ua.random.strip()

        params = HTMLRequests.get_title_request_parameters(game_id)
        headers = HTMLRequests.get_title_request_headers(request_user_agent)

        # Request and extract title
        contents = requests.get(HTMLRequests.GAME_URL, params=params, headers=headers, timeout=60)
        return HTMLRequests.__cut_game_title(contents.text)

    @staticmethod
    async def async_get_game_title(game_id: int):
        """
        Function that gets the title of a game from the game (howlongtobeat) id
        @param game_id: id of the game to get the title
        @return: The game title from the given id
        """

        # This is a request to get the game title so we can generate a UserAgent
        ua = UserAgent()
        request_user_agent = ua.random.strip()

        params = HTMLRequests.get_title_request_parameters(game_id)
        headers = HTMLRequests.get_title_request_headers(request_user_agent)

        # Request and extract title
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession() as session:
            async with session.post(HTMLRequests.GAME_URL, params=params, headers=headers, timeout=timeout) as resp:
                if resp is not None and resp.status == 200:
                    text = await resp.text()
                    return HTMLRequests.__cut_game_title(text)
                return None

    @staticmethod
    def send_website_request_getcode(parse_all_scripts: bool, user_agent):
        """
        Function that send a request to howlongtobeat to scrape the correct search url
        @return: The search informations to use in the request
        """
        # Make the post request and return the result if is valid
        headers = HTMLRequests.get_title_request_headers(user_agent)
        resp = requests.get(HTMLRequests.BASE_URL, headers=headers, timeout=60)
        if resp.status_code == 200 and resp.text is not None:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(resp.text, 'html.parser')
            # Find all <script> tags with a src attribute containing the substring
            scripts = soup.find_all('script', src=True)
            if parse_all_scripts:
                matching_scripts = [script['src'] for script in scripts]
            else:
                matching_scripts = [script['src'] for script in scripts if '_app-' in script['src']]
            for script_url in matching_scripts:
                script_url = HTMLRequests.BASE_URL + script_url
                script_resp = requests.get(script_url, headers=headers, timeout=60)
                if script_resp.status_code == 200 and script_resp.text is not None:
                    search_info = SearchInformations(script_resp.text)
                    if search_info.search_url is not None:
                        return search_info
        return None

    @staticmethod
    async def async_send_website_request_getcode(parse_all_scripts: bool, user_agent):
        """
        Function that send a request to howlongtobeat to scrape the correct search url
        @return: The search informations to use in the request
        """
        # Make the post request and return the result if is valid
        headers = HTMLRequests.get_title_request_headers(user_agent)
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession() as session:
            async with session.get(HTMLRequests.BASE_URL, headers=headers, timeout=timeout) as resp:
                if resp is not None and resp.status == 200:
                    resp_text = await resp.text()
                    # Parse the HTML content using BeautifulSoup
                    soup = BeautifulSoup(resp_text, 'html.parser')
                    # Find all <script> tags with a src attribute containing the substring
                    scripts = soup.find_all('script', src=True)
                    if parse_all_scripts:
                        matching_scripts = [script['src'] for script in scripts]
                    else:
                        matching_scripts = [script['src'] for script in scripts if '_app-' in script['src']]
                    for script_url in matching_scripts:
                        script_url = HTMLRequests.BASE_URL + script_url
                        async with aiohttp.ClientSession() as session:
                            async with session.get(script_url, headers=headers, timeout=timeout) as script_resp:
                                if script_resp is not None and resp.status == 200:
                                    script_resp_text = await script_resp.text()
                                    search_info = SearchInformations(script_resp_text)
                                    if search_info.search_url is not None:
                                        # The api key is necessary
                                        return search_info
                                else:
                                    return None
                else:
                    return None
                
    @staticmethod
    def get_auth_token_request_params():
        """
        Generate the params for the auth token request
        @return: The params object for the request
        """
        timestamp = int(time.time() * 1000)
        params = {
            't': timestamp
        }
        return params

    @staticmethod
    def send_website_get_auth_token(parsed_search_url, user_agent):
        """
        Function that send a request to howlongtobeat to get the x-auth-token to get in the request
        @return: The auth token to use
        """
        # Make the post request and return the result if is valid
        headers = HTMLRequests.get_title_request_headers(user_agent)
        params = HTMLRequests.get_auth_token_request_params()
        auth_struct = SearchAuthToken()
        auth_token_url = HTMLRequests.BASE_URL
        if parsed_search_url is not None:
            auth_token_url = HTMLRequests.BASE_URL + parsed_search_url + auth_struct.search_url_endpoint
        else:
            auth_token_url = HTMLRequests.BASE_URL + auth_struct.search_url + auth_struct.search_url_endpoint
        resp = requests.get(auth_token_url, params=params, headers=headers, timeout=60)
        if resp.status_code == 200 and resp.text is not None:
            return auth_struct.extract_auth_token_from_response(resp)
        return None

    @staticmethod
    async def async_send_website_get_auth_token(parsed_search_url, user_agent):
        """
        Function that send a request to howlongtobeat to get the x-auth-token to get in the request
        @return: The auth token to use
        """
        # Make the post request and return the result if is valid
        headers = HTMLRequests.get_title_request_headers(user_agent)
        params = HTMLRequests.get_auth_token_request_params()
        auth_struct = SearchAuthToken()
        auth_token_url = HTMLRequests.BASE_URL
        if parsed_search_url is not None:
            auth_token_url = HTMLRequests.BASE_URL + parsed_search_url + auth_struct.search_url_endpoint
        else:
            auth_token_url = HTMLRequests.BASE_URL + auth_struct.search_url + auth_struct.search_url_endpoint
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession() as session:
            async with session.get(auth_token_url, params=params, headers=headers, timeout=timeout) as resp:
                if resp is not None and resp.status == 200:
                    json_data = await resp.json()
                    return auth_struct.extract_auth_token_from_json(json_data)
        return None
