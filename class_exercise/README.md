# תרגיל כיתה - הרצאה 3 (Harris פרק 2): מהקל אל הקשה, ואי אפשר בלי הלוח

השאלות מסודרות **מהקלה אל הקשה**, וכל שאלה מחולקת לשלבים קטנים שגם הם עולים בקושי. התשובה נמצאת רק בתוך
הלוח: בכל שאלה מוסתר בו מעגל, ורק משחק במתגים והסתכלות על הנורות נותנים את התשובה. גם הבדיקה בלוח.

## שיעור שלם: `LESSON.bat`

דאבל-קליק אחד בתחילת השיעור, והחלון מריץ את כל השיעור לפי השעון (`tools/lesson.txt`):

| זמן | נושא | שאלות (מהקל לקשה) |
|---|---|---|
| 30 דקות | טבלאות אמת, minterms ו-maxterms, תיאורמות | Q01 Q02 Q03 Q04 Q21 Q08 Q23 Q13 Q17 |
| 30 דקות | ממילים למשוואה: סיפורים, De Morgan, טעויות, הכפלה ופירוק | Q09 Q10 Q11 Q12 Q24 Q25 Q27 Q26 |
| 30 דקות | אבני בניין ומעגלים: mux, decoder, עדיפויות, NAND/NOR, רב-שלבי, bubbles, ובסוף זיכרון | Q05 Q06 Q07 Q16 Q22 Q14 Q15 Q18 Q28 Q29 Q19 Q30 Q20 |

- לפני שעת ההתחלה (`START` בקובץ) - מסך המתנה עם ספירה לאחור ותוכנית היום.
- בכל נושא השאלות באות אחת אחרי השנייה; שאלה שהסתיימה פותחת את הבאה לבד. כותרת החלון מראה כמה זמן נשאר לנושא.
- נגמר הזמן של הנושא - "Time is up", ומתחיל הנושא הבא מהשאלה הקלה שלו. ההתקדמות נשמרת.
- סיימו מוקדם - "Well done", והמתנה לנושא הבא. מאחרים או שהמחשב נפל - נכנסים ישר לנושא שרץ עכשיו.
- **יציאה וחזרה:** כל שלב שעבר נשמר מיד (`progress.txt`), והזמן ממשיך לרוץ גם כשהחלון סגור. מי שחוזר מקבל
  "Welcome back" ונכנס לנושא שרץ עכשיו, בשאלה ובשלב שבהם עצר. ב-`START now` שעת ההתחלה נשמרת בפעם הראשונה
  (`lesson_start.txt`), אז גם שם יציאה לא מאפסת את השעון. **איפוס ידני של הזמן לסטודנט** (פספס, תקלה): המרצה מריץ במחשב שלו
  `C:\DE10_solutions\class_exercise
eset_time.bat` - הנושא הראשון מתחיל עכשיו (או `reset_time.bat 2` - מנושא 2); ההתקדמות נשמרת. איפוס (למרצה): `C:\DE10_solutions\class_exercise
eset_lesson.bat`.
- הכל לפי השעון של המחשב, אז כל הכיתה עוברת נושא יחד. לפני השיעור: לשנות את `START` (ואת הדקות / השאלות) ב-`tools/lesson.txt`.
  `START now` = השיעור מתחיל כשמפעילים (לתרגול בבית).

## לבחור נושא ושאלה: `goto.txt` + `GOTO.bat`

כותבים ב-`goto.txt` (ב-Notepad), שומרים, ומריצים `GOTO.bat`:

| כותבים | לאן |
|---|---|
| `TOPIC 2` | נושא 2, מהשאלה הראשונה שלו |
| `TOPIC 1 QUESTION 3` (או בשתי שורות: `TOPIC 1`, ומתחת `QUESTION 3`) | נושא 1, מהשאלה ה-3 שלו |

