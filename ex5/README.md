# תרגיל 5 - ארבעה משתנים: SOP מינימלי מול POS מינימלי

טבלת האמת (A B C D | Y), לפי הסדר 0000 עד 1111:
`1 1 1 1  0 0 0 0  1 0 1 0  0 0 1 0`

שבעה 1 ותשעה 0. ציירו שתי מפות קרנו - אחת ל-1 ואחת ל-0 - ובדקו מי באמת יוצא קצר יותר.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **SOP מינימלי**, **POS מינימלי**,
   ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. Quartus מקמפל ושורף ללוח. מזיזים מתגים, לוחצים על KEY3, ובודקים:

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| **KEY3** | **D** - לחוץ = 1, משוחרר = 0 |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / D (השורה בטבלה) |
| LEDG0 | Y מהטבלה (המטרה) |
| LEDR0 / LEDR1 | ה-SOP / ה-POS הקנוניים שלך |
| LEDR2 / LEDR3 | ה-SOP המינימלי / ה-POS המינימלי שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו |

אם Quartus מדווח ש-LEDR9 "stuck at GND", הכלי **הוכיח** שכל התשובות שוות ל-Y בכל 16 השורות.
הלוח בודק רק שהתשובה *נכונה*, לא שהיא *מינימלית* - את זה המשוב בודק.

מתקנים את `answer.txt` ומריצים שוב עד ש-LEDR9 לא נדלק באף שורה והמשוב אומר "מינימלי".
`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1-ex4 (`tools/run.ps1` identical), same board layout as ex4 (D = KEY3),
  LEDR3 is the minimal POS instead of the XOR form.
- The point: the minimal SOP needs the four-corner group (wrap-around on both edges), every prime
  implicant is essential, and the minimal POS (6 literals) beats the minimal SOP (7) although there
  are more 0s than 1s - counting 1s/0s predicts only the canonical forms. The tutor prompt forbids
  naming the corner group first.
- Answers in `C:\DE10_solutions\ex5\ANSWERS.md` - not in this repo. Both minimal forms checked
  against all 16 rows by script.
- Tested 2026-10-01 with a POS missing a maxterm, an MSOP using a pair instead of the corner quad,
  and an MPOS with a wrong complement: all kept wrong on the board, feedback named each without
  giving the fix. Compile OK; programming not run (board was unplugged) - same top level as ex4,
  which was tested on the board.
