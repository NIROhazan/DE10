# תרגיל 11 - מסיפור למשוואה

**לכל סטודנט סיפור משלו** (אחד מ-8, נבחר לפי מספר הסטודנט). כמו בהרצאה - הקפיטריה, הפארק, ה-Winner:
מתרגמים את הסיפור לטבלת אמת, ואז ל-SOP קנוני, SOP מינימלי ו-POS מינימלי. לכל הסיפורים אותו מבנה ואותה רמת קושי.

## שאלה אחת בכל קובץ BAT

לכל תשובה יש קובץ BAT משלה (`Q1_SOP.bat`, `Q2_MSOP.bat`, `Q3_MPOS.bat`). דאבל-קליק - הנתונים שלכם מוצגים בחלון, מקלידים את התשובה,
והיא נבדקת מיד: שווה למטרה בכל השורות, ובצורה הנכונה. תשובה נכונה נצרבת ללוח.
אפשר לכתוב A' או NOT A, AB או A AND B, A+B או A OR B.
**קוד למודל** מקבלים רק כשהתשובה גם עונה בדיוק על השאלה (קנונית / מינימלית).
גם לכל שאלה כתובה (ש1-ש4) יש BAT משלה (`Q4_TEXT1.bat`, `Q5_TEXT2.bat`, `Q6_TEXT3.bat`, `Q7_TEXT4.bat`): Notepad נפתח לתשובה, Claude בודק ופותח משוב.
כל הקודים נאספים בקובץ `moodle.txt` - אותו מגישים במודל. אפשר עדיין לענות על הכול ב-`answer.txt` ו-`run.bat`.

| על הלוח | משמעות |
|---|---|
| SW0 / SW1 / SW2 | A / B / C |
| HEX3 / HEX2 / HEX1 / HEX0 | A / B / C / Y |
| LEDG0 | Y של הסיפור (המטרה) |
| LEDR0 / LEDR1 / LEDR2 | SOP / SOP מינימלי / POS מינימלי שלכם |
| LEDR9 | התראה: אחת התשובות לא שווה ל-Y בשורה הזו |

## Instructor notes

- Same machinery as ex1-ex10: `tools/run.ps1`, `variant.ps1`, `check.ps1`, `ask.ps1`, `text.ps1`, `judge.md` identical in every exercise.
- `tools/stories.txt`: 8 stories (TABLE / EN / HE), all "X and (Y or Z)" with 3 ones; variant.ps1 picks one from MD5(ID),
  writes its table into exN_top.v, the Hebrew text into answer.txt (`@STORY@`), the English one in the console.
  No renaming (`VARIANTS: perms=ABC masks=-`). Keys are computed per student (`@CSOP` / `@MSOP` / `@MPOS`).
- Key and per-student answers: `C:/DE10_solutions/answers.bat ex11 <ID>`; Moodle check: `C:/DE10_solutions/verify.bat`.
