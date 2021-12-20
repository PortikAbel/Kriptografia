#!/usr/bin/env python3 -tt
"""
File: crypto.py
---------------
Assignment 1: Cryptography
Course: CS 41
Name: <YOUR NAME>
SUNet: <SUNet ID>

Replace this with a description of the program.
"""

import re
from queue import PriorityQueue

from utils import coprime, byte_to_bits, bits_to_byte, modinv
import random as rand
import frequentwords as fw

# Caesar Cipher

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


# Vigenere Cipher

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


# Merkle-Hellman Knapsack Cryptosystem

def generate_private_key(n=8):
    """Generate a private key for use in the Merkle-Hellman Knapsack Cryptosystem.

    Following the instructions in the handout, construct the private key components
    of the MH Cryptosystem. This consistutes 3 tasks:

    1. Build a superincreasing sequence `w` of length n
        (Note: you can check if a sequence is superincreasing with `utils.is_superincreasing(seq)`)
    2. Choose some integer `q` greater than the sum of all elements in `w`
    3. Discover an integer `r` between 2 and q that is coprime to `q` (you can use utils.coprime)

    You'll need to use the random module for this function, which has been imported already

    Somehow, you'll have to return all of these values out of this function! Can we do that in Python?!

    @param n bitsize of message to send (default 8)
    @type n int

    @return 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.
    """
    w = []
    q = rand.randint(2, 10)
    total = 0
    for _ in range(n):
        w.append(q)
        total += q
        q = rand.randint(total + 1, 2 * total)
    w = tuple(w)

    r = rand.randint(2, q-1)
    while not coprime(q, r):
        r = rand.randint(2, q-1)
    
    return (w, q, r)

def create_public_key(private_key):
    """Create a public key corresponding to the given private key.

    To accomplish this, you only need to build and return `beta` as described in the handout.

        beta = (b_1, b_2, ..., b_n) where b_i = r × w_i mod q

    Hint: this can be written in one line using a list comprehension

    @param private_key The private key
    @type private_key 3-tuple `(w, q, r)`, with `w` a n-tuple, and q and r ints.

    @return n-tuple public key
    """
    return tuple([private_key[2] * w_i % private_key[1] for w_i in private_key[0]])


def encrypt_mh(message, public_key):
    """Encrypt an outgoing message using a public key.

    1. Separate the message into chunks the size of the public key (in our case, fixed at 8)
    2. For each byte, determine the 8 bits (the `a_i`s) using `utils.byte_to_bits`
    3. Encrypt the 8 message bits by computing
         c = sum of a_i * b_i for i = 1 to n
    4. Return a list of the encrypted ciphertexts for each chunk in the message

    Hint: think about using `zip` at some point

    @param message The message to be encrypted
    @type message bytes
    @param public_key The public key of the desired recipient
    @type public_key n-tuple of ints

    @return list of ints representing encrypted bytes
    """
    return bytes(sum([a_i * b_i for (a_i, b_i) in zip(byte_to_bits(byte), public_key)]) for byte in message)

def decrypt_mh(message, private_key):
    """Decrypt an incoming message using a private key

    1. Extract w, q, and r from the private key
    2. Compute s, the modular inverse of r mod q, using the
        Extended Euclidean algorithm (implemented at `utils.modinv(r, q)`)
    3. For each byte-sized chunk, compute
         c' = cs (mod q)
    4. Solve the superincreasing subset sum using c' and w to recover the original byte
    5. Reconsitite the encrypted bytes to get the original message back

    @param message Encrypted message chunks
    @type message list of ints
    @param private_key The private key of the recipient
    @type private_key 3-tuple of w, q, and r

    @return bytearray or str of decrypted characters
    """
    w, q, r = private_key
    s = modinv(r, q)
    plain = []
    for c in message:
        c_ = c * s % q
        bits = []
        for w_i in reversed(w):
            if w_i < c_:
                bits.append(1)
                c -= w_i
            else:
                bits.append(0)
        plain.append(bits_to_byte(bits))
    return bytes(plain)

# Scytale Cipher

