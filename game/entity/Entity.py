from OpenGL.GL import *


class Entity:
    def __init__(self):
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]

        self.vertices = []

    def update(self):
        glBegin(GL_QUADS)

        for i in self.vertices:
            x, y, z = i
            x += self.position[0]
            y += self.position[1]
            z += self.position[2]

            glVertex3f(x, y, z)

        glEnd()
