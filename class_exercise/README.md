# תרגיל כיתה - הרצאה 3 (Harris פרק 2): אי אפשר בלי הלוח

25 שאלות על כל החומר של הרצאה 3 (שקופיות 1 ו-3 עד 106). **התשובה נמצאת רק בתוך הלוח:** בכל שאלה הלוח מחזיק
מעגל מוסתר (משוואה, שערים, mux, decoder, קופסאות עם זיכרון), ורק אחרי שמזיזים מתגים ומסתכלים על הנורות
אפשר לענות. גם הבדיקה נעשית בלוח: כשהתשובה נכונה, **הלוח עצמו מציג קוד** - והקוד הזה הוא מה שמגישים.
במחשב אין לא את התשובה ולא את הקוד.

## איך עובדים - שלושה מצבים

לכל שאלה BAT משלה (`Q01_SEQ.bat` ... `Q25_DECOR.bat`). דאבל-קליק: הלוח נצרב, והחלון מציג את מספר הכניסה שלכם ואת השאלה.

| מצב | על הלוח | מה עושים |
|---|---|---|
| 1. כניסה (LOGIN) | `HEX3` = L, `HEX2..HEX0` = המתגים | מרימים את המתגים של **מספר הכניסה** שבחלון (10 ביטים, נבנה ממספר הסטודנט) ולוחצים `KEY3` |
| 2. משחק (PLAY) | הנורות = המעגל המוסתר, HEX = הכניסות | מזיזים מתגים, רושמים טבלאות, פותרים על דף |
| 3. תשובה (ANSWER) | `LEDG7` דולקת, `HEX3` = A, השאר = המתגים ב-hex | `KEY3` עובר לכאן (ושוב `KEY3` חוזר למשחק). מרימים את מתגי התשובה, ו**מחזיקים `KEY2`**: נכון = קוד של 4 ספרות, לא נכון = `Err` |

את הקוד (`HEX3 HEX2 HEX1 HEX0`) מקלידים בחלון, והוא נשמר ב-`moodle.txt`. הספרה האחרונה היא ספרת ביקורת:
טעות הקלדה, או כניסה עם מספר לא נכון, נתפסות מיד. `KEY1` במצב תשובה מראה את מספר הכניסה שהלוח קיבל.
אחרי צריבה מחדש (הרצה נוספת של ה-BAT) נכנסים שוב.

## Q01 - בשלבים (פורמט חדש, לבדיקה)

ב-Q01 כל מסך הוא שלב קטן: מעט טקסט, עושים, מקלידים את הקוד שהלוח נתן, ומקבלים **PASS / FAIL**.
רק אחרי PASS המסך נמחק ומגיע השלב הבא. שלב 0 הוא הכניסה: אחרי `KEY3` הלוח מציג 4 ספרות (קבלה) - הן
מתאימות רק למספר הכניסה הנכון, אז כניסה שגויה נתפסת מיד. במצב תשובה `LEDG2..LEDG0` מראות את מספר השלב,
ושחרור `KEY2` אחרי תשובה נכונה מעביר את הלוח לשלב הבא. `KEY1` מראה את הקוד האחרון שהלוח נתן.

**חלון שנסגר באמצע:** כל שלב שעבר נשמר (`progress.txt`). הרצה חוזרת של ה-BAT ממשיכה מהשלב הבא - אי אפשר להתחיל מההתחלה,
ושאלה שהסתיימה רק מציגה את הקוד. הלוח נצרב מחדש, אז נכנסים שוב: לפני `KEY3` לוחצים `KEY2` עד ש-`LEDG2..LEDG0`
מראות את מספר השלב (החלון אומר בדיוק אילו נורות).

| שלב | מה עושים |
|---|---|
| 0 | כניסה: המתגים של מספר הכניסה, `KEY3`, מקלידים את הקבלה |
| 1 | A B = 00, 01, 10, 11, 00 - מעתיקים את הנורות למתגים |
| 2 | A B = 11, 10, 01, 00 - מעתיקים שוב |
| 3 | אילו קופסאות היו שונות בשני הניסיונות (אותה כניסה, אור אחר = זיכרון) |
| 4 | כל הקופסאות הסדרתיות - הקוד הזה נכנס ל-`moodle.txt` |

שאר השאלות (Q02-Q25) עדיין בפורמט הראשון: כל השאלה במסך אחד וקוד אחד.

## השאלות - לפי סדר ההרצאה

