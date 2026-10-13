# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - מכונות מצבים: מצבים, מעברים ויציאות

40 דקות, 17 שאלות: Q01-Q17

### Q01 - המחלק ב-3 מהשקופית

- **מתגים ונורות:** `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0     HEX1 = the state to set     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- המחלק ב-3 של שקופית 21. בלוח לוגיקת המצב הבא והיציאה שלו.
- `S0 -> S1 -> S2 -> S0     q = 1 in S0`
- `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0`
- `HEX1 = the state to set`
- הציבו במתגים את המצב שבתצוגה. מה המצב הבא?
- `S0 = all down     S1 = SW0     S2 = SW1`

**שלב 2**

- התחילו במצב שבתצוגה. אחרי כמה שעונים
- `q`
- נדלקת?
- שעון אחד = להציב במתגי המצב את המצב הבא.
- `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0`
- `HEX1 = the state to set`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q02 - בינארי ואחד-חם מהשקופית

- **מתגים ונורות:** `binary code = SW9 SW8     one-hot code = LEDG3 LEDG2 LEDG1 LEDG0     HEX3 HEX2 HEX1 HEX0 = a one-hot code     answer: SW1 SW0`
- **שלבים:** 1

**שלב 1**

- קידוד מצבים של שקופית 17: בבינארי 2 ביטים, באחד-חם ביט לכל מצב.
- `S0 = 00 / 0001     S1 = 01 / 0010     S2 = 10 / 0100     S3 = 11 / 1000`
- בלוח ממיר מקוד בינארי לקוד אחד-חם.
- `binary code = SW9 SW8     one-hot code = LEDG3 LEDG2 LEDG1 LEDG0`
- `HEX3 HEX2 HEX1 HEX0 = a one-hot code`
- מצאו את הקוד הבינארי שנותן בנורות את הקוד שבתצוגה.
- `SW1 SW0 = the binary code`

### Q03 - המחלק ב-3 אחרי כמה שעונים

- **מתגים ונורות:** `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0     HEX1 = the number of clocks     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- המחלק ב-3 של שקופית 21. בלוח לוגיקת המצב הבא והיציאה שלו.
- `S0 -> S1 -> S2 -> S0     q = 1 in S0`
- `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0`
- `HEX1 = the number of clocks`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0 ותנו את מספר השעונים שבתצוגה. באיזה מצב אתם?
- `S0 = all down     S1 = SW0     S2 = SW1`

**שלב 2**

- האם היציאה
- `q`
- דולקת במצב הזה?
- `S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0`
- `HEX1 = the number of clocks`
- דולקת - הרימו:
- `SW0`
- כבויה - השאירו למטה.

### Q04 - המחלק ב-3 והאיפוס

- **מתגים ונורות:** `state bits = SW9 SW8     reset = SW7     q = LEDG2     next state bits = LEDG1 LEDG0     the state to set = HEX3     reset = HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- המחלק ב-3 של שקופיות 21-22, עם האיפוס. בלוח לוגיקת המצב הבא והיציאה שלו.
- `if (reset) state <= S0;     S0 -> S1 -> S2 -> S0     q = 1 in S0`
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     reset = SW7     q = LEDG2     next state bits = LEDG1 LEDG0`
- `the state to set = HEX3     reset = HEX0`
- הציבו במתגים את מה שבתצוגה.
- האם היציאה
- `q`
- דולקת?
- דולקת - הרימו:
- `SW0`
- כבויה - השאירו למטה.

**שלב 2**

- מה המצב הבא?
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     reset = SW7     q = LEDG2     next state bits = LEDG1 LEDG0`
- `the state to set = HEX3     reset = HEX0`
- `SW1 SW0 = next state bits`

### Q05 - משוואה של המחלק ב-3

- **מתגים ונורות:** `S1 S0 = SW9 SW8     q = LEDG2     S'1 = LEDG1     S'0 = LEDG0     HEX0 = the LED to study (LEDG0, LEDG1 or LEDG2)     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- שלבי התכנון של שקופית 5 על המחלק ב-3 של שקופיות 21-22: מהטבלה המקודדת למשוואה.
- `S0 = 00     S1 = 01     S2 = 10     11 = default -> S0`
- `S1 S0 = SW9 SW8     q = LEDG2     S'1 = LEDG1     S'0 = LEDG0`
- `HEX0 = the LED to study (LEDG0, LEDG1 or LEDG2)`
- הציבו כל קוד. בכל קוד שבו הנורה שבתצוגה דולקת, הרימו את המתג שלו:
- `S1 S0 = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

**שלב 2**

- מה המשוואה של הנורה הזאת?
- `S1 S0 = SW9 SW8     q = LEDG2     S'1 = LEDG1     S'0 = LEDG0`
- `HEX0 = the LED to study (LEDG0, LEDG1 or LEDG2)`
- `LED = ?`
- `~S1 & S0 = all down     ~S1 & ~S0 = SW0     S1 & ~S0 = SW1     S1 ^ S0 = SW1+SW0`

### Q06 - כמה דלגלגים?

- **מתגים ונורות:** `the number of states = HEX1 HEX0     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מספר המצבים של מכונה. כמה דלגלגים צריך בקידוד אחד-חם (ביט לכל מצב)?
- `16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- וכמה בקידוד בינארי?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q07 - מחלק ב-N

- **מתגים ונורות:** `S = SW9 SW8 SW7 SW6   (HEX3)     next state = HEX0     q = LEDG0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של מחלק תדר, בלי כניסות: המצב הנוכחי על המתגים, המצב הבא בתצוגה.
- `S = SW9 SW8 SW7 SW6   (HEX3)     next state = HEX0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0. אחרי כמה שעונים חוזרים ל-0?
- `divide by N:   N = ?`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- באיזה מצב היציאה דולקת? (זה גם מספר השעונים ממצב 0 עד שהיא נדלקת)
- `S = SW9 SW8 SW7 SW6   (HEX3)     q = LEDG0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 3**

