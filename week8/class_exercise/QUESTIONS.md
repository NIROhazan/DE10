# פירוט השאלות לפי נושא

נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`tools/lesson.txt`).

## נושא 1 - זמני התקנה והחזקה

30 דקות, 10 שאלות: Q01-Q10

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

### Q02 - שני מסלולים: מי קובע?

- **מתגים ונורות:** `HEX3 = tpcq     HEX2 = tpd of path A     HEX1 = tpd of path B     HEX0 = tsetup     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:
- `HEX2 = tpd of path A     HEX1 = tpd of path B`
- `all times in units of 10 ps (5 = 50 ps)`
- איזה מסלול קובע את זמן המחזור?
- `path A = all down     path B = SW0`

**שלב 2**

- בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:
- `HEX3 = tpcq     HEX2 = tpd of path A     HEX1 = tpd of path B     HEX0 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + max(tpd A, tpd B) + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q03 - כמה זמן מותר ללוגיקה?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור וההשהיות של האוגרים:
- `HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הגדולה ביותר שמותרת ללוגיקה הצירופית בין שני האוגרים?
- `tpd <= Tc - tpcq - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q04 - כמה שערים נכנסים במחזור?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)     HEX0 = tpd of one gate     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן נשאר ללוגיקה?
- `tpd <= Tc - (tpcq + tsetup)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)     HEX0 = tpd of one gate`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה שערים כאלה אפשר לשים בטור לכל היותר?
- `n x tpd(gate) <= Tc - (tpcq + tsetup)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q05 - תדר השעון המקסימלי

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

### Q06 - אילוץ ההחזקה

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

### Q07 - האם המעגל עומד בזמן?

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

### Q08 - הדוגמה מהשקופית: שני שערים בטור

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

### Q09 - הדוגמה מהשקופית עם יותר שערים

- **מתגים ונורות:** `tpcq tsetup tpd n_long / tccq thold tcd n_short     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- כמו בדוגמה מהשקופית, עם מספר אחר של שערים. הנתונים בדף הראשון:
- `page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd of a gate   HEX0 = gates on the long path`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור המינימלי?
- `Tc >= tpcq + n_long x tpd + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path`
- `all times in units of 10 ps (5 = 50 ps)`
- האם אילוץ ההחזקה מתקיים?
- `tccq + n_short x tcd >= thold`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.

**שלב 3**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההשהיה הקטנה ביותר של שער במסלול הקצר כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)
- `tcd >= (thold - tccq) / n_short     (round up)`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q10 - כמה מאגרים לתקן את ההחזקה?

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

30 דקות, 11 שאלות: Q11-Q21

### Q11 - חלון הדגימה

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

### Q12 - זמן המחזור עם הטיית שעון

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

### Q13 - כמה הטיה מותרת?

- **מתגים ונורות:** `HEX3 = tccq     HEX2 = tcd     HEX1 = thold     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה ההשהיות של מסלול קצר:
- `HEX3 = tccq     HEX2 = tcd     HEX1 = thold`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההחזקה עוד עומד בה?
- `tskew <= tccq + tcd - thold`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q14 - מאגרים נגד הטיית שעון

- **מתגים ונורות:** `tccq tcd thold tskew / tcd of a buffer     SW9 = page 2     answer: SW8..SW0`
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

**שלב 2**

- מוסיפים מאגרים במסלול. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 = tccq   HEX2 = tcd   HEX1 = thold   HEX0 = tskew`
- `page 2 (SW9 up):    HEX3 = tcd of one buffer`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה מאגרים צריך לפחות כדי שהאילוץ יתקיים? (0 אם כבר מתקיים)
- `tccq + tcd + n x tcd(buffer) >= thold + tskew`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q15 - הטיה מותרת לפי אילוץ ההתקנה

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה זמן המחזור, וסכום ההשהיות של המסלול:
- `HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה הטיית השעון הגדולה ביותר שאילוץ ההתקנה עוד עומד בה?
- `Tc >= tpcq + tpd + tsetup + tskew`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q16 - הטיה לשני הכיוונים

- **מתגים ונורות:** `Tc, setup path / hold path, thold, tskew     SW9 = page 2     answer: SW8..SW0`
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

**שלב 2**

- הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):
- `page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- אם השעון של האוגר השני מאחר - האם אילוץ ההחזקה מתקיים?
- `tccq + tcd >= thold + tskew`
- מתקיים - הרימו:
- `SW0`
- לא מתקיים - השאירו למטה.

**שלב 3**

- ההטיה יכולה להיות לשני הכיוונים. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 HEX0 = tpcq + tpd + tsetup (together)`
- `page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew`
- `all times in units of 10 ps (5 = 50 ps)`
- מה ההטיה הגדולה ביותר ששני האילוצים יחד עומדים בה? (0 אם אפילו בלי הטיה לא)
- `tskew <= min(Tc - (tpcq + tpd + tsetup), tccq + tcd - thold)`
- `8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q17 - מסנכרן

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

### Q18 - כמה זמן לוקח לסנכרן?

