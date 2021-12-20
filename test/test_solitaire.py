from unittest import TestCase
from collections import Counter
from src.generators.solitaire import Solitaire

class SolitaireTest(TestCase):
  def setUp(self):
    self.valid_seed = [*range(1, 55)]
    self.invalid_seed_1 = [1 for _ in range(54)]
    self.invalid_seed_2 = [1, 2, 3, 4]
    self.generator = Solitaire(self.valid_seed)

  def test_constructor(self):
    self.assertRaises(Exception, Solitaire.__init__, (self.invalid_seed_1))
    self.assertRaises(Exception, Solitaire.__init__, (self.invalid_seed_2))
    self.assertEqual(self.valid_seed, self.generator.seed)
    self.assertEqual(self.valid_seed, self.generator.initial_seed)

  def test_gen_half(self):
    self.generator.gen_half(5)
    self.assertNotEqual(self.generator.seed, self.generator.initial_seed)
    self.assertCountEqual(self.generator.seed, self.generator.initial_seed)

  def test_reset(self):
    self.generator.gen(12)
    self.assertNotEqual(self.generator.seed, self.generator.initial_seed)
    self.assertCountEqual(self.generator.seed, self.generator.initial_seed)
    self.generator.reset()
    self.assertEqual(self.generator.seed, self.generator.initial_seed)
