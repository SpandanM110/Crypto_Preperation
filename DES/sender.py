from Crypto.Cipher import DES
import socket
import sys
import pickle

def pad_message(message):
    while len(message) % 8 != 0:
        message += b' '
    return message

def sender_side(message):
    key = b'abcdefgh'
    cipher = DES.new(key, DES.MODE_ECB)

    message = pad_message(message)
    encrypted_text = b''

    for i in range(16):
        encrypted_text += cipher.encrypt(encrypted_text+ message[i*8:i*8+8])
        print(f"Block {i+1}: {encrypted_text.hex()}")

    return encrypted_text

def main():
    host = '127.0.0.1'
    port = 12345

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()

        message = b'Hello, world!'
        encrypted_text = sender_side(message)

        data = pickle.dumps(encrypted_text)
        conn.sendall(data)

        conn.close()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
if __name__ == '__main__':
    main()