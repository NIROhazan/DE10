# תרגיל כיתה - שבוע 4 (הרצאה 4): מהקל אל הקשה, ואי אפשר בלי הלוח

אותה שיטה כמו תרגיל הכיתה של הרצאה 3 (`C:\DE10\class_exercise`): בכל שאלה מוסתר בלוח מספר, מעגל או שער, ורק
משחק במתגים והסתכלות על הנורות והתצוגה נותנים את התשובה. השאלות מחולקות לשלבים קטנים, והקושי עולה בהדרגה.

## איך עובדים

1. דאבל-קליק על `LESSON.bat`. המחשב מכין את הלוח ומדבר איתו לבד דרך כבל ה-USB. עד אז התצוגה מציגה `----`.
2. בכל שלב המסך מראה מה עושים ואיפה שמים את התשובה. התשובה על המתגים הימניים, ואז **`KEY2`**:
   `PASS` - המסך עובר לשלב הבא לבד; `Err` - לנסות שוב.
3. בסוף השאלה הקוד נשמר לבד ב-`moodle.txt` (שורות `w4ce-Qnn`) - מגישים את הקובץ הזה.
4. חץ שמאלה / ימינה = חזרה לשלב קודם / קדימה עד השלב שהגעתם אליו. חלון שנסגר ממשיך מאיפה שעצרתם.

לבחור נושא ושאלה: לכתוב ב-`goto.txt` למשל `TOPIC 2` או `TOPIC 1 QUESTION 3`, ואז `LESSON.bat`.
פירוט מלא של כל שאלה: [`QUESTIONS.md`](QUESTIONS.md).

## השאלות

| נושא (30 דקות כל אחד) | שאלה | מה |
|---|---|---|
| **1. מפות קרנו** | Q01 | מפה של שני משתנים: התאים, והמכפלה של העיגול |
| | Q02 | מפה של שלושה משתנים, עיגול אחד (גם מעבר לקצה) |
| | Q03 | שלושה משתנים: כמה עיגולים, והמכפלה של העיגול שמכסה תא שבתצוגה |
| | Q04 | מכפלות ראשוניות וחיוניות: כמה יש |
| | Q05 | מפה של ארבעה משתנים: ארבע שורות, כמה עיגולים, ועיגול של תא |
| **2. לא אכפת, השהיה ותקלות רגעיות** | Q06 | מפה של שלושה משתנים עם לא אכפת |
| | Q07 | מקטע מוסתר של מפענח BCD, עם לא אכפת ב-10 עד 15 |
| | Q08 | המעגל של השקופית: tpd של המסלול הקריטי ו-tcd של הקצר |
| | Q09 | מעגל עם שני ענפים: איזה מסלול קריטי, tpd ו-tcd |
| | Q10 | גליץ': איזה משתנה גורם לו, ואיזו מכפלה מתקנת |
| **3. תיאור חומרה** | Q11 | לקרוא מקטעים בסדר abc_defg, ולכתוב את הספרה הבאה |
| | Q12 | if / else בתוך always_comb: איזה שער בכל ענף |
| | Q13 | case עם שורה שגויה: ה-default, הספרה והמקטע השגויים |
| | Q14 | casez עם סדר עדיפות מוסתר |
| | Q15 | שורה של casez עם סימני שאלה: לגלות את התבנית |

## Instructor notes

- Source: `C:/DE10_solutions/week4/class_exercise/gen_w4.py` - the lecture-3 engine with `PREFIX = "w4|"`, `REPO` = this folder.
  `python gen_w4.py` simulates, `--compile` builds `sof/`, `--id <ID>` (= `answers.bat ce4 <ID>`) prints a student's answers.
- Instructor guide (questions, the lecture part and slides each covers, how every answer is found):
  `C:/DE10_solutions/week4/class_exercise/instructor_guide/guide.html`.
- `tools/` = the same tools as week 2, with `tools/label.txt` = `w4ce`. `verify.bat` counts the codes in the Week4 column.
  Reset a computer: delete progress.txt, moodle.txt, lesson_start.txt, lesson_pos.txt, goto_applied.txt here.
