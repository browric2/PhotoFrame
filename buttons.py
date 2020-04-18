import Settings
import pygame
SWidth = Settings.SWidth
SHeight = Settings.SHeight

class button:
    def __init__(self, parentgroup, left=0, top=0, width=0, height=0, caption="", colour=(0,0,0), text_col= (255,255,255)):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.caption = caption
        self.colour = colour
        self.fsize = int(self.height/2)
        self.parentgroup = parentgroup
        if self.parentgroup != "none":
            self.parentgroup.add(self)

    def rect(self):
        return pygame.Rect(self.left,self.top,self.width,self.height)

    def shadow(self,offset_ratio):
        return pygame.Rect(int(self.left+offset_ratio*self.height),
                           int(self.top + offset_ratio * self.height),
                           self.width,self.height)


    def setdims(self,left,top,width,height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.fsize = int(self.height/2)

    def setcol(self,col,text_col):
        self.colour = col
        self.text_col = text_col

    def caption_print(self,screen):
        pygame.font.init()
        capfont= pygame.font.SysFont('Garamond',self.fsize)
        capsurface = capfont.render(self.caption, True, self.text_col)
        text_width, text_height = capfont.size(self.caption)
        cap_x = int(self.left + self.width/2 - text_width/2)
        cap_y = int(self.top + self.height/4)
        screen.blit(capsurface,(cap_x,cap_y))

    def function(self, *args):
        print("error: parent method called.")

class buttongroup:
    def __init__(self,edgeratio,heightratio,gapratio,widthratio,butcol,text_col,top=True):
        self.button_list = []
        self.edgeratioleft = edgeratio[0]
        self.edgeratiobottom = edgeratio[1]
        self.heightratio = heightratio
        self.gapratio = gapratio
        self.widthratio = widthratio
        self.butcol = butcol
        self.text_col = text_col
        self.top = top

    def add(self,button):
        self.button_list.append(button)
        self.set_group_dims()

    def set_group_dims(self):
        n_group_b = len(self.button_list)

        for exp_but in range(0,n_group_b):
            left = int(SWidth*self.edgeratioleft)
            if self.top:
                top = int((SHeight*self.edgeratiobottom) +
                      (exp_but)*((self.heightratio*SHeight)+((self.gapratio*SHeight)/2)))
            else:
                top = int(SHeight-(SHeight*self.edgeratiobottom) - (SHeight*self.heightratio) -
                      (exp_but)*((self.heightratio*SHeight)+((self.gapratio*SHeight)/2)))
            width = int(SWidth*self.widthratio)
            height = int(self.heightratio*SHeight)

            self.button_list[exp_but].setdims(left,top,width,height)
            self.button_list[exp_but].setcol(self.butcol,self.text_col)