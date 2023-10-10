import os

class Piece:

    def __init__(self, name, color, value, texture = None, textureRect = None):
        self.name = name
        self.color = color

        valueSign = 1 if color == 'white' else -1
        self.vlaue = value * valueSign

        self.texture = texture
        self.setTexture()
        self.textureTect = textureRect

        self.moves = []
        self.moved = False

    def setTexture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')
        
    def addMove(self, move):
        self.moves.append(move)

    def clearMoves(self):
        self.moves = []

class Pawn(Piece):
    
    def __init__(self, color):
        self.dir = - 1 if color == 'white' else 1
        self.enPassant = False
        super().__init__('pawn', color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):

    def __init__(self, color):
        self.leftRook = None
        self.rightRook = None
        super().__init__('king', color, 10000.0)
