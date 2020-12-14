# ---------------------------------------------------------------------
# IMPORTS

from .HTMLResultParser import HTMLResultParser
from .HTMLRequests import HTMLRequests, SearchModifiers


# ---------------------------------------------------------------------


class HowLongToBeat:
    """
    Main class that contain the base "search" function
    The search function is available using standard request or using an async request that MUST be awaited
    """

    # ------------------------------------------
    # Constructor with optional parameters
    # ------------------------------------------

    def __init__(self, input_minimum_similarity: float = 0.4):
        """
        @param input_minimum_similarity: Minimum similarity to use to filter the results with the found name,
        0 will return all the results; 1 means perfectly equal and should not be used; default is 0.4;
        """
        self.minimum_similarity = input_minimum_similarity

    # body of the constructor

    # ------------------------------------------
    # (Standard) Search functions using game name
    # ------------------------------------------

    async def async_search(self, game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE,
                           similarity_case_sensitive: bool = True):
        """
        Function that search the game using an async request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param similarity_case_sensitive: If the similarity check between names should be case sensitive (default true)
        @return: A list of possible games (or None in case of wrong parameter or failed request)
        """
        if game_name is None or len(game_name) == 0:
            return None
        html_result = await HTMLRequests.send_async_web_request(game_name, search_modifiers)
        if html_result is not None:
            return self.__parse_web_result(game_name, html_result, None, similarity_case_sensitive)
        else:
            return None

    def search(self, game_name: str, search_modifiers: SearchModifiers = SearchModifiers.NONE,
               similarity_case_sensitive: bool = True):
        """
        Function that search the game using a normal request
        @param game_name: The original game name received as input
        @param search_modifiers: The "Modifiers" list in "Search Options", allow to show/isolate/hide DLCs
        @param similarity_case_sensitive: If the similarity check between names should be case sensitive (default true)
        @return: A list of possible games (or None in case of wrong parameter or failed request)
        """
        if game_name is None or len(game_name) == 0:
            return None
        html_result = HTMLRequests.send_web_request(game_name, search_modifiers)
        if html_result is not None:
            return self.__parse_web_result(game_name, html_result, None, similarity_case_sensitive)
        else:
            return None

    # ------------------------------------------
    # Search functions using game id
    # ------------------------------------------

    async def async_search_from_id(self, game_id: int):
        """
        Function that search the game using an async request
        To re-use code, i extract the game name and search game by name, picking only the game with the same id
        Otherwise a new parser is necessary, and is probably not worth to maintain 2 different html parsers
        Remember that this function use 2 requests: one to get the game title and one to get game data
        @param game_id: The game id to get data
        @return: The game data (single HowLongToBeatEntry object) or None in case of error
        """
        if game_id is None or game_id == 0:
            return None
        game_title = await HTMLRequests.async_get_game_title(game_id)
        if game_title is not None:
            html_result = await HTMLRequests.send_async_web_request(game_title)
            if html_result is not None:
                result_list = self.__parse_web_result(game_title, html_result, game_id)
                if result_list is None or len(result_list) == 0 or len(result_list) > 1:
                    return None
                else:
                    return result_list[0]
            else:
                return None
        else:
            return None

    def search_from_id(self, game_id: int):
        """
        To re-use code, i extract the game name and search game by name, picking only the game with the same id
        Otherwise a new parser is necessary, and is probably not worth to maintain 2 different html parsers
        Remember that this function use 2 requests: one to get the game title and one to get game data
        @param game_id: The game id to get data
        @return: The game data (single HowLongToBeatEntry object) None in case of error
        """
        if game_id is None or game_id == 0:
            return None
        game_title = HTMLRequests.get_game_title(game_id)
        if game_title is not None:
            html_result = HTMLRequests.send_web_request(game_title)
            if html_result is not None:
                result_list = self.__parse_web_result(game_title, html_result, game_id)
                if result_list is None or len(result_list) == 0 or len(result_list) > 1:
                    return None
                else:
                    return result_list[0]
            else:
                return None
        else:
            return None

    # ------------------------------------------
    # Private utils functions
    # ------------------------------------------

    def __parse_web_result(self, game_name: str, html_result, game_id=None,
                           similarity_case_sensitive: bool = True):
        """
        Function that call the HTML parser to get the data
        @param game_name: The original game name received as input
        @param html_result: The HTML received from the request
        @param game_id: The game id to search
        @return: A list of possible games
        """
        if game_id is None:
            parser = HTMLResultParser(game_name, HTMLRequests.GAME_URL, self.minimum_similarity, game_id,
                                      similarity_case_sensitive)
        else:
            # If the search is by id, ignore class minimum_similarity and set it to 0.0
            # The result is filter by ID anyway, so the similarity shouldn't count too much
            # Also ignore similarity_case_sensitive and leave default value
            parser = HTMLResultParser(game_name, HTMLRequests.GAME_URL, 0.0, game_id)
        parser.feed(html_result)
        return parser.results
