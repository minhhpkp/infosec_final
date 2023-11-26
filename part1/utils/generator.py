from Cryptodome.PublicKey import ElGamal, RSA
from Cryptodome.Random import get_random_bytes


def generate_elgamal_params(bits):
    """
    Generate a prime number p of bit length bits and
    a generator g of G(Z_p*, .)
    """
    return ElGamal.generate(bits, get_random_bytes)


def generate_rsa_params(bits):
    """
    Generate two prime number p, q of bit length bits / 2
    and a number n of bit length bits
    """
    return RSA.generate(bits)
