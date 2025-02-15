from OpenGL.GL import *
from OpenGL.GLU import *

# ADDERS

def add_material(diffuse=None, specular=None, shininess=32):
    """
    Realiza el pipeline para agregar materiales a los objetos cargados (Difuso, Especular, Brillo y Ambiente).
    En caso de no pasar alguno de los parámetros, este no se aplica

    diffuse     -- Array con los valores RGBA del color difuso (default: None)
    specular    -- Array con los valores RGBA del color especular (default: None)
    shininess   -- Brillo del material (default: 32)
    """
    if ((diffuse != None) and (len(diffuse) == 4)):
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    if ((specular != None) and (len(specular) == 4)):
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, shininess)
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1,0.1,0.1,1])


def add_light(light, diffuse=[], specular=[], position=[0,0,0,1]):
    """
    Realiza el pipeline para agregar los parámetros de la luz pasada a la escena (Difuso, Especular, Posición y Ambiente).
    En caso de no pasar alguno de los parámetros, este no se aplica

    light       -- Parámetro OpenGL referente a la luz (REQUERIDO)
    diffuse     -- Array con los valores RGBA del color difuso (default: None)
    specular    -- Array con los valores RGBA del color especular (default: None)
    position    -- Posición de la luz (default: [0,0,0,1])
    """
    if ((diffuse != []) and (len(diffuse) == 4)):
        glLight(light, GL_DIFFUSE, diffuse)
    if ((specular != []) and (len(specular) == 4)):
        glLight(light, GL_SPECULAR, specular)

    glLight(light, GL_POSITION, position)
    glLight(light, GL_AMBIENT, [0.1,0.1,0.1,1])

# CONFIGURATORS

def configure_light_position(light, position):
    """
    Modifica la posición de la luz

    light       -- Parámetro OpenGL (REQUERIDO)
    position    -- Nueva posición de la luz (REQUERIDO)
    """
    glLight(light, GL_POSITION, position)

def configure_frustum(left, right, bottom, top, distNear, distFar):
    """
    Aplica glFrustum

    left, right         -- Coordenadas máximas del plano vertical (REQUERIDOS)
    bottom, top         -- Coordenadas máximas del plano horizontal (REQUERIDAS)
    distNear, distFar   -- Distancias referentes a la escena (REQUERIDAS)
    """
    glFrustum(left, right, bottom, top, distNear, distFar)

# DRAWERS

def drawArrays(obj):
    """
    Carga y dibuja el objeto mediante glDrawArrays

    obj     -- Objeto a dibujar (REQUERIDO)
    """
    __load_vertexes(obj["ArrayElements"])
    __load_normals(obj["VertexNormals"])
    __load_texture_coords(obj["VertexTextures"])
    glDrawArrays(GL_TRIANGLES, 0, len(obj["ArrayElements"]))

def drawElements(obj):
    """
    Carga y dibuja el objeto mediante glDrawElements

    obj     -- Objeto a dibujar (REQUERIDO)
    """
    __load_vertexes(obj["Arrays"])
    __load_normals(obj["VertexNormals"])
    __load_texture_coords(obj["VertexTextures"])
    glDrawElements(GL_TRIANGLES, len(obj["Elements"]), GL_UNSIGNED_INT, obj["Elements"])

# ENABLERS

def enable(parameter):
    """
    Ejecuta glEnable

    parameter   -- El parámetro OpenGL (REQUERIDO)
    """
    glEnable(parameter)

def enable_type(array_type):
    """
    Ejecuta glEnableClientState

    array_type  -- El parámetro OpenGL (REQUERIDO)
    """
    glEnableClientState(array_type)

def disable_type(array_type):
    """
    Ejecuta glDisableClientState

    array_type  -- El parámetro OpenGL (REQUERIDO)
    """
    glDisableClientState(array_type)

# LOADERS

def __load_vertexes(vertexes, dimensions=3):
    """
    Carga los vértices del objeto

    dimensions  -- Dimensiones del objeto (default: 3)
    vertexes    -- Vértices del objeto (REQUERIDO)
    """
    glVertexPointer(dimensions, GL_FLOAT, 0, vertexes)

