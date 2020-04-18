import pygame
import math
import eztext
import buttons as but
import Settings
import os
import keypredict
from textbox import textbox
from pickle import dump

edgeratio = (0.01,0.045)
heightratio = 0.05
gapratio = heightratio*1.1
widthratio = 0.05
butcol = (50,50,50)
text_col = (255,255,255)
explorer_group = but.buttongroup(edgeratio,heightratio,gapratio,widthratio,butcol,text_col)

home_colour = (10,10,10)
pygame.mixer.init(11500, -16, 2, 64)
effect = pygame.mixer.Sound('data/sound_effects/tiny_button_edit3.wav')
wrongeffect = pygame.mixer.Sound('data/sound_effects/wrongsudden1616nrs.wav')
wrongeffect.set_volume(0.7)
righteffect = pygame.mixer.Sound('data/sound_effects/correct16.wav')
righteffect.set_volume(0.7)
track = 'data/music/05 Gas 05.mp3'
#track = 'data/music/Gaslow.mp3'

nrounds = 100
cutoff = 20

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


quitbut = Quit_but()
homebut = Home_but()

screen = Settings.screen

clock = pygame.time.Clock()

plat_edge = 0.24
plat_height = 0.7

imwidth = 300
platwidth = 368
platheight = int((324/515)*platwidth)
redwidth = int((485/515)*platwidth)

rock = pygame.image.load(os.path.abspath("data/images/rock.png"))
rockmini = pygame.transform.scale(rock, (80, 80))
rockmain = pygame.transform.scale(rock, (imwidth, imwidth))
rock2 = pygame.image.load(os.path.abspath("data/images/rock2.png"))
rockmain2 = pygame.transform.scale(rock2, (imwidth, imwidth))


paper = pygame.image.load(os.path.abspath("data/images/paper2.png"))
papermain = pygame.transform.scale(paper, (imwidth, imwidth))
papermini = pygame.transform.scale(paper, (80, 80))
paper2 = pygame.image.load(os.path.abspath("data/images/paper.png"))
papermain2 = pygame.transform.scale(paper2, (imwidth, imwidth))


scissors = pygame.image.load(os.path.abspath("data/images/scissors.png"))
scissorsmain = pygame.transform.scale(scissors, (imwidth, imwidth))
scissorsmini = pygame.transform.scale(scissors, (80, 80))
scissors2 = pygame.image.load(os.path.abspath("data/images/scissors2.png"))
scissorsmain2 = pygame.transform.scale(scissors2, (imwidth, imwidth))


iconwidth = 120

tick = pygame.image.load(os.path.abspath("data/images/tickrs.png"))
#tick = pygame.transform.scale(tick, (iconwidth, iconwidth))
cross = pygame.image.load(os.path.abspath("data/images/crossrs.png"))
#cross = pygame.transform.scale(cross, (iconwidth, iconwidth))
equal = pygame.image.load(os.path.abspath("data/images/equalrs.png"))
#equal = pygame.transform.scale(equal, (iconwidth, iconwidth))



keys = pygame.image.load(os.path.abspath("data/images/keys.png"))
keys = pygame.transform.scale(keys, (240, 82))
plat = pygame.image.load(os.path.abspath("data/images/platform.png"))
plat = pygame.transform.scale(plat, (platwidth, platheight))
plat2 = pygame.image.load(os.path.abspath("data/images/platform2.png"))
plat2 = pygame.transform.scale(plat2, (redwidth, platheight))


