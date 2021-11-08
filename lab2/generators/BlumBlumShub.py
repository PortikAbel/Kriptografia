from generators.PseudoRandomGenerator import PseudoRandomGenerator

class BlumBlumShub(PseudoRandomGenerator):
  def __init__(self, seed: int) -> None:
    self.n = 11 * 23
    self.s = seed

  def gen(self, n: int) -> bytearray:
    x = []
    for _i in range(n):
      byte = 0
      for _j in range(8):
        byte = (byte << 1) | (self.s % 2)
        self.s = self.s**2 % self.n
      x.append(byte)
    return bytes(x)
