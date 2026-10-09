# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - זמני התקנה והחזקה

30 דקות, 7 שאלות: Q01-Q07

### Q01 - זמן המחזור המינימלי

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה ההשהיות של מסלול בין שני אוגרים:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור הקצר ביותר שעוד עובד?
- `Tc >= tpcq + tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q02 - כמה זמן מותר ללוגיקה?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור וההשהיות של האוגרים:
- `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הגדולה ביותר שמותרת ללוגיקה הצירופית בין שני האוגרים?
- `tpd <= Tc - tpcq - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q03 - תדר השעון המקסימלי

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     (ns)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה ההשהיות של המסלול הארוך, בננו-שניות:
- `HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     (ns)`
- מה זמן המחזור המינימלי (ננו-שניות)?
- `Tc >= tpcq + tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- מה התדר המקסימלי, במגה-הרץ?
- `f = 1000 / Tc`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

### Q04 - אילוץ ההחזקה

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     answer: SW8..SW0`
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

**שלב 2**

- מה ההשהיה הקטנה ביותר שמותרת ללוגיקה כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)
- `tcd >= thold - tccq`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q05 - האם המעגל עומד בזמן?

- **מתגים ונורות:** `Tc, tpcq, tpd on page 1; tsetup on page 2     SW9 = page 2     answer: SW8..SW0`
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

**שלב 2**

- בכמה זמן המחזור גדול (או קטן) מהדרוש? כתבו את ההפרש בערך מוחלט:
- `| Tc - (tpcq + tpd + tsetup) |`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q06 - הדוגמה מהשקופית: שני שערים בטור

- **מתגים ונורות:** `tpcq tsetup tpd tcd / tccq thold     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בין שני האוגרים שני שערים בטור. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd gate   HEX0 = tcd gate`
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + 2 tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- האם אילוץ ההחזקה מתקיים?
- `tccq + 2 tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.

### Q07 - כמה מאגרים לתקן את ההחזקה?

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = thold     HEX1 = tcd of one buffer     answer: SW8..SW0`
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

**שלב 2**

- כמה מאגרים צריך לפחות להוסיף בדרך כדי שיתקיים?
- `tccq + n tcd >= thold`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0 6 = SW2+SW1 7 = SW2+SW1+SW0 8 = SW3 9 = SW3+SW0`

## נושא 2 - חלון הדגימה, הטיית שעון ומסנכרנים

30 דקות, 7 שאלות: Q08-Q14

### Q08 - חלון הדגימה

- **מתגים ונורות:** `HEX3 = tsetup     HEX2 = thold     HEX1 = when D changes, before the edge     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמני הדלגלג:
- `HEX3 = tsetup     HEX2 = thold     HEX1 = when D changes, before the edge`
- `all times in units of 10 ps (5 = 50 ps)`
- מה רוחב חלון הדגימה סביב עליית השעון?
- `ta = tsetup + thold`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- הנתון משתנה כמה זמן לפני העלייה (הספרה השלישית). האם זה בתוך החלון (סכנה)?
- `inside the aperture: change time < tsetup`
- בתוך החלון - הרימו:
- `SW0`
- בסדר - השאירו למטה.

### Q09 - זמן המחזור עם הטיית שעון

- **מתגים ונורות:** `tpcq tpd tsetup tskew / tccq tcd thold     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה שני דפים של מסלול עם הטיית שעון:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tpd   HEX1 = tsetup   HEX0 = tskew`
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = tcd   HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי עם ההטיה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- האם אילוץ ההחזקה מתקיים עם ההטיה?
- `tccq + tcd >= thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.

### Q10 - כמה הטיה מותרת?

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה ההשהיות של מסלול קצר:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההחזקה עוד עומד בה?
- `tskew <= tccq + tcd - thold`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q11 - הטיה מותרת לפי אילוץ ההתקנה

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור, וסכום ההשהיות של המסלול:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההתקנה עוד עומד בה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q12 - מסנכרן

