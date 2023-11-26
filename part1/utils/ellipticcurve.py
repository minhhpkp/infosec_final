from utils import inverse_mod, mod_sqrt
from random import randint


class EllipticCurve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a
        self.b = b
        self.INF = CurvePoint(None, None, self)

    def __eq__(self, other):
        if isinstance(other, EllipticCurve):
            return self.p == other.p and self.a == other.a and self.b == other.b
        return False

    def generate_random_point(self):
        while True:
            x = randint(0, self.p - 1)
            z = (x**3 + self.a * x + self.b) % self.p
            y = mod_sqrt(z, self.p)
            if y is not None:
                return CurvePoint(x, y, self)


class CurvePoint:
    def __init__(self, x, y, E: EllipticCurve):
        self.x = x
        self.y = y
        self.E = E

    def double(self):
        if self == self.E.INF:
            return self
        lmd = (
            (3 * self.x**2 + self.E.a) * inverse_mod(2 * self.y, self.E.p) % self.E.p
        )
        x = (lmd**2 - 2 * self.x) % self.E.p
        y = (lmd * (self.x - x) - self.y) % self.E.p
        return CurvePoint(x, y, self.E)

    def __add__(self, p):
        if not isinstance(p, CurvePoint):
            raise Exception("bad argument: not a point")
        if not p.E == self.E:
            raise Exception("bad argument: addition on points of different curves")

        if p == self.E.INF:
            return self
        if self == self.E.INF:
            return p
        if self == p:
            return self.double()
        if self.x == p.x and self.y != p.y:
            return self.E.INF

        lmd = (p.y - self.y) * inverse_mod(p.x - self.x, self.E.p) % self.E.p
        x = (lmd**2 - self.x - p.x) % self.E.p
        y = (lmd * (self.x - x) - self.y) % self.E.p
        return CurvePoint(x, y, self.E)

    def __eq__(self, other):
        if isinstance(other, CurvePoint):
            return self.x == other.x and self.y == other.y and self.E == other.E
        return False

    def __mul__(self, k: int):
        if k < 0:
            raise Exception(
                "bad argument: multiplication with negative integers not defined"
            )
        curSum = self.E.INF
        copy = CurvePoint(self.x, self.y, self.E)
        while k > 0:
            if k & 1:
                curSum += copy
            copy = copy.double()
            k >>= 1
        return curSum
    
    def __str__(self) -> str:
        return f"CurvePoint({self.x}, {self.y})"    


if __name__ == "__main__":
    E = EllipticCurve(11, 1, 6)
    p = CurvePoint(2, 7, E)
    q = CurvePoint(2, 7, E)
    d = p + q  # 5 2
    print(d.x, d.y)
    q = CurvePoint(2, -7, E)
    d = p + q  # None None
    print(d.x, d.y)
    q = q.E.INF
    d = p + q  # 2 7
    print(d.x, d.y)
    q = CurvePoint(7, 2, E)
    d = p + q  # 3 5
    print(d.x, d.y)
