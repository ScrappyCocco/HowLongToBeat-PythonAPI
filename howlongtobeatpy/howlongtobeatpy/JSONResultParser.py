# ---------------------------------------------------------------------
# IMPORTS

import json
import re
from .HowLongToBeatEntry import HowLongToBeatEntry
from difflib import SequenceMatcher

# ---------------------------------------------------------------------


class JSONResultParser:
    """
    This class parse the JSON code received from HowLongToBeat
    """

    # Used for both images and game links
    IMAGE_URL_PREFIX = "https://howlongtobeat.com/games/"
    GAME_URL_PREFIX = "https://howlongtobeat.com/game/"

    def __init__(self, input_game_name: str, input_game_url: str,
                 input_minimum_similarity: float, input_game_id: int = None,
                 input_similarity_case_sensitive: bool = True):
        # Init instance variables
        self.results = []
        self.minimum_similarity = input_minimum_similarity
        self.similarity_case_sensitive = input_similarity_case_sensitive
        self.game_id = input_game_id
        self.base_game_url = input_game_url
        # Init object
        self.game_name = input_game_name
        self.game_name_numbers = []
        for word in input_game_name.split(" "):
            if word.isdigit():
                self.game_name_numbers.append(word)

    def parse_json_result(self, input_json_result):
        response_result = json.loads(input_json_result)
        for game in response_result["data"]:
            new_game_entry = self.parse_json_element(game)
            # We have a game_id, so we are searching by id, add it only if the id is equal
            if self.game_id is not None and str(new_game_entry.game_id) != str(self.game_id):
                continue
            # Minimum Similarity is 0 so just add it straight away
            elif self.minimum_similarity == 0.0:
                self.results.append(new_game_entry)
            # Add it if it respects the minimum similarity
            elif new_game_entry.similarity >= self.minimum_similarity:
                self.results.append(new_game_entry)

    def parse_json_element(self, input_game_element):
        current_entry = HowLongToBeatEntry()
        # Compute base fields
        current_entry.game_id = input_game_element.get("game_id")
        current_entry.game_name = input_game_element.get("game_name")
        current_entry.game_alias = input_game_element.get("game_alias")
        current_entry.game_type = input_game_element.get("game_type")
        if "game_image" in input_game_element:
            current_entry.game_image_url = self.IMAGE_URL_PREFIX + input_game_element.get("game_image")
        current_entry.game_web_link = self.GAME_URL_PREFIX + str(current_entry.game_id)
        current_entry.review_score = input_game_element.get("review_score")
        current_entry.profile_dev = input_game_element.get("profile_dev")
        if "profile_platform" in input_game_element:
            current_entry.profile_platforms = input_game_element.get("profile_platform").split(", ")
        current_entry.release_world = input_game_element.get("release_world")
        # Add full JSON content to the entry
        current_entry.json_content = input_game_element
        # Add a few times elements as help for the user
        # Calculate only if value is not None
        if "comp_main" in input_game_element:
            current_entry.main_story = round(input_game_element.get("comp_main") / 3600, 2)
        if "comp_plus" in input_game_element:
            current_entry.main_extra = round(input_game_element.get("comp_plus") / 3600, 2)
        if "comp_100" in input_game_element:
            current_entry.completionist = round(input_game_element.get("comp_100") / 3600, 2)
        if "comp_all" in input_game_element:
            current_entry.all_styles = round(input_game_element.get("comp_all") / 3600, 2)
        # Compute Similarity
        game_name_similarity = self.similar(self.game_name, current_entry.game_name,
                                            self.game_name_numbers, self.similarity_case_sensitive)
        game_alias_similarity = self.similar(self.game_name, current_entry.game_alias,
                                            self.game_name_numbers, self.similarity_case_sensitive)
        current_entry.similarity = max(game_name_similarity, game_alias_similarity)
        # Return it
        return current_entry

    @staticmethod
    def similar(a, b, game_name_numbers, similarity_case_sensitive):
        """
        This function calculate how much the first string is similar to the second string
        @param a: First String
        @param b: Second String
        @param game_name_numbers: All the numbers in <a> string, used for an additional check
        @param similarity_case_sensitive: If the SequenceMatcher() should be case-sensitive (true) or ignore case (false)
        @return: Return the similarity between the two string (0.0-1.0)
        """
        if a is None or b is None:
            return 0
        # Check if we want a case-sensitive compare or not
        if similarity_case_sensitive:
            similarity = SequenceMatcher(None, a, b).ratio()
        else:
            similarity = SequenceMatcher(None, a.lower(), b.lower()).ratio()
        if game_name_numbers is not None and len(game_name_numbers) > 0:  # additional check about numbers in the string
            number_found = False
            cleaned = re.sub(r'([^\s\w]|_)+', '', b)
            for word in cleaned.split(" "):  # check for every word
                if word.isdigit():  # if is a digit
                    for number_entry in game_name_numbers:  # compare it with numbers in the begin string
                        if str(number_entry) == str(word):
                            number_found = True
                            break
            if not number_found:  # number in the given string not in this one, reduce prob
                similarity -= 0.1
        return similarity
