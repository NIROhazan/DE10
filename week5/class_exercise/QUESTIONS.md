# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - תפסנים, דלגלגים ומצב

40 דקות, 16 שאלות: Q01-Q16

### Q01 - תפסן קביעה-איפוס מהשקופיות

- **מתגים ונורות:** `S = SW9     R = SW8     Q = LEDG1     Q' = LEDG0     case 1 = HEX3 HEX2     case 2 = HEX1 HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח תפסן הקביעה-איפוס מהשקופיות, משני שערים:
- `SR latch:   N1 = NOR(R, Q')     N2 = NOR(S, Q)`
- `S = SW9     R = SW8     Q = LEDG1     Q' = LEDG0`
- שימו את המתגים כמו במצב 1 שבתצוגה, והעתיקו את הנורות:
- `case 1:   S = HEX3     R = HEX2`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- עכשיו שימו את המתגים כמו במצב 2 שבתצוגה, והעתיקו שוב:
- `case 2:   S = HEX1     R = HEX0`
- `S = SW9     R = SW8     Q = LEDG1     Q' = LEDG0`
- `SW1 SW0 = LEDG1 LEDG0`

### Q02 - תפסן D מהשקופיות

- **מתגים ונורות:** `CLK = SW9     D = SW8   S = LEDG3     R = LEDG2     Q = LEDG1     Q' = LEDG0     case 1 = HEX3 HEX2     case 2 = HEX1 HEX0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח תפסן
- `D`
- מהשקופיות: תפסן קביעה-איפוס ושני שערי וגם.
- `S = CLK & D     R = CLK & ~D`
- `CLK = SW9     D = SW8`
- `S = LEDG3     R = LEDG2     Q = LEDG1     Q' = LEDG0`
- שימו את המתגים כמו במצב 1 שבתצוגה, והעתיקו את הנורות:
- `case 1:   CLK = HEX3     D = HEX2`
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- עכשיו שימו את המתגים כמו במצב 2 שבתצוגה (קודם את השעון, אחר כך את הנתון), והעתיקו שוב:
- `case 2:   CLK = HEX1     D = HEX0`
- `CLK = SW9     D = SW8`
- `S = LEDG3     R = LEDG2     Q = LEDG1     Q' = LEDG0`
- `SW3..SW0 = LEDG3..LEDG0`

### Q03 - המעגל הדו-יציב מהשקופיות

- **מתגים ונורות:** `HEX3 = Q     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המעגל הדו-יציב מהשקופיות: שני מהפכים, היציאה של כל אחד היא הכניסה של השני.
- `I1: Q -> Q'     I2: Q' -> Q`
- `HEX3 = Q (the stored bit)`
- מה היציאה של המהפך הראשון?
- `Q' = ?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- העתיקו את שני הצמתים של המעגל:
- `HEX3 = Q`
- `SW1 = Q     SW0 = Q'`

### Q04 - דלגלג D מהשקופיות - עליית השעון

- **מתגים ונורות:** `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6     Q now = LEDG0     case = HEX3..HEX0     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הדלגלג
- `D`
- מהשקופיות: הוא דוגם את הנתון רק כשהשעון עולה מ-0 ל-1.
- `D flip-flop:   Q = D only on the rising edge of CLK`
- אין שעון: השעון לפני ועכשיו על מתגים, והנורה מראה את היציאה עכשיו.
- `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6     Q now = LEDG0`
- שימו את המתגים כמו בתצוגה. מה הנורה מראה?
- `case:   CLK before = HEX3     CLK now = HEX2     D = HEX1     Q before = HEX0`
- הנורה דולקת - הרימו:
- `SW0`
- הנורה כבויה - השאירו למטה.

**שלב 2**

- עכשיו הפכו רק את המתג של השעון לפני. מה הנורה מראה?
- `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6     Q now = LEDG0`
- הנורה דולקת - הרימו:
- `SW0`
- הנורה כבויה - השאירו למטה.

### Q05 - דלגלג D מבפנים - שני תפסנים

- **מתגים ונורות:** `CLK = SW9     D = SW8     N1 before = SW7     Q before = SW6   N1 = LEDG1     Q = LEDG0     case = HEX3..HEX0     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הדלגלג מהשקופיות: שני תפסנים בטור עם שעונים הפוכים.
- `D -> L1 -> N1 -> L2 -> Q     L1: transparent when CLK = 0     L2: transparent when CLK = 1`
- `CLK = SW9     D = SW8     N1 before = SW7     Q before = SW6`
- `N1 = LEDG1     Q = LEDG0`
- שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:
- `case:   CLK = HEX3     D = HEX2     N1 before = HEX1     Q before = HEX0`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- עכשיו השעון עולה: העתיקו את הנורה של
- `N1`
- למתג שלה, הרימו את השעון, והעתיקו שוב:
- `SW7 = LEDG1     SW9 = 1`
- `CLK = SW9     D = SW8     N1 before = SW7     Q before = SW6`
- `N1 = LEDG1     Q = LEDG0`
- `SW1 SW0 = LEDG1 LEDG0`

### Q06 - תפסן D מול דלגלג D מהשקופיות

- **מתגים ונורות:** `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6   LEDG1, LEDG0 = D latch, D flip-flop (in some order)     case = HEX3..HEX0     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בלוח תפסן
- `D`
- ודלגלג
- `D`
- מהשקופיות, על אותן כניסות.
- `D latch: Q = D while CLK = 1     D flip-flop: Q = D only when CLK rises from 0 to 1`
- `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6`
- `LEDG1, LEDG0 = D latch, D flip-flop (in some order)`
- שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:
- `case:   CLK before = HEX3     CLK now = HEX2     D = HEX1     Q before = HEX0`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- איזו נורה היא הדלגלג? (השעון לא עלה עכשיו - הוא היה 1 גם לפני)
- `CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6`
- `LEDG1, LEDG0 = D latch, D flip-flop (in some order)`
- `LEDG0 = all down     LEDG1 = SW0`

### Q07 - תפסן SR - מה קובע, מה מאפס?

- **מתגים ונורות:** `two switches = SW9 SW8     Q = LEDG1     Q' = LEDG0     answer: SW1 SW0`
- **שלבים:** 4

**שלב 1**

- בלוח תפסן קביעה-איפוס על שני מתגים:
- `SR latch:   Q = LEDG1     Q' = LEDG0`
- באיזה מצב של שני המתגים
- `Q`
- נדלק (קביעה)? העתיקו את המצב:
- `SW1 = SW9     SW0 = SW8     (the switch positions)`

**שלב 2**

- באיזה מצב
- `Q`
- נכבה (איפוס)? העתיקו את המצב:
- `SW1 = SW9     SW0 = SW8     (the switch positions)`

**שלב 3**

- באיזה מצב התפסן זוכר (הנורות לא משתנות)? העתיקו את המצב:
- `SW1 = SW9     SW0 = SW8     (the switch positions)`

**שלב 4**

- תפסן משערי
- `NOR`
- קובע ומאפס כשהכניסה 1, ותפסן משערי
- `NAND`
- כשהכניסה 0. איזה זה?
- `NOR = all down     NAND = SW0`

### Q08 - תפסן קביעה-איפוס עם אפשור

- **מתגים ונורות:** `S, R, EN = SW9, SW8, SW7 (in some order)     Q = LEDG1     Q' = LEDG0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח תפסן קביעה-איפוס עם אפשור על שלושה מתגים:
- `S, R, EN = SW9, SW8, SW7 (in some order)`
- `Q = LEDG1     Q' = LEDG0`
- איזה מתג הוא האפשור? (במצב אחד שלו הנורות קפואות, מה שלא תעשו בשני האחרים)
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

**שלב 2**

- האפשור פעיל כשהמתג שלו
- `EN`
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

**שלב 3**

- כשהאפשור פעיל: איזה מתג מדליק את
- `Q = LEDG1`
- (קביעה)?
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

### Q09 - תפסן D - שעון ונתון

- **מתגים ונורות:** `SW9 SW8 SW7     Q = LEDG0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח תפסן
- `D`
- על שניים משלושת המתגים (השלישי לא מחובר).
- איזה מתג הוא השעון? (כשהוא במצב אחד הנורה הולכת אחרי מתג אחר, ובמצב השני היא קפואה)
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

**שלב 2**

- איזה מתג הוא הנתון (שהנורה הולכת אחריו)?
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

**שלב 3**

- מתי התפסן שקוף (הנורה הולכת אחרי הנתון)?
- כשהשעון למעלה - הרימו:
- `SW0`
- כשהשעון למטה - השאירו למטה.

### Q10 - תפסן D מבפנים

- **מתגים ונורות:** `CLK, D = SW9, SW8 (in some order)     S, R, Q = LEDG2..LEDG0 (in some order)     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח תפסן
- `D`
- שבנוי מתפסן קביעה-איפוס ושני שערי וגם:
- `S = CLK & D     R = CLK & ~D`
- `CLK, D = SW9, SW8 (in some order)`
- `LEDG2 LEDG1 LEDG0 = S, R, Q (in some order)`
- איזה מתג הוא השעון? (כשהוא למטה שום נורה לא משתנה)
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- איזו נורה היא היציאה
- `Q`
- ? (היחידה שזוכרת ערך קודם)
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1`

**שלב 3**

- איזו נורה היא
- `S = CLK & D`
- `?`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1`

### Q11 - ארבעה תפסנים - מי זה מי?

- **מתגים ונורות:** `SW9 SW8     four latches = LEDG3..LEDG0     answer: SW1 SW0`
- **שלבים:** 4

**שלב 1**

- בלוח ארבעה תפסנים על שני המתגים. איזו נורה היא תפסן
- `SR`
- ש-
- `SW9`
- קובע בו (מדליק)?
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 2**

- איזו נורה היא תפסן
- `SR`
- ש-
- `SW8`
- קובע בו?
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 3**

- איזו נורה היא תפסן
- `D`
- שהאפשור שלו
- `SW9`
- (והנתון
- `SW8`
- `)?`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 4**

- ואיזו נורה היא תפסן
- `D`
- שהאפשור שלו
- `SW8`
- `?`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

### Q12 - דלגלג D

- **מתגים ונורות:** `SW9 SW8 SW7     LEDG0 = the output after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג
- `D`
- על אחד משלושת המתגים (השניים האחרים לא מחוברים).
- אין שעון: הנורה מראה את היציאה אחרי עליית השעון הבאה.
- `SW9 SW8 SW7     LEDG0 = the output after the next clock edge`
- איזה מתג הוא הנתון? (רק הוא משנה את הנורה)
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

**שלב 2**

- הנורה מראה את היציאה או את ההפוכה שלה? השוו אותה למתג הנתון.
- `SW9 SW8 SW7     LEDG0 = the output after the next clock edge`
- `Q = all down     Q' = SW0`

### Q13 - תפסן מול דלגלג - צורת גל

- **מתגים ונורות:** `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)     answer: SW7..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח צורת גל של שעון ונתון, בשמונה זמנים משמאל לימין:
- `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)`
- לפני זמן 1 השעון 0 והיציאה 0.
- מה היציאה של תפסן
- `D`
- (שקוף כשהשעון 1) בכל זמן?
- `SW7..SW0 = Q at times 1..8`

**שלב 2**

- ומה היציאה של דלגלג
- `D`
- (דוגם את הנתון רק כשהשעון עולה מ-0 ל-1) בכל זמן?
- `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)`
- לפני זמן 1 השעון 0 והיציאה 0.
- `SW7..SW0 = Q at times 1..8`

### Q14 - דלגלג משני תפסנים

- **מתגים ונורות:** `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)     answer: SW7..SW0`
- **שלבים:** 2

**שלב 1**

- דלגלג בנוי משני תפסנים בטור: הראשון שקוף כשהשעון 0, והשני שקוף כשהשעון 1.
- `D -> L1 -> N1 -> L2 -> Q`
- בלוח צורת גל של שעון ונתון, בשמונה זמנים משמאל לימין:
- `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)`
- לפני זמן 1 שני התפסנים 0.
- מה היציאה של התפסן הראשון בכל זמן?
- `SW7..SW0 = N1 at times 1..8`

**שלב 2**

- ומה היציאה של התפסן השני (שקוף כשהשעון 1, והנתון שלו הוא היציאה של הראשון)?
- `D -> L1 -> N1 -> L2 -> Q`
- `CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)`
- לפני זמן 1 שני התפסנים 0.
- `SW7..SW0 = Q at times 1..8`

### Q15 - כמה מצבים, כמה ביטים?

- **מתגים ונורות:** `HEX3 HEX2 = N states (decimal)     HEX1 = k bits     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- למעגל יש
- `N`
- מצבים. כמה ביטים של מצב צריך לפחות כדי לזכור אותם?
- `HEX3 HEX2 = N (decimal)`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1`

**שלב 2**

- וכמה מצבים לכל היותר אפשר לזכור בעזרת
- `k`
- ביטים?
- `HEX1 = k`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

### Q16 - טבעת של מהפכים - יציבה או מתנדנדת?

- **מתגים ונורות:** `HEX3 = N inverters     HEX2 HEX1 = tpd (ns, decimal)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח טבעת של מהפכים: היציאה של כל מהפך היא הכניסה של הבא.
- `HEX3 = N inverters`
- האם הטבעת מתנדנדת בלי סוף?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- מה זמן המחזור של הנדנוד, בננו-שניות? אם הטבעת יציבה - השאירו הכל למטה.
- `HEX3 = N inverters     HEX2 HEX1 = tpd of one inverter (ns, decimal)`
- `T = 2 N tpd`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

