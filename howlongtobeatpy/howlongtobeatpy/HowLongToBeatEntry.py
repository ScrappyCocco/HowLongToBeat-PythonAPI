class HowLongToBeatEntry:
    """
    A simple class to collect all game data that are being read from the HTML code
    """
    def __init__(self):
        # Base Game Details
        self.game_id = -1
        self.game_name = None
        self.game_image_url = None
        self.game_web_link = None
        # Gameplay Main
        self.gameplay_main = -1
        self.gameplay_main_unit = None
        # Gameplay Main + Extra
        self.gameplay_main_extra = -1
        self.gameplay_main_extra_unit = None
        # Completionist
        self.gameplay_completionist = -1
        self.gameplay_completionist_unit = None
        # Similarity with original name
        self.similarity = -1
