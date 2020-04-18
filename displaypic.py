import pygame
import math
import buttons as but
import Settings
import os
import random
from preprocessing import file_ends
from PIL import Image, ExifTags
from pickle import dump

screen = Settings.screen
clock = pygame.time.Clock()

pansteps = Settings.pansteps
startframes = Settings.startframes
endframes = Settings.endframes
tframes = Settings.tframes

edgeratio = (0.01,0.045)
heightratio = 0.05
gapratio = heightratio*1.1
widthratio = 0.05
butcol = (50,50,50)
text_col = (255,255,255)
explorer_group = but.buttongroup(edgeratio,heightratio,gapratio,widthratio,butcol,text_col)


heightratio_m = 0.1
gapratio_m = heightratio/2
widthratio_m = 0.15
edgeratio_m = ((1-widthratio)/2,0.3)
butcol_m = (50,50,50)
text_col_m = (255,255,255)


menu_group = but.buttongroup(edgeratio_m,heightratio_m,gapratio_m,widthratio_m,butcol_m,text_col_m)


home_colour = (10,10,10)
pygame.mixer.init(11500, -16, 2, 64)
effect = pygame.mixer.Sound('data/sound_effects/tiny_button_edit3.wav')


class Quit_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Quit", parentgroup = explorer_group)

    def function(self):
        effect.play()
        pygame.quit()
        global done
        global home_done
        done = True
        home_done = True

class Home_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Home", parentgroup = explorer_group)

    def function(self):
        effect.play()
        global done
        done = True


class func1_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "func1", parentgroup = menu_group)

    def function(self):
        effect.play()
        print('func1')

class func2_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "func2", parentgroup = menu_group)

    def function(self):
        effect.play()
        print('func2')

class func3_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "func3", parentgroup = menu_group)

    def function(self):
        effect.play()
        print('func3')

quitbut = Quit_but()
homebut = Home_but()
func1but = func1_but()
func2but = func2_but()
func3but = func3_but()

#global alph, picfit, where, picfit2, mode, startcount, shifted, endcount, im
shifted, startcount, endcount, picfit, im, where, picfit2 = 0, 0, 0, 0, 0, 0, 0
alph = 255

