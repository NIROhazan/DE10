# תרגיל 7 - מעגל עדיפויות (Priority Circuit)

ארבע בקשות A (הכי חשובה), B, C, D, וארבע יציאות Y3..Y0 - רק הבקשה החשובה ביותר שפעילה "מנצחת".
**אצל כל סטודנט חלק מהכניסות הן active low** (לחוץ = 0) - מגלים מהטבלה האישית אילו. לכל יציאה מוצאים SOP מינימלי.

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_Y3.bat`, `Q2_Y2.bat`, `Q3_Y1.bat`, `Q4_Y0.bat`). דאבל-קליק - הנתונים שלכם מוצגים בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה למטרה בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח.
אפשר לכתוב A' או NOT A, AB או A AND B, A+B או A OR B.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q5_TEXT1.bat`, `Q6_TEXT2.bat`, `Q7_TEXT3.bat`, `Q8_TEXT4.bat`): Notepad נפתח לתשובה, Claude בודק ופותח משוב.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 / SW3 | A / B / C / D |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / D |
| LEDG3..LEDG0 | Y3..Y0 מהטבלה (המטרה) |
| LEDR3..LEDR0 | ה-Y3..Y0 שלכם |
| LEDR9 | התראה: אחת היציאות שלכם לא שווה לטבלה בשורה הזו |

## Instructor notes

- Same machinery as ex1-ex10: `tools/run.ps1`, `variant.ps1`, `check.ps1`, `ask.ps1`, `text.ps1`, `judge.md` identical in every exercise.
- Several outputs: `// TARGETS: Y3 Y2 Y1 Y0`, case rows `4'b1000: Y = 4'b1000;`; check.ps1 compares an answer named Y2 with
  that column (and minimizes / canonicalizes per column). `VARIANTS: perms=ABCD masks=all` - the order stays, 16 active-low patterns.
- Key and per-student answers: `C:/DE10_solutions/answers.bat w3-ex7 <ID>`; Moodle check: `C:/DE10_solutions/verify.bat`.
