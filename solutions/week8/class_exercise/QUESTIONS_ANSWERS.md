# פירוט השאלות לפי נושא - עם התשובות (למרצה בלבד)

התשובות של הסטודנט `316009489` (מספר כניסה 746). לכל סטודנט מספרים אחרים - לסטודנט אחר:
`python gen.py --answers <ID>`  או  `answers.bat ce <ID>`.

## נושא 1 - זמני התקנה והחזקה

40 דקות, 16 שאלות: Q01-Q16

### Q01 - המעגל משקופית 10: זמן המחזור

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd of one gate     HEX1 = tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tpd 24, Tc 40`
- **שלבים:** 2

**שלב 1**

- המעגל משקופית 10: המסלול הארוך עובר דרך שלושה שערים.
- `A -> AND -> OR -> NOR -> Y'`
- בתצוגה ההשהיה של שער אחד:
- `HEX2 = tpd of one gate`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה של כל המסלול הארוך?
- `tpd = 3 x tpd(gate)`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW3`

**שלב 2**

- המעגל משקופית 10, וההשהיות בתצוגה:
- `A -> AND -> OR -> NOR -> Y'`
- `HEX3 = tpcq     HEX2 = tpd of one gate     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + 3 x tpd(gate) + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW5 + SW3`

### Q02 - המעגל משקופית 10: אילוץ ההחזקה

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd of one gate     HEX1 = thold     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tccq + tcd = 7 vs thold 6`
- **שלבים:** 1

**שלב 1**

- המעגל משקופית 10: המסלול הקצר עובר דרך שער אחד בלבד.
- `C -> OR -> X'`
- בתצוגה:
- `HEX3 = tccq     HEX2 = tcd of one gate     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים?
- `tccq + tcd > thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

### Q03 - התיקון משקופית 11: מאגר במסלול הקצר

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd of one gate     HEX1 = thold     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tcd 10, tccq + tcd = 16 vs thold 3`
- **שלבים:** 2

**שלב 1**

- התיקון משקופית 11: מוסיפים מאגר במסלול הקצר, ועכשיו יש בו שני שערים.
- `C -> BUF -> OR -> X'`
- בתצוגה ההשהיה של שער אחד:
- `HEX2 = tcd of one gate`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הקצרה ביותר של המסלול הקצר עכשיו?
- `tcd = 2 x tcd(gate)`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW1`

**שלב 2**

- התיקון משקופית 11: במסלול הקצר שני שערים.
- `C -> BUF -> OR -> X'`
- בתצוגה:
- `HEX3 = tccq     HEX2 = tcd of one gate     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים עכשיו?
- `tccq + 2 x tcd(gate) > thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

### Q04 - שקופית 4: מתי היציאה משתנה

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tpcq     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tccq 5 tpcq 6: 1`
- **שלבים:** 1

**שלב 1**

- השקופית של זמני היציאה של דלגלג (4): אחרי עליית השעון
- `Q`
- יכול להתחיל להשתנות אחרי
- `tccq`
- ובטוח יציב אחרי
- `tpcq`
- בשקופית 10:
- `tccq = 30 ps     tpcq = 50 ps  ->  20 ps`
- בתצוגה:
- `HEX3 = tccq     HEX2 = tpcq`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן
- `Q`
- עלול להשתנות?
- `t = tpcq - tccq`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW0`

### Q05 - שקופית 7: התקורה של האוגרים

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tsetup     HEX1 = tpd of the logic     answer: SW8..SW0`
- **מה מוסתר בלוח:** `overhead 10 vs tpd 13`
- **שלבים:** 2

**שלב 1**

- השקופית של אילוץ ההתקנה (7): החלק של האוגרים בזמן המחזור נקרא תקורה.
- `sequencing overhead = tpcq + tsetup`
- בתצוגה:
- `HEX3 = tpcq     HEX2 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה התקורה?
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW3 + SW1`

**שלב 2**

- בדוגמה משקופית 10 התקורה גדולה מהלוגיקה:
- `50 + 60 = 110 ps > tpd = 105 ps`
- בתצוגה:
- `HEX3 = tpcq     HEX2 = tsetup     HEX1 = tpd of the logic`
- `all times in units of 10 ps (5 = 50 ps)`
- האם התקורה גדולה מההשהיה של הלוגיקה?
- `tpcq + tsetup > tpd`
- גדולה - הרימו:
- `SW0`
- לא גדולה - השאירו למטה.
- **התשובה:** `all down`

### Q06 - שקופית 6: איזה מסלול לכל אילוץ

- **מתגים ונורות:** `HEX3 = delay of path A     HEX2 = delay of path B     HEX1 = delay of path C     answer: SW8..SW0`
- **מה מוסתר בלוח:** `setup path A, hold path C`
- **שלבים:** 2

**שלב 1**

- השקופית של המשמעת הדינמית (6): בין שני אוגרים יש השהיה מקסימלית ומינימלית.
- `R1 -> CL -> R2`
- בתצוגה ההשהיות של שלושה מסלולים בין שני האוגרים:
- `HEX3 = delay of path A     HEX2 = delay of path B     HEX1 = delay of path C`
- `all times in units of 10 ps (5 = 50 ps)`
- איזה מסלול בודקים באילוץ ההתקנה?
- `setup: the maximum delay`
- `path A = all down     path B = SW0     path C = SW1`
- **התשובה:** `all down`

**שלב 2**

- אותם שלושה מסלולים בין שני האוגרים:
- `HEX3 = delay of path A     HEX2 = delay of path B     HEX1 = delay of path C`
- `all times in units of 10 ps (5 = 50 ps)`
- איזה מסלול בודקים באילוץ ההחזקה?
- `hold: the minimum delay`
- `path A = all down     path B = SW0     path C = SW1`
- **התשובה:** `SW1`

### Q07 - זמן המחזור המינימלי

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tpcq 4 tpd 5 tsetup 5: Tc 14`
- **שלבים:** 1

