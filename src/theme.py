from color import Color

class Theme:
    
    def __init__(self, lightBG, darkBG, lightTrace, darkTrace,
                        lightMoves, darkMoves):
        self.bg = Color(lightBG, darkBG)
        self.trace = Color(lightTrace, darkTrace)
        self.moves = Color(lightMoves, darkMoves)