- **מתגים ונורות:** `the asynchronous input = SW9 (HEX3)     the synchronized output = LEDG0     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח מסנכרן: המתג הוא כניסה אסינכרונית (כמו לחצן של משתמש), והנורה היא הכניסה אחרי הסנכרון.
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה דלגלגים יש במסנכרן? (אחרי כמה לחיצות הנורה מגיבה לשינוי של המתג)
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 2**

- מסנכרן טוב בנוי משני דלגלגים לפחות. הוא מספיק?
- כן - הרימו:
- `SW0`
- לא - השאירו למטה.

### Q13 - כמה זמן לוקח לסנכרן?

- **מתגים ונורות:** `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מסנכרן:
- `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)`
- כמה זמן לכל היותר עובר עד שהכניסה האסינכרונית מגיעה ליציאה (בננו-שניות)?
- `about (flip-flops) x Tc`
- `128 = SW7`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q14 - כמה זמן יש להתייצבות?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tsetup     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:
- `HEX3 HEX2 = Tc     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן יש ליציאה של הדלגלג הראשון להתייצב לפני שהשני דוגם אותה?
- `tres = Tc - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- הסיכוי לכשל קטן פי
- `e^(tres / tau)`
- כשהזמן גדל. אם מוסיפים עוד דלגלג אחד, כמה זמן התייצבות יש בסך הכול?
- `2 (Tc - tsetup)`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

## נושא 3 - מקביליות והשהיות בקוד

30 דקות, 6 שאלות: Q15-Q20

### Q15 - זמן אחזור וקצב: עוגיות

- **מתגים ונורות:** `HEX3 = minutes of step 1     HEX2 HEX1 = minutes of step 2     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- אפייה בשני שלבים (הכנה ואפייה), מגש אחד בכל פעם. הזמנים בתצוגה:
- `HEX3 = minutes of step 1     HEX2 HEX1 = minutes of step 2`
- מה זמן האחזור של מגש אחד (בדקות)?
- `latency = step 1 + step 2`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- כמה מגשים בשעה, בלי מקביליות?
- `throughput = 60 / latency`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 3**

- עם צנרת (מגש חדש מתחיל הכנה כשהקודם בתנור): כמה מגשים בשעה?
- `throughput = 60 / the longest step`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q16 - מקביליות מרחבית

- **מתגים ונורות:** `HEX3 = workers     HEX2 HEX1 = minutes for one tray (latency)     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- כמה עובדים, כל אחד עם תנור משלו. בתצוגה:
- `HEX3 = workers     HEX2 HEX1 = minutes for one tray (latency)`
- כמה מגשים בשעה כולם יחד?
- `throughput = workers x 60 / latency`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- ומה זמן האחזור של מגש אחד?
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q17 - מקביליות מרחבית וזמנית יחד

- **מתגים ונורות:** `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- כמה עובדים, וכל אחד עובד בצנרת (הכנה של מגש חדש בזמן שהקודם בתנור). בתצוגה:
- `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2`
- כמה מגשים בשעה, כולם יחד?
- `throughput = workers x 60 / the longest step`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q18 - צנרת: זמן מחזור וזמן אחזור

- **מתגים ונורות:** `HEX3 HEX2 HEX1 = the delays of 3 pipeline stages     HEX0 = tpcq + tsetup     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- מעגל מחולק ל-3 שלבים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 HEX1 = the delays of 3 pipeline stages     HEX0 = tpcq + tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור הקצר ביותר?
- `Tc = the longest stage + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- מה זמן האחזור (מהכניסה עד היציאה, 3 מחזורים)?
- `latency = 3 Tc`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q19 - צנרת על הלוח

- **מתגים ונורות:** `a new token = SW9 (HEX3)     the stages = LEDG0.. (left to right)     clock = KEY1, reset = KEY0     answer: SW3..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח צנרת: בכל לחיצה כל אסימון עובר לשלב הבא. נורה דולקת = יש אסימון בשלב.
- `new token = SW9`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- כמה שלבים יש?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- הכניסו אסימון בכל לחיצה. כמה אסימונים נמצאים בצנרת בבת אחת, כשהיא מלאה?
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

### Q20 - השהיות בקוד

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)     answer: SW8..SW0`
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

**שלב 2**

- ואם רק
- `n1`
- משתנה בזמן 0 - מתי
- `y`
- משתנה?
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