**שלב 1**

- בתצוגה ההשהיות של מסלול בין שני אוגרים:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור הקצר ביותר שעוד עובד?
- `Tc >= tpcq + tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1`

### Q08 - שני מסלולים: מי קובע?

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd of path A     HEX1 = tpd of path B     HEX0 = tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `path B, Tc 18`
- **שלבים:** 2

**שלב 1**

- בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:
- `HEX2 = tpd of path A     HEX1 = tpd of path B`
- `all times in units of 10 ps (5 = 50 ps)`
- איזה מסלול קובע את זמן המחזור?
- `path A = all down     path B = SW0`
- **התשובה:** `SW0`

**שלב 2**

- בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:
- `HEX3 = tpcq     HEX2 = tpd of path A     HEX1 = tpd of path B     HEX0 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + max(tpd A, tpd B) + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW1`

### Q09 - כמה זמן מותר ללוגיקה?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 32 tpcq 8 tsetup 7: tpd max 17`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור וההשהיות של האוגרים:
- `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הגדולה ביותר שמותרת ללוגיקה הצירופית בין שני האוגרים?
- `tpd <= Tc - tpcq - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW0`

### Q10 - כמה שערים נכנסים במחזור?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)     HEX0 = tpd of one gate     answer: SW8..SW0`
- **מה מוסתר בלוח:** `8 gates`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן נשאר ללוגיקה?
- `tpd <= Tc - (tpcq + tsetup)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4`

**שלב 2**

- בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)     HEX0 = tpd of one gate`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה שערים כאלה אפשר לשים בטור לכל היותר?
- `n x tpd(gate) <= Tc - (tpcq + tsetup)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3`

### Q11 - תדר השעון המקסימלי

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 4 ns, 250 MHz`
- **שלבים:** 2

**שלב 1**

- בתצוגה ההשהיות של המסלול הארוך, בננו-שניות:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     (ns)`
- מה זמן המחזור המינימלי (ננו-שניות)?
- `Tc >= tpcq + tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2`

**שלב 2**

- מה התדר המקסימלי, במגה-הרץ?
- `f = 1000 / Tc`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW6 + SW5 + SW4 + SW3 + SW1`

### Q12 - אילוץ ההחזקה

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tccq 6 tcd 4 thold 9`
- **שלבים:** 2

**שלב 1**

- בתצוגה ההשהיות של מסלול בין שני אוגרים:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים?
- `tccq + tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- מה ההשהיה הקטנה ביותר שמותרת ללוגיקה כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)
- `tcd >= thold - tccq`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW1 + SW0`

### Q13 - האם המעגל עומד בזמן?

- **מתגים ונורות:** `Tc, tpcq, tpd on page 1; tsetup on page 2     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 26 needs 14`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני דפים (המתג השמאלי מחליף):
- `page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tpd`
- `page 2 (SW9 up):    HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההתקנה מתקיים?
- `Tc >= tpcq + tpd + tsetup`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- בכמה זמן המחזור גדול (או קטן) מהדרוש? כתבו את ההפרש בערך מוחלט:
- `| Tc - (tpcq + tpd + tsetup) |`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2`

### Q14 - הדוגמה מהשקופית: שני שערים בטור

- **מתגים ונורות:** `tpcq tsetup tpd tcd / tccq thold     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 25, hold ok`
- **שלבים:** 2

**שלב 1**

- בין שני האוגרים שני שערים בטור. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd gate   HEX0 = tcd gate`
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + 2 tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3 + SW0`

**שלב 2**

- האם אילוץ ההחזקה מתקיים?
- `tccq + 2 tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

### Q15 - הדוגמה מהשקופית עם יותר שערים

- **מתגים ונורות:** `tpcq tsetup tpd n_long / tccq thold tcd n_short     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 18, tcd min 1`
- **שלבים:** 3

**שלב 1**

- כמו בדוגמה מהשקופית, עם מספר אחר של שערים. הנתונים בדף הראשון:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd of a gate   HEX0 = gates on the long path`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + n_long x tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW1`

**שלב 2**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים?
- `tccq + n_short x tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

**שלב 3**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הקטנה ביותר של שער במסלול הקצר כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)
- `tcd >= (thold - tccq) / n_short     (round up)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW0`

### Q16 - כמה מאגרים לתקן את ההחזקה?

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = thold     HEX1 = tcd of one buffer     answer: SW8..SW0`
- **מה מוסתר בלוח:** `n = 3`
- **שלבים:** 2

**שלב 1**

