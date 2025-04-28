from perlin_noise import *
from random import randint

def map_fin(n_of_chunks, length, height):
    noise = PerlinNoise(octaves=10, seed=randint(1, 10*9))
    noise_2 = PerlinNoise(octaves=10, seed=randint(1, 10*9))
    noise_3 = PerlinNoise(octaves=10, seed=randint(1, 10*9))
    noise_4 = PerlinNoise(octaves=10, seed=randint(1, 10*9))
    noise_5 = PerlinNoise(octaves=10, seed=randint(1, 10*9))
    xpix, ypix = 100, 100

    map = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    map_2 = [[noise_2([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    map_3 = [[noise_3([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    map_4 = [[noise_4([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
    map_5 = [[noise_5([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

    mapa_fin = [[(map[i][j]+map_2[i][j]+map_3[i][j]+map_4[i][j]+map_5[i][j])/5 * 100 for j in range(xpix)] for i in range(ypix)]

    return mapa_fin