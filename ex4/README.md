# תרגיל 4 - ארבעה משתנים: SOP, POS, מפת קרנו ו-XOR

טבלת האמת (A B C D | Y), לפי הסדר 0000 עד 1111:
`1 0 0 1  0 1 1 0  0 1 1 0  1 0 0 1`

ציירו מפת קרנו לפני שאתם כותבים את ה-SOP המינימלי - והסתכלו טוב על מה שיוצא.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **SOP מינימלי** (ממפת קרנו),
   **Y עם XOR**, ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. run.bat בודק כל ביטוי על כל שורות הטבלה, ורק אם כולם נכונים Quartus מקמפל ושורף ללוח. מזיזים מתגים, לוחצים על KEY3, ובודקים:
   **הלוח נצרב רק כשכל התשובות נכונות.** תשובה ריקה - run.bat עוצר מיד ואומר איזו חסרה.
   תשובה שלא שווה ל-Y - run.bat מראה באילו שורות היא טועה, ולא צורב את הלוח.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| **KEY3** | **D** - לחוץ = 1, משוחרר = 0 |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / D (השורה בטבלה) |
| LEDG0 | Y מהטבלה (המטרה) |
| LEDR0 / LEDR1 | ה-SOP / ה-POS הקנוניים שלך |
| LEDR2 / LEDR3 | ה-SOP המינימלי / ביטוי ה-XOR שלך |
| LEDR9 | התראה: אחת התשובות שלך לא שווה ל-Y בשורה הזו |

אם Quartus מדווח ש-LEDR9 "stuck at GND", הכלי **הוכיח** שכל התשובות שוות ל-Y בכל 16 השורות.
הלוח בודק רק שהתשובה *נכונה*, לא שהיא *מינימלית* - את זה המשוב בודק.

מתקנים את `answer.txt` ומריצים שוב עד ש-LEDR9 לא נדלק באף שורה.
`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1-ex3 (`tools/run.ps1` identical). D = `~KEY[3]` so pressed = 1; with four
  inputs the four digits show the row (A B C D) and Y is on LEDG0 only.
- Y is even parity: the K-map is a checkerboard, nothing merges, the minimal SOP is the canonical
  SOP; the XOR line is where the real saving is. The tutor prompt forbids saying "parity" before
  the student does. XOR (`^`, `⊕`) is accepted only as notation for answer 4.
- Answers in `C:\DE10_solutions\ex4\ANSWERS.md` - not in this repo.
- Tested 2026-09-30 end to end on the DE1 with a false merge in MSOP (0000 with the 0-cell 0010)
  and an XOR missing its complement: both kept wrong on the board; feedback named the 0-cell and
  "every row inverted" and linked it to the student's own ת2, without writing the XNOR form.
