import pygame
from pygame.locals import *

# from OpenGL.GL import *
# from OpenGL.GLU import *

from os import listdir
from os.path import isfile, join

from handlers.objHandlerv4 import ObjHandler
from handlers.textureHandlerv3 import TextureHandler
from handlers.animationHandler import AnimationHandler

from controller.openglController import *
from controller.objController import ObjController

# Notas del profesor:
# Crear una clase obj que nos permita usar de controlador para realizar cambios
# Reducir la mayor cantidad de llamadas GL del main
# No es necesario tener debug en la entrega final
# Mientras más cosas al final, mejor!!

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
    frame = -1
    category = 0
    activeAnimation = False

    # Inicialización
    ## Pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    ## Parsers
    boxController = ObjController()

    boxController.load_model("./assets/models/box_texturas.obj")
    boxController.load_textures("./assets/textures/box")

    # boxController.bind_texture(GL_TEXTURE0, "box")

    box1 = boxController.get_obj()

    # boxController.bind_texture(GL_TEXTURE1, "box_old")

    box2 = boxController.get_obj()
    # playerController = ObjController()

    # playerController.load_model("./assets/models/hueteotl_stand_0.obj")
    # playerController.load_textures("./assets/textures/hueteotl")
    # playerController.load_animations("./assets/animations/hueteotl")

    # playerController.bind_texture(GL_TEXTURE0, "hueteotl")

    # player = playerController.get_obj()

    ## OpenGL
    set_background_color(0, 132, 250)
    ### Texturas
    enable(GL_TEXTURE_2D)

    ### Iluminación
    add_material([1,0,0,1], [1,1,1,1])
    enable(GL_LIGHT0)

    set_shade_model(GL_SMOOTH)

    add_light(GL_LIGHT0, [1,1,1,1], [1,1,1,1])
    enable(GL_LIGHTING)

    enable(GL_DEPTH_TEST)
    
    ### Viewport
    set_matrix_mode(GL_PROJECTION)
    set_viewport(display[0], display[1])
    configure_frustum(-1, 1, -1, 1, 1, 1000)

    # Main Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            keys = pygame.key.get_pressed()
            boxController.controls(keys, event.type)
        # Pasar eventos a ObjController
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         quit()
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_ESCAPE:
        #             pygame.quit()
        #             quit()
        #         if event.key == pygame.K_w:
        #             prof += 0.25
        #         if event.key == pygame.K_s:
        #             prof -= 0.25
        #         if event.key == pygame.K_k:
        #             texture = 0
        #             actual_texture = 0

        #             actual_obj += 1
        #             if (actual_obj >= len(keys)):
        #                 actual_obj = 0
        #             load_obj = obj_handler.get_obj(keys[actual_obj])
        #         if event.key == pygame.K_z:
        #             zEnable = not zEnable
        #             if zEnable:
        #                 glEnable(GL_CULL_FACE)
        #             else:
        #                 glDisable(GL_CULL_FACE)
        #         if event.key == pygame.K_c:
        #             clockW = not clockW
        #             if clockW:
        #                 glFrontFace(GL_CW)
        #             else:
        #                 glFrontFace(GL_CCW)
        #         if event.key == pygame.K_l:
        #             lineMode = not lineMode
        #             if lineMode:
        #                 glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        #             else:
        #                 glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        #         if event.key == pygame.K_t:
        #             glActiveTexture(GL_TEXTURE0)
        #             texture = texture_handler.bind_texture(box, actual_texture)
        #             glBindTexture(GL_TEXTURE_2D, texture)
        #             if (texture > 0):
        #                 actual_texture += 1
        #                 if (actual_texture >= box["TextureImage"]["Total"]):
        #                     actual_texture = 0
        #         if event.key == pygame.K_m:
        #             if (not activeAnimation):
        #                 obj_animations = box["Animations"]
        #                 all_categories = len(obj_animations["Keys"]) - 1
        #                 all_frames = obj_animations["Categories"][category]["Frames"]
        #                 max_frames = len(all_frames) - 1
        #                 load_obj_backup = box
        #                 activeAnimation = True

        ## Configuraciones
        set_matrix_mode(GL_MODELVIEW)

        identity()
        translate(0, 0, -5)
        scale(prof, prof, prof)
        rotate(-90, True, False, False)
        # rotate(angle, True, False, False)
        # angle += 0.1

        clear(GL_COLOR_BUFFER_BIT)
        clear(GL_DEPTH_BUFFER_BIT)

        ## Activaciones
        enable_type(GL_VERTEX_ARRAY)
        enable_type(GL_NORMAL_ARRAY)
        enable_type(GL_TEXTURE_COORD_ARRAY)

        ## Animaciones
        currentTime = pygame.time.get_ticks()
        deltaT += currentTime - lastTime
        lastTime = currentTime

        if boxController.hasAnimations():
            if (deltaT > 100):
                deltaT = 0
                frame_animation = boxController.play_frame(frame)
                frame = frame_animation[0]
                player = frame_animation[1]

        ## Dibujado
        boxController.bind_texture(GL_TEXTURE0, "box")
        drawArrays(box1)

        translate(0, 0, 2)

        boxController.bind_texture(GL_TEXTURE0, "box_old")
        drawArrays(box2)

        # drawArrays(box2.get_obj())

        disable_type(GL_VERTEX_ARRAY)
        disable_type(GL_NORMAL_ARRAY)
        disable_type(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()

main()