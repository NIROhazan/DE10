# פירוט השאלות לפי נושא - עם התשובות (למרצה בלבד)

התשובות של הסטודנט `316009489` (מספר כניסה 746). לכל סטודנט מספרים אחרים - לסטודנט אחר:
`python gen.py --answers <ID>`  או  `answers.bat ce <ID>`.

## נושא 1 - נקודה קבועה ונקודה צפה

40 דקות, 19 שאלות: Q01-Q19

### Q01 - 6.75 בפורמט אחר

- **מתגים ונורות:** `a = HEX1     b = HEX0 (the format Ua.b)     answer: SW7..SW0`
- **מה מוסתר בלוח:** `6.75 in U5.3 = 00110110`
- **שלבים:** 1

**שלב 1**

- בשקופית 5 המספר 6.75 בפורמט
- `U4.4 = 0110.1100 = 01101100`
- בתצוגה פורמט אחר:
- `Ua.b:   a = HEX1 integer bits     b = HEX0 fraction bits`
- כתבו את 6.75 בפורמט הזה:
- `SW7..SW0`
- **התשובה:** `SW5 + SW4 + SW2 + SW1`

### Q02 - המחבר ברוויה מהשקופית

- **מתגים ונורות:** `A = 11000000 (12)     B = LEDG7..LEDG0     answer: SW7..SW0`
- **מה מוסתר בלוח:** `11000000 + 10011011: saturated 11111111`
- **שלבים:** 2

**שלב 1**

- בשקופית 7 חיבור ברוויה בפורמט
- `U4.4`
- `:`
- `11000000 + 01111000 = 11111111     (12 + 7.5 = 15.9375)`
- בלוח אותו חיבור, עם אותו מספר ראשון ומספר שני אחר:
- `A = 11000000 (12)     B = LEDG7..LEDG0`
- האם החיבור גולש (לא נכנס ב-8 ביטים)?
- גולש - הרימו:
- `SW0`
- לא גולש - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- בלוח אותו חיבור:
- `A = 11000000 (12)     B = LEDG7..LEDG0`
- מה התוצאה ברוויה? (בגלישה התוצאה היא הערך הגדול ביותר)
- `SW7..SW0 = A + B (saturated)`
- **התשובה:** `SW7 + SW6 + SW5 + SW4 + SW3 + SW2 + SW1 + SW0`

### Q03 - מספרי נקודה צפה מהשקופיות

- **מתגים ונורות:** `HEX3..HEX0 = the high 16 bits (hex)     the low 16 bits are 0     answer: SW8..SW0`
- **מה מוסתר בלוח:** `-58.25 = C2690000`
- **שלבים:** 3

**שלב 1**

- בתצוגה אחד המספרים מהשקופיות 14, 15 ו-21 עד 24, בנקודה צפה:
- `HEX3..HEX0 = the high 16 bits (hex)     the low 16 bits are 0`
- `sign | biased exponent (8 bits) | fraction (23 bits)`
- מה ביט הסימן?
- 1 (שלילי) - הרימו:
- `SW0`
- 0 - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- בתצוגה אותו מספר:
- `HEX3..HEX0 = the high 16 bits (hex)     the low 16 bits are 0`
- `sign | biased exponent (8 bits) | fraction (23 bits)`
- מה המעריך המוטה?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW2`

**שלב 3**

- בתצוגה אותו מספר:
- `HEX3..HEX0 = the high 16 bits (hex)     the low 16 bits are 0`
- איזה מספר מהשקופיות הוא?
- `228 = all down     -58.25 = SW0     1.5 = SW1`
- `3.25 = SW1+SW0     4.75 = SW2`
- **התשובה:** `SW0`

### Q04 - קריאת חיישן בנקודה קבועה

- **מתגים ונורות:** `HEX3 HEX2 = the integer part (hex)     HEX1 HEX0 = the fraction (hex)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `U8.8 2C40 = 44.25`
- **שלבים:** 2

**שלב 1**

- בשקופית 5: הפורמט
- `U8.8`
- משמש לנתוני חיישנים. בתצוגה קריאה של חיישן בפורמט הזה:
- `HEX3 HEX2 = the integer part (hex)     HEX1 HEX0 = the fraction (hex)`
- מה החלק השלם שלה?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW5 + SW3 + SW2`

**שלב 2**

- בתצוגה אותה קריאה:
- `HEX3 HEX2 = the integer part (hex)     HEX1 HEX0 = the fraction (hex)`
- כמה רבעים שלמים יש בחלק השבור?
- `fraction x 4, rounded down`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`
- **התשובה:** `SW0`

### Q05 - כתיב מדעי בינארי

- **מתגים ונורות:** `n = LEDG7..LEDG0 (unsigned)     answer: SW6..SW0`
- **מה מוסתר בלוח:** `80 = 01010000 = 1.f x 2^6`
- **שלבים:** 2

**שלב 1**

- בשקופית 12 המספר 228 בכתיב מדעי בינארי:
- `228 = 11100100 = 1.11001 x 2^7`
- בנורות מספר אחר:
- `n = LEDG7..LEDG0 (unsigned)`
- כתבו אותו כך. מה המעריך?
- `n = 1.f x 2^E:   E = ?`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`
- **התשובה:** `SW2 + SW1`

**שלב 2**

- בנורות אותו מספר:
- `n = LEDG7..LEDG0 (unsigned)`
- מה נשאר אחרי שמורידים את ה-1 השמאלי? (הביטים של השבר)
- `SW6..SW0 = n - 2^E`
- **התשובה:** `SW4`

### Q06 - דיוק יחיד ודיוק כפול

- **מתגים ונורות:** `HEX3 HEX2 = the total number of bits (decimal)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `32 bits: 1 + 8 + 23`
- **שלבים:** 2

**שלב 1**

