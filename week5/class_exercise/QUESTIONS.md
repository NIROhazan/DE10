# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - תפסנים, דלגלגים ומצב

30 דקות, 10 שאלות: Q01-Q10

### Q01 - תפסן SR - מה קובע, מה מאפס?

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

### Q02 - תפסן קביעה-איפוס עם אפשור

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

### Q03 - תפסן D - שעון ונתון

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

### Q04 - תפסן D מבפנים

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

### Q05 - ארבעה תפסנים - מי זה מי?

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

### Q06 - תפסן מול דלגלג

- **מתגים ונורות:** `D = SW8     latch enable = SW9     clock = KEY1     LEDG1 LEDG0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח תפסן ודלגלג, שניהם עם אותו נתון:
- `D = SW8     latch enable = SW9`
- `KEY1 = the flip-flop clock`
- איזו נורה היא הדלגלג (משתנה רק בלחיצה)?
- `LEDG0 = all down     LEDG1 = SW0`

**שלב 2**

- מתי התפסן שקוף?
- כשמתג האפשור למעלה - הרימו:
- `SW0`
- כשהוא למטה - השאירו למטה.

### Q07 - שני תפסנים ודלגלג

- **מתגים ונורות:** `D = SW8     EN = SW9     LEDG3..LEDG0     clock = KEY1, reset = KEY0     answer: SW1 SW0`
- **שלבים:** 3

**שלב 1**

- בלוח ארבע נורות עם אותו נתון: שני תפסנים, ודלגלג שמוצג פעמיים (היציאה וההפוכה שלה).
- `D = SW8     latch enable = SW9     LEDG3..LEDG0`
- `KEY1 = the flip-flop clock     KEY0 = reset`
- איזו נורה היא התפסן שקוף כשהאפשור למעלה?
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 2**

- איזו נורה היא התפסן שקוף כשהאפשור למטה?
- `D = SW8     latch enable = SW9`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

**שלב 3**

- איזו נורה היא ההפוכה של הדלגלג? (לחצו על האיפוס: הדלגלג מתאפס ל-0)
- `Q'`
- `KEY0 = reset`
- `LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1     LEDG3 = SW1+SW0`

### Q08 - דלגלג D

- **מתגים ונורות:** `SW9 SW8 SW7     LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג
- `D`
- הנורה משתנה רק כשלוחצים על השעון:
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא הנתון? (שנו מתג, לחצו, וראו אם הנורה עוקבת)
- `SW9 = all down     SW8 = SW0     SW7 = SW1`

**שלב 2**

- לחצו על האיפוס. הנורה מראה את היציאה או את ההפוכה שלה?
- `KEY0`
- `Q = all down     Q' = SW0`

### Q09 - כמה מצבים, כמה ביטים?

- **מתגים ונורות:** `the state = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בכל לחיצה על השעון הלוח עובר למצב הבא, ומציג ספרה:
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אחרי כמה לחיצות חוזרים לספרה של ההתחלה? (כמה מצבים יש)
- `HEX0`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- כמה ביטים של מצב צריך לפחות כדי לזכור את כל המצבים האלה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

### Q10 - טבעת של מהפכים - יציבה או מתנדנדת?

- **מתגים ונורות:** `inverters = HEX0     their outputs = LEDG0, LEDG1, ...     KEY1 = one gate delay, KEY0 = reset     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח טבעת של מהפכים: היציאה של כל מהפך היא הכניסה של הבא.
- `number of inverters = HEX0     their outputs = LEDG0, LEDG1, ...`
- כל לחיצה על השעון = השהיה של שער אחד:
- `KEY1 = one gate delay     KEY0 = reset`
- לחצו כמה פעמים. האם התבנית ממשיכה להשתנות בלי סוף?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- אחרי כמה לחיצות התבנית חוזרת להתחלה? (אם היא לא משתנה בכלל - השאירו הכל למטה)
- `KEY1 = one gate delay     KEY0 = reset     LEDG0, LEDG1, ...`
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

## נושא 2 - אפשור, איפוס, קביעה ואוגרים

30 דקות, 10 שאלות: Q11-Q20

### Q11 - דלגלג עם אפשור

