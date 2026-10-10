# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - נקודה קבועה ונקודה צפה

30 דקות, 12 שאלות: Q01-Q12

### Q01 - נקודה קבועה בלי סימן

- **מתגים ונורות:** `the bits = LEDG7..LEDG0     a = HEX1     b = HEX0 (the format Ua.b)     answer: SW5..SW0`
- **שלבים:** 2

**שלב 1**

- בנורות מספר בנקודה קבועה בלי סימן, ובתצוגה הפורמט:
- `Ua.b:   a = HEX1 integer bits     b = HEX0 fraction bits`
- מה החלק השלם שלו?
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- כמה שישה-עשריות יש בחלק השבור? (למשל 0.75 = 12/16)
- `fraction x 16`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q02 - נקודה קבועה עם סימן

- **מתגים ונורות:** `the bits = LEDG7..LEDG0 (Q4.4)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בנורות מספר
- `Q4.4`
- (משלים ל-2, 4 ביטים שלמים כולל הסימן, 4 שבורים).
- `LEDG7..LEDG0`
- האם הוא שלילי?
- שלילי - הרימו:
- `SW0`
- חיובי - השאירו למטה.

**שלב 2**

- מה החלק השלם של הערך המוחלט שלו? (שלילי: הפכו את כל הביטים והוסיפו 1)
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 3**

- וכמה שישה-עשריות בחלק השבור של הערך המוחלט?
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q03 - מספר נגדי בנקודה קבועה

- **מתגים ונורות:** `x = LEDG7..LEDG0 (Q4.4, positive)     answer: SW7..SW0`
- **שלבים:** 2

**שלב 1**

- בנורות מספר חיובי בפורמט
- `Q4.4`
- `x = LEDG7..LEDG0`
- שלב 1 בהיפוך הסימן: הפכו את כל הביטים שלו.
- `SW7..SW0 = not x`

**שלב 2**

- בנורות אותו מספר:
- `x = LEDG7..LEDG0     (Q4.4)`
- שלב 2: הוסיפו 1 לביט הימני. כתבו את המספר הנגדי:
- `SW7..SW0 = -x`

### Q04 - לכתוב בנקודה קבועה

- **מתגים ונורות:** `HEX3 = integer     HEX2 HEX1 = hundredths     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר עשרוני:
- `HEX3 = the integer part (hex)     HEX2 HEX1 = hundredths`
- כתבו אותו בפורמט
- `U4.4`
- `:`
- `SW7..SW4 = integer     SW3..SW0 = fraction x 16`

### Q05 - חשבון רוויה

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = B (hex)     (unsigned 4 bits)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים של 4 ביטים בלי סימן:
- `HEX3 = A (hex)     HEX2 = B (hex)     (unsigned 4 bits)`
- מה החיבור הרגיל שלהם ב-4 ביטים (הנשא נזרק)?
- `SW3..SW0`

**שלב 2**

- ומה החיבור ברוויה (אם הסכום גדול מ-15, התוצאה 15)?
- `SW3..SW0`

### Q06 - חיבור ברוויה בנקודה קבועה

- **מתגים ונורות:** `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים בנקודה קבועה בלי סימן:
- `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)`
- האם החיבור שלהם גולש (לא נכנס ב-8 ביטים)?
- גולש - הרימו:
- `SW0`
- לא גולש - השאירו למטה.

**שלב 2**

- בתצוגה אותם שני מספרים:
- `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)`
- מה החיבור ברוויה? (בגלישה התוצאה היא הערך הגדול ביותר)
- `SW7..SW0 = A + B (U4.4, saturated)`

### Q07 - לפענח מספר נקודה צפה

- **מתגים ונורות:** `the float in hex, high / low 16 bits     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 4

**שלב 1**

- בתצוגה מספר נקודה צפה של 32 ביטים, בהקס, בשני דפים:
- `page 1 (SW9 down): the high 16 bits (hex)     page 2 (SW9 up): the low 16 bits`
- `sign | biased exponent (8 bits) | fraction (23 bits)`
- מה ביט הסימן?
- 1 (שלילי) - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- מה המעריך המוטה (8 הביטים שאחרי הסימן)?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

