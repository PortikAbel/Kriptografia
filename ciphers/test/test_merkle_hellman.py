from unittest import TestCase
from src.util.crypto.merkle_hellman import *
from math import gcd

class MerkleHellmanTest(TestCase):
  def setUp(self):
    self.n = 3

  def test_generate_private_key(self):
    private_key = generate_private_key(self.n)
    self.assertEqual(len(private_key), 3)
    w, q, r = private_key
    self.assertIsInstance(w, tuple)
    self.assertEqual(len(w), self.n)
    # is superincreasing
    sum = 0
    for w_i in w:
      self.assertGreater(w_i, sum)
      sum += w_i
    
    self.assertGreater(q, sum)
    self.assertEqual(gcd(q, r), 1)

  def test_create_public_key(self):
    private_key = generate_private_key()
    w, q, r = private_key
    public_key = create_public_key(private_key)
    self.assertIsInstance(public_key, tuple)
    self.assertEqual(len(w), len(public_key))
    for (w_i, b_i) in zip(w, public_key):
      self.assertEqual(b_i, (r * w_i) % q)

  def test_mh_crypting(self):
    private_key = generate_private_key()
    public_key = create_public_key(private_key)
    p = "message".encode()
    c = encrypt_mh(p, public_key)
    self.assertEqual(p, decrypt_mh(c, private_key))