from generators.PseudoRandomGenerator import PseudoRandomGenerator
from generators.Solitaire import Solitaire
from generators.BlumBlumShub import BlumBlumShub

class Config:
  def __init__(self) -> None:
    with open('config/gen.type') as type_input:
      generator_type = type_input.readline().strip()
      if generator_type == 'solitaire':
        with open('config/solitaire.seed') as seed_input:
          seed = list(map(int, seed_input.readline().split()))
          self.generator = Solitaire(seed)
      elif generator_type == 'bbs':
        with open('config/bbs.seed') as seed_input:
          seed = int(seed_input.readline().strip())
          self.generator = BlumBlumShub(seed)
      else:
        raise NotImplementedError

  def get_generator(self) -> PseudoRandomGenerator:
    return self.generator