## נושא 2 - אפשור, איפוס, קביעה ואוגרים

40 דקות, 17 שאלות: Q17-Q33

### Q17 - דלגלג עם אפשור מהשקופיות

- **מתגים ונורות:** `EN = SW9     D = SW8     Q now = SW7     LEDG0 = Q after the next clock edge     case = HEX3 HEX2 HEX1     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הדלגלג עם אפשור מהשקופיות: בורר לפני הדלגלג בוחר מה ייכנס בעליית השעון.
- `mux:   EN = 1 -> D     EN = 0 -> Q`
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `EN = SW9     D = SW8     Q now = SW7     LEDG0 = Q after the next clock edge`
- שימו את המתגים כמו בתצוגה, ומה הנורה מראה?
- `EN = HEX3     D = HEX2     Q now = HEX1`
- הנורה דולקת - הרימו:
- `SW0`
- הנורה כבויה - השאירו למטה.

**שלב 2**

- עכשיו הפכו רק את מתג האפשור. מה הנורה מראה?
- `EN = SW9     D = SW8     Q now = SW7     LEDG0 = Q after the next clock edge`
- הנורה דולקת - הרימו:
- `SW0`
- הנורה כבויה - השאירו למטה.

### Q18 - דלגלג עם איפוס או עם קביעה

- **מתגים ונורות:** `D = SW9     Reset or Set = SW8     LEDG0 = Q after the next clock edge     case = HEX3 HEX2     answer: SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משני הדלגלגים מהשקופיות: דלגלג עם איפוס, או דלגלג עם קביעה.
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `D = SW9     Reset or Set = SW8     LEDG0 = Q after the next clock edge`
- שימו את המתגים כמו בתצוגה. מה הנורה מראה?
- `D = HEX3     Reset or Set = HEX2`
- הנורה דולקת - הרימו:
- `SW0`
- הנורה כבויה - השאירו למטה.

