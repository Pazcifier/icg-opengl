from os import listdir
from os.path import isfile, join

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

class TextureHandler(object):
    def __init__(self, obj_handler):
        self.__obj_handler = obj_handler

    def load_textures(self, assets_path):
        onlyfiles = [f for f in listdir(assets_path) if isfile(join(assets_path, f))]
        for file in onlyfiles:
            print("INCIO DE CARGA DE", file)
            filename = file.split('.')[0]

            surface = pygame.image.load(join(assets_path, file))
            surface = pygame.transform.flip(surface, False, True)

            image = pygame.image.tostring(surface, 'RGBA', 1)
            width, height = surface.get_rect().size

            obj = self.__obj_handler.get_obj(filename)

            obj["TextureImage"] = {
                "Image": image,
                "Height": height,
                "Width": width
            }
    
    def bind_texture(self, obj):
        if ("TextureImage" in obj):
            textureID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, textureID)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, obj["TextureImage"]["Height"], obj["TextureImage"]["Width"], 0, GL_RGBA, GL_UNSIGNED_BYTE, obj["TextureImage"]["Image"])

            glBindTexture(GL_TEXTURE_2D, 0)
            
            return textureID
        else:
            print("El objeto NO tiene textura")