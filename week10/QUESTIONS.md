# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`lesson.txt`).

## נושא 1 - יחידת חישוב ודגלים

40 דקות, 17 שאלות: Q01-Q17

### Q01 - ה-ALU מהשקופית

- **מתגים ונורות:** `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח ה-
- `ALU`
- של שקופיות 3-5, ב-4 ביטים:
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- הדוגמה של שקופית 5: חיבור.
- `A + B:   ALUControl = 00`
- מה התוצאה?
- `SW3..SW0 = Result`

**שלב 2**

- הדוגמה של שקופיות 3-4:
- `A OR B:   ALUControl = 11`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- מה התוצאה?
- `SW3..SW0 = Result`

**שלב 3**

- חיסור:
- `A - B:   ALUControl = 01`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- מה התוצאה?
- `SW3..SW0 = Result`

### Q02 - הדגלים מהשקופית

- **מתגים ונורות:** `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     answer: SW0`
- **שלבים:** 3

**שלב 1**

- בלוח ה-
- `ALU`
- של שקופית 6, בלי נורות לדגלים:
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- שקופית 8: הדגל
- `N`
- הוא הביט השמאלי של התוצאה.
- `A - B:   ALUControl = 01`
- האם
- `N = 1`
- `?`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- שקופית 9: הדגל
- `Z = 1`
- כשכל הביטים של התוצאה 0.
- `A AND B:   ALUControl = 10`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- האם
- `Z = 1`
- `?`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 3**

- שקופית 10: הדגל
- `C`
- הוא הנשא שיוצא מהמחבר.
- `A + B:   ALUControl = 00`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- האם
- `C = 1`
- ? (האם הסכום גדול מ-15)
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q03 - SLT מהשקופית

- **מתגים ונורות:** `A = HEX3     B = HEX2     ALUControl = SW9 SW8 SW7 (HEX0)     Result = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח ה-
- `ALU`
- של שקופיות 16-17, עם
- `SLT`
- ועם תיקון הגלישה:
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 SW7 (HEX0)     Result = LEDR3..LEDR0`
- `000 add     001 subtract     010 and     011 or     101 slt`
- חיסור: מה התוצאה?
- `A - B:   ALUControl = 001`
- `SW3..SW0 = Result`

**שלב 2**

- עכשיו
- `SLT`
- (עם סימן):
- `Result = (A < B) ? 0001 : 0000     ALUControl = 101`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 SW7 (HEX0)     Result = LEDR3..LEDR0`
- מה התוצאה?
- `SW3..SW0 = Result`

### Q04 - המחבר שבתוך ה-ALU

- **מתגים ונורות:** `A = HEX3     B = HEX2     ALUControl0 = SW9 (HEX0)     2nd input = LEDR5..LEDR2     Sum = LEDR9..LEDR6     Cin = LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המחבר שבתוך ה-
- `ALU`
- של שקופית 5:
- `A = HEX3     B = HEX2     ALUControl0 = SW9 (HEX0)     2nd input = LEDR5..LEDR2     Sum = LEDR9..LEDR6     Cin = LEDR0`
- הדוגמה של שקופית 5: בחיבור
- `ALUControl0 = 0:   Cin = 0,   2nd input = B`
- בחיסור:
- `ALUControl0 = 1`
- מה הכניסה השנייה של המחבר?
- `SW3..SW0 = 2nd input`

**שלב 2**

- ומה הסכום בחיסור?
- `ALUControl0 = 1:   Sum = A + ~B + Cin`
- `A = HEX3     B = HEX2     ALUControl0 = SW9 (HEX0)     2nd input = LEDR5..LEDR2     Sum = LEDR9..LEDR6     Cin = LEDR0`
- `SW3..SW0 = Sum`

### Q05 - דגל הגלישה מהשקופית

- **מתגים ונורות:** `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     N Z C V = LEDR7 LEDR6 LEDR5 LEDR4     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בלוח ה-
- `ALU`
- עם הדגלים של שקופית 13, מספרים עם סימן:
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     N Z C V = LEDR7 LEDR6 LEDR5 LEDR4`
- שקופית 11: גלישה כשמחברים שני מספרים עם אותו סימן ומקבלים תוצאה עם סימן הפוך.
- `A + B:   ALUControl = 00`
- האם
- `V = 1`
- `?`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- שקופית 12: גם בחיסור.
- `A - B:   ALUControl = 01`
- `A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     N Z C V = LEDR7 LEDR6 LEDR5 LEDR4`
- האם
- `V = 1`
- `?`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q06 - השוואה מהטבלה של השקופית

- **מתגים ונורות:** `A = SW9..SW6     B = HEX3     A - B:   N = LEDR3   Z = LEDR2   C = LEDR1   V = LEDR0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח ה-
- `ALU`
- של שקופית 14 מחסר, ורק הדגלים בנורות:
- `A = SW9..SW6     B = HEX3     A - B:   N = LEDR3   Z = LEDR2   C = LEDR1   V = LEDR0`
- שימו
- `A = 0011`
- והעתיקו את הדגלים:
- `SW3..SW0 = LEDR3..LEDR0`

