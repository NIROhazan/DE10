# Lab 1 — detailed plan

> **Superseded in part by `lecture1_board_activities.md`.** Week 1 now keeps the full
> lecture, including course principles and formal requirements, and the board activity
> runs **inside** the lecture at the challenge slides. The overflow and sign phenomena
> (tasks 2–3 below) move there. What remains here is optional: the hex and active-low
> tasks, the harvest, and the toolchain shakeout.

**"The display that lies."** 150 min.
Lesson content is ~75 min; the remaining slack absorbs lab 2's toolchain risk.

Dependency for the **lesson**: boards only. The toolchain shakeout in stage 3 needs
Quartus, but **no lesson rides on it** — that is the whole point of doing it here.

| Min | Stage |
|---|---|
| 5 | Unbox and power on |
| 60 | Observe and record |
| 30 | Toolchain shakeout (risk absorption, not a lesson) |
| 5 | Close — hook question, videos out |

Design rules behind this lab live in `../../lab_plan_weeks_1_3.md`.
The governing one: every phenomenon here is answered **one week later**.

---

## Before they arrive

On each desk: a DE10-Lite in its antistatic bag, a USB cable, a printed observation
sheet (Hebrew). Boards are already programmed to on-chip flash — USB supplies power
only. **No PC work today. Nobody opens Quartus.**

### Board behaviour (fixed all session)

| Output | Behaviour |
|---|---|
| `LEDR9..0` | mirror the ten switches, one LED each — **the honest output** |
| `HEX2..HEX0` | the switch value in **hex**, `000`–`3FF` |
| `HEX5` | shows `-` when `SW9` is on |
| `HEX0` | **segments inverted** — displays the photographic negative of the correct digit, while `HEX1`/`HEX2` render normally |

Four phenomena, all answered in week 2: hex notation, finite width, two's complement,
active-low drive.

---

## Stage 1 — Unbox and power on (10 min)

They open the bag and plug in. The display lights immediately.

Say three things explicitly:

1. The board is theirs until the end of the semester.
2. Nothing needs to be installed today.
3. **You will not answer "why" questions.** Their job is to collect observations.

Point 3 must be said at the start, or the next hour feels like withholding rather than
design.

## Stage 2 — Observe and record (60 min, pairs)

### Task 1 — "Set the switches to ten."

The richest minute of the lab. The instruction sounds trivial and is ambiguous.

Expected outcomes, all of which occur:

* flip `SW9` — "the tenth switch"
* flip ten switches — there are only ten, so everything goes on, display reads `3FF`
* use the display as feedback and **hunt for `10` on it** — found at switch pattern
  `0000010000`, which is the value **sixteen**. They believe they succeeded.

**Correct nobody.** Let all three stand, and write on the whiteboard that three pairs
got three different results from one instruction. That relocates the problem from the
student to the instruction, makes the missing convention visible without naming it,
and keeps the question open for a week. Naming a winner spends the hook.

### Task 2 — "Turn on every switch. What is the largest value?"

All LEDs lit, display reads `3FF`. They expected 1023, or 9999, or "ten ones".
Raises: what is `F`, and why does it stop there.

### Task 3 — "Flip `SW9` on its own."

One switch and the number goes negative. Nothing else changed.

Strongest hook of the four, because it is so visibly disproportionate — one switch of
ten should not do that. Breaks the assumption that the switches are "just a number".

### Task 4 — "Find the digit whose segments look wrong."

`HEX0` renders inverted beside two digits that render correctly. Same chip, same
design, adjacent digits. They can see it and have no language for it beyond "inverted"
— which is exactly right, and gets explained next week.

### Tasks 5–6 — the harvest

5. **Write two questions you cannot answer.**
6. **Pick one behaviour and describe it precisely enough that someone who never saw
   the board could reproduce it.**

Task 6 is the artifact. Most descriptions will be unusable — "the number was weird",
"one digit looked broken". That is the point. **Keep them; hand them back in week 8.**

## Stage 3 — Toolchain shakeout (30 min)

**Not a lesson. Risk absorption for lab 2.**

Lab 2 is the most fragile session of the semester: 17 machines meet Quartus,
USB-Blaster drivers and the programmer at once, *with a lesson riding on it*. Here the
same work carries no lesson, so every failure found today is one that does not
detonate next week.

* Install Quartus Prime Lite (MAX 10 device support) on each student's machine
* Plug in a board, install the USB-Blaster driver, confirm the programmer sees it
* Open the template project and compile it — **do not** explain anything in it

Nothing is assessed. A machine that refuses today is a problem you own for a week
instead of discovering it live in lab 2.

## Stage 4 — Close (5 min)

Hand out the week-2 video list. One question as the hook — no Kahoot this week.

**Why no Kahoot:** a Kahoot *summarises the material*. Week 1 has no material; that is
the design. A quiz about course logistics is filler wearing the costume of a ritual.
The hook question costs two minutes and does the whole job.

**Method briefing is not done in lab.** Flipped format, entry quizzes, project, grading
— all of it is information transfer, so it goes on Moodle plus a 2-minute slide.
Spending 20 minutes of lab time transferring information contradicts the premise of
the course in the first session taught.

---

## What you do during stage 2

Circulate constantly. Answer **no** conceptual question. Standard reply:
*"Write that down as question one."* Do help with anything physical — a cable that
won't seat, a board that won't power.

Watch for a pair that is stuck and **frustrated** rather than stuck and curious.
Redirect to a task that always succeeds: *"Leave that, do task 4, come back."*

### Prior knowledge and phones

Some students already know hex and two's complement. Give them a different job rather
than asking them to sit on it: find a switch pattern where LEDs and display appear to
contradict each other; predict the neighbours of `3FF` before trying them; or hold
them to task 6 at professional standard. **Knowing a concept and describing a
behaviour precisely are different skills**, and the second stays hard.

**Allow phones and LLMs, explicitly:** *"If you want to photograph the board and ask
an AI what's going on, do it — but write down its answer, and next week we check
whether it was right."*

* Nothing is graded, so there is nothing to cheat on.
* What they get back is **labels, not capability** — they still cannot convert a
  number or predict what `SW9` does to a value that is not 512. The week-2 entry quiz
  tests use, not recognition, so this self-corrects.
* AI answers about this board are often vague or partly wrong (the inverted digit reads
  equally well as a faulty display), which is a cheap early lesson in verifying a
  confident answer.

The only real risk is a student who gets a label, feels finished, and skips the videos.
The entry quiz catches that.

## Collected at the end

17 observation sheets.
* The **two questions per student** open week 2 — their own words, on screen.
* The **task-6 descriptions** go in a folder until week 8.

## Fallback if boards have not arrived

`challenge.py` alone, observation sheet becomes a Python worksheet. Much weaker —
the physical fault is most of the force. **Order the boards now.**
