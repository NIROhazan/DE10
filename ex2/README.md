# תרגיל 2 - SOP / POS עם שלושה משתנים

**לכל סטודנט טבלת אמת משלו.** בהרצה הראשונה של `run.bat` מקלידים מספר סטודנט (למשל 3160009489), והטבלה
האישית נכתבת לתוך `answer.txt`. המשתנים מוחלפים ומתהפכים לפי המספר - אותו תרגיל, אותה רמת קושי, תשובות אחרות.
כשהכול נכון והלוח נצרב, מקבלים **קוד** בקובץ `moodle.txt` - אותו מגישים במודל.

בתרגיל 1 היה רק 0 אחד, ולכן ה-POS היה קצר. כאן יש רק שני 1 - ומה קורה עכשיו?

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_SOP.bat`, `Q2_POS.bat`, `Q3_MIN.bat`). דאבל-קליק - הטבלה (או הביטוי) שלכם מוצגת בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה ל-Y בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח - הנורה שלכם מול LEDG0.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית / רק מהשערים המותרים).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q4_TEXT1.bat`, `Q5_TEXT2.bat`, `Q6_TEXT3.bat`, `Q7_TEXT4.bat`): השאלה מוצגת בחלון, Notepad נפתח לתשובה (עברית או
אנגלית) - שומרים וסוגרים, Claude בודק ופותח משוב. תשובה נכונה = קוד. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad וכותבים SOP קנוני, POS קנוני, **POS מינימלי**, ותשובות לארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. run.bat בודק כל ביטוי על כל שורות הטבלה, ורק אם כולם נכונים Quartus מקמפל ושורף ללוח. מזיזים מתגים ובודקים:
   **הלוח נצרב רק כשכל התשובות נכונות.** תשובה ריקה - run.bat עוצר מיד ואומר איזו חסרה.
   תשובה שלא שווה ל-Y - run.bat מראה באילו שורות היא טועה, ולא צורב את הלוח.
   בכל עצירה כזו הלוח מציג `Err` וכל הנורות כבויות - כדי שלא יישאר עליו תרגיל קודם שנראה תקין.

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
- Personal tables (2026-10-04): `tools/base_top.v` is the original exercise; `tools/variant.ps1` (identical in
  ex1-ex6) renames/complements the variables from MD5(ID|exN), writes `exN_top.v`, `tools/tutor_personal.md`
  (the prompt with the student's table and the renaming, so the background still applies) and fills `@TABLE@`
  in answer.txt on the first run. The ID is in `..\student.txt` (shared by all exercises). Programmed = code
  HMAC(ID|exN) in moodle.txt. Instructor: `C:/DE10_solutions/answers.ps1 exN <ID>`, `C:/DE10_solutions/verify.bat`.
- Per-question bats (2026-10-05): `Qn_NAME.bat` -> `tools/ask.ps1 -Q Qn`, defined by the `// ASK` lines of base_top.v.
  The answer is typed in the console, translated by `ConvertTo-Verilog` (tools/check.ps1, no Claude), checked
  with the `ONLY` rules (blocks the board) and the `GRADE` rules (CSOP / CPOS / MIN / MAXLIT - needed for the
  code only, so run.bat keeps "correct = equals Y"). Code label `exN-Qn`. `DE10_NOBOARD=1` skips Quartus (testing).
- Written questions: `Qn_TEXTk.bat` -> `tools/text.ps1 -Q Qn`, from the `// TEXT Qn k:` lines (English, rows renamed);
  Notepad for the answer (`answers/Qn.txt`), Claude judges with `tools/judge.md` -> `verdict.txt` (OK / PARTIAL / WRONG);
  OK = code. `DE10_TEXTANSWER=...` replaces Notepad in test runs.