- כמה דלגלגים צריך לפחות לקידוד בינארי של המצבים?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q08 - שובל ומחזור

- **מתגים ונורות:** `S = SW9 SW8 SW7   (HEX3)     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של מכונה בלי כניסות: המצב הנוכחי על המתגים, המצב הבא בתצוגה.
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0 ועקבו הרבה שעונים. כמה מצבים שונים אתם פוגשים (כולל 0)?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 2**

- כמה מהם מופיעים רק פעם אחת (לא חוזרים)?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 3**

- האחרים חוזרים במחזור. כל כמה שעונים המחזור חוזר?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

### Q09 - טבלת מעברים של שני מצבים

- **מתגים ונורות:** `S = SW9     a = SW8     next state = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של מכונה עם שני מצבים: המצב והכניסה על המתגים, המצב הבא בנורה.
- `S = SW9     a = SW8     next state = LEDG0`
- לכל מצב ולכל ערך של הכניסה: מה המצב הבא? מצב 1 - הרימו:
- `S=0 a=0 -> SW3     S=0 a=1 -> SW2     S=1 a=0 -> SW1     S=1 a=1 -> SW0`

**שלב 2**

- בכמה מארבעת המקרים המכונה נשארת באותו מצב?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q10 - משוואת המצב הבא

- **מתגים ונורות:** `S = SW9     a = SW8     next state = LEDG0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של מכונה עם שני מצבים: המצב והכניסה על המתגים, המצב הבא בנורה.
- `S = SW9     a = SW8     next state = LEDG0`
- מה המצב הבא ממצב 0? מצב 1 - הרימו:
- `S=0 a=0 -> SW1     S=0 a=1 -> SW0`

**שלב 2**

- ומה המצב הבא ממצב 1? מצב 1 - הרימו:
- `S = SW9     a = SW8     next state = LEDG0`
- `S=1 a=0 -> SW1     S=1 a=1 -> SW0`

**שלב 3**

- מה משוואת המצב הבא?
- `S = SW9     a = SW8     next state = LEDG0`
- `S' = ?`
- `a = all down     ~a = SW0     S ^ a = SW1     ~(S ^ a) = SW1+SW0`
- `~S = SW2     S | a = SW2+SW0     ~S & a = SW2+SW1     S | ~a = SW2+SW1+SW0`

### Q11 - טבלת יציאות של מכונת מור

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     Y1 Y0 = LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת היציאה של מכונת מור עם 4 מצבים: המצב על המתגים, היציאות בנורות.
- `S1 S0 = SW9 SW8   (HEX3)     Y1 Y0 = LEDG1 LEDG0`
- בכל מצב שבו
- `Y0 = 1`
- הרימו את המתג שלו:
- `S = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

**שלב 2**

- אותו דבר בשביל
- `Y1 = 1`
- `S1 S0 = SW9 SW8   (HEX3)     Y1 Y0 = LEDG1 LEDG0`
- `S = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

### Q12 - מור או מילי?

- **מתגים ונורות:** `S = SW9 SW8 SW7   (HEX3)     a = SW6     y = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת היציאה של מכונה עם 8 מצבים: המצב והכניסה על המתגים, היציאה בנורה.
- `S = SW9 SW8 SW7   (HEX3)     a = SW6     y = LEDG0`
- במור היציאה תלויה רק במצב. במילי - גם בכניסה.
- הציבו כמה מצבים, ובכל אחד הזיזו רק את הכניסה. איזו מכונה?
- `Moore = all down     Mealy = SW0`

**שלב 2**

- בכמה מצבים היציאה תלויה בכניסה?
- `S = SW9 SW8 SW7   (HEX3)     a = SW6     y = LEDG0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

### Q13 - דיאגרמת מצבים של 4 מצבים

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 4

**שלב 1**

- בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה. ציירו את הדיאגרמה.
- `S = 0:   SW9 SW8 = 00`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 2**

- המצב הבא בדיאגרמה:
- `S = 1:   SW9 SW8 = 01`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 3**

- המצב הבא בדיאגרמה:
- `S = 2:   SW9 SW8 = 10`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 4**

- המצב הבא בדיאגרמה:
- `S = 3:   SW9 SW8 = 11`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- לאן עוברים ממנו כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

### Q14 - הדרך הקצרה ביותר

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- מה המספר הקטן ביותר של שעונים שמביא ממצב 0 למצב 3?
- `S = 0 -> S = 3`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q15 - מצב שאי אפשר להגיע אליו

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.
- `S = 0:   SW9 SW8 = 00`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- לאן עוברים ממצב 0 כש-
- `a = 0`
- ולאן כש-
- `a = 1`
- `?`
- `SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)`