- **מתגים ונורות:** `SW9 SW8 (D and EN)     Q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם אפשור: הוא שומר נתון חדש בלחיצה רק כשהאפשור פעיל.
- `EN, D = SW9, SW8 (in some order)`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא האפשור?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- האפשור פעיל כשהמתג שלו
- `EN`
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

### Q12 - איפוס סינכרוני או אסינכרוני

- **מתגים ונורות:** `SW9 SW8 (D and Reset)     Q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם איפוס על אחד המתגים (איפוס = 1):
- `Reset, D = SW9, SW8 (in some order)`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא האיפוס?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- הדליקו את הנורה, ואז הרימו את האיפוס בלי ללחוץ על השעון. היא כבתה מיד?
- `asynchronous = at once     synchronous = at the next clock edge`
- כבתה מיד - הרימו:
- `SW0`
- רק בלחיצה - השאירו למטה.

### Q13 - קביעה ואיפוס - מי מנצח?

- **מתגים ונורות:** `SW9 SW8 (Set and Reset)     Q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם קביעה ואיפוס סינכרוניים (בלחיצה על השעון):
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא הקביעה (מדליק)?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- הרימו את שניהם ולחצו. מי מנצח?
- `Set = all down     Reset = SW0`

### Q14 - אוגר עם קביעה ואיפוס

- **מתגים ונורות:** `D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     Q[3:0] = LEDG3..LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר של 4 ביטים. בחלק מהדלגלגים יש קביעה ובחלק איפוס, וכולם מחוברים לאותו מתג (סינכרוני).
- `D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     Q[3:0] = LEDG3..LEDG0     KEY1 = clock`
- שימו
- `D = 0000`
- הרימו את
- `SW5`
- ולחצו על השעון. כמה נורות דולקות? (כמה דלגלגים עם קביעה)
- `0 = all down 1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- אילו דלגלגים עם קביעה? העתיקו את הנורות אחרי לחיצה עם
- `set/reset = SW5 up`
- `SW3..SW0 = LEDG3..LEDG0`

### Q15 - דלגלג שמתהפך

- **מתגים ונורות:** `SW9 SW8     Q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח דלגלג עם משוב:
- `q <= q ^ T`
- כשהכניסה
- `T`
- פעילה, כל לחיצה הופכת את הנורה.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא
- `T`
- `?`
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- הכניסה פעילה כשהמתג שלה
- למעלה - הרימו:
- `SW0`
- למטה - השאירו למטה.

### Q16 - אוגרים בטור

- **מתגים ונורות:** `D = SW9 (HEX3)     LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בין המתג לנורה יש כמה דלגלגים בטור. אפסו, שנו את המתג, ולחצו על השעון שוב ושוב:
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אחרי כמה לחיצות הנורה מגיבה? (כמה דלגלגים)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- בסוף השרשרת יש מהפך?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q17 - אוגר הזזה

- **מתגים ונורות:** `serial in = SW9 or SW8     LEDG3..LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר הזזה: בכל לחיצה כל ביט זז נורה אחת, וביט חדש נכנס מאחד המתגים.
- `serial in = SW9 or SW8     LEDG3..LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- איזה מתג הוא הכניסה?
- `SW9 = all down     SW8 = SW0`

**שלב 2**

- באיזו נורה נכנס הביט החדש?
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- `LEDG0 = all down     LEDG3 = SW0`

**שלב 3**

- יש מהפך בכניסה? (נכנסת נורה דולקת כשמתג הכניסה למטה)
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q18 - טבעת של דלגלגים

- **מתגים ונורות:** `LEDG3..LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח כמה דלגלגים שמחוברים בטבעת: היציאה של כל אחד היא הכניסה של הבא.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה דלגלגים יש? (כמה נורות משתתפות)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2`

**שלב 2**

- אחרי כמה לחיצות הנורות חוזרות לתבנית של ההתחלה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3`

### Q19 - אוגר של 4 ביטים

- **מתגים ונורות:** `D[3:0] = SW9..SW6 (HEX0)     Q[3:0] = LEDG3..LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר של 4 ביטים, אבל החוטים מעורבבים.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- שימו
- `D = 1000  (SW9)`
- לחצו על השעון, והעתיקו את הנורות:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 2**

- עכשיו
- `D = 0100  (SW8)`
- לחצו, והעתיקו:
- `SW3..SW0 = LEDG3..LEDG0`

**שלב 3**

- ועכשיו
- `D = 0010  (SW7)`
- לחצו, והעתיקו:
- `SW3..SW0 = LEDG3..LEDG0`

### Q20 - אוגר עם משוב דרך מחבר

- **מתגים ונורות:** `q = HEX0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אוגר של ספרה, ומחבר במשוב מהיציאה שלו לכניסה שלו:
- `always_ff @(posedge clk)  q <= (q + K) % 10;`
- `q = HEX0     clk = KEY1     KEY0 = reset (q = 0)`
- אפסו ולחצו פעם אחת. מה
- `K`
- `?`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

