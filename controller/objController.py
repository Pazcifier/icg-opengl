from camera.trackBall import TrackBall
import pygame
from pygame.locals import *

import math

from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

from camera.trackBall import TrackBall

from controller.openglController import (translate, rotate)

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
    def __init__(self, camera=False, repeat=False):
        self.__obj_handler = ObjHandler(repeat)
        self.__texture_handler = TextureHandler()
        self.__animation_handler = AnimationHandler()

        self.__position = [0,0,0]
        self.__rotation = 0

        if camera:
        #foco[0] izquierda y derecha
        #foco[1] adelante y atrás
        #foco[2] arriba y abajo

        #elev rotación adelante y atrás
        #rot rotación sobre el eje
        #dist adelante y atrás

            self.__camera = TrackBall([0,0,10], 10, 90, 5)

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

    def load_character(self):
        rotate(self.__rotation, 0, 0, 1)
        translate(self.__position[0], self.__position[1], self.__position[2])

    def load_camera(self):
        self.__camera.loadMatrix()

    def get_camera(self):
        return self.__camera

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
                    self.__move(5)
                if keys[pygame.K_s]:
                    print("Hacia atrás")
                    self.__move(-5)
                if keys[pygame.K_a]:
                    print("Hacia izquierda")
                    self.__rotate(-5)
                if keys[pygame.K_d]:
                    print("Hacia derecha")
                    self.__rotate(5)

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

            if keys[pygame.K_LEFT]:
                self.__camera.rot -= 5

            if keys[pygame.K_RIGHT]:
                self.__camera.rot += 5

    def __reset_states(self):
        self.__crouch = False

    def __move(self, dist):
        # self.__walk(dist)
        self.__camera.walk(dist)

    def __walk(self, dist):
        x = math.cos(math.radians(self.__rotation * math.pi/180)) * dist
        z = math.sin(math.radians(self.__rotation * math.pi/180)) * dist

        print("Posiciones de Player", self.__position)
        print("X y Z de Player", (x,z))

        self.__position[0] += x
        self.__position[2] += z
    
    def __rotate(self, rot):
        self.__rotation -= rot
        self.__camera.rot += rot
        print(self.__rotation, self.__camera.rot)