**שלב 3**

- מה המעריך האמיתי?
- `exponent = biased - 127`
- `4 = SW2   2 = SW1   1 = SW0`

**שלב 4**

- מה החלק השלם של הערך המוחלט?
- `|value| = 1.fraction x 2^exponent`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

### Q08 - לקודד מספר בנקודה צפה

- **מתגים ונורות:** `HEX2 HEX1 HEX0 = N (decimal)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מספר שלם:
- `HEX2 HEX1 HEX0 = N (decimal)`
- בנקודה צפה הוא
- `1.f x 2^e`
- . מה המעריך המוטה?
- `biased = 127 + e`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

**שלב 2**

- מה 8 הביטים הראשונים של השבר (אחרי ה-1 שלא נכתב)?
- `SW7 = the first fraction bit`

### Q09 - מקרים מיוחדים בנקודה צפה

- **מתגים ונורות:** `the float in hex: high 16 bits / low 16 bits (SW9)     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר נקודה צפה בהקס, בשני דפים:
- `page 1 (SW9 down): the high 16 bits (hex)     page 2 (SW9 up): the low 16 bits`
- `exponent all 0 and fraction 0: zero     exponent all 1: fraction 0 = infinity, else NaN`
- מה הוא?
- `0 = all down     -0 = SW0     infinity = SW1`
- `-infinity = SW1+SW0     NaN = SW2     a normal number = SW2+SW0`

### Q10 - השוואת מספרים בנקודה צפה

- **מתגים ונורות:** `N1 / N2 high 16 bits     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- מה הסימנים שלהם?
- `N1+ N2+ = all down     N1+ N2- = SW0     N1- N2+ = SW1     N1- N2- = SW1+SW0`

**שלב 2**

- בתצוגה אותם שני מספרים:
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- למי יש מעריך מוטה גדול יותר?
- `N1 = all down     N2 = SW0     equal = SW1`

**שלב 3**

- בתצוגה אותם שני מספרים:
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- מי המספר הגדול יותר (עם הסימן)?
- `N1 = all down     N2 = SW0`

### Q11 - עיגול בנקודה צפה

- **מתגים ונורות:** `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits     answer: SW2..SW0`
- **שלבים:** 3

**שלב 1**

- בנורות מנטיסה חיובית עם 6 ביטי שבר:
- `1.f`
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר כלפי מטה. מה 3 ביטי השבר?
- `SW2..SW0`

**שלב 2**

- בנורות אותה מנטיסה:
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר כלפי מעלה:
- `SW2..SW0`

**שלב 3**

- בנורות אותה מנטיסה:
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר לקרוב ביותר:
- `SW2..SW0`

### Q12 - חיבור בנקודה צפה

- **מתגים ונורות:** `N1 / N2 high 16 bits     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- החיבור: מוציאים מעריכים, מזיזים את הקטן ימינה בהפרש. בכמה מקומות מזיזים?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- מה המעריך המוטה של הסכום (אחרי נרמול)?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

## נושא 2 - מונים ואוגרי הזזה

30 דקות, 8 שאלות: Q13-Q20

### Q13 - מחלק ב-2 בחזקת N

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q     answer: SW4..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מונה בינארי, והנורה מחוברת לאחד הביטים שלו.
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- שימו במתגים את ערכי המונה לפי הסדר: 0, 1, 2, 3, ... כל כמה ספירות הנורה משתנה?
- `1 = SW0     2 = SW1     4 = SW2     8 = SW3`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- לאיזה ביט של המונה הנורה מחוברת?
- `q[k]:   k = ?`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 3**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- המונה סופר 1 בכל עליית שעון. כמה עליות שעון נמשך מחזור שלם של הנורה (דולקת וכבויה)?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q14 - מונה עם ערך איפוס

