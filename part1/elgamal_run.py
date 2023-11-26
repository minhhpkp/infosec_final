from utils import generator, num_to_text
from ElGamal import ElGamal
import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Run El Gamal with options.")

# Add arguments to the parser
parser.add_argument(
    "--load",
    type=bool,
    default=1,
    help="Choose either to load precalculated parameters or to calculate new parameters for El Gamal. Input 1 to load precalculated params or 0 to calculate new params.",
)

# Parse the command line arguments
args = parser.parse_args()

plain_text = open("./inputs/plaintext.txt", "r", encoding="utf-8").read()
if args.load:
    with open("./inputs/elgamal.txt", "r") as file:
        p = int(file.readline().strip())
        g = int(file.readline().strip())
else:
    BIT_LENGTH = 512
    key = generator.generate_elgamal_params(BIT_LENGTH)
    p = int(key.p)
    g = int(key.g)

print(f"modulus: p = {p}")
print(f"generator: g = {g}")

elgamal = ElGamal(p, g)

print(f"public key: beta = {elgamal.public_key()}")
print(f"private key: a = {elgamal.private_key()}")

cipher = elgamal.encrypt(plain_text)
y1, y2 = cipher
print(f"cipher: y1 = {y1}, y2 = {y2}")

decrypted_text = elgamal.decrypt(cipher)
print(f"decrypted_text: {decrypted_text}")

print(f"plain_text == decrypted_text ?: {plain_text == decrypted_text}")


signature = elgamal.sign(plain_text)
print(f"signature: {signature}")
print(f"verification result: {elgamal.verify(plain_text, signature)}")
