import pygame
from pygame.locals import *

from controller.openglController import *
from controller.objController import ObjController
from controller.animController import AnimationController

# from camera.trackBall import TrackBall

# Notas del profesor:
# Crear una clase obj que nos permita usar de controlador para realizar cambios
# Reducir la mayor cantidad de llamadas GL del main
# No es necesario tener debug en la entrega final
# Mientras más cosas al final, mejor!!

# Siguiente pasos
# Rework de las cámaras para que sean referentes a un modelo

def main():
    light_angle = 0
    # Inicialización
    ## Pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    ## Parsers
    playerController = ObjController(True)
    planeController = ObjController(False, True)
    knightController = ObjController(False)
    boxController = ObjController(False)

    playerController.load_model("./assets/models/hueteotl_stand_0.obj")
    playerController.load_textures("./assets/textures/hueteotl")
    playerController.load_animations("./assets/animations/hueteotl")

    planeController.load_model("./assets/models/plane.obj")
    planeController.load_textures("./assets/textures/plane")

    knightController.load_model("./assets/models/knight_texturas.obj")
    knightController.load_textures("./assets/textures/knight")
    knightController.load_animations("./assets/animations/knight")

    boxController.load_model("./assets/models/box_texturas.obj")
    boxController.load_textures("./assets/textures/box")

    player = playerController.get_obj()
    plane = planeController.get_obj()
    knight = knightController.get_obj()
    box = boxController.get_obj()

    animationControllerPlayer = AnimationController(player)
    animationControllerKnight = AnimationController(knight)

    ## OpenGL
    set_background_color(0, 132, 250)
    ### Texturas
    enable(GL_TEXTURE_2D)

    ### Iluminación
    add_material([1,1,1,1], [1,1,1,1])
    set_shade_model(GL_SMOOTH)

    # enable(GL_LIGHT0)
    # add_light(GL_LIGHT0, [1,0,0,1], [1,1,1,1])

    # enable(GL_LIGHT1)
    # add_light(GL_LIGHT1, [0,0,1,1], [1,1,1,1])

    enable(GL_LIGHT0)
    add_light(GL_LIGHT0, [1,1,1,1], [1,1,1,1])

    enable(GL_LIGHT1)
    add_light(GL_LIGHT1, [1, 0, 0, 1], [1,0,0,1])

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
            playerController.controls(keys, event.type)

        ## Configuraciones
        set_matrix_mode(GL_MODELVIEW)

        identity()
        translate(0, 0, -30)
        rotate(-90, True, False, False)

        light_angle += 0.1
        configure_light_position(GL_LIGHT1, [light_angle, light_angle, light_angle])

        # playerController.get_camera().elev = angle

        clear(GL_COLOR_BUFFER_BIT)
        clear(GL_DEPTH_BUFFER_BIT)

        ## Activaciones
        enable_type(GL_VERTEX_ARRAY)
        enable_type(GL_NORMAL_ARRAY)
        enable_type(GL_TEXTURE_COORD_ARRAY)

        ## Animaciones
        if playerController.hasAnimations():
            player = animationControllerPlayer.play_animation(playerController.get__action())

        if knightController.hasAnimations():
            knight = animationControllerKnight.play_animation(0)

        ## Dibujado
        playerController.load_camera()
        translate(0, 0, -24)
        planeController.bind_texture(GL_TEXTURE0, "grass")
        drawArrays(plane)
        translate(0, 0, 24)

        translate(100, 0, 0)
        rotate(180, False, False, True)
        knightController.bind_texture(GL_TEXTURE0, "knight")
        drawArrays(knight)

        translate(0, 50, 0)
        knightController.bind_texture(GL_TEXTURE0, "knight_good")
        drawArrays(knight)

        translate(100, -50, 0)
        rotate(-180, False, False, True)
        playerController.load_character()
        playerController.bind_texture(GL_TEXTURE0, "hueteotl")
        drawArrays(player)

        # translate(10, 0, 0)

        # drawArrays(box2.get_obj())

        disable_type(GL_VERTEX_ARRAY)
        disable_type(GL_NORMAL_ARRAY)
        disable_type(GL_TEXTURE_COORD_ARRAY)

        pygame.display.flip()

main()