- בשקופית 17 שני פורמטים של נקודה צפה: דיוק יחיד ודיוק כפול. בתצוגה מספר הביטים של אחד מהם:
- `HEX3 HEX2 = the total number of bits (decimal)`
- כמה ביטים יש למעריך שלו?
- `8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW3`

**שלב 2**

- בתצוגה אותו פורמט:
- `HEX3 HEX2 = the total number of bits (decimal)`
- כמה ביטים יש לשבר שלו?
- `total = 1 sign + exponent + fraction`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW2 + SW1 + SW0`

### Q07 - נרמול אחרי חיבור

- **מתגים ונורות:** `LEDG5..LEDG0 = the sum mantissa xx.xxxx     HEX0 = its exponent E     answer: SW4..SW0`
- **מה מוסתר בלוח:** `11.0010 x 2^4 = 1.10010 x 2^5`
- **שלבים:** 3

**שלב 1**

- בשקופית 24 מנרמלים את הסכום:
- `10.011 x 2^1 = 1.0011 x 2^2`
- בנורות סכום אחר של מנטיסות, עם 2 ביטים שלמים:
- `LEDG5..LEDG0 = the sum mantissa xx.xxxx     HEX0 = its exponent E`
- האם צריך לנרמל אותו (הביטים השלמים הם 10 או 11)?
- צריך - הרימו:
- `SW0`
- לא צריך - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- בנורות אותו סכום:
- `LEDG5..LEDG0 = the sum mantissa xx.xxxx     HEX0 = its exponent E`
- מה המעריך אחרי הנרמול?
- `SW2..SW0 = the new E`
- **התשובה:** `SW2 + SW0`

**שלב 3**

- בנורות אותו סכום:
- `LEDG5..LEDG0 = the sum mantissa xx.xxxx     HEX0 = its exponent E`
- מה 5 ביטי השבר אחרי הנרמול (אחרי ה-1 שלפני הנקודה)?
- `SW4..SW0 = 1.f:  f = ?`
- **התשובה:** `SW4 + SW1`

### Q08 - נקודה קבועה בלי סימן

- **מתגים ונורות:** `the bits = LEDG7..LEDG0     a = HEX1     b = HEX0 (the format Ua.b)     answer: SW5..SW0`
- **מה מוסתר בלוח:** `U6.2 11110000 = 60.0`
- **שלבים:** 2

**שלב 1**

- בנורות מספר בנקודה קבועה בלי סימן, ובתצוגה הפורמט:
- `Ua.b:   a = HEX1 integer bits     b = HEX0 fraction bits`
- מה החלק השלם שלו?
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW5 + SW4 + SW3 + SW2`

**שלב 2**

- כמה שישה-עשריות יש בחלק השבור? (למשל 0.75 = 12/16)
- `fraction x 16`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `all down`

### Q09 - נקודה קבועה עם סימן

- **מתגים ונורות:** `the bits = LEDG7..LEDG0 (Q4.4)     answer: SW3..SW0`
- **מה מוסתר בלוח:** `Q4.4 01110101 = 7.3125`
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
- **התשובה:** `all down`

**שלב 2**

- מה החלק השלם של הערך המוחלט שלו? (שלילי: הפכו את כל הביטים והוסיפו 1)
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW1 + SW0`

**שלב 3**

- וכמה שישה-עשריות בחלק השבור של הערך המוחלט?
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW0`

### Q10 - מספר נגדי בנקודה קבועה

- **מתגים ונורות:** `x = LEDG7..LEDG0 (Q4.4, positive)     answer: SW7..SW0`
- **מה מוסתר בלוח:** `Q4.4 00011010 = 1.625, negated 11100110`
- **שלבים:** 2

**שלב 1**

- בנורות מספר חיובי בפורמט
- `Q4.4`
- `x = LEDG7..LEDG0`
- מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.
- במשלים ל-2 מוצאים את הנגדי כך: הופכים את כל הביטים (0 ל-1 ו-1 ל-0), ואז מוסיפים 1.
- שלב 1 בהיפוך הסימן: הפכו את כל הביטים שלו.
- `SW7..SW0 = not x`
- **התשובה:** `SW7 + SW6 + SW5 + SW2 + SW0`

**שלב 2**

- בנורות אותו מספר:
- `x = LEDG7..LEDG0     (Q4.4)`
- מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.
- שלב 2: הוסיפו 1 לביט הימני. כתבו את המספר הנגדי:
- `SW7..SW0 = -x`
- **התשובה:** `SW7 + SW6 + SW5 + SW2 + SW1`

### Q11 - לכתוב בנקודה קבועה

- **מתגים ונורות:** `HEX3 = integer     HEX2 HEX1 = hundredths     answer: SW8..SW0`
- **מה מוסתר בלוח:** `6.50`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר עשרוני:
- `HEX3 = the integer part (hex)     HEX2 HEX1 = hundredths`
- כתבו אותו בפורמט
- `U4.4`
- `:`
- `SW7..SW4 = integer     SW3..SW0 = fraction x 16`
- **התשובה:** `SW6 + SW5 + SW3`

### Q12 - חשבון רוויה

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = B (hex)     (unsigned 4 bits)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `15 + 6: wrap 5, saturate 15`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים של 4 ביטים בלי סימן:
- `HEX3 = A (hex)     HEX2 = B (hex)     (unsigned 4 bits)`
- מה החיבור הרגיל שלהם ב-4 ביטים (הנשא נזרק)?
- `SW3..SW0`
- **התשובה:** `SW2 + SW0`

**שלב 2**

- ומה החיבור ברוויה (אם הסכום גדול מ-15, התוצאה 15)?
- `SW3..SW0`
- **התשובה:** `SW3 + SW2 + SW1 + SW0`

### Q13 - חיבור ברוויה בנקודה קבועה

