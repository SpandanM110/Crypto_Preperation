import binascii
import struct
import random

initial_hash = tuple(random.getrandbits(64) for _ in range(8))

round_constants = tuple(random.getrandbits(64) for _ in range(80))

def _right_rotate(n, bits):
    return (n >> bits) | ((n << (64 - bits)) & 0xFFFFFFFFFFFFFFFF)

def sha512(message):
    message_array = bytearray(message, encoding='utf-8')

    mdi = len(message_array) % 128
    padding_len = 119 - mdi if mdi < 112 else 247 - mdi
    ending = struct.pack('!Q', len(message_array) << 3)
    message_array.append(0x80)
    message_array.extend([0] * padding_len)
    message_array.extend(bytearray(ending))

    sha512_hash = list(initial_hash)
    for chunk_start in range(0, len(message_array), 128):
        chunk = message_array[chunk_start:chunk_start + 128]
        w = [0] * 80

        w[0:16] = struct.unpack('!16Q', chunk)
        for i in range(16, 80):
            s0 = (_right_rotate(w[i - 15], 1) ^ _right_rotate(w[i - 15], 8) ^ (w[i - 15] >> 7))
            s1 = (_right_rotate(w[i - 2], 19) ^ _right_rotate(w[i - 2], 61) ^ (w[i - 2] >> 6))
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFFFFFFFFFF

        a, b, c, d, e, f, g, h = sha512_hash

        for i in range(80):
            sum1 = (_right_rotate(e, 14) ^ _right_rotate(e, 18) ^ _right_rotate(e, 41))
            ch = (e & f) ^ (~e & g)
            temp1 = h + sum1 + ch + round_constants[i] + w[i]
            sum0 = (_right_rotate(a, 28) ^ _right_rotate(a, 34) ^ _right_rotate(a, 39))
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = sum0 + maj

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF
        
        sha512_hash = [(x + y) & 0xFFFFFFFFFFFFFFFF for x, y in zip(sha512_hash, [a, b, c, d, e, f, g, h])]

    return binascii.hexlify(b''.join(struct.pack('!Q', i) for i in sha512_hash)).decode('utf-8')

if __name__ == '__main__':
    print(sha512('hello world'))