# Lab 1 — the board that raises the whole course's questions

**Decision (2026-09-29):** the board activity moves from lecture 1 into **lab 1**. Lecture 1
stays as the course-principles talk. In lab 1, students only **play** with a pre-flashed
board and write down what surprised them. Nobody explains anything. Each later lab opens
by taking that week's questions off the wall and answering them with that week's videos.

Supersedes the board part of `old material/lecture1_board_activities.md` and tasks 2–3 of
`old material/lab1_detailed_plan.md` (both archived 2026-10-14, with the old 4-mode lecture
board `old material/board_lecture1/`).

## The 11 riddles (decided 2026-10-08)

Week 1 presents all 11. Each later lesson **opens by answering one riddle** and **closes by
showing the next week's riddle again**. Week 1 closes with riddle 1; week 11 closes with
riddle 11, which the exam-rehearsal lesson (4.1.27) answers.

| # | Riddle (shown in week 1) | Board card | Answered in |
|---|---|---|---|
| 1 | 63 + 1 = −64. How can adding 1 make a number negative? | 1 (+1) | Week 2 (26.10) |
| 2 | Three switches turn one chip into different machines. How? | the mode switches | Week 3 (2.11) |
| 3 | The same chip was reprogrammed into a game. How did it become a different circuit? | teacher's board | Week 4 (9.11) |
| 4 | The light stays on with no finger on any button. Where is the "on" kept? | 4 (remembers) | Week 5 (16.11) |
| 5 | The turnstile knows you already paid. How does it remember what happened? | 5 (turnstile) | Week 6 (23.11) |
| 6 | Same button, two lights: one instant, one waits for the tick and can miss a press. Why? | 6 (instant / late) | Week 7 (30.11) |
| 7 | A faster clock gives *wrong* answers, not just faster ones. Why? | 7 (speed dial) | Week 8 (7.12) |
| 8 | The big addition fails at a lower speed than the small one. Why? | 7 (speed dial) | Week 9 (14.12) |
| 9 | ÷8 just slides the lights but ÷6 scrambles them, and divide fails first on the speed dial. Why is division so expensive? | 2 (moving lights) + 7 | Week 10 (21.12) |
| 10 | 10 × 0.1 shows 0.976 but 4 × 0.25 shows 1.000; `0.1 + 0.2 == 0.3` is `False`. Why? | 8 (× 0.1) | Week 11 (28.12) |
| 11 | Squeezed into a smaller box, 8 became −8. Ariane 5 blew up the same way. Why? | 3 (squeeze) | Week 12, exam rehearsal (4.1.27): needs week 2 (width, sign) and week 11 (floating point) |

The cards keep their play order below. The riddle numbers above follow the answer order.

## Rules the design follows

1. **One mode, one phenomenon, one short prompt.** No mode teaches two things.
2. **Students never need binary.** Every number they set or read is decimal. Every task is
   "try things and compare", never "set x to 63".
3. **The prompt asks what they did, expected and saw.** It never says what is surprising.
4. **No surprise the course never answers.** The board is programmed to flash memory
   (`.pof`), so power-cycling changes nothing. Slide switches are never used as event
   inputs, only as settings, so switch bounce never shows up. Events come from KEY0/KEY1,
   which are hardware-debounced.
5. **Choosing a mode needs no binary.** Each student gets a printed card per mode with a
   picture of `SW9 SW8 SW7` (up/down) and the prompt.

## The design: 8 modes, one pre-flashed `.pof`

`SW9 SW8 SW7` select the mode. The rest of the switches are inputs or settings. **All
student-facing text on the cards is Hebrew.**

| Card | `SW9 SW8 SW7` | Mode | Week answered |
|---|---|---|---|
| 1 | ↓ ↓ ↓ | +1 | 2 |
| 2 | ↓ ↓ ↑ | moving lights (÷8, ÷6, ×2) | 2 (and 10) |
| 3 | ↓ ↑ ↓ | squeeze into a small box | 2 |
| — | the mode switch itself | "how does one chip become different machines?" | 3 |
| — | teacher's board | a new design is loaded live | 4 |
| 4 | ↓ ↑ ↑ | the light that remembers | 5 |
| 5 | ↑ ↓ ↓ | turnstile | 6 |
| 6 | ↑ ↓ ↑ | instant light, late light | 7 |
| 7 | ↑ ↑ ↓ | speed dial ⚠ prototype first | 8, 9, 10 |
| 8 | ↑ ↑ ↑ | × 0.1 | 11 |

