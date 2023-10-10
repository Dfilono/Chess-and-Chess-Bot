import sys
import pygame as pg
from constants import *
from game import Game
from square import Square
from move import Move

class Main:

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('Chess')

        self.game = Game()

    def mainLoop(self):
        
        game = self.game
        screen = self.screen
        drag = game.drag
        board = game.board

        while True:
            game.showBG(screen)
            game.showLastMove(screen)
            game.showMoves(screen)
            game.showPieces(screen)
            game.showHover(screen)

            if drag.dragging:
                drag.updateBlit(screen)

            for event in pg.event.get():

                # Click
                if event.type == pg.MOUSEBUTTONDOWN:
                    drag.updateMouse(event.pos)

                    clickedRow = drag.mouseY // SQUARE_SIZE
                    clickCol = drag.mouseX // SQUARE_SIZE

                    if board.squares[clickedRow][clickCol].hasPiece():
                        piece = board.squares[clickedRow][clickCol].piece

                        if piece.color == game.nextPlayer:
                            board.calcMoves(piece, clickedRow, clickCol)
                            drag.saveInit(event.pos)
                            drag.dragPiece(piece)

                            game.showBG(screen)
                            game.showLastMove(screen)
                            game.showMoves(screen)
                            game.showPieces(screen)
                
                # Move mouse
                elif event.type == pg.MOUSEMOTION:
                    motionRow = event.pos[1] // SQUARE_SIZE
                    motionCol = event.pos[0] // SQUARE_SIZE
                    game.setHover(motionRow, motionCol)

                    if drag.dragging:
                        drag.updateMouse(event.pos)
                        game.showBG(screen)
                        game.showLastMove(screen)
                        game.showMoves(screen)
                        game.showPieces(screen)
                        game.showHover(screen)
                        drag.updateBlit(screen)
                
                # Release
                elif event.type == pg.MOUSEBUTTONUP:
                    if drag.dragging:
                        drag.updateMouse(event.pos)

                        releasedRow = drag.mouseY // SQUARE_SIZE
                        releasedCol = drag.mouseX // SQUARE_SIZE

                        initial = Square(drag.initRow, drag.initCol)
                        final = Square(releasedRow, releasedCol)
                        move = Move(initial, final)

                        if board.validMove(drag.piece, move):
                            # Normal capture
                            captured = board.squares[releasedRow][releasedCol].hasPiece()

                            board.move(drag.piece, move)

                            board.setEnPassantTrue(drag.piece)

                            game.soundEffect(captured)

                            game.showBG(screen)
                            game.showLastMove(screen)
                            game.showPieces(screen)

                            game.nextTurn()

                    drag.undragPiece()
                
                elif event.type == pg.KEYDOWN:
                    if event.key  == pg.K_t:
                        game.changeTheme()

                    if event.key == pg.K_r:
                        game.reset()
                        game = self.game
                        drag = game.drag
                        board = game.board

                # Quit application
                elif event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            pg.display.update()

main = Main()
main.mainLoop()