- **מתגים ונורות:** `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `7.375 + 6.1875: saturated 11011001`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים בנקודה קבועה בלי סימן:
- `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)`
- האם החיבור שלהם גולש (לא נכנס ב-8 ביטים)?
- גולש - הרימו:
- `SW0`
- לא גולש - השאירו למטה.
- **התשובה:** `all down`

**שלב 2**

- בתצוגה אותם שני מספרים:
- `HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)`
- מה החיבור ברוויה? (בגלישה התוצאה היא הערך הגדול ביותר)
- `SW7..SW0 = A + B (U4.4, saturated)`
- **התשובה:** `SW7 + SW6 + SW4 + SW3 + SW0`

### Q14 - לפענח מספר נקודה צפה

- **מתגים ונורות:** `the float in hex, high / low 16 bits     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `249.5 = 43798000`
- **שלבים:** 4

**שלב 1**

- בתצוגה מספר נקודה צפה של 32 ביטים, בהקס, בשני דפים:
- `page 1 (SW9 down): the high 16 bits (hex)     page 2 (SW9 up): the low 16 bits`
- `sign | biased exponent (8 bits) | fraction (23 bits)`
- מה ביט הסימן?
- 1 (שלילי) - הרימו:
- `SW0`
- 0 - השאירו למטה.
- **התשובה:** `all down`

**שלב 2**

- מה המעריך המוטה (8 הביטים שאחרי הסימן)?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW2 + SW1`

**שלב 3**

- מה המעריך האמיתי?
- `exponent = biased - 127`
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW2 + SW1 + SW0`

**שלב 4**

- מה החלק השלם של הערך המוחלט?
- `|value| = 1.fraction x 2^exponent`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW6 + SW5 + SW4 + SW3 + SW0`

### Q15 - לקודד מספר בנקודה צפה

- **מתגים ונורות:** `HEX2 HEX1 HEX0 = N (decimal)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `215 = 43570000`
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
- **התשובה:** `SW7 + SW2 + SW1`

**שלב 2**

- מה 8 הביטים הראשונים של השבר (אחרי ה-1 שלא נכתב)?
- `SW7 = the first fraction bit`
- **התשובה:** `SW7 + SW5 + SW3 + SW2 + SW1`

### Q16 - מקרים מיוחדים בנקודה צפה

- **מתגים ונורות:** `the float in hex: high 16 bits / low 16 bits (SW9)     answer: SW3..SW0`
- **מה מוסתר בלוח:** `43640000 = a normal number`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר נקודה צפה בהקס, בשני דפים:
- `page 1 (SW9 down): the high 16 bits (hex)     page 2 (SW9 up): the low 16 bits`
- `exponent all 0 and fraction 0: zero     exponent all 1: fraction 0 = infinity, else NaN`
- מה הוא?
- `0 = all down     -0 = SW0     infinity = SW1`
- `-infinity = SW1+SW0     NaN = SW2     a normal number = SW2+SW0`
- **התשובה:** `SW2 + SW0`

### Q17 - השוואת מספרים בנקודה צפה

- **מתגים ונורות:** `N1 / N2 high 16 bits     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `N1 = -27.0  N2 = 26.75`
- **שלבים:** 3

**שלב 1**

- בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- מה הסימנים שלהם?
- `N1+ N2+ = all down     N1+ N2- = SW0     N1- N2+ = SW1     N1- N2- = SW1+SW0`
- **התשובה:** `SW1`

**שלב 2**

- בתצוגה אותם שני מספרים:
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- למי יש מעריך מוטה גדול יותר?
- `N1 = all down     N2 = SW0     equal = SW1`
- **התשובה:** `SW1`

**שלב 3**

- בתצוגה אותם שני מספרים:
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- מי המספר הגדול יותר (עם הסימן)?
- `N1 = all down     N2 = SW0`
- **התשובה:** `SW0`

### Q18 - עיגול בנקודה צפה

- **מתגים ונורות:** `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits     answer: SW2..SW0`
- **מה מוסתר בלוח:** `1.001010: down 001 up 010 nearest 001`
- **שלבים:** 3

**שלב 1**

- בנורות מנטיסה חיובית עם 6 ביטי שבר:
- `1.f`
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר כלפי מטה. מה 3 ביטי השבר?
- `SW2..SW0`
- **התשובה:** `SW0`

**שלב 2**

- בנורות אותה מנטיסה:
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר כלפי מעלה:
- `SW2..SW0`
- **התשובה:** `SW1`

**שלב 3**

- בנורות אותה מנטיסה:
- `LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits`
- עגלו אותה ל-3 ביטי שבר לקרוב ביותר:
- `SW2..SW0`
- **התשובה:** `SW0`

### Q19 - חיבור בנקודה צפה

- **מתגים ונורות:** `N1 / N2 high 16 bits     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `14.0 + 6.75 = 20.75`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):
- `page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)`
- החיבור: מוציאים מעריכים, מזיזים את הקטן ימינה בהפרש. בכמה מקומות מזיזים?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW0`

**שלב 2**

- מה המעריך המוטה של הסכום (אחרי נרמול)?
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW1 + SW0`

## נושא 2 - מונים ואוגרי הזזה

40 דקות, 14 שאלות: Q20-Q33

### Q20 - המונה מהשקופית

- **מתגים ונורות:** `reset = SW9     q = SW8..SW6 (HEX3)     q after the next clock edge = LEDG2..LEDG0     the q to set = HEX0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `q = 110: next 111, then 000`
- **שלבים:** 2

**שלב 1**

- בשקופית 27 המונה:
- `if (reset) q <= 0; else q <= q + 1;`
- בלוח המונה הזה, של 3 ביטים. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `reset = SW9     q = SW8..SW6 (HEX3)`
- `q after the next clock edge = LEDG2..LEDG0`
- שימו במתגים:
- `reset = 0     q = HEX0`
- מה הערך אחרי עליית השעון הבאה?
- `SW2..SW0`
- **התשובה:** `SW2 + SW1 + SW0`

**שלב 2**

- בלוח אותו מונה:
- `reset = SW9     q = SW8..SW6 (HEX3)`
- `q after the next clock edge = LEDG2..LEDG0`
- מתחילים מ:
- `reset = 0     q = HEX0`
- מה הערך אחרי שתי עליות שעון?
- `SW2..SW0`
- **התשובה:** `all down`

### Q21 - המתנד מהשקופית

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0     p = HEX0     the q to set = HEX1     answer: SW3..SW0`
- **מה מוסתר בלוח:** `p = 11, from q = 13: 8, 3`
- **שלבים:** 2

