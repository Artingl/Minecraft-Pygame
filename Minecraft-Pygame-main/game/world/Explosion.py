from random import randint


class Explosion:
    def __init__(self, gl, pos, fr, bc):
        self.gl, self.pos, self.fr, self.bc = gl, list(pos), fr, bc

    def run(self):
        self.gl.particles.addParticle(self.pos, self.bc, numbers=range(-15, 15), direction="down", count=100)
        self.gl.cubes.remove(tuple(self.pos))

        for x in range(-(self.fr // 2) + randint(-1, 1), self.fr // 2 + randint(-1, 1)):
            for y in range(-(self.fr // 2) + randint(-1, 1), self.fr // 2 + randint(-1, 1)):
                for z in range(-(self.fr // 2) + randint(-1, 1), self.fr // 2 + randint(-1, 1)):
                    nx, ny, nz = self.pos[0] + x, self.pos[1] + y, self.pos[2] + z

                    if (nx, ny, nz) in self.gl.cubes.cubes:
                        if self.gl.cubes.cubes[(nx, ny, nz)].name == "tnt":
                            nexp = Explosion(self.gl, (nx, ny, nz), self.fr, self.bc)
                            nexp.run()

                    self.gl.cubes.remove((nx, ny, nz))
