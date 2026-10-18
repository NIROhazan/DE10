import time
import numpy as np

print("=== חידות מערכות ספרתיות - תוצאות בפורמט מדויק ===")

# 0. מכפלה vs חיבור
print("\n0. *2 vs +")
def mult2():
    x = 2**2000
    for i in range(10_000_000):
        _ = x * 2

def add2():
    x = 2**2000
    for i in range(10_000_000):
        _ = x + x

t_mult2 = time.time()
mult2()
t_mult2 = time.time() - t_mult2

t_add2 = time.time()
add2()
t_add2 = time.time() - t_add2

print(f" *2: {t_mult2:.3f}s")
print(f" + : {t_add2:.3f}s")
print(f" + faster {t_mult2/t_add2:.1f}x than *2")

# 1. כפל vs חלוקה
print("\n1. *5 vs //5")
def mult():
    x = 2**2000
    for i in range(10_000_000):
        _ = x * 5

def div():
    x = 2**2000
    for i in range(10_000_000):
        _ = x // 5

t_mult = time.time()
mult()
t_mult = time.time() - t_mult

t_div = time.time()
div()
t_div = time.time() - t_div

print(f" *5: {t_mult:.3f}s")
print(f" //5: {t_div:.3f}s")
print(f" *5 faster {t_div/t_mult:.1f}x than //5")

# 2. חלוקה בחזקה של 2 vs חלוקה במספר ראשוני
print("\n2. //8  vs //6 ")
def div_pow2():
    x = 2**2000
    for i in range(10_000_000):
        _ = x >> 3

def div_prime():
    x = 2**2000
    for i in range(10_000_000):
        _ = x // 6

t_pow2 = time.time()
div_pow2()
t_pow2 = time.time() - t_pow2

t_prime = time.time()
div_prime()
t_prime = time.time() - t_prime

print(f" //8: {t_pow2:.3f}s")
print(f" //6: {t_prime:.3f}s")
print(f" //8 faster {t_prime/t_pow2:.1f}x than //6")

# 3. Overflow
print("\n3. positive number + 1  = <0")
print(f"{np.int32(2147483647)} + {np.int32(1)} =  {np.int32(2147483647) + np.int32(1)} ")

# 4. דיוק מספרים צפים
print("\n4. 0.1 + 0.2 == 0.3?")
print(f"   {0.1 + 0.2:.20f} ≠ 0.3 → False")
