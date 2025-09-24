import sys
from math import trunc
from time import time
import random
import math


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if y == 0:
        return 1
    z = mod_exp(x, y // 2, N)
    if y % 2 == 0:
        return (z ** 2) % N
    else:
        return (x * (z ** 2)) % N


def fermat(N: int, k: int) -> bool:
    if N <= 1 or N % 2 == 0 or N % 3 == 0: return False

    for j in range(1, k + 1):
        a = random.randint(1, N - 1)
        if mod_exp(a, N - 1, N) != 1: return False
    return True


def miller_rabin(N: int, k: int) -> bool:
    if N == 2 or N == 3: return True
    if N <= 1 or N % 2 == 0 or N % 3 == 0: return False
    for i in range(k):
        exponent = N - 1
        a = random.randint(1, exponent)
        while exponent >= 1:
            result = mod_exp(a, exponent, N)
            if result != 1 and result != N-1 : return False
            if result == N-1: break
            if exponent % 2 == 1: break
            else: exponent = exponent // 2
    return True



def generate_large_prime(n_bits: int) -> int:
    num = random.getrandbits(n_bits)
    if fermat(num, 20) == False:
        return generate_large_prime(n_bits)
    else: return num


def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f'Generation took {time() - start} seconds')


if __name__ == '__main__':
    main(int(sys.argv[1]))
