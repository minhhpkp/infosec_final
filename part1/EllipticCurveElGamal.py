from utils.ellipticcurve import EllipticCurve, CurvePoint
from random import randint
from math import log, floor
from typing import Callable
from utils import mod_sqrt, text_to_num, num_to_text, BASE_UCS4


class EllipticCurveElGamal:
    def __init__(
        self, E: EllipticCurve, n: int, P: CurvePoint, h: Callable[..., int] = hash
    ):
        """
        Initialize the Elliptic Curve ElGamal cryptosystem with an elliptic curve E
        and a hash function h. E has a subgroup that has prime order n and generator P.
        """
        self.E = E
        self.n = n
        self.P = P
        self.h = h
        self.change_key()

    def change_key(self):
        """
        Change the private key (and consequently, the public key).
        """
        self.m = randint(1, self.n - 1)

    def public_key(self) -> tuple[CurvePoint, CurvePoint]:
        """
        Generate a public key consisting of two points P, Q
        on the elliptic curve such that Q = m * P,
        where m is the private key.
        """
        Q = self.P * self.m
        return (self.P, Q)

    def private_key(self):
        """
        Return the private key m which is the discrete logarithm
        of Q to the base P, where (P, Q) is the public key.
        """
        return self.m

    def encrypt(self, publicKey: tuple[CurvePoint, CurvePoint], plain_text: str):
        """
        Encrypt the plain text using Cryptosystem 7.2 in section 7.5.6
        of the text book Cryptography: Theory and Practice
        """
        (P, Q) = publicKey
        # split plain_text into blocks
        cipher = []
        block_length = floor(log(self.E.p, BASE_UCS4))
        for i in range(0, len(plain_text), block_length):
            block = plain_text[i : i + block_length]
            x = text_to_num(block)

            k = randint(1, self.n - 1)
            kP_compressed = self._point_compress(P * k)
            kQ = Q * k
            hash_kQ = self.h((kQ.x, kQ.y))
            cipher.append((kP_compressed, (x + hash_kQ) % self.E.p))
        return cipher

    def decrypt(self, privateKey: int, cipher: list):
        """
        Decrypt the cipher using Cryptosystem 7.2 in section 7.5.6
        of the text book Cryptography: Theory and Practice
        """
        m = privateKey
        plain = []
        for y1, y2 in cipher:
            # y1 is kP_compressed and y2 is x + hash(kQ) mod p
            # therefore x = y2 - hash(R) mod p where R = m * decompress(y1)
            R = self._point_decompress(*y1) * m
            x = (y2 - self.h((R.x, R.y))) % self.E.p

            block = num_to_text(x)
            plain.append(block)
        plain_text = "".join(plain)
        return plain_text

    def _point_compress(self, P: CurvePoint):
        """
        Compress a point using Algorithm 7.5 in Section 7.5.6 of
        the text book Cryptography: Theory and Practice.
        """
        return (P.x, P.y % 2)

    def _point_decompress(self, x: int, i: int):
        """
        Decompress a point using Algorithm 7.5 in Section 7.5.6 of
        the text book Cryptography: Theory and Practice.
        """
        z = (x**3 + self.E.a * x + self.E.b) % self.E.p
        y = mod_sqrt(z, self.E.p)
        if y == None:
            return None
        if y % 2 == i:
            return CurvePoint(x, y, self.E)
        return CurvePoint(x, (-y) % self.E.p, self.E)
