from utils import generator
from ElGamal import ElGamal
import argparse
from utils import BASE_UCS4, text_to_num
from math import floor, log

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="Run El Gamal with options.")

# Add arguments to the parser
parser.add_argument(
    "--load",
    type=int,
    default=True,
    help="Choose either to load precalculated parameters or to calculate new parameters for El Gamal. Input 1 to load precalculated params or 0 to calculate new params.",
)

# Parse the command line arguments
args = parser.parse_args()

if args.load == 1:
    with open("./inputs/elgamal.txt", "r") as file:
        p = int(file.readline().strip())
        g = int(file.readline().strip())
else:
    BIT_LENGTH = 1024
    key = generator.generate_elgamal_params(BIT_LENGTH)
    p = int(key.p)
    g = int(key.g)

plain_text = open("./inputs/plaintext.txt", "r", encoding="utf-8").read()
textblocks = []
numblocks = []
block_length = floor(log(p, BASE_UCS4))
for i in range(0, len(plain_text), block_length):
    block = plain_text[i : i + block_length]
    textblocks.append(block)
    x = text_to_num(block, BASE_UCS4)
    numblocks.append(x)
print(textblocks)
print(numblocks)


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