Cards are ordered by the week that answers them, so the question wall fills left to right
in course order. Built as three Quartus projects in `board_lab1/` (see its `README.md`):
`lab1/` (warm-up, cards 1–6 and 8; card 7 shows `SPEEd`), `game/` (riddle 3) and
`speeddial/` (card 7). All simulated in Icarus before the warm-up was added; `lab1`
compiles in Quartus 25.1 (2026-10-14), the Icarus testbenches are in `old material/icarus_sim/`.

---

### Warm-up — "Set the switches to ten." (week 2)

Brought back from `old material/lab1_detailed_plan.md` (2026-10-14). The richest minute of the
lab: the instruction sounds trivial and is ambiguous.

**Design.** The board powers up in the warm-up, before any card. `LEDR9..0` mirror the ten
switches, `HEX2..0` show `SW9..0` in **hex** (`000`–`3FF`), the other digits are dark.
Holding **KEY0 and KEY1 together** leaves the warm-up and the cards start. It doesn't come
back until power-off, and the keys do nothing else while it is on.

**Student does.** Hears one sentence: «כוונו את המתגים לעשר.» Expected outcomes, all of
which occur:
* flip `SW9`, "the tenth switch": display reads `200`
* flip all ten, since there are only ten: display reads `3FF`
* use the display as feedback and hunt for `10` on it: found at `0000010000`, which is
  the value **sixteen**. They believe they succeeded.

**Correct nobody.** Write on the whiteboard that three students got three different results
from one instruction. That puts the problem in the instruction, not the student, and keeps
the question open for a week. Naming a winner spends the hook.

**Question they raise.** What does "ten" mean on this board, and what are `F` and `3FF`?
**Answered by.** Week 2: *Number Systems* (hex), lab 2 ex1. It goes on the wall with
riddle 1, not as an 11th riddle.

Then: «החזיקו את שני הכפתורים יחד» and the cards start.

### Card 1 — +1 (week 2)

**Design.** `SW6..0` = x (signed, −64…63). Left display `HEX5..3` = x in decimal. Right
display `HEX2..0` = x + 1, wrapping. LEDs = the switch pattern. 

**Student does.** Hunts for the biggest number they can make. Finds 63, and sees the right
display say −64. On the way, finds that one switch (`SW6`) makes everything negative.

**Prompt.** «צרו את המספר הגדול ביותר שאתם מצליחים בצג השמאלי. מה מופיע בצג הימני?»

**Question they raise.** How can adding 1 make a number negative?
**Answered by.** Week 2: *Binary Addition*, *Signed Numbers*.
**Teacher fallback.** "What is the biggest number the left display can reach? Why that one?"

### Card 2 — moving lights (weeks 2 and 10)

**Design.** `SW6..0` = x (unsigned), shown on the left. The right display and the LEDs
show the result:
* nothing held: x ÷ 8, and the LED pattern is the switch pattern **slid 3 places right**
* `KEY0` held: x ÷ 6, and the LED pattern looks **scrambled**
* `KEY1` held: x × 2, and the LED pattern is the switch pattern **slid 1 place left**

⚠ Check on a real board that the LEDs sit right
above their switches.

**Student does.** Flips switches at random and compares the lights with the switches in
each of the three cases. Describes it in plain words ("it slid", "it's mixed up").

**Prompt.** «הזיזו מתגים. השוו את הנורות למתגים. עכשיו החזיקו KEY0, ואחר כך KEY1. מה
קורה לתבנית בכל מקרה?»

**Question they raise.** Why do ÷8 and ×2 only move the lights, and ÷6 doesn't?
**Answered by.** Week 2 (*Unsigned Binary Numbers*, place value) for the sliding. Week 10
(*Shifters, Multipliers & Dividers*) for why ÷6 needs real hardware. Card 7 comes back to
this.
**Teacher fallback.** "Is there any number other than 8 you could divide by and see the
lights slide?"

