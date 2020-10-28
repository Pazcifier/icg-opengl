from os import listdir
from os.path import isfile, join

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

class TextureHandler():
    def load_textures(self, obj, file):
        print("INICIO DE CARGA DE TEXTURA DE", file, "PARA", obj["Name"])
        surface = pygame.image.load(file)
        surface = pygame.transform.flip(surface, False, True)

        image = pygame.image.tostring(surface, "RGBA", 1)
        width, height = surface.get_rect().size

        # total_textures = len(obj["TextureImages"]) + 1

        obj["TextureImage"] = {
            "Image": image,
            "Height": height,
            "Width": width,
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
            return 0