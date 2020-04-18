import pygame
import buttons as but
import Settings
import displaypic
import time

clock = pygame.time.Clock()
screen = Settings.screen
SWidth, SHeight = Settings.size

global home_done
home_done = False

heightratio = 0.1
gapratio = heightratio/2
widthratio = 0.15
edgeratio = ((1-widthratio)/2,0.3)
butcol = (50,50,50)
text_col = (255,255,255)

pygame.mixer.init(11500, -16, 2, 64)
effect = pygame.mixer.Sound('data/sound_effects/tiny_button_edit3.wav')

home_colour = (10,10,10)

home_group = but.buttongroup(edgeratio,heightratio,gapratio,widthratio,butcol,text_col)

class Play_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Play", parentgroup = home_group)

    def function(self):
        effect.play()
        displaypic.display_pic()

class Settings_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Settings", parentgroup = home_group)

    def function(self):
        effect.play()
        print('settings')
        #Saved_destinations.saved_dest()

class Quit_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Quit", parentgroup = home_group)

    def function(self):
        effect.play()
        time.sleep(0.45)
        global home_done
        home_done = True
        pygame.quit()

playbut = Play_but()
settingsbut = Settings_but()
quitbut = Quit_but()

BLACK = (0,0,0)

def home_run():
    global home_done
    Settings.currentgroup = home_group

    while not home_done:


        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                home_done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()

                    if Settings.currentgroup == home_group:

                        if quitbut.rect().collidepoint(pos):
                            quitbut.function()

                        elif playbut.rect().collidepoint(pos):
                            playbut.function()

                        elif settingsbut.rect().collidepoint(pos):
                            settingsbut.function()


                    # elif Settings.currentgroup == Saved_destinations.saved_dest_group:
                    #
                    #     if Saved_destinations.backbut.rect().collidepoint(pos):
                    #         Saved_destinations.backbut.function()
                    #
                    #     elif Saved_destinations.quitbut.rect().collidepoint(pos):
                    #         Saved_destinations.quitbut.function()
                    #
                    #     elif Saved_destinations.dispy.rect().collidepoint(pos):
                    #         Saved_destinations.dispy.function()
                    #
                    # elif Settings.currentgroup == Saved_destinations.colgrouplist:
                    #     for i in Settings.currentgroup:
                    #         for tempbut in i.button_list:
                    #             if tempbut.rect().collidepoint(pos):
                    #                 tempbut.function()

        if home_done == False:

            screen.fill(home_colour)

            cgl = Settings.currentgroup

            if type(cgl) == list:
                for i in cgl:
                    for current_but in i.button_list:
                        pygame.draw.rect(screen, BLACK,current_but.shadow(0.15))
                        pygame.draw.rect(screen, current_but.colour,current_but.rect())
                        current_but.caption_print(screen)
            else:
                for current_but in Settings.currentgroup.button_list:
                    pygame.draw.rect(screen, BLACK, current_but.shadow(0.15))
                    pygame.draw.rect(screen, current_but.colour,current_but.rect())
                    current_but.caption_print(screen)

            pygame.display.flip()
            clock.tick(60)