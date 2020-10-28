import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from obj import *

def main():
    pygame.init()
    display = (900,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    #Esta es la llamada a mi parser de OBJ, deben remplazarla por la de uds.
    model = Obj()
    model.parse("/home/sergio/Dropbox/py-cg/iluminacion/box_normales.obj")

    #Empiezo por setear los parametros del material del objeto a dibujar
    #Color difuso
    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    #Color ambiente (iluminacion indirecta)
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [0.1,0.1,0.1,1])
    #Color especular, para la parte de Lambert extendida por Phong
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    #Coeficiente especular
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 32)

    #Enciendo una de las 8 luces soportadas por OpenGL (GL_LIGHT0..7)
    glEnable(GL_LIGHT0)

    #Le digo al pipeline estatico que dibuje usando sombreado suaviazado (es decir Gouraud Shading)
    glShadeModel(GL_SMOOTH)

    #Ahora seteo las propiedades de la luz que habilite
    #Color difuso de la luz, el cual me da intensidad y color a la vez
    #Por ejemplo, para una luz blanca muy itensa seteo color blanco, para una menos intensa un tono de gris
    #Lo mismo para cualquier otro color y sus tonalidades.
    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    #La posicion de la luz me dice en que parte de la escena se encuentra el foco.
    #La cuarta coordenada determina el tipo de luz: 1 para una luz puntual, 0 para una direccional
    #Mucho cuidado al setear esta propiedad, pues se va a multiplicar por lo que haya en la matriz modelview en ese momento.
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
    #Cuanto aporta esta luz a la intensidad ambiente (iluminacion indirecta)
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    #El color especular de la luz
    glLight(GL_LIGHT0, GL_SPECULAR, [1,1,1,1])

    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glViewport(0,0,display[0],display[1])
    glFrustum(-1,1,-1,1,1,1000)

    ang = 0.0
    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    light = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_m:
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode( GL_FRONT_AND_BACK, mode)
                if event.key == pygame.K_z:
                    zBuffer = not zBuffer
                    if(zBuffer):
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)
                if event.key == pygame.K_b:
                    bfc = not bfc
                    if(bfc):
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)
                if event.key == pygame.K_c:
                    bfcCW = not bfcCW
                    if(bfcCW):
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)
                if event.key == pygame.K_l:
                    #Con la letra L prendo y apago la iluminacion
                    #notese que con la iluminacion prendida, se ignoran los colores de cada vertice y se toma
                    #unicamente los colores del material.
                    light = not light
                    if(light):
                        glEnable(GL_LIGHTING)
                    else:
                        glDisable(GL_LIGHTING)

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0,0.0, -2)
        glRotatef(ang, 0, 1, 0)
        glRotatef(ang, 0, 0, 1)
        glRotatef(ang, 1, 0, 0)
        ang += 0.5
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        #Para que la iluminacion funcione correctamente es indispensable pasarle un array de Normales
        #una para cada vertice
        #Primero habilito el array de normales
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, model.vertices)
        #Luego le paso el array en si
        glNormalPointer(GL_FLOAT, 0, model.normales)
        glColorPointer(3, GL_FLOAT, 0, model.colores)

        glDrawArrays(GL_TRIANGLES, 0, len(model.faces) * 3)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        pygame.display.flip()

main()