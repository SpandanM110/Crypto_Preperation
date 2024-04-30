import socket
import math
import random

def main():
    HOST = 'localhost'
    PORT = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print("Connected to server")

        p = int(input("Enter p: "))
        q = int(input("Enter q: "))
        h = int(input("Enter h: "))

        exponent = (p - 1) // q
        g = pow(h, exponent, p)
        print("g: ", g)

        x = int(input("Enter x: "))
        y = pow(g, x, p)
        print("y: ", y)

        M = int(input("Enter M: "))
        hashkey = 1234

        hasval = (M ^ hashkey) % p

        print("hash: ", hasval)

        q_bit_length = int(math.log2(q))
        k = random.getrandbits(q_bit_length - 1)

        r = pow(g, k, p) % q
        s = (pow(k, -1, q) * (h + x * r)) % q

        print("Generated signature {r, s} = " + str(r) + ", " + str(s)+ "}")

        print("Sending signature to server")
        client_socket.sendall(str(p).encode())
        client_socket.sendall(str(q).encode())
        client_socket.sendall(str(g).encode())
        client_socket.sendall(str(y)).encode()
        client_socket.sendall(str(r).encode())
        client_socket.sendall(str(s).encode())
        client_socket.sendall(str(hashval).encode())

if __name__ == "__main__":
    main()



