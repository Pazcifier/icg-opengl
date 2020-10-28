from os import listdir
from os.path import isfile, join, isdir

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

class TextureHandler(object):
    def load_textures(self, obj, assets_path):
        if(isdir(assets_path)):
            onlyfiles = [f for f in listdir(assets_path) if isfile(join(assets_path, f))]
            allTextures = []
            for file in onlyfiles:
                print("INCIO DE CARGA DE", file, "PARA", obj["Name"])
                surface = pygame.image.load(join(assets_path, file))
                surface = pygame.transform.flip(surface, False, True)

                image = pygame.image.tostring(surface, 'RGBA', 1)
                width, height = surface.get_rect().size

                loadedTexture = {
                    "Image": image,
                    "Height": height,
                    "Width": width
                }

                allTextures = allTextures + [loadedTexture]

            obj["TextureImage"] = {
                "Textures": allTextures,
                "Total": len(allTextures)
            }
            print("FIN DE CARGA DE TEXTURAS PARA", obj["Name"])
    
    def bind_texture(self, obj, actual):
        if ("TextureImage" in obj):
            textureID = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, textureID)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

            actual_texture = obj["TextureImage"]["Textures"][actual]
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, actual_texture["Height"], actual_texture["Width"], 0, GL_RGBA, GL_UNSIGNED_BYTE, actual_texture["Image"])

            glBindTexture(GL_TEXTURE_2D, 0)
            
            return textureID
        else:
            print("El objeto NO tiene textura")
            return 0