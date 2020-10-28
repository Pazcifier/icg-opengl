# Clase para parsear y dibujar archivos .obj

#1. o -> Reviso si tengo una línea llamada o, si existe, la clave de mi HashMap es el valor de o, sino es el nombre del archivo
#2. # -> Comentarios, ignoradas a menos que contenga #Fin Archivo
#3. v -> Función de carga de vértices. Guardarlos en una lista
#4. f -> Función de carga de caras. Tomar la posición dada-1 y buscarlo en la lista de vértices

#Función de dibujado: glDrawElements y glDrawArrays (prioridad)

# Cambiar el parser para que todo se guarde en un mismo array -> de append a concat
# Agregar propiedades para que tengamos los vértices listos para hacer DrawElements y otro para DrawArrays

from os import listdir
from os.path import isfile, join

class ObjHandler(object):
    def __init__(self):
        self.__name = ""
        # self.__numVertx = 0
        # self.__numFaces = 0

        self.__arrays = []
        self.__elements = []
        self.__arrayElements = [] # DrawArrays
        self.__normals = []
        self.__faceNormals = []
        self.__vertexNormals = []
        
        self.__loaded = {}

    def load_objs(self, assets_path):
        onlyfiles = [f for f in listdir(assets_path) if isfile(join(assets_path, f))]
        for file in onlyfiles:
            print("INCIO DE CARGA DE", file)
            f = open(join(assets_path, file), "r")
            filename = file.split('.')[0]
            self.__name = filename
            file_lines = f.readlines()
            for line in file_lines:
                metadata = line.replace("\n", "").split(' ')
                line_type = metadata[0]
                line_info = metadata[1:]
                if (len(line_info) > 3):
                    while("" in line_info):
                        line_info.remove('')
                self.__load_line(line_type, line_info)

    def __load_line(self, line_type, line):
        if (line_type == 'o'):
            self.__load_name(line)
        elif (line_type == 'v'):
            self.__load_vertex(line)
        elif (line_type == 'vn'):
            self.__load_vertexnormal(line)
        elif (line_type == 'f'):
            self.__load_face(line)
        elif (line_type == "#"):
            self.__eof(line)
        # print("El tipo de línea es:", line_type)
        # types = {
        #     'o': self.__load_name(line),
        #     'v': self.__load_vertex(line),
        #     'f': self.__load_face(line),
        #     '#': self.__eof(line)
        # }
        # return types.get(line_type, 'Invalid')
    
    def __load_name(self, line):
        #Carga del nombre
        self.__name = line[0]
    
    def __load_vertex(self, line):
        #Carga del vértice
        # self.__numVertx = self.__numVertx + 1
        #for value in line:
        self.__arrays = self.__arrays + [(float(line[0]), float(line[1]), float(line[2]))]

    def __load_vertexnormal(self, line):
        #Carga de normales de un vértice
        self.__normals = self.__normals + [(float(line[0]), float(line[1]), float(line[2]))]

    def __load_face(self, line):
        #Carga de la cara
        # self.__numFaces = self.__numFaces + 1
        for face in line:
            if ("/" in face):
                faces = face.split('/')
                self.__load_face_normals(faces)
            else:         
                for face in line:
                    self.__elements = self.__elements + [(int(face) - 1)]
                    self.__arrayElements = self.__arrayElements + [self.__arrays[int(face) - 1]]

    def __load_face_normals(self, faces):
        vertexFace = faces[0]
        normalFace = faces[1]

        #Carga de caras de vértices
        self.__elements = self.__elements + [(int(vertexFace) - 1)]
        self.__arrayElements = self.__arrayElements + [self.__arrays[int(vertexFace) - 1]]

        #Carga de caras de normales
        self.__faceNormals = self.__faceNormals + [(int(normalFace) - 1)]
        self.__vertexNormals = self.__vertexNormals + [self.__normals[int(normalFace) - 1]]
    
    def __eof(self, line):
        #Revisión de última línea
        comment = " ".join(line)
        if (comment.lower().__contains__("fin")):
            print("FIN DE CARGA DE ARCHIVO")
            self.__save()
        else:
            print("COMENTARIO DEL ARCHIVO:", comment)

    def __save(self):
        # Guarda el objeto cargado
        print("GUARDANDO DATOS EN CLAVE:", self.__name)
        self.__loaded.update({ 
            self.__name: {
                "Arrays": self.__arrays, 
                "Elements": self.__elements, 
                "ArrayElements": self.__arrayElements,
                "Normals": self.__normals,
                "FaceNormals": self.__faceNormals,
                "VertexNormals": self.__vertexNormals
            } 
        })
        self.__reset()
    
    def __reset(self):
        # Reseteo de variables
        self.__name = ""
        self.__arrays = []
        self.__elements = []
        self.__arrayElements = [] # DrawArrays
        self.__normals = []
        self.__faceNormals = []
        self.__vertexNormals = []

    def get_obj(self, obj_name):
        # Obtención de un objeto guardado
        return self.__loaded[obj_name]

    def get_all(self):
        # Obtención de todas las keys
        return list(self.__loaded.keys())