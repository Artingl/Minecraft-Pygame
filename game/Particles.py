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
            self.particles.append([list(p), cubeClass, 0.2, [dx, dy, dz], .0001, direction])

    def drawParticles(self):
        if not self.particles:
            return

        for e, i in enumerate(self.particles):
            if i[2] <= 0:
                self.particles.pop(e)
                continue

            i[3][1] += i[4]

            if i[5] != "no":

                i[0][0] += i[3][0] / 50
                i[0][1] += i[3][1] / 50
                i[0][2] += i[3][2] / 50

                if i[5] == "down":
                    i[0][0] -= i[4]
                    i[0][1] -= i[4]
                    i[0][2] -= i[4]
                elif i[5] == "up":
                    i[0][0] += i[4]
                    i[0][1] += i[4]
                    i[0][2] += i[4]
                elif i[5] == "left":
                    i[0][0] += i[4]
                    i[0][2] += i[4]
                elif i[5] == "right":
                    i[0][0] -= i[4]
                    i[0][2] -= i[4]
            else:
                i[0][0] += i[3][0] / 50
                i[0][2] += i[3][2] / 50

            self.gl.particleBatch.add(24,
                                      GL_QUADS,
                                      i[1].t[1],
                                      ('v3f', flatten(cube_vertices((i[0][0], i[0][1], i[0][2]), i[2]))))

            i[2] -= 0.01
            self.particles[e] = i