**שלב 1**

- בשקופית 29 מתנד בשליטה ספרתית: מונה שמוסיף בכל עליית שעון את
- `p`
- במקום 1.
- `q <= q + p`
- בלוח מונה כזה, של 4 ביטים. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- `p = HEX0`
- שימו במתגים:
- `q = HEX1`
- מה הערך אחרי עליית השעון הבאה?
- `SW3..SW0`
- **התשובה:** `SW3`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- `p = HEX0`
- מתחילים מ:
- `q = HEX1`
- מה הערך אחרי שתי עליות שעון?
- `SW3..SW0`
- **התשובה:** `SW1 + SW0`

### Q22 - אוגר הזזה עם טעינה מהשקופית

- **מתגים ונורות:** `Load = SW9     Sin = SW8     Q3..Q0 = SW7..SW4 (HEX3)     q after the next clock edge = LEDG3..LEDG0     D = HEX0     the Q to set = HEX1     the Sin to set = LEDR0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `D = 0100; Q = 1110, Sin = 0: shift -> 1100`
- **שלבים:** 2

**שלב 1**

- בשקופיות 31-32 אוגר הזזה עם טעינה מקבילית:
- `Load = 1: Q <= D     Load = 0: Q <= {Q[2:0], Sin}`
- בלוח האוגר הזה, של 4 ביטים. במתגים הכניסות והערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `Load = SW9     Sin = SW8     Q3..Q0 = SW7..SW4 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `D = HEX0`
- שימו במתגים:
- `Load = 1`
- מה הערך אחרי עליית השעון הבאה?
- `SW3..SW0`
- **התשובה:** `SW2`

**שלב 2**

- בלוח אותו אוגר:
- `Load = 1: Q <= D     Load = 0: Q <= {Q[2:0], Sin}`
- `Load = SW9     Sin = SW8     Q3..Q0 = SW7..SW4 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- שימו במתגים:
- `Load = 0     Sin = LEDR0     Q = HEX1`
- מה הערך אחרי עליית השעון הבאה?
- `SW3..SW0`
- **התשובה:** `SW3 + SW2`

### Q23 - מטורי למקבילי מהשקופית

- **מתגים ונורות:** `Q3..Q0 = SW9..SW6 (HEX3)     Sin = SW5     q after the next clock edge = LEDG3..LEDG0     the bits to send = LEDR3..LEDR0 (LEDR0 first)     answer: SW3..SW0`
- **מה מוסתר בלוח:** `send 0010: Q = 0010`
- **שלבים:** 2

**שלב 1**

- בשקופית 30 אוגר הזזה הוא ממיר מטורי למקבילי: בכל עליית שעון הביט החדש נכנס ל-
- `Q0`
- והשאר זזים.
- `Q <= {Q[2:0], Sin}`
- בלוח האוגר הזה, של 4 ביטים. במתגים הערך עכשיו והכניסה, ובנורות הערך אחרי עליית השעון הבאה:
- `Q3..Q0 = SW9..SW6 (HEX3)     Sin = SW5`
- `q after the next clock edge = LEDG3..LEDG0`
- `the bits to send = LEDR3..LEDR0 (LEDR0 first)`
- שימו במתגים:
- `Q = 0000     Sin = LEDR0`
- מה הערך אחרי עליית השעון הבאה?
- `SW3..SW0`
- **התשובה:** `all down`

**שלב 2**

- בלוח אותו אוגר:
- `Q <= {Q[2:0], Sin}`
- `Q3..Q0 = SW9..SW6 (HEX3)     Sin = SW5`
- `q after the next clock edge = LEDG3..LEDG0`
- `the bits to send = LEDR3..LEDR0 (LEDR0 first)`
- שולחים את 4 הביטים, אחד בכל עליית שעון. מה הערך אחרי 4 עליות שעון?
- `SW3..SW0`
- **התשובה:** `SW1`

### Q24 - התדר של המתנד

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `p = 1: f_out = 2 Hz`
- **שלבים:** 1

**שלב 1**

- בשקופית 29 התדר של הביט העליון במתנד בשליטה ספרתית:
- `f_out = f_clk x p / 2^N`
- בלוח מתנד של 4 ביטים עם
- `p`
- מוסתר. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- השעון הוא 32 הרץ. מה התדר של הביט העליון, בהרץ?
- `f_clk = 32 Hz     N = 4     f_out = ?`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW1`

### Q25 - הביט העליון של המונה

- **מתגים ונורות:** `q = SW9..SW7 (HEX3)     q after the next clock edge = LEDG2..LEDG0     the start value = HEX0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `from 000: q[2] changes after 4 edges, to 100`
- **שלבים:** 2

**שלב 1**

- בשקופיות 26 ו-28 מונה של 3 ביטים: 000, 001, ..., 111, 000. הביט העליון שלו משמש לחלוקת תדר.
- בלוח המונה הזה. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW7 (HEX3)     q after the next clock edge = LEDG2..LEDG0`
- `the start value = HEX0`
- מתחילים מ:
- `q = HEX0`
- אחרי כמה עליות שעון הביט העליון משתנה בפעם הראשונה?
- `q[2] = LEDG2`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW2`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW7 (HEX3)     q after the next clock edge = LEDG2..LEDG0`
- `the start value = HEX0`
- מתחילים מ:
- `q = HEX0`
- מה הערך ברגע שהביט העליון משתנה?
- `SW2..SW0`
- **התשובה:** `SW2`

