from Crypto.Cipher import DES
import socket
import sys
import pickle

def decrypt_message(cipher_text):
    key = b'abcdefgh'
    cipher = DES.new(key, DES.MODE_ECB)

    decrypted_text = b''

    for i in range(16):
        decrypted_block += cipher.decrypt(decrypted_text + cipher_text[i*8:i*8+8])
        print(f"Block {i+1}: {decrypted_text.decode()}")
        decrypted_text = decrypted_block

        print(f"Round {i+1}: {decrypted_text.hex()}")
    return decrypted_text.rstrip(b' ')

def main():
    host = '127.0.0.1'
    port = 12345

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        data = s.recv(4096)
        encrypted_text = pickle.loads(data)

        decrypted_text = decrypt_message(encrypted_text)
        print(f"Decrypted message: {decrypted_text.decode()}")
        s.close()

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()