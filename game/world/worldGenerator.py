import random

from game.world.PerlinNoise import PerlinNoise
from settings import *


class worldGenerator:
    def __init__(self, glClass, seed=43242):
        self.seed = seed
        self.chunks = {}
        self.worldPerlin = PerlinNoise(seed, mh=6)
        self.parent = glClass

    def add(self, p, t):
        self.parent.cubes.add(p, t, now=True)

    def genChunk(self, XX, YY, player):
        if player.hp == -1:
            player.hp = 20

        sx, sy, sz = CHUNK_SIZE
        xx, zz = XX * (sx - 1), YY * (sz - 1)

        for x in range(xx, xx + 1):
            for z in range(zz, zz + 1):
                sand = False
                y = self.worldPerlin(x, z) + sy
                if random.randint(0, 120) == 20 and y > sy - 5:
                    self.spawnTree(x, y, z)
                if y < sy - 15:
                    self.add((x, y, z), "sand")
                    sand = True
                else:
                    self.add((x, y, z), "grass")
                    if self.parent.startPlayerPos == [0, -90, 0]:
                        self.parent.startPlayerPos = [x, y + 2, z]
                self.add((x, 0, z), "bedrock")
                for i in range(1, y):
                    if i > y - random.randint(5, 10):
                        self.add((x, i, z), "sandstone" if sand else "dirt")
                    else:
                        self.add((x, i, z), "stone")
                    if i < sy - 20:
                        self.genOre(x, i, z)

    def genOre(self, x, y, z):
        if random.randint(0, 5753) != random.randint(0, 1575):
            return
        r1 = random.randint(1, 7)
        r2 = random.randint(r1, r1 + 7)
        ore = self.getOreByY(y)

        for xi in range(r1, r2):
            for yi in range(random.randint(2, 5)):
                for zi in range(random.randint(2, 5)):
                    self.add((x + xi, yi + y, zi + z), ore)

    def getOreByY(self, y):
        if y < 20:
            if random.randint(0, 150) > 54:
                return "diamond_ore"
            if random.randint(0, 1000) > 54:
                return "emerald_ore"
            if random.randint(0, 180) < 54:
                return "redstone_ore"
        elif y < 40:
            if random.randint(0, 180) == 54:
                return "gold_ore"
        if random.randint(0, 100) < 54:
            return "iron_ore"
        if random.randint(0, 80) < 54:
            return "coal_ore"
        if random.randint(0, 180) == 54:
            return "dirt"
        if random.randint(0, 180) == 54:
            return "gravel"
        return "dirt"

    def spawnTree(self, x, y, z):
        treeHeight = random.randint(5, 7)

        for i in range(y, y + treeHeight):
            self.add((x, i, z), 'log_oak')
        for i in range(x + -2, x + 3):
            for j in range(z + -2, z + 3):
                for k in range(y + treeHeight - 2, y + treeHeight):
                    self.add((i, k, j), 'leaves_oak')
        for i in range(treeHeight, treeHeight + 1):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    self.add((x + j, y + i, z + k), 'leaves_oak')
        cl = 2
        for i in range(treeHeight + 1, treeHeight + 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if cl % 2 != 0:
                        self.add((x + j, y + i, z + k), 'leaves_oak')
                    cl += 1
        self.add((x, y + treeHeight + 1, z), 'leaves_oak')
