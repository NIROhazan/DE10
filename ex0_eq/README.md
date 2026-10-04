# תרגיל 0 - משוואה על הלוח

כותבים משוואה עם A, B, C בקובץ טקסט, והלוח מראה את התוצאה בתצוגות 7-סגמנט.

| בלוח | מה מוצג |
|---|---|
| `HEX0` (הימני) | A = SW3..SW0 (0-F) |
| `HEX1` | B = SW6..SW4 (0-7) |
| `HEX2` | C = SW9..SW7 (0-7) |
| `HEX3` (השמאלי) | Y - התוצאה של המשוואה (וגם LEDG3..LEDG0) |

`+` = OR, `*` = AND, `~` / `'` = NOT, `^` = XOR - **ביט אחרי ביט** על 4 ביטים, לא חשבון:
`1 * 2 = 0001 AND 0010 = 0000`.

## מה עושים

1. פותחים את `answer.txt`. לכל שאלה כותבים את המשוואה שלה בשורה `Y =` בקובץ `equation.txt`, ומריצים `run.bat` (צורב ללוח).
2. **חלק 1:** מרימים את המתגים שבשאלה וכותבים מה רואים - 4 תווים, משמאל לימין: HEX3 HEX2 HEX1 HEX0.
3. **חלק 2:** מוצאים אילו מתגים להרים כדי שהלוח יראה את המספרים שבשאלה, וכותבים את מספרי המתגים.
4. מריצים `check.bat` - הוא אומר OK / wrong / empty לכל שאלה, בלי לגלות את התשובה.

## Instructor notes

- `tools/eq.ps1` = the parser (shared); `run.ps1` writes `equation.v` and programs; `check.ps1` computes the right
  answer from each `Qn:` line, so questions can be edited freely: `Qn: Y = <eq> | SW: 0 5 8` (level 1) or
  `Qn: Y = <eq> | HEX: 7 0 3 4` (level 2, `?` = any digit, any switch set that gives it is accepted).
- Key: `C:/DE10_solutions/ex0_eq/answer_filled.txt` (12/12 by check.bat).
- Traps: Q3 `A*B` with 6 and 3 gives 2, not 18; Q5 `~A` is 4 bits; Q12 needs every switch except A's low 3 bits -
  the only way to get F with A = 8 is B = C = 7.
