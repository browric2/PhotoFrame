import pygame

SWidth = 500
SHeight = 500

##################### CONTROL PANEL: TWEAK THESE! ########################

iterations_per_point = 1000   # CUT-OFF POINT FOR SET INCLUSION. HIGHER -> SLOWER, MORE DETAIL ON ZOOMING, CRASHES FASTER.[~1-150]
Resolving_Speed = 50         # CONTROLS THE NUMBER OF FRAMES IMAGE RESOLVES AT. HIGHER -> SLOWER, SMOOTHER TRANSISIONS.   [~ 7-50]
colour_divisions = 50        # NUMBER OF DIFFERENT COLOUR DIVISIONS. HIGHER -> MORE SUBTLE BUT SMOOTHER COLOUR.           [~ 1-50]

##################### CONTROL PANEL: TWEAK THESE! ########################

size = (SWidth, SHeight)
#screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Ricky's Photo Viewer")

currentgroup = 0

pansteps = 200
startframes = 80
endframes = 80
tframes = 50
fps = 40