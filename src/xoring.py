import numpy as np
import struct
from scipy.signal import wiener
from itertools import product
from joblib import Parallel, delayed
from scipy.interpolate import interpn
import random
PRIME32_3 = 0xC2B2AE3D
PRIME_MX2 = 0x9FB21C651E98DF25

PRIME32_3 = 0xC2B2AE3D
PRIME_MX2 = 0x9FB21C651E98DF25
default_secret = bytes([
    0xb8, 0xfe, 0x6c, 0x39, 0x23, 0xa4, 0x4b, 0xbe, 0x7c, 0x01, 0x81, 0x2c, 0xf7, 0x21, 0xad, 0x1c,
    0xde, 0xd4, 0x6d, 0xe9, 0x83, 0x90, 0x97, 0xdb, 0x72, 0x40, 0xa4, 0xa4, 0xb7, 0xb3, 0x67, 0x1f,
    0xcb, 0x79, 0xe6, 0x4e, 0xcc, 0xc0, 0xe5, 0x78, 0x82, 0x5a, 0xd0, 0x7d, 0xcc, 0xff, 0x72, 0x21,
    0xb8, 0x08, 0x46, 0x74, 0xf7, 0x43, 0x24, 0x8e, 0xe0, 0x35, 0x90, 0xe6, 0x81, 0x3a, 0x26, 0x4c,
    0x3c, 0x28, 0x52, 0xbb, 0x91, 0xc3, 0x00, 0xcb, 0x88, 0xd0, 0x65, 0x8b, 0x1b, 0x53, 0x2e, 0xa3,
    0x71, 0x64, 0x48, 0x97, 0xa2, 0x0d, 0xf9, 0x4e, 0x38, 0x19, 0xef, 0x46, 0xa9, 0xde, 0xac, 0xd8,
    0xa8, 0xfa, 0x76, 0x3f, 0xe3, 0x9c, 0x34, 0x3f, 0xf9, 0xdc, 0xbb, 0xc7, 0xc7, 0x0b, 0x4f, 0x1d,
    0x8a, 0x51, 0xe0, 0x4b, 0xcd, 0xb4, 0x59, 0x31, 0xc8, 0x9f, 0x7e, 0xc9, 0xd9, 0x78, 0x73, 0x64,
    0xea, 0xc5, 0xac, 0x83, 0x34, 0xd3, 0xeb, 0xc3, 0xc5, 0x81, 0xa0, 0xff, 0xfa, 0x13, 0x63, 0xeb,
    0x17, 0x0d, 0xdd, 0x51, 0xb7, 0xf0, 0xda, 0x49, 0xd3, 0x16, 0x55, 0x26, 0x29, 0xd4, 0x68, 0x9e,
    0x2b, 0x16, 0xbe, 0x58, 0x7d, 0x47, 0xa1, 0xfc, 0x8f, 0xf8, 0xb8, 0xd1, 0x7a, 0xd0, 0x31, 0xce,
    0x45, 0xcb, 0x3a, 0x8f, 0x95, 0x16, 0x04, 0x28, 0xaf, 0xd7, 0xfb, 0xca, 0xbb, 0x4b, 0x40, 0x7e,
])
def lower_half(x):
    return x & 0xFFFFFFFFFFFFFFFF
def XXH3_64_4to8(input_length, secret, seed):
    secret_words = secret[8:24]
    to_int = str(bin(seed))[2:]
    input_first = int(to_int[0:4], base=2)
    input_last = int(to_int[-4:], base=2)
    modified_seed = seed ^ (struct.unpack('>I', struct.pack('<I', lower_half(seed)))[0] << 32)
    combined = (input_last | (input_first << 32)) & 0xFFFFFFFFFFFFFFFF
    value = ((secret_words[0] ^ secret_words[1]) - modified_seed) ^ combined
    value ^= (value << 49) & 0xFFFFFFFFFFFFFFFF
    value ^= (value << 24) & 0xFFFFFFFFFFFFFFFF
    value = (value * PRIME_MX2) & 0xFFFFFFFFFFFFFFFF
    value ^= ((value >> 35) + input_length) & 0xFFFFFFFFFFFFFFFF
    value = (value * PRIME_MX2) & 0xFFFFFFFFFFFFFFFF
    value ^= (value >> 28)
    return value
