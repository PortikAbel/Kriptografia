import sys
from socket import socket, AF_INET, SOCK_STREAM
import json
from util.Cipher import Cipher
from config.config import Config


HOST = 'localhost'
PORT = 4242
SIZE = 1024

offset = 0


def initialize_connection():
  sock = socket(AF_INET, SOCK_STREAM)
  sock.bind((HOST, PORT))
  # print('Client listening on port {} for connection'.format(PORT))
  sock.listen(1)

  while True:
    connection, _ = sock.accept()
    try:
      # print('Sending initial message')
      connection.sendall(json.dumps({
        'status': 'init',
      }).encode())
      data = json.loads(connection.recv(SIZE).decode())
      # print('Received data: {}'.format(data))
      if 'status' in data and data['status'] == 'connected':
        return connection
    except Exception:
      print('Exception while connecting. Waiting for another connection')


def connect():
  sock = socket(AF_INET, SOCK_STREAM)
  # print('Client connecting to port {}'.format(PORT))
  sock.connect((HOST, PORT))

  try:
    data = json.loads(sock.recv(SIZE).decode())
    # print('Received data: {}'.format(data))
    if 'status' in data and data['status'] == 'init':
      sock.sendall(json.dumps({'status': 'connected'}).encode())
      return sock
    print('Could not connect')
    exit()
  except Exception:
    print('Could not connect')
    exit()


def initialize_cipher():
  conf = Config()
  return Cipher(conf.get_generator())


def send_message(connection: socket, cipher: Cipher) -> int:
  plain_text = input('Enter your message:\n')
  if plain_text == '':
    print('Leaving')
    connection.sendall(json.dumps({'status': 'exit'}).encode())
    connection.close()
    exit()
  connection.sendall(
    json.dumps({
      'offset': cipher.get_offset(),
      'cipher_text': list(cipher.encrypt(bytes(plain_text, 'ascii')))
    }).encode()
  )
  return len(plain_text)


def receive_message(connection: socket, cipher: Cipher) -> str:
  data = json.loads(connection.recv(SIZE).decode())
  if 'status' in data and data['status'] == 'exit':
    print('Peer left the connection')
    connection.close()
    exit()
  if 'offset' not in data or 'cipher_text' not in data:
    return 'Invalid message received.'
  msg_offset = data['offset']
  cipher_text = data['cipher_text']
  return cipher.decrypt(bytes(cipher_text), msg_offset).decode()


if __name__ == '__main__':
  if len(sys.argv) <= 0:
    print('Missing argument.')
    print('Usage: {} {{1|2}}'.format(sys.argv[0]))
    exit()

  cipher = initialize_cipher()
  
  if len(sys.argv) <= 1 or sys.argv[1] == '1':
    connection = initialize_connection()
    if send_message(connection, cipher) < 0:
      connection.close()
  elif sys.argv[1] == '2':
    connection = connect()
  else:
    print('Incorrect argument.')
    print('Usage: {} {{1|2}}'.format(sys.argv[0]))
    exit()

  while True:
    msg = receive_message(connection, cipher)
    print('Peer messaged you:')
    print(msg)
    send_message(connection, cipher)