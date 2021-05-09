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
    def __repr__(self):
        print("game_id:",self.game_id )
        print("game_name:",self.game_name ) 
        print("game_name_suffix:",self.game_name_suffix ) 
        print("game_image_url:",self.game_image_url ) 
        print("game_web_link:",self.game_web_link ) 
        # Gameplay Main
        print("gameplay_main:",self.gameplay_main ) 
        print("gameplay_main_unit:",self.gameplay_main_unit ) 
        print("gameplay_main_label:",self.gameplay_main_label ) 
        # Gameplay Main + Extra
        print("gameplay_main_extra:",self.gameplay_main_extra ) 
        print("gameplay_main_extra_unit:",self.gameplay_main_extra_unit ) 
        print("gameplay_main_extra_label:",self.gameplay_main_extra_label ) 
        # Completionist
        print("gameplay_completionist:",self.gameplay_completionist ) 
        print("gameplay_completionist_unit:",self.gameplay_completionist_unit ) 
        print("gameplay_completionist_label:",self.gameplay_completionist_label ) 
        # Similarity with original name
        print("similarity:",self.similarity)
