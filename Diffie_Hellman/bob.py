import socket
import random
import secrets

P = 225
G = 14

def sender():
    HOST = 'localhost'
    PORT = 4000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        a = secrets.randbelow(P - 1)
        A = pow(G, a, P)

        print(f"Alice: {A}")

        s.sendall(A.to_bytes((P.bit_length() + 7) // 8, byteorder='big'))

        B_bytes = s.recv(2048)
        B = int.from_bytes(B_bytes, byteorder='big')

        print(f"Alice: {B}")

if __name__ == '__main__':
    sender()