| שאלה | נושא (שקופיות) | מה מוסתר בלוח | התשובה על המתגים |
|---|---|---|---|
| Q01 SEQ | צירופי מול סדרתי (4-7) | 8 קופסאות, חלקן עם זיכרון | אילו קופסאות סדרתיות |
| Q02 LATCH | זיכרון (6-7) | קופסה אחת: שורת set ושורת reset | שתי השורות |
| Q03 PI | maxterms, POS קנוני (9-13) | F של 2 משתנים | Π(...) |
| Q04 SIGMA | minterms, SOP קנוני (9-16) | F של 3 משתנים | Σ(...) |
| Q05 MINTERM | הגדרות: minterm (10) | 8 איברים (מכפלות / סכומים) | אילו נורות הן minterms |
| Q06 MAXTERM | הגדרות: maxterm (10) | 8 איברים | אילו נורות הן maxterms |
| Q07 STORY | מסיפור למשוואה (14, 17-21) | 4 מעגלים של 4 "סטודנטים" | איזה מהם מממש את הסיפור שלכם |
| Q08 MATTER | כניסה שלא משנה, E = HS + H (20-21) | חוק הכניסה של השומר | אילו כניסות באמת משפיעות |
| Q09 EQUAL | הוכחה באינדוקציה מלאה (37-40) | 8 טענות LEFT = RIGHT בסדר מוסתר | אילו נכונות |
| Q10 WHERE | תיאורמות T8'-T12 (36-44) | אותן 8 טענות | איפה שתי הטענות שלכם |
| Q11 MINSOP | פישוט ל-SOP מינימלי (45-48) | F של 3 משתנים | מספר האיברים והליטרלים |
| Q12 LITERAL | פישוט (50-61) | ליטרל אחד (?) בביטוי מודפס | הליטרל + ליטרלים ב-SOP המינימלי |
| Q13 ERRORS | טעויות נפוצות (70-73) | 5 פישוטים של סטודנטים | אילו שגויים |
| Q14 DEMORGAN | De Morgan (68-69, 89-92) | 4 תשובות | אילו נכונות |
| Q15 MULTIPLY | הכפלה ל-SOP, פירוק ל-POS (59-67) | 6 תשובות | אילו נכונות |
| Q16 PRIORITY | מעגל עדיפויות (80-82) | סדר העדיפויות | הסדר מהגבוה לנמוך |
| Q17 ACTIVELOW | כניסות active low (80-82) | אילו כניסות פעילות ב-0 | המסכה |
| Q18 NANDNOR | שתי רמות NAND / NOR (83-87) | סוג כל שער (הצמתים n1-n3 על נורות) | NAND או NOR לכל שער |
| Q19 NODE | שתי רמות (83-87) | הכניסות של שער אחד | שני הליטרלים |
| Q20 GATES | מעגל רב-שלבי (79, 94-97) | AND / OR / NAND / NOR בכל שער | שלושת הסוגים |
| Q21 BUBBLES | Bubble pushing (88-97) | איזה מ-8 מעגלים מודפסים נמצא בלוח | מספר המעגל |
| Q22 MUXDATA | Mux 4:1 (99-101) | מה מחובר ל-D0..D3 (0, 1, C, C') | ארבעת הקודים |
| Q23 MUXLOGIC | לוגיקה עם mux (102) | F | D0..D3 עבור קווי הבחירה שלכם |
| Q24 DECODER | Decoder 3:8, one-hot, active low (104-105) | סדר החיווט של היציאות | הנורות של שני ה-minterms שלכם |
| Q25 DECOR | לוגיקה עם decoder (106) | אילו יציאות נכנסות לשער | המסכה |

חלק מהשאלות מדפיסות בחלון גם טקסט אישי (סיפור, ביטוי, רשימת מעגלים). **הטקסט לבד לא מספיק:** תמיד חסר החלק שבלוח.

## מה לא נבדק בלוח - בבדיקה מול המרצה

שמות התיאורמות בכל צעד, הוכחה אלגברית (שיטה 2), כללי ציור סכמה (76-77), סדר ליטרלים (62) ועקרון הדואליות (23-25):
הלוח בודק רק שוויון ותוצאה, לא נימוק. אלה נבדקים בעל פה, על התשובות שלכם מהלוח ("איזו תיאורמה כאן?", "תכתוב את הדואלי").

## Instructor notes

- Source: `C:/DE10_solutions/class_exercise/gen.py` (instructor only). `python gen.py` builds and simulates all 25 questions in
  iverilog (every row, the memory boxes on a random walk, login / answer / code / Err / KEY1 per test login);
  `--compile` builds with Quartus 13.0sp1 and copies `sof/Qnn.sof` here; `--id <ID>` (or `answers.bat ce <ID>`) prints a student's
  login number, every answer as switches and every code. `ANSWERS.md` there describes every question.
- Q01 is in steps (questions.txt `| steps 5`, `Sk:` lines): its `ce.v` adds a step register, a want ROM {variant, step} ->
  {mask, answer}, and the step code = mix(secret16, step) in logic + check digit with the step (gen.py, `verify.ps1` too).
  Q02-Q25 are still the first format; their sof files were built by `gen_v1.py.bak` and gen.py does not rebuild them.
- One hardware for all (`ce.v`): seed ROM (1024 logins x {code, mask, answer, variant}) + table ROM (variant x row -> 0 / 1 / hold
  per output). 169-196 LEs, 47-111 Kbit M4K. Outputs stay 0 after the login until the first switch change.
- `variant = pub * nsec + sec`: `pub` = MD5 (public - picks the printed text, computed by `tools/common.ps1` too), `sec` = HMAC with
  `C:/DE10_solutions/class_exercise/key.txt` (hidden). gen.py checks that the answer follows from the board and that every printed
  text still has several answers (at least 4).
- Codes: `ce-Qnn: XXXX` in `moodle.txt`; `C:/DE10_solutions/verify.bat <folder>` shows them as Class n/25. Change `key.txt` each
  semester, then `python gen.py --compile`.
- Tested 2026-10-06: all 25 pass simulation; PowerShell and Python agree on login / printed variant / check digit;
  Q05 run through `Q05` runner on the board (programmed; wrong code rejected, right code saved; verify 25/25 and a fake code flagged).
  The KEY presses themselves have not been tried by hand on the board yet.