- **מתגים ונורות:** `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- בתצוגה מסנכרן:
- `HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)`
- כמה זמן לכל היותר עובר עד שהכניסה האסינכרונית מגיעה ליציאה (בננו-שניות)?
- `about (flip-flops) x Tc`
- `128 = SW7`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q19 - כמה זמן יש להתייצבות?

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

### Q20 - כמה עוזר עוד דלגלג?

- **מתגים ונורות:** `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:
- `HEX3 HEX2 = Tc     HEX1 = tsetup`
- `all times in units of 10 ps (5 = 50 ps)`
- כמה זמן התייצבות נותן כל דלגלג נוסף?
- `tres = Tc - tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:
- `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau`
- `all times in units of 10 ps (5 = 50 ps)`
- כל דלגלג נוסף מגדיל את הזמן הממוצע בין כשלים פי
- `e^(tres / tau)`
- מה החזקה?
- `tres / tau = (Tc - tsetup) / tau`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 3**

- בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:
- `HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau`
- `all times in units of 10 ps (5 = 50 ps)`
- מסנכרן של 4 דלגלגים במקום 2: פי
- `e`
- בחזקת כמה גדל הזמן הממוצע בין כשלים?
- `2 x (Tc - tsetup) / tau`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q21 - הזמן הממוצע בין כשלים

- **מתגים ונורות:** `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K     answer: SW8..SW0`
- **שלבים:** 2

**שלב 1**

- בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:
- `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K`
- `P(failure) per change = 1 / (K x 1000)`
- כל כמה שניות, בממוצע, המסנכרן נכשל?
- `MTBF = 1 / (N x P) = K x 1000 / N`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

**שלב 2**

- בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:
- `HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K`
- `P(failure) per change = 1 / (K x 1000)`
- ואם הכניסה משתנה פי 2 יותר פעמים בשנייה?
- `MTBF = K x 1000 / (2 N)`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

## נושא 3 - מקביליות והשהיות בקוד

30 דקות, 12 שאלות: Q22-Q33

### Q22 - זמן אחזור וקצב: עוגיות

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

### Q23 - מקביליות מרחבית

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

### Q24 - מקביליות מרחבית וזמנית יחד

- **מתגים ונורות:** `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2     answer: SW8..SW0`
- **שלבים:** 1

**שלב 1**

- כמה עובדים, וכל אחד עובד בצנרת (הכנה של מגש חדש בזמן שהקודם בתנור). בתצוגה:
- `HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2`
- כמה מגשים בשעה, כולם יחד?
- `throughput = workers x 60 / the longest step`
- `64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q25 - צנרת: זמן מחזור וזמן אחזור

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

### Q26 - חלוקה לשלבים שווים

- **מתגים ונורות:** `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור בלי צנרת?
- `Tc = tpd + tpcq + tsetup`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

**שלב 2**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור עם הצנרת?
- `Tc = tpd / stages + tpcq + tsetup`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

**שלב 3**

- מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:
- `HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן האחזור עם הצנרת? (הוא גדל בגלל האוגרים)
- `latency = stages x Tc`
- `64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1`
- `1 = SW0`

### Q27 - כמה זמן לכמה אסימונים?

- **מתגים ונורות:** `HEX3 = stages     HEX2 HEX1 = tokens     HEX0 = Tc (ns)     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages`
- אחרי כמה מחזורים יוצא האסימון הראשון?
- `latency = stages`
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages     HEX2 HEX1 = tokens`
- אחרי כמה מחזורים יוצא האסימון האחרון?
- `cycles = stages + tokens - 1`
- `32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0`

**שלב 3**

- צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:
- `HEX3 = stages     HEX2 HEX1 = tokens     HEX0 = Tc (ns)`
- כמה ננו-שניות עד שהאסימון האחרון יוצא?
- `t = (stages + tokens - 1) x Tc`
- `256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3`
- `4 = SW2   2 = SW1   1 = SW0`

### Q28 - איפה לשים את האוגר?

- **מתגים ונורות:** `the 4 gate delays / tpcq + tsetup     SW9 = page 2     answer: SW8..SW0`
- **שלבים:** 3

**שלב 1**

- שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- `page 2 (SW9 up):    HEX3 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור עכשיו?
- `Tc = tpd1 + tpd2 + tpd3 + tpd4 + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

**שלב 2**

- שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- מוסיפים אוגר אחד בתוך השרשרת. אחרי איזה שער כדאי לשים אותו כדי שזמן המחזור יהיה הקצר ביותר?
- `1 = SW0 2 = SW1 3 = SW1+SW0`

**שלב 3**

- שרשרת של ארבעה שערים, ואוגר במקום הטוב ביותר. בתצוגה שני דפים:
- `page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)`
- `page 2 (SW9 up):    HEX3 = tpcq + tsetup (together)`
- `all times in units of 10 ps (5 = 50 ps)`
- מה זמן המחזור אז?
- `Tc = max(stage 1, stage 2) + tpcq + tsetup`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q29 - צנרת על הלוח

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

### Q30 - זמן האחזור של צנרת נסתרת

- **מתגים ונורות:** `a token = SW9 (HEX3)     the output = LEDG0     HEX0 = Tc (ns)     clock = KEY1, reset = KEY0     answer: SW5..SW0`
- **שלבים:** 2

**שלב 1**

- בלוח צנרת נסתרת: המתג מכניס אסימון, והנורה דולקת כשהוא יוצא מהשלב האחרון.
- `token = SW9     output = LEDG0`
- `KEY1 = clock (one rising edge per press)     KEY0 = reset`
- אחרי כמה לחיצות האסימון יוצא? (כמה שלבים יש)
- `1 = SW0 2 = SW1 3 = SW1+SW0 4 = SW2 5 = SW2+SW0`

**שלב 2**

- בתצוגה זמן המחזור:
- `HEX0 = Tc (ns)`
- מה זמן האחזור בננו-שניות?
- `latency = stages x Tc`
- `32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0`

### Q31 - השהיות בקוד

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

### Q32 - המסלול הקצר בקוד

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)     answer: SW8..SW0`
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

### Q33 - השהיות בקוד בדיקה

- **מתגים ונורות:** `HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     HEX0 = #dg     (ns)     answer: SW8..SW0`
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

