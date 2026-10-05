# תרגיל 9 - רק NAND, רק NOR

**לכל סטודנט טבלת אמת משלו.** בהרצה הראשונה של `run.bat` מקלידים מספר סטודנט (למשל 3160009489), והטבלה האישית
נכתבת לתוך `answer.txt`. המשתנים מוחלפים ומתהפכים לפי המספר - אותו תרגיל, אותה רמת קושי, תשובות אחרות.
כשהכול נכון והלוח נצרב, מקבלים **קוד** בקובץ `moodle.txt` - אותו מגישים במודל.

מוצאים SOP ו-POS מינימליים, ובונים מהם את Y **רק משערי NAND** (מה-SOP) ו**רק משערי NOR** (מה-POS) -
"bubble pushing" מההרצאה. NAND כותבים (XY)', NOR כותבים (X+Y)'.

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_SOP.bat`, `Q2_POS.bat`, `Q3_NAND.bat`, `Q4_NOR.bat`). דאבל-קליק - הטבלה (או הביטוי) שלכם מוצגת בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה ל-Y בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח - הנורה שלכם מול LEDG0.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית / רק מהשערים המותרים).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q5_TEXT1.bat`, `Q6_TEXT2.bat`, `Q7_TEXT3.bat`, `Q8_TEXT4.bat`): השאלה מוצגת בחלון, Notepad נפתח לתשובה (עברית או
אנגלית) - שומרים וסוגרים, Claude בודק ופותח משוב. תשובה נכונה = קוד. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad, כותבים SOP, POS, NAND ו-NOR, ועונים על ארבע השאלות.
2. שומרים ומריצים `run.bat` (דאבל-קליק).
3. Claude קורא את התשובות, **מתרגם אותן ל-Verilog בדיוק כפי שנכתבו - כולל הטעויות** (`student_logic.v`),
   ופותח את `feedback.txt` עם משוב, רמז ושאלה מכוונת. הוא לא כותב את התשובה הנכונה.
4. run.bat בודק שכל תשובה שווה ל-Y, **וגם שה-NAND בנוי רק מ-NAND וה-NOR רק מ-NOR** (כל AND / OR חייב ' מיד אחריו); ורק אם הכול נכון Quartus מקמפל ושורף ללוח.
   תשובה ריקה או שגויה - הלוח לא נצרב ומציג `Err`.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y |
| LEDG0 | Y מהטבלה (המטרה) |
| LEDR0 / LEDR1 | SOP / POS שלכם |
| LEDR2 / LEDR3 | NAND / NOR שלכם |
| LEDR9 | התראה: אחת התשובות לא שווה ל-Y בשורה הזו |

`run.bat check` - רק משוב, בלי לוח.

## Instructor notes

- Same machinery as ex1-ex6: `tools/run.ps1` and `tools/variant.ps1` are identical in every exercise;
  the original is `tools/base_top.v`, the personal copy `exN_top.v` is made from the ID.
- `// ONLY: NAND : NAND` (every AND directly under a NOT, no OR/XOR), `NOR : NOR`, `SOP : SOP`, `POS : POS`.
  Original SOP AB' + BC, POS (A + B)(B' + C); 4 gates each with the B' inverter.
- Key and per-student answers: `C:/DE10_solutions/answers.bat ex9 <ID>`; Moodle check: `C:/DE10_solutions/verify.bat`.
- Per-question bats (2026-10-05): `Qn_NAME.bat` -> `tools/ask.ps1 -Q Qn`, defined by the `// ASK` lines of base_top.v.
  The answer is typed in the console, translated by `ConvertTo-Verilog` (tools/check.ps1, no Claude), checked
  with the `ONLY` rules (blocks the board) and the `GRADE` rules (CSOP / CPOS / MIN / MAXLIT - needed for the
  code only, so run.bat keeps "correct = equals Y"). Code label `exN-Qn`. `DE10_NOBOARD=1` skips Quartus (testing).
- Written questions: `Qn_TEXTk.bat` -> `tools/text.ps1 -Q Qn`, from the `// TEXT Qn k:` lines (English, rows renamed);
  Notepad for the answer (`answers/Qn.txt`), Claude judges with `tools/judge.md` -> `verdict.txt` (OK / PARTIAL / WRONG);
  OK = code. `DE10_TEXTANSWER=...` replaces Notepad in test runs.
