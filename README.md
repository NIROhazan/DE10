# DE10

Digital systems course on the **Terasic DE10-Lite** (MAX 10 `10M50DAF484C7G`). One folder per week: the week's class
exercise. Quartus Prime Lite with MAX 10 support is at `C:\altera_lite\25.1std` (or `C:\altera_standard\25.1std`).

| Folder / file | What it is |
|---|---|
| `week1/` | Week 1 board lab |
| `week2/` ... `week11/` | The class exercise of that week: `LESSON.bat`, the questions, `sof/` (one board per question) |
| `tools/` | The lesson scripts, shared by every week |
| `other/ex0/` | Week 1 LED wave demo (change numbers, predict, check on the board) |
| `top.v` / `top.qpf` / `top.qsf` / `top.sdc` | Blank starter project: SW -> LEDR, HEX2..HEX0 show SW in hex, HEX0's dot blinks at 1 Hz |
| `DE10_Lite_pin_assignments.qsf` | Full DE10-Lite pin list, copy lines from it when you use more of the board |

| Week | Lecture |
|---|---|
| [`week2`](week2/README.md) | 2 - number systems, signed numbers, gates, CMOS (Harris ch. 1) |
| [`week3`](week3/README.md) | 3 - Boolean equations, SOP / POS, theorems, building blocks (Harris ch. 2) |
| [`week4`](week4/README.md) | 4 - Karnaugh maps, don't-cares, timing, glitches |
| [`week5`](week5/README.md) | 5 - latches, flip-flops, registers |
| [`week6`](week6/README.md) | 6 - finite state machines |
| [`week7`](week7/README.md) | 7 - Moore and Mealy, factoring and designing FSMs |
| [`week8`](week8/README.md) | 8 - timing, synchronizers, parallelism |
| [`week9`](week9/README.md) | 9 - adders, comparators, parameterized modules |
| [`week10`](week10/README.md) | 10 - ALU, shifters, multiplication, division |
| [`week11`](week11/README.md) | 11 - fixed and floating point, counters, shift registers, memories |

## איך עובדים (הסטודנטים)

1. דאבל-קליק על `LESSON.bat` בתיקייה של השבוע, ומכניסים תעודת זהות. הזמן של השיעור מתחיל מהרגע הזה.
2. בתפריט בוחרים שאלה: חץ ימינה / שמאלה = נושא, חץ למעלה / למטה = שאלה, Enter = לפתוח. רק אז הלוח נצרב.
3. המחשב מדבר עם הלוח לבד דרך כבל ה-USB. עד שהוא מוכן התצוגה מציגה `----`.
4. בכל שלב המסך מראה מה עושים. התשובה על המתגים הימניים, ואז **`KEY0`**: `PASS` - עוברים לשלב הבא לבד; `Err` - לנסות שוב.
5. בסוף השאלה הלוח מציג `donE`, והקוד נשמר לבד ב-`moodle.txt` - מגישים את הקובץ הזה.
6. חץ שמאלה / ימינה = השלב הקודם / הבא (אפשר לדלג; את השלב האחרון צריך לפתור). חלון שנסגר ממשיך מאיפה שעצרתם.

## Instructor notes

- **Boards:** every question is one board, `weekN/sof/Qnn.sof`: the hidden circuit, every step's answer and the Moodle code
  are inside the board; the PC holds none of them. The PC link is In-System Sources and Probes (`tools/link.tcl`):
  the PC writes {go, start step, login number}, the board reports {done, step, code}.
- **Source of week 2** (not in this repo): `C:\DE10_solutions\class_exercise_de10\` = the shared engine (`gen_lib.py`, `ce_top.v`) and
  `secret.txt`, the key of the codes and of every student's numbers - keep it, and keep it private.
  Each week: `C:\DE10_solutions\weekN\class_exercise\gen_wN.py`.
  - `py gen_wN.py` checks every question for all 1024 login numbers
  - `py gen_wN.py --compile [Qnn ...]` builds `weekN/sof/`
  - `py gen_wN.py --id <ID>` prints a student's login number, every step's answer and the codes
  - `py gen_wN.py --verify <moodle.txt> ...` checks handed-in codes
- **Texts:** `weekN/questions.txt` (what the screen shows), `weekN/lesson.txt` (topics and minutes), `weekN/label.txt`
  (the codes' label, e.g. `w2ce`), `tools/ui.txt` (fixed Hebrew messages). A line is either Hebrew or English, never both.
- **Reset a computer:** delete `progress.txt`, `moodle.txt`, `lesson_start.txt`, `lesson_pos.txt` in the week's folder;
  `student.txt` (the ID) is here in the course folder.
- **Do one question again:** in the question menu the student presses `R` on it, then `Y`. Its lines in
  `progress.txt` are removed, so it starts from step 1 as new; the lesson clock and the Moodle code already
  earned stay.
- **Weeks 3-11** are ported with `C:\DE10\solutions\de10\port.py`: the questions, answers and codes of the DE1
  generators (`class_exercise\gen.py` for week 3, `weekN\class_exercise\gen_wN.py`, same `class_exercise\key.txt`)
  in a DE10-Lite top level. `KEY0` = check; the DE10 has no green LEDs, so `LEDGi` is now `LEDRi` (questions with red
  and green outputs move the green ones up, or a free switch picks which LEDs show). The screens say the same.
  - `py port.py N` simulates week N and writes `weekN/questions.txt`, `QUESTIONS.md` (and `lesson.txt` for weeks 5-11)
  - `py port.py N --compile [--only Qnn ...]` builds `weekN/sof/` with Quartus Prime 25.1
  - `py port.py N --id <ID>` prints a student's login number, every step's answer and the codes
- The old per-topic exercises (weeks 2-4 `exN`) and `locked/` are kept outside the repo in `C:\DE10_solutions\old_exercises\`.
- **Weeks 3-11, the source and the answers:** [`solutions/`](solutions/README.md) - how to fix a question and rebuild its board.

## Starter project

```
C:\altera_lite\25.1std\quartus\bin64\quartus_sh --flow compile top
C:\altera_lite\25.1std\quartus\bin64\quartus_pgm -c USB-Blaster -m jtag -o "p;output_files/top.sof"
```