### Q26 - מחלק ב-2 בחזקת N

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q     answer: SW4..SW0`
- **מה מוסתר בלוח:** `LED = q[3]`
- **שלבים:** 3

**שלב 1**

- בלוח מונה בינארי, והנורה מחוברת לאחד הביטים שלו.
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- שימו במתגים את ערכי המונה לפי הסדר: 0, 1, 2, 3, ... כל כמה ספירות הנורה משתנה?
- `1 = SW0     2 = SW1     4 = SW2     8 = SW3`
- **התשובה:** `SW3`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- לאיזה ביט של המונה הנורה מחוברת?
- `q[k]:   k = ?`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`
- **התשובה:** `SW1 + SW0`

**שלב 3**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     LEDG0 = one bit of q`
- המונה סופר 1 בכל עליית שעון. כמה עליות שעון נמשך מחזור שלם של הנורה (דולקת וכבויה)?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4`

### Q27 - מונה עם ערך איפוס

- **מתגים ונורות:** `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `reset to 5, counts up`
- **שלבים:** 2

**שלב 1**

- בלוח מונה:
- `always_ff @(posedge clk) if (reset) q <= R; else q <= q +- 1;`
- במתגים הכניסות עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:
- `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0`
- מה ערך האיפוס?
- `R = ?     SW3..SW0`
- **התשובה:** `SW2 + SW0`

**שלב 2**

- בלוח אותו מונה:
- `always_ff @(posedge clk) if (reset) q <= R; else q <= q +- 1;`
- `reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0`
- הוא סופר למעלה או למטה?
- `up = all down     down = SW0`
- **התשובה:** `all down`

### Q28 - מונה עם מחזור מוסתר

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `counts 0..15`
- **שלבים:** 2

**שלב 1**

- בלוח מונה שחוזר ל-0 אחרי ערך מוסתר. במתגים הערך עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0`
- התחילו ב-0 ועקבו אחרי המונה. מה הערך הגדול ביותר שהוא מגיע אליו?
- `SW3..SW0`
- **התשובה:** `SW3 + SW2 + SW1 + SW0`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0`
- כמה ערכים שונים יש במחזור שלו?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4`

### Q29 - מתנד בשליטה ספרתית

- **מתגים ונורות:** `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `adds 12`
- **שלבים:** 2

**שלב 1**

- בלוח מונה של 4 ביטים שמוסיף מספר מוסתר בכל עליית שעון (במקום 1).
- במתגים הערך של המונה עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- מה המספר שהוא מוסיף?
- `p = ?     SW3..SW0`
- **התשובה:** `SW3 + SW2`

**שלב 2**

- בלוח אותו מונה:
- `q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0`
- הוא מתחיל ב-0. אחרי כמה עליות שעון הוא חוזר ל-0 בפעם הראשונה?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW2`

### Q30 - אוגר הזזה

- **מתגים ונורות:** `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `enters at LEDG3, as is`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר הזזה של 4 ביטים עם כניסה טורית. במתגים הערך עכשיו והכניסה, ובנורות הערך אחרי עליית השעון הבאה:
- `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0`
- באיזו נורה נכנס הביט החדש?
- `LEDG0 = all down     LEDG3 = SW0`
- **התשובה:** `SW0`

**שלב 2**

- בלוח אותו אוגר:
- `Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     q after the next clock edge = LEDG3..LEDG0`
- הביט נכנס כמו שהוא, או הפוך?
- `as is = all down     inverted = SW0`
- **התשובה:** `all down`

### Q31 - אוגר הזזה כקו השהיה

- **מתגים ונורות:** `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)     LEDG0 = one output, after the next clock edge     answer: SW3..SW0`
- **מה מוסתר בלוח:** `LEDG0 = Q[3]`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר הזזה של 4 ביטים. בכל עליית שעון הכניסה הטורית נכנסת לביט הראשון והשאר זזים הלאה.
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- הנורה מחוברת לאחת היציאות, ומראה אותה אחרי עליית השעון הבאה.
- `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)`
- `LEDG0 = one output, after the next clock edge`
- את איזה ערך הנורה מעתיקה?
- `Sin = all down     Q[0] = SW0     Q[1] = SW1     Q[2] = SW1+SW0`
- **התשובה:** `SW1 + SW0`

**שלב 2**

- בלוח אותו אוגר:
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- `Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)`
- `LEDG0 = one output, after the next clock edge`
- לאיזו יציאה מחוברת הנורה?
- `Q[k]:   k = ?`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`
- **התשובה:** `SW1 + SW0`

**שלב 3**

- בלוח אותו אוגר:
- `Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]`
- `LEDG0 = Q[k]`
- ביט חדש נכנס ב-
- `Sin`
- . אחרי כמה עליות שעון הוא מגיע לנורה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW2`

### Q32 - ממקבילי לטורי

- **מתגים ונורות:** `Load = SW9     Q = SW8..SW5 (HEX3)     q after the next clock edge = LEDG3..LEDG0     Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)     answer: SW3..SW0`
- **מה מוסתר בלוח:** `loads 0100, shifts left`
- **שלבים:** 3

**שלב 1**

- בלוח ממיר ממקבילי לטורי: אוגר הזזה שטוען מילה מוסתרת ומוציא אותה ביט אחרי ביט.
- במתגים הכניסות עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- מה המילה שנטענת?
- `SW3..SW0 = W`
- **התשובה:** `SW2`

**שלב 2**

- בלוח אותו אוגר:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- לאיזה כיוון הוא מזיז?
- `left: Sout = Q3 = all down     right: Sout = Q0 = SW0`
- **התשובה:** `all down`

**שלב 3**

- בלוח אותו אוגר:
- `Load = SW9     Q = SW8..SW5 (HEX3)`
- `q after the next clock edge = LEDG3..LEDG0`
- `Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)`
- טוענים את המילה, ואחר כך היא יוצאת ביט אחרי ביט. מה סדר היציאה?
- `SW3 = the first bit out   ...   SW0 = the last bit out`
- **התשובה:** `SW2`

### Q33 - אוגר הזזה עם טעינה מקבילית

- **מתגים ונורות:** `D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)     q after the next clock edge = LEDG3..LEDG0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `D C, Load = SW5, shifts right`
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
- **התשובה:** `all down`

