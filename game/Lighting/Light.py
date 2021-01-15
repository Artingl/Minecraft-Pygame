from functions import roundPos


class Light:
    def __init__(self, gl):
        self.gl = gl
        self.lightSources = []

        self.addLightSource(0, 60, 0)

    def addLightSource(self, x, y, z):
        self.lightSources.append([x, y, z])

    def update(self):
        lightDist = 15

        for i in self.lightSources:
            for xx in range(lightDist):
                for yy in range(lightDist):
                    for zz in range(lightDist):
                        x = xx + self.gl.player.position[0] - (lightDist / 2)
                        y = yy + self.gl.player.position[1] - (lightDist / 2)
                        z = zz + self.gl.player.position[2] - (lightDist / 2)
                        clr = (xx + yy + zz) / (lightDist * 3)

                        if roundPos((x, y, z)) in self.gl.cubes.cubes:
                            self.gl.cubes.updateCube(self.gl.cubes.cubes[roundPos((x, y, z))], customColor={
                                'left': ('c3f', (clr,) * 12),
                                'front': ('c3f', (clr,) * 12),
                                'right': ('c3f', (clr,) * 12),
                                'back': ('c3f', (clr,) * 12),
                                'bottom': ('c3f', (clr,) * 12),
                                'top': ('c3f', (clr,) * 12),
                            })
