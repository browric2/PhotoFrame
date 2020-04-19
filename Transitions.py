import Settings
screen = Settings.screen
tframes = Settings.tframes


def fade(player):
    delta_alph = int(255 / tframes)
    if player.alph >= 0:

        player.picfit.set_alpha(player.alph)
        screen.fill(player.home_colour)
        screen.blit(player.picfit2, (0, 0))
        screen.blit(player.picfit, player.where)
        player.alph -= delta_alph

    else:
        where = (0, 0)
        player.picfit.set_alpha(0)
        screen.fill(player.home_colour)
        screen.blit(player.picfit2, where)

        player.picfit = player.picfit2
        player.mode = 'start'
        player.alph = 255
        player.startcount, player.shifted, player.endcount = 0, 0, 0





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
