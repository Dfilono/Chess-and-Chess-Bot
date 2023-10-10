class Square:

    ALPHACOL = {0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D',
                4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H'}

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphaCol = self.ALPHACOL[col]

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def hasPiece(self):
        return self.piece != None
    
    def isEmpty(self):
        return not self.hasPiece()
    
    def hasTeam(self, color):
        return self.hasPiece() and self.piece.color == color
    
    def hasRival(self, color):
        return self.hasPiece() and self.piece.color != color

    def isEmptyOrRival(self, color):
        return self.isEmpty() or self.hasRival(color)
    
    @staticmethod
    def inRange(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
    
    @staticmethod
    def getAlphaCol(col):
        ALPHACOL = {0 : 'A', 1 : 'B', 2 : 'C', 3 : 'D',
                    4 : 'E', 5 : 'F', 6 : 'G', 7 : 'H'}
        return ALPHACOL[col]