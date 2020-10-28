import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from handlers.objHandlerv3 import ObjHandler
from handlers.textureHandlerv2 import TextureHandler

from camera.trackBall import TrackBall
from camera.fps import FPS

def main():
    # Configuraciones
    zEnable = False
    clockW = False
    lineMode = False
    prof = 1
    angle = 0
    actual = 0

    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable(GL_TEXTURE_2D)
    glActiveTexture(GL_TEXTURE0)

    # Carga de objetos
    obj_handler = ObjHandler()
    texture_handler = TextureHandler(obj_handler)

    obj_handler.load_objs('./assets/models')
    texture_handler.load_textures('./assets/textures')

    keys = obj_handler.get_all()
    load_obj = obj_handler.get_obj(keys[actual])

    cam = TrackBall()
    cam.foco = [0,0,-30]
    cam.elev = -20
    cam.rot = 0
    cam.dist = 35

    cam2 = FPS()
    cam2.pos = [0,0,-25]
    cam2.elev = 25
    cam2.rot = 15

    def info():
        print("===AYUDA E INFORMACIÓN===")
        print("H - Muestra esta información")
        print("K - Cambiar el modelo en pantalla - Modelo actual:", keys[actual])
        print("Z - Activar/Desactivar Z-Buffer, por defecto False - Valor actual:", zEnable)
        print("C - Cambiar modo de Backface Culling, por defecto False (Clock-wise) - Valor actual:", clockW)
        print("L - Cambiar el modo de dibujo del modelo, por defecto False (Fill) - Valor actual:", lineMode)
        print("W/S - Aumentar/Disminuir la escala del modelo - Valor actual:", prof)

    # print(load_obj["VertexTextures"])

    print(glGetString(GL_VERSION))

    glMatrixMode(GL_PROJECTION)
        
    glLoadIdentity()
    
    glViewport(0,0,800,600)

    glFrustum(-1,1,-1,1,1,10000)
    # glEnable(GL_DEPTH_TEST)

    verts = [-1,-1,-2, 1,-1,-2, 0,1,-2]
    colors= [ 1,0,0, 0,0,0, 0,0,1]

    # Configuración de Iluminación
    ## Material del objeto
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1,0.1,0.1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 32)

    glEnable(GL_LIGHT0)

    glShadeModel(GL_FLAT)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_LIGHTING)
    info()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_h:
                    info()
                if event.key == pygame.K_w:
                    prof += 0.25
                    # cam2.walk(1)
                if event.key == pygame.K_s:
                    prof -= 0.25
                    # cam2.walk(-1)
                if event.key == pygame.K_k:
                    actual += 1
                    if (actual >= len(keys)):
                        actual = 0
                    load_obj = obj_handler.get_obj(keys[actual])
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
                if event.key == pygame.K_RIGHT:
                    cam2.rot -= 5
                if event.key == pygame.K_LEFT:
                    cam2.rot += 5
                if event.key == pygame.K_UP:
                    cam2.elev += 5
                if event.key == pygame.K_DOWN:
                    cam2.elev -= 5
                if event.key == pygame.K_t:
                    glActiveTexture(GL_TEXTURE0)
                    texture = texture_handler.bind_texture(load_obj)
                    # glBindTexture(GL_TEXTURE_2D, texture)
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        #activo el stack de matrices MODELVIEW
        glMatrixMode(GL_MODELVIEW)
        #Limpio todas la transformaciones previas, seteando una identidad en el tope del stack
        glLoadIdentity()

        # cam.rot += 5

        # cam2.loadMatrix()

        glTranslatef(0,0,-30)
        glScale(prof,prof,prof)
        glRotatef(angle, 0,1,0)
        glRotatef(angle, 1, 0, 0)

        angle += 0.1

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        # glEnableClientState(GL_COLOR_ARRAY)

        glNormalPointer(GL_FLOAT, 0, load_obj["VertexNormals"])
        glTexCoordPointer(2, GL_FLOAT, 0, load_obj["VertexTextures"])
        # glColorPointer(3, GL_FLOAT, 0, colors)
        

        # CARGA DE DRAWARRAYS
        glVertexPointer(3, GL_FLOAT, 0, load_obj["ArrayElements"])
        
        glBindTexture(GL_TEXTURE_2D, texture)

        glDrawArrays(GL_TRIANGLES, 0, len(load_obj["ArrayElements"]))

        # CARGA PARA DRAWELEMENTS
        # glVertexPointer(3, GL_FLOAT, 0, load_obj["Arrays"])
        # glDrawElements(GL_TRIANGLES, len(load_obj['Elements']), GL_UNSIGNED_INT, load_obj['Elements'])

        glBindTexture(GL_TEXTURE_2D, 0)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()

main()