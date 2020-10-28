import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
from obj import *

#Uso esta funcion para compilar de forma individual el codigo de cada componente del shader (vertex y fragment)
#Le paso el path al archivo y el tipo de shader (GL_VERTEX_SHADER o GL_FRAGMENT_SHADER)
def compileProgram(path, type):
    #Leo el codigo fuente desde el archivo
    sourceFile = open(path, "r")
    source = sourceFile.read()
    #Creo un shader vacio en memoria de video, del tipo indicado
    #En la variable shader queda almacenado un indice que nos va a permitir identificar este shader de ahora en mas
    shader = glCreateShader(type)
    #Le adjunto el codigo fuente leido desde el archivo
    glShaderSource(shader, source)
    #Intento compilarlo
    glCompileShader(shader)
    #Con la funcion glGelShaderiv puedo obtener el estado del compilador de shaders
    #En este caso le pido el stado de la ultima compilacion ejecutada
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        #Si la compilacion falla, muestro el error y retorno 0 (shader nulo)
        print path + ': ' + glGetShaderInfoLog(shader)
        #Me aseguro de liberar los recursos que reserve en memoria de vide, ya que no los voy a usar
        glDeleteShader(shader)
        return 0
    else:
        return shader

#Esta funcion me permite crear un programa de shading completo, basado en un vertex y un fragment shader
#Le paso el path a ambos codigos fuentes
def createShader(vSource, fSource):
    #Creo y compilo el vertex shader
    vProgram = compileProgram(vSource, GL_VERTEX_SHADER)
    #Creo y compilo el fragment shader
    fProgram = compileProgram(fSource, GL_FRAGMENT_SHADER)
    #Creo un programa de shading vacio en memoria de video
    shader = glCreateProgram()
    #Le adjunto el codigo objeto del vertex shader compilado
    glAttachShader(shader, vProgram)
    #Le adjunto el codigo objeto del fragment shader compilado
    glAttachShader(shader, fProgram)
    #Intento linkear el programa para generar un ejecutable en memoria de video
    glLinkProgram(shader)
    #Chequeo si la ejecucion del linkeo del programa fue exitosa
    if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
        #Si falla, imprimo el mensaje de error y libero los recursos
        print glGetProgramInfoLog(shader)
        glDeleteProgram(shader)
        return 0
    #Una vez que el programa fue linkeado, haya sido exitoso o no, ya no necesito los shaders
    #individuales compilados, asi que libero sus recursos
    glDeleteShader(vProgram)
    glDeleteShader(fProgram)

    return shader

def main():
    pygame.init()
    display = (900,900)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    model = Obj()
    model.parse("/home/sergio/Dropbox/py-cg/Shaders/box_normales.obj")

    #Creo un programa de shading y guardo la referencia en la variable gouraud
    gouraud = createShader("/home/sergio/Dropbox/py-cg/Shaders/shaders/gouraud_vs.hlsl",
                           "/home/sergio/Dropbox/py-cg/Shaders/shaders/gouraud_fs.hlsl")

    glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, [1,0,0,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, 16)

    glEnable(GL_LIGHT0)

    glLight(GL_LIGHT0, GL_DIFFUSE, [1,1,1,1])
    glLight(GL_LIGHT0, GL_AMBIENT, [0.1,0.1,0.1,1])
    glLight(GL_LIGHT0, GL_POSITION, [0,0,0,1])
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
                glDeleteProgram(gouraud)
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
                    light = not light
                    if(light):
                        #Con la tecla L habilito y deshabilito el shader
                        glUseProgram(gouraud)
                    else:
                        glUseProgram(0)

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    glDeleteProgram(gouraud)
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
        glEnableClientState(GL_NORMAL_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, model.vertices)
        glNormalPointer(GL_FLOAT, 0, model.normales)
        glColorPointer(3, GL_FLOAT, 0, model.colores)

        glDrawArrays(GL_TRIANGLES, 0, len(model.faces) * 3)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        pygame.display.flip()

main()