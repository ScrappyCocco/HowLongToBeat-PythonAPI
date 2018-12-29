# ---------------------------------------------------------------------
# IMPORTS

from .HowLongToBeatEntry import HowLongToBeatEntry
from html.parser import HTMLParser
from difflib import SequenceMatcher


# ---------------------------------------------------------------------


class HTMLResultParser(HTMLParser):
    """
    This class override the default HTMLParser to analyze the HTML code received from HowLongToBeat
    """

    def __init__(self, input_game_name: str, input_game_url: str):
        super().__init__()
        # Init instance variables
        self.results = []
        self.base_game_url = input_game_url
        self.current_entry = None
        self.li_encountered = False
        self.inside_a_div = False
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
            if tag == "a":  # The <a> tag contain the game title and the game page id
                for att in attrs:
                    if att[0] == "title":  # Read the current game title
                        self.current_entry.game_name = att[1]
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
        if tag == "div":  # I save that i'm no longer inside a <div> element
            self.inside_a_div = False
        if tag == "li" and self.li_encountered:  # I finished reading the game entry
            self.li_encountered = False
            # Calculate name similarity with original input name
            self.current_entry.similarity = self.similar(self.game_name, self.current_entry.game_name,
                                                         self.game_name_numbers)
            # If the similarity is too low skipping adding it to results list
            if self.current_entry.similarity > 0.4:
                self.results.append(self.current_entry)
            # Set the current entry to None, will be created on the next <li>
            self.current_entry = None

    # OVERRIDE from HTMLParser
    def handle_data(self, data):
        if self.inside_a_div:
            # If i'm inside a <div> i must analyze all the possible times, saving title and then his value
            if data.lower().strip() == "main story" \
                    or data.lower().strip() == "single-player" \
                    or data.lower().strip() == "solo":
                self.currently_reading = "main"
                return
            if data.lower().strip() == "main + extra" or data.lower().strip() == "co-op":
                self.currently_reading = "main&extra"
                return
            if data.lower().strip() == "completionist" or data.lower().strip() == "vs.":
                self.currently_reading = "complete"
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
        :param time_string: The original string with the time (ex. 50 Hours)
        :return: the numeric part of that time (ex. 50 or 51½ , IS A STRING)
        """
        if "-" in time_string:
            return 0
        end_pos = time_string.find(' ')
        return time_string[:end_pos].strip()

    @staticmethod
    def get_time_unit(time_string: str):
        """
        Function that return the time unit from the string (Minutes/Hours)
        :param time_string: The original string with the time (ex. 50 Hours)
        :return: the unit of that time (ex. "Hours")
        """
        if "-" in time_string:
            return None
        start_pos = time_string.find(' ')
        return time_string[start_pos:].strip()

    @staticmethod
    def similar(a, b, game_name_numbers):
        """ This function calculate how much the first string is similar to the second string
        :param a: First String
        :param b: Second String
        :param game_name_numbers: All the numbers in <a> string, used for an additional check
        :return: Return the similarity between the two string (0.0-1.0)
        """
        if a is None or b is None:
            return 0
        similarity = SequenceMatcher(None, a, b).ratio()
        if game_name_numbers is not None and len(game_name_numbers) > 0:  # additional check about numbers in the string
            number_found = False
            for word in b.split(" "):  # check for every word
                if word.isdigit():  # if is a digit
                    for number_entry in game_name_numbers:  # compare it with numbers in the begin string
                        if str(number_entry) == str(word):
                            number_found = True
                            break
            if not number_found:  # number in the given string not in this one, reduce prob
                similarity -= 0.1
        return similarity