**שלב 2**

- איזה שער יש לפני הכניסה של הדלגלג? נסו גם מצבים אחרים של המתגים.
- `D = SW9     Reset or Set = SW8     LEDG0 = Q after the next clock edge`
- `AND:  D & ~Reset  (resettable) = all down     OR:  D | Set  (settable) = SW0`

### Q19 - אוגר של 4 ביטים מהשקופיות

- **מתגים ונורות:** `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח האוגר של 4 ביטים מהשקופיות: ארבעה דלגלגים עם שעון משותף.
- אבל דלגלג אחד מקולקל: היציאה שלו תקועה.
- אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה.
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- שימו
- `D = 0000`
- והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- עכשיו
- `D = 1111`
- והעתיקו:
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 3**

- איזה דלגלג מקולקל?
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `Q0 = all down     Q1 = SW0     Q2 = SW1     Q3 = SW1+SW0`

### Q20 - אוגר עם איפוס מהשקופיות

- **מתגים ונורות:** `Reset = SW9     D[3:0] = SW8..SW5 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge     HEX3 = a number     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר של 4 ביטים מהשקופיות: ארבעה דלגלגים עם שעון משותף ואיפוס משותף.
- אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה.
- `Reset = SW9     D[3:0] = SW8..SW5 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `HEX3 = a number`
- הורידו את האיפוס, שימו ב-
- `D`
- את המספר שב-
- `HEX3`
- והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- עכשיו הרימו את האיפוס, והעתיקו שוב:
- `Reset = SW9     D[3:0] = SW8..SW5 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `HEX3 = a number`
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 3**

- כמה נורות כבו כשהרמתם את האיפוס?
- `Reset = SW9     D[3:0] = SW8..SW5 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `HEX3 = a number`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q21 - דלגלג עם אפשור - ארבע עליות שעון

- **מתגים ונורות:** `EN = LEDR3..LEDR0     D = LEDG3..LEDG0     (edge 1 = the left LED)     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הדלגלג עם אפשור מהשקופיות, בארבע עליות שעון משמאל לימין:
- `EN = 1: Q = D at the edge     EN = 0: Q keeps its value`
- `EN = LEDR3..LEDR0     D = LEDG3..LEDG0     (edge 1 = the left LED)`
- באילו עליות האפשור פעיל? העתיקו:
- `SW3..SW0 = LEDR3..LEDR0`