**שלב 2**

- אחרי כמה לחיצות מהאיפוס התצוגה חוזרת ל-0?
- `q = HEX0     clk = KEY1     KEY0 = reset (q = 0)`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0 10 = SW3+SW1`

## נושא 3 - תיאור חומרה סדרתי

30 דקות, 11 שאלות: Q21-Q31

### Q21 - דלגלג עם איפוס בקוד

- **מתגים ונורות:** `reset = SW9     d = SW8     q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משני הקודים:
- `A:  always_ff @(posedge clk)              if (reset) q <= R; else q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= d;`
- `reset = SW9     d = SW8     clk = KEY1`
- הרימו את האיפוס ולחצו על השעון. מה הערך שהאיפוס טוען?
- `R = ?`
- 1 - הרימו:
- `SW0`
- 0 - השאירו למטה.

**שלב 2**

- איזה קוד? (בדקו: האם האיפוס פועל גם בלי לחיצה)
- `A = all down     B = SW0`

### Q22 - מונה עם ערך איפוס

- **מתגים ונורות:** `reset = SW9     q = HEX0     clk = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח מונה של 4 ביטים עם איפוס לערך
- `R`
- (ולא ל-0):
- `reset = SW9     q = HEX0 (hex)     clk = KEY1`
- הרימו את האיפוס ולחצו על השעון. מה
- `R`
- ? (בבינארי)
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- בלוח אחד הקודים:
- `A:  always_ff @(posedge clk)  if (reset) q <= R; else q <= q + 1;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= q + 1;`
- `reset = SW9     q = HEX0     clk = KEY1`
- הורידו את האיפוס ולחצו כמה פעמים. אחר כך הרימו אותו בלי ללחוץ. איזה קוד?
- `A = all down     B = SW0`

**שלב 3**

- הורידו את האיפוס. אחרי כמה לחיצות מהערך
- `R`
- התצוגה מראה 0?
- `reset = SW9     q = HEX0     clk = KEY1`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0 10 = SW3+SW1 11 = SW3+SW1+SW0 12 = SW3+SW2 13 = SW3+SW2+SW0 14 = SW3+SW2+SW1 15 = SW3+SW2+SW1+SW0`

### Q23 - איפוס ואפשור - באיזה סדר?

- **מתגים ונורות:** `reset = SW9     en = SW8     d = SW7     q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד משלושת הקודים:
- `A:  always_ff @(posedge clk)  if (reset) q <= 0; else if (en) q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else if (en) q <= d;`
- `C:  always_ff @(posedge clk)  if (en) begin if (reset) q <= 0; else q <= d; end`
- `reset = SW9     en = SW8     d = SW7     clk = KEY1`
- הדליקו את הנורה. אחר כך הורידו את האפשור, הרימו את האיפוס ולחצו. הנורה כבתה?
- כבתה - הרימו:
- `SW0`
- נשארה דולקת - השאירו למטה.

**שלב 2**

- איזה קוד בלוח?
- `A:  always_ff @(posedge clk)  if (reset) q <= 0; else if (en) q <= d;`
- `B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else if (en) q <= d;`
- `C:  always_ff @(posedge clk)  if (en) begin if (reset) q <= 0; else q <= d; end`
- `A = all down     B = SW0     C = SW1`

### Q24 - תפסן בקוד

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

### Q25 - תפסן שנוצר בטעות

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

### Q26 - צירופי או סדרתי?

- **מתגים ונורות:** `a = SW9     b = SW8     y = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד מהשניים:
- `always_comb                y = a ? b;`
- `always_ff @(posedge clk)   y <= a ? b;`
- `a = SW9     b = SW8     clk = KEY1`
- האם הנורה משתנה רק כשלוחצים על השעון?
- רק בלחיצה - הרימו:
- `SW0`
- מיד - השאירו למטה.

**שלב 2**

- איזה שער? (אם צריך, לחצו על השעון אחרי כל שינוי)
- `AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0`

### Q27 - דלגלג עם ארבע פעולות

- **מתגים ונורות:** `sel = SW9 SW8     d = SW7     q = LEDG0     clk = KEY1     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח דלגלג שהפעולה שלו נבחרת לפי
- `sel`
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q = LEDG0     clk = KEY1`
- איזה ערך של
- `sel`
- הופך את הנורה בכל לחיצה?
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

