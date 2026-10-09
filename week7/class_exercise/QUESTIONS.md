# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - החילזון: מור ומילי

30 דקות, 7 שאלות: Q01-Q07

### Q01 - כמה מצבים לגלאי?

- **מתגים ונורות:** `the pattern length = HEX0     the pattern = the right LEDs of LEDG3..LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה האורך של רצף, ובנורות הירוקות הרצף עצמו.
- `length = HEX0`
- כמה מצבים צריך גלאי מור של הרצף הזה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- וכמה מצבים צריך גלאי מילי?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

### Q02 - החילזון: מתי הוא מחייך?

- **מתגים ונורות:** `the tape bit A = SW9 (HEX3)     smile Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- החילזון זוחל על סרט של אפסים ואחדות: ביט אחד בכל לחיצה. הוא מחייך כששני הביטים האחרונים הם רצף מסוים.
- `A = SW9     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה הרצף?
- `SW1 = first bit     SW0 = second bit`

**שלב 2**

- האם החיוך מופיע כבר כשמזיזים את המתג (לפני הלחיצה)?
- `Moore (no) = all down     Mealy (yes) = SW0`

### Q03 - המצבים של חילזון מור

- **מתגים ונורות:** `A = SW9 (HEX3)     S1 S0 = LEDG3 LEDG2     Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח חילזון מור של שלושה מצבים, וביטי המצב מוצגים:
- `A = SW9     S1 S0 = LEDG3 LEDG2     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה הקוד של מצב ההתחלה (אחרי איפוס)?
- `SW1 SW0 = LEDG3 LEDG2`

**שלב 2**

- מה הרצף שמחייך?
- `SW1 = first bit     SW0 = second bit`

**שלב 3**

- מה הקוד של המצב שבו הוא מחייך?
- `SW1 SW0 = LEDG3 LEDG2`

### Q04 - טבלת היציאה של חילזון מילי

- **מתגים ונורות:** `A = SW9 (HEX3)     S0 = LEDG1     Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח חילזון מילי: ביט מצב אחד (הביט הקודם בסרט), והיציאה תלויה בו ובביט הנוכחי.
- `A = SW9     S0 = LEDG1     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מתי
- `Y = 1`
- ? הרימו את המתג של כל מקרה:
- `S0 A = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

### Q05 - כמה חיוכים על הסרט?

- **מתגים ונורות:** `A = SW9 (HEX3)     Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח חילזון מור (רצף נסתר, חופף). אפסו, והעבירו אותו על הסרט: ביט אחד בכל לחיצה.
- `the tape:   0 1 1 0 1 0 0 1 1 1`
- `A = SW9     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה פעמים הוא חייך (אחרי לחיצה)?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

### Q06 - כמה אחדות ברצף?

- **מתגים ונורות:** `A = SW9 (HEX3)     Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח גלאי מור: הנורה נדלקת אחרי כמה אחדות ברצף.
- `A = SW9     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה אחדות ברצף צריך?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- כמה מצבים צריך לגלאי הזה כמכונת מור? (מצב לכל מספר אחדות שנראו, כולל 0)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

**שלב 3**

- וכמה כמכונת מילי? (היציאה נקבעת כבר עם הביט האחרון)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

### Q07 - גלאי שינוי

- **מתגים ונורות:** `A = SW9 (HEX3)     Y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח גלאי שינוי בכניסה: הנורה נדלקת למחזור אחד כשהכניסה משתנה בדרך מסוימת.
- `A = SW9     Y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה שינוי?
- `rising (0 -> 1) = all down     falling (1 -> 0) = SW0     any change = SW1`

**שלב 2**

- האם הנורה נדלקת כבר כשמזיזים את המתג, לפני הלחיצה?
- `Moore (no) = all down     Mealy (yes) = SW0`

## נושא 2 - פירוק מכונות: התהלוכה

30 דקות, 4 שאלות: Q08-Q11

### Q08 - מכונת המצב של התהלוכה

- **מתגים ונורות:** `P / R on SW7 SW6     M = LEDG4     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח בקר הרמזור עם תהלוכה. כאן מסתכלים רק על מכונת המצב:
- `M = LEDG4     P, R = SW7, SW6 (in some order)`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג מפסיק תהלוכה
- `(R)`
- - מכבה את
- `M`
- `?`
- `SW7 = all down     SW6 = SW0`

**שלב 2**

- הורידו את שניהם. האם
- `M`
- נשאר כמו שהוא (מכונה עם זיכרון)?
- נשאר - הרימו:
- `SW0`
- חוזר ל-0 - השאירו למטה.

**שלב 3**

- הרימו את שניהם ולחצו. מי מנצח?
- `P = all down     R = SW0`

### Q09 - מצב תהלוכה

- **מתגים ונורות:** `TA SW9, TB SW8, P / R on SW7 SW6     lights LEDG7..5, LEDG2..0     M = LEDG4     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח בקר הרמזור עם מצב תהלוכה (שתי מכונות: מכונת המצב ומכונת הרמזורים).
- `TA = SW9     TB = SW8     P, R = SW7, SW6 (in some order)     M = LEDG4`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג מתחיל תהלוכה
- `(P)`
- - מדליק את
- `M`
- בלחיצה?
- `SW7 = all down     SW6 = SW0`

**שלב 2**

- בזמן תהלוכה, איזה רחוב נשאר ירוק (גם בלי מכוניות)?
- `A = all down     B = SW0`

### Q10 - כמה זמן עד שהתהלוכה עוברת?

