# תרגיל 13 - קריאת מעגל רב-שלבי

מקבלים מעגל כרשימת שערים (NAND ו-NOR, עם חוטים פנימיים n1, n2, n3), ומוצאים מה הוא מחשב -
כמו "What is the Boolean expression for this circuit?" ו-bubble pushing בהרצאה. ואז SOP ו-POS מינימליים.

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_MSOP.bat`, `Q2_MPOS.bat`). דאבל-קליק - הנתונים שלכם מוצגים בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה למטרה בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח.
אפשר לכתוב A' או NOT A, AB או A AND B, A+B או A OR B.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q3_TEXT1.bat`, `Q4_TEXT2.bat`, `Q5_TEXT3.bat`, `Q6_TEXT4.bat`): Notepad נפתח לתשובה, Claude בודק ופותח משוב.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y |
| LEDG0 | Y של המעגל (המטרה) |
| LEDR0 / LEDR1 | SOP מינימלי / POS מינימלי שלכם |
| LEDR9 | התראה: אחת התשובות לא שווה ל-Y בשורה הזו |

## Instructor notes

- Same machinery as ex1-ex10: `tools/run.ps1`, `variant.ps1`, `check.ps1`, `ask.ps1`, `text.ps1`, `judge.md` identical in every exercise.
- `// NET:` lines in base_top.v are the circuit (n1 = (AB')', n2 = (A' + C)', n3 = (n1 n2')', Y = (n3 + BC)'); they are renamed
  like the table and written into answer.txt (`@NET@`). Y = A'B' + A'C' = A'(B' + C') in the original.
- Key and per-student answers: `C:/DE10_solutions/answers.bat ex13 <ID>`; Moodle check: `C:/DE10_solutions/verify.bat`.