- בתצוגה מסלול בלי לוגיקה בין שני אוגרים (חוט ישר):
- `HEX3 = tccq     HEX2 = thold     HEX1 = tcd of one buffer`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים בלי שום דבר באמצע?
- `tccq + tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `all down`

**שלב 2**

- כמה מאגרים צריך לפחות להוסיף בדרך כדי שיתקיים?
- `tccq + n tcd >= thold`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`
- **התשובה:** `SW1 + SW0`

## נושא 2 - חלון הדגימה, הטיית שעון ומסנכרנים

40 דקות, 17 שאלות: Q17-Q33

### Q17 - שקופית 14: השעון השני מקדים

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     HEX0 = tskew     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 17 -> 18`
- **שלבים:** 2

**שלב 1**

- השקופית של הטיית שעון (14): מסלול בין שני אוגרים. בתצוגה:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי בלי הטיה?
- `Tc >= tpcq + tpd + tsetup`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW0`

**שלב 2**

- השקופית של הטיית שעון (14): השעון של האוגר השני מקדים.
- `CLK2 is earlier than CLK1`
- בתצוגה:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     HEX0 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי עם ההטיה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW1`

### Q18 - שקופית 15: השעון השני מאחר

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     HEX0 = tskew     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tccq + tcd 4 vs thold + tskew 7`
- **שלבים:** 2

**שלב 1**

- השקופית של הטיית שעון (15): מסלול קצר בין שני אוגרים. בתצוגה:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן אחרי עליית השעון הנתון בכניסה של האוגר השני עוד יציב?
- `tccq + tcd`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2`

**שלב 2**

- השקופית של הטיית שעון (15): השעון של האוגר השני מאחר.
- `CLK2 is later than CLK1`
- בתצוגה:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     HEX0 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים עם ההטיה?
- `tccq + tcd > thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `all down`

### Q19 - המסנכרן משקופיות 22 ו-26

- **מתגים ונורות:** `HEX3 HEX2 HEX1 = f (MHz)     HEX0 = tsetup (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 20 ns, tres 19 ns`
- **שלבים:** 2

**שלב 1**

- המסנכרן משקופיות 22 ו-26: שני דלגלגים בטור, עם שעון בתדר שבתצוגה.
- `D -> F1 -> D2 -> F2 -> Q`
- בתצוגה:
- `HEX3 HEX2 HEX1 = f (MHz)`
- מה זמן המחזור (בננו-שניות)? בשקופית 26:
- `Tc = 1 / 500 MHz = 2 ns`
- `Tc = 1000 / f`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW2`

**שלב 2**

- המסנכרן משקופיות 22 ו-26: שני דלגלגים בטור.
- `D -> F1 -> D2 -> F2 -> Q`
- בתצוגה:
- `HEX3 HEX2 HEX1 = f (MHz)     HEX0 = tsetup (ns)`
- כמה זמן יש לאות
- `D2`
- להתייצב (בננו-שניות)?
- `tres = Tc - tsetup = 1000 / f - tsetup`
- `16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW1 + SW0`

### Q20 - שקופית 13: מה ההטיה?

- **מתגים ונורות:** `HEX3 = CLK arrives at R1     HEX2 = CLK arrives at R2     HEX1 = CLK arrives at R3     answer: SW8..SW0`
- **מה מוסתר בלוח:** `skew 4, R1->R2: hold`
- **שלבים:** 2

**שלב 1**

- השקופית של הטיית שעון (13): השעון לא מגיע לכל האוגרים באותו זמן.
- `tskew = the difference between two clock edges`
- בתצוגה מתי השעון מגיע לשלושה אוגרים:
- `HEX3 = CLK arrives at R1     HEX2 = CLK arrives at R2     HEX1 = CLK arrives at R3`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההטיה במקרה הגרוע ביותר?
- `tskew = latest - earliest`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2`

**שלב 2**

- מסלול מהאוגר הראשון לשני. בתצוגה:
- `HEX3 = CLK arrives at R1     HEX2 = CLK arrives at R2`
- `all times in units of 10 ps (5 = 50 ps)`
- איזה אילוץ בסכנה? (השעון השני מקדים - התקנה, שקופית 14; מאחר - החזקה, שקופית 15)
- `setup = all down     hold = SW0`
- **התשובה:** `SW0`

### Q21 - שקופית 17: לחצן אסינכרוני

- **מתגים ונורות:** `HEX3 = thold     HEX2 = when the button changes, after the clock edge     answer: SW8..SW0`
- **מה מוסתר בלוח:** `thold 2, change 4: ok`
- **שלבים:** 1

**שלב 1**

- השקופית של הפרת המשמעת הדינמית (17): משתמש לוחץ על לחצן בזמן אקראי, בלי קשר לשעון.
- בתצוגה זמן ההחזקה של הדלגלג, ומתי הלחצן משתנה אחרי עליית השעון:
- `HEX3 = thold     HEX2 = when the button changes, after the clock edge`
- `all times in units of 10 ps (5 = 50 ps)`
- האם השינוי מפר את אילוץ ההחזקה?
- `violation: change time < thold`
- מפר - הרימו:
- `SW0`
- בסדר - השאירו למטה.
- **התשובה:** `all down`

### Q22 - שקופית 26: כשלים בשנייה

- **מתגים ונורות:** `HEX3 = N (input changes per second)     HEX2 = K     answer: SW8..SW0`
- **מה מוסתר בלוח:** `15 x 10^-6 / s`
- **שלבים:** 1

