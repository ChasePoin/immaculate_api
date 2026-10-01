TEAMS = [
    "ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET",
    "EDM","FLA","LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT",
    "PHI","PIT","SEA","SJS","STL","TBL","TOR","UTA","VAN","VGK","WPG","WSH"
]


class Player():
    """
    Fields a Player should have (helpful, I Know)
    """
    def __init__(self, name: str = None, pos: str = None, rating: int = None, img: str = None, team: str=None):
        self.name   = name
        self.pos    = pos
        self.rating = rating
        self.img    = img
        self.team   = team


#add a late date accesssed, also add a picture field.
class Question():
    """ 
    Fields a Question should have (actually helpful)
    """
    def __init__(self, type: str = None, message: str = None, options: list = None, image: str = None, last_accessed: str = None, answer: dict = None):
        self.type           = type
        self.message        = message
        self.options        = options
        self.image          = image
        self.last_accessed  = last_accessed
        self.answer         = answer

class Answer():
    """
    Fields an Anaswer should have (even more helpful)
    """
    def __init__ (self, type: str = None, message: str | list = None):
        self.type    = type
        self.message = message

class PlayerRequest():
    """
    General Player Request Class
    """
    def __init__(self, 
                 name: str = None,
                 pos: str = None, 
                 rating: int = 100, 
                 team: str = None,
                 count: int = None):
        self.name   = name
        self.pos    = pos
        self.rating = rating
        self.team   = team
        self.count  = count

class QuestionRequest():
    def __init__(self,
                 count: int = None,
                 type: str = None,
                 special: str = None):
        self.count   = count
        self.type    = type
        self.special = special