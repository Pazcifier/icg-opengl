from controller.openglController import (
    translate,
    rotate
)
import math

class TrackBall():
    def __init__(self, foco=[0,0,0], elev=0, rot=0, dist=1):
        self.foco = foco
        self.elev = elev
        self.rot = rot
        self.dist = dist

    def loadMatrix(self):
        translate(0,self.dist,0)
        rotate(self.elev, 1, 0, 0)
        rotate(self.rot, 0, 0, 1)
        translate(-self.foco[0], -self.foco[1], -self.foco[2])

    def walk(self, dist):
        x = math.cos(math.radians(self.rot * math.pi/180)) * dist
        z = math.sin(math.radians(self.rot * math.pi/180)) * dist

        print("Posiciones de Camera", self.foco)
        print("X y Z de Camara", (x,z))

        self.foco[0] += x
        self.foco[2] += z