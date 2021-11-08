from generators.PseudoRandomGenerator import PseudoRandomGenerator

def crypting(message: bytearray, generator: PseudoRandomGenerator) -> bytearray:
  return bytes(a ^ b for (a, b) in zip(message, generator.gen(len(message))))