**שלב 2**

- הטבלה של שקופית 14:
- `signed A < B:  N ^ V`
- `A = SW9..SW6     B = HEX3     A - B:   N = LEDR3   Z = LEDR2   C = LEDR1   V = LEDR0`
- עם
- `A = 0011`
- , האם
- `A < B`
- עם סימן?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 3**

- הטבלה של שקופית 14:
- `unsigned A < B:  ~C`
- `A = SW9..SW6     B = HEX3     A - B:   N = LEDR3   Z = LEDR2   C = LEDR1   V = LEDR0`
- עם
- `A = 0011`
- , האם
- `A < B`
- בלי סימן?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q07 - XOR מהשקופית

- **מתגים ונורות:** `A = SW9..SW6     B = HEX3     Result = A XOR B = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- שקופית 15: פעולה נוספת של ה-
- `ALU`
- `:`
- `Result = A XOR B`
- `A = SW9..SW6     B = HEX3     Result = A XOR B = LEDR3..LEDR0`
- שימו
- `A = 1111`
- . מה התוצאה?
- `SW3..SW0 = Result`

**שלב 2**

- איזה
- `A`
- נותן תוצאה אפס?
- `Result = 0000`
- `A = SW9..SW6     B = HEX3     Result = A XOR B = LEDR3..LEDR0`
- `SW3..SW0 = A`

### Q08 - הקודים של ה-ALU

- **מתגים ונורות:** `A = SW9 SW8 (HEX3)     B = SW7 SW6 (HEX2)     ALUControl = SW5 SW4 (HEX1)     Result = LEDR1 LEDR0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח
- `ALU`
- של 2 ביטים, אבל הקודים של הפעולות מעורבבים.
- `A = SW9 SW8     B = SW7 SW6     ALUControl = SW5 SW4     Result = LEDR1 LEDR0`
- מה הקוד של
- `AND`
- `?`
- `SW1 SW0`

**שלב 2**

- מה הקוד של
- `OR`
- `?`
- `SW1 SW0`

**שלב 3**

- מה הקוד של חיבור?
- `add:   SW1 SW0`

### Q09 - פעולה ומספר מוסתרים

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     Result = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 4

**שלב 1**

- בלוח
- `ALU`
- שהפעולה וה-
- `B`
- שלו מוסתרים.
- `A = SW9..SW6     Result = LEDR3..LEDR0`
- שימו
- `A = 0000`
- והעתיקו את התוצאה:
- `SW3..SW0 = LEDR3..LEDR0`

**שלב 2**

- עכשיו
- `A = 1111`
- והעתיקו:
- `SW3..SW0 = LEDR3..LEDR0`

**שלב 3**

- איזו פעולה?
- `add = all down     subtract = SW0     and = SW1     or = SW1+SW0`

**שלב 4**

- מה
- `B`
- `?`
- `SW3..SW0`

### Q10 - דגל האפס בפעולת וגם

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     Z = LEDR0 (of A AND B, B hidden)     answer: SW4..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח
- `ALU`
- שעושה
- `AND`
- בין
- `A`
- למספר מוסתר, ורק דגל האפס מוצג:
- `Result = A AND B     Z = LEDR0     A = SW9..SW6`
- שימו
- `A = 0001`
- . האם
- `Z`
- דולק?
- דולק - הרימו:
- `SW0`
- כבוי - השאירו למטה.

**שלב 2**

- `Z = LEDR0     A = SW9..SW6`
- מה המספר המוסתר?
- `B = ?     SW3..SW0`

**שלב 3**

- `Z = LEDR0     A = SW9..SW6`
- לכמה ערכים של
- `A`
- הדגל
- `Z`
- דולק?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q11 - דגלי ה-ALU

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     Result = LEDR7..LEDR4     flags = LEDR3..LEDR0 (hidden order)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח
- `ALU`
- שמחסר מ-
- `A`
- מספר מוסתר, והדגלים בנורות בסדר מוסתר:
- `Result = A - B = LEDR7..LEDR4     N Z C V = LEDR3..LEDR0 (in some order)`
- איזו נורה היא
- `Z`
- (התוצאה אפס)?
- `LEDR0 = all down     LEDR1 = SW0     LEDR2 = SW1     LEDR3 = SW1+SW0`

**שלב 2**

- איזו נורה היא
- `N`
- (התוצאה שלילית)?
- `LEDR0 = all down     LEDR1 = SW0     LEDR2 = SW1     LEDR3 = SW1+SW0`

**שלב 3**

- מה המספר המוסתר?
- `B = ?     SW3..SW0`

