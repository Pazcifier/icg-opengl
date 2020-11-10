import pygame
from pygame.locals import *

class AnimationController():
    def __init__(self, obj, actions):
        self.__obj = obj
        self.__actions = actions
        
        self.__animation = None
        self.__frame = -1
        self.__deltaT = 0
        self.__lastTime = 0

        self.__playing = False
    
    def play_animation(self, action):
        currentTime = pygame.time.get_ticks()
        self.__deltaT += currentTime - self.__lastTime
        self.__lastTime = currentTime

        if (self.__deltaT > 100):
            self.__deltaT = 0
            self.__select_animation(action)
            return self.__get_frame()
        
        return self.__animation[self.__frame]

    def __select_animation(self, action):
        animations = self.__obj["Animations"]
        last_animation = self.__animation

        if not self.__playing:
            if action == self.__actions["NONE"]:
                self.__animation = animations["stand"]

            if action == self.__actions["MOVE"]:
                self.__animation = animations["run"]
            
            if action == self.__actions["CROUCH"]:
                self.__animation = animations["crouch_stand"]

            if action == self.__actions["CROUCH_MOVE"]:
                self.__animation = animations["crouch_walk"]

            if action == self.__actions["JUMP"]:
                self.__animation = animations["jump"]
                self.__playing = True
            
            if action == self.__actions["PRAISE"]:
                self.__animation = animations["wave"]
                self.__playing = True

            if action == self.__actions["TAUNT"]:
                self.__animation = animations["flip"]
                self.__playing = True
        
        if last_animation != self.__animation:
            self.__frame = 0

    def __get_frame(self):
        numberFrames = len(self.__animation) - 1
        self.__frame += 1

        if (self.__frame > numberFrames):
            self.__frame = 0
            if self.__playing:
                self.__playing = False

        return self.__animation[self.__frame]