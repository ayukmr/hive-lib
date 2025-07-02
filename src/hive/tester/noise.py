import math
import random

class Noise:
    GRADIENTS = [
        (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0),
        (1.0, 1.0), (-1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)
    ]

    def __init__(self):
        perm = list(range(256))
        random.shuffle(perm)
        self.p = [perm[i % 256] for i in range(512)]

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        return a + t * (b - a)

    def grad(self, h, x, y):
        g = self.GRADIENTS[h & 7]
        return g[0] * x + g[1] * y

    def sample(self, x, y):
        xi = int(math.floor(x)) & 255
        yi = int(math.floor(y)) & 255
        xf = x - math.floor(x)
        yf = y - math.floor(y)

        u = self.fade(xf)
        v = self.fade(yf)

        aa = self.p[self.p[xi] + yi]
        ab = self.p[self.p[xi] + yi + 1]
        ba = self.p[self.p[xi + 1] + yi]
        bb = self.p[self.p[xi + 1] + yi + 1]

        x1 = self.lerp(u, self.grad(aa, xf, yf), self.grad(ba, xf - 1, yf))
        x2 = self.lerp(u, self.grad(ab, xf, yf - 1), self.grad(bb, xf - 1, yf - 1))

        return self.lerp(v, x1, x2) / 2 + 0.5
