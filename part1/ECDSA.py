from utils.ellipticcurve import EllipticCurve, CurvePoint
from hashlib import sha3_224
from random import randint
from utils import inverse_mod


def changeHashFuncReturnType(h):
    """
    Hash functions in hashlib return hash objects.
    We will use this function to convert the hash object into int.
    """

    def intdigest(message: str):
        return int(h(message.encode("utf-8")).hexdigest(), 16)

    return intdigest


class EllipticCurveDigitalSignatureAlgorithm:
    def __init__(
        self,
        E: EllipticCurve,
        q: int,
        A: CurvePoint,
        h=changeHashFuncReturnType(sha3_224),
    ):
        """
        Create an Elliptic Curve Digital Signature Cryptosystem
        using elliptic curve E, a subgroup of order q of E with
        the generator A and the hash function.
        """
        self.E = E
        self.q = q
        self.A = A
        self.h = h
        self.change_key()

    def change_key(self):
        """
        Change the private key (and as a result, the public key).
        """
        self.m = randint(1, self.q - 1)

    def public_key(self):
        """
        Generate a public key for the crypto system
        consisting of two points A and B such that B = A * m
        where A is the given generator
        and m is the private key
        """
        B = self.A * self.m
        return (self.A, B)

    def private_key(self):
        """
        Generate a private key m for the crypto system
        such that m is the discrete logarithm of B to the base A
        where (A, B) is the public key
        """
        return self.m

    def sign(self, message: str, key: tuple[tuple[CurvePoint, CurvePoint], int]):
        """
        Sign a message using the given key consisting of a public key and private key pair.
        """
        if key == None:
            A = self.public_key()[0]
            m = self.private_key()
        else:
            A = key[0][0]
            m = key[1]
        x = self.h(message)
        while True:
            k = randint(1, self.q - 1)
            kA = A * k
            r = kA.x % self.q
            s = inverse_mod(k, self.q) * (x + m * r) % self.q
            if r != 0 and s != 0:
                break
        return (r, s)

    def verify(
        self,
        message: str,
        publicKey: tuple[CurvePoint, CurvePoint],
        signature: tuple[int, int],
    ):
        """
        Verify a signature of a message using the passed public key.
        Return True if the signature is valid, and False otherwise.
        """
        r, s = signature
        if r <= 0 or r >= self.q or s <= 0 or s >= self.q:
            return False
        A, B = publicKey
        w = inverse_mod(s, self.q)
        i = w * self.h(message) % self.q
        j = w * r % self.q
        u = (A * i + B * j).x
        return u % self.q == r
