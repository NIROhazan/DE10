# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - מכונות מצבים: מצבים, מעברים ויציאות

30 דקות, 8 שאלות: Q01-Q08

### Q01 - כמה דלגלגים?

- **מתגים ונורות:** `the number of states = HEX1 HEX0     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מספר המצבים של מכונה. כמה דלגלגים צריך בקידוד אחד-חם (ביט לכל מצב)?
- `16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- וכמה בקידוד בינארי?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q02 - מחלק ב-N

- **מתגים ונורות:** `q = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מכונת מצבים בלי כניסות: היא עוברת מצב בכל לחיצה, והנורה דולקת רק במצב אחד.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כל כמה לחיצות הנורה נדלקת?
- `divide by N:   N = ?`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- אפסו. אחרי כמה לחיצות הנורה נדלקת בפעם הראשונה?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 3**

- כמה דלגלגים צריך לפחות לקידוד בינארי של המצבים?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q03 - טבלת מעברים של שני מצבים

- **מתגים ונורות:** `a = SW9 (HEX3)     state S = LEDG1     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכונה של שני מצבים. המצב מוצג בנורה, והכניסה על מתג:
- `S = LEDG1     a = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לכל מצב ולכל ערך של הכניסה: לאן עוברים בלחיצה? מצב 1 - הרימו:
- `S=0 a=0 -> SW3     S=0 a=1 -> SW2     S=1 a=0 -> SW1     S=1 a=1 -> SW0`

**שלב 2**

- בכמה מארבעת המקרים המכונה נשארת באותו מצב?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q04 - טבלת יציאות של מכונת מור

- **מתגים ונורות:** `S1 S0 = LEDG3 LEDG2     Y1 Y0 = LEDG1 LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכונת מור שעוברת על 4 מצבים. ביטי המצב והיציאות מוצגים:
- `S1 S0 = LEDG3 LEDG2     Y1 Y0 = LEDG1 LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- בכל מצב שבו
- `Y0 = 1`
- הרימו את המתג שלו:
- `S = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

**שלב 2**

- אותו דבר בשביל
- `Y1 = 1`
- `S = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

### Q05 - מור או מילי?

- **מתגים ונורות:** `a = SW9 (HEX3)     y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח מכונת מצבים עם כניסה ויציאה:
- `a = SW9     y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- במכונת מור היציאה תלויה רק במצב. במכונת מילי היא תלויה גם בכניסה, ויכולה להשתנות בלי לחיצה.
- נסו כמה מצבים: הזיזו את המתג בלי ללחוץ. איזו מכונה?
- `Moore = all down     Mealy = SW0`

### Q06 - דיאגרמת מצבים של 4 מצבים

- **מתגים ונורות:** `a = SW9 (HEX3)     the state = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 4

**שלב 1**

- בלוח מכונה של 4 מצבים (0 עד 3, מוצג בתצוגה), עם כניסה אחת. ציירו את הדיאגרמה.
- `S = 0  (HEX0)`
- `a = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 2**

- המצב הבא בדיאגרמה:
- `S = 1  (HEX0)`
- `a = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 3**

- המצב הבא בדיאגרמה:
- `S = 2  (HEX0)`
- `a = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 4**

- המצב הבא בדיאגרמה:
- `S = 3  (HEX0)`
- `a = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

### Q07 - הדרך הקצרה ביותר

- **מתגים ונורות:** `a = SW9 (HEX3)     the state = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח מכונה של 4 מצבים, המצב בתצוגה, כניסה אחת:
- `a = SW9     HEX0 = S`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה המספר הקטן ביותר של לחיצות שמביא ממצב 0 (אחרי איפוס) למצב 3?
- `S = 3`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q08 - קידוד מצבים

- **מתגים ונורות:** `the state bits = LEDG3..LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מכונה שעוברת על כמה מצבים. הנורות מראות את ביטי המצב (הדלגלגים).
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה מצבים יש?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- כמה דלגלגים משתמשים בהם? (נורות שנדלקות לפחות פעם אחת, ואפשר גם נורה שתמיד כבויה בקידוד בינארי)
- `binary / Gray: 2     one-hot: one per state`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 3**

- איזה קידוד? בגריי רק ביט אחד משתנה בכל מעבר.
- `binary = all down     one-hot = SW0     Gray = SW1`

## נושא 2 - בקר הרמזור מההרצאה

30 דקות, 5 שאלות: Q09-Q13

### Q09 - בקר הרמזור

- **מתגים ונורות:** `TA, TB = SW9, SW8 (in some order)     lights = LEDG7..5, LEDG2..0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח בקר הרמזור מההרצאה. חיישני התנועה על המתגים, והרמזורים בנורות:
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא
- `TA`
- (כשהוא למעלה, הירוק של הרחוב הראשון נשאר)?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- כמה לחיצות נמשך הצהוב?
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q10 - מצב ההתחלה של הרמזור

- **מתגים ונורות:** `TA, TB = SW9, SW8 (in some order)     lights = LEDG7..5, LEDG2..0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח בקר הרמזור, אבל מצב האיפוס (העיגול הכפול) שונה אולי.
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אפסו. איזה רחוב ירוק?
- `A = all down     B = SW0`

**שלב 2**

- איזה מתג הוא
- `TA`
- `?`
- `SW9 = all down     SW8 = SW0`

### Q11 - קידוד הצבעים