- **מתגים ונורות:** `TA SW9, TB SW8, P = SW7, R = SW6     lights LEDG7..5, LEDG2..0     M = LEDG4     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח בקר הרמזור עם תהלוכה ברחוב השני.
- `TA = SW9   TB = SW8   P = SW7   R = SW6   M = LEDG4`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אפסו (הרחוב הראשון ירוק), הרימו את
- `TA`
- ואת
- `P`
- ולחצו פעם אחת. אחרי כמה לחיצות נוספות הרחוב השני ירוק?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q11 - כמה מצבים עם פירוק ובלי?

- **מתגים ונורות:** `TA = SW9     TB = SW8     lights LEDG7..5, LEDG2..0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח בקר רמזור שבו הצהוב נמשך כמה לחיצות (כל לחיצה של צהוב היא מצב).
- `TA = SW9     TB = SW8`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה מצבים יש למכונת הרמזורים? (2 ירוקים ועוד כל מצבי הצהוב)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 2**

- מוסיפים מצב תהלוכה (שני מצבים: יש או אין). כמה מצבים צריך מכונה אחת בלי פירוק?
- `16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 3**

- וכמה מצבים בסך הכול בשתי מכונות נפרדות (פירוק)?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`
- `10 = SW3+SW1`

## נושא 3 - תכנון מכונות מצבים

30 דקות, 9 שאלות: Q12-Q20

### Q12 - זוגיות טורית

- **מתגים ונורות:** `SW9 SW8 (one is the input)     LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכונה שסופרת כמה אחדות נכנסו (ביט בכל לחיצה) ומראה רק זוגי או אי-זוגי. אחד המתגים לא מחובר.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא הכניסה?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- אפסו (נכנסו 0 אחדות). הנורה דולקת?
- `LED on after reset = even parity`
- דולקת - הרימו:
- `SW0`
- כבויה - השאירו למטה.

### Q13 - מונה אחדות

- **מתגים ונורות:** `SW9 SW8     the count = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מונה: בכל לחיצה הוא מוסיף 1 אם הכניסה 1. אחד המתגים הוא הכניסה.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- אחרי איזה מספר הוא חוזר ל-0? כתבו כמה מצבים יש.
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

### Q14 - מונה שנעצר או חוזר

- **מתגים ונורות:** `the count = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מונה. לחצו שוב ושוב.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה המספר הגדול ביותר שהוא מגיע אליו?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- ואחריו - הוא נעצר שם, או חוזר ל-0?
- נעצר - הרימו:
- `SW0`
- חוזר ל-0 - השאירו למטה.

### Q15 - מסנן קפיצות

- **מתגים ונורות:** `the button = SW9 (HEX3)     clean = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מסנן: הנורה נדלקת רק אם הכניסה נשארה 1 כמה לחיצות ברצף, ונכבית מיד כשהיא 0.
- `the button = SW9     clean = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה לחיצות ברצף צריך?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

**שלב 2**

- כמה מצבים יש למכונה? (מונה מ-0 עד המספר הזה)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`

### Q16 - מנעול של שלושה ביטים

- **מתגים ונורות:** `the bit = SW9 (HEX3)     open = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח מנעול: מכניסים שלושה ביטים, אחד בכל לחיצה. ביט שגוי מחזיר להתחלה, ואחרי שנפתח הוא נשאר פתוח עד איפוס.
- `the bit = SW9     open = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה הקוד?
- `SW2 = first bit     SW1 = second     SW0 = third`

### Q17 - מנעול צירופים

- **מתגים ונורות:** `the symbol = SW9 SW8     open = LEDG0     clock = KEY1, reset = KEY0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מנעול: מכניסים שני סמלים (כל אחד = שני מתגים, לחיצה אחת), והנורה נדלקת כשהצירוף נכון.
- `the symbol = SW9 SW8     open = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה הסמל הראשון?
- `SW1 SW0 = SW9 SW8`

**שלב 2**

- ומה הסמל השני?
- `SW1 SW0 = SW9 SW8`

### Q18 - מכונת שתייה

- **מתגים ונורות:** `SW9 SW8 (nickel 5, dime 10)     paid = HEX1 HEX0     drink = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכונת שתייה: מטבע של 5 ומטבע של 10, כל אחד על מתג (מטבע נכנס בלחיצה). התצוגה מראה כמה שולם.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא המטבע של 10?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- כמה עולה שתייה (הנורה נדלקת)? כתבו את המחיר חלקי 5.
- `15 = SW1+SW0     20 = SW2     25 = SW2+SW0     30 = SW2+SW1`

### Q19 - שתי מכונות שמדברות

- **מתגים ונורות:** `machine A = LEDG0     machine B = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח שתי מכונות: מכונה א' מתהפכת בכל לחיצה (נורה), ומכונה ב' סופרת (תצוגה), אבל רק כשמכונה א' במצב מסוים.
- `A = LEDG0     B = HEX0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה מצבים יש למכונה ב'?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`

**שלב 2**

- מכונה ב' מתקדמת בלחיצה כשהנורה של א' (לפני הלחיצה)
- דולקת - הרימו:
- `SW0`
- כבויה - השאירו למטה.

### Q20 - בורר בקשות

- **מתגים ונורות:** `request 1 = SW9     request 0 = SW8     grant 1 = LEDG1     grant 0 = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח בורר: שתי בקשות, ובכל לחיצה הוא נותן אישור לאחת.
- `requests: SW9 (1), SW8 (0)     grants: LEDG1, LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אפסו, הרימו את שתי הבקשות ולחצו. מי קיבל?
- `0 = all down     1 = SW0`

**שלב 2**

- לחצו שוב כמה פעמים עם שתי הבקשות. האישור מתחלף (סבב) או נשאר לאותה בקשה (עדיפות קבועה)?
- `round robin = all down     fixed = SW0`

