from random import randint

from OpenGL.GL import *


class Clouds:
    def __init__(self, gl):
        self.gl = gl
        self.xz = 0

    def update(self):
        sx, sz = 1000, 1000

        x, y, z = -(sx / 2), 100, -(sz / 2) + self.xz
        X, Y, Z = x + sx, y, z + sz

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        self.gl.stuffBatch.add(4, GL_QUADS, self.gl.block["clouds"][0],
                               ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)), tex_coords)
        self.xz += 0.01