- **מתגים ונורות:** `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מונה:
- `always_ff @(posedge clk) if (reset) q <= R; else q <= q +- 1;`
- במתגים הכניסות עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:
- `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0`
- מה ערך האיפוס?
- `R = ?     SW3..SW0`

**שלב 2**

- בלוח אותו מונה:
- `always_ff @(posedge clk) if (reset) q <= R; else q <= q +- 1;`
- `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0`
- הוא סופר למעלה או למטה?
- `up = all down     down = SW0`

### Q15 - מונה עם מחזור מוסתר

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מונה שחוזר ל-0 אחרי ערך מוסתר. במתגים הערך עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0`
- התחילו ב-0 ועקבו אחרי המונה. מה הערך הגדול ביותר שהוא מגיע אליו?
- `SW3..SW0`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0`
- כמה ערכים שונים יש במחזור שלו?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q16 - מתנד בשליטה ספרתית

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מונה של 4 ביטים שמוסיף מספר מוסתר בכל עליית שעון (במקום 1).
- במתגים הערך של המונה עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- מה המספר שהוא מוסיף?
- `p = ?     SW3..SW0`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- הוא מתחיל ב-0. אחרי כמה עליות שעון הוא חוזר ל-0 בפעם הראשונה?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q17 - אוגר הזזה

- **מתגים ונורות:** `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר הזזה של 4 ביטים עם כניסה טורית. במתגים הערך עכשיו והכניסה, ובנורות הערך אחרי עליית השעון הבאה:
- `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0`
- באיזו נורה נכנס הביט החדש?
- `LEDG0 = all down     LEDG3 = SW0`

**שלב 2**

- בלוח אותו אוגר:
- `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0`
- הביט נכנס כמו שהוא, או הפוך?
- `as is = all down     inverted = SW0`

### Q18 - אוגר הזזה כקו השהיה

- **מתגים ונורות:** `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)     LEDG0 = one output, after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר הזזה של 4 ביטים. בכל עליית שעון הכניסה הטורית נכנסת לביט הראשון והשאר זזים הלאה.
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- הנורה מחוברת לאחת היציאות, ומראה אותה אחרי עליית השעון הבאה.
- `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)`
- `LEDG0 = one output, after the next clock edge`
- את איזה ערך הנורה מעתיקה?
- `Sin = all down     Q[0] = SW0     Q[1] = SW1     Q[2] = SW1+SW0`

**שלב 2**

- בלוח אותו אוגר:
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)`
- `LEDG0 = one output, after the next clock edge`
- לאיזו יציאה מחוברת הנורה?
- `Q[k]:   k = ?`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 3**

- בלוח אותו אוגר:
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- `LEDG0 = Q[k]`
- ביט חדש נכנס ב-
- `Sin`
- . אחרי כמה עליות שעון הוא מגיע לנורה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q19 - ממקבילי לטורי

- **מתגים ונורות:** `Load = SW9     Q = SW8..SW5 (HEX3)     q after the next clock edge = LEDG3..LEDG0     Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח ממיר ממקבילי לטורי: אוגר הזזה שטוען מילה מוסתרת ומוציא אותה ביט אחרי ביט.
- במתגים הכניסות עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- מה המילה שנטענת?
- `SW3..SW0 = W`

**שלב 2**

- בלוח אותו אוגר:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- לאיזה כיוון הוא מזיז?
- `left: Sout = Q3 = all down     right: Sout = Q0 = SW0`

**שלב 3**

- בלוח אותו אוגר:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- טוענים את המילה, ואחר כך היא יוצאת ביט אחרי ביט. מה סדר היציאה?
- `SW3 = the first bit out   ...   SW0 = the last bit out`

### Q20 - אוגר הזזה עם טעינה מקבילית

- **מתגים ונורות:** `D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)     q after the next clock edge = LEDG3..LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר הזזה עם טעינה מקבילית: כש-
- `Load = 1`
- הוא טוען את הכניסה המקבילית, ואחרת הוא מזיז ומכניס את הביט הטורי.
- `Load = 1: Q <= D     Load = 0: shift in Sin`
- במתגים הערך עכשיו והכניסות, ובנורות הערך אחרי עליית השעון הבאה:
- `D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)`
- `q after the next clock edge = LEDG3..LEDG0`
- איזה מתג הוא
- `Load`
- `?`
- `SW5 = all down     SW4 = SW0`