### Q12 - דגל הנשא בחיסור

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     C = LEDR0 (of A - B, B hidden)     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח
- `ALU`
- שמחסר מ-
- `A`
- מספר מוסתר, ורק דגל הנשא מוצג:
- `Result = A - B = A + ~B + 1     C = LEDR0     A = SW9..SW6`
- מה הערך הקטן ביותר של
- `A`
- שנותן נשא?
- `SW3..SW0`

**שלב 2**

- `C = LEDR0     A = SW9..SW6`
- לכמה ערכים של
- `A`
- יש נשא?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q13 - דגל הגלישה

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     Result = LEDR3..LEDR0     V = LEDR4     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח
- `ALU`
- שמחבר ל-
- `A`
- מספר מוסתר:
- `Result = A + B     V = LEDR4`
- מה המספר המוסתר?
- `B = ?     SW3..SW0`

**שלב 2**

- שימו
- `A = 0111`
- (המספר החיובי הגדול). האם יש גלישה?
- יש - הרימו:
- `SW0`
- אין - השאירו למטה.

### Q14 - גלישה בחיסור

- **מתגים ונורות:** `A = SW9..SW6 (HEX0, signed)     V = LEDR0 (of A - B, B hidden)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח
- `ALU`
- שמחסר מ-
- `A`
- מספר מוסתר עם סימן, ורק דגל הגלישה מוצג:
- `Result = A - B     V = LEDR0     A = SW9..SW6`
- שימו
- `A = 1000`
- (מינוס 8). האם יש גלישה?
- יש - הרימו:
- `SW0`
- אין - השאירו למטה.

**שלב 2**

- `V = LEDR0     A = SW9..SW6`
- לכמה ערכים של
- `A`
- יש גלישה?
- `8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 3**

- `V = LEDR0     A = SW9..SW6`
- מה המספר המוסתר, במשלים ל-2?
- `B = ?     SW3..SW0`

### Q15 - השוואה לפי הדגלים

- **מתגים ונורות:** `N Z C V = LEDR3 LEDR2 LEDR1 LEDR0 (of A - B)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- ה-
- `ALU`
- חיסר שני מספרים מוסתרים, ורק הדגלים מוצגים:
- `A - B:   N = LEDR3   Z = LEDR2   C = LEDR1   V = LEDR0`
- האם המספרים שווים?
- `A == B:  Z`
- שווים - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- האם
- `A < B`
- עם סימן?
- `signed A < B:  N ^ V`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 3**

- האם
- `A < B`
- בלי סימן?
- `unsigned A < B:  ~C`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q16 - איזו השוואה בנורה?

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     B = HEX1     LEDR0 = a comparison of A and B (from the flags of A - B)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח השוואה אחת בין
- `A`
- ל-
- `B`
- , מחושבת מהדגלים של החיסור:
- `A = SW9..SW6 (HEX0)     B = HEX1     LEDR0 = (A ? B)`
- ההשוואה עם סימן או בלי סימן? (נסו גם מספרים שהביט השמאלי שלהם 1)
- `signed = all down     unsigned = SW0`

**שלב 2**

- `A = SW9..SW6 (HEX0)     B = HEX1     LEDR0 = (A ? B)`
- איזה יחס?
- `A < B = all down     A <= B = SW0     A > B = SW1     A >= B = SW1+SW0`

**שלב 3**

- איזו נוסחה של הדגלים מדליקה את הנורה?
- `N ^ V = all down     ~C = SW0     Z | (N ^ V) = SW1     Z | ~C = SW1+SW0`
- `~Z & ~(N ^ V) = SW2     ~Z & C = SW2+SW0     ~(N ^ V) = SW2+SW1     C = SW2+SW1+SW0`

### Q17 - SLT: עם תיקון הגלישה או בלי

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     SLT result = LEDR0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- בלוח הפעולה
- `SLT`
- של ה-
- `ALU`
- עם מספר מוסתר:
- `Result = (A < B) ? 1 : 0     (signed)`
- בלי תיקון היא בודקת רק את דגל השלילי, ועם תיקון גם את דגל הגלישה. נסו את כל הכניסות והשוו לחשבון.
- `no fix: N     fixed: N ^ V`
- `A = SW9..SW6`
- `N (no fix) = all down     N ^ V (fixed) = SW0`

## נושא 2 - הזזות, כפל וחילוק

40 דקות, 21 שאלות: Q18-Q38

### Q18 - ההזזות מהשקופית

- **מתגים ונורות:** `A = HEX3     shamt = SW9 SW8 (HEX0)     << = LEDR3..LEDR0 (SW7 = 0)     >> = LEDR7..LEDR4 (SW7 = 1)     >>> = LEDR3..LEDR0 (SW7 = 1)     answer: SW3..SW0     SW7 = which LEDs (0 / 1)`
- **שלבים:** 3

**שלב 1**

- בלוח המזיזים של שקופית 20, ב-4 ביטים.
- הדוגמה של שקופית 19:
- `11001 >> 2 = 00110`
- `A = HEX3     shamt = SW9 SW8 (HEX0)     A >> shamt = LEDR7..LEDR4 (SW7 = 1)`
- מה
- `A >> 2`
- `?`
- `SW3..SW0`

**שלב 2**

- הדוגמה של שקופית 19 בהזזה אריתמטית:
- `11001 >>> 2 = 11110`
- `A = HEX3     shamt = SW9 SW8 (HEX0)     A >>> shamt = LEDR3..LEDR0 (SW7 = 1)`
- מה
- `A >>> 2`
- `?`
- `SW3..SW0`

**שלב 3**

- הדוגמה של שקופית 19 בהזזה שמאלה:
- `11001 << 2 = 00100`
- `A = HEX3     shamt = SW9 SW8 (HEX0)     A << shamt = LEDR3..LEDR0 (SW7 = 0)`
- מה
- `A << 2`
- `?`
- `SW3..SW0`

### Q19 - המכפל מהשקופית

- **מתגים ונורות:** `A = HEX3     B = HEX2     P = A x B = LEDR7..LEDR0     answer: SW7..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המכפל של 4 על 4 משקופית 23.
- הדוגמה של שקופית 22:
- `0101 x 0111:   0101 + 0101 << 1 + 0101 << 2 + 0000 << 3`
- לכל ביט של
- `B`
- יש מכפלה חלקית:
- `A`
- אם הביט 1, ואפס אם הביט 0.
- `A = HEX3     B = HEX2`
- כמה מכפלות חלקיות אינן אפס?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- מה המכפלה? (בדקו בנורות)
- `A = HEX3     B = HEX2     P = A x B = LEDR7..LEDR0`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