**שלב 2**

- בלוח אותו אוגר:
- `D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)`
- `q after the next clock edge = LEDG3..LEDG0`
- לאיזה כיוון הוא מזיז?
- `left (into LEDG0) = all down     right (into LEDG3) = SW0`
- **התשובה:** `SW0`

## נושא 3 - זיכרונות

40 דקות, 17 שאלות: Q34-Q50

### Q34 - מערך הזיכרון מהשקופית

- **מתגים ונורות:** `address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0     the addresses to read = HEX1, HEX0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `address 00: 011, address 01: 110`
- **שלבים:** 2

**שלב 1**

- בשקופית 36 מערך זיכרון של 4 מילים של 3 ביטים. בלוח המערך הזה:
- `address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0`
- מה המילה בכתובת שבתצוגה?
- `address = HEX1`
- `SW2..SW0`
- **התשובה:** `SW1 + SW0`

**שלב 2**

- בלוח אותו מערך:
- `address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0`
- ומה המילה בכתובת:
- `address = HEX0`
- `SW2..SW0`
- **התשובה:** `SW2 + SW1`

### Q35 - הזיכרון מהשקופית: שלוש פונקציות

- **מתגים ונורות:** `A1 A0 = SW9 SW8 (HEX3)     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0     the addresses to read = HEX1, HEX0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `address 11: 011, address 01: 110`
- **שלבים:** 2

**שלב 1**

- בשקופית 54 זיכרון של 4 מילים של 3 ביטים שמממש שלוש פונקציות של הכתובת:
- `Data2 = A1 xor A0     Data1 = A1 + A0     Data0 = A1 A0`
- בלוח הזיכרון הזה:
- `A1 A0 = SW9 SW8 (HEX3)     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0`
- מה המילה בכתובת שבתצוגה?
- `A1 A0 = HEX1`
- `SW2..SW0`
- **התשובה:** `SW1 + SW0`

**שלב 2**

- בלוח אותו זיכרון:
- `A1 A0 = SW9 SW8 (HEX3)     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0`
- ומה המילה בכתובת:
- `A1 A0 = HEX0`
- `SW2..SW0`
- **התשובה:** `SW2 + SW1`

### Q36 - לוגיקה בזיכרון מהשקופית

- **מתגים ונורות:** `A = SW9     B = SW8     X Y Z = LEDG2 LEDG1 LEDG0     the inputs to set: HEX3 HEX2, then HEX1 HEX0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `AB 01: XYZ 010, AB 00: XYZ 000`
- **שלבים:** 2

**שלב 1**

- בשקופיות 55 ו-57 מימוש שלוש פונקציות בזיכרון של 4 מילים של 3 ביטים:
- `X = AB     Y = A + B     Z = AB'`
- בלוח הזיכרון הזה:
- `A = SW9     B = SW8     X Y Z = LEDG2 LEDG1 LEDG0`
- שימו במתגים:
- `A = HEX3     B = HEX2`
- מה היציאות?
- `SW2 SW1 SW0 = X Y Z`
- **התשובה:** `SW1`

**שלב 2**

- בלוח אותו זיכרון:
- `X = AB     Y = A + B     Z = AB'`
- `A = SW9     B = SW8     X Y Z = LEDG2 LEDG1 LEDG0`
- שימו במתגים:
- `A = HEX1     B = HEX0`
- מה היציאות?
- `SW2 SW1 SW0 = X Y Z`
- **התשובה:** `all down`

### Q37 - קובץ הזיכרון מהשקופית

- **מתגים ונורות:** `address = SW9 SW8     SW7 = 0: HEX3..HEX0 = the high 16 bits     SW7 = 1: the low 16 bits     answer: SW1 SW0`
- **מה מוסתר בלוח:** `00:FFFFFFFF 01:A5A5A5A5 10:89ABCDEF 11:01234567`
- **שלבים:** 2

**שלב 1**

- בשקופית 62 ארבע שורות של קובץ זיכרון. בלוח זיכרון לקריאה בלבד שאותחל מהשורות האלה, בסדר אחר:
- `01234567     89ABCDEF     FFFFFFFF     A5A5A5A5`
- `address = SW9 SW8     SW7 = 0: HEX3..HEX0 = the high 16 bits     SW7 = 1: the low 16 bits`
- מה כתוב בכתובת 00?
- `01234567 = all down     89ABCDEF = SW0     FFFFFFFF = SW1     A5A5A5A5 = SW1+SW0`
- **התשובה:** `SW1`

**שלב 2**

- בלוח אותו זיכרון:
- `address = SW9 SW8     SW7 = 0: HEX3..HEX0 = the high 16 bits     SW7 = 1: the low 16 bits`
- באיזו כתובת כתוב
- `FFFFFFFF`
- `?`
- `SW1 SW0 = the address`
- **התשובה:** `all down`

### Q38 - קובץ אוגרים עם שני פורטי קריאה

