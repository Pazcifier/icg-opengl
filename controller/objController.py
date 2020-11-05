from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

class ObjController():
    def __init__(self):
        self.__obj_handler = ObjHandler()
        self.__texture_handler = TextureHandler()

        self.__obj = {}

    def get_obj(self):
        return self.__obj

    def load_model(self, path):
        self.__obj = self.__obj_handler.load_obj(path)

    def load_textures(self, path):
        self.__texture_handler.load_textures(self.__obj, path)

    def bind_texture(self, gl_texture, texture_name):
        self.__texture_handler.bind_texture(self.__obj, gl_texture, texture_name)