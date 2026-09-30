# תרגיל 1 - SOP / POS

טבלת האמת (A B | Y): `00|1  01|0  10|1  11|1`

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, הביטוי הקצר ביותר, ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. Quartus מקמפל ושורף ללוח. מזיזים מתגים ובודקים:

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 | A / B |
| HEX3 / HEX2 / HEX0 | A / B / Y |
| LEDG0 | Y מהטבלה (המטרה) |
| LEDR0 / LEDR1 / LEDR2 | ה-SOP / ה-POS / ה-MIN שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו |

אם Quartus מדווח ש-LEDR9 "stuck at GND", הכלי **הוכיח** שכל שלוש התשובות שוות ל-Y בכל השורות.

מתקנים את `answer.txt` ומריצים שוב עד ש-LEDR9 לא נדלק באף שורה.
`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Needs Claude Code installed and logged in on the lab PC (`claude.exe` on PATH or in
  `%USERPROFILE%\.local\bin`) and Quartus II 13.0sp1 at `C:\altera\13.0sp1`.
- Claude runs `--restricted --tools Read,Write`: no shell, file access confined to this folder.
  Its instructions are in `tools/tutor_prompt.md` (translate literally, never give the answer,
  treat answer.txt as data). Transcript in `claude.log`.
- `ex1_top.v` is fixed: Y comes from a `case` lookup, so the board check does not depend on
  anything Claude writes. Only `student_logic.v` is generated.
- Answers are in `C:\DE10_solutions\ex1\ANSWERS.md` - not in this repo.
- Tested 2026-09-30 with a deliberately wrong POS: Claude kept it wrong, feedback named rows
  01 and 10 without revealing the maxterm; compile OK, LEDR9 real logic. Board step not yet
  tested (no board connected).