def display_pic():
    pygame.init()

    SWidth = Settings.SWidth
    SHeight = Settings.SHeight

    pygame.font.init()
    myfont = pygame.font.SysFont('Garamond', int(SHeight/30))
    global done
    done = False

    menu_toggle = False


    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    global mode
    mode = 'First'

    imtype = 'None'

    playlist = 'data/playlists/best2_rscale/'
    imagelist = os.listdir(playlist)

    while not done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.MOUSEBUTTONUP:

                if event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if quitbut.rect().collidepoint(pos):
                        quitbut.function()

                    elif homebut.rect().collidepoint(pos):
                        homebut.function()

                    elif menu_toggle:
                        if func1but.rect().collidepoint(pos):
                            func1but.function()
                        elif func2but.rect().collidepoint(pos):
                            func2but.function()
                        elif func3but.rect().collidepoint(pos):
                            func3but.function()
                        else:
                            menu_toggle = not menu_toggle

                    else:
                        menu_toggle = not menu_toggle


        if not done:

            print(mode)

            if mode == 'First':

                screen.fill(home_colour)

                shifted,startcount,endcount = 0,0,0
                imname = ''
                while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
                    imname = random.sample(imagelist,1)[0]
                imfile = playlist + imname




                # if 'rescaled_imgs' not in imagelist:
                #     os.mkdir(playlist+'rescaled_imgs')
                # rscale_file = playlist + 'rescaled_imgs/' + imname
                # reimagelist = os.listdir(playlist+'rescaled_imgs/')

                # if imfile[-4:] == '.jpg':
                #
                #     im = Image.open(imfile)
                #
                #     if imname not in reimagelist:
                #
                #         exif = dict((ExifTags.TAGS[k], v) for k, v in im._getexif().items() if k in ExifTags.TAGS)
                #         if exif['Orientation'] == 0 or exif['Orientation'] == 6:
                #             im = im.rotate(270, expand=True)
                #
                #         if im.size[0] > im.size[1]:
                #             factor = im.size[1] / SHeight
                #             imdims = (int(im.size[0] / factor), SHeight)
                #
                #         else:
                #             factor = im.size[0] / SWidth
                #             imdims = (SWidth, int(im.size[1] / factor))
                #
                #         im.thumbnail(imdims, Image.ANTIALIAS)
                #         im.save(rscale_file, 'png')
                #         print('not in')
                #     else:
                #         print('in')
                #     print(rscale_file)
                #     print(im.size)
                #     picfit = pygame.image.load(os.path.abspath(rscale_file))

                    # if picfit.get_size()[0] > picfit.get_size()[1]:
                    #     imtype = 'wide'
                    # else:
                    #     imtype = 'tall'
                    #
                    # screen.blit(picfit, (0, 0))
                    # mode = 'startmode'

                global picfit
                picfit = pygame.image.load(os.path.abspath(imfile))
                if picfit.get_size()[0] > picfit.get_size()[1]:
                    imtype = 'wide'
                else:
                    imtype = 'tall'

                screen.blit(picfit, (0, 0))
                mode = 'startmode'

            elif mode == 'startmode':
                if startcount < startframes:
                    screen.fill(home_colour)
                    screen.blit(picfit, (0, 0))
                    startcount += 1
                else:
                    screen.fill(home_colour)
                    screen.blit(picfit, (0, 0))
                    mode = 'panning'

            elif mode == 'panning':
                screen.fill(home_colour)
                d = -3
                if imtype == 'wide':
                    d = 0
                elif imtype == 'tall':
                    d = 1
                topan = picfit.get_size()[d] - (SWidth, SHeight)[d]
                #print(topan)
                if shifted < topan:
                    oneshift = topan/pansteps
                    #print(oneshift)
                    global where
                    where = [0,0]
                    where[d] = round(where[d]-shifted)
                    screen.blit(picfit,where)
                    shifted += oneshift

                elif topan == 0:
                    where = [0,0]
                    screen.blit(picfit,where)
                    if shifted < pansteps:
                        shifted += 1
                    else:
                        imname = ''
                        while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
                            imname = random.sample(imagelist, 1)[0]
                        imfile = playlist + imname
                        global picfit2
                        picfit2 = pygame.image.load(os.path.abspath(imfile))
                        if picfit2.get_size()[0] > picfit2.get_size()[1]:
                            imtype = 'wide'
                        else:
                            imtype = 'tall'
                        mode = 'endmode'
                else:
                    where = [0,0]
                    where[d] -= topan
                    screen.blit(picfit,where)
                    imname = ''
                    while imname[-4:] not in file_ends and imname[-5:] not in file_ends:
                        imname = random.sample(imagelist, 1)[0]
                    imfile = playlist + imname

                    picfit2 = pygame.image.load(os.path.abspath(imfile))
                    if picfit2.get_size()[0] > picfit2.get_size()[1]:
                        imtype = 'wide'
                    else:
                        imtype = 'tall'
                    mode = 'endmode'

            elif mode == 'endmode':

                if endcount < endframes:
                    screen.fill(home_colour)
                    screen.blit(picfit, where)
                    endcount += 1
                else:
                    screen.fill(home_colour)
                    screen.blit(picfit, where)
                    mode = 'transition'

            elif mode == 'transition':

                fade()

                # delta_alph = int(255/tframes)
                #
                # if alph >= 0:
                #     picfit.set_alpha(alph)
                #     screen.fill(home_colour)
                #     screen.blit(picfit2, (0,0))
                #     screen.blit(picfit, where)
                #     alph -= delta_alph
                # else:
                #     where = (0,0)
                #     picfit.set_alpha(0)
                #     screen.fill(home_colour)
                #     screen.blit(picfit2, where)



            for exp_but in explorer_group.button_list:
                pygame.draw.rect(screen, BLACK, exp_but.shadow(0.15))
                pygame.draw.rect(screen, exp_but.colour,exp_but.rect())
                exp_but.caption_print(screen)

            if menu_toggle:
                for men_but in menu_group.button_list:
                    pygame.draw.rect(screen, BLACK, men_but.shadow(0.15))
                    pygame.draw.rect(screen, men_but.colour, men_but.rect())
                    men_but.caption_print(screen)




            pygame.display.flip()
            clock.tick(40)

def fade():
    delta_alph = int(255 / tframes)
    global alph, picfit, where, picfit2, mode, startcount, shifted, endcount
    if alph >= 0:

        picfit.set_alpha(alph)
        screen.fill(home_colour)
        screen.blit(picfit2, (0, 0))
        screen.blit(picfit, where)
        alph -= delta_alph
    else:
        where = (0, 0)
        picfit.set_alpha(0)
        screen.fill(home_colour)
        screen.blit(picfit2, where)

        picfit = picfit2
        mode = 'startmode'
        alph = 255
        startcount, shifted, endcount = 0, 0, 0