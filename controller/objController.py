from camera.trackBall import TrackBall
import pygame
from pygame.locals import *

from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

from camera.trackBall import TrackBall

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
    def __init__(self, camera=False):
        self.__obj_handler = ObjHandler()
        self.__texture_handler = TextureHandler()
        self.__animation_handler = AnimationHandler()

        if camera:
            self.__camera = TrackBall([0,0,0], 10, 90, 1)

        self.__obj = {}
        self.__action = action["NONE"]

        self.__hasAnimations = False
        self.__hasTextures = False

        self.__crouch = False

    def get_obj(self):
        return self.__obj

    def get_actions(self):
        return action

    def get__action(self):
        return self.__action

    def load_camera(self):
        self.__camera.loadMatrix()

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

    def __reset_states(self):
        self.__crouch = False