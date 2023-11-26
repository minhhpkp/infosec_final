import argparse

# Create an ArgumentParser object
parser = argparse.ArgumentParser(
    description="Run Elliptic Curve cryptography system with options."
)

# Add arguments to the parser
parser.add_argument(
    "--input",
    type=str,
    default="bn_elliptic_curve",
    help="Choose the input elliptic curve for loading into the system. Options are bn_elliptic_curve, cp_elliptic_curve, and dem_elliptic_curve.",
)

parser.add_argument(
    "--type",
    type=str,
    default="encryption",
    help="Choose the type of cryptography system. Options are encryption and signature.",
)

# Parse the command line arguments
args = parser.parse_args()

ecinput = "./inputs/" + args.input + ".txt"

with open(ecinput, "r") as file:
    # Prime Field characteristic
    p = int(file.readline().strip())
    # Curve coefficients
    a = int(file.readline().strip())
    b = int(file.readline().strip())
    # Prime Order of the elliptic curve (of 300 bit length)
    n = int(file.readline().strip())
    # plain text to be encrypted
plain_text = open("./inputs/plaintext.txt", "r", encoding="utf-8").read()

from utils import curve_to_string
print(curve_to_string(p, a, b, n))

from utils.ellipticcurve import EllipticCurve
if args.type == "encryption":    
    from EllipticCurveElGamal import EllipticCurveElGamal

    # define a elliptic curve E over prime field Zp, with coefficients a and b
    # E will have order n
    E = EllipticCurve(p, a, b)
    # define a elliptice curve elgamal cryptosystem
    ece = EllipticCurveElGamal(E, n, E.generate_random_point(), hash)

    # encrypt the plain text with the public key
    publicKey = ece.public_key()
    cipher = ece.encrypt(publicKey, plain_text)

    print(f"public key:\n  P = {publicKey[0]},\n  Q = P * m = {publicKey[1]}")    
    print(f"cipher:")
    for c in cipher:
        print(f"  kP compressed = {c[0]}\n  encrypted message = {c[1]}")

    # decrypt the cipher with the private key
    privateKey = ece.private_key()
    received_text = ece.decrypt(privateKey, cipher)
    print(f"private key: m = {privateKey}")
    print(f"decrypted text: {received_text}")

    print(f"decrypted text == plain text ?: {received_text == plain_text}")
else:    
    from ECDSA import EllipticCurveDigitalSignatureAlgorithm, changeHashFuncReturnType
    from hashlib import sha3_512
    # define a elliptic curve E over prime field Zp, with coefficients a and b
    # E will have order n
    E = EllipticCurve(p, a, b)
    # Since the curve we generated has a prime order, that is, n is prime
    # We can use the whole curve E as the subgroup for the ECDS cryptosystem
    ecdsa = EllipticCurveDigitalSignatureAlgorithm(
        E, n, E.generate_random_point(), changeHashFuncReturnType(sha3_512)
    )

    publicKey = ecdsa.public_key()
    privateKey = ecdsa.private_key()

    print(f"public key:\n  P = {publicKey[0]},\n  Q = P * m = {publicKey[1]}")
    print(f"private key: m = {privateKey}")

    # sign the message
    signature = ecdsa.sign(plain_text, (publicKey, privateKey))
    print(f"signature:\n  r = {signature[0]},\n  s = {signature[1]}")

    # verify the signature
    verificationResult = ecdsa.verify(plain_text, publicKey, signature)
    print(f"verification result: {verificationResult}")    

