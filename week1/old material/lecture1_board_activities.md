# Lecture 1 — which challenges run on the board

> **Superseded (2026-09-29):** the board activity moved from lecture 1 to lab 1. See `lab1_board_challenges.md`. This file is kept for the slide analysis and the Python timing fixes.


Source: `L1_2025_.pptx`, challenge slides 6–15. The rest of the lecture (why, course
content, how we learn, formal requirements) stays as it is. The board activity runs
**inside** the lecture, at the challenge slides. Boards are pre-flashed; nothing depends
on Quartus.

## The constraint that sorts the slides

"Which is faster?" **cannot be seen on an FPGA.** Every one of these operations finishes
inside one clock cycle, so a stopwatch shows nothing. On hardware, "faster" becomes
**how much hardware** and **how long the signal path is**, and both of those show up only
in a Quartus report.

The board *can* show two things directly: **wiring**, where multiplying or dividing by a
power of two is just moving the bits, and **width**, where a number runs out of room.

## Slide by slide

| Slide | Challenge | On the board? | What students do | Question it raises | Answered |
|---|---|---|---|---|---|
| 6 | Israeli chip beats Nvidia | — | nothing (context) | — | — |
| 7–8 | `×5` vs `//5`, 4× gap | **No** | stays in Python | why is division slow? | wk 10 → **the one long-arc mystery**, name it as such |
| 9 | `/2` vs `/3` | **Yes** | mode `10`: watch the lights move | why is ÷2 "free"? | wk 2 |
| 10 | `/8` vs `/6` | **Yes, strongest** | mode `10`: ÷8 shifts the pattern 3 places, ÷6 doesn't | why does ÷8 only move the lights? | wk 2 (why ÷6 costs more: wk 10) |
| 11–12 | `×2` vs `x+x` (Python: nearly equal) | **Yes: flips the answer** | mode `01`: ×2 is the pattern moving one place left | in Python they tied; in hardware one of them costs no gates. why? | wk 2 / wk 3 |
| 13–14 | `x>0`, `y=x+1`, `y<0`? | **Yes, direct** | mode `00`: make the biggest number they can (they find 63), read x+1 = −64 | how can adding 1 make it negative? | wk 2 |
| 15 | Ariane 5 | **The core idea, yes** | mode `11`: same value squeezed into fewer bits | why did the number break when it moved? | wk 2 (Extension video); float part wk 11 |
| new | `0.1 + 0.2 == 0.3` → `False`, but `0.5 + 0.25 == 0.75` → `True` | **No** | Python, two lines, no timing | why does one work and the other not? | wk 11 (Fixed Point, Floating-Point Numbers). **The second long-arc mystery**, name it as such. Why: 0.1 repeats forever in binary (like 1/3 in decimal) and is rounded; ½ and ¼ are exact. |

Five of seven challenges can be done on the board, and four of those are answered next
week.

## The pre-flashed design (one `.pof`, four modes)

`SW9:SW8` select the mode, `SW6..0` are the input **x** (7 bits, so values fit three
digits including a minus sign).

### Rule: students never need binary

They know nothing about binary in week 1, so the design must never ask them to *set* a
number:

1. **The left display always shows x in decimal.** That is their feedback. They flip
   switches freely and read what number they made. They never convert anything.
2. **Every task is a search or a pattern comparison**, never "set x to 63":
   "make the biggest number you can", "increase until the two displays disagree",
   "compare the lights to the switches".

| Mode `SW9 SW8` | Left `HEX5..3` | Right `HEX2..0` | LEDs | Mirrors |
|---|---|---|---|---|
| `0 0` | x (signed, −64…63) | x + 1 | switch pattern of x | slides 13–14 |
| `0 1` | x (unsigned, 0…127) | 2·x (wraps past 127) | pattern of **2·x** | slides 11–12 |
| `1 0` | x (unsigned) | x ÷ 8, or x ÷ 6 while `KEY0` is held | pattern of **the right display's value** | slides 9–10 |
| `1 1` | x (signed) | the same x stored in **4 bits** (−8…7) | switch pattern of x | slide 15 |

