import random
from Crypto.Util.number import getPrime
import sys
import base64

BIT_LENGTH = 1024
E_VALUE = 65537

def gcd(a, h):
    while True:
        temp = a % h
        if temp == 0:
            return h
        a = h
        h = temp

def generate_prime():
    while True:
        prime = getPrime(BIT_LENGTH)
        if prime.bit_length() == BIT_LENGTH:
            return prime

def main():
    message = input("Enter the message: ")
    msg = int.from_bytes(message.encode('utf-8'), byteorder=sys.byteorder)
    print("Message in bytes: ", msg)

    p = generate_prime()
    q = generate_prime()
    n = p*q
    phi = (p-1)*(q-1)

    e = E_VALUE

    k = 2
    d = (1 + k * phi) // e

    c = pow(msg, e, n)

    print("Public key: ", c)

    m = pow(c, d, n)
    decrypted_bytes = m.to_bytes((m.bit_length() + 7) // 8, byteorder=sys.byteorder)

    decrypted_message_base64 = base64.b64encode(decrypted_bytes).decode('utf-8')

    print("Decrypted message: ", decrypted_message_base64)

if __name__ == "__main__":
    main()