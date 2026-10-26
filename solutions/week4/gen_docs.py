# week4 ex8..ex10: bats and READMEs; week4/README.md
import os
W4 = "C:/DE10/week4"
BS = chr(92)

def write(path, text):
    with open(path, "wb") as f:
        f.write(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8"))

EX = {
    8: ("Exercise 8 - critical path and short path", [
        ("Q1", "GATES", "measure the delay of each gate type (needs the board)"),
        ("Q2", "TPD_TCD", "tpd and tcd of a puzzle (needs the board)"),
        ("Q3", "PAPER", "tpd and tcd of a circuit on paper"),
        ("Q4", "FASTER", "a faster gate type: the new tpd (paper)")]),
    9: ("Exercise 9 - glitches", [
        ("Q1", "FUNCTION", "the hidden Y as a minimal SOP (needs the board)"),
        ("Q2", "GLITCH", "the switch flip that makes Y glitch (needs the board)"),
        ("Q3", "TIMING", "when the glitch starts and ends (paper + board)"),
        ("Q4", "FIX", "the term that removes the glitch")]),
    10: ("Exercise 10 - case and casez", [
        ("Q1", "VALUE", "y for one value of a"),
        ("Q2", "DEFAULT", "how many values of a reach default"),
        ("Q3", "NEVER", "the line that never fires"),
        ("Q4", "BIT_SOP", "one bit of y as a minimal SOP (K-map)")]),
}
for n, (title, qs) in EX.items():
    for q, name, what in qs:
        write(f"{W4}/ex{n}/{q}_{name}.bat", f"""@echo off
rem ============================================================
rem  {title}
rem  {q}: {what}
rem  Programs the board, asks the question here with your own
rem  numbers, and checks your answer. A wrong answer gives NEW
rem  numbers. A right one gives a code in moodle.txt for Moodle.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools{BS}run.ps1" -Only {q}
echo.
pause
""")

COMMON = """## איך עובדים

- לכל שאלה קובץ BAT משלה (`Q1_....bat`). דאבל-קליק: הלוח נצרב, השאלה מופיעה בחלון, מקלידים את התשובה שם. לא עורכים שום קובץ.
- **המספרים אישיים** - נבנים ממספר הסטודנט (נשמר ב-`student.txt` בתיקיית הקורס, אותו מספר לכל התרגילים).
- **תשובה שגויה = מספרים חדשים.** אין טעם לנחש - פותרים שוב מההתחלה.
- תשובה נכונה נותנת **קוד** בקובץ `moodle.txt` - אותו מגישים במודל. כל ניסיון נרשם ב-`results.txt`.
- `S` = לדלג על השאלה, `Q` = לעצור.
- SW0 הוא המתג הימני ביותר, HEX0 התצוגה הימנית ביותר.
"""

write(f"{W4}/ex8/README.md", """# תרגיל 8 - מסלול קריטי ומסלול קצר (Timing)

הרצאה 4: השהיה (delay), `tpd` = ההשהיה הארוכה ביותר מכניסה ליציאה (המסלול הקריטי), `tcd` = הקצרה ביותר (המסלול הקצר).

## הלוח - מעגל בהילוך איטי

- `A = SW0`, `B = SW1`, `C = SW2`, `D = SW3`. מספר הפאזל = `SW9..SW7` בבינארי.
- המעגל מההרצאה: `n1 = A AND B`, `n2 = NOT C`, `n3 = n1 OR n2`, `Y = n3 AND D`. ‏`LEDG0 = Y`.
- **הילוך איטי:** כל שער מחכה כמה "טיקים" (טיק = 0.1 שנייה) עד שהיציאה שלו מגיבה. לכל השערים מאותו סוג אותה השהיה;
  ההשהיות נסתרות ותלויות בפאזל.
- **שעון עצר:** אחרי שמזיזים מתג אחד - `HEX3 HEX2` = מספר הטיקים עד השינוי **האחרון** של Y, `HEX1 HEX0` = עד השינוי **הראשון**
  (`00` = Y לא השתנה). `LEDR3..0` = כמה פעמים Y השתנה.
- הטריק: לבחור את שאר המתגים כך שהמסלול "פתוח" - השינוי באמת מגיע ל-Y (למשל: כדי ש-D יגיע ל-Y, צריך `n3 = 1`).

## השאלות

| קובץ | מה שואלים |
|---|---|
| `Q1_GATES.bat` | מודדים את ההשהיה של AND, של OR ושל NOT (לוח) |
| `Q2_TPD_TCD.bat` | `tpd` ו-`tcd` של פאזל - איזה מסלול הוא הקריטי? (לוח) |
| `Q3_PAPER.bat` | מעגל על הנייר עם השהיות ב-ps משלכם: `tpd` ו-`tcd` |
| `Q4_FASTER.bat` | סוג שער אחד נעשה מהיר יותר - מה ה-`tpd` החדש? (המסלול הקריטי עלול להתחלף) |

""" + COMMON + """
## למרצה

`board.sof` נבנה מ-`C:\\DE10\\solutions\\week4\\gen_w4.py` (המעגל עם `dly` = shift register לכל שער, טיק של 0.1 s).
ב-`tools/secrets.txt` יש רק hash של התשובות. Q3-Q4 מחושבות ב-`tools/questions.ps1`. תשובות: `answers.bat w4-ex8 <ID>`.
""")

write(f"{W4}/ex9/README.md", """# תרגיל 9 - Glitches

הרצאה 4: Glitch = שינוי של כניסה אחת שגורם ליציאה להשתנות כמה פעמים. רואים אותו בסימולציה או באוסצילוסקופ - וכאן, על הלוח, בהילוך איטי.

## הלוח

- `A = SW0`, `B = SW1`, `C = SW2`. מספר הפאזל = `SW9..SW7` בבינארי. `SW6` = התיקון (להשאיר **למטה** עד Q4).
- בכל פאזל `Y` (‏`LEDG0`) הוא SOP נסתר של שני איברים, בנוי משערי NOT / AND / OR בהילוך איטי (טיק = 0.1 שנייה).
- אחרי שמזיזים מתג אחד: `HEX3 HEX2` = טיקים עד השינוי **האחרון** של Y, `HEX1 HEX0` = עד **הראשון**, `LEDR3..0` = כמה פעמים Y השתנה.
  **2 שינויים כש-Y היה אמור להישאר אותו דבר = glitch.**
- מחכים שהמספרים ייעצרו לפני שקוראים את Y.

## השאלות

| קובץ | מה שואלים |
|---|---|
| `Q1_FUNCTION.bat` | Y של הפאזל כ-SOP מינימלי (8 שורות על הלוח, מפת קרנו) |
| `Q2_GLITCH.bat` | איזה מתג, ומאיזה מצב של A B C, עושה glitch |
| `Q3_TIMING.bat` | מתי Y משתבש, מתי חוזר, וכמה זמן הוא שגוי - מההשהיות של השערים, ואז בודקים על הלוח |
| `Q4_FIX.bat` | איזה איבר מוסיפים ל-Y כדי שה-glitch ייעלם (`SW6` למעלה מראה שזה עובד) |

רמז מההרצאה: glitch קורה כששני 1 שכנים במפת קרנו נמצאים בעיגולים שונים - המעבר ביניהם "קופץ" מעיגול לעיגול.

""" + COMMON + """
## למרצה

`board.sof` נבנה מ-`C:\\DE10\\solutions\\week4\\gen_w4.py`: `Y = L1 V' + V L2` (+ `L1 L2` כש-SW6 למעלה), ה-NOT של V הוא שער אמיתי (איטי).
הפונקציות וה-glitch רק כ-hash ב-`tools/secrets.txt`; ההשהיות של כל פאזל פתוחות ב-`tools/puzzles.txt`.
תשובה מסוג SOP נבדקת לפי טבלת האמת + מספר האיברים/הליטרלים (`Get-SopKey`), כך שכל SOP מינימלי שקול מתקבל. תשובות: `answers.bat w4-ex9 <ID>`.
""")

write(f"{W4}/ex10/README.md", """# תרגיל 10 - case ו-casez

הרצאה 4 (Harris פרק 4): לוגיקה צירופית עם `always`, ‏`case`, ‏`casez` (‏`?` = לא אכפת), ושורת `default` שחייבת להיות.

## הלוח

- מספר הפאזל = `SW9..SW6` (מוצג ב-`HEX1`), ‏`a = SW3..SW0` (מוצג ב-`HEX0`), ‏`y` = ‏`LEDG3..LEDG0` וגם `HEX3` (הקסה).
- בכל פאזל בלוק אחד: `always @(*) casez (a) ... default: y = 4'h0; endcase` - הקוד שלו מוצג בשאלה.
- קודם קוראים את הקוד וחושבים, **אחר כך** בודקים על הלוח.

## השאלות

| קובץ | מה שואלים |
|---|---|
| `Q1_VALUE.bat` | מה `y` עבור `a` מסוים |
| `Q2_DEFAULT.bat` | לכמה ערכים של `a` מגיעים ל-`default` (ובלעדיו - latch) |
| `Q3_NEVER.bat` | איזו שורה אף פעם לא "יורה" (`casez` לוקח את השורה הראשונה שמתאימה) |
| `Q4_BIT_SOP.bat` | ביט אחד של `y` כ-SOP מינימלי של `A B C D` (מפת קרנו של 4 משתנים) |

""" + COMMON + """
## למרצה

`board.sof` נבנה מ-`C:\\DE10\\solutions\\week4\\gen_w4.py`: 16 בלוקים של casez, בכל אחד בדיוק שורה אחת שאף פעם לא יורה, ו-1 עד 6 ערכים שמגיעים ל-default.
הקוד פתוח (`tools/puzzles.txt`), התשובות מחושבות ב-`tools/questions.ps1`. תשובות: `answers.bat w4-ex10 <ID>`.
""")

write(f"{W4}/README.md", """# שבוע 4 - הרצאה 4 (Harris פרק 2 + פרק 4)

מפות קרנו (2, 3, 4 משתנים), Prime implicants, "לא אכפת" (X), Timing (‏tpd, ‏tcd, מסלול קריטי), Glitches, ו-`case` / `casez` ב-Verilog.

| תרגיל | נושא |
|------|------|
| [ex1](ex1/README.md) | מפת קרנו - ארבעה משתנים, SOP, POS ו-XOR (לוח שחמט) |
| [ex2](ex2/README.md) | מפת קרנו - SOP מינימלי מול POS מינימלי (ארבע הפינות) |
| [ex3](ex3/README.md) | מפת קרנו - שורות "לא אכפת" (X), שלושה משתנים |
| [ex4](ex4/README.md) | מפת קרנו - שלושה משתנים, עיגול שעוטף את הקצה |
| [ex5](ex5/README.md) | Implicant, Prime implicant ו-Essential |
| [ex6](ex6/README.md) | מפת קרנו - ארבעה משתנים, עיגולים של 8 ושל 4 |
| [ex7](ex7/README.md) | תצוגת 7 מקטעים: ספרת BCD עם X |
| [ex8](ex8/README.md) | Timing: מסלול קריטי ומסלול קצר (לוח בהילוך איטי) |
| [ex9](ex9/README.md) | Glitches: למצוא, למדוד ולתקן (לוח בהילוך איטי) |
| [ex10](ex10/README.md) | `case` ו-`casez` |

ex1-ex7: טבלת אמת אישית (או מקטע אישי), שאלה אחת בכל BAT, או `answer.txt` + `run.bat` עם משוב של Claude - כמו בשבוע 3.
ex8-ex10: שאלה אחת בכל BAT עם מספרים אישיים, תשובה שגויה = מספרים חדשים - כמו בשבוע 2.
ex1-ex3 הגיעו מ-`other/` (היו שם ex4, ex5, ex6).
""")
print("ok")
