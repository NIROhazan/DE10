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

### Q06 - דלגלג D

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

### Q07 - תפסן מול דלגלג - צורת גל

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

### Q08 - דלגלג משני תפסנים

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

### Q09 - כמה מצבים, כמה ביטים?

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

### Q10 - טבעת של מהפכים - יציבה או מתנדנדת?

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

30 דקות, 10 שאלות: Q11-Q20

### Q11 - דלגלג עם אפשור

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

### Q12 - איפוס סינכרוני או אסינכרוני

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

### Q13 - קביעה ואיפוס - מי מנצח?

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

### Q14 - דלגלג שמתהפך

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

### Q15 - אוגר של 4 ביטים

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

### Q16 - אוגר עם קביעה ואיפוס

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

### Q17 - אוגרים בטור

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

### Q18 - אוגר הזזה

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

### Q19 - טבעת של דלגלגים

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

### Q20 - אוגר עם משוב דרך מחבר

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

30 דקות, 11 שאלות: Q21-Q31

### Q21 - תפסן בקוד

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

### Q22 - תפסן שנוצר בטעות

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

### Q23 - צירופי או סדרתי?

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

### Q24 - דלגלג עם איפוס בקוד

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

### Q25 - איפוס ואפשור - באיזה סדר?

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

### Q26 - דלגלג עם ארבע פעולות

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

### Q27 - מונה עם ערך איפוס

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

### Q28 - השמה חוסמת ולא חוסמת

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

### Q29 - החלפה בין שני אוגרים

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

### Q30 - הזזה וסיבוב בשרשור

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

### Q31 - איזה מודול מהשקופיות?

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

