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
| | Q04 | מספר הקסדצימלי בתצוגה - לעשרוני |
| | Q05 | כמה ביטים וכמה ספרות הקס צריך למספר שבתצוגה |
| | Q06 | הערכת 2 בחזקה גדולה: קילו / מגה / גיגה, כפול כמה |
| **2. חיבור ומספרים עם סימן** | Q07 | מחבר שמוסיף מספר מוסתר: המספר, הגלישה, הסכום ב-4 ביטים |
| | Q08 | סימן וגודל: שלילי?, הגודל, ואותו מספר במשלים ל-2 |
| | Q09 | משלים ל-2: שלילי?, ערך מוחלט, היפוך סימן |
| | Q10 | מספר שלילי בתצוגה - במשלים ל-2 ב-4 וב-8 ביטים |
| | Q11 | הטווח של N ביטים: בלי סימן, משלים ל-2, סימן וגודל |
| | Q12 | פעולה מוסתרת על מספר (מינוס, היפוך ביטים, ועוד 1 ...) |
| | Q13 | חיסור: המספר הנגדי, והתוצאה |
| | Q14 | חיבור של שני מספרים עם סימן, וגלישה |
| | Q15 | הרחבת סימן והרחבה באפסים |
| **3. שערים וטרנזיסטורים** | Q16 | שער מוסתר של שתי כניסות |
| | Q17 | שער מוסתר של שלוש כניסות (כולל זוגיות) |
| | Q18 | שער מוסתר של ארבע כניסות, בשלוש בדיקות |
| | Q19 | אילו טרנזיסטורים דולקים ב-NAND / NOR, ולאן מחוברת היציאה |
| | Q20 | איזה שער, nMOS / pMOS בטור או במקביל, כמה טרנזיסטורים |
| | Q21 | שער CMOS מורכב: הפונקציה, וטור / מקביל ברשת התחתונה |

## Instructor notes

- Source: `C:/DE10_solutions/week2/class_exercise/gen_w2.py` - imports the lecture-3 engine (`C:/DE10_solutions/class_exercise/gen.py`)
  with `PREFIX = "w2|"` (other codes and variants), `REPO` = this folder. `python gen_w2.py` simulates, `--compile` builds `sof/`,
  `--id <ID>` (= `answers.bat ce2 <ID>`) prints a student's answers. New output kinds in the engine: a HEX digit (`H`) and a minus (`M`),
  for numbers shown on the 7-segment display.
- Instructor guide (questions, the lecture part and slides each covers, how every answer is found):
  `C:/DE10_solutions/week2/class_exercise/instructor_guide/guide.html`; with one student's answers: `QUESTIONS_ANSWERS.md` there.
- `tools/` = the lecture-3 tools (identical), plus `tools/label.txt` = `w2ce` (the codes' label in moodle.txt). `verify.bat` counts
  them in the Week2 column. Reset a computer: delete progress.txt, moodle.txt, lesson_start.txt, lesson_pos.txt, goto_applied.txt here.
