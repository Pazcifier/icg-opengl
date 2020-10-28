import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from os import listdir
from os.path import isfile, join

from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

# Notas del profesor:
# Crear una clase obj que nos permita usar de controlador para realizar cambios
# Reducir la mayor cantidad de llamadas GL del main
# No es necesario tener debug en la entrega final
# Mientras más cosas al final, mejor!!

# def bind_texture(obj):
#     if ("TextureImage" in obj):
#         textureID = glGenTextures(1)
#         glBindTexture(GL_TEXTURE_2D, textureID)
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
#         glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

#         glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, obj["TextureImage"]["Height"], obj["TextureImage"]["Width"], 0, GL_RGBA, GL_UNSIGNED_BYTE, obj["TextureImage"]["Image"])

#         glBindTexture(GL_TEXTURE_2D, 0)
        
#         return textureID
#     else:
#         print("El objeto NO tiene textura")

def main():
    # Configuraciones
    zEnable = False
    clockW = False
    lineMode = False
    prof = 1
    angle = 0
    actual_obj = 0
    actual_texture = 0

    currentTime = 0
    deltaT = 0
    lastTime = 0
    frame = 0
    category = 0
    activeAnimation = False

    # Inicialización
    ## Pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    ## Parsers
    obj_handler = ObjHandler()
    texture_handler = TextureHandler()
    animation_handler = AnimationHandler(obj_handler)
    # texture_handler = TextureHandler(obj_handler)

    # obj_handler.load_objs('./assets/models')
    objs_path = "./assets/models/"
    obj_files = [f for f in listdir(objs_path) if isfile(join(objs_path, f))]

    for file in obj_files:
        obj_path = objs_path + file
        obj_handler.load_obj(obj_path)

    keys = obj_handler.get_all()
    load_obj = obj_handler.get_obj(keys[actual_obj])

    ## Animaciones
    for obj in keys:
        animation_path = "./assets/animations/" + obj
        # animation_handler.load_animations(animation_path)

    ## OpenGL
    glClearColor(0, 0.55, 0.98, 1)
    ### Texturas
    glEnable(GL_TEXTURE_2D)
    # glActiveTexture(GL_TEXTURE0)
    
    for obj in keys:
        texture_path = "./assets/textures/" + obj
        texture_handler.load_textures(obj_handler.get_obj(obj), texture_path)
    # texture_handler.load_textures('./assets/textures')
    texture = 0

    ### Iluminación
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1,0.1,0.1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 32)

    glEnable(GL_LIGHT0)

    glShadeModel(GL_SMOOTH)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    # glEnable(GL_LIGHTING)

    glEnable(GL_DEPTH_TEST)
    
    ### Viewport
    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, display[0], display[1])
    glFrustum(-1, 1, -1, 1, 1, 1000)

    # Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_w:
                    prof += 0.25
                if event.key == pygame.K_s:
                    prof -= 0.25
                if event.key == pygame.K_k:
                    texture = 0
                    actual_texture = 0

                    actual_obj += 1
                    if (actual_obj >= len(keys)):
                        actual_obj = 0
                    load_obj = obj_handler.get_obj(keys[actual_obj])
                if event.key == pygame.K_z:
                    zEnable = not zEnable
                    if zEnable:
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)
                if event.key == pygame.K_c:
                    clockW = not clockW
                    if clockW:
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)
                if event.key == pygame.K_l:
                    lineMode = not lineMode
                    if lineMode:
                        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                    else:
                        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                if event.key == pygame.K_t:
                    glActiveTexture(GL_TEXTURE0)
                    texture = texture_handler.bind_texture(load_obj, actual_texture)
                    glBindTexture(GL_TEXTURE_2D, texture)
                    if (texture > 0):
                        actual_texture += 1
                        if (actual_texture >= load_obj["TextureImage"]["Total"]):
                            actual_texture = 0
                if event.key == pygame.K_m:
                    if (not activeAnimation):
                        obj_animations = load_obj["Animations"]
                        all_categories = len(obj_animations["Keys"]) - 1
                        all_frames = obj_animations["Categories"][category]["Frames"]
                        max_frames = len(all_frames) - 1
                        load_obj_backup = load_obj
                        activeAnimation = True

                # glClearColor(R,G,B,A)


        ## Configuraciones
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -30)
        glScale(prof, prof, prof)
        glRotatef(angle, 0,1,0)
        glRotatef(angle, 1, 0, 0)
        angle += 0.1
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        ## Activaciones
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)

        ## Animaciones
        currentTime = pygame.time.get_ticks()
        deltaT += currentTime - lastTime
        lastTime = currentTime

        if activeAnimation:
            if (deltaT > 100):
                deltaT = 0
                load_obj = all_frames[frame]
                frame += 1
                # print(frame)
                if (frame > max_frames):
                    frame = 0
                    activeAnimation = False
                    load_obj = load_obj_backup
                    category += 1
                    if (category > all_categories):
                        category = 0

        ## Carga de vértices
        ### DrawArrays
        glVertexPointer(3, GL_FLOAT, 0, load_obj["ArrayElements"])
        ### DrawElements
        # glVertexPointer(3, GL_FLOAT, 0, load_obj["Arrays"])
        
        glNormalPointer(GL_FLOAT, 0, load_obj["VertexNormals"])
        glTexCoordPointer(2, GL_FLOAT, 0, load_obj["VertexTextures"])

        ## Dibujado
        glBindTexture(GL_TEXTURE_2D, texture)

        glDrawArrays(GL_TRIANGLES, 0, len(load_obj["ArrayElements"]))
        # glDrawElements(GL_TRIANGLES, len(load_obj["Elements"]), GL_UNSIGNED_INT, load_obj["Elements"])

        ## Desactivaciones
        glBindTexture(GL_TEXTURE_2D, 0)
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()

main()