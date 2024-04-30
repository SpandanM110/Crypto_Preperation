import socket
import math

def main():
    HOST = 'localhost'
    PORT = 1234

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print("Server is listening...")

        conn, addr = server_socket.accept()
        with conn:
            print("Connected by", addr)

            data = conn.recv(1024).decode()
            p = int(data)
            data = conn.recv(1024).decode()
            q = int(data)
            data = conn.recv(1024).decode()
            g = int(data)
            data = conn.recv(1024).decode()
            y = int(data)
            data = conn.recv(1024).decode()
            r = int(data)
            dataa = conn.recv(1024).decode()
            s = int(data)
            data = conn.recv(1024).decode()
            hashval = int(data)

            print("p: ", p)
            print("q: ", q)
            print("g: ", g)
            print("y: ", y)
            print("r: ", r)
            print("s: ", s)
            print("hash: ", hashval)

            print("Received signature {r, s} = " + str(r) + ", " + str(s)+ "}")

            w = pow(s, -1, q)
            u1 = (hashval * w) % q
            u2 = (r * w) % q
            v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q

            print("w =", w)
            print("v =", v)

            if v == r:
                print("Signature is valid")
            else:
                print("Signature is invalid")

if __name__ == "__main__":
    main()       