**שלב 2**

- לאחד המצבים אין דרך להגיע ממצב 0 (מצב האיפוס), מה שלא תעשו. איזה?
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

### Q16 - מצב מלכודת

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- באחד המצבים המכונה נתקעת: אף ערך של הכניסה לא מוציא ממנו. איזה?
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

**שלב 2**

- בכמה מהמצבים האחרים יש חץ לעצמו (לפחות ערך אחד של הכניסה משאיר במקום)?
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q17 - קידוד מצבים

- **מתגים ונורות:** `state bits = SW9 SW8 SW7 SW6     next state bits = LEDG3 LEDG2 LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח לוגיקת המצב הבא של מכונה בלי כניסות. ביטי המצב על המתגים, ביטי המצב הבא בנורות (באותו סדר).
- `state bits = SW9 SW8 SW7 SW6     next state bits = LEDG3 LEDG2 LEDG1 LEDG0`
- התחילו מכל המתגים למטה, ובכל פעם העתיקו את הנורות למתגים. כמה קודים שונים יש במחזור?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- כמה ביטים משתנים לפחות פעם אחת במחזור (כמה דלגלגים באמת בשימוש)?
- `state bits = SW9 SW8 SW7 SW6     next state bits = LEDG3 LEDG2 LEDG1 LEDG0`
- `binary / Gray: 2     one-hot: one per state`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 3**

- איזה קידוד? באחד-חם ביט אחד דולק, בגריי רק ביט אחד משתנה בכל מעבר.
- `binary = all down     one-hot = SW0     Gray = SW1`

## נושא 2 - בקר הרמזור מההרצאה

40 דקות, 15 שאלות: Q18-Q32

### Q18 - טבלת המעברים של הרמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     S'1 S'0 = LEDG1 LEDG0     the state to set = HEX3     TA = HEX1     TB = HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור, טבלת המעברים המקודדת של שקופיות 11-12. בלוח לוגיקת המצב הבא שלו.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     S'1 S'0 = LEDG1 LEDG0`
- `the state to set = HEX3     TA = HEX1     TB = HEX0`
- הציבו במתגים את מה שבתצוגה.
- מה המצב הבא?
- `SW1 SW0 = S'1 S'0`

**שלב 2**

- האם המכונה נשארת באותו מצב (חץ לעצמו)?
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     S'1 S'0 = LEDG1 LEDG0`
- `the state to set = HEX3     TA = HEX1     TB = HEX0`
- נשארת - הרימו:
- `SW0`
- עוברת - השאירו למטה.

### Q19 - טבלת היציאות של הרמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0     HEX3 = the state to set     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור, טבלת היציאות של שקופית 13. בלוח לוגיקת היציאה שלו, וכל רמזור בשני ביטים.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `green = 00     yellow = 01     red = 10`
- `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `HEX3 = the state to set`
- הציבו במתגים את המצב שבתצוגה. מה הצבע של הרחוב הראשון?
- `LA = ?`
- `green = all down     yellow = SW0     red = SW1`

**שלב 2**

- ומה הצבע של הרחוב השני באותו מצב?
- `green = 00     yellow = 01     red = 10`
- `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `HEX3 = the state to set`
- `LB = ?`
- `green = all down     yellow = SW0     red = SW1`

### Q20 - הרמזור באחד-חם מהשקופית

- **מתגים ונורות:** `S3 S2 S1 S0 = SW9 SW8 SW7 SW6   (one-hot)     TA = SW5     TB = SW4     S'3 S'2 S'1 S'0 = LEDG3 LEDG2 LEDG1 LEDG0     the state to set = HEX3     TA = HEX1     TB = HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור בקידוד אחד-חם, הטבלה של שקופית 18. בלוח לוגיקת המצב הבא שלו.
- `S0 = 0001     S1 = 0010     S2 = 0100     S3 = 1000`
- `S3 S2 S1 S0 = SW9 SW8 SW7 SW6   (one-hot)     TA = SW5     TB = SW4     S'3 S'2 S'1 S'0 = LEDG3 LEDG2 LEDG1 LEDG0`
- `the state to set = HEX3     TA = HEX1     TB = HEX0`
- הציבו במתגים את מה שבתצוגה.
- מה המצב הבא?
- `SW3 SW2 SW1 SW0 = S'3 S'2 S'1 S'0`

**שלב 2**

- איזה מצב זה?
- `S0 = 0001     S1 = 0010     S2 = 0100     S3 = 1000`
- `S3 S2 S1 S0 = SW9 SW8 SW7 SW6   (one-hot)     TA = SW5     TB = SW4     S'3 S'2 S'1 S'0 = LEDG3 LEDG2 LEDG1 LEDG0`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

### Q21 - חץ לעצמו בדיאגרמת הרמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0     HEX3 = the state to set     lights = LEDG7..5, LEDG2..0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור, דיאגרמת המעברים של שקופית 10. בלוח לוגיקת המצב הבא שלו.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0`
- `HEX3 = the state to set`
- הציבו במתגים את מה שבתצוגה.
- שני החיישנים למטה. מה המצב הבא?
- `TA = 0     TB = 0`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