def __load_normals(vertexes):
    """
    Carga las normales del objeto

    vertexes    -- Normales del objeto (REQUERIDO)
    """
    glNormalPointer(GL_FLOAT, 0, vertexes)

def __load_texture_coords(vertexes, dimensions=2):
    """
    Carga las coordenadas de textura del objeto

    dimensions  -- Dimensiones de la textura (default: 2)
    vertexes    -- Coordenadas de textura del objeto (REQUERIDO)
    """
    glTexCoordPointer(dimensions, GL_FLOAT, 0, vertexes)

# OPERATORS

def identity():
    """
    Carga la matriz de identidad
    """
    glLoadIdentity()

def translate(x=0, y=0, z=0):
    """
    Traslada el objeto

    x   -- Coordenada X (default: 0)
    y   -- Coordenada Y (default: 0)
    z   -- Coordenada Z (default: 0)
    """
    glTranslatef(x, y, z)

def scale(x=0, y=0, z=0):
    """
    Escala el objeto

    x   -- Coordenada X (default: 0)
    y   -- Coordenada Y (default: 0)
    z   -- Coordenada Z (default: 0)
    """
    glScale(x, y, z)

def rotate(angle=0, rx=False, ry=False, rz=False):
    """
    Rota el objeto

    angle   -- Ángulo de rotación (default: 0)
    rx      -- Rotar en el eje X? (default: False)
    ry      -- Rotar en el eje Y? (default: False)
    rz      -- Rotar en el eje Z? (default: False)
    """
    glRotatef(angle, rx, ry, rz)

def clear(buffer):
    """
    Limpia el buffer

    buffer  -- Buffer OpenGL (REQUERIDO)
    """
    glClear(buffer)

# SETTERS

def set_background_color(red=255, green=255, blue=255, alpha=1):
    """
    Aplica glClearColor

    red     -- Valor del color rojo (0 - 255) (default: 255)
    green   -- Valor del color verde (0 - 255) (default: 255)
    blue    -- Valor del color azul (0 - 255) (default: 255)
    alpha   -- Valor del alfa (0 - 1) (default: 1)
    """
    glClearColor(red / 255, green / 255, blue / 255, alpha)

def set_shade_model(shade_type):
    """
    Aplica glShadeModel

    shade_type  -- El tipo de shader a aplicar (REQUERIDO)
    """
    glShadeModel(shade_type)

def set_matrix_mode(mode):
    """
    Aplica glMatrixMode

    mode    -- El modo de matrix a aplicar (REQUERIDO)
    """
    glMatrixMode(mode)

def set_viewport(width, height, x=0, y=0):
    """
    Asigna el viewport

    widht   -- Ancho del viewport (REQUERIDO)
    height  -- Alto del viewport (REQUERIDO)
    x       -- Posición horizontal inicial del viewport (default: 0)
    y       -- Posición vertical inicial del viewport (default: 0)
    """
    glViewport(x, y, width, height)

# TEXTURES

def active_texture(texture):
    """
    Aplica glActiveTexture a la textura pasada

    texture     -- El parámetro OpenGL (REQUERIDO)
    """
    glActiveTexture(texture)

def bind_texture(texture=0):
    """
    Aplica glBindTexture

    texture     -- Textura del objeto (default: 0)
    """
    glBindTexture(GL_TEXTURE_2D, texture)

def generate_texture(size=1):
    """
    Aplica glGenTextures

    size        -- Cantidad de texturas a ser generada (default: 1)
    """
    return glGenTextures(size)

def apply_filter(filter, preference=GL_NEAREST):
    """
    Aplica glTexParameteri

    filter      -- Primitiva de filtro de OpenGL (REQUERIDO)
    preference  -- Primitiva de preferencia en donde aplicar el filtro (default: GL_NEAREST)
    """
    glTexParameteri(GL_TEXTURE_2D, filter, preference)

def apply_texture(height, width, image):
    """
    Aplica glTexImage2D

    height      -- Altura de la textura (REQUERIDO)
    width       -- Anchura de la textura (REQUERIDO)
    image       -- Imagen de la textura (REQUERIDO)
    """
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, height, width, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)