### Card 3 — squeeze into a small box (week 2)

**Design.** `SW6..0` = x (signed) on the left. The right display shows the same x after
being stored in 4 bits (−8…7). 

**Student does.** Starts at 0 and increases until the two displays stop agreeing. Finds
the break at 8, and that bigger numbers come out as strange small ones.

**Prompt.** «הגדילו את המספר עד ששני הצגים מפסיקים להסכים. איפה זה קרה? מה קורה אחרי?»

**Question they raise.** Why did the number break when it moved into the smaller box?
(This is Ariane 5.)
**Answered by.** Week 2: *Extension*, *Signed Numbers*.
**Teacher fallback.** "The right display is a smaller box. How small?"

### The mode switch itself (week 3)

Asked right after card 3, once they have seen three different machines:

**Prompt.** «עברתם על 3 כרטיסים. אותו לוח, אותו שבב. אילו מתגים שינו *מה הלוח עושה*,
ואילו רק את המספר?»

**Question they raise.** How do three switches turn one chip into different machines?
**Answered by.** Week 3: *Multiplexers*. In lab 3 they build a 2:1 mux themselves.

### Teacher's board, right after the mode-switch question (week 4)

**Design.** The teacher's own board, in front of the class, is programmed live (`.sof`, a
few seconds) with `board_lab1/game/`: a reaction-time game. KEY0 starts, all LEDs light after
a random 1–3 s, KEY1 stops the clock and the time in ms appears; pressing KEY1 too early
shows `Err`. Then `lab1.sof` is programmed back. Don't power-cycle during class: the board
would return to its flash image and raise "why did it forget?", which the course doesn't
answer.

**Question they raise.** The chip is the same. How did it become a different circuit?
**Answered by.** Week 4: *Logic Arrays*. An FPGA is built from lookup tables, and a lookup
table is a small memory (confirmed in the transcript). **Say aloud**: programming the board
fills those memories.

### Card 4 — the light that remembers (week 5)

**Design.** `KEY1` = "on", `KEY0` = "off".
* `LEDR0` = the remembered light: press KEY1 and it stays on after release, press KEY0
  and it goes off.
* `LEDR1` = just KEY1 itself, on only while pressed. It is there for contrast.
* `LEDR2` = the opposite of `LEDR0`.

**Recommended build:** a real cross-coupled NOR pair (an SR latch) in the fabric, kept with
`keep` attributes, so that **pressing both keys turns LEDR0 and LEDR2 off together**. That
is exactly the SR latch's invalid state. ⚠ Prototype it. Quartus warns about a
combinational loop. Fallback: a register, where pressing both does nothing strange.

**Student does.** Compares LEDR0 with LEDR1. Finds that LEDR0 stays on with no finger on
anything. Tries pressing both keys at once.

**Prompt.** «לחצו על KEY1 ושחררו. לחצו על KEY0 ושחררו. מה עושה כל נורה? נסו ללחוץ על
שניהם יחד.»

**Questions they raise.** Where is the "on" kept when nobody presses anything? Why are
LEDR0 and its opposite both off when I press both?
**Answered by.** Week 5: *Bistable Circuit* (feedback stores a bit), *SR Latch* (the
both-zero case).
**Teacher fallback.** "Nobody is touching the board. What is keeping LEDR0 on?"

### Card 5 — turnstile (week 6)

**Design.** `KEY1` = coin, `KEY0` = push. `HEX5..2` show `LOC` or `OPEn`. `HEX1..0` count
the people who passed. One more LED lights for each coin inserted, so a wasted coin is
visible.

Rules: locked + coin → open. Open + push → locked, and one more person counted. Locked +
push → stays locked. Open + coin → stays open, and the coin is wasted.

**Student does.** Works out the rules by trying, and writes them down in their own words.
Many students will draw circles and arrows without being told to.

**Prompt.** «זהו מחסום כניסה: KEY1 = מטבע, KEY0 = לדחוף. גלו את החוקים ורשמו אותם. מה
קורה אם מכניסים שני מטבעות ועוברים פעמיים?»

