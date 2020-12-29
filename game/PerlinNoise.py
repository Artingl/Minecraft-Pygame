import random
import math
import threading


class PerlinNoise(threading.Thread):
    def __call__(self, x, y): return int(sum(self.noise(x * s, y * s) * h for s, h in self.perlins) * self.avg)

    def __init__(self, seed=10000, mh=0):
        super().__init__()
        self.m = 65536
        p = list(range(self.m))
        random.seed(seed)
        random.shuffle(p)
        self.p = p + p
        p = self.perlins = tuple((1 / i, i) for i in (16, 20, 22, 31, 32, 64, 512) for j in range(2))
        self.pp = p
        self.avg = mh * len(p) / sum(f + i for f, i in p)

    def updateAvg(self, mh):
        self.avg = mh * len(self.pp) / sum(f + i for f, i in self.pp)

    def fade(self, t): return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b): return a + t * (b - a)

    def grad(self, hash, x, y, z):
        h = hash & 15
        u = y if h & 8 else x
        v = (x if h == 12 or h == 14 else z) if h & 12 else y
        return (u if h & 1 else -u) + (v if h & 2 else -v)

    def noise(self, x, y, z=0):
        p, fade, lerp, grad = self.p, self.fade, self.lerp, self.grad
        xf, yf, zf = math.floor(x), math.floor(y), math.floor(z)
        X, Y, Z = xf % self.m, yf % self.m, zf % self.m
        x -= xf
        y -= yf
        z -= zf
        u, v, w = fade(x), fade(y), fade(z)
        A = p[X] + Y
        AA = p[A] + Z
        AB = p[A + 1] + Z
        B = p[X + 1] + Y
        BA = p[B] + Z
        BB = p[B + 1] + Z
        return lerp(w, lerp(v, lerp(u, grad(p[AA], x, y, z), grad(p[BA], x - 1, y, z)),
                            lerp(u, grad(p[AB], x, y - 1, z), grad(p[BB], x - 1, y - 1, z))),
                    lerp(v, lerp(u, grad(p[AA + 1], x, y, z - 1), grad(p[BA + 1], x - 1, y, z - 1)),
                         lerp(u, grad(p[AB + 1], x, y - 1, z - 1), grad(p[BB + 1], x - 1, y - 1, z - 1))))

