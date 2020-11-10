from controller.openglController import (
    translate,
    rotate
)

class TrackBall():
    def __init__(self, foco=[0,0,0], elev=0, rot=0, dist=1):
        self.foco = [0,0,0]
        self.elev = 0
        self.rot = 0
        self.dist = 1

    def loadMatrix(self):
        translate(0,0,-self.dist)
        rotate(-self.elev, 1, 0 , 0)
        rotate(-self.rot, 0, 1, 0)
        translate(-self.foco[0], -self.foco[1], -self.foco[2])
