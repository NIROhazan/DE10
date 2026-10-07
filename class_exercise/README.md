# תרגיל כיתה - הרצאה 3 (Harris פרק 2): מהקל אל הקשה, ואי אפשר בלי הלוח

השאלות מסודרות **מהקלה אל הקשה**, וכל שאלה מחולקת לשלבים קטנים שגם הם עולים בקושי. התשובה נמצאת רק בתוך
הלוח: בכל שאלה מוסתר בו מעגל, ורק משחק במתגים והסתכלות על הנורות נותנים את התשובה. גם הבדיקה בלוח.

## איך עובדים

1. דאבל-קליק על ה-BAT של השאלה (למשל `Q01_GATE.bat`). המחשב מכין את הלוח ומדבר איתו בעצמו דרך כבל ה-USB:
   הוא כותב לתוכו את מספר הכניסה שלכם (בלי מתגים, בלי הקלדה). עד אז ה-HEX מציג `----`.
2. בכל שלב המסך מראה מעט טקסט: מה עושים ואיפה שמים את התשובה. הכניסות של המעגל על המתגים **השמאליים**
   (`SW9`, `SW8`), התשובה על המתגים **הימניים** (`SW3..SW0`).
3. שמים את התשובה ולוחצים **`KEY2`**: הלוח מציג `PASS` או `Err` לשנייה. אחרי PASS **המסך עובר לשלב הבא לבד**.
4. בסוף הלוח מציג `donE`, והמחשב שומר את הקוד ב-`moodle.txt` לבד - מגישים את הקובץ הזה.

חלון שנסגר באמצע ממשיך מהשלב הבא (`progress.txt`) - המחשב אומר ללוח מאיזה שלב להתחיל. שאלה שהסתיימה רק מציגה את הקוד.

## השאלות

| שאלה | מה | השלבים |
|---|---|---|
| Q01 GATE | איזה שער מוסתר בלוח? (2 כניסות) | נורה אחת → טבלת אמת → שם השער |
| Q02 SIGMA | minterms ו-maxterms של F מוסתרת (3 כניסות) | נורה אחת → חצי טבלה (A = 0) → החצי השני → כמה minterms (Σ) → כמה maxterms (Π) |
| Q03 TERMS | איזו נורה היא minterm ואיזו maxterm? (4 נורות ירוקות, 3 כניסות) | העתקת הנורות ב-111 → בכמה שורות LEDG0 דולקת → ה-minterm (דולק בשורה אחת) → ה-maxterm (כבוי בשורה אחת) |
| Q04 MATTER | איזו כניסה לא משנה את F? (כמו E = HS + H) | טבלת F → האם A משנה (זוגות שורות) → האם B משנה → הכניסה שלא משנה |
| Q05 MUX | מה מחובר ל-mux 4:1? (D0..D3 = 0, 1, C או C') | Y ב-S1 S0 = 00 עם C = 0 ו-1 → D0 → D1 → D2 → D3 |
| Q06 DECODER | decoder 2:4 שהיציאות שלו מחווטות בסדר מוסתר | הנורה של 00 → של 01 → של 10 → של 11 → אילו שתי יציאות נכנסות ל-OR של F = Σ(...) אישית |

שאר השאלות יתווספו אחת-אחת, אחרי שהקודמת נבדקה. הסדר המתוכנן (מהקל לקשה):
מעגל עדיפויות, מעבדת תיאורמות,
מסיפור למשוואה, De Morgan, טעויות נפוצות, הכפלה ופירוק, SOP מינימלי, NAND / NOR, מעגל רב-שלבי,
bubble pushing, ובסוף - קופסאות עם זיכרון (latch, צירופי מול סדרתי).

הגרסה הקודמת (25 שאלות בפורמט הראשון, לפי סדר ההרצאה) נמצאת ב-[`old/`](old/README.md) לעיון.

## Instructor notes

- Source: `C:/DE10_solutions/class_exercise/gen.py` - the new list is `NEW` (ids Q01, Q02, ...; easy -> hard, in steps).
  `python gen.py` simulates the new questions in iverilog, `--compile` builds `sof/Qnn.sof`, `--id <ID>` (= `answers.bat ce <ID>`)
  prints the login number, every step's answer and the codes. The first-format puzzles stay in gen.py as o01..o25.
- The PC link: `ce.v` has an In-System Sources and Probes instance (altsource_probe, works in Quartus 13.0sp1 Web Edition).
  `run.ps1` starts `quartus_stp -t tools/link.tcl <hex>`: source = {go, start step, login} (no login on the switches, resume
  without the student), probe = {done, step, code} (code = 0 until the last step is solved). The screen follows the probe.
  KEY2 = check: PASS / Err for one second; the last step = `donE`, the code = mix(secret, step) + check digit, read by the PC.
  Codes `ce-Qnn` counted by `C:/DE10_solutions/verify.bat`. Testing without KEYs: `CE_TEST_SECONDS=12` makes link.tcl stop by itself.
- Q01 GATE: 6 gates (AND OR XOR NAND NOR XNOR), 439 LEs. Simulated (with an altsource_probe stand-in); on the board: the link
  writes the login and the runner shows the right step; the advance and the saved code tested with a fake link. KEY2 by hand: not yet.