**שלב 2**

- באותו מצב: הרימו כל חיישן לבד. איזה חיישן משאיר את המכונה במקום (חץ לעצמו)?
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0`
- `HEX3 = the state to set`
- `none = all down     TA = SW0     TB = SW1`

### Q22 - משוואת יציאה מהשקופית

- **מתגים ונורות:** `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0     HEX1 = the street (A or b)     HEX0 = the bit (1 or 0)     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור, טבלת היציאות ומשוואות היציאה של שקופיות 13-14. בלוח לוגיקת היציאה שלו.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `green = 00     yellow = 01     red = 10`
- `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `HEX1 = the street (A or b)     HEX0 = the bit (1 or 0)`
- הציבו כל מצב. בכל מצב שבו הביט שבתצוגה דולק, הרימו את המתג שלו:
- `S1 S0 = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3`

**שלב 2**

- מה המשוואה של הביט הזה?
- `S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `HEX1 = the street (A or b)     HEX0 = the bit (1 or 0)`
- `bit = ?`
- `S1 = all down     ~S1 = SW0     ~S1 & S0 = SW1     S1 & S0 = SW1+SW0`

### Q23 - שני שעונים ברמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX2     the start state = HEX3     TA = HEX1     TB = HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור, דיאגרמת הזמנים של שקופיות 15-16. בלוח לוגיקת המצב הבא שלו.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX2`
- `the start state = HEX3     TA = HEX1     TB = HEX0`
- הציבו במתגים את מה שבתצוגה.
- החיישנים לא משתנים. באיזה מצב תהיו אחרי שעון אחד?
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

**שלב 2**

- ואחרי שעון נוסף?
- שעון אחד = להציב במתגי המצב את המצב הבא.
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX2`
- `the start state = HEX3     TA = HEX1     TB = HEX0`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

### Q24 - מתי יהיה ירוק?

- **מתגים ונורות:** `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0     HEX3 = the start state     HEX1 = the street (A or b)     lights = LEDG7..5, LEDG2..0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בקר הרמזור של שקופיות 8-10. בלוח לוגיקת המצב הבא והיציאות שלו.
- `S0 = 00     S1 = 01     S2 = 10     S3 = 11`
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0`
- `HEX3 = the start state     HEX1 = the street (A or b)`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- הציבו את מצב ההתחלה. מה הצבע עכשיו של הרחוב שבתצוגה?
- `green = all down     yellow = SW0     red = SW1`

**שלב 2**

- שני החיישנים למטה. אחרי כמה שעונים הרחוב שבתצוגה ירוק?
- שעון אחד = להציב במתגי המצב את המצב הבא.
- `S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0`
- `HEX3 = the start state     HEX1 = the street (A or b)`
- `TA = 0     TB = 0`
- `0 = green now = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q25 - בקר הרמזור

- **מתגים ונורות:** `S = SW9 SW8 SW7   (HEX3)     next state = HEX0     TA, TB = SW6, SW5 (in some order)     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של בקר הרמזור מההרצאה, עם כמה מצבים לצהוב: המצב והחיישנים על המתגים, המצב הבא בתצוגה.
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `TA, TB = SW6, SW5   (in some order)`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- במצב 0 הרחוב הראשון ירוק. איזה מתג הוא
- `TA`
- ? (כשהוא למעלה, המצב הבא נשאר 0)
- `SW6 = all down     SW5 = SW0`

**שלב 2**

- שני החיישנים למטה. התחילו במצב 0 ועקבו אחרי המצב הבא.
- שעון אחד = להציב במתגי המצב את המצב הבא.
- כמה שעונים הצהוב של הרחוב הראשון דולק?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `SW6 = 0     SW5 = 0     LA yellow = LEDG6`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q26 - מחזור שלם של הרמזור

- **מתגים ונורות:** `S = SW9 SW8 SW7   (HEX3)     next state = HEX0     TA = SW6     TB = SW5     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0`
- **שלבים:** 4

**שלב 1**

- בלוח הלוגיקה של בקר הרמזור, אבל הצהוב של כל רחוב נמשך זמן אחר. המצב והחיישנים על המתגים, המצב הבא בתצוגה.
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `TA = SW6     TB = SW5`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- שני החיישנים למטה. התחילו במצב 0. כמה שעונים הצהוב של הרחוב הראשון דולק?
- `LA yellow = LEDG6`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 2**

- כמה שעונים הצהוב של הרחוב השני דולק?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `SW6 = 0     SW5 = 0     LB yellow = LEDG1`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 3**

- כמה שעונים נמשך מחזור שלם, ממצב 0 עד שחוזרים אליו?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `SW6 = 0     SW5 = 0`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 4**

- כל שעון במחזור הוא מצב אחר. כמה דלגלגים צריך לפחות בקידוד בינארי?
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q27 - מצב האיפוס של הרמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0     TA, TB = SW7, SW6 (in some order)     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של בקר הרמזור, אבל הקידוד של המצבים אולי שונה מהשקופית.
- אחרי איפוס אוגר המצב מכיל 00. מה מראה אז הרמזור של הרחוב הראשון?
- `S1 S0 = SW9 SW8 = 00`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `green = all down     yellow = SW0     red = SW1`

**שלב 2**

- מצאו את המצב שבו הרחוב הראשון ירוק. איזה מתג הוא
- `TA`
- ? (כשהוא למעלה, המצב הבא לא משתנה)
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `TA, TB = SW7, SW6   (in some order)`
- `LA green = LEDG7`
- `SW7 = all down     SW6 = SW0`

### Q28 - חיישן פעיל בנמוך

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0     TA = SW7     TB = SW6     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של בקר הרמזור. כל חיישן אולי הפוך: יש תנועה כשהמתג למטה.
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `TA = SW7     TB = SW6`
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- במצב 0: באיזה מצב של המתג יש תנועה ברחוב הראשון (המצב הבא נשאר 0)?
- `S = 0     TA = SW7`
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

**שלב 2**

- במצב 2: באיזה מצב של המתג יש תנועה ברחוב השני (המצב הבא נשאר 2)?
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `S = 2     TB = SW6`
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

**שלב 3**

- שני המתגים למטה. התחילו במצב 0 ועקבו אחרי המצב הבא. מה קורה?
- שעון אחד = להציב במתגי המצב את המצב הבא.
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `SW7 = 0     SW6 = 0`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- `A green forever = all down     B green forever = SW0     full cycle = SW1`

### Q29 - קידוד הצבעים

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח לוגיקת היציאה של בקר הרמזור: המצב על המתגים, וכל רמזור בשני ביטים.
- `S1 S0 = SW9 SW8   (HEX3)     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `S0: LA green, LB red`
- במצב 0 הרחוב הראשון ירוק. מה הקוד של ירוק?
- `S = 0     SW1 SW0 = LA1 LA0`

