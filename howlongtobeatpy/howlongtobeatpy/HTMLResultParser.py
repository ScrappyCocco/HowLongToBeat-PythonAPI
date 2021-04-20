# ---------------------------------------------------------------------
# IMPORTS

from .HowLongToBeatEntry import HowLongToBeatEntry
from html.parser import HTMLParser
from difflib import SequenceMatcher

import re


# ---------------------------------------------------------------------


class HTMLResultParser(HTMLParser):
    """
    This class override the default HTMLParser to analyze the HTML code received from HowLongToBeat
    """

    def __init__(self, input_game_name: str, input_game_url: str,
                 input_minimum_similarity: float, input_game_id: int = None,
                 input_similarity_case_sensitive: bool = True):
        super().__init__()
        # Init instance variables
        self.results = []
        self.minimum_similarity = input_minimum_similarity
        self.similarity_case_sensitive = input_similarity_case_sensitive
        self.game_id = input_game_id
        self.base_game_url = input_game_url
        self.current_entry = None
        self.li_encountered = False
        self.inside_a_div = False
        self.inside_a_strong = False
        self.inside_a_title_link = False
        self.currently_reading = None
        self.game_name = None
        self.game_name_numbers = []
        # Init object
        self.game_name = input_game_name
        for word in input_game_name.split(" "):
            if word.isdigit():
                self.game_name_numbers.append(word)

    # OVERRIDE from HTMLParser (empty)
    def error(self, message):
        pass

    # OVERRIDE from HTMLParser
    def handle_starttag(self, tag, attrs):
        if tag == "li":  # If the tag is an <li> this is a game entry
            if not self.li_encountered:
                self.li_encountered = True
                self.current_entry = HowLongToBeatEntry()

        if self.li_encountered:  # If i already read the <li> tag i'm inside a game entry
            if tag == "strong":
                self.inside_a_strong = True
            if tag == "a":  # The <a> tag contain the game title and the game page id
                for att in attrs:
                    if att[0] == "title":  # Read the current game title
                        self.inside_a_title_link = True
                    if att[0] == "href":  # Get the game id from the link
                        start_pos = att[1].find('=') + 1
                        self.current_entry.game_id = att[1][start_pos:]
                        self.current_entry.game_web_link = self.base_game_url + str(self.current_entry.game_id)

            if tag == "img":  # The tag <img> contains the img link for the game
                for att in attrs:
                    if att[0] == "src":
                        self.current_entry.game_image_url = att[1]

            if tag == "div":  # Save that i have entered a <div> tag
                self.inside_a_div = True

    # OVERRIDE from HTMLParser
    def handle_endtag(self, tag):
        if tag == "a" and self.inside_a_title_link:  # No longer in the <a> link with the game name
            self.inside_a_title_link = False
        if tag == "strong" and self.inside_a_strong:
            self.inside_a_strong = False
        if tag == "div":  # I save that i'm no longer inside a <div> element
            self.inside_a_div = False
        if tag == "li" and self.li_encountered:  # I finished reading the game entry
            self.li_encountered = False
            # Check if the game can be added, if the id is different skip it
            if self.game_id is not None and str(self.game_id) != str(self.current_entry.game_id):
                return
            # Can be added
            # Calculate name similarity with original input name
            self.current_entry.similarity = self.similar(self.game_name, self.current_entry.game_name,
                                                         self.game_name_numbers, self.similarity_case_sensitive)
            # If the minimum_similarity is 0 just add the result
            # Otherwise if the similarity is < minimum_similarity skipping adding it to results list
            if self.minimum_similarity == 0.0:
                # Check that the entry is actually valid before adding it
                if self.current_entry.game_name is not None and self.current_entry.game_id != -1:
                    self.results.append(self.current_entry)
            elif self.current_entry.similarity >= self.minimum_similarity:
                self.results.append(self.current_entry)
            # Set the current entry to None, will be created on the next <li>
            self.current_entry = None

    # OVERRIDE from HTMLParser
    def handle_data(self, data):
        if self.inside_a_title_link and len(data.strip()) > 0:
            self.current_entry.game_name = data.strip()  # Save the title of the game
        if self.inside_a_strong and len(data.strip()) > 0:
            self.current_entry.game_name_suffix = data.strip()  # Save the suffix of the game
        if self.inside_a_div:
            # If i'm inside a <div> i must analyze all the possible times, saving title and then his value
            if data.lower().strip() == "main story" \
                    or data.lower().strip() == "single-player" \
                    or data.lower().strip() == "solo":
                self.currently_reading = "main"
                self.current_entry.gameplay_main_label = data.strip()
                return
            if data.lower().strip() == "main + extra" or data.lower().strip() == "co-op":
                self.currently_reading = "main&extra"
                self.current_entry.gameplay_main_extra_label = data.strip()
                return
            if data.lower().strip() == "completionist" or data.lower().strip() == "vs.":
                self.currently_reading = "complete"
                self.current_entry.gameplay_completionist_label = data.strip()
                return
            # If i've just read a title, and i find data, i save the time in the current_entry
            if self.currently_reading == "main" and len(data.strip()) > 0:
                self.current_entry.gameplay_main = self.convert_time_to_number(data.strip())
                self.current_entry.gameplay_main_unit = self.get_time_unit(data.strip())
                self.currently_reading = None
            if self.currently_reading == "main&extra" and len(data.strip()) > 0:
                self.current_entry.gameplay_main_extra = self.convert_time_to_number(data.strip())
                self.current_entry.gameplay_main_extra_unit = self.get_time_unit(data.strip())
                self.currently_reading = None
            if self.currently_reading == "complete" and len(data.strip()) > 0:
                self.current_entry.gameplay_completionist = self.convert_time_to_number(data.strip())
                self.current_entry.gameplay_completionist_unit = self.get_time_unit(data.strip())
                self.currently_reading = None

    @staticmethod
    def convert_time_to_number(time_string: str):
        """
        Function that return the number part from the string
        @param time_string: The original string with the time (ex. 50 Hours)
        @return: the numeric part of that time (ex. 50 or 51 (and half) , IS A STRING)
        """
        if "-" in time_string:
            return -1
        end_pos = time_string.find(' ')
        return time_string[:end_pos].strip()

    @staticmethod
    def get_time_unit(time_string: str):
        """
        Function that return the time unit from the string (Minutes/Hours)
        @param time_string: The original string with the time (ex. 50 Hours)
        @return: the unit of that time (ex. "Hours")
        """
        if "-" in time_string:
            return None
        start_pos = time_string.find(' ')
        return time_string[start_pos:].strip()

    @staticmethod
    def similar(a, b, game_name_numbers, similarity_case_sensitive):
        """
        This function calculate how much the first string is similar to the second string
        @param a: First String
        @param b: Second String
        @param game_name_numbers: All the numbers in <a> string, used for an additional check
        @param similarity_case_sensitive: If the SequenceMatcher() should be case sensitive (true) or ignore case (false)
        @return: Return the similarity between the two string (0.0-1.0)
        """
        if a is None or b is None:
            return 0
        # Check if we want a case sensitive compare or not
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
