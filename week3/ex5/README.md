# תרגיל 5 - פישוט בעזרת התיאורמות (T1-T12)

**לכל סטודנט ביטוי משלו.** בהרצה הראשונה של `run.bat` מקלידים מספר סטודנט (למשל 3160009489), והביטוי האישי
נכתב לתוך `answer.txt`. המשתנים מוחלפים ומתהפכים לפי המספר - אותו תרגיל, אותה רמת קושי, תשובות אחרות.
כשהכול נכון והלוח נצרב, מקבלים **קוד** בקובץ `moodle.txt` - אותו מגישים במודל.

מקבלים ביטוי ארוך, ומפשטים אותו צעד אחר צעד - בכל צעד **תיאורמה אחת**, ושמה כתוב בסוגריים מרובעים.
זה בדיוק מה שעשינו בהרצאה (דוגמאות 1-7), רק שהלוח והמשוב בודקים אתכם.

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_STEPS.bat`, `Q2_MIN.bat`). דאבל-קליק - הטבלה (או הביטוי) שלכם מוצגת בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה ל-Y בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח - הנורה שלכם מול LEDG0.
אפשר לכתוב A' או NOT A, AB או A AND B, A+B או A OR B.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית / רק מהשערים המותרים).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q3_TEXT1.bat`, `Q4_TEXT2.bat`, `Q5_TEXT3.bat`, `Q6_TEXT4.bat`): השאלה מוצגת בחלון, Notepad נפתח לתשובה (עברית או
אנגלית) - שומרים וסוגרים, Claude בודק ופותח משוב. תשובה נכונה = קוד. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad, כותבים עד 8 צעדים (S1..S8) ואת הביטוי הסופי (MIN), ועונים על ארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. run.bat בודק **שכל צעד שווה ל-Y** בכל השורות (צעד שגוי = שם בדיוק נשבר השוויון), ושה-MIN בצורת SOP; ורק אם הכול נכון Quartus מקמפל ושורף ללוח.
   תשובה ריקה או שגויה - הלוח לא נצרב ומציג `Err`.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y |
| LEDG0 | Y - הביטוי שקיבלתם |
| LEDR0..LEDR7 | הצעדים S1..S8 שלכם |
| LEDR8 | הביטוי הסופי MIN |
| LEDR9 | התראה: אחד הצעדים לא שווה ל-Y בשורה הזו |

Claude בודק שכל תיאורמה באמת מעבירה מהשורה הקודמת לנוכחית. הלוח בודק רק שוויון - לא את שם התיאורמה.

`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1-ex6: `tools/run.ps1` and `tools/variant.ps1` are identical in every exercise;
  the original is `tools/base_top.v`, the personal copy `exN_top.v` is made from the ID.
- `// EXPR:` in base_top.v is the starting expression (Y = AB + A(B + C)' + A'BC); `@EXPR@` in answer.txt becomes
  the student's renamed copy. run.bat compares every step to Y; `// ONLY: MIN : SOP`. Minimal = AC' + BC (8-step path in the key).
- Key and per-student answers: `C:/DE10_solutions/answers.bat w3-ex5 <ID>`; Moodle check: `C:/DE10_solutions/verify.bat`.
- Per-question bats (2026-10-05): `Qn_NAME.bat` -> `tools/ask.ps1 -Q Qn`, defined by the `// ASK` lines of base_top.v.
  The answer is typed in the console, translated by `ConvertTo-Verilog` (tools/check.ps1, no Claude), checked
  with the `ONLY` rules (blocks the board) and the `GRADE` rules (CSOP / CPOS / MIN / MAXLIT - needed for the
  code only, so run.bat keeps "correct = equals Y"). Code label `exN-Qn`. `DE10_NOBOARD=1` skips Quartus (testing).
- Written questions: `Qn_TEXTk.bat` -> `tools/text.ps1 -Q Qn`, from the `// TEXT Qn k:` lines (English, rows renamed);
  Notepad for the answer (`answers/Qn.txt`), Claude judges with `tools/judge.md` -> `verdict.txt` (OK / PARTIAL / WRONG);
  OK = code. `DE10_TEXTANSWER=...` replaces Notepad in test runs.
