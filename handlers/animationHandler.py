# A partir del nombre de la animación, separa el nombre del objeto con el de la animación
# Esta animación posteriormente la guardarás en una lista y luego en una entrada nueva de tu diccionario
# En el diccionario vas a tener una pestaña de animaciones con objetos que denotan una lista de esas animaciones


from os import listdir, name
from os.path import isfile, join, isdir, split, splitdrive

from handlers.objHandlerv4 import ObjHandler

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
    def __init__(self):
        self.__obj_handler = ObjHandler()
        self.__frame = None

        self.__currentCategory = None
        self.__framesOfCategory = []
        self.__allAnimations = {}

    def load_animations(self, obj, assets_path):
        try:
            onlyfiles = [f for f in listdir(assets_path) if isfile(join(assets_path, f))]
        except FileNotFoundError:
            print("No se encontró la ruta de animaciones denotada por:", assets_path)
            return

        obj["Animations"] = {}

        print("CARGANDO ANIMACIONES DE:", obj["Name"])

        for file in sorted(onlyfiles, key=file_sort): # Después de todo este loop, resetear todo
            print("CARGANDO FRAME:", file)
            file_path = assets_path + "/" + file
            self.__frame = self.__obj_handler.load_obj(file_path)

            filename = self.__frame["Name"]
            filename = filename.split("/")[-1]

            base = filename.split("_")[1:]
            
            filename = "_".join(base)
            animation_category = "_".join(base[0:-1])

            self.__frame["Name"] = filename

            if animation_category != self.__currentCategory:
                print("Nueva categoría", animation_category)
                self.__load_category()
                self.__currentCategory = animation_category

            self.__add_frame()
        
        self.__load_category()
        self.__load_animation(obj)
        self.__reset()
            
    def __add_frame(self):
        # print(self.__frame)
        self.__framesOfCategory = self.__framesOfCategory + [self.__frame]

    def __load_category(self):
        if (self.__currentCategory != None):
            print("CARGANDO ANIMACIÓN", self.__currentCategory)

            category = {
                self.__currentCategory: self.__framesOfCategory
            }

            self.__allAnimations.update(category)
            self.__reset()

    def __load_animation(self, obj):
        obj["Animations"] = self.__allAnimations

    def __reset(self):
        self.__framesOfCategory = []