# תרגיל 3 - SOP מינימלי מול POS מינימלי

טבלת האמת (A B C | Y): `000|1  001|0  010|1  011|0  100|1  101|1  110|0  111|1`

חמישה 1 ושלושה 0. הפעם מבקשים את **שתי** הצורות המינימליות - ומשווים ביניהן.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **SOP מינימלי**, **POS מינימלי**,
   ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. run.bat בודק כל ביטוי על כל שורות הטבלה, ורק אם כולם נכונים Quartus מקמפל ושורף ללוח. מזיזים מתגים ובודקים:
   **הלוח נצרב רק כשכל התשובות נכונות.** תשובה ריקה - run.bat עוצר מיד ואומר איזו חסרה.
   תשובה שלא שווה ל-Y - run.bat מראה באילו שורות היא טועה, ולא צורב את הלוח.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y |
| LEDG0 | Y מהטבלה (המטרה) |
| LEDR0 / LEDR1 | ה-SOP / ה-POS הקנוניים שלך |
| LEDR2 / LEDR3 | ה-SOP המינימלי / ה-POS המינימלי שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו |

אם Quartus מדווח ש-LEDR9 "stuck at GND", הכלי **הוכיח** שכל התשובות שוות ל-Y בכל השורות.
**שימו לב:** הלוח בודק רק שהתשובה *נכונה*, לא שהיא *מינימלית*. ביטוי עם איבר מיותר עדיין
ידליק את הנורה הנכונה - את זה רק המשוב (והספירה שלכם) יגלו.

מתקנים את `answer.txt` ומריצים שוב עד ש-LEDR9 לא נדלק באף שורה והמשוב אומר "מינימלי".
`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1/ex2 (`tools/run.ps1` identical), but four answers: LEDR0-3.
- The minimal SOP is not unique (two 3-term covers); question 1 asks for the second one.
  The minimal POS (2 terms) is cheaper than the minimal SOP (3 terms).
- Answers in `C:\DE10_solutions\ex3\ANSWERS.md` - not in this repo.
- Tested 2026-09-30 end to end on the DE1 with a correct but redundant 4-term MSOP: the board
  proof passed (LEDR9 stuck at GND), feedback flagged "correct but not minimal" and pointed at
  the doubly covered row 100 without writing the minimal cover.
