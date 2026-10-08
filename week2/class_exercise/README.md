# תרגיל כיתה - שבוע 2 (הרצאה 2, Harris פרק 1): מהקל אל הקשה, ואי אפשר בלי הלוח

אותה שיטה כמו תרגיל הכיתה של הרצאה 3 (`C:\DE10\class_exercise`): בכל שאלה מוסתר בלוח מספר, מעגל או שער, ורק
משחק במתגים והסתכלות על הנורות והתצוגה נותנים את התשובה. השאלות מחולקות לשלבים קטנים, והקושי עולה בהדרגה.

## איך עובדים

1. דאבל-קליק על `LESSON.bat`. המחשב מכין את הלוח ומדבר איתו לבד דרך כבל ה-USB. עד אז התצוגה מציגה `----`.
2. בכל שלב המסך מראה מה עושים ואיפה שמים את התשובה. התשובה על המתגים הימניים, ואז **`KEY2`**:
   `PASS` - המסך עובר לשלב הבא לבד; `Err` - לנסות שוב.
3. בסוף השאלה הקוד נשמר לבד ב-`moodle.txt` (שורות `w2ce-Qnn`) - מגישים את הקובץ הזה.
4. חץ שמאלה / ימינה = חזרה לשלב קודם / קדימה עד השלב שהגעתם אליו. חלון שנסגר ממשיך מאיפה שעצרתם.

לבחור נושא ושאלה: לכתוב ב-`goto.txt` למשל `TOPIC 2` או `TOPIC 1 QUESTION 3`, ואז `LESSON.bat`.
פירוט מלא של כל שאלה: [`QUESTIONS.md`](QUESTIONS.md).

## השאלות

| נושא (30 דקות כל אחד) | שאלה | מה |
|---|---|---|
| **1. מערכות ספירה** | Q01 | מספר עשרוני בתצוגה - לבינארי (זוגי? החזקה הגדולה, כל המספר) |
| | Q02 | מספר הקסדצימלי בתצוגה - לבינארי (כל ספרה, בייט שלם) |
| | Q03 | מספר בינארי בנורות - לעשרוני (מאות, עשרות, אחדות) |
| | Q04 | כמה ביטים וכמה ספרות הקס צריך למספר שבתצוגה |
| **2. חיבור ומספרים עם סימן** | Q05 | מחבר שמוסיף מספר מוסתר: המספר, הגלישה, הסכום ב-4 ביטים |
| | Q06 | סימן וגודל: שלילי?, הגודל, ואותו מספר במשלים ל-2 |
| | Q07 | משלים ל-2: שלילי?, ערך מוחלט, היפוך סימן |
| | Q08 | מספר שלילי בתצוגה - במשלים ל-2 ב-4 וב-8 ביטים |
| | Q09 | חיסור: המספר הנגדי, והתוצאה |
| | Q10 | הרחבת סימן והרחבה באפסים |
| **3. שערים וטרנזיסטורים** | Q11 | שער מוסתר של שתי כניסות |
| | Q12 | שער מוסתר של שלוש כניסות (כולל זוגיות) |
| | Q13 | איזה שער, nMOS / pMOS בטור או במקביל, כמה טרנזיסטורים |

## Instructor notes

- Source: `C:/DE10_solutions/week2/class_exercise/gen_w2.py` - imports the lecture-3 engine (`C:/DE10_solutions/class_exercise/gen.py`)
  with `PREFIX = "w2|"` (other codes and variants), `REPO` = this folder. `python gen_w2.py` simulates, `--compile` builds `sof/`,
  `--id <ID>` (= `answers.bat ce2 <ID>`) prints a student's answers. New output kinds in the engine: a HEX digit (`H`) and a minus (`M`),
  for numbers shown on the 7-segment display.
- Instructor guide (questions, the lecture part and slides each covers, how every answer is found):
  `C:/DE10_solutions/week2/class_exercise/instructor_guide/guide.html`; with one student's answers: `QUESTIONS_ANSWERS.md` there.
- `tools/` = the lecture-3 tools (identical), plus `tools/label.txt` = `w2ce` (the codes' label in moodle.txt). `verify.bat` counts
  them in the Week2 column. Reset a computer: delete progress.txt, moodle.txt, lesson_start.txt, lesson_pos.txt, goto_applied.txt here.
