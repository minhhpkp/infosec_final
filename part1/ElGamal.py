from random import randint
from utils import power_mod, text_to_blocks, num_to_text, inverse_mod, gcd


class ElGamal:
    def __init__(self, p: int, g: int):
        """
        Create an El Gamal cryptosystem with prime modulus p
        and generator g.
        """
        self.p = p
        self.g = g
        self.change_key()

    def change_key(self):
        self.a = randint(1, self.p - 1)
        self.beta = power_mod(self.g, self.a, self.p)

    def public_key(self):
        return self.beta

    def private_key(self):
        return self.a

    def encrypt(self, plain_text: str):
        k = randint(0, self.p - 2)
        y1 = power_mod(self.g, k, self.p)

        blocks = text_to_blocks(plain_text, self.p)

        y2 = []
        for x in blocks:
            y2.append(x * power_mod(self.beta, k, self.p) % self.p)
        return (y1, y2)

    def decrypt(self, cipher: tuple[int, list[int]]):
        y1, y2 = cipher
        plain = []
        for y in y2:
            x = y * power_mod(y1, self.p - 1 - self.a, self.p) % self.p
            text = num_to_text(x)
            plain.append(text)
        return "".join(plain)

    def sign(self, message: str):
        while True:
            k = randint(1, self.p - 2)
            if gcd(k, self.p - 1) == 1:
                break
        gamma = power_mod(self.g, k, self.p)
        blocks = text_to_blocks(message, self.p)
        deltas = []
        for x in blocks:
            delta = (x - self.a * gamma) * inverse_mod(k, self.p - 1) % (self.p - 1)
            deltas.append(delta)
        return (gamma, deltas)

    def verify(self, message, signature: tuple[int, list[int]]):
        gamma, deltas = signature
        blocks = text_to_blocks(message, self.p)
        for x, delta in zip(blocks, deltas):
            to_check = (
                power_mod(self.beta, gamma, self.p)
                * power_mod(gamma, delta, self.p)
                % self.p
            )
            against = power_mod(self.g, x, self.p)
            if to_check != against:
                return False
        return True
