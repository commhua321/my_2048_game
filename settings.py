import numpy
import pygame

class Settings():

    def __init__(self,block):

        self.screen_width = block.whole_size
        self.screen_height = block.whole_size
        self.bg_color = (200, 200, 200)
        self.matrix = numpy.zeros([4, 4])
        self.zerolist = []
        self.titlerect = pygame.Rect(0, 0, self.screen_width, 120)
        self.titlecolor = (112, 128, 105)
        self.score = 0
        self.scorefont = pygame.font.SysFont(None, 48)
        self.reset = False
        self.gameover_check = False
        self.gamewin_check = False




