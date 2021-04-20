class HowLongToBeatEntry:
    """
    A simple class to collect all game data that are being read from the HTML code
    The first value of each section contain the actual time (or -1/0 if not available)
    The second value of each section contain the unit of the time (Minutes/Hours, or None if not available)
    The third value of each section contains the label
        (Can be Main Story/Main + Extras/Completionist/Single-Player/Solo/Co-Op/Vs.)
    """

    def __init__(self):
        # Base Game Details
        self.game_id = -1
        self.game_name = None
        self.game_name_suffix = None
        self.game_image_url = None
        self.game_web_link = None
        # Gameplay Main
        self.gameplay_main = -1
        self.gameplay_main_unit = None
        self.gameplay_main_label = None
        # Gameplay Main + Extra
        self.gameplay_main_extra = -1
        self.gameplay_main_extra_unit = None
        self.gameplay_main_extra_label = None
        # Completionist
        self.gameplay_completionist = -1
        self.gameplay_completionist_unit = None
        self.gameplay_completionist_label = None
        # Similarity with original name
        self.similarity = -1
