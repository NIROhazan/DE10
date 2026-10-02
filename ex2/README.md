# תרגיל 2 - SOP / POS עם שלושה משתנים

טבלת האמת (A B C | Y): `000|1  001|0  010|0  011|0  100|0  101|0  110|0  111|1`

בתרגיל 1 היה רק 0 אחד, ולכן ה-POS היה קצר. כאן יש רק שני 1 - ומה קורה עכשיו?

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **POS מינימלי**, ותשובות לארבע השאלות.
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
| LEDR0 / LEDR1 / LEDR2 | ה-SOP / ה-POS / ה-POS המינימלי שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו |

אם Quartus מדווח ש-LEDR9 "stuck at GND", הכלי **הוכיח** שכל שלוש התשובות שוות ל-Y בכל השורות.

מתקנים את `answer.txt` ומריצים שוב עד ש-LEDR9 לא נדלק באף שורה.
`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1 (`tools/run.ps1` is identical; only `tools/tutor_prompt.md`, `ex2_top.v`
  and `answer.txt` differ). Answers in `C:\DE10_solutions\ex2\ANSWERS.md` - not in this repo.
- Tested 2026-09-30 end to end on the DE1, programming included, with a canonical POS missing
  one maxterm: Claude kept it wrong, feedback pointed at row 110 without writing the maxterm.