מספר השאלה הוא בתוך הנושא (נושא 1: 9 שאלות, נושא 2: 8, נושא 3: 13); מספר שלא קיים מקבל הודעה ורשימת הנושאים.
הנושא שנבחר מתחיל עכשיו עם כל הזמן שלו - אין בחירה של דקות. ההתקדמות נשמרת, ו-`LESSON.bat` ממשיך עם אותו שעון.
חזרה לשעון של הכיתה: `reset_lesson.bat` של המרצה.

## איך עובדים (בתוך השיעור)

**נכנסים לשאלות רק דרך `LESSON.bat`** - אין קבצי BAT לשאלות בודדות, ו-`tools/run.ps1` מסרב לרוץ בלי השיעור.
בכל שאלה:

1. המחשב מכין את הלוח ומדבר איתו בעצמו דרך כבל ה-USB: הוא כותב לתוכו את מספר הכניסה שלכם (בלי מתגים, בלי הקלדה).
   עד אז ה-HEX מציג `----`.
2. בכל שלב המסך מראה מעט טקסט: מה עושים ואיפה שמים את התשובה. הכניסות של המעגל על המתגים **השמאליים**,
   התשובה על המתגים **הימניים** (`SW3..SW0`).
3. שמים את התשובה ולוחצים **`KEY2`**: הלוח מציג `PASS` או `Err` לשנייה. אחרי PASS **המסך עובר לשלב הבא לבד**.
4. בסוף הלוח מציג `donE`, והמחשב שומר את הקוד ב-`moodle.txt` לבד - מגישים את הקובץ הזה.

## השאלות

