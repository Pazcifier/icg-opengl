from OpenGL.GL import *

class TrackBall():
    foco = [0,0,0]
    elev = 0
    rot = 0
    dist = 1

    def loadMatrix(self):
        glTranslatef(0,0,-self.dist)
        glRotate(-self.elev, 1, 0 , 0)
        glRotate(-self.rot, 0, 1, 0)
        glTranslatef(-self.foco[0], -self.foco[1], -self.foco[2])
