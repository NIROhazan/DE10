import numpy as np
import timeit

# 1. מספר INT שהופך לשלילי
max_int = np.int32(2147483647)
print(max_int + np.int32(1))

# 2. הכפלה בחזקה של 2 לעומת אחר
print(timeit.timeit("1000 * 4", number=1000000))
print(timeit.timeit("1000 * 5", number=1000000))

# 3. חלוקה ב-2 לעומת ב-3
print(timeit.timeit("1000 // 2", number=1000000))
print(timeit.timeit("1000 // 3", number=1000000))

# 4. דיוק מספרים צפים
print(0.1 + 0.2 == 0.3)

# 5. בדיקת חזקה של 2
def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0
print(is_power_of_two(8))
print(is_power_of_two(7))

# 6. שלילה ב-Two's Complement
x = np.int32(5)
print(np.int32(~x + 1))

# 7. בדיקת זוגיות
print(timeit.timeit("1000 & 1 == 0", number=1000000))
print(timeit.timeit("1000 % 2 == 0", number=1000000))

# 8. הביט הנמוך ביותר
x = 40
print(x & -x)