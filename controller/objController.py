import pygame
from pygame.locals import *

from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

# Hacer un AnimationController

action = {
    "NONE": 0,
    "MOVE": 1,
    "CROUCH": 2,
    "CROUCH_MOVE": 3,
    "PRAISE": 4,
    "TAUNT": 5,
    "JUMP": 6
}

class ObjController():
    def __init__(self):
        self.__obj_handler = ObjHandler()
        self.__texture_handler = TextureHandler()
        self.__animation_handler = AnimationHandler()

        self.__obj = {}

        self.__action = action["NONE"]
        self.__animation = None

        self.__hasAnimations = False
        self.__hasTextures = False

        self.__crouch = False

    def get_obj(self):
        return self.__obj

    def load_model(self, path):
        self.__obj = self.__obj_handler.load_obj(path)

    def load_textures(self, path):
        self.__texture_handler.load_textures(self.__obj, path)
        self.__hasTextures = True

    def load_animations(self, path):
        self.__animation_handler.load_animations(self.__obj, path)
        self.__hasAnimations = True

    def bind_texture(self, gl_texture, texture_name):
        self.__texture_handler.bind_texture(self.__obj, gl_texture, texture_name)

    def hasAnimations(self):
        return self.__hasAnimations

    def play_frame(self, frame):
        numberFrames = len(self.__animation) - 1
        frame += 1

        if (frame >  numberFrames):
            frame = 0
        
        return (frame, self.__animation[frame])

    def __select_animation(self):
        animations = self.__obj["Animations"]

        if self.__action == action["NONE"]:
            self.__animation = animations["stand"]

        if self.__action == action["MOVE"]:
            self.__animation = animations["run"]
        
        if self.__action == action["CROUCH"]:
            self.__animation = animations["crouch_stand"]

        if self.__action == action["CROUCH_MOVE"]:
            self.__animation = animations["crouch_walk"]

        if self.__action == action["JUMP"]:
            self.__animation = animations["jump"]
        
        if self.__action == action["PRAISE"]:
            self.__animation = animations["wave"]

        if self.__action == action["TAUNT"]:
            self.__animation = animations["flip"]


    def controls(self, keys, event):
        if event == pygame.KEYUP:
            print("STOP")
            if self.__crouch:
                self.__action = action["CROUCH"]
            else:
                self.__action = action["NONE"]
        
        if event == pygame.KEYDOWN:
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

            if (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
                if self.__crouch:
                    self.__action = action["CROUCH_MOVE"]
                else:
                    self.__action = action["MOVE"]
                
                if keys[pygame.K_w]:
                    print("Hacia adelante")
                if keys[pygame.K_s]:
                    print("Hacia atras")
                if keys[pygame.K_a]:
                    print("Hacia izquierda")
                if keys[pygame.K_d]:
                    print("Hacia derecha")

            if (keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]):
                print("AGACHADO")
                self.__action = action["CROUCH"]
                self.__crouch = not self.__crouch

            if keys[pygame.K_UP]:
                self.__action = action["PRAISE"]
                self.__reset_states()
            
            if keys[pygame.K_DOWN]:
                self.__action = action["TAUNT"]
                self.__reset_states()

            if keys[pygame.K_SPACE]:
                self.__action = action["JUMP"]
                self.__reset_states()

        if (self.__hasAnimations):
            self.__select_animation()

    def __reset_states(self):
        self.__crouch = False