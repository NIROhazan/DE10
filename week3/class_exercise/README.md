# תרגיל כיתה - הרצאה 3 (Harris פרק 2): מהקל אל הקשה, ואי אפשר בלי הלוח

השאלות מסודרות **מהקלה אל הקשה**, וכל שאלה מחולקת לשלבים קטנים שגם הם עולים בקושי. התשובה נמצאת רק בתוך
הלוח: בכל שאלה מוסתר בו מעגל, ורק משחק במתגים והסתכלות על הנורות נותנים את התשובה. גם הבדיקה בלוח.

## שיעור שלם: `LESSON.bat`

דאבל-קליק על `LESSON.bat`, ומכניסים תעודת זהות. **הזמן של השיעור מתחיל מהרגע הזה** (נשמר ב-`lesson_start.txt`), ונגמר אחרי הדקות של כל הנושאים יחד (`tools/lesson.txt`). הזמנים של הנושאים הם רק המלצה:

| זמן | נושא | שאלות (מהקל לקשה) |
|---|---|---|
| 40 דקות | טבלאות אמת, minterms ו-maxterms, תיאורמות | Q01-Q12 |
| 40 דקות | ממילים למשוואה: סיפורים, De Morgan, טעויות, הכפלה ופירוק | Q13-Q22 |
| 40 דקות | אבני בניין ומעגלים: mux, decoder, עדיפויות, NAND/NOR, רב-שלבי, bubbles, ובסוף זיכרון | Q23-Q38 |

- **תפריט השאלות:** לפני כל שאלה מופיעה רשימה של השאלות, נושא אחד בכל דף: חץ ימינה / שמאלה = נושא אחר, חץ למעלה / למטה = שאלה, Enter = לפתוח. רק אחרי הבחירה המחשב צורב את הלוח. שאלה שהסתיימה נפתחת שוב לחזרה.
- **יציאה וחזרה:** כל שלב שעבר נשמר מיד (`progress.txt`), והזמן ממשיך לרוץ גם כשהחלון סגור. מי שחוזר מקבל "ברוכים השבים" והתפריט עומד על השאלה שבה עצר. שיעור שנגמר לפני יותר משעתיים - השעון מתחיל מחדש.
- **איפוס ידני של הזמן לסטודנט** (תקלה): המרצה מריץ `C:\DE10_solutions\class_exercise\reset_time.bat`; איפוס מלא: `C:\DE10_solutions\class_exercise\reset_lesson.bat`. ההתקדמות נשמרת בשניהם חוץ מבאיפוס המלא.
- `goto.txt` לא נחוץ. אם כותבים בו `TOPIC 2` או `TOPIC 1 QUESTION 3`, התפריט רק נפתח על השאלה הזאת (השעון לא משתנה).

## המסכים בעברית

השאלות וההודעות על המסך בעברית, קצרות ובשלבים. כל שורה היא או עברית או אנגלית (שמות מתגים, נוסחאות, אותיות) -
אף פעם לא שתיהן, כי החלון השחור לא יודע לערבב כיוונים. שורה בעברית מוצגת מיושרת לימין.

## איך עובדים (בתוך השיעור)

**נכנסים לשאלות רק דרך `LESSON.bat`** - אין קבצי BAT לשאלות בודדות, ו-`tools/run.ps1` מסרב לרוץ בלי השיעור.
בכל שאלה:

1. המחשב מכין את הלוח ומדבר איתו בעצמו דרך כבל ה-USB: הוא כותב לתוכו את מספר הכניסה שלכם (בלי מתגים, בלי הקלדה).
   עד אז ה-HEX מציג `----`.
2. בכל שלב המסך מראה מעט טקסט: מה עושים ואיפה שמים את התשובה. הכניסות של המעגל על המתגים **השמאליים**,
   התשובה על המתגים **הימניים** (`SW3..SW0`).
3. שמים את התשובה ולוחצים **`KEY2`**: הלוח מציג `PASS` או `Err` לשנייה. אחרי PASS **המסך עובר לשלב הבא לבד**.
4. בסוף הלוח מציג `donE`, והמחשב שומר את הקוד ב-`moodle.txt` לבד - מגישים את הקובץ הזה.
5. **מעבר בין שלבים:** חץ שמאלה = השלב הקודם, חץ ימינה = השלב הבא - אפשר גם לדלג על שלב שלא פתרתם (המחשב מעביר את הלוח לשם). את השלב האחרון צריך לפתור כדי לקבל את הקוד.
   שאלה שכבר הסתיימה נפתחת שוב מהשלב הראשון אם בוחרים אותה בתפריט. ההתקדמות לא יורדת אחורה.