**שלב 2**

- ובמצב 0 הרחוב השני אדום. מה הקוד של אדום?
- `S1 S0 = SW9 SW8   (HEX3)     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `S = 0     SW1 SW0 = LB1 LB0`

**שלב 3**

- במצב 1 הרחוב הראשון צהוב. מה הקוד של צהוב?
- `S1 S0 = SW9 SW8   (HEX3)     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0`
- `S1: LA yellow     S = 1     SW1 SW0 = LA1 LA0`

### Q30 - משוואת יציאה של הרמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח לוגיקת היציאה של בקר הרמזור בקידוד בינארי, אבל לא בקידוד של השקופית. קוד המצב על המתגים.
- `S1 S0 = SW9 SW8   (HEX3)`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `LB:  green = LEDG2   yellow = LEDG1   red = LEDG0`
- מה הקוד של
- `S0`
- (הרחוב הראשון ירוק)?
- `SW1 SW0 = S1 S0`

**שלב 2**

- מה הקוד של
- `S2`
- (הרחוב השני ירוק)?
- `S1 S0 = SW9 SW8   (HEX3)`
- `LB green = LEDG2`
- `SW1 SW0 = S1 S0`

**שלב 3**

- הרמזור של הרחוב הראשון אדום בדיוק בשני מצבים. מה משוואת היציאה שלו?
- `S1 S0 = SW9 SW8   (HEX3)`
- `LA red = LEDG5`
- `LA red = ?`
- `S1 = all down     ~S1 = SW0     S0 = SW1`
- `~S0 = SW1+SW0     S1 ^ S0 = SW2     ~(S1 ^ S0) = SW2+SW0`

### Q31 - קידוד אחד-חם של הרמזור

- **מתגים ונורות:** `state bits = SW9 SW8 SW7 SW6   (one-hot)     next state bits = LEDG3 LEDG2 LEDG1 LEDG0     TA = SW5     TB = SW4     LA:  green = LEDG7   yellow = LEDG6   red = LEDG5     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של בקר הרמזור בקידוד אחד-חם: ביט לכל מצב, ובדיוק אחד למעלה. סדר הביטים נסתר.
- `state bits = SW9 SW8 SW7 SW6   (one-hot)     next state bits = LEDG3 LEDG2 LEDG1 LEDG0`
- `TA = SW5     TB = SW4`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- איזה מתג הוא
- `S0`
- ? (כשרק הוא למעלה, הרחוב הראשון ירוק)
- `SW6 = all down     SW7 = SW0     SW8 = SW1     SW9 = SW1+SW0`

**שלב 2**

- איזה מתג הוא
- `S1`
- ? (הרחוב הראשון צהוב)
- `state bits = SW9 SW8 SW7 SW6   (one-hot)     next state bits = LEDG3 LEDG2 LEDG1 LEDG0`
- `TA = SW5     TB = SW4`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `SW6 = all down     SW7 = SW0     SW8 = SW1     SW9 = SW1+SW0`

**שלב 3**

- איזה מתג הוא
- `S2`
- ? (הרחוב הראשון אדום, וכש-
- `TB = 1`
- המצב הבא לא משתנה)
- `state bits = SW9 SW8 SW7 SW6   (one-hot)     next state bits = LEDG3 LEDG2 LEDG1 LEDG0`
- `TA = SW5     TB = SW4`
- `LA:  green = LEDG7   yellow = LEDG6   red = LEDG5`
- `SW6 = all down     SW7 = SW0     SW8 = SW1     SW9 = SW1+SW0`

