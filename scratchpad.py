import pygame
import pygame
import buttons as but
import Settings
import displaypic
import time
import os

clock = pygame.time.Clock()
screen = Settings.screen
SWidth, SHeight = Settings.size
# Initialize the game engine
pygame.init()


image=pygame.image.load('data/playlists/best2/pic0.jpg')
image2=pygame.image.load('data/playlists/best2/pic1.jpg')
#image=image.convert()

i = 255

out = True

global home_done
home_done= False
while not home_done:


    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            home_done = True  # Flag that we are done so we exit this loop

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                pos = pygame.mouse.get_pos()

    if home_done == False:

        print(i)
        screen.fill((0,0,0))

        if out:
            i -= 3
            if i <= 0:
                i = 0
                out = False
        if not out:
            i += 3
            if i >= 255:
                i = 255
                out = True

        image.set_alpha(i)
        screen.blit(image2, (0, 0))
        screen.blit(image, (0, 0))



        pygame.display.flip()
        clock.tick(30)





# Be IDLE friendly
pygame.quit()