from taurex.log import Logger


class CatalogueReader(Logger):
    """
    A base class for reading target lists and generating taurex planet and star objects
    """

    def __init__(self):
        super().__init__(self.__class__.__name__)

    def load_planet_list(self):
        raise NotImplementedError

    
    #def generate_planet(self):
    #    raise NotImplementedError

    #def generate_star(self, phoenix_path=None):
    #    raise NotImplementedError
    

    #def generate_instrument(self):
    #    raise NotImplementedError