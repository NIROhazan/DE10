import time
import sympy

x = 2**2000
d_pow2 = 2**1000
p = sympy.nextprime(d_pow2 + 1)

# Time bit shift (faster)
start = time.time()
for _ in range(100000):
    _ = x >> 1000
t_shift = time.time() - start

# Time // by power of 2 (no shift, slower)
start = time.time()
for _ in range(100000):
    _ = x // d_pow2
t_div_pow2 = time.time() - start

# Time // by prime (similarly slow)
start = time.time()
for _ in range(100000):
    _ = x // p
t_div_prime = time.time() - start
tst = 1
# Example results: shift ~0.006s, div pow2 ~0.205s (33x slower), div prime ~0.208s (33x slower)