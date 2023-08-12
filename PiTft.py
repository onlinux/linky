#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame

# set up the colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
DARKSLATEGREY = (47, 79, 79)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
MYGREEN = (0, 96, 65)
DARKORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 100, 0)
NAVY = (16, 22, 137)
LIGHTBLUE = (0, 113, 188)

class PiTft:
    'Pi Tft screen class'
    screen = None

    def __init__(self, title='PiTft', bgc=BLACK, no_frame=False, display_clock=True):
        """
        Initializes a new pygame screen using the framebuffer.
        Based on "Python GUI in Linux frame buffer
        """
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print("I'm running under X display = {0}".format(disp_no))

        try:
            pygame.init()
            pygame.mixer.quit()
        except pygame.error:
            print('Driver:  failed.')

        pygame.display.set_caption(title)

        if display_clock:
            size = (480, 360)
        else:
            size = (480, 8 * 1.5 * 18)

        print("Framebuffer size: %d x %d" % (size[0], size[1]))

        # Set up the drawing window
        if no_frame:
            self.screen = pygame.display.set_mode(size, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(size)
        pygame.mouse.set_visible(True)
        # Clear the screen to start
        self.bgc = bgc
        self.screen.fill(self.bgc)
        # Initialise font support
        pygame.font.init()
        # Render the screen
        #  print(pygame.display.Info())
        pygame.display.update()

    def __del__(self):
        # Destructor to make sure pygame shuts down, etc."
        print("del pygame instance")

    def clear(self, colour=None):
        if colour == None:
            colour = self.bgc
        self.screen.fill(colour)

    def setBackgroundColour(self, colour=None):
        if colour != None:
            self.bgc = colour