**שלב 2**

- בלוח אותו אוגר:
- `D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)`
- `q after the next clock edge = LEDG3..LEDG0`
- לאיזה כיוון הוא מזיז?
- `left (into LEDG0) = all down     right (into LEDG3) = SW0`

## נושא 3 - זיכרונות

30 דקות, 11 שאלות: Q21-Q31

### Q21 - גודל מערך זיכרון

- **מתגים ונורות:** `HEX3 = N address bits     HEX2 = M data bits     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מערך זיכרון:
- `HEX3 = N address bits     HEX2 = M data bits`
- כמה מילים יש בו?
- `2^N`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- כמה ביטים בסך הכול?
- `M x 2^N`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

### Q22 - כמה ביטי כתובת?

- **מתגים ונורות:** `HEX2 HEX1 HEX0 = the number of words     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר המילים בזיכרון:
- `HEX2 HEX1 HEX0 = the number of words`
- `logic [31:0] mem [words-1:0];`
- כמה ביטי כתובת צריך?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

### Q23 - קווי מילה

- **מתגים ונורות:** `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מפענח הכתובות של זיכרון של 8 מילים: כל כתובת צריכה להעלות בדיוק קו מילה אחד.
- `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi`
- המפענח שבור בכתובת אחת. עברו על כל הכתובות: מה התקלה?
- `no wordline HIGH = all down     two wordlines HIGH = SW0`

**שלב 2**

- בלוח אותו מפענח:
- `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi`
- באיזו כתובת התקלה?
- `4 = SW2   2 = SW1   1 = SW0`

### Q24 - לקרוא זיכרון לקריאה בלבד

- **מתגים ונורות:** `address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0     answer: SW2..SW0`
- **שלבים:** 4

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 4 מילים של 3 ביטים. מה כתוב בכתובת:
- `address = 00`
- `SW2..SW0 = LEDG2..LEDG0`

**שלב 2**

- ובכתובת:
- `address = 01`
- `SW2..SW0 = LEDG2..LEDG0`

**שלב 3**

- ובכתובת:
- `address = 10`
- `SW2..SW0 = LEDG2..LEDG0`

**שלב 4**

- ובכתובת:
- `address = 11`
- `SW2..SW0 = LEDG2..LEDG0`

### Q25 - סימון נקודות בזיכרון

- **מתגים ונורות:** `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0     answer: SW4..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 4 מילים של 4 ביטים. בסימון נקודות, נקודה היא ביט 1.
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בשורה של כתובת 00?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- בלוח אותו זיכרון:
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בעמודה של
- `Data0 = LEDG0`
- (בכל 4 הכתובות)?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 3**

- בלוח אותו זיכרון:
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בכל הזיכרון?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q26 - זיכרון מקובץ

- **מתגים ונורות:** `address = SW9..SW6 (HEX3)     data = HEX0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 16 מילים של 4 ביטים, שאותחל מקובץ:
- `logic [3:0] ROM[15:0];     initial $readmemh("memfile.dat", ROM);`
- `address = SW9..SW6 (HEX3)     data = HEX0`
- מה כתוב בשורה הראשונה של הקובץ (כתובת 0)?
- `SW3..SW0`

**שלב 2**

- בלוח אותו זיכרון:
- `address = SW9..SW6 (HEX3)     data = HEX0`
- מה כתוב בשורה האחרונה של הקובץ (השורה ה-16)?
- `SW3..SW0`

**שלב 3**

- בלוח אותו זיכרון:
- `address = SW9..SW6 (HEX3)     data = HEX0`
- כל ערך מופיע בקובץ פעם אחת. באיזו כתובת כתוב
- `F`
- `?`
- `SW3..SW0 = the address`

### Q27 - לוגיקה בזיכרון

- **מתגים ונורות:** `A1 = SW9     A0 = SW8     Data2..0 = LEDG2..LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח זיכרון של 4 מילים של 3 ביטים שמממש שלוש פונקציות של הכתובת (כמו בשקופית):
- `A1 = SW9     A0 = SW8     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0`
- איזה ביט נתונים הוא
- `A1 xor A0`
- `?`
- `Data0 = all down     Data1 = SW0     Data2 = SW1`

