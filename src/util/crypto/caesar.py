
def encrypt_caesar(plaintext: str, offset: int) -> str:
    """Encrypt plaintext using a Caesar cipher.

    Add more implementation details here.
    """
    ciphertext = ''
    a, A = ord('a'), ord('A')
    for c in plaintext:
        if c.islower():
            ciphertext += chr((ord(c) - a + offset) % 26 + a)
        elif c.isupper():
            ciphertext += chr((ord(c) - A + offset) % 26 + A)
        else:
            ciphertext += c
    return ciphertext


def decrypt_caesar(ciphertext: str, offset: int) -> str:
    """Decrypt a ciphertext using a Caesar cipher.

    Add more implementation details here.
    """
    plaintext = ''
    a, A = ord('a'), ord('A')
    for c in ciphertext:
        if c.islower():
            plaintext += chr((ord(c) - a - offset) % 26 + a)
        elif c.isupper():
            plaintext += chr((ord(c) - A - offset) % 26 + A)
        else:
            plaintext += c
    return plaintext
