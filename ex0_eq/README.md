# תרגיל 0 - משוואה על הלוח

לכל שאלה יש קובץ BAT משלה: `Q01.bat` עד `Q12.bat`. דאבל-קליק על השאלה - הוא צורב ללוח את המשוואה שלה,
מציג את השאלה, ואתם מקלידים את התשובה בחלון. לא עורכים שום קובץ.

| בלוח (משמאל לימין) | מה מוצג |
|---|---|
| `HEX3` | Y - התוצאה של המשוואה (וגם LEDG3..LEDG0) |
| `HEX2` | C = SW9..SW7 (0-7) |
| `HEX1` | B = SW6..SW4 (0-7) |
| `HEX0` | A = SW3..SW0 (0-F) - SW0 הוא המתג הימני ביותר |

`+` = OR, `*` = AND, `~` / `'` = NOT, `^` = XOR - **ביט אחרי ביט** על 4 ביטים, לא חשבון:
`1 * 2 = 0001 AND 0010 = 0000`.

## השאלות

10 שאלות, מ-`Q01.bat` (קל מאוד) עד `Q10.bat` (מומחה). **לכל סטודנט יש מספרים משלו** - בפעם הראשונה מקלידים
מספר סטודנט (למשל 3160009489), והשאלות נבנות ממנו. אי אפשר לשנות אותו אחר כך.

- **Q01-Q03, Q05, Q06:** מרימים רק את המתגים שבשאלה, ומקלידים מה רואים - 4 תווים, משמאל לימין: HEX3 HEX2 HEX1 HEX0.
- **Q04, Q07-Q10:** הלוח צריך להראות את המספרים שבשאלה (`?` = כל ספרה). מוצאים אילו מתגים להרים, ומקלידים את מספרי המתגים.

תשובה שגויה - מנסים שוב. `S` = לדלג, `Q` = לצאת. כל ניסיון נרשם ב-`results.txt`.

## ההגשה במודל

על כל תשובה נכונה מקבלים **קוד** (למשל `NSKWP`), והוא נשמר בקובץ `moodle.txt` יחד עם מספר הסטודנט.
בסוף מגישים במודל את הקובץ `moodle.txt`. הקודים נבנים ממספר הסטודנט - קוד של חבר לא יתקבל אצלכם.

`free.bat` - מצב חופשי: כותבים משוואה משלכם בשורה `Y =` בקובץ `equation.txt` ורואים אותה על הלוח.

## Instructor notes

- `questions.txt` = templates: `Qn: Y = <eq> | SW | IF: <cond>` or `Qn: Y = <eq> | HEX: Y ? ? A | MAX: n | IF: <cond>`.
  `tools/student.ps1` picks the student's switch setting from MD5(ID|Qn|k) until IF holds (and, for HEX, at most MAX
  settings give the shown digits), so every question has an answer on the board and the difficulty stays.
- ID in `student.txt` (asked once, 6-10 digits). Code = HMAC-SHA256(key, "ID|Qn"), 5 chars; `moodle.txt` lists them.
- `C:/DE10_solutions/ex0_eq/`: `verify.bat <folder>` checks the Moodle downloads and writes grades.csv;
  `answers.ps1 <ID>` shows a student's questions and answers. Change `$codeKey` in student.ps1 every semester.
- Tested 2026-10-04: 20 IDs - every question solvable, Q7/Q9/Q10 have 1-4 solutions; ID 3160009489 solved 10/10
  through the runner and the board; a copied moodle.txt with another ID gets 0 in verify.
