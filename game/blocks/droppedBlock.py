from random import randint
from OpenGL.GL import *
import numpy as np
import math
from functions import roundPos


class droppedBlock:
    def __init__(self, gl):
        self.gl = gl
        self.blocks = {}

    def addBlock(self, coords, name, dr=True):
        self.blocks[len(self.blocks)] = [coords, name, randint(0, 2) / 10, [0, "-"], 0, dr]

    def update(self):
        cpy = self.blocks.copy().items()
        for i in cpy:

            pp = list(self.gl.player.position)
            sx, sy, sz = 0.25, 0.25, 0.25

            x, y, z = 0, 0, 0
            X, Y, Z = x + sx, y + sy, z + sz
            kx, ky, kz = i[1][0][0] - i[1][2], i[1][0][1] + 0.1 + i[1][3][0], i[1][0][2] + i[1][2]

            br = False
            for xs in (1, 0, -1):
                for ys in (1, 0, -1, -2):
                    for zs in (1, 0, -1):
                        if roundPos((pp[0] + xs, pp[1] + ys, pp[2] + zs)) == roundPos((x + kx, y + ky, z + kz)) and \
                                self.gl.player.hp > 0:
                            self.blocks.pop(i[0])
                            self.gl.blockSound.playPickUpSound()
                            self.gl.player.inventory.addBlock(i[1][1])
                            br = True
                        if br:
                            break
                    if br:
                        break
                if br:
                    break
            if br:
                continue

            vertexes = [
                (X, y, z, x, y, z, x, Y, z, X, Y, z),
                (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z),
                (x, y, z, x, y, Z, x, Y, Z, x, Y, z),
                (X, y, Z, X, y, z, X, Y, z, X, Y, Z),
                (x, y, z, X, y, z, X, y, Z, x, y, Z),
                (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z),
            ]

            rot = np.array([
                [math.cos(i[1][4]), 0, -math.sin(i[1][4]), 0],
                [0, 1, 0, 0],
                [math.sin(i[1][4]), 0, math.cos(i[1][4]), 0],
                [0, 0, 0, 1]
            ])
            i[1][4] += 0.01

            for e, j in enumerate(vertexes):
                r1 = (
                         (j[0], j[1], j[2], 1), (j[3], j[4], j[5], 1), (j[6], j[7], j[8], 1),
                         (j[9], j[10], j[11], 1)) @ rot
                vertexes[e] = (r1[0][0] + kx, r1[0][1] + ky, r1[0][2] + kz, r1[1][0] + kx, r1[1][1] + ky,
                               r1[1][2] + kz, r1[2][0] + kx, r1[2][1] + ky, r1[2][2] + kz,
                               r1[3][0] + kx, r1[3][1] + ky, r1[3][2] + kz)

            block = self.gl.block[i[1][1]]
            tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
            self.gl.stuffBatch.add(4, GL_QUADS, block[4], ('v3f', vertexes[0]),
                                   tex_coords)  # back
            if i[1][5]:
                self.gl.stuffBatch.add(4, GL_QUADS, block[5], ('v3f', vertexes[1]),
                                       tex_coords)  # front

                self.gl.stuffBatch.add(4, GL_QUADS, block[0], ('v3f', vertexes[2]),
                                       tex_coords)  # left
                self.gl.stuffBatch.add(4, GL_QUADS, block[1], ('v3f', vertexes[3]),
                                       tex_coords)  # right

                self.gl.stuffBatch.add(4, GL_QUADS, block[2], ('v3f', vertexes[4]),
                                       tex_coords)  # bottom
                self.gl.stuffBatch.add(4, GL_QUADS, block[3], ('v3f', vertexes[5]),
                                       tex_coords)  # top

            if i[1][3][1] == "-":
                i[1][3][0] -= 0.003
            if i[1][3][1] == "+":
                i[1][3][0] += 0.003

            if i[1][3][0] < -0.1:
                i[1][3][1] = "+"
            if i[1][3][0] > 0.1:
                i[1][3][1] = "-"

            yy = i[1][0][1]
            if roundPos((i[1][0][0], i[1][0][1], i[1][0][2])) not in self.gl.cubes.cubes:
                yy -= 0.1
                if y < -2:
                    self.blocks.pop(i[0])
                    continue
            self.blocks[i[0]][0] = (i[1][0][0], yy, i[1][0][2])
            self.blocks[i[0]][4] = i[1][4]
