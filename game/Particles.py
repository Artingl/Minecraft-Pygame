from random import choice
from OpenGL.GL import *
from functions import *


class Particles:
    def __init__(self, gl):
        self.particles = []
        self.gl = gl
        self.texture = pyglet.graphics.TextureGroup(pyglet.image.load("particles/particle.png").get_mipmapped_texture())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    def addParticle(self, p, cubeClass, direction=None, numbers=None, count=30):
        if numbers is None:
            numbers = range(-5, 5)

            if not direction:
                numbers = range(-5, 5)

        for i in range(count):
            dx, dy, dz = choice(numbers), choice(numbers), choice(numbers)
            ps = randint(4, 8) / 1000  # 0.005
            self.particles.append([list(p), cubeClass, randint(1, 4) / 10, [dx, dy, dz], .001, direction, 0.02, ps])

    def drawParticles(self):
        if not self.particles:
            return

        for e, i in enumerate(self.particles):
            if i[2] <= 0:
                self.particles.pop(e)
                continue

            if i[5] != "no":
                if i[5] == "down":
                    if roundPos((i[0][0], i[0][1], i[0][2])) not in self.gl.cubes.cubes:
                        i[0][1] += i[6]
                    else:
                        i[7] /= 2
                    i[0][0] += i[3][0] / 100
                    i[0][2] += i[3][2] / 100

                    i[6] -= i[7]
                elif i[5] == "up":
                    if roundPos((i[0][0], i[0][1], i[0][2])) not in self.gl.cubes.cubes:
                        i[0][1] += i[6]
                    else:
                        i[7] /= 2
                    i[0][0] += i[3][0] / 100
                    i[0][2] += i[3][2] / 100

                    i[6] += i[7]
                elif i[5] == "left":
                    if roundPos((i[0][0], i[0][1], i[0][2])) not in self.gl.cubes.cubes:
                        i[0][0] += i[6]
                        i[0][1] += i[3][1] / 100
                        i[0][2] += i[6]

                        i[6] -= i[7]
                elif i[5] == "right":
                    if roundPos((i[0][0], i[0][1], i[0][2])) not in self.gl.cubes.cubes:
                        i[0][0] += i[6]
                        i[0][1] += i[3][1] / 100
                        i[0][2] += i[6]

                        i[6] += i[7]
            else:
                i[0][0] += i[3][0] / 50
                i[0][2] += i[3][2] / 50

            # self.gl.stuffBatch.add(24,
            #                          GL_QUADS,
            #                          i[1].t[1],
            #                          ('v3f', flatten(cube_vertices((i[0][0], i[0][1], i[0][2]), i[2]))))
            x, y, z = tuple(i[0])
            X, Y, Z = x + i[2], y + i[2], z + i[2]

            tex_coords = ('t2f', (0, 0, 1, 0, 1, 1, 0, 1))
            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[4], ('v3f', (X, y, z, x, y, z, x, Y, z, X, Y, z)),
                                   tex_coords)  # back
            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[5], ('v3f', (x, y, Z, X, y, Z, X, Y, Z, x, Y, Z)),
                                   tex_coords)  # front

            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[0], ('v3f', (x, y, z, x, y, Z, x, Y, Z, x, Y, z)),
                                   tex_coords)  # left
            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[1], ('v3f', (X, y, Z, X, y, z, X, Y, z, X, Y, Z)),
                                   tex_coords)  # right

            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[2], ('v3f', (x, y, z, X, y, z, X, y, Z, x, y, Z)),
                                   tex_coords)  # bottom
            self.gl.stuffBatch.add(4, GL_QUADS, i[1].t[3], ('v3f', (x, Y, Z, X, Y, Z, X, Y, z, x, Y, z)),
                                   tex_coords)  # top

            i[2] -= 0.009
            self.particles[e] = i