- **מתגים ונורות:** `A1 = SW9 SW8 (HEX2)     RD1 = HEX3     A2 = SW7 SW6 (HEX1)     RD2 = HEX0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `R0 = 0  R1 = B  R2 = F  R3 = 5`
- **שלבים:** 2

**שלב 1**

- בשקופיות 63-64 קובץ אוגרים עם שני פורטי קריאה, ואוגר 0 תמיד נקרא כ-0. בלוח קובץ כזה של 4 אוגרים של 4 ביטים:
- `A1 = SW9 SW8 (HEX2)     RD1 = HEX3     A2 = SW7 SW6 (HEX1)     RD2 = HEX0`
- מה כתוב באוגר 1?
- `SW3..SW0 = R1`
- **התשובה:** `SW3 + SW1 + SW0`

**שלב 2**

- בלוח אותו קובץ:
- `A1 = SW9 SW8 (HEX2)     RD1 = HEX3     A2 = SW7 SW6 (HEX1)     RD2 = HEX0`
- קראו את אוגר 2 ואת אוגר 3 בבת אחת, בשני הפורטים. מה הסכום שלהם?
- `SW4..SW0 = R2 + R3`
- **התשובה:** `SW4 + SW2`

### Q39 - זיכרון נדיף או לא

- **מתגים ונורות:** `SW9 = 0: power on     SW9 = 1: after power off and on again     HEX0 = the word in the memory     answer: SW3..SW0`
- **מה מוסתר בלוח:** `RAM holding 7`
- **שלבים:** 2

**שלב 1**

- בשקופיות 40-42: זיכרון לקריאה וכתיבה נדיף (מאבד את המידע כשהמתח נופל), וזיכרון לקריאה בלבד שומר עליו.
- בלוח זיכרון של מילה אחת:
- `SW9 = 0: power on     SW9 = 1: after power off and on again     HEX0 = the word in the memory`
- מה כתוב בו עכשיו (המתח דלוק)?
- `SW3..SW0`
- **התשובה:** `SW2 + SW1 + SW0`

**שלב 2**

- בלוח אותו זיכרון:
- `SW9 = 0: power on     SW9 = 1: after power off and on again     HEX0 = the word in the memory`
- כבו והדליקו את המתח. איזה סוג זיכרון זה?
- `RAM = all down     ROM = SW0`
- **התשובה:** `all down`

### Q40 - גודל מערך זיכרון

- **מתגים ונורות:** `HEX3 = N address bits     HEX2 = M data bits     answer: SW8..SW0`
- **מה מוסתר בלוח:** `2 words x 4 bits`
- **שלבים:** 2

**שלב 1**

- בתצוגה מערך זיכרון:
- `HEX3 = N address bits     HEX2 = M data bits`
- כמה מילים יש בו?
- `2^N`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW1`

**שלב 2**

- כמה ביטים בסך הכול?
- `M x 2^N`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW3`

### Q41 - כמה ביטי כתובת?

- **מתגים ונורות:** `HEX2 HEX1 HEX0 = the number of words     answer: SW8..SW0`
- **מה מוסתר בלוח:** `32 words: 5 address bits`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר המילים בזיכרון:
- `HEX2 HEX1 HEX0 = the number of words`
- `logic [31:0] mem [words-1:0];`
- כמה ביטי כתובת צריך?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`
- **התשובה:** `SW2 + SW0`

### Q42 - קווי מילה

- **מתגים ונורות:** `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi     answer: SW2..SW0`
- **מה מוסתר בלוח:** `address 7: wordlines 7 and 6`
- **שלבים:** 2

**שלב 1**

- בלוח מפענח הכתובות של זיכרון של 8 מילים: כל כתובת צריכה להעלות בדיוק קו מילה אחד.
- `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi`
- המפענח שבור בכתובת אחת. עברו על כל הכתובות: מה התקלה?
- `no wordline HIGH = all down     two wordlines HIGH = SW0`
- **התשובה:** `SW0`

**שלב 2**

- בלוח אותו מפענח:
- `address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi`
- באיזו כתובת התקלה?
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW2 + SW1 + SW0`

### Q43 - לקרוא זיכרון לקריאה בלבד

- **מתגים ונורות:** `address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0     answer: SW2..SW0`
- **מה מוסתר בלוח:** `00:100 01:001 10:000 11:100`
- **שלבים:** 4

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 4 מילים של 3 ביטים. מה כתוב בכתובת:
- `address = 00`
- `SW2..SW0 = LEDG2..LEDG0`
- **התשובה:** `SW2`

**שלב 2**

- ובכתובת:
- `address = 01`
- `SW2..SW0 = LEDG2..LEDG0`
- **התשובה:** `SW0`

**שלב 3**

- ובכתובת:
- `address = 10`
- `SW2..SW0 = LEDG2..LEDG0`
- **התשובה:** `all down`

**שלב 4**

- ובכתובת:
- `address = 11`
- `SW2..SW0 = LEDG2..LEDG0`
- **התשובה:** `SW2`

### Q44 - סימון נקודות בזיכרון

- **מתגים ונורות:** `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `00:1101 01:1000 10:1010 11:0101`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 4 מילים של 4 ביטים. בסימון נקודות, נקודה היא ביט 1.
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בשורה של כתובת 00?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW1 + SW0`

**שלב 2**

- בלוח אותו זיכרון:
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בעמודה של
- `Data0 = LEDG0`
- (בכל 4 הכתובות)?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW1`

**שלב 3**

- בלוח אותו זיכרון:
- `address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0`
- כמה נקודות יש בכל הזיכרון?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW3`

### Q45 - זיכרון מקובץ

- **מתגים ונורות:** `address = SW9..SW6 (HEX3)     data = HEX0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `memfile 51BAF42C89ED0736`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון לקריאה בלבד של 16 מילים של 4 ביטים, שאותחל מקובץ:
- `logic [3:0] ROM[15:0];     initial $readmemh("memfile.dat", ROM);`
- `address = SW9..SW6 (HEX3)     data = HEX0`
- מה כתוב בשורה הראשונה של הקובץ (כתובת 0)?
- `SW3..SW0`
- **התשובה:** `SW2 + SW0`

**שלב 2**