### Q20 - המחלק מהשקופית

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     B = HEX3     Q = LEDR7..LEDR4     R = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המחלק של 4 על 4 משקופית 27.
- הדוגמה של שקופית 25:
- `1101 / 0010 = 0110 R1`
- `A = SW9..SW6 (HEX0)     B = HEX3     Q = LEDR7..LEDR4     R = LEDR3..LEDR0`
- שימו את המחולק של השקופית:
- `A = 1101`
- מה המנה?
- `Q = ?     SW3..SW0`

**שלב 2**

- `A = 1101`
- `A = SW9..SW6 (HEX0)     B = HEX3     Q = LEDR7..LEDR4     R = LEDR3..LEDR0`
- מה השארית?
- `R = ?     SW3..SW0`

### Q21 - המסובב מהשקופית

- **מתגים ונורות:** `A = HEX3     shamt = SW9 SW8 (HEX0)     A ROR shamt = LEDR7..LEDR4     A ROL shamt = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מסובב של 4 ביטים: הביטים שיוצאים מצד אחד נכנסים מהצד השני.
- הדוגמה של שקופית 19:
- `11001 ROR 2 = 01110`
- `A = HEX3     shamt = SW9 SW8 (HEX0)     A ROR shamt = LEDR7..LEDR4     A ROL shamt = LEDR3..LEDR0`
- מה
- `A ROR 2`
- `?`
- `SW3..SW0`

**שלב 2**

- הדוגמה של שקופית 19 לצד השני:
- `11001 ROL 2 = 00111`
- `A = HEX3     shamt = SW9 SW8 (HEX0)     A ROR shamt = LEDR7..LEDR4     A ROL shamt = LEDR3..LEDR0`
- מה
- `A ROL 1`
- `?`
- `SW3..SW0`

### Q22 - הזזה שמאלה ככפל

- **מתגים ונורות:** `A = HEX3     shamt = SW9 SW8     Y = A << shamt = LEDR7..LEDR0     target = HEX2 HEX1 (hex)     answer: SW7..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מזיז שמאלה של 8 ביטים, ככפל.
- הדוגמה של שקופית 21:
- `00001 << 3 = 01000     (1 x 8 = 8)`
- `A = HEX3     shamt = SW9 SW8     Y = A << shamt = LEDR7..LEDR0`
- שימו
- `shamt = 3`
- . מה
- `Y`
- `?`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

**שלב 2**

- באיזו הזזה
- `Y`
- שווה למספר שבתצוגה?
- `Y = HEX2 HEX1 (hex)`
- `A = HEX3     shamt = SW9 SW8     Y = A << shamt = LEDR7..LEDR0`
- `SW1 SW0 = shamt`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0`

### Q23 - הזזה אריתמטית ימינה כחילוק

- **מתגים ונורות:** `A = SW9..SW5     shamt = HEX3     Y = A >>> shamt = LEDR4..LEDR0     answer: SW4..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מזיז אריתמטי ימינה של 5 ביטים, כחילוק.
- הדוגמה של שקופית 21:
- `10000 >>> 2 = 11100     (-16 / 4 = -4)`
- `A = SW9..SW5     shamt = HEX3     Y = A >>> shamt = LEDR4..LEDR0`
- שימו
- `A = 10000`
- (מינוס 16). מה
- `Y`
- `?`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- הדוגמה של שקופית 21:
- `01000 >>> 1 = 00100     (8 / 2 = 4)`
- `A = SW9..SW5     shamt = HEX3     Y = A >>> shamt = LEDR4..LEDR0`
- שימו
- `A = 01000`
- . מה
- `Y`
- `?`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q24 - מכפלות חלקיות בלוח

