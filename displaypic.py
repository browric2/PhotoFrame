import pygame
import buttons as but
import Settings
import Display_Playlist


playlist = 'data/playlists/best2_rscale/'
home_colour = (10,10,10)
player = Display_Playlist.Player(playlist, home_colour)


screen = Settings.screen
clock = pygame.time.Clock()

pansteps = Settings.pansteps
startframes = Settings.startframes
endframes = Settings.endframes
tframes = Settings.tframes

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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


pygame.mixer.init(11500, -16, 2, 64)
effect = pygame.mixer.Sound('data/sound_effects/tiny_button_edit3.wav')


class Quit_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Quit", parentgroup = explorer_group)

    def function(self):
        effect.play()
        pygame.quit()
        global home_done
        home_done = True

class Home_but(but.button):
    def __init__(self):
        but.button.__init__(self, caption = "Home", parentgroup = explorer_group)

    def function(self):
        effect.play()
        player.done = True

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


def display_pic():
    pygame.init()
    SHeight = Settings.SHeight
    pygame.font.init()
    myfont = pygame.font.SysFont('Garamond', int(SHeight/30))
    menu_toggle = False

    while not player.done:

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                player.done = True  # Flag that we are done so we exit this loop

            elif event.type == pygame.MOUSEBUTTONUP:

                print('!!!!!!!!!!!!!!!!!!')

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


        if not player.done:

            if player.mode == 'first':
                player.First_Mode()

            elif player.mode == 'start':
                player.Start_Mode()

            elif player.mode == 'panning':
                player.Panning_Mode()

            elif player.mode == 'end':
                player.End_Mode()

            elif player.mode == 'transition':
                player.Transition_Mode()

            else:
                raise AssertionError('Invalid Player Mode Selected')


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
            clock.tick(Settings.fps)