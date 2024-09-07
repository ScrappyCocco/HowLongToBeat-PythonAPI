class HowLongToBeatEntry:
    """
    A simple class to collect all game data that are being read from the JSON response
    It contains just the main data and values for the game, the rest can be read manually from the JSON
    Consider that some values could be None, such as profile_dev, since HLTB sometimes remove/add values
    The full content for the entry is available in json_content
    """

    def __init__(self):
        # Base Game Details
        # How Long To Beat Game ID
        self.game_id = -1
        # Default Game Name
        self.game_name = None
        # Alias for the same game, as a second name
        self.game_alias = None
        # The type of entry, usually "game" or "dlc"
        self.game_type = None
        self.game_image_url = None
        # Link to How Long To Beat
        self.game_web_link = None
        # The review score
        self.review_score = None
        # The name of the dev
        self.profile_dev = None
        # The list of the platforms for the title
        self.profile_platforms = None
        # Should contain the release year
        self.release_world = None
        # Similarity between this entry game name and the searched string
        # Calculated as the max similarity between the searched string and game_name & game_alias
        self.similarity = -1
        # JSON Fields
        # Full JSON response
        self.json_content = None
        # The four different completion times, in Hours
        # Remember not all games will have them valid (like coop or pvp games)
        # Main Story
        self.main_story = None
        # Main + Extra
        self.main_extra = None
        # Main Completionist
        self.completionist = None
        # All styles
        self.all_styles = None
