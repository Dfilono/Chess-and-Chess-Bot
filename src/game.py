import pygame as pg
from constants import *
from board import Board
from drag import Drag
from config import Config
from square import Square

class Game:

    def __init__(self):
        self.nextPlayer = 'white'
        self.hoverSqr = None
        self.board = Board()
        self.drag = Drag()
        self.config = Config()

    # Show Functions
    def showBG(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(surface, color, rect)

                if col == 0:
                    fontColor = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.config.font.render(str(ROWS - row), 1, fontColor)
                    labelPos = (5, 5 + row * SQUARE_SIZE)
                    surface.blit(label, labelPos)

                if row == 7:
                    fontColor = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    label = self.config.font.render(Square.getAlphaCol(col), 1, fontColor)
                    labelPos = (col * SQUARE_SIZE + SQUARE_SIZE - 20, HEIGHT - 20)
                    surface.blit(label, labelPos)

    def showPieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].hasPiece():
                    piece = self.board.squares[row][col].piece

                    # all pieces except piece being dragged
                    if piece is not self.drag.piece:
                        piece.setTexture(size=80)
                        img = pg.image.load(piece.texture)
                        imgCenter = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.textureRect = img.get_rect(center=imgCenter)
                        surface.blit(img, piece.textureRect)

    def showMoves(self, surface):
        theme = self.config.theme
        if self.drag.dragging:
            piece = self.drag.piece

            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(surface, color, rect)

    def showLastMove(self, surface):
        theme = self.config.theme
        if self.board.lastMove:
            initial = self.board.lastMove.initial
            final = self.board.lastMove.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pg.draw.rect(surface, color, rect)

    def showHover(self, surface):
        if self.hoverSqr:
            color = (180, 180, 180)
            rect = (self.hoverSqr.col * SQUARE_SIZE, self.hoverSqr.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pg.draw.rect(surface, color, rect, width=3)
    
    # Other Functions
    def nextTurn(self):
        self.nextPlayer = 'white' if self.nextPlayer == 'black' else 'black'

    def setHover(self, row, col):
        self.hoverSqr = self.board.squares[row][col]

    def changeTheme(self):
        self.config.changeTheme()

    def soundEffect(self, captured=False):
        if captured:
            self.config.captureSound.play()
        else:
            self.config.moveSound.play()

    def reset(self):
        self.__init__()
