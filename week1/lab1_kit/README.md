# מעבדה 1 - משחקים עם הלוח

1. מחברים את הלוח למחשב בכבל ה-USB.
2. דאבל-קליק על `LAB1.bat`.
3. בכל שלב: עושים מה שכתוב על המסך, מסתכלים, וכותבים מה ראיתם ומה הניחוש שלכם.
   המחשב צורב לבד את הלוח כשצריך.
4. התשובות נשמרות ב-`answers_<ת.ז.>.txt` בתיקייה הזאת. בסוף הקובץ נפתח: מעלים אותו למודל.

אף אחד לא מסביר כלום היום. את התשובות נגלה במעבדות 2 עד 11.

---

## For the instructor

One folder for every student PC. Copy it whole to a **plain English path without spaces**
(e.g. `C:\lab1_kit`); Quartus is unreliable with Hebrew letters in a path.

| Item | What it is |
|---|---|
| `LAB1.bat` | Starts `tools\lab1.ps1` |
| `tools\steps.txt` | The 13 steps (Hebrew, UTF-8), in the order of the 10 riddles on slide 16 of `../L1_2026.pptx`: warm-up, riddle 1 (two parts), 2, 3, ... 10 (7 and 8 share the speed dial). Each step is titled by its riddle. Edit it freely: `== id \| design \| title`, then `>` shown, `!` shown as is, `?` asked and saved, `@ math` prints `0.1 + 0.2 == 0.3` live. |
| `tools\ui.txt` | Fixed screen texts (Hebrew) |
| `sof\` | `lab1.sof`, `card1..6.sof`, `card8.sof`, `game.sof`, `speeddial.sof`, built by `../board_lab1/build_kit.ps1` |

* **Every step programs its own `.sof` on entry** (Enter, `b` or a jump), so the board is always
  that step, whatever the switches say, and a power-cycled board is fixed by moving one step.
  `cardN.sof` is `lab1` with card N fixed and no warm-up; the warm-up step and the "three switches"
  step load the full `lab1.sof` (warm-up, then SW9..SW7 pick the card; the screen says to hold
  KEY0+KEY1 on the second). Rebuild all of `sof\` with `../board_lab1/build_kit.ps1` (~15 min).
* Needs `quartus_pgm` (Quartus Prime Lite or the stand-alone Programmer) and the USB-Blaster driver.
  It looks in `C:\altera_lite\25.1std` and `C:\intelFPGA_lite\{25,24,23}.1std`. Without it the
  steps still run, with no programming.
* Navigation: Enter = next, `r` = redo this step (board reprogrammed, questions asked again; the new
  answers are tagged `redo` and replace the ones above them), `b` = back, a number = jump to that step,
  `q` = quit. Answers are
  appended to `answers_<ID>.txt`, one block per run, headed by ID, name and time. At the end the file
  opens in Notepad and the screen says to upload it to the Moodle lab-1 assignment.
* One student per PC. Answers are typed in a small right-to-left window (the console can only type
  left to right); `LAB1_TEST=1` replaces it with stdin for scripted tests.
* Each answer is echoed back in the console in reading order.
* Tested 2026-10-14 on the course PC: all 13 steps, 4 programmings, 25 answers saved.

After changing a design, run `../board_lab1/build_kit.ps1` again.