- **מתגים ונורות:** `A = HEX3     B = SW9 SW8 (HEX0)     P = A x B = LEDR7..LEDR0     answer: SW5..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המכפל של שקופית 23, והמכפיל רק 2 ביטים:
- `A = HEX3     B = SW9 SW8 (HEX0)     P = A x B = LEDR7..LEDR0`
- שקופית 22: לכל ביט 1 של
- `B`
- יש מכפלה חלקית, מוזזת לפי מקום הביט.
- שימו
- `B = 10`
- . מה
- `P`
- `?`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- שתי מכפלות חלקיות:
- `B = 11:   P = A + (A << 1)`
- `A = HEX3     B = SW9 SW8 (HEX0)     P = A x B = LEDR7..LEDR0`
- מה
- `P`
- `?`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q25 - איזו הזזה?

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     Y = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מזיז של 4 ביטים:
- `A = SW9..SW6     Y = LEDR3..LEDR0`
- איזה סוג הזזה? (נסו גם מספר שהביט השמאלי שלו 1)
- `sll (<<) = all down     srl (>>) = SW0     sra (>>>) = SW1`

**שלב 2**

- בכמה מקומות הוא מזיז?
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q26 - הזזה בכל עליית שעון

- **מתגים ונורות:** `q = SW9..SW6 (HEX0)     q after the next clock edge = LEDR3..LEDR0     HEX3 = the start value     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר שמזיז את עצמו במקום אחד בכל עליית שעון. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:
- `q = SW9..SW6 (HEX0)     q after the next clock edge = LEDR3..LEDR0`
- איזו הזזה?
- `sll (<<) = all down     srl (>>) = SW0     sra (>>>) = SW1`

**שלב 2**

- בלוח אותו אוגר:
- `q = SW9..SW6 (HEX0)     q after the next clock edge = LEDR3..LEDR0`
- `HEX3 = the start value`
- מתחילים בערך שבתצוגה. מה הערך אחרי שתי עליות שעון?
- `SW3..SW0 = q`

**שלב 3**

- בלוח אותו אוגר:
- `q = SW9..SW6 (HEX0)     q after the next clock edge = LEDR3..LEDR0`
- `HEX3 = the start value`
- מתחילים בערך שבתצוגה. אחרי כמה עליות שעון הוא מפסיק להשתנות?
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q27 - הזזה שמאלה = כפל

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = N     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר וכמה מקומות להזיז:
- `HEX3 = A (hex)     HEX2 = N`
- מה
- `A << N`
- `?`
- `A << N = A x 2^N`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

### Q28 - הזזה לוגית ימינה = חילוק שלם

- **מתגים ונורות:** `HEX3 HEX2 = A (decimal)     HEX1 = N     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מספר בלי סימן וכמה מקומות להזיז:
- `HEX3 HEX2 = A (decimal)     HEX1 = N`
- מה
- `A >> N`
- ? (חילוק שלם, בלי שארית)
- `A >> N = A / 2^N`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q29 - הזזה אריתמטית ימינה = חילוק

- **מתגים ונורות:** `A = HEX3 HEX2 (decimal, signed)     N = HEX1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מספר שלילי וכמה מקומות להזיז:
- `HEX3 = minus if A is negative     HEX2 = |A|     HEX1 = N`
- כתבו את המספר במשלים ל-2 ב-4 ביטים:
- `SW3..SW0`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- הזיזו אותו אריתמטית ימינה (ממלאים בביט הסימן):
- `A >>> N`
- `SW3..SW0`

### Q30 - הזזה שמאלה של מספר שלילי

- **מתגים ונורות:** `A = HEX3 HEX2 (decimal, negative)     N = HEX1     answer: SW4..SW0`
- **שלבים:** 3

**שלב 1**

- בתצוגה מספר שלילי וכמה מקומות להזיז:
- `HEX3 = minus     HEX2 = |A|     HEX1 = N`
- כתבו אותו במשלים ל-2 ב-5 ביטים:
- `A`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- הזיזו אותו שמאלה (5 ביטים, ממלאים ב-0):
- `HEX3 = minus     HEX2 = |A|     HEX1 = N`
- `A << N`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 3**

- האם התוצאה ב-5 ביטים עדיין שווה לכפל?
- `HEX3 = minus     HEX2 = |A|     HEX1 = N`
- `A << N == A x 2^N`
- שווה - הרימו:
- `SW0`
- לא (גלישה) - השאירו למטה.

