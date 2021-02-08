
class CharDatabaseInterface:
    """ store the personality of character text"""
    def add_char(self, char_personality: dict):
        """ Adds character personality to database"""
        pass

    def search_char(self, char_personality: dict) -> str:
        """ Searches for character closest to passed in personality """
        pass


class DiscoveryCharDatabase(CharDatabaseInterface):

    def add_char(self, char_personality: dict):
        pass

    def search_char(self, char_personality: dict) -> str:
        pass