**שלב 2**

- מה היציאה אחרי כל עלייה? לפני עלייה 1 היציאה 0.
- `EN = LEDR3..LEDR0     D = LEDG3..LEDG0     (edge 1 = the left LED)`
- `SW3..SW0 = Q after edges 1..4`

### Q22 - המעגל המתנדנד מהשקופיות

- **מתגים ונורות:** `X -> Y -> Z -> X  (three inverters)     HEX3 = X     HEX2 = Y     HEX1 = Z  (now)     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח המעגל הבעייתי מהשקופיות: שלושה מהפכים במסלול מעגלי, בלי כניסות.
- כל מהפך הופך את הכניסה שלו אחרי השהיית שער אחת.
- `X -> Y -> Z -> X  (three inverters)     HEX3 = X     HEX2 = Y     HEX1 = Z  (now)`
- מה הצמתים אחרי השהיית שער אחת?
- `SW2 = X     SW1 = Y     SW0 = Z`

**שלב 2**

- ואחרי עוד השהיית שער אחת?
- `X -> Y -> Z -> X  (three inverters)     HEX3 = X     HEX2 = Y     HEX1 = Z  (now)`
- `SW2 = X     SW1 = Y     SW0 = Z`

### Q23 - לוגיקה סינכרונית - שני אוגרים

- **מתגים ונורות:** `A = SW9     R1 now = SW8     R2 now = SW7   LEDG1 = R1 after the next clock edge     LEDG0 = R2 after the next clock edge     case = HEX3..HEX1     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מעגל סינכרוני מהשקופיות: שני אוגרים עם אותו שעון, ומהפך ביניהם.
- `R1 <= A;     R2 <= ~R1;`
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `A = SW9     R1 now = SW8     R2 now = SW7`
- `LEDG1 = R1 after the next clock edge     LEDG0 = R2 after the next clock edge`
- שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:
- `case:   A = HEX3     R1 = HEX2     R2 = HEX1`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- עוד עליית שעון: העתיקו את הנורות למתגי האוגרים, והעתיקו שוב את הנורות:
- `SW8 = LEDG1     SW7 = LEDG0`
- `A = SW9     R1 now = SW8     R2 now = SW7`
- `LEDG1 = R1 after the next clock edge     LEDG0 = R2 after the next clock edge`
- `SW1 SW0 = LEDG1 LEDG0`

### Q24 - דלגלג עם אפשור

- **מתגים ונורות:** `Q = SW9 (now)     EN, D = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם אפשור: בעליית השעון הוא שומר נתון חדש רק כשהאפשור פעיל.
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `Q = SW9 (now)     EN, D = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge`
- איזה מתג הוא האפשור? (כשהוא לא פעיל, הנורה שווה למצב הנוכחי)
- `SW8 = all down     SW7 = SW0`

**שלב 2**

- `Q = SW9 (now)     EN, D = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge`
- מתי האפשור פעיל?
- כשהמתג שלו למעלה - הרימו:
- `SW0`
- כשהוא למטה - השאירו למטה.

### Q25 - איפוס סינכרוני או אסינכרוני

- **מתגים ונורות:** `Q = SW9 (before)     Reset, D = SW8, SW7 (in some order)   LEDG1 = Q now     LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם איפוס (איפוס = 1).
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `Q = SW9 (before)     Reset, D = SW8, SW7 (in some order)`
- `LEDG1 = Q now     LEDG0 = Q after the next clock edge`
- איזה מתג הוא האיפוס? (הוא מכבה את הנורה של אחרי העלייה)
- `SW8 = all down     SW7 = SW0`

**שלב 2**

- הרימו את הערך הקודם ואת האיפוס. האם הנורה של עכשיו כבתה מיד, עוד לפני עליית השעון?
- `Q = SW9 (before)     Reset, D = SW8, SW7 (in some order)`
- `LEDG1 = Q now     LEDG0 = Q after the next clock edge`
- `asynchronous = at once     synchronous = at the next clock edge`
- כבתה מיד - הרימו:
- `SW0`
- נשארה דולקת - השאירו למטה.

### Q26 - קביעה ואיפוס - מי מנצח?

- **מתגים ונורות:** `Q = SW9 (now)     Set, Reset = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם קביעה ואיפוס סינכרוניים (פועלים בעליית השעון).
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `Q = SW9 (now)     Set, Reset = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge`
- איזה מתג הוא הקביעה (מדליק)?
- `SW8 = all down     SW7 = SW0`

**שלב 2**

- `Q = SW9 (now)     Set, Reset = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge`
- הרימו את שניהם. מי מנצח?
- `Set = all down     Reset = SW0`

### Q27 - דלגלג שמתהפך

- **מתגים ונורות:** `Q = SW9 (now)     T = SW8 or SW7 (the other is not connected)     LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם משוב:
- `q <= q ^ T`
- כשהכניסה פעילה, כל עליית שעון הופכת את היציאה.
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `Q = SW9 (now)     T = SW8 or SW7 (the other is not connected)     LEDG0 = Q after the next clock edge`
- איזה מתג הוא הכניסה?
- `SW8 = all down     SW7 = SW0`

**שלב 2**

- `Q = SW9 (now)     T = SW8 or SW7 (the other is not connected)     LEDG0 = Q after the next clock edge`
- מתי הכניסה פעילה?
- כשהמתג שלה למעלה - הרימו:
- `SW0`
- כשהוא למטה - השאירו למטה.

### Q28 - אוגר של 4 ביטים

- **מתגים ונורות:** `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר של 4 ביטים, אבל החוטים מעורבבים.
- אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה.
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- שימו
- `D = 1000`
- והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- עכשיו
- `D = 0100`
- והעתיקו:
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 3**

- ועכשיו
- `D = 0010`
- והעתיקו:
- `D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

