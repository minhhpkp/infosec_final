from math import floor, log


def power_mod(a, b, m):
    curprod = 1
    while b > 0:
        if b & 1 == 1:
            curprod = curprod * a % m
        a = a * a % m
        b >>= 1
    return curprod


def extended_euclid(a, b):
    x = 1
    y = 0
    x1 = 0
    y1 = 1
    while b > 0:
        q = a // b
        x, x1 = x1, x - q * x1
        y, y1 = y1, y - q * y1
        a, b = b, a - q * b
    return a, x, y


# calculate a^-1 mod m
def inverse_mod(a, m):
    return extended_euclid(a, m)[1] % m


BASE_UCS4 = 0x10FFFF + 1


def text_to_num(text, base=BASE_UCS4, basech=chr(0)):
    """
    Convert a text to a number in the numerical system of given base
    """
    n = 0
    for ch in text:
        digit = ord(ch) - ord(basech)
        n = n * base + digit
    return n


def num_to_text(num, base=BASE_UCS4, basech=chr(0)):
    """
    Convert a number in a given base to a text.
    """
    chlist = []
    while num > 0:
        digit = num % base
        ch = chr(digit + ord(basech))
        chlist.append(ch)
        num //= base
    return "".join(reversed(chlist))


def text_to_blocks(text, p, base=BASE_UCS4, basech=chr(0)):
    """
    Split a text into blocks of length floor(log_{base}(p))
    then convert those blocks into numbers.
    """
    blocks = []
    block_length = floor(log(p, base))
    for i in range(0, len(text), block_length):
        block = text[i : i + block_length]
        x = text_to_num(block, base, basech)
        blocks.append(x)
    return blocks


def mod_sqrt(a, p):
    """
    Calculating square root of quadratic residue a
    modulo p. None is returned if a is non-residue.
    """
    def legendre_symbol(a1, p1):
        ls = pow(a1, (p1 - 1) // 2, p1)
        return -1 if ls == p1 - 1 else ls
    if legendre_symbol(a, p) != 1:
        return None
    elif a == 0:
        return None
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


def gcd(a, b):
    while b > 0:
        r = a % b
        a = b
        b = r
    return a


def curve_to_string(p, a, b, n):
    plusax = "" if a == 0 else f" + {a}*x"
    plusb = "" if b == 0 else f" + {b}"
    return f"Elliptic Curve defined by y^2 = x^3{plusax}{plusb} of order {n} over Finite Field of size {p}."