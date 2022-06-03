plaintext = "Hello, I am Alice. Can I borrow your laptop? - from Alice -"


def sxor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))


def encrypt(message):
    if type(message) is int:
        message = str(message)

    encrypted = ""
    for c in message:
        encrypted += chr(ord(c) + 1)
    return encrypted


def decrypt(message):
    if type(message) is int:
        message = str(message)

    decrypted = ""
    for c in message:
        decrypted += chr(ord(c) - 1)
    return decrypted


def split(message, size=8):
    return [message[i:i + size] for i in range(0, len(message), size)]


def ECB_encrypt(message):
    encrypted = []
    for block in split(message):
        encrypted.append(encrypt(block))
    return encrypted


def ECB_decrypt(blocks):
    decrypted = []
    for block in blocks:
        decrypted.append(decrypt(block))
    return decrypted


def CBC_encrypt(message):
    encrypted = ["INITVECT"]  # initial vector

    for i, block in enumerate(split(message)):
        encrypted.append(encrypt(sxor(block, encrypted[i])))
    return encrypted


def CBC_decrypt(blocks):
    decrypted = []
    for i, block in enumerate(blocks):
        if i == 0:  # initial vector
            continue
        decrypted.append(sxor(decrypt(block), blocks[i - 1]))
    return decrypted


def CFB_encrypt(message):
    encrypted = [encrypt("INITVECT")]
    for i, block in enumerate(split(message)):
        encrypted.append(sxor(block, encrypt(encrypted[i])))
    return encrypted


def CFB_decrypt(blocks):
    decrypted = []
    for i, block in enumerate(blocks):
        if i == 0:
            continue
        decrypted.append(sxor(block, encrypt(blocks[i - 1])))
    return decrypted


def OFB_encrypt(message):
    iv = encrypt("INITVECT")
    encrypted = [iv]
    for i, block in enumerate(split(message)):
        iv = encrypt(iv)
        encrypted.append(sxor(block, iv))
    return encrypted


def OFB_decrypt(blocks):
    iv = blocks.pop(0)
    decrypted = []
    for i, block in enumerate(blocks):
        iv = encrypt(iv)
        decrypted.append(sxor(block, iv))
    return decrypted


def CTR_encrypt(message):
    nonce = 13891000
    encrypted = [nonce]
    count = 0
    for i, block in enumerate(split(message)):
        encrypted.append(sxor(block, encrypt(nonce | count)))
        count += 1
    return encrypted


def CTR_decrypt(blocks):
    decrypted = []
    nonce = blocks.pop(0)
    count = 0
    for i, block in enumerate(blocks):
        decrypted.append(sxor(block, encrypt(nonce | count)))
        count += 1
    return decrypted


def CTR_test():
    message = "Hello, I am Alice. Can I borrow your laptop? - from Alice -"
    print("Message", message)
    encrypted = CTR_encrypt(message)
    print("Encrypted:", encrypted)
    decrypted = CTR_decrypt(encrypted)
    print("Decrypted:", decrypted)


def gcd(a, b):
    a, b = (a, b) if a > b else (b, a)
    return b if a % b == 0 else gcd(b, a - b)


def RSA_generateKey(p, q):
    N = p * q
    P = (p - 1) * (q - 1)
    e = 3
    while gcd(P, e) != 1:
        e += 1

    d = 17
    while e * d % P != 1:
        d += 1

    return (N, e), (N, d)


def RSA_encrypt(num, pubKey):
    return pow(num, pubKey[1]) % pubKey[0]


def RSA_decrypt(num, priKey):
    return pow(num, priKey[1]) % priKey[0]


def RSA_test():
    pubKey, priKey = RSA_generateKey(11, 37)
    message = 150
    print("Message:", message)
    encrypted = RSA_encrypt(message, pubKey)
    print("Encrypted:", encrypted)
    decrypted = RSA_decrypt(encrypted, priKey)
    print("Decrypted:", decrypted)


class Crypto:
    @classmethod
    def getInstance(cls, type):
        instance = Crypto()
        instance.mode = type
        if type == "ECB":
            instance.encrypt = ECB_encrypt
            instance.decrypt = ECB_decrypt
        elif type == "CBC":
            instance.encrypt = CBC_encrypt
            instance.decrypt = CBC_decrypt
        elif type == "CFB":
            instance.encrypt = CFB_encrypt
            instance.decrypt = CFB_decrypt
        elif type == "OFB":
            instance.encrypt = OFB_encrypt
            instance.decrypt = OFB_decrypt
        elif type == "CTR":
            instance.encrypt = CTR_encrypt
            instance.decrypt = CTR_decrypt
        return instance


test = [
    Crypto.getInstance("ECB"),
    Crypto.getInstance("CBC"),
    Crypto.getInstance("CFB"),
    Crypto.getInstance("OFB"),
    Crypto.getInstance("CTR")
]

for crypt in test:
    plaintext = "Hello, world! Hello, Python!"
    c = crypt.encrypt(plaintext)
    d = crypt.decrypt(c)
    print("MODE:", crypt.mode)
    print(c)
    print(d)
    print()
