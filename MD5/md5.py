import struct

from enum import Enum
from math import floor, sin

from bitarray import bitarray

def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x,y,z):
    return y ^ (x | ~z)

def rotate_left(x,n):
    return (x << n) | (x >> (32-n))

def modular_add(a,b):
    return (a + b) % 2**32

T = [floor((2**32) * abs(sin(i+1))) for i in range(64)]

class MD5:
    input_string = None
    buffers = {
        'A': 0x67452301,
        'B': 0xefcdab89,
        'C': 0x98badcfe,
        'D': 0x10325476
    }

    def hash(self, string):
        self.input_string = string
        temp = self.step_1()
        preprocessed = self.step_2(temp)
        return self.step_4()
    
    def step_1(self):
        bit_array = bitarray(endian='big')
        bit_array.frombytes(self.input_string.encode('utf-8'))
        bit_array.append(1)
        while len(bit_array) % 512 != 448:
            bit_array.append(0)
        bit_array = bit_array.tobytes(endian='little')
        return bit_array
    
    def step_2(self, step_2_result):
        N = len(step_2_result) // 32
        for chunk_index in range(N//16):
            start = chunk_index * 512
            X = [step_2_result[start + (x * 32) : start + ( x*32) + 32] for x in range(16)]
            X = [int.from_bytes(word, byteorder='little') for word in X]

            A = self.buffers['A']
            B = self.buffers['B']
            C = self.buffers['C']
            D = self.buffers['D']

            for i in range(64):
                if 0 <= i <= 15:
                    k = i
                    s = [7, 12, 17, 22]
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    k = ((5*i)+1) % 16
                    s = [5, 9, 14, 20]
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    k = ((3*i)+5) % 16
                    s = [4, 11, 16, 23]
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    k = (7*i) % 16
                    s = [6, 10, 15, 21]
                    temp = I(B, C, D)

                temp = modular_add(temp, A)
                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, s[i % 4])

                A = D
                D = C
                C = B
                B = modular_add(B, temp)

            self.buffers['A'] = modular_add(self.buffers['A'], A)
            self.buffers['B'] = modular_add(self.buffers['B'], B)
            self.buffers['C'] = modular_add(self.buffers['C'], C)
            self.buffers['D'] = modular_add(self.buffers['D'], D)
        return self.buffers

    def step_4(self):
        A = struct.unpack("<I", struct.pack(">I", self.buffers['A']))[0]
        B = struct.unpack("<I", struct.pack(">I", self.buffers['B']))[0]
        C = struct.unpack("<I", struct.pack(">I", self.buffers['C']))[0]
        D = struct.unpack("<I", struct.pack(">I", self.buffers['D']))[0]
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"

if __name__ == "__main__":
    md5 = MD5()
    print(md5.hash("Hello World"))
