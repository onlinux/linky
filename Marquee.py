#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import time
import random

# set up the colors
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
RED = (255,   0,   0)
GREEN = (0, 255,   0)
BLUE = (0,   0, 255)
MYGREEN = (0, 96, 65)
DARKORANGE = (255, 140, 0)
YELLOW = (255, 255, 0)
DARKGREEN = (0, 100, 0)
NAVY = (16, 22, 137)
LIGHTBLUE = (0, 113, 188)


class Marquee:
    def __init__(self, font, color=GREEN, ry=0, speed=5, bg=BLUE, direction=0):

        self.screen = pygame.display.get_surface()
        self.font = font
        self.tw, self.th = (0, 0)
        info = pygame.display.Info()  # width and height
        self.w, self.h = info.current_w, info.current_h

        if direction == 0:
            self.rx = self.w
        else:
            self.rx = 0

        self.ry = ry
        self.speed = speed
        self.color = color  # text color
        self.bg = bg  # background color
        self.direction = direction
        self.dict = {}
        self.text = None
        self.rect = ()

    def getRect(self):
        # return  rectangle
        rect = pygame.Rect(0, self.ry, self.w, self.th)
        return rect

    def addMsg(self, msg, color, name='message'):

        if len(msg) > 0:

            if not color:
                color = self.color

            surface = self.font.render(msg + "   ", 1, color)
            self.dict[name] = {'msg': msg, 'color': color, 'surface': surface}
            self.updateMsg()

    def delMsg(self, name):
        del self.dict[name]
        self.updateMsg()

    def updateMsg(self):
        line = ""
        for msg in self.dict:
            line = line + "   " + self.dict[msg]['msg']

        self.text = self.font.render(line, 1, self.color)
        self.tw, self.th = self.text.get_size()

    def update(self):
        if not self.text:
            return

        if self.direction == 0 and self.rx > -1 * self.tw:
            self.rx -= self.speed
            if self.rx <= self.tw * -1:
                self.rx = self.w

        elif self.direction == 1 and self.rx < self.w:
            self.rx += self.speed
            if self.rx >= self.w:
                self.rx = -1 * self.tw

        self.rect = self.text.get_rect()
        rect = self.rect.move(self.rx, self.ry)

        offset = 0
        for msg in self.dict:
            textSurface = self.dict[msg]['surface']
            self.screen.blit(textSurface, (self.rx + offset, self.ry))
            offset += textSurface.get_width()

        #pygame.draw.rect(self.screen, GREEN, rect, 1)

    def reset(self):
        self.dict.clear()
        self.text = None