### Q29 - אוגר עם קביעה ואיפוס

- **מתגים ונורות:** `D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     LEDG3..LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר של 4 ביטים. בחלק מהדלגלגים יש קביעה ובחלק איפוס, וכולם מחוברים לאותו מתג (סינכרוני).
- אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה.
- `D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     LEDG3..LEDG0 = Q after the next clock edge`
- שימו
- `D = 0000     SW5 = 1`
- כמה נורות דולקות? (כמה דלגלגים עם קביעה)
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- אילו דלגלגים עם קביעה? הרימו את מתג הקביעה-איפוס, והעתיקו את הנורות:
- `D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     LEDG3..LEDG0 = Q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

### Q30 - אוגרים בטור

- **מתגים ונורות:** `D = LEDR7..LEDR0     Q = LEDG7..LEDG0     (cycle 1 = the left LED)     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בין מתג לנורה יש כמה דלגלגים בטור, עם שעון משותף.
- בלוח צורת גל: הנתון בכניסה והיציאה בסוף השרשרת, בכל מחזור שעון משמאל לימין.
- `D = LEDR7..LEDR0     Q = LEDG7..LEDG0     (cycle 1 = the left LED)`
- לפני מחזור 1 כל הדלגלגים 0.
- כמה דלגלגים יש בטור? (בכמה מחזורים היציאה מאחרת)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- בסוף השרשרת יש מהפך?
- `D = LEDR7..LEDR0     Q = LEDG7..LEDG0     (cycle 1 = the left LED)`
- לפני מחזור 1 כל הדלגלגים 0.
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q31 - אוגר הזזה

- **מתגים ונורות:** `Q[3:0] = SW9..SW6 (now, HEX0)     serial in = SW5 or SW4   LEDG3..LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר הזזה: בכל עליית שעון כל ביט זז מקום אחד, וביט חדש נכנס מאחד המתגים.
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `Q[3:0] = SW9..SW6 (now, HEX0)     serial in = SW5 or SW4`
- `LEDG3..LEDG0 = Q after the next clock edge`
- איזה מתג הוא הכניסה?
- `SW5 = all down     SW4 = SW0`

**שלב 2**

- באיזו נורה נכנס הביט החדש?
- `Q[3:0] = SW9..SW6 (now, HEX0)     serial in = SW5 or SW4`
- `LEDG3..LEDG0 = Q after the next clock edge`
- `LEDG0 = all down     LEDG3 = SW0`

**שלב 3**

- יש מהפך בכניסה? (נכנס 1 כשמתג הכניסה למטה)
- `Q[3:0] = SW9..SW6 (now, HEX0)     serial in = SW5 or SW4`
- `LEDG3..LEDG0 = Q after the next clock edge`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q32 - טבעת של דלגלגים

