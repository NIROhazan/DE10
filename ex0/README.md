# תרגיל 0 - גל הלדים: משנים מספרים, מנבאים, בודקים

גל של אור עובר על הלדים האדומים LEDR9..LEDR0 משמאל לימין. אתם **לא כותבים לוגיקה** - משנים רק
מספרים בבלוק `KNOBS` בראש `ex0_top.v`, ובכל פעם **חוזים קודם** מה יקרה, ורק אחר כך בודקים על הלוח.
התיאוריה של השבוע: יחידות (MHz, ms, ns), עשרוני / בינארי / הקסה, כמה ביטים צריך למספר, ואחוזים.

## מה עושים

1. פותחים את `answer.txt` ב-Notepad ועונים על השאלות לפי הסדר (חלקים 1-6). חישובים - על דף, לא במחשבון של צ'אט.
2. משנים מספר ב-`ex0_top.v` (רק בין שורות ה-`KNOBS`), ושומרים.
3. כותבים חיזוי בשורה `PREDICT:` בתחתית `answer.txt`, ושומרים.
4. מריצים `run.bat` (דאבל-קליק). הוא מקמפל, מדפיס כמה חומרה נבנתה ואזהרות חשובות, וצורב ללוח.
5. משווים למה שחזיתם וכותבים ב-`answer.txt` מה **ראיתם**.

**בלי חיזוי - אין ריצה.** `run.bat` מסרב לרוץ כשהשורה `PREDICT:` ריקה, ומוחק אותה אחרי כל ריצה מוצלחת.
כל ריצה נרשמת ב-`history.txt` עם השעה, המספרים והחיזוי - המרצה יסתכל בו בבדיקה.

| הכפתור ב-KNOBS | מה הוא עושה |
|---|---|
| `MOVE_DIV` | כמה תקתוקי שעון (50 MHz) לכל צעד של הגל |
| `PEAK` | בהירות הלד המרכזי, באחוזים |
| `B1` / `B2` / `B3` | בהירות הלד במרחק 1 / 2 / 3 ממנו (רחוק יותר = כבוי) |

אפשר לכתוב `15_000_000` במקום `15000000` - הקו התחתון רק עוזר לקרוא.

## בבדיקה מול המרצה (2 דקות)

תתבקשו, בלי מחשב עזר: לעשות את הגל מהר פי 2 בדיוק; לומר **לפני** קומפילציה מה יקרה עם מספר שהמרצה בוחר;
לכתוב את ה-MOVE_DIV שלכם ב-hex על דף; ולהראות איפה קראתם כמה logic elements נבנו.

## Instructor notes

- Week 1 (meeting 1): no Verilog writing. `led_wave.v` (the demo) now takes `PEAK`, `B1`-`B3` as 7-bit
  parameters; `ex0_top.v` passes them from a `KNOBS` block of `localparam`s.
- `run.bat` -> `tools/run.ps1`: refuses to run with an empty `PREDICT:` line, appends knobs + prediction
  to `history.txt` (not in git), compiles, prints LEs / registers / `truncated value` / `stuck at` lines,
  programs, then empties `PREDICT:`. No Claude step.
- Traps (all verified in iverilog and Quartus 13.0sp1): `MOVE_DIV = 50_000_000` never fits the 25-bit
  counter, so the wave freezes on LEDR9 (Quartus: 238 -> 52 LEs, 54 -> 27 registers, LEDR3-5 stuck at GND);
  `B1 = 130` is truncated to 2, so the LEDs next to the peak go almost dark (warning at led_wave.v line 19); `MOVE_DIV = 10` gives an
  even 29.9 % on all ten LEDs. Do not use `MOVE_DIV = 5000` as the "too fast" value - its loop period equals
  the 1 ms PWM period and the LEDs come out uneven (20-50 %).
- Per-digit step times are 100 + 60 d ms (all below the 671 ms limit, none equal to the default 300 ms).
- Answers in `C:\DE10_solutions\ex0\ANSWERS.md` - not in this repo.
- Default build: 238 LEs, 54 registers, Fmax 175.3 MHz (Slow model).
