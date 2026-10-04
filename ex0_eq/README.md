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

- **Q01-Q07 (חלק 1):** מרימים רק את המתגים שבשאלה, ומקלידים מה רואים - 4 תווים, משמאל לימין: HEX3 HEX2 HEX1 HEX0.
- **Q08-Q12 (חלק 2):** הלוח צריך להראות את המספרים שבשאלה (`?` = כל ספרה). מוצאים אילו מתגים להרים, ומקלידים את מספרי המתגים.

תשובה שגויה - מנסים שוב. `S` = לדלג, `Q` = לצאת. כל ניסיון נרשם ב-`results.txt` עם השעה - המרצה יסתכל בו.

`free.bat` - מצב חופשי: כותבים משוואה משלכם בשורה `Y =` בקובץ `equation.txt` ורואים אותה על הלוח.

## Instructor notes

- `questions.txt` holds the questions: `Qn: Y = <eq> | SW: 0 5 8` (part 1) or `Qn: Y = <eq> | HEX: 7 0 3 4`
  (part 2, any switch set that gives the digits is accepted). The right answer is computed from that line and
  never printed, so questions can be edited freely. A new question needs its own `Qnn.bat`
  (copy one and change the `-Only Qn`).
- `tools/eq.ps1` parser, `tools/board.ps1` builds `sof/<hash>.sof` once per equation (prebuilt and committed
  for Q1-Q12, a new equation compiles in about 10 s) and programs it, `tools/run.ps1 -Only Qn` asks one question
  (without `-Only` it asks all unsolved ones in order), `tools/free.ps1` = free mode.
- Key: `C:/DE10_solutions/ex0_eq/answer_filled.txt` (all 12 verified through the runner).
- Traps: Q3 `A*B` with 6 and 3 gives 2, not 18; Q5 `~A` is 4 bits; Q12 needs every switch except A's low 3 bits -
  the only way to get F with A = 8 is B = C = 7.
