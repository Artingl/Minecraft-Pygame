from OpenGL.GL import *


class Model:
    def __init__(self, gl):
        self.cubes = []
        self.gl = gl

    def addCube(self, x, y, z, w, h, d, texture):
        self.cubes.append((texture, x, y, z, w, h, d))

    def drawModel(self, pos, rot):
        for i in self.cubes:
            i = list(i)

            i[1] += pos[0]
            i[2] += pos[1]
            i[3] += pos[2]

            self.drawCube(*i)

    def drawCube(self, texture, x, y, z, w=1, h=1, d=1):
        X, Y, Z = x + w, y + h, z + d

        vertexes = [
            (X, y, z, x, y, z, x, Y, z, X, Y, z),
            (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z),
            (x, y, z, x, y, Z, x, Y, Z, x, Y, z),
            (X, y, Z, X, y, z, X, Y, z, X, Y, Z),
            (x, y, z, X, y, z, X, y, Z, x, y, Z),
            (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z),
        ]

        tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
        mode = GL_QUADS
        self.gl.stuffBatch.add(4, mode, texture[2], ('v3f', vertexes[0]),
                               tex_coords)  # back
        self.gl.stuffBatch.add(4, mode, texture[0], ('v3f', vertexes[1]),
                               tex_coords)  # front

        self.gl.stuffBatch.add(4, mode, texture[3], ('v3f', vertexes[2]),
                               tex_coords)  # left
        self.gl.stuffBatch.add(4, mode, texture[1], ('v3f', vertexes[3]),
                               tex_coords)  # right

        self.gl.stuffBatch.add(4, mode, texture[5], ('v3f', vertexes[4]),
                               tex_coords)  # bottom

        self.gl.stuffBatch.add(4, mode, texture[4], ('v3f', vertexes[5]),
                               tex_coords)  # top
