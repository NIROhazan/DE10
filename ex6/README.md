# תרגיל 6 - שורות "לא אכפת" (X)

טבלת האמת (A B C | Y): `000|0  001|0  010|0  011|1  100|X  101|1  110|X  111|1`

**X = לא אכפת** (don't care): הצירוף לא יקרה, או שלא משנה מה ייצא בו. אתם מחליטים אם X הוא 0 או 1 -
וכל ביטוי רשאי להחליט אחרת. השאלה: איך הבחירה הזו מקצרת את הביטוי המינימלי?

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **SOP מינימלי**, **POS מינימלי**,
   ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. Quartus מקמפל ושורף ללוח. מזיזים מתגים ובודקים:

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y (`-` בשורת X) |
| LEDR0 / LEDR1 | ה-SOP / ה-POS הקנוניים שלך |
| LEDR2 / LEDR3 | ה-SOP המינימלי / ה-POS המינימלי שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו (לעולם לא בשורת X) |

בשורת X נורות LEDR0-3 יכולות להיות שונות זו מזו - וזה בסדר. אם Quartus מדווח ש-LEDR9 "stuck at GND",
הכלי **הוכיח** שכל התשובות שוות ל-Y בכל השורות שאכפת לנו מהן.
**שימו לב:** הלוח בודק רק נכונות, לא מינימליות - ביטוי שמתעלם מה-X עדיין נכון. את זה רק המשוב יגלה.

`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1-ex5 (`tools/run.ps1` identical), board as ex3 but no green LEDs: Y (or `-` on an X row) is on HEX0 only.
  The alarm is masked on X rows.
- New idea: don't-cares. The minimal SOP (2 terms, 3 literals) takes **both** X rows as 1, the
  minimal POS (2 terms, 3 literals) takes both as 0 - so MSOP and MPOS are different functions
  that are both right. Without the X rows the minimal SOP costs 4 literals (question 1).
- Question 4 (A=1 B=0 C=0) is a trap: correct canonical forms disagree on an X row too
  (canonical SOP gives 0, canonical POS gives 1).
- Answers in `C:\DE10_solutions\ex6\ANSWERS.md` - not in this repo.
