import pygame as pg
from constants import *

class Drag:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initRow = 0
        self.initCol = 0
        self.dragging = False
        self.piece = None

    def updateBlit(self, surface):
        self.piece.setTexture(size=128)
        texture = self.piece.texture

        img = pg.image.load(texture)

        imgCenter = (self.mouseX, self.mouseY)
        self.piece.textureRect = img.get_rect(center=imgCenter)
        surface.blit(img, self.piece.textureRect)

    def updateMouse(self, pos):
        self.mouseX, self.mouseY = pos

    def saveInit(self, pos):
        self.initRow = pos[1] // SQUARE_SIZE
        self.initCol = pos[0] // SQUARE_SIZE

    def dragPiece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undragPiece(self):
        self.piece = None
        self.dragging = False