### Q31 - מזיז עם יציאה תקועה

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     shamt = SW5 SW4 (HEX1)     Y = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מזיז של 4 ביטים, ואחת היציאות שלו תקועה:
- `A = SW9..SW6     shamt = SW5 SW4     Y = LEDR3..LEDR0`
- לאיזה כיוון הוא מזיז?
- `sll (<<) = all down     srl (>>) = SW0`

**שלב 2**

- `A = SW9..SW6     shamt = SW5 SW4     Y = LEDR3..LEDR0`
- איזו יציאה תקועה?
- `LEDR0 = all down     LEDR1 = SW0     LEDR2 = SW1     LEDR3 = SW1+SW0`

**שלב 3**

- `A = SW9..SW6     shamt = SW5 SW4     Y = LEDR3..LEDR0`
- על איזה ערך היא תקועה?
- `0 = all down     1 = SW0`

### Q32 - מכפלות חלקיות

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = B (hex)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני מספרים של 4 ביטים:
- `HEX3 = A (hex)     HEX2 = B (hex)`
- המכפלה החלקית של ביט 2 של
- `B`
- היא המספר הראשון אם הביט 1, מוזזת שני מקומות שמאלה. מה היא?
- `PP2 = (B2 ? A : 0) << 2`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- מה המכפלה כולה (8 ביטים)?
- `A x B`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`

### Q33 - מכפל עם מספר מוסתר

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     P = LEDR7..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכפל של 4 על 4 ביטים, והמספר השני מוסתר:
- `P = A x B     A = SW9..SW6     P = LEDR7..LEDR0`
- מה המספר המוסתר?
- `B = ?     SW3..SW0`

**שלב 2**

- כמה ביטים צריך למכפלה של שני מספרים של 4 ביטים?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

### Q34 - מכפל מערך עם שורה שבורה

- **מתגים ונורות:** `A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDR7..LEDR0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מכפל מערך של 4 על 4, ואחת מארבע השורות של המכפלות החלקיות שבורה:
- `A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDR7..LEDR0`
- `PPk = (Bk ? A : 0) << k`
- איזו שורה שבורה?
- `PP0 = all down     PP1 = SW0     PP2 = SW1     PP3 = SW1+SW0`

**שלב 2**

- `A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDR7..LEDR0`
- `PPk = (Bk ? A : 0) << k`
- השורה השבורה תמיד אפס, או תמיד מוסיפה את המספר הראשון?
- `PPk = 0 = all down     PPk = A << k = SW0`

### Q35 - חילוק: מנה ושארית

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = B (hex)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מחולק ומחלק:
- `HEX3 = A (hex)     HEX2 = B (hex)`
- `A / B = Q + R / B`
- מה המנה?
- `Q = ?     SW3..SW0`

**שלב 2**

- ומה השארית?
- `R = ?     SW3..SW0`

### Q36 - מחלק שמראה רק שארית

- **מתגים ונורות:** `A = SW9..SW6 (HEX0)     R = LEDR3..LEDR0 (A / B, B hidden)     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מחלק עם מחלק מוסתר, ורק השארית מוצגת:
- `A / B = Q + R / B     A = SW9..SW6     R = LEDR3..LEDR0`
- מה השארית הגדולה ביותר שרואים?
- `SW3..SW0`

**שלב 2**

- `A = SW9..SW6     R = LEDR3..LEDR0`
- מה המחלק המוסתר?
- `B = ?     SW3..SW0`

**שלב 3**

- מה המנה כשהמחולק הוא 15?
- `A = 1111:   Q = ?     SW3..SW0`

### Q37 - האלגוריתם של המחלק

- **מתגים ונורות:** `HEX3 = A (hex)     HEX2 = B (hex)     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- בתצוגה מחולק ומחלק. האלגוריתם מהשקופית:
- `HEX3 = A (hex)     HEX2 = B (hex)`
- `R' = 0;  for i = 3 to 0:  R = {R' << 1, A[i]};  D = R - B;  if D < 0: Q[i] = 0, R' = R  else: Q[i] = 1, R' = D`
- אחרי הסיבוב הראשון: מה
- `i = 3:   Q[3] = ?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- ומה השארית החלקית אחרי שני סיבובים?
- `i = 3, 2:   R' = ?     SW3..SW0`

**שלב 3**

- מה המנה בסוף?
- `Q = ?     SW3..SW0`

### Q38 - מערך המחלק

- **מתגים ונורות:** `HEX3 = N (bits)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה הרוחב של מחלק מערך (כמו המחלק של 4 על 4 בשקופית):
- `HEX3 = N (bits)`
- כל שורה במערך מחשבת סיבוב אחד של האלגוריתם. כמה שורות?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

**שלב 2**

- כמה ביטים במכפלה של שני מספרים ברוחב הזה?
- `2N`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

## נושא 3 - בודקים

40 דקות, 12 שאלות: Q39-Q50

### Q39 - sillyfunction בלוח

- **מתגים ונורות:** `a = SW9     b = SW8     c = SW7     y = LEDR0     the inputs to apply = HEX3 HEX2 HEX1 (a b c)     answer: SW6..SW0`
- **שלבים:** 2

**שלב 1**

- הלוח הוא
- `sillyfunction`
- של שקופית 31:
- `y = ~b & ~c | a & ~b`
- `a = SW9     b = SW8     c = SW7     y = LEDR0`
- שימו את הכניסות שבתצוגה:
- `HEX3 HEX2 HEX1 = a b c`
- מה
- `y`
- `?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- הבודק הפשוט של שקופית 32 נותן כניסה חדשה כל 10 יחידות זמן:
- `000 at #0     001 at #10     010 at #20     ...     111 at #70`
- מתי הוא נותן את הכניסות שבתצוגה?
- `HEX3 HEX2 HEX1 = a b c`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

