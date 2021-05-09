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

    def __str__(self):
        tup = ("game_id:", self.game_id,"game_name:", self.game_name,"game_name_suffix:", self.game_name_suffix,"game_image_url:", self.game_image_url,"game_web_link:", self.game_web_link,"gameplay_main:", self.gameplay_main,"gameplay_main_unit:", self.gameplay_main_unit,"gameplay_main_label:", self.gameplay_main_label,"gameplay_main_extra:",self.gameplay_main_extra,"gameplay_main_extra_unit:", self.gameplay_main_extra_unit,"gameplay_main_extra_label:", self.gameplay_main_extra_label,"gameplay_completionist:", self.gameplay_completionist,"gameplay_completionist_unit:", self.gameplay_completionist_unit,"gameplay_completionist_label:", self.gameplay_completionist_label,"similarity:", self.similarity)
        string = " ".join([str(x) for x in tup])
        return string
