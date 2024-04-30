import socket
import secrets

P =225
G = 14

def receiver():
    HOST = 'localhost'
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        b = secrets.randbelow(P - 1)
        B = pow(G, b, P)

        print(f"Alice: {B}")

        A_bytes = s.recv(2048)
        A = int.from_bytes(A_bytes, byteorder='big')

        s.sendall(B.to_bytes((P.bit_length() + 7) // 8, byteorder='big'))


if __name__ == '__main__':
    receiver()