**שלב 2**

- איזה ערך שומר את הנורה כמו שהיא? (הדליקו אותה קודם - אחרת אי אפשר להבדיל מאיפוס)
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q = LEDG0     clk = KEY1`
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

**שלב 3**

- איזה ערך טוען את
- `d`
- `?`
- `always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase`
- `the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;`
- `sel = SW9 SW8     d = SW7     q = LEDG0     clk = KEY1`
- `00 = all down     01 = SW0     10 = SW1     11 = SW1+SW0`

### Q28 - השמה חוסמת ולא חוסמת

- **מתגים ונורות:** `d = SW9 (HEX3)     q = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד מארבעת הקודים, בתוך
- `always_ff @(posedge clk) begin ... end`
- `1:  n1 <= d; q <= n1;`
- `2:  q <= n1; n1 <= d;`
- `3:  n1 = d; q = n1;`
- `4:  q = n1; n1 = d;`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אפסו, הרימו את
- `d = SW9`
- ולחצו שוב ושוב. אחרי כמה לחיצות
- `q`
- נדלק?
- `1 = SW0 2 = SW1`

**שלב 2**

- אילו מהקודים מתנהגים כך? הרימו מתג לכל קוד מתאים:
- `1 -> SW0     2 -> SW1     3 -> SW2     4 -> SW3`

### Q29 - החלפה בין שני אוגרים

- **מתגים ונורות:** `a = LEDG1     b = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח שני אוגרים, ואחד הקודים בתוך
- `always_ff @(posedge clk) begin ... end`
- `1:  a <= b; b <= a;`
- `2:  a = b; b = a;`
- `3:  b = a; a = b;`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- לחצו על האיפוס, ואז פעם אחת על השעון. העתיקו את הנורות:
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 2**

- לחצו שוב על השעון. העתיקו:
- `SW1 SW0 = LEDG1 LEDG0`

**שלב 3**

- איזה קוד בלוח?
- `1:  a <= b; b <= a;`
- `2:  a = b; b = a;`
- `3:  b = a; a = b;`
- `1 = all down     2 = SW0     3 = SW1`

### Q30 - הזזה וסיבוב בשרשור

- **מתגים ונורות:** `d = SW9     q[3:0] = LEDG3..LEDG0     clk = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 3

**שלב 1**

- בלוח אוגר של 4 ביטים עם אחד הקודים, בתוך
- `always_ff @(posedge clk)`
- `1:  q <= {q[2:0], d};`
- `2:  q <= {d, q[3:1]};`
- `3:  q <= {q[2:0], q[3]};`
- `4:  q <= {q[0], q[3:1]};`
- `d = SW9     q[3:0] = LEDG3..LEDG0     clk = KEY1     KEY0 = reset`
- אפסו, השאירו את
- `d = 0`
- ולחצו 4 פעמים. התבנית חזרה?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- לאיזה כיוון הנורות זזות?
- `d = SW9     q[3:0] = LEDG3..LEDG0     clk = KEY1     KEY0 = reset`
- `LEDG0 -> LEDG3 = all down     LEDG3 -> LEDG0 = SW0`

**שלב 3**

- איזה קוד בלוח?
- `1:  q <= {q[2:0], d};`
- `2:  q <= {d, q[3:1]};`
- `3:  q <= {q[2:0], q[3]};`
- `4:  q <= {q[0], q[3:1]};`
- `d = SW9     q[3:0] = LEDG3..LEDG0     clk = KEY1     KEY0 = reset`
- `1 = all down     2 = SW0     3 = SW1     4 = SW1+SW0`

### Q31 - איזה מודול מהשקופיות?

- **מתגים ונורות:** `reset = SW9     d = SW8     en (or the latch clk) = SW7     q = LEDG0     clock = KEY1     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח אחד המודולים מהשקופיות:
- `flop:     always_ff @(posedge clk) q <= d;`
- `flopr:    always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else q <= d;`
- `flopren:  always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else if (en) q <= d;`
- `latch:    always_latch if (clk) q <= d;     (clk = SW7, not KEY1)`
- `reset = SW9     d = SW8     en / latch clk = SW7     clk = KEY1`
- האם הנורה הולכת אחרי
- `d`
- גם בלי לחיצה, כש-
- `SW7`
- למעלה?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

**שלב 2**

- איזה מודול?
- `flop = all down     flopr = SW0     flopren = SW1     latch = SW1+SW0`