| שאלה | מה | השלבים |
|---|---|---|
| Q01 GATE | איזה שער מוסתר בלוח? (2 כניסות) | נורה אחת → טבלת אמת → שם השער |
| Q02 SIGMA | minterms ו-maxterms של F מוסתרת (3 כניסות) | נורה אחת → חצי טבלה (A = 0) → החצי השני → כמה minterms (Σ) → כמה maxterms (Π) |
| Q03 TERMS | איזו נורה היא minterm ואיזו maxterm? (4 נורות ירוקות, 3 כניסות) | העתקת הנורות ב-111 → בכמה שורות LEDG0 דולקת → ה-minterm (דולק בשורה אחת) → ה-maxterm (כבוי בשורה אחת) |
| Q04 MATTER | איזו כניסה לא משנה את F? (כמו E = HS + H) | טבלת F → האם A משנה (זוגות שורות) → האם B משנה → הכניסה שלא משנה |
| Q05 MUX | מה מחובר ל-mux 4:1? (D0..D3 = 0, 1, C או C') | Y ב-S1 S0 = 00 עם C = 0 ו-1 → D0 → D1 → D2 → D3 |
| Q06 DECODER | decoder 2:4 שהיציאות שלו מחווטות בסדר מוסתר | הנורה של 00 → של 01 → של 10 → של 11 → אילו שתי יציאות נכנסות ל-OR של F = Σ(...) אישית |
| Q07 PRIORITY | מעגל עדיפויות, 4 כניסות, סדר כוח מוסתר | כניסה אחת → שתיים (מי מנצחת) → ארבע (החזקה) → החלשה |
| Q08 THEOREMS | אינדוקציה מלאה: 4 טענות LEFT = RIGHT על A B | זוג 0 שווה בכל השורות? → אילו זוגות נכונים → איפה הטענה האישית |
| Q09 STORY | מסיפור למשוואה: 4 מעגלים של "סטודנטים" | הנורות ב-111 → המשוואה שלכם בשורה אחת → איזו נורה היא המשוואה |
| Q10 DEMORGAN | De Morgan: 4 תשובות על הנורות | כמה 1 בתוצאה שלכם → הנורות ב-000 → איזו תשובה נכונה |
| Q11 ERRORS | טעויות נפוצות: 4 פישוטים של הביטוי האישי, שניים שגויים | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו שגויות |
| Q12 MULTIPLY | הכפלה (SOP) ופירוק (POS): 4 תשובות, שתיים נכונות | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו נכונות |
| Q13 MINSOP | SOP מינימלי של F מוסתרת | טבלה: כמה 1 → כמה איברים → כמה ליטרלים |
| Q14 NANDNOR | שתי רמות NAND-NAND או NOR-NOR, הצמתים על נורות | הנורות ב-000 → n1 הוא NAND או NOR → אילו שני ליטרלים נכנסים ל-n1 |
| Q15 GATES | מעגל רב-שלבי: n1 = G1(A,B), n2 = G2(n1,C), Y = G3(n2,D) | הנורות ב-0000 → G1 → G2 → G3 |
| Q16 MUXLOGIC | לבנות F מוסתרת מ-mux 4:1 עם קווי בחירה אישיים (שקופית 102) | טבלת F → D0 → D1 → D2 → D3 |
| Q17 LITERAL | ביטוי אישי עם ליטרל מוסתר `?` | טבלת Y מהלוח → מהו `?` → ליטרלים ב-SOP המינימלי |
| Q18 BUBBLES | bubble pushing: איזה מ-4 מעגלים מודפסים נמצא בלוח | Y ב-0000 וב-1111 → איזה מעגל |
| Q19 LATCH | קופסה עם זיכרון: איזו שורה מדליקה ואיזו מכבה | האם השתנתה במסלול → שורת ההדלקה → שורת הכיבוי |
| Q20 SEQ | 8 קופסאות - לאילו יש זיכרון (הכי קשה, אחרונה) | טבלה של קופסה אחת → קופסה אחת זוכרת → כל 8 בשני מסלולים → כל הקופסאות עם זיכרון |
| **סבב שני** | **כל נושא צעד אחד קדימה** | |
| Q21 SIGMA4 | minterms ו-maxterms עם 4 כניסות (16 שורות) | ארבעה רבעי טבלה → כמה minterms → כמה maxterms |
| Q22 DEC38 | decoder 3:8 בסדר מוסתר | הנורה של 000 → של 111 → של ה-minterm האישי |
| Q23 THEOREMS8 | אינדוקציה מלאה: 8 טענות על A B C | טענה 0 נכונה? → כמה נכונות → איפה הטענה האישית |
| Q24 STORY4 | סיפור עם 4 אותיות | הנורות ב-1111 → המשוואה בשורה אחת → איזה מעגל |
| Q25 DEMORGAN4 | De Morgan עם 4 משתנים | הנורות ב-0000 → ב-1111 → אילו נכונות |
| Q26 MULTIPLY4 | הכפלה ופירוק עם 6 תשובות | הנורות ב-0000 → ב-1111 → אילו נכונות |
| Q27 ERRORS5 | טעויות נפוצות עם 5 פישוטים | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו שגויות |
| Q28 NANDNOR3 | שתי רמות, 3 שערים מעורבים NAND / NOR | הנורות ב-000 → n1 → כל השערים |
| Q29 BUBBLES8 | bubble pushing עם 8 מעגלים | Y ב-0000 וב-1111 → איזה מעגל |
| Q30 DLATCH | D latch: איזו כניסה היא ה-enable, ובאיזו רמה | האם השתנתה → מי ה-enable → פעיל ב-1 או ב-0 |

30 שאלות על כל החומר של הרצאה 3: Q01-Q20 מהקלה אל הקשה, ו-Q21-Q30 סבב שני שבו כל נושא מתקדם צעד.

## Instructor notes

- Questions open only through LESSON.bat: lesson.ps1 sets CE_LESSON=1, run.ps1 refuses without it, gen.py writes no Qnn BATs.
  Instructor, one question directly: `C:/DE10_solutions/class_exercise/question.bat Q05`; reset: `reset_lesson.bat` there.
- A student's own clock (missed the lesson, a technical problem): on their computer `reset_time.bat` (topic 1 starts now) or
  `reset_time.bat 2` (topic 2 starts now); the progress stays. It writes lesson_start.txt, which wins over START;
  `reset_lesson.bat` deletes it - back to the class clock, progress too.
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
