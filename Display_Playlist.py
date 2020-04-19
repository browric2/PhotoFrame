from preprocessing import file_ends
import random
import pygame
import Settings
import Transitions
import os

screen = Settings.screen
SWidth = Settings.SWidth
SHeight = Settings.SHeight
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
clock = pygame.time.Clock()

pansteps = Settings.pansteps
startframes = Settings.startframes
endframes = Settings.endframes
tframes = Settings.tframes


class Player():

    def __init__(self,playlist,home_colour,transition = Transitions.fade):

        self.playlist = playlist
        self.home_colour = home_colour
        self.transition = transition

        self.clock = pygame.time.Clock()
        self.done = False
        self.pause_state = False
        self.mode = 'first'
        self.imshape = 'Error: Imshape undefined'
        self.imagelist = os.listdir(playlist)
        self.picfit = 'Error: picfit undefined'
        self.picfit2 = pygame.image.load(os.path.abspath(self.playlist+self.imagelist[0]))
        self.alph = 255
        self.startcount = 0
        self.endcount = 0
        self.shifted = 0
        self.where = [0,0]

        pass

    def First_Mode(self):
        screen.fill(self.home_colour)

        shifted, startcount, endcount = 0, 0, 0
        imname = ''
        while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
            imname = random.sample(self.imagelist, 1)[0]
        imfile = self.playlist + imname

        self.picfit = pygame.image.load(os.path.abspath(imfile))
        if self.picfit.get_size()[0] > self.picfit.get_size()[1]:
            self.imshape = 'wide'
        else:
            self.imshape = 'tall'

        screen.blit(self.picfit, (0, 0))
        self.mode = 'start'

    def Start_Mode(self):
        if self.startcount < startframes:
            screen.fill(self.home_colour)
            screen.blit(self.picfit, (0, 0))
            self.startcount += 1
        else:
            screen.fill(self.home_colour)
            screen.blit(self.picfit, (0, 0))
            self.mode = 'panning'

    def Panning_Mode(self):
        screen.fill(self.home_colour)
        d = -3
        if self.imshape == 'wide':
            d = 0
        elif self.imshape == 'tall':
            d = 1
        topan = self.picfit.get_size()[d] - (SWidth, SHeight)[d]

        if self.shifted < topan:
            oneshift = topan / pansteps
            self.where = [0, 0]
            self.where[d] = round(self.where[d] - self.shifted)
            screen.blit(self.picfit, self.where)
            self.shifted += oneshift

        elif topan == 0:
            self.where = [0, 0]
            screen.blit(self.picfit, self.where)
            if self.shifted < pansteps:
                self.shifted += 1
            else:
                imname = ''
                while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
                    imname = random.sample(self.imagelist, 1)[0]
                imfile = self.playlist + imname
                self.picfit2 = pygame.image.load(os.path.abspath(imfile))
                if self.picfit2.get_size()[0] > self.picfit2.get_size()[1]:
                    self.imshape = 'wide'
                else:
                    self.imshape = 'tall'
                self.mode = 'end'
        else:
            self.where = [0, 0]
            self.where[d] -= topan
            screen.blit(self.picfit, self.where)
            imname = ''
            while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
                imname = random.sample(self.imagelist, 1)[0]
            imfile = self.playlist + imname

            self.picfit2 = pygame.image.load(os.path.abspath(imfile))
            if self.picfit2.get_size()[0] > self.picfit2.get_size()[1]:
                self.imshape = 'wide'
            else:
                self.imshape = 'tall'
            self.mode = 'end'

    def End_Mode(self):

        if self.endcount < endframes:
            screen.fill(self.home_colour)
            screen.blit(self.picfit, self.where)
            self.endcount += 1
        else:
            screen.fill(self.home_colour)
            screen.blit(self.picfit, self.where)
            self.mode = 'transition'

    def Pause_Mode(self):
        self.picfit.set_alpha(self.alph)
        screen.fill(self.home_colour)
        screen.blit(self.picfit2, (0, 0))
        screen.blit(self.picfit, self.where)

    def Transition_Mode(self):

        self.transition(self)
