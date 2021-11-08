from generators.PseudoRandomGenerator import PseudoRandomGenerator

class Solitaire(PseudoRandomGenerator):
  def __init__(self, seed: list[int]) -> None:
    self.pack = seed.copy()

  def gen(self, n: int) -> bytes:
    seq = []
    pack_size = len(self.pack)
    while len(seq) < n:
      # a)
      w_joker = self.pack.index(53)
      if w_joker == pack_size - 1:
        self.pack[1], self.pack[2:] = self.pack[w_joker], self.pack[1:w_joker]
        w_joker = 1
      else:
        self.pack[w_joker+1], self.pack[w_joker] = self.pack[w_joker], self.pack[w_joker+1]
        w_joker += 1
      # b)
      b_joker = self.pack.index(54)
      if b_joker == pack_size - 2:
        self.pack[1], self.pack[2:] = self.pack[b_joker], self.pack[1:b_joker] + self.pack[b_joker:]
        b_joker = 1
      elif b_joker == pack_size - 1:
        self.pack[2], self.pack[3:] = self.pack[b_joker], self.pack[2:b_joker]
        b_joker = 2
      else:
        self.pack[b_joker+2], self.pack[b_joker:b_joker+2] = self.pack[b_joker], self.pack[b_joker+1:b_joker+3]
        b_joker += 2
      # c)
      joker_1, joker_2 = min(w_joker, b_joker), max(w_joker, b_joker)
      self.pack = self.pack[joker_2+1:] + self.pack[joker_1:joker_2+1] + self.pack[:joker_1]
      # d)
      cards_to_count = min(self.pack[-1], 53)
      self.pack[:-1] = self.pack[cards_to_count:-1] + self.pack[:cards_to_count]
      # e)
      if self.pack[0] < 53:
        seq.append(self.pack[self.pack[0]])
    return bytes(seq)