**שלב 1**

- הדוגמה משקופית 26: הסיכוי לכשל בכל שינוי של הכניסה, כפול מספר השינויים בשנייה.
- `N = 10     P = 5.6 x 10^-6  ->  5.6 x 10^-5 / second`
- בתצוגה:
- `HEX3 = N (input changes per second)     HEX2 = K`
- `P(failure) per change = K x 10^-6`
- מה הסיכוי לכשל בשנייה? כתבו את המספר שלפני
- `x 10^-6`
- `P(failure)/second = N x K x 10^-6`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1 + SW0`

### Q23 - חלון הדגימה

- **מתגים ונורות:** `HEX3 = tsetup     HEX2 = thold     HEX1 = when D changes, before the edge     answer: SW8..SW0`
- **מה מוסתר בלוח:** `aperture 9, change 7 before the edge: ok`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמני הדלגלג:
- `HEX3 = tsetup     HEX2 = thold     HEX1 = when D changes, before the edge`
- `all times in units of 10 ps (5 = 50 ps)`
- מה רוחב חלון הדגימה סביב עליית השעון?
- `ta = tsetup + thold`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW0`

**שלב 2**

- הנתון משתנה כמה זמן לפני העלייה (הספרה השלישית). האם זה בתוך החלון (סכנה)?
- `inside the aperture: change time < tsetup`
- בתוך החלון - הרימו:
- `SW0`
- בסדר - השאירו למטה.
- **התשובה:** `all down`

### Q24 - זמן המחזור עם הטיית שעון

- **מתגים ונורות:** `tpcq tpd tsetup tskew / tccq tcd thold     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 24, hold ok`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני דפים של מסלול עם הטיית שעון:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tpd   HEX1 = tsetup   HEX0 = tskew`
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = tcd   HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי עם ההטיה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3`

**שלב 2**

- האם אילוץ ההחזקה מתקיים עם ההטיה?
- `tccq + tcd >= thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

### Q25 - כמה הטיה מותרת?

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tskew max 5`
- **שלבים:** 1

**שלב 1**

- בתצוגה ההשהיות של מסלול קצר:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההחזקה עוד עומד בה?
- `tskew <= tccq + tcd - thold`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW0`

### Q26 - מאגרים נגד הטיית שעון

- **מתגים ונורות:** `tccq tcd thold tskew / tcd of a buffer     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `0 buffers`
- **שלבים:** 2

**שלב 1**

- השעון של האוגר השני מגיע מאוחר. הנתונים בדף הראשון:
- `page 1 (SW9 down):  HEX3 = tccq   HEX2 = tcd   HEX1 = thold   HEX0 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים עם ההטיה?
- `tccq + tcd >= thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

**שלב 2**

- מוסיפים מאגרים במסלול. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 = tccq   HEX2 = tcd   HEX1 = thold   HEX0 = tskew`
- `page 2 (SW9 up):    HEX3 = tcd of one buffer`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה מאגרים צריך לפחות כדי שהאילוץ יתקיים? (0 אם כבר מתקיים)
- `tccq + tcd + n x tcd(buffer) >= thold + tskew`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `all down`

### Q27 - הטיה מותרת לפי אילוץ ההתקנה

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tskew max 7`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור, וסכום ההשהיות של המסלול:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההתקנה עוד עומד בה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW1 + SW0`

### Q28 - הטיה לשני הכיוונים

- **מתגים ונורות:** `Tc, setup path / hold path, thold, tskew     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `setup bad, hold ok, max skew 0`
- **שלבים:** 3

**שלב 1**

- ההטיה יכולה להיות לשני הכיוונים. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 HEX0 = tpcq + tpd + tsetup (together)`
- `page 2 (SW9 up):    HEX1 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- אם השעון של האוגר השני מקדים - האם אילוץ ההתקנה מתקיים?
- `Tc >= tpcq + tpd + tsetup + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `all down`

**שלב 2**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- אם השעון של האוגר השני מאחר - האם אילוץ ההחזקה מתקיים?
- `tccq + tcd >= thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.
- **התשובה:** `SW0`

**שלב 3**

- ההטיה יכולה להיות לשני הכיוונים. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 HEX0 = tpcq + tpd + tsetup (together)`
- `page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההטיה הגדולה ביותר ששני האילוצים יחד עומדים בה? (0 אם אפילו בלי הטיה לא)
- `tskew <= min(Tc - (tpcq + tpd + tsetup), tccq + tcd - thold)`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `all down`

### Q29 - מסנכרן

- **מתגים ונורות:** `A = SW9 (the asynchronous input)     Q1 Q2 Q3 = SW8 SW7 SW6 (the flip-flops, now)     Y = LEDG0 = the synchronized output after the next clock edge     answer: SW3..SW0`
- **מה מוסתר בלוח:** `2 flip-flops`
- **שלבים:** 3

**שלב 1**

- בלוח מסנכרן: שרשרת של דלגלגים. הכניסה האסינכרונית נכנסת לדלגלג הראשון, והיציאה היא הדלגלג האחרון.
- `A -> Q1 -> Q2 -> Q3 -> ...`
- `A = SW9 (the asynchronous input)     Q1 Q2 Q3 = SW8 SW7 SW6 (the flip-flops, now)`
- `Y = LEDG0 = the synchronized output after the next clock edge`
- את איזה ערך היציאה מעתיקה בעליית השעון הבאה?
- `A = all down     Q1 = SW0     Q2 = SW1`
- **התשובה:** `SW0`

