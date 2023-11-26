from random import randrange
from utils import gcd, inverse_mod, text_to_blocks, power_mod, generator, num_to_text


class RSA:
    def __init__(self, p, q):
        self.p = p
        self.q = q
        self.n = p * q
        self.phi = (p - 1) * (q - 1)
        self.change_key()

    def change_key(self):
        while True:
            self.e = randrange(65537, self.phi - 1, 2)
            if gcd(self.e, self.phi) == 1:
                break
        self.d = inverse_mod(self.e, self.phi)

    def public_key(self):
        return self.e

    def private_key(self):
        return self.d

    def encrypt(self, plain_text: str):
        blocks = text_to_blocks(plain_text, self.n)
        cipher = []
        for x in blocks:
            y = power_mod(x, self.e, self.n)
            cipher.append(y)
        return cipher

    def decrypt(self, cipher: list[int]):
        plain = []
        for y in cipher:
            x = power_mod(y, self.d, self.n)
            text = num_to_text(x)
            plain.append(text)
        return "".join(plain)

    def sign(self, message: str):
        blocks = text_to_blocks(message, self.n)
        signatures = []
        for x in blocks:
            y = power_mod(x, self.d, self.n)
            signatures.append(y)
        return signatures

    def verify(self, message: str, signatures: list[int]):
        blocks = text_to_blocks(message, self.n)
        for x, y in zip(blocks, signatures):
            if x != power_mod(y, self.e, self.n):
                return False
        return True


def run():
    BIT_LENGTH = 3072
    key = generator.generate_rsa_params(BIT_LENGTH)
    p = key.p
    q = key.q
    print(f"p = {p}")
    print(f"q = {q}")

    rsa = RSA(p, q)
    print(f"public key: e = {rsa.public_key()}")
    print(f"private key: d = {rsa.private_key()}")

    plain_text = open("./inputs/plaintext.txt", "r", encoding="utf-8").read()

    cipher = rsa.encrypt(plain_text)
    print(f"cipher: {cipher}")
    cipher_text = "".join([num_to_text(y) for y in cipher])
    try:
        print(f"cipher in text form: {cipher_text}")
    except:
        pass

    decrypted_text = rsa.decrypt(cipher)
    print(f"decrypted text: {decrypted_text}")
    print(f"decrypted text == plain text ?: {decrypted_text == plain_text}")

    signatures = rsa.sign(plain_text)
    print(f"signature: {signatures}")
    print(f"verification result: {rsa.verify(plain_text, signatures)}")


if __name__ == "__main__":
    run()
