# Project Report - RSA and Primality Tests

## Baseline

### Design Experience

I'm doing this project next to my brother Jack, so we will discuss our ideas as we work. In the generate_large_prime() function, I'll start a 'while' loop that chooses random numbers and checks them with fermat(). If it passes, the loop ends and the number is returned.

In fermat(), I'll start a 'for' loop from range 0 to k to test the number k times. In each iteration of the loop, I'll generate a new base number 'a' and call mod_exp(). If mod_exp() doesn't return 1, fermat() return false and generate_large_primes() picks a new candidate prime. If mod_exp() returns 1 in each iteration of the 'for' loop, the number is accepted as a prime.

In mod_exp(), I will recurse down to the base case y == 0 returns 1 and then return exponentiations of the base number 'a' (these exponentiations are 'z') back up the recursion. If y is divisible by 0 in a recursive call, I'll return 'z' squared mod N. If not, I'll return 'a' multiplied by 'z' squared mod N.

### Theoretical Analysis - Prime Number Generation

#### Time 

```py
def mod_exp(x: int, y: int, N: int) -> int:
    if (y == 0):                        # O(1) - comparison
        return 1
    z = mod_exp(x, y//2, N)             # O(log y) - runs log y times
    if (y % 2 == 0):                    # O(1) - check if number is even
        return (z ** 2) % N             # O(1) - return math operation
    else:
        return (x * (z ** 2)) % N       # O(1) - return math operation

def fermat(N: int, k: int) -> bool:
    if N <= 1 or N % 2 == 0:            # O(1) - small checks
        return False                    # O(1) - return bool
    for i in range(0, k):               # O(1) - loop runs k (20) times
        a = random.randint(1, N-1)          # O(1) - picks random base number
        if (mod_exp(a, N-1, N) != 1):       # O(log N-1) - runs mod_exp()
            return False                        # O(1) - return bool
    return True                         # O(1) - return bool

def generate_large_prime(n_bits: int) -> int:
    while True:                             # O(n) - 1/n chance of finding a prime between 0 and n-bits
        N = random.getrandbits(n_bits)          # O(1) - picks a random number
        if fermat(N, 20) == True:               # O(log N-1) - comparison
            return N

# Overall: O(n * log(n))
```
The 'while' loop in generating_large_primes() is going to run about n times to find a valid prime. The 'for' loop in fermat runs k times. The recursion in mod_exp() goes log(N-1) layers deep.

#### Space

```py
def mod_exp(x: int, y: int, N: int) -> int:
    if (y == 0):
        return 1                        # O(1) - returns int
    z = mod_exp(x, y//2, N)             # O(log y) - returns int for each recursive call
    if (y % 2 == 0):
        return (z ** 2) % N             # O(1) - returns int
    else:
        return (x * (z ** 2)) % N       # O(1) - returns int

def fermat(N: int, k: int) -> bool:
    if N <= 1 or N % 2 == 0:
        return False
    for i in range(0, k):               # O(1) - stores one int i
        a = random.randint(1, N-1)          # O(1) - stores int 'a'
        if (mod_exp(a, N-1, N) != 1):       # O(log N-1) - log(N-1) z's created in mod_exp()
            return False
    return True

def generate_large_prime(n_bits: int) -> int:
    while True:
        N = random.getrandbits(n_bits)          # O(1) stores int N
        if fermat(N, 20) == True:               # O(log y)
            return N

```

Generate_large_primes initializes int N. Fermat() stores int i in it's 'for' loop. Mod_exp() stores new z's for every recursive call, but they are wiped when we exit the scope of the function.

### Empirical Data

| N    | time (ms) |
|------|-----------|
| 64   | 2.0       |
| 128  | 5.4       |
| 256  | 9.0       |
| 512  | 94.2      |
| 1024 | 1846.3    |
| 2048 | 24754.5   |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: O(n * log(n))
- Measured constant of proportionality for theoretical order: 0.00521
- Empirical order of growth (if different from theoretical): n^2.32
- Measured constant of proportionality for empirical order: 0.00012

![img](plots\Figure_1.png)

I think I severely underestimated the work mod_exp was doing. While I can keep track of the recursive calls, I can't keep track of the mathematics that goes on behind the scenes.

## Core

### Design Experience

In generate_key_pairs(), I will generate two prime numbers p and q and calculate N and (p-1)*(q-1). In a loop, I'll pick a prime 'e' from the array and test it with extended_euclids. If the gcd is 1, I can break from the loop and use the 'd'. Then, I will return (N,e,d).

In extended_euclids(), I will recurse down to the base case b == 0 using recursive calls extended_euclid(b, a % b). For each recursive call, I'll return (y, x-((a//b)*y), z) as (x,y,z) for the recursive call above it.

### Theoretical Analysis - Key Pair Generation

#### Time 