**שלב 2**

- בלוח אותו מסנכרן:
- `A -> Q1 -> Q2 -> Q3 -> ...`
- `A = SW9 (the asynchronous input)     Q1 Q2 Q3 = SW8 SW7 SW6 (the flip-flops, now)`
- `Y = LEDG0 = the synchronized output after the next clock edge`
- כמה דלגלגים יש במסנכרן? (היציאה היא הדלגלג האחרון)
- `1 = SW0 2 = SW1 3 = SW1+SW0`
- **התשובה:** `SW1`

**שלב 3**

- בלוח אותו מסנכרן.
- מסנכרן טוב בנוי משני דלגלגים לפחות. הוא מספיק?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.
- **התשובה:** `SW0`

### Q30 - כמה זמן לוקח לסנכרן?

- **מתגים ונורות:** `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `24 ns`
- **שלבים:** 1

**שלב 1**

- בתצוגה מסנכרן:
- `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)`
- כמה זמן לכל היותר עובר עד שהכניסה האסינכרונית מגיעה ליציאה (בננו-שניות)?
- `about (flip-flops) x Tc`
- `128 = SW7`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3`

### Q31 - כמה זמן יש להתייצבות?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tres 21`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:
- `HEX3 HEX2 = Tc     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן יש ליציאה של הדלגלג הראשון להתייצב לפני שהשני דוגם אותה?
- `tres = Tc - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW2 + SW0`

**שלב 2**

- הסיכוי לכשל קטן פי
- `e^(tres / tau)`
- כשהזמן גדל. אם מוסיפים עוד דלגלג אחד, כמה זמן התייצבות יש בסך הכול?
- `2 (Tc - tsetup)`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW5 + SW3 + SW1`

### Q32 - כמה עוזר עוד דלגלג?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tres 28, e^7 per flip-flop`
- **שלבים:** 3

**שלב 1**

- בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:
- `HEX3 HEX2 = Tc     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן התייצבות נותן כל דלגלג נוסף?
- `tres = Tc - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3 + SW2`

**שלב 2**

- בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:
- `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau`
- `all times in units of 10 ps (5 = 50 ps)`
- כל דלגלג נוסף מגדיל את הזמן הממוצע בין כשלים פי
- `e^(tres / tau)`
- מה החזקה?
- `tres / tau = (Tc - tsetup) / tau`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW1 + SW0`

**שלב 3**

- בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:
- `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau`
- `all times in units of 10 ps (5 = 50 ps)`
- מסנכרן של 4 דלגלגים במקום 2: פי
- `e`
- בחזקת כמה גדל הזמן הממוצע בין כשלים?
- `2 x (Tc - tsetup) / tau`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1`

### Q33 - הזמן הממוצע בין כשלים

- **מתגים ונורות:** `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K     answer: SW8..SW0`
- **מה מוסתר בלוח:** `MTBF 500 s, doubled N: 250 s`
- **שלבים:** 2

**שלב 1**

- בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:
- `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K`
- `P(failure) per change = 1 / (K x 1000)`
- כל כמה שניות, בממוצע, המסנכרן נכשל?
- `MTBF = 1 / (N x P) = K x 1000 / N`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW8 + SW7 + SW6 + SW5 + SW4 + SW2`

**שלב 2**

- בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:
- `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K`
- `P(failure) per change = 1 / (K x 1000)`
- ואם הכניסה משתנה פי 2 יותר פעמים בשנייה?
- `MTBF = K x 1000 / (2 N)`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW6 + SW5 + SW4 + SW3 + SW1`

## נושא 3 - מקביליות והשהיות בקוד

40 דקות, 17 שאלות: Q34-Q50

### Q34 - העוגיות משקופית 32: בן ואליסה

- **מתגים ונורות:** `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     answer: SW8..SW0`
- **מה מוסתר בלוח:** `latency 24, 5/h`
- **שלבים:** 2

**שלב 1**

- העוגיות משקופית 32: בן ואליסה, כל אחד עם תנור משלו, מכינים מגש בבת אחת. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake`
- מה זמן האחזור של מגש אחד (בדקות)?
- `latency = roll + bake`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3`

**שלב 2**

- העוגיות משקופית 32: בן ואליסה, כל אחד עם תנור משלו. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake`
- כמה מגשים בשעה שניהם יחד?
- `throughput = 2 x 60 / (roll + bake)`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW0`

### Q35 - העוגיות משקופית 33: צנרת

- **מתגים ונורות:** `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     answer: SW8..SW0`
- **מה מוסתר בלוח:** `tray 1 at 14, tray 2 at 25`
- **שלבים:** 2

**שלב 1**

- העוגיות משקופית 33: בן לבד עם שני מגשים. בזמן שמגש אחד בתנור, הוא מכין את הבא. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake`
- מתי מגש 1 יוצא מהתנור (בדקות מההתחלה)?
- `t1 = roll + bake`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1`

**שלב 2**

- העוגיות משקופית 33: מגש 2 נכנס לתנור כשמגש 1 יוצא. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake`
- מתי מגש 2 יוצא מהתנור?
- `t2 = roll + 2 x bake`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3 + SW0`

### Q36 - הקוד משקופית 36: מתי היציאה משתנה

- **מתגים ונורות:** `HEX3 HEX2 = the time c changes (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `c at 29: cb 30, y 36`
- **שלבים:** 2

**שלב 1**

- הקוד משקופית 36, עם ההשהיות שלו:
- `assign #1 {ab, bb, cb} = ~{a, b, c};`
- `assign #2 n1 = ab & bb & cb;`
- `assign #2 n2 = a & bb & cb;`
- `assign #2 n3 = a & bb & c;`
- `assign #4 y = n1 | n2 | n3;`
- כמו בסימולציה בשקופית:
- `a = 0     b = 0     c: 0 -> 1`
- בתצוגה:
- `HEX3 HEX2 = the time c changes (ns)`
- באיזה זמן
- `cb`
- משתנה?
- `t + 1`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW4 + SW3 + SW2 + SW1`

**שלב 2**

- הקוד משקופית 36, עם ההשהיות שלו:
- `assign #1 {ab, bb, cb} = ~{a, b, c};`
- `assign #2 n1 = ab & bb & cb;`
- `assign #2 n2 = a & bb & cb;`
- `assign #2 n3 = a & bb & c;`
- `assign #4 y = n1 | n2 | n3;`
- כמו בסימולציה בשקופית:
- `a = 0     b = 0     c: 0 -> 1`
- בתצוגה:
- `HEX3 HEX2 = the time c changes (ns)`
- השינוי עובר דרך
- `n1`
- ומשנה את היציאה. באיזה זמן
- `y`
- משתנה?
- `c -> cb -> n1 -> y`
- `t + 1 + 2 + 4`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW5 + SW2`

### Q37 - העוגיות משקופיות 30 ו-32: כמה מגשים

- **מתגים ונורות:** `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     HEX0 = trays     answer: SW8..SW0`
- **מה מוסתר בלוח:** `32 min alone, 16 min with Alyssa`
- **שלבים:** 2

**שלב 1**

- העוגיות משקופית 30: בן לבד, בלי מקביליות - מגש אחד בכל פעם. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     HEX0 = trays`
- כמה דקות לוקח להכין את כל המגשים?
- `t = trays x (roll + bake)`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW5`

**שלב 2**

- העוגיות משקופית 32: אליסה עוזרת עם תנור משלה, וכל אחד מכין חצי מהמגשים. בתצוגה:
- `HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     HEX0 = trays`
- כמה דקות עכשיו?
- `t = trays / 2 x (roll + bake)`
- `128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2`
- `2 = SW1   1 = SW0`
- **התשובה:** `SW4`

### Q38 - הקוד משקופיות 38-39: הכניסה a

- **מתגים ונורות:** `HEX3 HEX2 = the time a changes (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `a at 54: n2 56, n1 57`
- **שלבים:** 2

**שלב 1**

- הקוד משקופית 36, עם ההשהיות שלו:
- `assign #1 {ab, bb, cb} = ~{a, b, c};`
- `assign #2 n1 = ab & bb & cb;`
- `assign #2 n2 = a & bb & cb;`
- `assign #2 n3 = a & bb & c;`
- `assign #4 y = n1 | n2 | n3;`
- כמו בשקופית 39, הכניסה
- `a`
- נכנסת ישר לשער של
- `n2`
- `b = 0     c = 0     a: 0 -> 1`
- בתצוגה:
- `HEX3 HEX2 = the time a changes (ns)`
- באיזה זמן
- `n2`
- משתנה?
- `a -> n2`
- `t + 2`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW5 + SW4 + SW3`

**שלב 2**

- הקוד משקופית 36, עם ההשהיות שלו:
- `assign #1 {ab, bb, cb} = ~{a, b, c};`
- `assign #2 n1 = ab & bb & cb;`
- `assign #2 n2 = a & bb & cb;`
- `assign #2 n3 = a & bb & c;`
- `assign #4 y = n1 | n2 | n3;`
- `b = 0     c = 0     a: 0 -> 1`
- בתצוגה:
- `HEX3 HEX2 = the time a changes (ns)`
- אל
- `n1`
- השינוי מגיע דרך המהפך (שקופית 38). באיזה זמן
- `n1`
- משתנה?
- `a -> ab -> n1`
- `t + 1 + 2`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW5 + SW4 + SW3 + SW0`

### Q39 - זמן אחזור וקצב: עוגיות

- **מתגים ונורות:** `HEX3 = minutes of step 1     HEX2 HEX1 = minutes of step 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `latency 12, 5/h, pipelined 6/h`
- **שלבים:** 3

**שלב 1**

- אפייה בשני שלבים (הכנה ואפייה), מגש אחד בכל פעם. הזמנים בתצוגה:
- `HEX3 = minutes of step 1     HEX2 HEX1 = minutes of step 2`
- מה זמן האחזור של מגש אחד (בדקות)?
- `latency = step 1 + step 2`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2`

**שלב 2**

- כמה מגשים בשעה, בלי מקביליות?
- `throughput = 60 / latency`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW0`

**שלב 3**

- עם צנרת (מגש חדש מתחיל הכנה כשהקודם בתנור): כמה מגשים בשעה?
- `throughput = 60 / the longest step`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW2 + SW1`

### Q40 - מקביליות מרחבית

- **מתגים ונורות:** `HEX3 = workers     HEX2 HEX1 = minutes for one tray (latency)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `25/h`
- **שלבים:** 2

**שלב 1**

- כמה עובדים, כל אחד עם תנור משלו. בתצוגה:
- `HEX3 = workers     HEX2 HEX1 = minutes for one tray (latency)`
- כמה מגשים בשעה כולם יחד?
- `throughput = workers x 60 / latency`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW3 + SW0`

**שלב 2**

- ומה זמן האחזור של מגש אחד?
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2`

### Q41 - מקביליות מרחבית וזמנית יחד

- **מתגים ונורות:** `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `8/h`
- **שלבים:** 1

**שלב 1**

- כמה עובדים, וכל אחד עובד בצנרת (הכנה של מגש חדש בזמן שהקודם בתנור). בתצוגה:
- `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2`
- כמה מגשים בשעה, כולם יחד?
- `throughput = workers x 60 / the longest step`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3`

### Q42 - צנרת: זמן מחזור וזמן אחזור

- **מתגים ונורות:** `HEX3 HEX2 HEX1 = the delays of 3 pipeline stages     HEX0 = tpcq + tsetup     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 11`
- **שלבים:** 2

**שלב 1**

- מעגל מחולק ל-3 שלבים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 HEX1 = the delays of 3 pipeline stages     HEX0 = tpcq + tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור הקצר ביותר?
- `Tc = the longest stage + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW1 + SW0`

**שלב 2**

- מה זמן האחזור (מהכניסה עד היציאה, 3 מחזורים)?
- `latency = 3 Tc`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW5 + SW0`

### Q43 - חלוקה לשלבים שווים

- **מתגים ונורות:** `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `Tc 50 -> 26, latency 52`
- **שלבים:** 3

**שלב 1**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור בלי צנרת?
- `Tc = tpd + tpcq + tsetup`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW5 + SW4 + SW1`

**שלב 2**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור עם הצנרת?
- `Tc = tpd / stages + tpcq + tsetup`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW4 + SW3 + SW1`

**שלב 3**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן האחזור עם הצנרת? (הוא גדל בגלל האוגרים)
- `latency = stages x Tc`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`
- **התשובה:** `SW5 + SW4 + SW2`

### Q44 - כמה זמן לכמה אסימונים?

- **מתגים ונורות:** `HEX3 = stages     HEX2 HEX1 = tokens     HEX0 = Tc (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `24 cycles, 168 ns`
- **שלבים:** 3

**שלב 1**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages`
- אחרי כמה מחזורים יוצא האסימון הראשון?
- `latency = stages`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`
- **התשובה:** `SW2`

**שלב 2**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages     HEX2 HEX1 = tokens`
- אחרי כמה מחזורים יוצא האסימון האחרון?
- `cycles = stages + tokens - 1`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW4 + SW3`

**שלב 3**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages     HEX2 HEX1 = tokens     HEX0 = Tc (ns)`
- כמה ננו-שניות עד שהאסימון האחרון יוצא?
- `t = (stages + tokens - 1) x Tc`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`
- **התשובה:** `SW7 + SW5 + SW3`

### Q45 - איפה לשים את האוגר?

- **מתגים ונורות:** `the 4 gate delays / tpcq + tsetup     SW9 = page 2     answer: SW8..SW0`
- **מה מוסתר בלוח:** `cut after 2, Tc 11`
- **שלבים:** 3

**שלב 1**

- שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- `page 2 (SW9 up):    HEX3 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור עכשיו?
- `Tc = tpd1 + tpd2 + tpd3 + tpd4 + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4`

**שלב 2**

- שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- מוסיפים אוגר אחד בתוך השרשרת. אחרי איזה שער כדאי לשים אותו כדי שזמן המחזור יהיה הקצר ביותר?
- `1 = SW0 2 = SW1 3 = SW1+SW0`
- **התשובה:** `SW1`

**שלב 3**

- שרשרת של ארבעה שערים, ואוגר במקום הטוב ביותר. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- `page 2 (SW9 up):    HEX3 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור אז?
- `Tc = max(stage 1, stage 2) + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW1 + SW0`

### Q46 - צנרת על הלוח

- **מתגים ונורות:** `new token = SW9     stages 1..5 now = SW8..SW4 (1 = a token)     stages 1..5 after the next clock edge = LEDG4..LEDG0     answer: SW3..SW0`
- **מה מוסתר בלוח:** `2 stages`
- **שלבים:** 2

**שלב 1**

- בלוח צנרת: בכל עליית שעון כל אסימון עובר לשלב הבא. במתגים השלבים עכשיו, ובנורות השלבים אחרי עליית השעון הבאה.
- בלוח יש מקום ל-5 שלבים, אבל רק חלק מהם קיימים.
- `new token = SW9     stages 1..5 now = SW8..SW4 (1 = a token)`
- `stages 1..5 after the next clock edge = LEDG4..LEDG0`
- כמה שלבים יש?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`
- **התשובה:** `SW1`

**שלב 2**

- בלוח אותה צנרת:
- `new token = SW9     stages 1..5 now = SW8..SW4 (1 = a token)`
- `stages 1..5 after the next clock edge = LEDG4..LEDG0`
- מכניסים אסימון חדש בכל עליית שעון. כמה אסימונים נמצאים בצנרת בבת אחת, כשהיא מלאה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`
- **התשובה:** `SW1`

### Q47 - זמן האחזור של צנרת נסתרת

- **מתגים ונורות:** `stage registers 1..4 = SW9 SW8 SW7 SW6 (1 = a token)     Y = LEDG0 = the output of the last stage     HEX0 = Tc (ns)     answer: SW5..SW0`
- **מה מוסתר בלוח:** `2 stages, Tc 5 ns: 10 ns`
- **שלבים:** 2

**שלב 1**

- בלוח צנרת נסתרת: בכל עליית שעון אסימון עובר שלב אחד, והיציאה היא האוגר של השלב האחרון.
- בלוח מקום ל-4 שלבים, אבל רק חלק מהם קיימים.
- `stage registers 1..4 = SW9 SW8 SW7 SW6 (1 = a token)     Y = LEDG0 = the output of the last stage`
- כמה שלבים יש? (כמה עליות שעון לוקח לאסימון לעבור מהכניסה ליציאה)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`
- **התשובה:** `SW1`

**שלב 2**

- בתצוגה זמן המחזור:
- `HEX0 = Tc (ns)`
- מה זמן האחזור בננו-שניות?
- `latency = stages x Tc`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW1`

### Q48 - השהיות בקוד

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `y after 15 ns`
- **שלבים:** 2

**שלב 1**

- הקוד מהשקופית, וההשהיות בתצוגה:
- `assign #d1 {ab, bb, cb} = ~{a, b, c};`
- `assign #d2 n1 = ab & bb & cb;   (and n2, n3 the same)`
- `assign #d3 y = n1 | n2 | n3;`
- `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)`
- הכניסה הראשונה משתנה בזמן 0 ומשנה את היציאה. מתי היציאה משתנה (בננו-שניות)?
- `a -> y`
- `t = d1 + d2 + d3`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1 + SW0`

**שלב 2**

- ואם רק
- `n1`
- משתנה בזמן 0 - מתי
- `y`
- משתנה?
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW0`

### Q49 - המסלול הקצר בקוד

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `b: 18 ns, a earliest: 11 ns`
- **שלבים:** 2

**שלב 1**

- הקוד מהשקופית, וההשהיות בתצוגה:
- `assign #d1 {ab, bb, cb} = ~{a, b, c};`
- `assign #d2 n1 = ab & bb & cb;`
- `assign #d2 n2 = a & bb & cb;`
- `assign #d2 n3 = a & bb & c;`
- `assign #d3 y = n1 | n2 | n3;`
- `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)`
- הכניסה השנייה משתנה בזמן 0. מתי היציאה משתנה (בננו-שניות)?
- `b -> bb -> n1, n2, n3 -> y`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW1`

**שלב 2**

- הקוד מהשקופית, וההשהיות בתצוגה:
- `assign #d1 {ab, bb, cb} = ~{a, b, c};`
- `assign #d2 n1 = ab & bb & cb;`
- `assign #d2 n2 = a & bb & cb;`
- `assign #d2 n3 = a & bb & c;`
- `assign #d3 y = n1 | n2 | n3;`
- `HEX2 = #d2     HEX1 = #d3     (ns)`
- עכשיו הכניסה הראשונה משתנה בזמן 0. מה הרגע המוקדם ביותר שבו היציאה יכולה להשתנות?
- `the shortest path: a -> n2 -> y`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW1 + SW0`

### Q50 - השהיות בקוד בדיקה

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     HEX0 = #dg     (ns)     answer: SW8..SW0`
- **מה מוסתר בלוח:** `b at 13, y 1 at 14, y 0 at 19`
- **שלבים:** 3

**שלב 1**

- קוד בדיקה ושער, וההשהיות בתצוגה:
- `initial begin`
- `a = 0; b = 0;`
- `#d1 a = 1;`
- `#d2 b = 1;`
- `#d3 a = 0;`
- `end`
- `assign #dg y = a & b;`
- `HEX3 = #d1     HEX2 = #d2     (ns)`
- באיזה זמן
- `b`
- עולה ל-1?
- `t = d1 + d2`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW0`

**שלב 2**

- קוד בדיקה ושער, וההשהיות בתצוגה:
- `initial begin`
- `a = 0; b = 0;`
- `#d1 a = 1;`
- `#d2 b = 1;`
- `#d3 a = 0;`
- `end`
- `assign #dg y = a & b;`
- `HEX3 = #d1     HEX2 = #d2     HEX0 = #dg     (ns)`
- באיזה זמן
- `y`
- עולה ל-1?
- `t = d1 + d2 + dg`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW3 + SW2 + SW1`

**שלב 3**

- קוד בדיקה ושער, וההשהיות בתצוגה:
- `initial begin`
- `a = 0; b = 0;`
- `#d1 a = 1;`
- `#d2 b = 1;`
- `#d3 a = 0;`
- `end`
- `assign #dg y = a & b;`
- `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     HEX0 = #dg     (ns)`
- באיזה זמן
- `y`
- חוזרת ל-0?
- `t = d1 + d2 + d3 + dg`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`
- **התשובה:** `SW4 + SW1 + SW0`

