# A partir del nombre de la animación, separa el nombre del objeto con el de la animación
# Esta animación posteriormente la guardarás en una lista y luego en una entrada nueva de tu diccionario
# En el diccionario vas a tener una pestaña de animaciones con objetos que denotan una lista de esas animaciones


from os import listdir, name
from os.path import isfile, join, isdir, split, splitdrive

import pygame

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

def file_sort(value):
    splitted_value = value.split("_")[1:]
    name_first = splitted_value[0:len(splitted_value) - 1]
    name_first = "_".join(name_first)
    number_second = splitted_value[-1].split(".")[0]
    return (name_first, int(number_second))

class AnimationHandler(object):
    def __init__(self, obj_handler):
        self.__obj_handler = obj_handler
        self.__obj = ""
        self.__frame = None
        self.__animation_obj = {
            "Category": "",
            "Frames": []
        }

    def load_animations(self, assets_path):
        try:
            onlyfiles = [f for f in listdir(assets_path) if isfile(join(assets_path, f))]
        except FileNotFoundError:
            print("No se encontró la ruta de animaciones denotada por:", assets_path)
            return

        self.__obj = self.__obj_handler.get_obj(assets_path.split("/")[-1])
        self.__obj["Animations"] = {
            "Keys": [],
            "Categories": []
        }

        print("CARGANDO ANIMACIONES DE:", self.__obj["Name"])

        for file in sorted(onlyfiles, key=file_sort): # Después de todo este loop, resetear todo
            print("CARGANDO FRAME:", file)
            file_path = assets_path + "/" + file
            self.__frame = self.__obj_handler.load_obj(file_path, True)

            animation_category = self.__frame["Name"].split("_")[0]

            if animation_category != self.__animation_obj["Category"]:
                print("Nueva categoría", animation_category)
                self.__obj["Animations"]["Keys"] = self.__obj["Animations"]["Keys"] + [animation_category]
                if len(self.__animation_obj["Category"]) == 0:
                    self.__animation_obj["Category"] = animation_category
                else:
                    self.__load_animation()
                    self.__animation_obj["Category"] = animation_category

            self.__add_frame()
        
        self.__load_animation()
        self.__reset()
            
    def __add_frame(self):
        self.__animation_obj["Frames"] = self.__animation_obj["Frames"] + [self.__frame]

    def __load_animation(self):
        print("CARGANDO ANIMACIÓN", self.__animation_obj["Category"])
        self.__obj["Animations"]["Categories"] = self.__obj["Animations"]["Categories"] + [self.__animation_obj]

        # print(self.__obj["Animations"])

        self.__animation_obj = {
            "Category": "",
            "Frames": []
        }

    def __reset(self):
        self.__frame = None
        self.__animation_obj = {
            "Category": "",
            "Frames": []
        }