```py
def extended_euclid(a, b):
    if b == 0:                              # O(1) - boolean check
        return (1,0,a)
    (x,y,z) = extended_euclid(b, a % b)     # O(a/b) - I honestly can't calculate it, but this is my best guess as to how many times it runs
    return (y, x-((a//b)*y), z)             # O(1)


def generate_key_pairs(n_bits) -> tuple[int, int, int]:
    while (True):                           # O(1) - basically NEVER has to repeat
        p = generate_large_prime(n_bits)    # O(n^2.32) - ~empirical runtime from baseline
        q = generate_large_prime(n_bits)    # O(n^2.32) - ~empirical runtime from baseline
        if p != q: break
    N = p * q                               # O(1) - calculation
    pxq = (p-1) * (q-1)                     # O(1) - calculation
    while (True):                           # O(1) - all primes have gcd of 1
        e = primes[random.randint(0, len(primes)-1)]    # O(1) - picks number
        d, _, gcd = extended_euclid(e, pxq)             # O(e / (p-1)(q-1)) - I think extended_euclid should run about this many times
        if gcd == 1: break
    d = d % pxq         # O(1) - modulo
    return (N,e,d)
```
Generate_key_pairs() incurs the O(n^2.32) from generate_large_primes(). I struggled to understand runtime of extended_euclids(), but I think it's around O(e / (p-1)(q-1))

#### Space

```py
def extended_euclid(a, b):
    if b == 0:
        return (1,0,a)                  # O(1) - returns 3 numbers
    (x,y,z) = extended_euclid(b, a % b) # O(a/b) - stores 3 numbers
    return (y, x-((a//b)*y), z)         # O(1) - returns 3 numbers


def generate_key_pairs(n_bits) -> tuple[int, int, int]:

    while (True):
        p = generate_large_prime(n_bits)    # O(1) - stores large prime
        q = generate_large_prime(n_bits)    # O(1) - stores large prime
        if p != q: break
    N = p * q                               # O(1) - stores multiplied number
    pxq = (p-1) * (q-1)                     # O(1) - stores multiplied number
    while (True):
        e = primes[random.randint(0, len(primes)-1)]    # O(1) - stores e
        d, _, gcd = extended_euclid(e, pxq)             # O(e / (p-1)(q-1)) - calls function that stores numbers in its recursive calls
        if gcd == 1: break
    d = d % pxq
    return (N,e,d)          # O(1) - returns 3 numbers

```
I don't think these should take up much space, but extended_euclids() will store more depending on the number of recursive calls

### Empirical Data

| N    | time (ms) |
|------|-----------|
| 64   | 2.0       |
| 128  | 7.5       |
| 256  | 45.6      |
| 512  | 404.5     |
| 1024 | 5681.7    |
| 2048 | 25143.7   |

### Comparison of Theoretical and Empirical Results

- Theoretical order of growth: O(n^2.32)
- Measured constant of proportionality for theoretical order: 0.00012
- Empirical order of growth (if different from theoretical): seems to be the same
- Measured constant of proportionality for empirical order: 

![img](img.png)

The main time contribution to this process seemed to be the O(n^2.32) from generating and verifying the primes. Negligible time was added.

## Stretch 1

### Design Experience

I didn't design anything for this stretch, the code was provided to us. My brother and I exchanged small encrypted messages to each other for the other to decrypt.

### Theoretical Analysis - Encrypt and Decrypt

#### Time 

N/A

#### Space

N/A

### Empirical Data

#### Encryption

| N    | time (ms) |
|------|-----------|
| 64   | 0.018540  |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

No way to change n_bits

#### Decryption

| N    | time (ms) |
|------|-----------|
| 64   | 0.336926  |
| 128  |           |
| 256  |           |
| 512  |           |
| 1024 |           |
| 2048 |           |

No way to change n_bits

### Comparison of Theoretical and Empirical Results

#### Encryption
- No way to change n_bits, not sure what to do here
- Theoretical order of growth: *copy from section above* 
- Measured constant of proportionality for theoretical order: 
- Empirical order of growth (if different from theoretical): 
- Measured constant of proportionality for empirical order: 

![img](img.png)

No way to change n_bits for encryption and decryption in encrypt_decrypt_files.

#### Decryption

- No way to change n_bits, not sure what to do here
- Theoretical order of growth: *copy from section above* 
- Measured constant of proportionality for theoretical order: 
- Empirical order of growth (if different from theoretical): 
- Measured constant of proportionality for empirical order: 

![img](img.png)

No way to change n_bits for encryption and decryption in encrypt_decrypt_files.

### Encrypting and Decrypting With A Classmate

My brother Jack and I exchanged small encrypted messages with each other over Discord. Our encryption was successful, though we had a bit of trouble at first because we pasted the messages into Discord rather than sending each other the files. Discord's handling of the encrypted characters was incorrect. Once we used the files themselves, it worked.

## Stretch 2

### Design Experience

For miller_rabin(), I will start the function like fermat(), checking for N <= 1 and if N is even. Then, I'll start a for loop from values 0 to k (with k going up the more certain you need to be in the number being prime). I'll initialize a random int 'a' and the exponent as 'N-1'. In a while loop, I'll call mod_exp(a, exp, N). If the result isn't 1 or -1, we can break from the loop and return false. If the result is -1 (or N-1), then we can break from the loop knowing the number is prime. Also, if the exponent is no longer divisible by 2, we can break from the loop knowing the number is prime.

### Discussion: Probabilistic Natures of Fermat and Miller Rabin 

For each k of Fermat that we run, the probability of the number being prime goes up by at least 50%. This means that the probability of fermat returning yes when N is not prime at k=5 is 2^-5, or about 3%. In Miller Rabin, 3/4 of the possible values of a will reveal a composite number. This means that the probability of returning yes when N is not prime at k=5 is 4^-5, or about 0.09%. Fermat's works pretty well, but Miller Rabin's is exceptional. It does not require as high of a k value to reach the same certainty that a number is prime.

## Project Review