- **מתגים ונורות:** `Q[3:0] = SW9..SW6 (now, HEX0)     LEDG3..LEDG0 = Q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח כמה דלגלגים שמחוברים בטבעת: היציאה של כל אחד היא הכניסה של הבא.
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `Q[3:0] = SW9..SW6 (now, HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- כמה דלגלגים יש? (הנורות של שאר הביטים תמיד כבויות)
- `2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- האם הביט שחוזר מהסוף להתחלה עובר מהפך? (טבעת מפותלת)
- `Q[3:0] = SW9..SW6 (now, HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 3**

- התחילו מ-
- `Q = 0001`
- בטבעת רגילה, או מ-
- `Q = 0000`
- בטבעת מפותלת.
- כדי לעבור עליית שעון אחת: העתיקו את מה שאחרי העלייה למתגי המצב, וקראו שוב.
- `Q[3:0] = SW9..SW6 (now, HEX0)     LEDG3..LEDG0 = Q after the next clock edge`
- אחרי כמה עליות שעון התבנית חוזרת להתחלה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

### Q33 - אוגר עם משוב דרך מחבר

- **מתגים ונורות:** `q = SW9..SW6 (now, HEX0)     HEX1 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר של ספרה, ומחבר במשוב מהיציאה שלו לכניסה שלו:
- `always_ff @(posedge clk)  q <= (q + K) % 10;`
- אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה.
- `q = SW9..SW6 (now, HEX0)     HEX1 = q after the next clock edge`
- שימו
- `q = 0`
- מה
- `K`
- `?`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- מתחילים מאפס. אחרי כמה עליות שעון חוזרים לאפס?
- כדי לעבור עליית שעון אחת: העתיקו את מה שאחרי העלייה למתגי המצב, וקראו שוב.
- `q = SW9..SW6 (now, HEX0)     HEX1 = q after the next clock edge`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0 10 = SW3+SW1`

## נושא 3 - תיאור חומרה סדרתי

40 דקות, 17 שאלות: Q34-Q50

### Q34 - flopr מהשקופיות

- **מתגים ונורות:** `reset = SW9     d = SW8     q before = SW7   LEDG1 = q now     LEDG0 = q after the next clock edge     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הדלגלג עם איפוס מהשקופיות, באחד משני הקודים:
- `36:  always_ff @(posedge clk)              if (reset) q <= 0; else q <= d;`
- `37:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else q <= d;`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `reset = SW9     d = SW8     q before = SW7`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- שימו
- `reset = 1     d = 1     q before = 1`
- והעתיקו את הנורות:
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- איזה קוד בלוח?
- `36:  always_ff @(posedge clk)              if (reset) q <= 0; else q <= d;`
- `37:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else q <= d;`
- `reset = SW9     d = SW8     q before = SW7`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- `36 = all down     37 = SW0`

### Q35 - syncgood או syncbad?

- **מתגים ונורות:** `d = SW9     n1 before = SW8     q before = SW7   LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge     answer: SW1 SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משני המודולים מהשקופיות, בתוך
- `always_ff @(posedge clk) begin ... end`
- `syncgood:  n1 <= d;  q <= n1;`
- `syncbad:   n1 = d;   q = n1;`
- אין שעון: הערכים הקודמים על מתגים, והנורות מראות אותם אחרי עליית שעון אחת.
- `d = SW9     n1 before = SW8     q before = SW7`
- `LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge`
- שימו
- `d = 1     n1 before = 0     q before = 0`
- והעתיקו את הנורות:
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- איזה מודול בלוח?
- `syncgood:  n1 <= d;  q <= n1;`
- `syncbad:   n1 = d;   q = n1;`
- `d = SW9     n1 before = SW8     q before = SW7`
- `LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge`
- `syncgood = all down     syncbad = SW0`

### Q36 - מודול ה-latch מהשקופיות

- **מתגים ונורות:** `clk = SW9     d[3:0] = SW8..SW5 (HEX0)     q = LEDG3..LEDG0     HEX3, HEX2 = two numbers     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מודול ה-
- `latch`
- מהשקופיות, של 4 ביטים:
- `always_latch  if (clk) q <= d;`
- `clk = SW9     d[3:0] = SW8..SW5 (HEX0)     q = LEDG3..LEDG0`
- הרימו את השעון, שימו ב-
- `d`
- את המספר שב-
- `HEX3`
- והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- הורידו את השעון, ואז שימו ב-
- `d`
- את המספר שב-
- `HEX2`
- והעתיקו שוב את הנורות:
- `clk = SW9     d[3:0] = SW8..SW5 (HEX0)     q = LEDG3..LEDG0`
- `SW3..SW0 = LEDG3..LEDG0`

### Q37 - flopren מהשקופיות

- **מתגים ונורות:** `reset = SW9     en = SW8     d[3:0] = SW7..SW4 (HEX0)     HEX3 = q now     HEX2 = a number   LEDG3..LEDG0 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח המודול
- `flopren`
- מהשקופיות, של 4 ביטים:
- `flopren:  always_ff @(posedge clk, posedge reset)`
- `if (reset) q <= 4'b0;  else if (en) q <= d;`
- אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה.
- `reset = SW9     en = SW8     d[3:0] = SW7..SW4 (HEX0)     HEX3 = q now     HEX2 = a number`
- `LEDG3..LEDG0 = q after the next clock edge`
- הרימו את האיפוס, והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- הורידו את האיפוס, הרימו את האפשור, שימו ב-
- `d`
- את המספר שב-
- `HEX2`
- והעתיקו:
- `flopren:  always_ff @(posedge clk, posedge reset)`
- `if (reset) q <= 4'b0;  else if (en) q <= d;`
- `reset = SW9     en = SW8     d[3:0] = SW7..SW4 (HEX0)     HEX3 = q now     HEX2 = a number`
- `LEDG3..LEDG0 = q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 3**

- עכשיו הורידו את האפשור, והעתיקו שוב:
- `flopren:  always_ff @(posedge clk, posedge reset)`
- `if (reset) q <= 4'b0;  else if (en) q <= d;`
- `reset = SW9     en = SW8     d[3:0] = SW7..SW4 (HEX0)     HEX3 = q now     HEX2 = a number`
- `LEDG3..LEDG0 = q after the next clock edge`
- `SW3..SW0 = LEDG3..LEDG0`

### Q38 - syncgood בארבע עליות שעון

- **מתגים ונורות:** `d = LEDR3..LEDR0  (d at edges 1..4, edge 1 = the left LED)     before edge 1: n1 = 0, q = 0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הנתון של
- `syncgood`
- מהשקופיות, בארבע עליות שעון:
- `always_ff @(posedge clk) begin  n1 <= d;  q <= n1;  end`
- `d = LEDR3..LEDR0  (d at edges 1..4, edge 1 = the left LED)     before edge 1: n1 = 0, q = 0`
- מה
- `n1`
- אחרי כל עלייה?
- `SW3..SW0 = n1 after edges 1..4`

**שלב 2**

- ומה
- `q`
- אחרי כל עלייה? (הוא מקבל את
- `n1`
- של לפני העלייה)
- `d = LEDR3..LEDR0  (d at edges 1..4, edge 1 = the left LED)     before edge 1: n1 = 0, q = 0`
- `SW3..SW0 = q after edges 1..4`

### Q39 - assign ו-always_ff מהשקופיות

- **מתגים ונורות:** `a = SW9     b = SW8     q now = SW7   LEDG2 = y     LEDG1 = q now     LEDG0 = q after the next clock edge     case = HEX3..HEX1     answer: SW2..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח הכללים מהשקופיות: לוגיקה צירופית ב-
- `assign`
- ודלגלג ב-
- `always_ff`
- `:`
- `assign y = a & b;`
- `always_ff @(posedge clk)  q <= y;`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `a = SW9     b = SW8     q now = SW7`
- `LEDG2 = y     LEDG1 = q now     LEDG0 = q after the next clock edge`
- שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:
- `case:   a = HEX3     b = HEX2     q now = HEX1`
- `SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0`

**שלב 2**

- עכשיו הפכו רק את
- `a`
- והעתיקו שוב:
- `assign y = a & b;`
- `always_ff @(posedge clk)  q <= y;`
- `a = SW9     b = SW8     q now = SW7`
- `LEDG2 = y     LEDG1 = q now     LEDG0 = q after the next clock edge`
- `SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0`

### Q40 - תפסן בקוד

- **מתגים ונורות:** `clk = SW9     d = SW8     q = LEDG0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח:
- `always_latch  if (?clk) q <= ?d;`
- `clk = SW9     d = SW8     q = LEDG0`
- מתי התפסן שקוף?
- כשהשעון למעלה - הרימו:
- `SW0`
- כשהוא למטה - השאירו למטה.

**שלב 2**

- כשהוא שקוף, הנורה שווה ל-
- `d`
- או הפוכה לו?
- `d = all down     ~d = SW0`

**שלב 3**

- כתבו את הקוד: שני ביטים
- `SW1 = 1 if (clk), 0 if (!clk)     SW0 = 1 for ~d, 0 for d`

### Q41 - תפסן שנוצר בטעות

- **מתגים ונורות:** `s = SW9     a = SW8     b = SW7     y = LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד הקודים, בתוך
- `always_comb begin ... end`
- `1:  if (s) y = a; else y = b;`
- `2:  if (s) y = a;`
- `3:  if (!s) y = b;`
- `4:  if (s) y = a; else if (b) y = 0;`
- `5:  if (a) y = 1; else if (b) y = 0;`
- `s = SW9     a = SW8     b = SW7     y = LEDG0`
- יש בלוח תפסן? (יש מצב של המתגים שבו הנורה זוכרת ערך קודם)
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- איזה קוד בלוח?
- `1:  if (s) y = a; else y = b;`
- `2:  if (s) y = a;`
- `3:  if (!s) y = b;`
- `4:  if (s) y = a; else if (b) y = 0;`
- `5:  if (a) y = 1; else if (b) y = 0;`
- `s = SW9     a = SW8     b = SW7     y = LEDG0`
- `1 = all down     2 = SW0     3 = SW1     4 = SW1+SW0`
- `5 = SW2`

### Q42 - צירופי או סדרתי?

- **מתגים ונורות:** `a = SW9     b = SW8     y before = SW7   LEDG1 = y now     LEDG0 = y after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד מהשניים:
- `always_comb                y = a ? b;`
- `always_ff @(posedge clk)   y <= a ? b;`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `a = SW9     b = SW8     y before = SW7`
- `LEDG1 = y now     LEDG0 = y after the next clock edge`
- האם הנורה של עכשיו משתנה רק בעליית השעון (ולא מיד כשמשנים את המתגים)?
- רק בעליית השעון - הרימו:
- `SW0`
- מיד - השאירו למטה.

**שלב 2**

- איזה שער? הסתכלו על הנורה של אחרי העלייה.
- `a = SW9     b = SW8     y before = SW7`
- `LEDG1 = y now     LEDG0 = y after the next clock edge`
- `AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0`

### Q43 - דלגלג עם איפוס בקוד

- **מתגים ונורות:** `reset = SW9     d = SW8     q before = SW7   LEDG1 = q now     LEDG0 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משני הקודים:
- `A:  always_ff @(posedge clk)              if (reset) q <= R; else q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= d;`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `reset = SW9     d = SW8     q before = SW7`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- הרימו את האיפוס. מה הערך שהאיפוס טוען?
- `R = ?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- איזה קוד? בדקו: האם האיפוס משנה את הנורה של עכשיו, עוד לפני עליית השעון?
- `A:  always_ff @(posedge clk)              if (reset) q <= R; else q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= d;`
- `reset = SW9     d = SW8     q before = SW7`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- `A = all down     B = SW0`

### Q44 - איפוס ואפשור - באיזה סדר?

- **מתגים ונורות:** `reset = SW9     en = SW8     d = SW7     q before = SW6   LEDG1 = q now     LEDG0 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משלושת הקודים:
- `A:  always_ff @(posedge clk)  if (reset) q <= 0; else if (en) q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else if (en) q <= d;`
- `C:  always_ff @(posedge clk)  if (en) begin if (reset) q <= 0; else q <= d; end`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `reset = SW9     en = SW8     d = SW7     q before = SW6`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- הרימו את הערך הקודם ואת האיפוס, והורידו את האפשור. הנורה של אחרי העלייה כבתה?
- כבתה - הרימו:
- `SW0`
- נשארה דולקת - השאירו למטה.

**שלב 2**

- איזה קוד בלוח? בדקו גם את הנורה של עכשיו כשהאיפוס למעלה.
- `A:  always_ff @(posedge clk)  if (reset) q <= 0; else if (en) q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else if (en) q <= d;`
- `C:  always_ff @(posedge clk)  if (en) begin if (reset) q <= 0; else q <= d; end`
- `reset = SW9     en = SW8     d = SW7     q before = SW6`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- `A = all down     B = SW0     C = SW1`

### Q45 - דלגלג עם ארבע פעולות

- **מתגים ונורות:** `sel = SW9 SW8     d = SW7     q before = SW6     LEDG0 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח דלגלג שהפעולה שלו נבחרת לפי
- `sel`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q before = SW6     LEDG0 = q after the next clock edge`
- איזה ערך של
- `sel`
- הופך את היציאה?
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

**שלב 2**

- איזה ערך שומר את היציאה כמו שהיא? הרימו קודם את הערך הקודם - אחרת אי אפשר להבדיל מאיפוס.
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q before = SW6     LEDG0 = q after the next clock edge`
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

**שלב 3**

- איזה ערך טוען את הנתון?
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q before = SW6     LEDG0 = q after the next clock edge`
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

### Q46 - מונה עם ערך איפוס

- **מתגים ונורות:** `reset = SW9     q before = SW8..SW5 (HEX0)   HEX3 = q now     HEX2 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מונה של 4 ביטים עם איפוס לערך
- `R`
- (ולא לאפס).
- אין שעון: הערך הקודם על מתגים, והתצוגה מראה את המונה עכשיו ואחרי עליית השעון הבאה.
- `reset = SW9     q before = SW8..SW5 (HEX0)`
- `HEX3 = q now     HEX2 = q after the next clock edge`
- הרימו את האיפוס. מה
- `R`
- ? (בבינארי)
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- בלוח אחד הקודים:
- `A:  always_ff @(posedge clk)  if (reset) q <= R; else q <= q + 1;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= q + 1;`
- `reset = SW9     q before = SW8..SW5 (HEX0)`
- `HEX3 = q now     HEX2 = q after the next clock edge`
- האם האיפוס משנה את המונה של עכשיו, עוד לפני עליית השעון? איזה קוד?
- `A = all down     B = SW0`

**שלב 3**

- הורידו את האיפוס. אחרי כמה עליות שעון מהערך
- `R`
- המונה מגיע לאפס?
- כדי לעבור עליית שעון אחת: העתיקו את מה שאחרי העלייה למתגי המצב, וקראו שוב.
- `reset = SW9     q before = SW8..SW5 (HEX0)`
- `HEX3 = q now     HEX2 = q after the next clock edge`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0 10 = SW3+SW1 11 = SW3+SW1+SW0 12 = SW3+SW2 13 = SW3+SW2+SW0 14 = SW3+SW2+SW1 15 = SW3+SW2+SW1+SW0`

### Q47 - השמה חוסמת ולא חוסמת

- **מתגים ונורות:** `d = SW9     n1 before = SW8     q before = SW7   LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אחד מארבעת הקודים, בתוך
- `always_ff @(posedge clk) begin ... end`
- `1:  n1 <= d; q <= n1;`
- `2:  q <= n1; n1 <= d;`
- `3:  n1 = d; q = n1;`
- `4:  q = n1; n1 = d;`
- אין שעון: הערכים הקודמים על מתגים, והנורות מראות אותם אחרי עליית שעון אחת.
- `d = SW9     n1 before = SW8     q before = SW7`
- `LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge`
- מאיפה היציאה מקבלת את הערך שלה?
- `n1 before = all down     d = SW0`

**שלב 2**

- אחרי כמה עליות שעון שינוי בנתון מגיע ליציאה?
- `d = SW9     n1 before = SW8     q before = SW7`
- `LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge`
- `1 = SW0 2 = SW1`

**שלב 3**

- אילו מהקודים מתנהגים כך? הרימו מתג לכל קוד מתאים:
- `1:  n1 <= d; q <= n1;`
- `2:  q <= n1; n1 <= d;`
- `3:  n1 = d; q = n1;`
- `4:  q = n1; n1 = d;`
- `1 -> SW0     2 -> SW1     3 -> SW2     4 -> SW3`

### Q48 - החלפה בין שני אוגרים

- **מתגים ונורות:** `a before = SW9     b before = SW8   LEDG1 = a after one clock edge     LEDG0 = b after one clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח שני אוגרים, ואחד הקודים בתוך
- `always_ff @(posedge clk) begin ... end`
- `1:  a <= b; b <= a;`
- `2:  a = b; b = a;`
- `3:  b = a; a = b;`
- אין שעון: הערכים הקודמים על מתגים, והנורות מראות אותם אחרי עליית שעון אחת.
- `a before = SW9     b before = SW8`
- `LEDG1 = a after one clock edge     LEDG0 = b after one clock edge`
- שימו
- `a = 1     b = 0`
- והעתיקו את הנורות:
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- עכשיו
- `a = 0     b = 1`
- והעתיקו:
- `a before = SW9     b before = SW8`
- `LEDG1 = a after one clock edge     LEDG0 = b after one clock edge`
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 3**

- איזה קוד בלוח?
- `1:  a <= b; b <= a;`
- `2:  a = b; b = a;`
- `3:  b = a; a = b;`
- `1 = all down     2 = SW0     3 = SW1`

### Q49 - הזזה וסיבוב בשרשור

- **מתגים ונורות:** `d = SW9     q[3:0] before = SW8..SW5 (HEX0)   LEDG3..LEDG0 = q after one clock edge     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר של 4 ביטים עם אחד הקודים, בתוך
- `always_ff @(posedge clk)`
- `1:  q <= {q[2:0], d};`
- `2:  q <= {d, q[3:1]};`
- `3:  q <= {q[2:0], q[3]};`
- `4:  q <= {q[0], q[3:1]};`
- אין שעון: הערכים הקודמים על מתגים, והנורות מראות אותם אחרי עליית שעון אחת.
- `d = SW9     q[3:0] before = SW8..SW5 (HEX0)`
- `LEDG3..LEDG0 = q after one clock edge`
- הזזה או סיבוב? בסיבוב הנתון לא משפיע, והביט שיוצא חוזר מהצד השני.
- `shift = all down     rotate = SW0`

**שלב 2**

- לאיזה כיוון הביטים זזים?
- `d = SW9     q[3:0] before = SW8..SW5 (HEX0)`
- `LEDG3..LEDG0 = q after one clock edge`
- `LEDG0 -> LEDG3 = all down     LEDG3 -> LEDG0 = SW0`

**שלב 3**

- איזה קוד בלוח?
- `1:  q <= {q[2:0], d};`
- `2:  q <= {d, q[3:1]};`
- `3:  q <= {q[2:0], q[3]};`
- `4:  q <= {q[0], q[3:1]};`
- `d = SW9     q[3:0] before = SW8..SW5 (HEX0)`
- `LEDG3..LEDG0 = q after one clock edge`
- `1 = all down     2 = SW0     3 = SW1     4 = SW1+SW0`

### Q50 - איזה מודול מהשקופיות?

- **מתגים ונורות:** `reset = SW9     d = SW8     en (or the latch clk) = SW7     q before = SW6   LEDG1 = q now     LEDG0 = q after the next clock edge     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד המודולים מהשקופיות:
- `flop:     always_ff @(posedge clk) q <= d;`
- `flopr:    always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else q <= d;`
- `flopren:  always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else if (en) q <= d;`
- `latch:    always_latch if (clk) q <= d;     (clk = SW7, both LEDs show the latch)`
- אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה.
- `reset = SW9     d = SW8     en (or the latch clk) = SW7     q before = SW6`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- האם הנורה של עכשיו הולכת אחרי הנתון כשמתג האפשור למעלה, גם כשלא נוגעים בערך הקודם?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- איזה מודול?
- `flop:     always_ff @(posedge clk) q <= d;`
- `flopr:    always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else q <= d;`
- `flopren:  always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else if (en) q <= d;`
- `latch:    always_latch if (clk) q <= d;     (clk = SW7, both LEDs show the latch)`
- `reset = SW9     d = SW8     en (or the latch clk) = SW7     q before = SW6`
- `LEDG1 = q now     LEDG0 = q after the next clock edge`
- `flop = all down     flopr = SW0     flopren = SW1     latch = SW1+SW0`