### Q40 - שורה מקובץ הווקטורים

- **מתגים ונורות:** `a = SW9     b = SW8     c = SW7     y = LEDR0     HEX3 HEX2 HEX1 = a b c     HEX0 = yexpected     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שורה מהקובץ
- `example.txt`
- של שקופית 36:
- `abc_yexpected`
- `HEX3 HEX2 HEX1 = a b c     HEX0 = yexpected`
- הלוח הוא המעגל הנבדק:
- `a = SW9     b = SW8     c = SW7     y = LEDR0`
- שימו את הכניסות של השורה. מה
- `y`
- `?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- הבודק של שקופית 35 משווה את
- `y`
- ל-
- `yexpected`
- `.`
- `a = SW9     b = SW8     c = SW7     y = LEDR0`
- `HEX3 HEX2 HEX1 = a b c     HEX0 = yexpected`
- האם הבדיקה עוברת?
- עוברת - הרימו:
- `SW0`
- שגיאה - השאירו למטה.

### Q41 - שורה בקובץ הווקטורים של ה-ALU

- **מתגים ונורות:** `HEX3 = A     HEX2 = B     HEX1 = Result expected     ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0     answer: SW1 SW0`
- **שלבים:** 1

**שלב 1**

- קובץ וקטורים (שקופית 34) ל-
- `ALU`
- של שקופית 5. כל שורה:
- `A_B_ALUControl_Result`
- בשורה שבתצוגה חסר הקוד:
- `HEX3 = A     HEX2 = B     HEX1 = Result expected`
- הלוח הוא ה-
- `ALU`
- הנבדק:
- `ALUControl = SW9 SW8 (HEX0)     Result = LEDR3..LEDR0`
- איזה קוד נותן את התוצאה הצפויה?
- `00 add = all down     01 subtract = SW0     10 and = SW1     11 or = SW1+SW0`

### Q42 - בדיקת המכפל עם וקטור

- **מתגים ונורות:** `HEX3 = A     HEX2 = B     HEX1 HEX0 = Pexpected (hex)     A = SW9..SW6     B = HEX2     P = LEDR7..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- שורה מקובץ הווקטורים של המכפל של שקופית 23:
- `A_B_Pexpected`
- `HEX3 = A     HEX2 = B     HEX1 HEX0 = Pexpected (hex)`
- הלוח הוא המכפל הנבדק:
- `A = SW9..SW6     B = HEX2     P = LEDR7..LEDR0`
- שימו את
- `A`
- של השורה. מה ארבעת הביטים הימניים של המכפלה בלוח?
- `SW3..SW0 = LEDR3..LEDR0`

**שלב 2**

- הבודק משווה את
- `P`
- ל-
- `Pexpected`
- `.`
- `HEX3 = A     HEX2 = B     HEX1 HEX0 = Pexpected (hex)`
- `A = SW9..SW6     B = HEX2     P = LEDR7..LEDR0`
- האם הבדיקה עוברת?
- עוברת - הרימו:
- `SW0`
- שגיאה - השאירו למטה.

### Q43 - בדיקת המחלק עם וקטור

- **מתגים ונורות:** `HEX3 = A     HEX2 = B     HEX1 = Qexpected     HEX0 = Rexpected     A = SW9..SW6     B = HEX2     Q = LEDR7..LEDR4     R = LEDR3..LEDR0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- שורה מקובץ הווקטורים של המחלק של שקופית 27:
- `A_B_Qexpected_Rexpected`
- `HEX3 = A     HEX2 = B     HEX1 = Qexpected     HEX0 = Rexpected`
- הלוח הוא המחלק הנבדק:
- `A = SW9..SW6     B = HEX2     Q = LEDR7..LEDR4     R = LEDR3..LEDR0`
- שימו את
- `A`
- של השורה. מה המנה בלוח?
- `SW3..SW0 = Q`

**שלב 2**

- הבודק משווה את
- `Q`
- ואת
- `R`
- לערכים הצפויים.
- `HEX3 = A     HEX2 = B     HEX1 = Qexpected     HEX0 = Rexpected`
- `A = SW9..SW6     B = HEX2     Q = LEDR7..LEDR4     R = LEDR3..LEDR0`
- האם הבדיקה עוברת?
- עוברת - הרימו:
- `SW0`
- שגיאה - השאירו למטה.