**Question they raise.** How does the board know what to do next? It has to know what
already happened.
**Answered by.** Week 6: *Intro to FSMs* (state register + next-state logic), *Moore FSM
Example 1*. In lab 6: "you drew a state machine in week 1."
**Teacher fallback.** "The same push does two different things. What decides which?"

### Card 6 — instant light, late light (week 7)

**Design.** A slow 1 Hz tick blinks `LEDR9`. A small machine watches `KEY0`, and its state
updates only on the tick. This is Harris's Mealy-vs-Moore example:
* `LEDR0` (Mealy): lights **the moment** KEY0 is pressed, if it wasn't pressed at the last
  tick, and goes off at the next tick even if you are still pressing.
* `LEDR1` (Moore): lights **at the next tick** after the press, and stays for one tick.

**Student does.** Presses short, long, right after a blink, right before one. Discovers
that LEDR0 is always immediate, LEDR1 is late by a varying amount, and a very short press
between ticks can make LEDR1 **miss it completely**.

**Prompt.** «נורה 9 מהבהבת. לחצו על KEY0 בזמנים שונים: לחיצה קצרה, ארוכה, מיד אחרי הבהוב,
רגע לפני. מתי נדלקת כל נורה ומתי נכבית?»

**Questions they raise.** Same button, why is one light late? Why did LEDR1 miss my press?
**Answered by.** Week 7: *Mealy FSM Example*. Its timing diagram shows exactly this: the
Mealy output rises at once, the Moore output waits for the clock edge (confirmed in the
transcript).
**Teacher fallback.** "What does LEDR9 have to do with when LEDR1 lights?"

### Card 7 — speed dial (weeks 8, 9, 10) ⚠ prototype on one board first

**Design.**
* `SW4..3` choose an operation: small add (8-bit), big add (64-bit), multiply (16 × 16,
  forced into logic with `multstyle = "logic"`), divide (16 ÷ 8).
* `SW2..0` choose the clock the operation runs at: 10, 25, 50, 100, 200, 300 MHz (one
  PLL plus the 50 MHz input). Every clock × operation pair runs all the time in its own
  tester, so nothing switches clocks; the switches only choose what is shown.
* Built in `board_lab1/speeddial/`. In simulation with pretend delays the ladder appears:
  divide goes wrong first, then multiply, then the 64-bit add; the 8-bit add never does.
* `HEX5..3` = clock in MHz. `HEX1..0` = percentage of wrong answers (99 means 99–100%).

The error detector changes the inputs every 16 cycles. It compares the result captured
**one** cycle after the change (the fast path under test) with the result captured 15
cycles after (settled), and counts mismatches.

**Student does.** For each operation, raises the clock until wrong answers appear, and
fills a table: *the fastest clock with 0% wrong*. Then compares their table with the
student next to them.

**Prompt.** «בחרו פעולה (מתגים 4-3) והעלו את מהירות השעון (מתגים 2-0). רשמו בטבלה, לכל
פעולה, את המהירות הגבוהה ביותר בלי תשובות שגויות. השוו לסטודנט שלידכם.»

| Operation | Fastest clock with 0% wrong |
|---|---|
| small add | |
| big add | |
| multiply | |
| divide | |

**Questions they raise.**
1. Why does a faster clock give **wrong** answers, not just the same answers sooner?
   (week 8, *Timing*: the setup-time constraint)
2. Why does the big add fail before the small one? (week 9, *Ripple-Carry Adders*: "the
   carry ripples through")
3. Why does multiply fail before add, and divide before multiply? (week 10, *Shifters,
   Multipliers & Dividers*)
4. Why is the neighbour's board a little different? (week 4, *Timing of Combinational
   Logic*: delay depends on temperature and voltage)

The table is the course's timing thread in one sheet. They refill it in weeks 8, 9 and 10.

**⚠ Risks. This card must work on a real board before the semester.**
* MAX 10 adders use a dedicated fast carry chain, so small add and big add may not
  separate at clocks the PLL can reach. Choose the widths after measuring.
* Real chips run well past Quartus's reported Fmax, and the margin varies by board and
  temperature. Pick the frequency steps from measurements, not from the report.