6. **בחירת שאלה:** לפני כל שאלה מופיעה רשימת השאלות של הנושא. בוחרים בחץ למעלה / למטה ולוחצים Enter - רק אז הלוח נצרב. בתוך שאלה, חץ למטה / למעלה מחזיר לרשימה (על השאלה הבאה / הקודמת), גם אם לא סיימתם.

## השאלות

פירוט מלא של כל שאלה - מה על הלוח, המתגים, הנתון האישי וכל השלבים, לפי נושא: [`QUESTIONS.md`](QUESTIONS.md).

השמות לפי סדר השיעור: נושא 1 = Q01-Q12, נושא 2 = Q13-Q22, נושא 3 = Q23-Q38. כל נושא נפתח בשאלות קלות על המעגלים של השקפים עצמם, ואחריהן שאלות האתגר.

| שאלה | מה | השלבים |
|---|---|---|
| **נושא 1 - טבלאות אמת, minterms ו-maxterms, תיאורמות** (40 דקות) | | |
| Q01 SOP2 | המעגל של שקופית 12: `Y = A'B + AB = Σ(1,3)` | טבלת האמת (4 שורות) → Y בשורה שמוצגת ב-HEX0 |
| Q02 CAFE | הקפטריה של שקופיות 14-16: `E = CM' = Π(0,1,3)` | כמה מקסטרמים → הסכום של המקסטרם בשורה מ-HEX0 |
| Q03 COVER | משפט הכיסוי `B(B+C) = B` (שקופיות 39-40), שני הצדדים על נורות | אינדוקציה מלאה: שווים תמיד? → שתי הנורות בשורה מ-HEX0 |
| Q04 GATE | איזה שער מוסתר בלוח? (2 כניסות) | נורה אחת → טבלת אמת → שם השער |
| Q05 SIGMA | minterms ו-maxterms של F מוסתרת (3 כניסות) | נורה אחת → חצי טבלה (A = 0) → החצי השני → כמה minterms (Σ) → כמה maxterms (Π) |
| Q06 TERMS | איזו נורה היא minterm ואיזו maxterm? (4 נורות ירוקות, 3 כניסות) | העתקת הנורות ב-111 → בכמה שורות LEDG0 דולקת → ה-minterm (דולק בשורה אחת) → ה-maxterm (כבוי בשורה אחת) |
| Q07 MATTER | איזו כניסה לא משנה את F? (כמו E = HS + H) | טבלת F → האם A משנה (זוגות שורות) → האם B משנה → הכניסה שלא משנה |
| Q08 SIGMA4 | minterms ו-maxterms עם 4 כניסות (16 שורות) | ארבעה רבעי טבלה → כמה minterms → כמה maxterms |
| Q09 THEOREMS | אינדוקציה מלאה: 4 טענות LEFT = RIGHT על A B | זוג 0 שווה בכל השורות? → אילו זוגות נכונים → איפה הטענה האישית |
| Q10 THEOREMS8 | אינדוקציה מלאה: 8 טענות על A B C | טענה 0 נכונה? → כמה נכונות → איפה הטענה האישית |
| Q11 MINSOP | SOP מינימלי של F מוסתרת | טבלה: כמה 1 → כמה איברים → כמה ליטרלים |
| Q12 LITERAL | ביטוי אישי עם ליטרל מוסתר `?` | טבלת Y מהלוח → מהו `?` → ליטרלים ב-SOP המינימלי |
| **נושא 2 - ממילים למשוואה: סיפורים, De Morgan, טעויות, הכפלה ופירוק** (40 דקות) | | |
| Q13 PARK | הפארק של שקופית 17: `P = R'S` | באיזו שורה P דולקת → P בשורה מ-HEX0 |
| Q14 DMGATES | דה-מורגן בשערים (שקופית 93): NAND ו-NOR, כל אחד בשתי צורות | אינדוקציה מלאה: כל זוג שווה? → 4 הנורות בשורה מ-HEX0 |
| Q15 STORY | מסיפור למשוואה: 4 מעגלים של "סטודנטים" | הנורות ב-111 → המשוואה שלכם בשורה אחת → איזו נורה היא המשוואה |
| Q16 DEMORGAN | De Morgan: 4 תשובות על הנורות | כמה 1 בתוצאה שלכם → הנורות ב-000 → איזו תשובה נכונה |
| Q17 ERRORS | טעויות נפוצות: 4 פישוטים של הביטוי האישי, שניים שגויים | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו שגויות |
| Q18 MULTIPLY | הכפלה (SOP) ופירוק (POS): 4 תשובות, שתיים נכונות | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו נכונות |
| Q19 STORY4 | סיפור עם 4 אותיות | הנורות ב-1111 → המשוואה בשורה אחת → איזה מעגל |
| Q20 DEMORGAN4 | De Morgan עם 4 משתנים | הנורות ב-0000 → ב-1111 → אילו נכונות |
| Q21 ERRORS5 | טעויות נפוצות עם 5 פישוטים | כמה 1 ב-Y שלכם → הנורות ב-000 → אילו שגויות |
| Q22 MULTIPLY4 | הכפלה ופירוק עם 6 תשובות | הנורות ב-0000 → ב-1111 → אילו נכונות |
| **נושא 3 - אבני בניין ומעגלים, ובסוף זיכרון** (40 דקות) | | |
| Q23 MUX2 | mux 2:1 משערים (שקופית 100): `Y = S'D0 + SD1` | איזו כניסה עוברת כש-S = 0 → Y בשורה מ-HEX0 |
| Q24 DEC24 | decoder 2:4 (שקופיות 104-105) | כמה נורות דולקות (one-hot) → איזו נורה בשורה מ-HEX0 |
| Q25 PRIO4 | מעגל העדיפויות של שקופית 81 | כל הכניסות למעלה → הכניסות של HEX0 (עד ש-HEX3 זהה): איזו נורה |
| Q26 MUX | מה מחובר ל-mux 4:1? (D0..D3 = 0, 1, C או C') | Y ב-S1 S0 = 00 עם C = 0 ו-1 → D0 → D1 → D2 → D3 |
| Q27 DECODER | decoder 2:4 שהיציאות שלו מחווטות בסדר מוסתר | הנורה של 00 → של 01 → של 10 → של 11 → אילו שתי יציאות נכנסות ל-OR של F = Σ(...) אישית |
| Q28 PRIORITY | מעגל עדיפויות, 4 כניסות, סדר כוח מוסתר | כניסה אחת → שתיים (מי מנצחת) → ארבע (החזקה) → החלשה |
| Q29 MUXLOGIC | לבנות F מוסתרת מ-mux 4:1 עם קווי בחירה אישיים (שקופית 102) | טבלת F → D0 → D1 → D2 → D3 |
| Q30 DEC38 | decoder 3:8 בסדר מוסתר | הנורה של 000 → של 111 → של ה-minterm האישי |
| Q31 NANDNOR | שתי רמות NAND-NAND או NOR-NOR, הצמתים על נורות | הנורות ב-000 → n1 הוא NAND או NOR → אילו שני ליטרלים נכנסים ל-n1 |
| Q32 GATES | מעגל רב-שלבי: n1 = G1(A,B), n2 = G2(n1,C), Y = G3(n2,D) | הנורות ב-0000 → G1 → G2 → G3 |
| Q33 BUBBLES | bubble pushing: איזה מ-4 מעגלים מודפסים נמצא בלוח | Y ב-0000 וב-1111 → איזה מעגל |
| Q34 NANDNOR3 | שתי רמות, 3 שערים מעורבים NAND / NOR | הנורות ב-000 → n1 → כל השערים |
| Q35 BUBBLES8 | bubble pushing עם 8 מעגלים | Y ב-0000 וב-1111 → איזה מעגל |
| Q36 LATCH | קופסה עם זיכרון: איזו שורה מדליקה ואיזו מכבה | האם השתנתה במסלול → שורת ההדלקה → שורת הכיבוי |
| Q37 DLATCH | D latch: איזו כניסה היא ה-enable, ובאיזו רמה | האם השתנתה → מי ה-enable → פעיל ב-1 או ב-0 |
| Q38 SEQ | 8 קופסאות - לאילו יש זיכרון (הכי קשה, אחרונה) | טבלה של קופסה אחת → קופסה אחת זוכרת → כל 8 בשני מסלולים → כל הקופסאות עם זיכרון |

38 שאלות על כל החומר של הרצאה 3, בכל נושא מהקלה אל הקשה.

## Instructor notes

- Questions open only through LESSON.bat: lesson.ps1 sets CE_LESSON=1, run.ps1 refuses without it, gen.py writes no Qnn BATs.
  Instructor, one question directly: `C:/DE10_solutions/class_exercise/question.bat Q05`; reset: `reset_lesson.bat` there.
- A student's own clock (missed the lesson, a technical problem): on their computer `reset_time.bat` (topic 1 starts now) or
  `reset_time.bat 2` (topic 2 starts now); the progress stays. It writes lesson_start.txt, which wins over START;
  `reset_lesson.bat` deletes it - back to the class clock, progress too.
- Hebrew screens: question texts in `C:/DE10_solutions/class_exercise/he_text.py` (by question name; gen.py checks that no line
  mixes Hebrew and Latin), fixed messages in `tools/ui.txt` (UTF-8, `U "key"`), drawn by `Write-Line` in common.ps1 (a Hebrew line
  is put in visual order and aligned right - the console has no right-to-left). Topic names in lesson.txt are Hebrew too.
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