- בלוח אותו זיכרון:
- `address = SW9..SW6 (HEX3)     data = HEX0`
- מה כתוב בשורה האחרונה של הקובץ (השורה ה-16)?
- `SW3..SW0`
- **התשובה:** `SW2 + SW1`

**שלב 3**

- בלוח אותו זיכרון:
- `address = SW9..SW6 (HEX3)     data = HEX0`
- כל ערך מופיע בקובץ פעם אחת. באיזו כתובת כתוב
- `F`
- `?`
- `SW3..SW0 = the address`
- **התשובה:** `SW2`

### Q46 - לוגיקה בזיכרון

- **מתגים ונורות:** `A1 = SW9     A0 = SW8     Data2..0 = LEDG2..LEDG0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `Data0=AND Data1=XOR Data2=OR`
- **שלבים:** 2

**שלב 1**

- בלוח זיכרון של 4 מילים של 3 ביטים שמממש שלוש פונקציות של הכתובת (כמו בשקופית):
- `A1 = SW9     A0 = SW8     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0`
- איזה ביט נתונים הוא
- `A1 xor A0`
- `?`
- `Data0 = all down     Data1 = SW0     Data2 = SW1`
- **התשובה:** `SW0`

**שלב 2**

- איזה ביט הוא
- `A1 + A0`
- `(OR)?`
- `Data0 = all down     Data1 = SW0     Data2 = SW1`
- **התשובה:** `SW1`

### Q47 - טבלת חיפוש

- **מתגים ונורות:** `address = SW9 SW8 SW7     out = LEDG0     answer: SW4..SW0`
- **מה מוסתר בלוח:** `LUT 01010010`
- **שלבים:** 3

**שלב 1**

- בלוח טבלת חיפוש
- `(LUT)`
- של 3 כניסות: זיכרון של 8 ביטים, והכניסות הן הכתובת.
- `address = SW9 SW8 SW7     out = LEDG0`
- כתבו את התוכן בכתובות 3 עד 0: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:
- `address 3 -> SW3   ...   address 0 -> SW0`
- **התשובה:** `SW1`

**שלב 2**

- בלוח אותה טבלה:
- `address = SW9 SW8 SW7     out = LEDG0`
- עכשיו התוכן בכתובות 7 עד 4: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:
- `address 7 -> SW3   ...   address 4 -> SW0`
- **התשובה:** `SW2 + SW0`

**שלב 3**

- כמה ביטים צריך לטבלת חיפוש של 4 כניסות?
- `2^4`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4`

### Q48 - זיכרון לקריאה וכתיבה

- **מתגים ונורות:** `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)     a = SW9     wd = SW8 SW7     we = SW6     LEDG3 LEDG2 = the word at a after the next clock edge     answer: SW1 SW0`
- **מה מוסתר בלוח:** `word0 10 word1 01, we active high`
- **שלבים:** 3

**שלב 1**

- בלוח זיכרון של 2 מילים של 2 ביטים. הקריאה מיידית, והכתיבה קורית בעליית השעון.
- `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)`
- מה כתוב עכשיו במילה 0?
- `a = 0:   SW1 SW0 = rd`
- **התשובה:** `SW1`

**שלב 2**

- בלוח אותו זיכרון:
- `a = SW9     rd = LEDG1 LEDG0 (the word at a, now)`
- מה כתוב עכשיו במילה 1?
- `a = 1:   SW1 SW0 = rd`
- **התשובה:** `SW0`

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
- **התשובה:** `SW0`

### Q49 - תא זיכרון דינמי

- **מתגים ונורות:** `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)     the bit read = LEDG0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `the charge leaks after 5 clocks`
- **שלבים:** 2

**שלב 1**

- בלוח תא זיכרון דינמי: הביט נשמר בקבל, והמטען דולף אחרי כמה עליות שעון בלי כתיבה.
- במתגים הביט שנכתב, וכמה עליות שעון עברו מאז הכתיבה. בנורה מה שנקרא עכשיו:
- `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)`
- `the bit read = LEDG0`
- כתבו 1. אחרי כמה עליות שעון הביט נעלם?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`
- **התשובה:** `SW2 + SW0`

**שלב 2**

- בלוח אותו תא:
- `the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)`
- `the bit read = LEDG0`
- כדי לא לאבד את הביט צריך לרענן אותו (לכתוב שוב).
- אחרי כמה עליות שעון בלי כתיבה, לכל היותר, צריך לרענן?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0`
- **התשובה:** `SW2`

### Q50 - קובץ אוגרים

- **מתגים ונורות:** `read: A1 = SW5 SW4 (HEX1)     RD1 = LEDG0 (now)     write: A3 = SW9 SW8 (HEX3)     WD3 = SW7     WE3 = SW6     LEDG7..LEDG4 = R3..R0 after the next clock edge     answer: SW3..SW0`
- **מה מוסתר בלוח:** `register 0 hardwired to 0, now R3..R0 = 0000`
- **שלבים:** 2

**שלב 1**

- בלוח קובץ אוגרים של 4 אוגרים של ביט אחד: פורט קריאה ופורט כתיבה.
- `read: A1 = SW5 SW4 (HEX1)     RD1 = LEDG0 (now)`
- מה כתוב עכשיו בארבעת האוגרים? קראו את כולם.
- `SW3..SW0 = R3..R0`
- **התשובה:** `all down`

**שלב 2**

- בלוח אותו קובץ אוגרים. הנורות העליונות מראות את האוגרים אחרי עליית השעון הבאה:
- `write: A3 = SW9 SW8 (HEX3)     WD3 = SW7     WE3 = SW6`
- `LEDG7..LEDG4 = R3..R0 after the next clock edge`
- כתבו 1 לכל אחד מארבעת האוגרים. אולי אחד מחובר תמיד ל-0. איזה?
- `R0 = all down     R1 = SW0     R2 = SW1`
- `R3 = SW1+SW0     none = SW2`
- **התשובה:** `all down`

