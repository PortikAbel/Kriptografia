from queue import PriorityQueue
import re
import frequentwords as fw

def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """Encrypt plaintext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    k = len(keyword)
    i = 0
    ciphertext = ''
    a, A = ord('a'), ord('A')
    keyword = keyword.upper()
    for c in plaintext:
        if c.islower():
            ciphertext += chr((ord(c) + ord(keyword[i]) - a - A) % 26 + a)
            i = (i + 1) % k
        elif c.isupper():
            ciphertext += chr((ord(c) + ord(keyword[i]) - 2 * A) % 26 + A)
            i = (i + 1) % k
        else:
            ciphertext += c
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: int) -> str:
    """Decrypt ciphertext using a Vigenere cipher with a keyword.

    Add more implementation details here.
    """
    k = len(keyword)
    i = 0
    plaintext = ''
    a, A = ord('a'), ord('A')
    keyword = keyword.upper()
    for c in ciphertext:
        if c.islower():
            plaintext += chr((ord(c) - a - ord(keyword[i]) + A) % 26 + a)
            i = (i + 1) % k
        elif c.isupper():
            plaintext += chr((ord(c) - ord(keyword[i])) % 26 + A)
            i = (i + 1) % k
        else:
            plaintext += c
    return plaintext


def _count_frequent_words(text: str) -> int:
    count = 0
    for word in re.split('\W+', text):
        if fw.is_frequent_word(word):
            count += 1
    return count

def break_vigenere(ciphertext: str, possible_keys: list[str]) -> str:
    pqueue = PriorityQueue()
    for key in possible_keys:
        plaintext = decrypt_vigenere(ciphertext, key)
        pqueue.put((-_count_frequent_words(plaintext), key))
    _, potential_key = pqueue.get()
    return decrypt_vigenere(ciphertext, potential_key)