In mode `01`, the ×2-vs-x+x comparison lives on the slide: both give the same number, and
the board shows that ×2 is just the pattern moving one place left.

**Why the LEDs show the result:** the red LEDs sit in a row right above the switches, one
per switch. In mode `01` the light pattern appears **one place left** of the switch
pattern, and in mode `10` **three places right**. They see with their own eyes that ×2 and
÷8 are just wires moving. ⚠ Check the LED-over-switch alignment on a physical board
before relying on it.

Mode `00` is the int32 slide in a smaller box: 63 + 1 = −64 is exactly 2147483647 + 1 =
−2147483648. **Say so out loud**, so they link the Python result to the board. While
hunting for the biggest number, they will also find that one switch (`SW6`) makes
everything negative. That is a free extra question.

**How ÷8 vs ÷6 works with no binary.** The display shows ordinary arithmetic they can
check in their heads (40 → 5, 40 → 6), so nothing surprises them there. The surprise is in
the **patterns**. For ÷8 the lights are the switch pattern slid three places right. For
÷6 they look scrambled. They can describe that in plain words ("it slid over", "it's
mixed up") without knowing what a bit is. The question left open is why ÷8 only moves
the lights, and week 2's place-value material answers it.

## Where it sits in the lecture

At each challenge slide: show the Python result first (that is the question), then 2–4
minutes on the board (that is the evidence), then **move on without explaining.** About
25 minutes on top of the existing lecture.

Student prompts (Hebrew, for the slides):

| Mode | Prompt |
|---|---|
| `00` | "צרו את המספר הגדול ביותר שאתם מצליחים. מה מופיע מימין?" |
| `01` | "השוו את האורות למתגים. מה קרה לתבנית?" |
| `10` | "הזיזו מתגים כרצונכם. השוו את האורות למתגים ב-÷8, ואז החזיקו KEY0 (÷6). מה ההבדל?" |
| `11` | "הגדילו את המספר עד ששני הצגים מפסיקים להסכים. איפה זה קרה?" |

Close with the harvest: **two questions you cannot answer**, collected as before.

## What happens to the "display that lies" lab

The lecture board modes now carry the overflow and sign phenomena, which were tasks 2–3
of `lab1_detailed_plan.md`. What the lecture does not cover is **hex** and **active-low**.
Either keep a short 10-minute version of those two tasks after the lecture, or drop them.
Active-low is ambushed in lab 2 regardless.

---

## ⚠ Fix before the semester: the Python timings

A student with an LLM can catch all three of these.

1. ✔ **Decided 2026-10-08: keep slide 10 as is** (instructor: in hardware ÷8 *is* a shift by 3, which is the point of the slide). Original note: **Slide 10 (`//8` vs `//6`).** In `challenge.py` the "//8" case actually times
   `x >> 3`, a shift. `challnge_answer.py` shows that a true `x // 2**k` is as slow as
   dividing by a prime. If the slide's 1.382 s / 5.557 s came from `challenge.py`, the
   slide compares a **shift** against a **division**, not ÷8 against ÷6. Either relabel it
   "`>>3` vs `//6`" or re-time a true `//8`. Confirm which script produced the slide's
   numbers.
2. **`challenge_.py` timings measure nothing.** `timeit("1000 // 2")` and the lines like
   it use constant expressions. CPython folds those at compile time, so every variant
   times the same no-op.
3. **All timings use `2**2000` bignums.** They measure CPython's big-number algorithms,
   not machine arithmetic. The direction is broadly real (dividers are slower on real
   CPUs too, and compilers turn ÷8 into a shift), but the ratios are not hardware ratios.

Fixing 1 is cheap, and it makes a better story: the board shows *why* the shift is free.

## Also in the kept slides

* **Slides 24–27** still list "writing SystemVerilog code and simulation tests" as a course
  goal. That contradicts the decision to treat HDL as notation rather than as a subject.
  Reword them.
* **Slides 32, 33 and 36** still carry 2025 details: the Moodle `…/2025/` URL and the final
  quiz date `19/1/25`.