- **מתגים ונורות:** `TA = SW9     TB = SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0     clock = KEY1     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח בקר הרמזור, והרמזורים מוצגים בשני ביטים כל אחד:
- `LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `TA = SW9     TB = SW8`
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אחרי איפוס הרחוב הראשון ירוק. מה הקוד של ירוק?
- `SW1 SW0`

**שלב 2**

- מה הקוד של אדום?
- `SW1 SW0`

**שלב 3**

- ומה הקוד של צהוב?
- `SW1 SW0`

### Q12 - קידוד אחד-חם של הרמזור

- **מתגים ונורות:** `TA = SW9     TB = SW8     the one-hot state bits = LEDG3..LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח בקר הרמזור בקידוד אחד-חם: ביט אחד לכל מצב, ותמיד בדיוק אחד דולק.
- `TA = SW9     TB = SW8`
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזו נורה היא
- `S0`
- (אחרי איפוס)?
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 2**

- איזו נורה היא
- `S1`
- `?`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 3**

- איזו נורה היא
- `S2`
- `?`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

### Q13 - מעבר שגוי ברמזור

- **מתגים ונורות:** `TA = SW9     TB = SW8     lights = LEDG7..5, LEDG2..0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח בקר הרמזור, אבל מעבר אחד שונה מהשקופית:
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- `TA = SW9     TB = SW8`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מאיזה מצב יוצא המעבר השגוי?
- `S0: A green     S1: A yellow     S2: B green     S3: B yellow`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

## נושא 3 - מכונות מצבים בקוד וגלאי רצף

30 דקות, 7 שאלות: Q14-Q20

### Q14 - גלאי רצף

- **מתגים ונורות:** `a = SW9 (HEX3)     smile = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח גלאי רצף: הנורה נדלקת כשנכנס רצף מסוים של 3 ביטים (ביט אחד בכל לחיצה).
- `a = SW9     smile = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- האם הנורה יכולה להשתנות כשמזיזים את המתג בלי ללחוץ?
- `Moore (no) = all down     Mealy (yes) = SW0`

**שלב 2**

- מה הרצף? (אחרי איפוס המכונה כאילו ראתה אפסים)
- `SW2 = first bit     SW1 = second     SW0 = last`

### Q15 - מור ומילי זה ליד זה

- **מתגים ונורות:** `a = SW9 (HEX3)     two detectors = LEDG1 LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח שני גלאים של אותו רצף של 2 ביטים: אחד מור ואחד מילי.
- `a = SW9     LEDG1 LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזו נורה היא גלאי המילי (מגיבה לכניסה עוד לפני הלחיצה)?
- `LEDG0 = all down     LEDG1 = SW0`

**שלב 2**

- מה הרצף?
- `SW1 = first bit     SW0 = second bit`

### Q16 - רצף חופף או לא?

- **מתגים ונורות:** `a = SW9 (HEX3)     smile = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח גלאי מור של רצף של 2 ביטים.
- `a = SW9     smile = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- מה הרצף?
- `SW1 = first bit     SW0 = second bit`

**שלב 2**

- השאירו את הכניסה כך שהרצף חוזר שוב ושוב (למשל 1111 בשביל 11). האם הנורה נדלקת שוב מיד (חופף)?
- `overlapping: 1111 -> hit, hit, hit     not overlapping: hit, -, hit`
- חופף - הרימו:
- `SW0`
- לא חופף - השאירו למטה.

### Q17 - טבלת יציאות של מכונת מילי

- **מתגים ונורות:** `a = SW9 (HEX3)     S = LEDG1     y = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח מכונת מילי של שני מצבים: המצב בנורה אחת, היציאה בשנייה.
- `a = SW9     S = LEDG1     y = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לכל מצב וכניסה: מתי
- `y = 1`
- ? הרימו את המתג שלו:
- `S=0 a=0 -> SW0     S=0 a=1 -> SW1     S=1 a=0 -> SW2     S=1 a=1 -> SW3`

### Q18 - קידוד של enum

- **מתגים ונורות:** `the state bits = LEDG1 LEDG0     clock = KEY1, reset = KEY0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח המחלק ב-3 מהשקופית. ביטי המצב מוצגים:
- `S0 -> S1 -> S2 -> S0     the state bits = LEDG1 LEDG0`
- `typedef enum logic [1:0] {?, ?, ?} statetype;     (the first name = 00, the second = 01, the third = 10)`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אפסו. מה הקוד של
- `S0`
- `?`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- מה הקוד של
- `S1`
- `?`
- `SW1 SW0`

**שלב 3**

- ומה הקוד של
- `S2`
- `?`
- `SW1 SW0`

### Q19 - שורה שגויה במכונת המצבים

- **מתגים ונורות:** `the state = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מחלק כמו בשקופית, והמצב מוצג בתצוגה. אבל באחת השורות של
- `S0 -> S1 -> ... -> S0     case (state)`
- המצב הבא שגוי.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה מצבים יש בקוד? (המספר הגדול שמופיע ועוד 1)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- מאיזה מצב יש מעבר שגוי?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 3**

- ולאיזה מצב הוא הולך במקום?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q20 - מונה למעלה ולמטה

- **מתגים ונורות:** `up, down = SW9, SW8 (in some order)     count = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכונה שסופרת: מתג אחד סופר למעלה ואחד למטה (בכל לחיצה). המספר בתצוגה.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג סופר למעלה?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- כמה מצבים יש? (אחרי המספר הגדול הוא חוזר ל-0)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

