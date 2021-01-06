from OpenGL.GL import *

from functions import roundPos, cube_vertices, adjacent
from game.blocks.Cube import Cube


class CubeHandler:
    def __init__(self, batch, block, opaque, alpha_textures, gl):
        self.batch, self.block, self.alpha_textures, self.opaque = batch, block, alpha_textures, opaque
        self.cubes = {}
        self.transparent = gl.transparent
        self.gl = gl
        self.fluids = {}
        self.collidable = {}

    def hitTest(self, p, vec, dist=6):
        m = 8
        x, y, z = p
        dx, dy, dz = vec
        dx /= m
        dy /= m
        dz /= m
        prev = None
        for i in range(dist * m):
            key = roundPos((x, y, z))
            if key in self.cubes and key not in self.fluids:
                return key, prev
            prev = key
            x, y, z = x + dx, y + dy, z + dz
        return None, None

    def show(self, v, t, i):
        return self.opaque.add(4, GL_QUADS, t, ('v3f', v), ('t2f', (0, 0, 1, 0, 1, 1, 0, 1)))

    def updateCube(self, cube):
        shown = any(cube.shown.values())
        if shown:
            if (cube.name != 'water' and cube.name != 'lava') and cube.p not in self.collidable:
                self.collidable[cube.p] = cube
        else:
            if cube.p in self.collidable:
                del self.collidable[cube.p]
            return

        show = self.show
        v = cube_vertices(cube.p)
        f = 'left', 'right', 'bottom', 'top', 'back', 'front'
        for i in (0, 1, 2, 3, 4, 5):
            if cube.shown[f[i]] and not cube.faces[f[i]]:
                cube.faces[f[i]] = show(v[i], cube.t[i], i)

    def set_adj(self, cube, adj, state):
        x, y, z = cube.p
        X, Y, Z = adj
        d = X - x, Y - y, Z - z
        f = 'left', 'right', 'bottom', 'top', 'back', 'front'
        for i in (0, 1, 2):
            if d[i]:
                j = i + i
                a, b = [f[j + 1], f[j]][::d[i]]
                cube.shown[a] = state
                if not state and cube.faces[a]:
                    cube.faces[a].delete()
                    face = cube.faces[a]
                    cube.faces[a] = None

    def add(self, p, t, now=False):
        if p in self.cubes:
            return
        cube = self.cubes[p] = Cube(t, p, self.block[t],
                                    'alpha' if t in self.alpha_textures else 'blend' if (t == 'water' or t == "lava")
                                    else 'solid')

        for adj in adjacent(*cube.p):
            if adj not in self.cubes:
                self.set_adj(cube, adj, True)
            else:
                a, b = cube.type, self.cubes[adj].type
                if a == b and (a == 'solid' or b == 'blend'):
                    self.set_adj(self.cubes[adj], cube.p, False)
                elif a != 'blend' and b != 'solid':
                    self.set_adj(self.cubes[adj], cube.p, False)
                    self.set_adj(cube, adj, True)
                if now:
                    self.updateCube(self.cubes[adj])

        if now:
            self.updateCube(cube)

    def remove(self, p):
        if p not in self.cubes:
            return
        if self.cubes[p].name == "bedrock":
            return
        if p in self.fluids:
            self.fluids.pop(p)
        cube = self.cubes.pop(p)

        for side, face in cube.faces.items():
            if face:
                face.delete()
            cube.shown[side] = False
        self.updateCube(cube)

        for adj in adjacent(*cube.p):
            if adj in self.cubes:
                self.set_adj(self.cubes[adj], cube.p, True)
                self.updateCube(self.cubes[adj])
