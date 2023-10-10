import pygame as pg

class Sound:

    def __init__(self, path):
        self.path = path
        self.sound = pg.mixer.Sound(path)

    def play(self):
        pg.mixer.Sound.play(self.sound)