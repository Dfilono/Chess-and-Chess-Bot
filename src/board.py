from constants import *
from square import Square
from move import Move
from piece import *
from sound import Sound
import os
import copy

class Board:

    def __init__(self):
        self.squares = []

        self.lastMove = None

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing=False):
        initial = move.initial
        final = move.final

        enPassantEmpty = self.squares[final.row][final.col].isEmpty()

        # Board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        if isinstance(piece, Pawn):
            diff = final.col - initial.col
            if diff != 0 and enPassantEmpty:
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()


            # Pawn promotion
            self.checkPromo(piece, final)

        # King Castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.leftRook if (diff < 0) else piece.rightRook
                self.move(rook, rook.moves[-1])


        piece.moved = True

        # Clear valid moves
        piece.clearMoves()

        # Save last move
        self.lastMove = move

    def validMove(self, piece, move):
        return move in piece.moves

    def checkPromo(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def inCheck(self, piece, move):
        tempBoard = copy.deepcopy(self)
        tempPiece = copy.deepcopy(piece)
        tempBoard.move(tempPiece, move, testing=True)

        for row in range(ROWS):
            for col in range(COLS):
                if tempBoard.squares[row][col].hasRival(piece.color):
                    p = tempBoard.squares[row][col].piece
                    tempBoard.calcMoves(p, row, col, bool=False)

                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False
    
    def setEnPassantTrue(self, piece):
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.enPassant = False
        
        piece.enPassant = True

    def calcMoves(self, piece, row, col, bool=True):
        '''Calculate all possible/valid moves of a piece in a position'''

        def pawnMoves():
            steps = 1 if piece.moved else 2

            # Vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))

            for moveRow in range(start, end, piece.dir):
                if Square.inRange(moveRow):
                    if self.squares[moveRow][col].isEmpty():
                        # Make valid move
                        initial = Square(row, col)
                        final = Square(moveRow, col)

                        move = Move(initial, final)
                        
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.addMove(move)
                        else:
                            piece.addMove(move)
                    else:
                        break
                else:
                    break
            
            # Diaganol Move
            moveRow = row + piece.dir
            moveCols = [col - 1, col + 1]

            for moveCol in moveCols:
                if Square.inRange(moveRow, moveCol):
                    if self.squares[moveRow][moveCol].hasRival(piece.color):
                        # Make valid move
                        initial = Square(row, col)
                        finalPiece = self.squares[moveRow][moveCol].piece
                        final = Square(moveRow, moveCol,  finalPiece)

                        move = Move(initial, final)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.addMove(move)
                        else:
                            piece.addMove(move)
            
            # Enpassant move left
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            if Square.inRange(col - 1) and row == r:
                if self.squares[row][col - 1].hasRival(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.enPassant:
                            # Make valid move
                            initial = Square(row, col)
                            final = Square(fr, col - 1,  p)

                            move = Move(initial, final)
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)

             # Enpassant move right
            if Square.inRange(col + 1) and row == r:
                if self.squares[row][col + 1].hasRival(piece.color):
                    p = self.squares[row][col + 1].piece
                    if isinstance(p, Pawn):
                        if p.enPassant:
                            # Make valid move
                            initial = Square(row, col)
                            final = Square(fr, col + 1,  p)

                            move = Move(initial, final)
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)

        def knightMoves():
            possibleMoves = [
                (row - 2, col + 1),
                (row - 2, col - 1),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 1, col - 2),
                (row - 1, col + 2)
            ]

            for posMove in possibleMoves:
                moveRow, moveCol = posMove

                if Square.inRange(moveRow, moveCol):
                    if self.squares[moveRow][moveCol].isEmptyOrRival(piece.color):
                        # Make valid move
                        initial = Square(row, col)
                        finalPiece = self.squares[moveRow][moveCol].piece
                        final = Square(moveRow, moveCol, finalPiece)

                        move = Move(initial, final)

                        if bool:
                            if not self.inCheck(piece, move):
                                piece.addMove(move)
                            else: break
                        else:
                            piece.addMove(move)

        def striaghtMoves(incrs):
            for incr in incrs:
                rowIncr, colIncr = incr
                moveRow = row + rowIncr
                moveCol = col + colIncr

                while True:
                    if Square.inRange(moveRow, moveCol):

                        initial = Square(row, col)
                        finalPiece = self.squares[moveRow][moveCol].piece
                        final = Square(moveRow, moveCol, finalPiece)
                        move = Move(initial, final)

                        if self.squares[moveRow][moveCol].isEmpty():
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)

                        elif self.squares[moveRow][moveCol].hasRival(piece.color):
                            if bool:
                                if not self.inCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)
                            break

                        elif self.squares[moveRow][moveCol].hasTeam(piece.color):
                            break
                    else:
                        break
                        
                    moveRow, moveCol = moveRow + rowIncr, moveCol + colIncr

        def kingMoves():
            adjs = [
                (row - 1, col),
                (row - 1, col + 1),
                (row, col + 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row + 1, col - 1),
                (row, col - 1),
                (row - 1, col - 1)
            ]

            for adj in adjs:
                moveRow, moveCol = adj

                if Square.inRange(moveRow, moveCol):
                    if self.squares[moveRow][moveCol].isEmptyOrRival(piece.color):
                        initial = Square(row, col)
                        final = Square(moveRow, moveCol)

                        move = Move(initial, final)
                        if bool:
                            if not self.inCheck(piece, move):
                                piece.addMove(move)
                            else:
                                break
                        else:
                            piece.addMove(move)

            # Castling
            if not piece.moved:
                # Queen Castle
                leftRook = self.squares[row][0].piece

                if isinstance(leftRook, Rook):
                    if not leftRook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].hasPiece():
                                # Castling is not possible
                                break
                            
                            if c == 3:
                                piece.leftRook = leftRook
                                
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.inCheck(piece, moveK) and not self.inCheck(leftRook, moveR):
                                        leftRook.addMove(moveR)
                                        piece.addMove(moveK)
                                    else:
                                        break
                                else:
                                    leftRook.addMove(moveR)
                                    piece.addMove(moveK)
                            
                # King Castle
                rightRook = self.squares[row][7].piece

                if isinstance(rightRook, Rook):
                    if not rightRook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].hasPiece():
                                # Castling is not possible
                                break
                            
                            if c == 6:
                                piece.rightRook = rightRook
                                
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                if bool:
                                    if not self.inCheck(piece, moveK) and not self.inCheck(rightRook, moveR):
                                        rightRook.addMove(moveR)
                                        piece.addMove(moveK)
                                    else:
                                        break
                                else:
                                    rightRook.addMove(moveR)
                                    piece.addMove(moveK)

        if isinstance(piece, Pawn): pawnMoves()
        
        elif isinstance(piece, Knight): knightMoves()

        elif isinstance(piece, Bishop): 
            striaghtMoves([
                (-1, 1),
                (-1, -1),
                (1, -1),
                (1, 1)
            ])

        elif isinstance(piece, Rook): 
            striaghtMoves([
                (-1, 0),
                (1, 0),
                (0, 1),
                (0, -1)
            ])

        elif isinstance(piece, Queen): 
            striaghtMoves([
                (-1, 1),
                (-1, -1),
                (1, -1),
                (1, 1),
                (-1, 0),
                (1, 0),
                (0, 1),
                (0, -1)
            ])

        elif isinstance(piece, King): kingMoves()

    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]

        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        rowPawn, rowOther = (6, 7) if color == 'white' else (1, 0)

        # Draw Pawns
        for col in range(COLS):
            self.squares[rowPawn][col] = Square(rowPawn, col, Pawn(color))

        # Draw Knights
        self.squares[rowOther][1] = Square(rowOther, 1, Knight(color))
        self.squares[rowOther][6] = Square(rowOther, 6, Knight(color))

        # Draw Bishops
        self.squares[rowOther][2] = Square(rowOther, 2, Bishop(color))
        self.squares[rowOther][5] = Square(rowOther, 5, Bishop(color))

        # Draw Rooks
        self.squares[rowOther][0] = Square(rowOther, 0, Rook(color))
        self.squares[rowOther][7] = Square(rowOther, 7, Rook(color))

        # Draw Queen
        self.squares[rowOther][3] = Square(rowOther, 3, Queen(color))

        # Draw King
        self.squares[rowOther][4] = Square(rowOther, 4, King(color))
