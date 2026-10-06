# תרגיל כיתה - הרצאה 3 (Harris פרק 2): מהקל אל הקשה, ואי אפשר בלי הלוח

השאלות מסודרות **מהקלה אל הקשה**, וכל שאלה מחולקת לשלבים קטנים שגם הם עולים בקושי. התשובה נמצאת רק בתוך
הלוח: בכל שאלה מוסתר בו מעגל, ורק משחק במתגים והסתכלות על הנורות נותנים את התשובה. גם הבדיקה בלוח.

## איך עובדים

1. דאבל-קליק על ה-BAT של השאלה (למשל `Q01_GATE.bat`). הלוח נצרב והחלון מציג שלב אחד בכל פעם.
2. **כניסה (פעם אחת):** מרימים את המתגים שבחלון (מספר הכניסה, נבנה ממספר הסטודנט), לוחצים `KEY3`,
   ומקלידים את 4 התווים שהלוח מציג. הם מתאימים רק למספר הכניסה הנכון.
3. **כל שלב:** הכניסות של המעגל על המתגים **השמאליים** (`SW9`, `SW8`), התשובה על המתגים **הימניים** (`SW3..SW0`).
   מחזיקים `KEY2`: הלוח מציג **`PASS`** או **`Err`**. אחרי PASS משחררים את `KEY2` ולוחצים Enter במחשב.
4. **השלב האחרון:** `KEY2` מציג קוד של 4 תווים - מקלידים אותו, והוא נשמר ב-`moodle.txt` להגשה.

חלון שנסגר באמצע ממשיך מהשלב הבא (`progress.txt`), ושאלה שהסתיימה רק מציגה את הקוד.

## השאלות

| שאלה | מה | השלבים |
|---|---|---|
| Q01 GATE | איזה שער מוסתר בלוח? (2 כניסות) | נורה אחת → טבלת אמת → שם השער |

שאר השאלות יתווספו אחת-אחת, אחרי שהקודמת נבדקה. הסדר המתוכנן (מהקל לקשה):
טבלת אמת ו-Σ / Π, minterm / maxterm, כניסה שלא משנה, mux, decoder, מעגל עדיפויות, מעבדת תיאורמות,
מסיפור למשוואה, De Morgan, טעויות נפוצות, הכפלה ופירוק, SOP מינימלי, NAND / NOR, מעגל רב-שלבי,
bubble pushing, ובסוף - קופסאות עם זיכרון (latch, צירופי מול סדרתי).

הגרסה הקודמת (25 שאלות בפורמט הראשון, לפי סדר ההרצאה) נמצאת ב-[`old/`](old/README.md) לעיון.

## Instructor notes

- Source: `C:/DE10_solutions/class_exercise/gen.py` - the new list is `NEW` (ids Q01, Q02, ...; easy -> hard, in steps).
  `python gen.py` simulates the new questions in iverilog, `--compile` builds `sof/Qnn.sof`, `--id <ID>` (= `answers.bat ce <ID>`)
  prints the login number, every step's answer and the codes. The first-format puzzles stay in gen.py as o01..o25.
- Hardware per question (`ce.v`): LOGIN (KEY2 there = the step to resume from, LEDG2..0) -> PLAY; `FLAT` questions have no answer
  mode (inputs on the left switches, answer on the right, KEY2 any time). Steps show PASS / Err; only the last step shows the code
  = mix(secret, step) + check digit. Codes `ce-Qnn` counted by `C:/DE10_solutions/verify.bat`.
- Q01 GATE: 6 gates (AND OR XOR NAND NOR XNOR), 263 LEs. Simulated; programmed and run through the runner on the board
  (codes typed from `--id`); the switches and KEYs by hand not yet.