def play_mode():
    pygame.init()

    SWidth = Settings.SWidth
    SHeight = Settings.SHeight

    pygame.font.init()
    myfont = pygame.font.SysFont('Garamond', int(SHeight/30))
    global done
    done = False

    pygame.mixer.music.load(track)
    pygame.mixer.music.play()

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    mode = 'First'
    key = ''
    keylist = []
    responselist = []
    resultlist = []

    wins = 0
    losses = 0
    winpc = 0

    roundx = int(SWidth/1.5)
    roundwidth = int(SWidth-roundx-10)
    roundheight = int(SHeight/5)
    offset = 10
    winpclist = []
    roundxlist = [int(roundx + i*(roundwidth/nrounds)) for i in range(nrounds)]
    graphframe = [(roundx,offset),(roundx,offset+roundheight),(roundx,offset+roundheight),(roundx+roundwidth,offset+roundheight)]
    graphmiddle = ((roundx,int(offset+roundheight/2)),(roundx+roundwidth,int(offset+roundheight/2)))
    graphcutoff = ((roundx+int(roundwidth*(cutoff/nrounds))-int(2*(roundwidth/nrounds)),offset),
                   (roundx+int(roundwidth*(cutoff/nrounds))-int(2*(roundwidth/nrounds)),offset+roundheight))

    newresult = False
    rstring = ''
    res = ''

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key = 'rock'
                if event.key == pygame.K_DOWN:
                    key = 'paper'
                if event.key == pygame.K_RIGHT:
                    key = 'scissors'

        if not done:

            screen.fill(home_colour)

            a=400
            b=240
            screen.blit(rockmini,(120,0))
            screen.blit(papermini,(200,0))
            screen.blit(scissorsmini,(280,0))
            screen.blit(keys,(120,80))
            screen.blit(plat,(int(plat_edge*SWidth),int(plat_height*SHeight)))
            screen.blit(plat2,(int(SWidth - plat_edge*SWidth-redwidth),int(plat_height*SHeight)))

            for exp_but in explorer_group.button_list:
                pygame.draw.rect(screen, BLACK, exp_but.shadow(0.15))
                pygame.draw.rect(screen, exp_but.colour,exp_but.rect())
                exp_but.caption_print(screen)

            wtext = 'Wins:   ' + str(wins)
            textbox(screen, wtext, 0.21, 0.2, 30, (SWidth, SHeight),offset = -0.44)
            ltext = 'Losses: ' + str(losses)
            textbox(screen, ltext, 0.21, 0.2, 30, (SWidth, SHeight),offset = -0.33)

            roundtext = 'Round ' + str(len(keylist)+1) +'/' + str(nrounds)

            textbox(screen, roundtext, 0.3, 0.2, 45, (SWidth, SHeight),offset = -0.39)


            pygame.draw.line(screen,(200, 200, 0),graphcutoff[0],graphcutoff[1])
            for dat in winpclist:
                pointlist = []
                for i in range(len(winpclist)):
                    pointlist.append((roundxlist[i],int(roundheight-(roundheight * (winpclist[i]/100)))+offset))
            if len(winpclist)>1:
                pygame.draw.lines(screen,(255,0,0),False,pointlist)
            pygame.draw.lines(screen, WHITE, False, graphframe)
            pygame.draw.line(screen,(100, 100, 100),graphmiddle[0],graphmiddle[1])
            wintext = 'W:L ' + keypredict.percent_win(wins, losses) + '%'
            if float(keypredict.percent_win(wins, losses)) > 50:
                col = (0,255,0)
            else:
                col = (255,0,0)
            textbox(screen, wintext, (roundheight+offset+10)/SHeight, 0.2, 30,
                    (SWidth, SHeight),offset = 0.43,colour=col)



            if mode == 'First':
                text = 'To start, use the arrow keys to enter your choice, and wait while the computer decides.'
                textbox(screen, text, 0.01, 0.2, 30, (SWidth, SHeight))
                if len(key)>1:
                    keylist.append(key)
                    mode = 'Response'
                    key = ''

            elif mode == 'Response':
                text = 'Please wait while the computer prepares its response... Round: ' + str(len(keylist))
                textbox(screen, text, 0.01, 0.2, 30, (SWidth, SHeight))
                mode = 'Result'
                newresult = True
                key = ''

            elif mode == 'Result':
                if newresult == True:
                    response = keypredict.predict(keylist)
                    responselist.append(response)
                    newresult = False
                    selection = keylist[-1]
                    prediction = responselist[-1]
                    res = keypredict.result(selection, prediction)
                    resultlist.append(res)
                    if res == 'win':
                        righteffect.stop()
                        righteffect.play()
                        wins += 1
                        resultstring = 'Nice work! ' + selection.capitalize() + ' beats ' + prediction.capitalize()
                        resultstring += ', giving you the win in round ' + str(len(keylist))
                    elif res == 'loss':
                        wrongeffect.stop()
                        wrongeffect.play()
                        losses += 1
                        resultstring = 'Ouch! ' + prediction.capitalize() + ' beats ' + selection.capitalize()
                        resultstring += ', giving the computer the victory in round ' + str(len(keylist))
                    else:
                        resultstring = 'Draw! ' + selection.capitalize() + ' met ' + prediction.capitalize()
                        resultstring += ', so in round ' + str(len(keylist)) + ', no points are given.'
                    resultstring += '. Now use the arrow keys to make your next selection.'
                    rstring = resultstring
                    winpclist.append(float(keypredict.percent_win(wins, losses)))

                    if len(keylist) == nrounds:
                        fname = 'keyruns/keyrun' + str(nrounds) + 'n' + str(len(os.listdir('keyruns')))
                        dump(keylist,open(fname,'wb'))
                        endloop = True
                        while endloop:
                            overtext = 'Game Over. Press any key to return to the main menu.'
                            textbox(screen, overtext, 0.45, 0.5, 40, (SWidth, SHeight), colour=(123, 222, 255))
                            for event in pygame.event.get():  # User did something
                                if event.type == pygame.KEYDOWN:
                                    done = True
                                    endloop = False
                            pygame.display.flip()
                            clock.tick(60)


                else:
                    if res == 'loss':
                        pass
                textbox(screen, rstring, 0.01, 0.2, 30, (SWidth, SHeight))

                if keylist[-1] == 'rock':
                    screen.blit(rockmain, (int(plat_edge * SWidth), int(plat_height * SHeight)-imwidth))
                if keylist[-1] == 'paper':
                    screen.blit(papermain, (int(plat_edge * SWidth), int(plat_height * SHeight)-imwidth))
                if keylist[-1] == 'scissors':
                    screen.blit(scissorsmain, (int(plat_edge * SWidth), int(plat_height * SHeight)-imwidth))

                if responselist[-1] == 'rock':
                    screen.blit(rockmain2, (int(SWidth - plat_edge*SWidth-redwidth)+(redwidth-imwidth), int(plat_height * SHeight)-imwidth))
                if responselist[-1] == 'paper':
                    screen.blit(papermain2, (int(SWidth - plat_edge*SWidth-redwidth)+(redwidth-imwidth), int(plat_height * SHeight)-imwidth))
                if responselist[-1] == 'scissors':
                    screen.blit(scissorsmain2, (int(SWidth - plat_edge*SWidth-redwidth)+(redwidth-imwidth), int(plat_height * SHeight)-imwidth))

                if res == 'win':
                    screen.blit(tick, (int((SWidth-iconwidth)*0.5), int((SHeight-iconwidth)*0.5)))

                elif res == 'loss':
                    # if len(resultlist) > 1 and resultlist[-2] == 'loss':
                    #     wrongeffect.stop()
                    screen.blit(cross, (int((SWidth-iconwidth)*0.5), int((SHeight-iconwidth)*0.5)))

                else:
                    screen.blit(equal, (int((SWidth-iconwidth)*0.5), int((SHeight-iconwidth)*0.5)))

                if len(key)>1:
                    keylist.append(key)
                    mode = 'Response'
                key = ''

            #print(mode)

            pygame.display.flip()
            clock.tick(60)