def random_num(a,b):
  return 0
def side_gen(s):
  return int(2**s + 1)
def chunk_gen(a, b, c, d, side_x, side_y):
    def mid(a, b):
        return (a + b) // 2 + random_num(-1, 1)

    chunk = np.zeros((side_x, side_y), dtype=int)
    chunk[0][0], chunk[0][side_y - 1], chunk[side_x - 1][0], chunk[side_x - 1][side_y - 1] = a, b, d, c
    ab = mid(a, b)
    bc = mid(b, c)
    cd = mid(c, d)
    da = mid(d, a)
    mid_val = (a + b + c + d) // 4 + random_num(-1, 1)

    if min(side_x, side_y) != 3:  # Проверяем, чтобы хотя бы одна из сторон не была равна 3
        to_x = (side_x + 1) // 2
        from_x = (side_x - 1) // 2
        to_y = (side_y + 1) // 2
        from_y = (side_y - 1) // 2
        
        chunk[0:to_x, 0:to_y] = chunk_gen(a, ab, mid_val, da, to_x, to_y)
        chunk[0:to_x, from_y:side_y] = chunk_gen(ab, b, bc, mid_val, to_x, to_y)
        chunk[from_x:side_x, from_y:side_y] = chunk_gen(mid_val, bc, c, cd, to_x, to_y)
        chunk[from_x:side_x, 0:to_y] = chunk_gen(da, mid_val, cd, d, to_x, to_y)
    else:
        chunk[0][1] = ab
        chunk[1][0] = da
        chunk[1][2] = bc
        chunk[2][1] = cd
        chunk[1][1] = mid_val

    return chunk
def generate_xor(side, chunk_side,  max_height, num_points=100):
    max_height = round(max_height / 4) * 4
    arr = []
    x_arr = []
    y_arr = []
    for i in range(side+2):
        arr_1 =[]
        for j in range(side+2):
            x_arr.append(i)
            y_arr.append(j)
            x = int(str(XXH3_64_4to8(j, default_secret, i))[:random.choice([2, 3])])
            arr_1.append(x % max_height)
        arr.append(arr_1)
    x_arr = np.array(x_arr)
    y_arr = np.array(y_arr)
    x_arr = np.arange(np.min(x_arr), np.max(x_arr) + 1)
    y_arr = np.arange(np.min(y_arr), np.max(y_arr) + 1)
    x_new = np.linspace(np.min(x_arr), np.max(x_arr), num_points)
    y_new = np.linspace(np.min(y_arr), np.max(y_arr), num_points)
    p1_i = (x_arr, y_arr)
    new_nodes = list(product(x_new, y_new))
    new_values = interpn(p1_i, arr, new_nodes, method='cubic')
    new_values = new_values.reshape((len(x_new), len(y_new)))
    heights = new_values
    heights_mid = np.array([[0]*(side+1)]*(side+1))
    def compute_height(x, y):
        return int((heights[x, y] + heights[x + 1, y] + heights[x, y + 1] + heights[x + 1, y + 1]) // 4) + random.randint(max_height - max_height // 4, max_height + max_height // 4)

    data = product(range(side + 1), range(side + 1))
    xyz_list = Parallel(n_jobs=-1)(
        delayed(lambda x, y: (x, y, compute_height(x, y)))(x, y) for x, y in data
    )

    for x, y, height in xyz_list:
        heights_mid[x, y] = height
        
    #heights_mid = wiener(heights_mid, (12, 9))
    map = np.array([[0]*(side*chunk_side)]*(side*chunk_side))
    for x in range(side):
        for y in range(side):
            map[chunk_side*y:chunk_side*(y+1), chunk_side*x:chunk_side*(x+1)] = chunk_gen(heights_mid[x,y], heights_mid[x,y+1], heights_mid[x+1,y+1], heights_mid[x+1,y],chunk_side, chunk_side)
    return map