def encrypt_scytale(plaintext: str, circumference: int) -> str:
    """Encrypt plaintext using a Scytale cipher with a circumference number.
    
    We make character sequences by selecting every 'circumference'th character
    starting from 1st, 2nd, ... characters and append these sequences

    @param plaintext text to be encrypted
    @type plaintext string
    @param circumference the number of rows used at the scytale
    @type circumference positive integer

    @return encrypted string
    """
    
    ciphertext = ''
    for i in range(circumference):
        ciphertext += ''.join(plaintext[i::circumference])
    return ciphertext

def decrypt_scytale(ciphertext: str, circumference: int) -> str:
    """Decrypt ciphertext using a Scytale cipher with a circumference number.
    
    1. Check if the length of the ciphertext is a perfect multiple of the circumference
    2. If yes, the decription is simmilar to encription
    2. Else we divide the cypher text into two parts based on the length of rows in the encripting method
        - whole rows
        - truncated rows
    3. We sort out the characters from the two parts alternatively

    @param ciphertext text to be decrypted
    @type ciphertext string
    @param circumference the number of rows used at the scytale
    @type circumference positive integer

    @return decrypted string
    """
    plaintext = ''
    length = len(ciphertext)
    whole_seq_nr = length // circumference

    if length % circumference == 0:
        for i in range(whole_seq_nr):
            plaintext += ''.join(ciphertext[i::whole_seq_nr])
    else:
        whole_row_nr = length - whole_seq_nr * circumference
        seq_nr = whole_seq_nr + 1
        whole_rows = ciphertext[:seq_nr*whole_row_nr]
        trunc_rows = ciphertext[seq_nr*whole_row_nr:]
        for i in range(whole_seq_nr):
            plaintext += ''.join(whole_rows[i::seq_nr])
            plaintext += ''.join(trunc_rows[i::whole_seq_nr])
        plaintext += ''.join(whole_rows[whole_seq_nr::seq_nr])

    return plaintext

# Railfence Cipher

def encrypt_railfence(plaintext: str, nr_rails: int, binary: bool) -> str:
    """Encrypt plaintext using a Railfence cipher with a rail number.

    @param plaintext text to be encrypted
    @type plaintext string
    @param nr_rails the number of rails used at the railfence
    @type nr_rails positive integer

    @return encrypted string
    """
    low_rail_index = nr_rails - 1
    step = 2*(low_rail_index)

    ciphertext = plaintext[::step]
    for rail_i in range(1, low_rail_index):
        odd_chars = plaintext[rail_i::step]
        even_chars = plaintext[step-rail_i::step]
        merged_chars = [None]*(len(odd_chars)+len(even_chars))
        merged_chars[0::2] = odd_chars
        merged_chars[1::2] = even_chars
        ciphertext += (bytes(merged_chars) if binary else ''.join(merged_chars))
    ciphertext += plaintext[low_rail_index::step]

    return ciphertext

def decrypt_railfence(ciphertext: str, nr_rails: int, binary: bool) -> str:
    """Decrypt ciphertext using a Railfence cipher with a rail number.

    @param ciphertext text to be decrypted
    @type ciphertext string
    @param nr_rails the number of rails used at the railfence
    @type nr_rails positive integer

    @return decrypted string
    """
    length = len(ciphertext)
    segment_length = nr_rails - 1
    step = 2 * segment_length
    segment_nr = length // segment_length
    back_n_forth_segment_nr = segment_nr // 2
    truncated_segment_length = length % (segment_length * 2)

    plaintext = [None]*length

    processed_length = back_n_forth_segment_nr
    if truncated_segment_length > 0:
        processed_length += 1
    plaintext[::step] = ciphertext[:processed_length]

    for rail_i in range(1, segment_length):
        if truncated_segment_length <= rail_i:
            rail_length = 2 * back_n_forth_segment_nr
        elif truncated_segment_length <= 2 * segment_length - rail_i:
            rail_length = 2 * back_n_forth_segment_nr + 1
        else:
            rail_length = 2 * back_n_forth_segment_nr + 2
        rail = ciphertext[processed_length:processed_length+rail_length]
        processed_length += rail_length

        odd_chars = rail[0::2]
        even_chars = rail[1::2]
        plaintext[rail_i::step] = odd_chars
        plaintext[step-rail_i::step] = even_chars

    plaintext[segment_length::step] = ciphertext[processed_length:]

    return bytes(plaintext) if binary else ''.join(plaintext)


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