**שלב 2**

- איזה ביט הוא
- `A1 + A0`
- `(OR)?`
- `Data0 = all down     Data1 = SW0     Data2 = SW1`

### Q28 - טבלת חיפוש

- **מתגים ונורות:** `address = SW9 SW8 SW7     out = LEDG0     answer: SW4..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח טבלת חיפוש
- `(LUT)`
- של 3 כניסות: זיכרון של 8 ביטים, והכניסות הן הכתובת.
- `address = SW9 SW8 SW7     out = LEDG0`
- כתבו את התוכן בכתובות 3 עד 0: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:
- `address 3 -> SW3   ...   address 0 -> SW0`

**שלב 2**

- בלוח אותה טבלה:
- `address = SW9 SW8 SW7     out = LEDG0`
- עכשיו התוכן בכתובות 7 עד 4: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:
- `address 7 -> SW3   ...   address 4 -> SW0`

**שלב 3**

- כמה ביטים צריך לטבלת חיפוש של 4 כניסות?
- `2^4`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q29 - זיכרון לקריאה וכתיבה

- **מתגים ונורות:** `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)     a = SW9     wd = SW8 SW7     we = SW6     LEDG3 LEDG2 = the word at a after the next clock edge     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון של 2 מילים של 2 ביטים. הקריאה מיידית, והכתיבה קורית בעליית השעון.
- `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)`
- מה כתוב עכשיו במילה 0?
- `a = 0:   SW1 SW0 = rd`

**שלב 2**

- בלוח אותו זיכרון:
- `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)`
- מה כתוב עכשיו במילה 1?
- `a = 1:   SW1 SW0 = rd`

**שלב 3**

- בלוח אותו זיכרון. הנורות העליונות מראות את המילה אחרי עליית השעון הבאה:
- `a = SW9     wd = SW8 SW7     we = SW6`
- `LEDG3 LEDG2 = the word at a after the next clock edge`
- הכתיבה קורית כש-
- `we`
- `?`
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

### Q30 - תא זיכרון דינמי

- **מתגים ונורות:** `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)     the bit read = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח תא זיכרון דינמי: הביט נשמר בקבל, והמטען דולף אחרי כמה עליות שעון בלי כתיבה.
- במתגים הביט שנכתב, וכמה עליות שעון עברו מאז הכתיבה. בנורה מה שנקרא עכשיו:
- `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)`
- `the bit read = LEDG0`
- כתבו 1. אחרי כמה עליות שעון הביט נעלם?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`

**שלב 2**

- בלוח אותו תא:
- `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)`
- `the bit read = LEDG0`
- כדי לא לאבד את הביט צריך לרענן אותו (לכתוב שוב).
- אחרי כמה עליות שעון בלי כתיבה, לכל היותר, צריך לרענן?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`

### Q31 - קובץ אוגרים

- **מתגים ונורות:** `read: A1 = SW5 SW4 (HEX1)     RD1 = LEDG0 (now)     write: A3 = SW9 SW8 (HEX3)     WD3 = SW7     WE3 = SW6     LEDG7..LEDG4 = R3..R0 after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח קובץ אוגרים של 4 אוגרים של ביט אחד: פורט קריאה ופורט כתיבה.
- `read: A1 = SW5 SW4 (HEX1)     RD1 = LEDG0 (now)`
- מה כתוב עכשיו בארבעת האוגרים? קראו את כולם.
- `SW3..SW0 = R3..R0`

**שלב 2**

- בלוח אותו קובץ אוגרים. הנורות העליונות מראות את האוגרים אחרי עליית השעון הבאה:
- `write: A3 = SW9 SW8 (HEX3)     WD3 = SW7     WE3 = SW6`
- `LEDG7..LEDG4 = R3..R0 after the next clock edge`
- כתבו 1 לכל אחד מארבעת האוגרים. אולי אחד מחובר תמיד ל-0. איזה?
- `R0 = all down     R1 = SW0     R2 = SW1`
- `R3 = SW1+SW0     none = SW2`

