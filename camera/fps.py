from OpenGL.GL import *
import math

class FPS():
    pos = [0,0,0]
    elev = 0
    rot = 0

    def loadMatrix(self):
        glRotatef(-self.elev, 1, 0, 0)
        glRotatef(-self.rot, 0, 1, 0)
        glTranslatef(-self.pos[0], -self.pos[1], -self.pos[2])

    def walk(self, dist):
        x = math.sin(self.rot * math.pi/180) * dist
        z = math.cos(self.rot * math.pi/180) * dist

        self.pos[0] -= x
        self.pos[2] -= z