# Clase para parsear y dibujar archivos .obj

#1. o -> Reviso si tengo una línea llamada o, si existe, la clave de mi HashMap es el valor de o, sino es el nombre del archivo
#2. # -> Comentarios, ignoradas a menos que contenga #Fin Archivo
#3. v -> Función de carga de vértices. Guardarlos en una lista
#4. f -> Función de carga de caras. Tomar la posición dada-1 y buscarlo en la lista de vértices

#Función de dibujado: glDrawElements y glDrawArrays (prioridad)

# Cambiar el parser para que todo se guarde en un mismo array -> de append a concat
# Agregar propiedades para que tengamos los vértices listos para hacer DrawElements y otro para DrawArrays

class ObjHandler():
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
        self.__textures = []
        self.__faceTextures = []
        self.__vertexTextures = []
        
        self.__loaded = {}

    def load_obj(self, file, animation=False):
        print("INCIO DE CARGA DE", file)
        f = open(file, "r")
        if (animation):
            filename = file.split("/")[4]
        else:
            filename = file.split("/")[3]
        self.__name = filename
        file_lines = f.readlines()
        for line in file_lines:
            metadata = line.replace("\n", "").split(' ')
            line_type = metadata[0]
            line_info = metadata[1:]
            while("" in line_info):
                line_info.remove('')
            self.__load_line(line_type, line_info)
        if (not animation):
            self.__eof()
        else:
            return self.__build_object(filename)
            

    def __load_line(self, line_type, line):
        if (line_type == 'o'):
            self.__load_name(line)
        elif (line_type == 'v'):
            self.__load_vertex(line)
        elif (line_type == 'vn'):
            self.__load_vertexnormal(line)
        elif (line_type == 'vt'):
            self.__load_vertextexture(line)
        elif (line_type == 'f'):
            self.__load_face(line)
        elif (line_type == "#"):
            self.__comment(line)
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

    def __load_vertextexture(self, line):
        textureW = max(0, min(float(line[0]), 1))
        textureH = max(0, min(float(line[1]), 1))
        #Carga de texturas
        self.__textures = self.__textures + [(textureW, textureH)]

    def __load_face(self, line):
        #Carga de la cara
        # self.__numFaces = self.__numFaces + 1
        for face in line:
            if ("/" in face):
                faces = face.split('/')
                if (len(faces) > 2):
                    self.__load_face_textures(faces)
                else:
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

    def __load_face_textures(self, faces):
        vertexFace = faces[0]
        normalFace = faces[1]
        textureFace = faces[2]

        #Carga de caras de vértices
        self.__elements = self.__elements + [(int(vertexFace) - 1)]
        self.__arrayElements = self.__arrayElements + [self.__arrays[int(vertexFace) - 1]]

        #Carga de caras de normales
        self.__faceNormals = self.__faceNormals + [(int(normalFace) - 1)]
        self.__vertexNormals = self.__vertexNormals + [self.__normals[int(normalFace) - 1]]

        #Carga de texturas
        self.__faceTextures = self.__faceTextures + [(int(textureFace) - 1)]
        self.__vertexTextures = self.__vertexTextures + [self.__textures[int(textureFace) - 1]]
    
    def __comment(self, line):
        # Comentarios del archivo
        comment = " ".join(line)
        print("COMENTARIO DEL ARCHIVO:", comment)

    def __eof(self):
        #Revisión de última línea
        print("FIN DE CARGA DE ARCHIVO")
        self.__save()

    def __save(self):
        # Guarda el objeto cargado
        print("GUARDANDO DATOS EN CLAVE:", self.__name)
        self.__loaded.update({ 
            self.__name: {
                "Name": self.__name,
                "Arrays": self.__arrays, 
                "Elements": self.__elements, 
                "ArrayElements": self.__arrayElements,
                "Normals": self.__normals,
                "FaceNormals": self.__faceNormals,
                "VertexNormals": self.__vertexNormals,
                "Textures": self.__textures,
                "FaceTextures": self.__faceTextures,
                "VertexTextures": self.__vertexTextures
            } 
        })
        self.__reset()

    def __build_object(self, filename):
        # Retorna el objeto en vez de guardarlo (ANIMACIONES)

        # Cleansing del nombre del archivo
        splitted_name = filename.split("_")
        splitted_name = splitted_name[1:]
        separator = "_"
        name = separator.join(splitted_name)

        self.__name = name.split(".")[0]

        object = {
            "Name": self.__name,
            "Arrays": self.__arrays, 
            "Elements": self.__elements, 
            "ArrayElements": self.__arrayElements,
            "Normals": self.__normals,
            "FaceNormals": self.__faceNormals,
            "VertexNormals": self.__vertexNormals,
            "Textures": self.__textures,
            "FaceTextures": self.__faceTextures,
            "VertexTextures": self.__vertexTextures
        }
        self.__reset()
        return object
    
    def __reset(self):
        # Reseteo de variables
        self.__name = ""

        self.__arrays = []
        self.__elements = []
        self.__arrayElements = [] # DrawArrays
        self.__normals = []
        self.__faceNormals = []
        self.__vertexNormals = []
        self.__textures = []
        self.__faceTextures = []
        self.__vertexTextures = []

    def get_obj(self, obj_name):
        # Obtención de un objeto guardado
        return self.__loaded[obj_name]

    def get_all(self):
        # Obtención de todas las keys
        return list(self.__loaded.keys())