### Q32 - מעבר שגוי ברמזור

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0     TA = SW7     TB = SW6     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת המצב הבא של בקר הרמזור, אבל מעבר אחד שונה מהשקופית:
- `S0: TA -> S0, else S1`
- `S1 -> S2`
- `S2: TB -> S2, else S3`
- `S3 -> S0`
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `TA = SW7     TB = SW6`
- מאיזה מצב יוצא המעבר השגוי?
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

**שלב 2**

- ולאיזה מצב הוא הולך במקום?
- `S1 S0 = SW9 SW8   (HEX3)     next state = HEX0`
- `TA = SW7     TB = SW6`
- `S0 = all down     S1 = SW0     S2 = SW1     S3 = SW1+SW0`

## נושא 3 - מכונות מצבים בקוד וגלאי רצף

40 דקות, 18 שאלות: Q33-Q50

### Q33 - גלאי המור מהשקופית

- **מתגים ונורות:** `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0     the state to set = HEX3     a = HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- גלאי הרצף של מור בקוד של שקופית 24. בלוח הלוגיקה שלו.
- `typedef enum logic [1:0] {S0, S1, S2}     assign smile = (state == S2);`
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `the state to set = HEX3     a = HEX0`
- הציבו במתגים את מה שבתצוגה.
- האם החיוך דולק?
- דולק - הרימו:
- `SW0`
- כבוי - השאירו למטה.

**שלב 2**

- מה המצב הבא?
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `the state to set = HEX3     a = HEX0`
- `S0 = all down     S1 = SW0     S2 = SW1`

### Q34 - גלאי המילי מהשקופית

- **מתגים ונורות:** `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0     the state to set = HEX3     a = HEX0     answer: SW0`
- **שלבים:** 2

**שלב 1**

- גלאי הרצף של מילי בקוד של שקופית 26. בלוח הלוגיקה שלו.
- `typedef enum logic {S0, S1}     S0 = 0     S1 = 1`
- `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0`
- `the state to set = HEX3     a = HEX0`
- הציבו במתגים את מה שבתצוגה.
- האם החיוך דולק?
- דולק - הרימו:
- `SW0`
- כבוי - השאירו למטה.

**שלב 2**

- מה המצב הבא?
- `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0`
- `the state to set = HEX3     a = HEX0`
- `S0 = all down     S1 = SW0`

### Q35 - ה-case של המחלק ב-3

- **מתגים ונורות:** `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0     HEX3 HEX2 = the state bits to set     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- המחלק ב-3 בקוד של שקופית 22. בלוח לוגיקת המצב הבא והיציאה שלו.
- `typedef enum logic [1:0] {S0, S1, S2}     S0: nextstate = S1;   S1: nextstate = S2;   S2: nextstate = S0;   default: nextstate = S0;`
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- `HEX3 HEX2 = the state bits to set`
- איזו שורה של ה-
- `case`
- מתבצעת בקוד שבתצוגה?
- `S0 = all down     S1 = SW0     S2 = SW1     default = SW1+SW0`

**שלב 2**

- הציבו את הקוד במתגים. מה המצב הבא?
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- `HEX3 HEX2 = the state bits to set`
- `SW1 SW0 = next state bits`

### Q36 - מתי גלאי המור נשאר במקום?

- **מתגים ונורות:** `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0     HEX3 = the state to set     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- גלאי הרצף של מור בקוד של שקופית 24. בלוח הלוגיקה שלו.
- `S0: if (a) S0 else S1     S1: if (a) S2 else S1     S2: if (a) S0 else S1`
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `HEX3 = the state to set`
- הציבו במתגים את מה שבתצוגה.
- האם החיוך דולק?
- דולק - הרימו:
- `SW0`
- כבוי - השאירו למטה.

**שלב 2**

- הזיזו רק את הכניסה. באיזה ערך שלה המצב הבא שווה למצב הנוכחי?
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `HEX3 = the state to set`
- `none = all down     a=0 = SW0     a=1 = SW1`

### Q37 - ארבעה ביטים לגלאי המור

- **מתגים ונורות:** `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0     the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- גלאי הרצף של מור של שקופיות 23-24. בלוח הלוגיקה שלו.
- `S0 = 00     S1 = 01     S2 = 10`
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0 והכניסו את הביטים שבתצוגה, ביט בכל שעון. באיזה מצב אתם בסוף?
- `S0 = all down     S1 = SW0     S2 = SW1`

**שלב 2**

- אחרי כמה מארבעת השעונים החיוך דלק?
- `state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0`
- `the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)`
- `0 = all down`
- `1 = SW0 2 = SW1`

### Q38 - ארבעה ביטים לגלאי המילי

