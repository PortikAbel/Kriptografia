from config.config import Config
from config.config import Config
from util.cipher import Cipher

if __name__ == '__main__':
  config = Config()
  # 'hello' ecrypted with Solitaire
  # print(cipher.crypting(b'ni`zdNsuGM'))

  # 'hello' ecrypted with BBS
  # print(cipher.crypting(b'\x8dc\xa2<\x03'))
  
  cipher = Cipher(config.get_generator())
  print(cipher.crypting(b'hello', 0))