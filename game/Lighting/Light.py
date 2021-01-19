from functions import roundPos


def spiral(n):
    dx, dy = 1, 0
    x, y = 0, 0
    arr = {}
    numm = 0
    pls = 0
    for i in range(1, n**2+1):
        arr[x, y] = numm
        nx, ny = x+dx, y+dy
        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in arr:
            x, y = nx, ny
        else:
            dx, dy = -dy, dx
            x, y = x+dx, y+dy
            pls += 1
            if pls % 4 == 0:
                numm += 0.1
    return arr


class Light:
    def __init__(self, gl):
        self.gl = gl

        self.oldLightSources = []
        self.lightSources = []
        self.notDark = {}

        self.spiral = spiral(16)

    def addLightSource(self, x, y, z):
        self.lightSources.append([x, y, z])

    def update(self):
        if self.oldLightSources == self.lightSources:
            return
        self.oldLightSources = self.lightSources.copy()

        lightDist = 15
        lightVal = 1

        cpy = self.notDark.copy()
        for i in cpy.items():
            px, py, pz = roundPos(self.gl.player.position)
            x, y, z = i[0]
            mx, mn = (lightDist // 2), -(lightDist // 2)

            if x not in range(px - mn, px + mx) and \
                    y not in range(py - mn, py + mx) and \
                    z not in range(pz - mn, pz + mx) and \
                    (x, y, z) in self.gl.cubes.cubes:
                self.gl.cubes.updateCube(self.gl.cubes.cubes[(x, y, z)], customColor={
                    'left': ('c3f', (0.1,) * 12),
                    'front': ('c3f', (0.1,) * 12),
                    'right': ('c3f', (0.1,) * 12),
                    'back': ('c3f', (0.1,) * 12),
                    'bottom': ('c3f', (0.1,) * 12),
                    'top': ('c3f', (0.1,) * 12),
                })
                self.notDark.pop(i[0])

        for i in self.lightSources:
            for xx in range(0, lightDist + 1):
                for yy in range(0, lightDist + 1):
                    for zz in range(0, lightDist + 1):
                        x = xx + i[0] - (lightDist // 2)
                        y = yy + i[1] - (lightDist // 2)
                        z = zz + i[2] - (lightDist // 2)

                        clr = self.spiral[xx, zz]
                        if clr < 0.1:
                            clr = 0.1

                        if roundPos((x, y, z)) in self.gl.cubes.cubes:
                            if clr != 0.1:
                                self.notDark[roundPos((x, y, z))] = clr

                            self.gl.cubes.updateCube(self.gl.cubes.cubes[roundPos((x, y, z))], customColor={
                                'left': ('c3f', (clr,) * 12),
                                'front': ('c3f', (clr,) * 12),
                                'right': ('c3f', (clr,) * 12),
                                'back': ('c3f', (clr,) * 12),
                                'bottom': ('c3f', (clr,) * 12),
                                'top': ('c3f', (clr,) * 12),
                            })
                lightVal -= 0.15