- **מתגים ונורות:** `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0     the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- גלאי הרצף של מילי של שקופיות 25-26. בלוח הלוגיקה שלו.
- `S0 = 0     S1 = 1`
- `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0`
- `the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0. בכל ביט: הציבו אותו בכניסה, הסתכלו על החיוך, ואז שעון. באיזה ביט החיוך דולק לראשונה?
- `0 = never = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- בכמה מארבעת הביטים החיוך דלק?
- `state = SW9     a = SW8     smile = LEDG1     next state = LEDG0`
- `the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)`
- `0 = all down`
- `1 = SW0 2 = SW1`

### Q39 - מור ומילי של השקופיות על אותם ביטים

- **מתגים ונורות:** `Moore:  state bits = SW9 SW8     smile = LEDG7     next state bits = LEDG6 LEDG5     Mealy:  state = SW7     smile = LEDG1     next state = LEDG0     a = SW6     the input bits = HEX3 HEX2 HEX1   (HEX3 = the first)     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- שני גלאי הרצף של שקופיות 23-26, מור ומילי, על אותה כניסה. בלוח הלוגיקה של שניהם.
- `Moore:  S0 = 00     S1 = 01     S2 = 10`
- `Moore:  state bits = SW9 SW8     smile = LEDG7     next state bits = LEDG6 LEDG5`
- `Mealy:  state = SW7     smile = LEDG1     next state = LEDG0`
- `a = SW6`
- `the input bits = HEX3 HEX2 HEX1   (HEX3 = the first)`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו את שניהם במצב 0. בכל ביט: הציבו אותו בכניסה, הסתכלו, ואז שעון.
- באיזה ביט החיוך של המילי דולק לראשונה (לפני השעון)?
- `0 = never = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 2**

- ואחרי כמה שעונים החיוך של המור דולק לראשונה?
- `Moore:  state bits = SW9 SW8     smile = LEDG7     next state bits = LEDG6 LEDG5`
- `Mealy:  state = SW7     smile = LEDG1     next state = LEDG0`
- `a = SW6`
- `the input bits = HEX3 HEX2 HEX1   (HEX3 = the first)`
- `0 = never = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q40 - גלאי רצף

- **מתגים ונורות:** `S = SW9 SW8 SW7 = the last three bits (SW9 = the oldest)     a = SW6     smile = LEDG0     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת היציאה של גלאי רצף של 3 ביטים. המצב הוא שלושת הביטים האחרונים, והכניסה היא הביט הבא.
- `S = SW9 SW8 SW7 = the last three bits (SW9 = the oldest)     a = SW6     smile = LEDG0`
- הציבו כמה מצבים והזיזו רק את הכניסה. האם החיוך משתנה?
- `Moore (no) = all down     Mealy (yes) = SW0`

**שלב 2**

- מה הרצף? במור: המצב שבו החיוך דולק. במילי: שני הביטים האחרונים והכניסה.
- `S = SW9 SW8 SW7 = the last three bits (SW9 = the oldest)     a = SW6     smile = LEDG0`
- `SW2 = first bit     SW1 = second     SW0 = last`

### Q41 - כמה פעמים הגלאי מזהה?

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של גלאי מור של רצף של 3 ביטים (חופף): המצב והכניסה על המתגים, המצב הבא בתצוגה.
- החיוך דולק לפי המצב הנוכחי בלבד.
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- התחילו במצב 0, והכניסו את 5 הביטים האלה, ביט בכל שעון. כמה פעמים הגעתם למצב עם חיוך?
- `a = 1 0 0 1 0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- התחילו שוב במצב 0 והכניסו את כל 10 הביטים. כמה פעמים הגעתם למצב עם חיוך?
- `a = 1 0 0 1 0 0 1 0 1 0`
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

### Q42 - מור ומילי זה ליד זה

- **מתגים ונורות:** `S = SW9 SW8 = the last two bits (SW9 = the older)     a = SW7     LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת היציאה של שני גלאים של אותו רצף של 2 ביטים: אחד מור ואחד מילי.
- `S = SW9 SW8 = the last two bits (SW9 = the older)     a = SW7     LEDG1 LEDG0`
- איזו נורה היא גלאי המילי (משתנה כשמזיזים רק את הכניסה)?
- `LEDG0 = all down     LEDG1 = SW0`

**שלב 2**

- מה הרצף?
- `S = SW9 SW8 = the last two bits (SW9 = the older)     a = SW7     LEDG1 LEDG0`
- `SW1 = first bit     SW0 = second bit`

### Q43 - רצף חופף או לא?

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של גלאי מור של רצף של 2 ביטים: המצב והכניסה על המתגים, המצב הבא בתצוגה.
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0`
- שעון אחד = להציב במתגי המצב את המצב הבא.
- מצאו את המצב עם החיוך ואת הדרך אליו ממצב 0. מה הרצף?
- `SW1 = first bit     SW0 = second bit`

**שלב 2**

- במצב עם החיוך, הכניסו שוב את הביט של הרצף. האם המצב הבא שוב עם חיוך (חופף)?
- `S1 S0 = SW9 SW8   (HEX3)     a = SW7     next state = HEX0     smile = LEDG0`
- `overlapping: 1111 -> hit, hit, hit     not overlapping: hit, -, hit`
- חופף - הרימו:
- `SW0`
- לא חופף - השאירו למטה.

### Q44 - טבלת יציאות של מכונת מילי