* **Fallback if it can't be made reliable:** show the Quartus Fmax figure for each
  operation on the screen. It raises questions 2 and 3, but not "faster gives wrong answers".

**Teacher fallback.** "These are identical copies of the same circuit, each run at a different clock. Why do the fast copies give wrong answers?"

### Card 8 — × 0.1 (week 11)

**Design.** `SW3..0` = x (0…15), shown on `HEX5..4`. `HEX3..0` shows the result as
`d.ddd` (decimal point after `HEX3`). By default the result is x × 0.1, where 0.1 is stored
with 8 fraction bits (25/256 = 0.0977, truncated). While `KEY0` is held, the result is
x × 0.25, stored exactly (64/256).

On the PC next to the board, two lines of Python.

**Student does.** Sets 10 and reads 0.976, not 1.000. Holds KEY0, sets 4, and reads
exactly 1.000. Then types both lines of Python and finds the same thing in their
computer.

**Prompt.** «קבעו 10 בצג השמאלי. בצג הימני: 10 כפול 0.1. מה ציפיתם? עכשיו החזיקו KEY0
(כפול 0.25) וקבעו 4.»
«במחשב הקלידו: `0.1 + 0.2 == 0.3` ואחר כך `0.5 + 0.25 == 0.75`»

**Question they raise.** Why does 0.1 go wrong and 0.25 not, on the board and in Python?
**Answered by.** Week 11: *Fixed Point Numbers*, *Floating-Point Numbers* (fixed precision,
rounding). **Say aloud** the missing sentence: 0.1 never ends in binary, like 1/3 in decimal;
½ and ¼ do end. Name this one as **the second long mystery** of the course.
**Teacher fallback.** "Find any x where the × 0.1 answer is exactly right."

---

## Run sheet (150 min, singles, one board each)

Each student runs `lab1_kit/LAB1.bat` (see its `README.md`): it walks the steps below in this
order, programs the board itself when the design changes, and saves the answers to
`answers_<ID>.txt` for Moodle. The kit needs Quartus Programmer on the student PCs **before**
the lab, so the toolchain shakeout below can't be the first time Quartus meets those PCs.

> **If there is only one board (whole-class demo):** use the program order in
> `board_lab1/README.md` → *One-board demo order*, with students calling the switch moves
> and writing predictions before each result.

| Min | Stage |
|---|---|
| 5 | Hand out boards and cards. One sentence: "Play. Don't explain. Write down what surprised you." |
| 5 | **Warm-up:** "set the switches to ten", then both keys to start the cards |
| 10 | Card 1, all together, to learn how to use a card |
| 20 | Cards 2–3 |
| 5 | The mode-switch question |
| 5 | The game: `LAB1.bat` reprograms each board into it (or the teacher's board, live) |
| 55 | Cards 4–8 at each student's own pace, about 11 min each |
| 20 | **Harvest.** Each student writes their questions on sticky notes. The teacher sorts them onto a **question wall** by the week that answers them, and tells the students the week, never the answer. |
| 25 | Toolchain shakeout: Quartus opens, the board is detected (from `old material/lab1_detailed_plan.md`, stage 3) |

Students who finish early do card 7 a second time on a different operation.

## The question wall is the course's spine

* Each lab from 2 to 11 opens by taking that week's notes off the wall, before the entry
  quiz. The student who wrote a question gets to answer it now.
* Keep the wall's photo on Moodle, since the lab room may be shared.

## Before the semester

* ✔ All cards, the game and the speed dial built and simulated (`board_lab1/`). Next:
  compile the three projects in Quartus (follow `board_lab1/README.md`).
* **Prototype card 7 on one board**: fill the table in the README. Adjust widths or clock
  steps if no clear ladder appears.
* Single-board demo order: `lab1` (flash) cards 1–3 → `game.sof` → `lab1.sof` cards 4, 5, 6, 8
  → `speeddial.sof` card 7.
* Prototype card 4's real NOR latch, or fall back to a register.
* Check that the LEDs sit directly above their switches (card 2).
* Print the 8 cards with switch pictures, in Hebrew.
* The Python timing fixes in `old material/lecture1_board_activities.md` still apply if lecture 1
  keeps the Python slides.