### Q44 - שורה בקובץ הווקטורים

- **מתגים ונורות:** `a = SW9   b = SW8   c = SW7   y = LEDR0   the line to write = HEX3 HEX2 HEX1 (a b c)   answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- הלוח הוא מעגל, ואתם כותבים לו קובץ וקטורים. כל שורה היא
- `abc_yexpected`
- `a = SW9   b = SW8   c = SW7   y = LEDR0`
- כתבו את השורה של הכניסות שבתצוגה:
- `HEX3 HEX2 HEX1 = a b c`
- `SW3 SW2 SW1 = a b c     SW0 = y`

### Q45 - מה הבודק רואה בזמן נתון?

- **מתגים ונורות:** `a = SW9   b = SW8   c = SW7   y = LEDR0 (dut)     t = HEX3 HEX2 (decimal)     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- בודק פשוט נותן את הכניסות אחת אחרי השנייה, כל אחת אחרי 10 יחידות זמן:
- `000 at #0     001 at #10     010 at #20     ...     111 at #70`
- בתצוגה זמן:
- `t = HEX3 HEX2 (decimal)`
- אילו כניסות מקבל המעגל בזמן הזה?
- `SW2 SW1 SW0 = a b c`

**שלב 2**

- הלוח הוא המעגל הנבדק:
- `a = SW9   b = SW8   c = SW7   y = LEDR0 (dut)`
- מה היציאה בזמן שבתצוגה?
- `t = HEX3 HEX2 (decimal)`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

### Q46 - איזה וקטור נכשל?

- **מתגים ונורות:** `a = SW9     b = SW8     c = SW7     y = LEDR0 (the device under test)     answer: SW2..SW0`
- **שלבים:** 1

**שלב 1**

- הלוח הוא המעגל הנבדק
- `(dut)`
- של
- `sillyfunction`
- . קובץ הווקטורים מהשקופית:
- `testvectors (abc_y):   000_1  001_0  010_0  011_0  100_1  101_1  110_0  111_0`
- `a = SW9     b = SW8     c = SW7     y = LEDR0`
- באיזה וקטור הבדיקה נכשלת? כתבו את הכניסות שלו:
- `SW2 SW1 SW0 = a b c`

### Q47 - כמה הודעות שגיאה?

- **מתגים ונורות:** `a = SW9     b = SW8     c = SW7     y = LEDR0     answer: SW3..SW0`
- **שלבים:** 1

**שלב 1**

- הלוח הוא המעגל הנבדק. בודק עצמי מהשקופית בודק את כל 8 השורות של
- `y = ~b ~c + a ~b`
- ומדפיס הודעה על כל שורה שנכשלת:
- `if (y !== expected) $display("failed.");`
- `a = SW9     b = SW8     c = SW7     y = LEDR0`
- כמה הודעות יודפסו?
- `0 = all down`
- `1 = SW0 2 = SW1 3 = SW1+SW0`

### Q48 - שעון בבודק

- **מתגים ונורות:** `HEX3 = high time     HEX2 = low time     (ns)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- השעון בבודק:
- `always begin clk = 1; #H; clk = 0; #L; end`
- `HEX3 = high time     HEX2 = low time     (ns)`
- מה זמן המחזור?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- השעון עולה בזמן 0. מתי העלייה השלישית?
- `0, T, 2T, ...`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q49 - מתי הבודק משווה?

- **מתגים ונורות:** `HEX3 = high time     HEX2 = low time     HEX1 = k     (ns)     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- השעון בבודק עם וקטורים:
- `always begin clk = 1; #H; clk = 0; #L; end`
- `HEX3 = high time     HEX2 = low time     HEX1 = k     (ns)`
- הכניסות נכנסות בעלייה, והיציאות נבדקות בירידה.
- מתי הבדיקה הראשונה?
- `8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- השעון עולה בזמן 0, ואז נכנס הווקטור הראשון.
- `always begin clk = 1; #H; clk = 0; #L; end`
- `HEX3 = high time     HEX2 = low time     HEX1 = k     (ns)`
- מתי נכנס הווקטור
- `k`
- `?`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

**שלב 3**

- מתי נבדקת היציאה של הווקטור
- `k`
- `?`
- `always begin clk = 1; #H; clk = 0; #L; end`
- `HEX3 = high time     HEX2 = low time     HEX1 = k     (ns)`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

### Q50 - כמה וקטורי בדיקה?

- **מתגים ונורות:** `HEX3 = inputs     HEX2 = outputs     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה מעגל צירופי שבודקים אותו עם כל הצירופים:
- `HEX3 = inputs     HEX2 = outputs`
- כמה וקטורים בקובץ?
- `2^inputs`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- כמה ביטים בכל שורה של הקובץ (כניסות ויציאות צפויות)?
- `8 = SW3   4 = SW2   2 = SW1   1 = SW0`