- **מתגים ונורות:** `S = SW9     a = SW8     y = LEDG0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח לוגיקת היציאה של מכונת מילי עם שני מצבים: המצב והכניסה על המתגים, היציאה בנורה.
- `S = SW9     a = SW8     y = LEDG0`
- לכל מצב וכניסה: מתי
- `y = 1`
- ? הרימו את המתג שלו:
- `S=0 a=0 -> SW0     S=0 a=1 -> SW1     S=1 a=0 -> SW2     S=1 a=1 -> SW3`

### Q45 - שכחו את ברירת המחדל

- **מתגים ונורות:** `S = SW9 = the last bit     a = SW8     two Mealy detectors = LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח לוגיקת היציאה של שני גלאי מילי של אותו רצף של 2 ביטים, כמו בשקופית. באחד מהם חסרה השורה
- `smile = 1'b0;`
- בתחילת
- `always_comb`
- ולכן היציאה נשמרת (תפס).
- `S = SW9 = the last bit     a = SW8     two Mealy detectors = LEDG1 LEDG0`
- איזו נורה היא הגלאי עם הבאג (נדלקת ולא נכבית יותר)?
- `LEDG0 = all down     LEDG1 = SW0`

**שלב 2**

- מה הרצף? (לפי הגלאי התקין)
- `S = SW9 = the last bit     a = SW8     two Mealy detectors = LEDG1 LEDG0`
- `SW1 = first bit     SW0 = second bit`

### Q46 - קידוד של enum

- **מתגים ונורות:** `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של המחלק ב-3 מהשקופית: ביטי המצב על המתגים, ביטי המצב הבא בנורות.
- `S0 -> S1 -> S2 -> S0     q = 1 in S0`
- `typedef enum logic [1:0] {?, ?, ?} statetype;     (the first name = 00, the second = 01, the third = 10)`
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- מה הקוד של
- `S0`
- `?`
- `SW1 SW0`

**שלב 2**

- מה הקוד של
- `S1`
- `?`
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- `SW1 SW0`

**שלב 3**

- ומה הקוד של
- `S2`
- `?`
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- `SW1 SW0`

### Q47 - הקוד שאין לו שם

- **מתגים ונורות:** `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של המחלק ב-3 מהשקופית. לקוד 11 אין שם, ומה שקורה בו נקבע בשורה
- `default: nextstate = ?;`
- `S0 = 00     S1 = 01     S2 = 10     q = 1 in S0`
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- הציבו את הקוד 11. מה המצב הבא?
- `SW9 SW8 = 11`
- `S0 = all down     S1 = SW0     S2 = SW1     stays 11 = SW1+SW0`

**שלב 2**

- התחילו בקוד 11 ועקבו אחרי המצב הבא. אחרי כמה שעונים
- `q`
- נדלקת?
- שעון אחד = להציב במתגי המצב את המצב הבא.
- `state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0`
- `never = all down     1 = SW0     2 = SW1     3 = SW1+SW0`

### Q48 - שורה שגויה במכונת המצבים

- **מתגים ונורות:** `S = SW9 SW8 SW7   (HEX3)     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח לוגיקת המצב הבא של מחלק כמו בשקופית, אבל באחת השורות של
- `S0 -> S1 -> ... -> S0     case (state)`
- המצב הבא שגוי. לכל קוד אחר יש
- `default: nextstate = S0;`
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- כמה מצבים יש בקוד? (בין 3 ל-5: המצב הגדול שיש לו שורה משלו ועוד 1)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- מאיזה מצב יש מעבר שגוי?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 3**

- ולאיזה מצב הוא הולך במקום?
- `S = SW9 SW8 SW7   (HEX3)     next state = HEX0`
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q49 - איזה בלוק שבור?

- **מתגים ונורות:** `S1 S0 = SW9 SW8   (HEX3)     reset = SW7     next state = HEX0     q = LEDG0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח הלוגיקה של המחלק ב-3 מהשקופית, אבל אחד משלושת הבלוקים שלו שבור. המצב והאיפוס על המתגים, המצב הבא בתצוגה.
- `S1 S0 = SW9 SW8   (HEX3)     reset = SW7     next state = HEX0     q = LEDG0`
- הרימו את האיפוס. מה המצב הבא?
- `S0 = all down     S1 = SW0     S2 = SW1`

**שלב 2**

- באיזה מצב
- `q`
- דולקת?
- `S1 S0 = SW9 SW8   (HEX3)     reset = SW7     next state = HEX0     q = LEDG0`
- `S0 = all down     S1 = SW0     S2 = SW1`

**שלב 3**

- השוו לשקופית. איזה בלוק שבור?
- `S0 -> S1 -> S2 -> S0     reset -> S0     q = 1 in S0`
- `S1 S0 = SW9 SW8   (HEX3)     reset = SW7     next state = HEX0     q = LEDG0`
- `state register = all down     next state logic = SW0     output logic = SW1`

### Q50 - מונה למעלה ולמטה

- **מתגים ונורות:** `S = SW9 SW8 SW7 SW6   (HEX3)     up, down = SW5, SW4 (in some order)     next state = HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הלוגיקה של מונה: מתג אחד סופר למעלה ואחד למטה. המצב והכניסות על המתגים, המצב הבא בתצוגה.
- `S = SW9 SW8 SW7 SW6   (HEX3)     up, down = SW5, SW4 (in some order)     next state = HEX0`
- איזה מתג סופר למעלה?
- `SW5 = all down     SW4 = SW0`

**שלב 2**

- כמה מצבים יש? (ממצב 0 כלפי מטה הולכים למצב הגדול)
- `S = SW9 SW8 SW7 SW6   (HEX3)     up, down = SW5, SW4 (in some order)     next state = HEX0`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

