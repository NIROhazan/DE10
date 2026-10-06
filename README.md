# DE10

Blank starter project. For now it targets the **Terasic DE1** (Cyclone II `EP2C20F484C7`).

| File | What it is |
|------|------------|
| `top.v` | Top level: SW -> LEDR, KEY -> LEDG[7:4], LEDG0 blinks at 1 Hz, HEX2..HEX0 show SW in hex |
| `top.qpf` / `top.qsf` | Quartus project, pins for CLOCK_50, KEY, SW, LEDG, LEDR, HEX0-3 |
| `top.sdc` | 50 MHz clock constraint |
| `DE1_pin_assignments.qsf` | Full DE1 pin list, copy lines from it when you use more of the board |

## Build and program

Needs Quartus II 13.0sp1 (newer Quartus dropped Cyclone II).

```
C:\altera\13.0sp1\quartus\bin64\quartus_sh --flow compile top
C:\altera\13.0sp1\quartus\bin64\quartus_pgm -m jtag -o "p;output_files/top.sof"
```

Fit (13.0sp1): 63 logic elements, 26 registers, 61 pins.
The "output pins stuck at VCC or GND" warning is expected (LEDG[3:1] and HEX3 are tied off).

`locked/` - a design with HEX3..HEX1 = "Err" and all LEDs off. `run.bat` in ex1-ex6 programs
`locked/locked.sof` whenever it stops (empty or wrong answers), so the board never keeps an older,
correct-looking design. Rebuild: `quartus_sh --flow compile locked` in `locked/`, copy `output_files/locked.sof` up.

## Exercises

The exercises are split by lecture and numbered from 1 in every week. Codes for Moodle carry the week:
`w2-ex3-Q1`, `w3-ex4`, `w4-ex9-Q2`, so ex3 of two weeks never share a code or a table.
`student.txt` (the student ID) and `locked/` stay here in the course folder; the scripts find them from
`weekN/exN` or `other/exN`.

### [`week2/`](week2/README.md) - lecture 2 (Harris ch. 1: number systems, signed numbers, gates, CMOS)

One `Qn_NAME.bat` per question; the runner (`tools/run.ps1`, the same in every week-2 exercise) programs the
prebuilt `board.sof`, asks in the console with the student's own numbers, and gives NEW numbers after a wrong
answer. The hidden boards (secret bytes, mystery gates, CMOS gates) are built from `C:\DE10_solutions\week2\gen.py`;
`tools/secrets.txt` holds only hashes of the right answers.

- [`ex1/`](week2/ex1/README.md) - binary, decimal and hex; a secret byte per puzzle on LEDG (KEY3).
- [`ex2/`](week2/ex2/README.md) - 4-bit adder with carry in (KEY0): overflow, 8-bit sum in two steps.
- [`ex3/`](week2/ex3/README.md) - sign/magnitude and two's complement, subtraction, signed overflow, ranges.
- [`ex4/`](week2/ex4/README.md) - sign-extension and zero-extension (SW9 picks which).
- [`ex5/`](week2/ex5/README.md) - mystery gates: 16 puzzles x 8 hidden gates, found from truth tables.
- [`ex6/`](week2/ex6/README.md) - CMOS gates: find the hidden gate, then its transistors (series / parallel, count).

### [`week3/`](week3/README.md) - lecture 3 (Harris ch. 2), in the order of the lecture

- [`ex0_eq/`](week3/ex0_eq/README.md) - warm-up: an equation on the board (AND / OR / NOT / XOR on switch values), 20 questions.
- [`ex1/`](week3/ex1/README.md) - SOP / POS with two variables: canonical SOP, canonical POS, minimal.
- [`ex2/`](week3/ex2/README.md) - SOP / POS with three variables (Y = 1 when A = B = C).
- [`ex3/`](week3/ex3/README.md) - minimal SOP vs minimal POS; the minimal SOP is not unique.
- [`ex4/`](week3/ex4/README.md) - from a story to an equation (like the cafeteria example).
- [`ex5/`](week3/ex5/README.md) - simplifying step by step with the theorems T1-T12.
- [`ex6/`](week3/ex6/README.md) - De Morgan, multiplying out (SOP) and factoring (POS).
- [`ex7/`](week3/ex7/README.md) - priority circuit, four outputs, some inputs active low.
- [`ex8/`](week3/ex8/README.md) - only NAND, only NOR.
- [`ex9/`](week3/ex9/README.md) - reading a multilevel NAND / NOR circuit (bubble pushing).
- [`ex10/`](week3/ex10/README.md) - a function on a 4:1 mux and on a decoder.

### [`class_exercise/`](class_exercise/README.md) - lecture 3 (Harris ch. 2, slides 1 and 3-106), needs the board

25 questions, one `Qnn_NAME.bat` each. The answer exists only in the board: every question is a hidden circuit in a prebuilt
`sof/Qnn.sof`, and the board itself judges the answer (the student sets it on the switches, holds KEY2, and the board shows a code
or `Err`). The PC holds neither answers nor codes. Login number from the ID on SW9..0 + KEY3. Source and key:
`C:\DE10_solutions\class_exercise\gen.py` (iverilog-checked); codes `ce-Qnn` in moodle.txt, counted by `verify.bat`.

### [`week4/`](week4/README.md) - lecture 4 (Harris ch. 2: Karnaugh maps, don't-cares, timing, glitches; ch. 4: case / casez)

- [`ex1/`](week4/ex1/README.md) - K-map, four variables, D on KEY3: canonical SOP/POS, minimal SOP, XOR form (a checkerboard - even parity). Was `other/ex4`.
- [`ex2/`](week4/ex2/README.md) - K-map, four variables: minimal SOP (four-corner group) vs minimal POS - POS wins with more 0s. Was `other/ex5`.
- [`ex3/`](week4/ex3/README.md) - K-map with don't-care rows (X): MSOP takes both X as 1, MPOS both as 0 - both right. Was `other/ex6`.
- [`ex4/`](week4/ex4/README.md) - K-map, three variables: a group that wraps around the edge, a prime implicant that is not needed.
- [`ex5/`](week4/ex5/README.md) - implicant / prime implicant / essential: a cyclic map with 6 prime implicants, none essential, two minimal SOPs.
- [`ex6/`](week4/ex6/README.md) - K-map, four variables: a group of 8 (one literal), groups of 4; POS has fewer terms, SOP fewer literals.
- [`ex7/`](week4/ex7/README.md) - one segment (a, d, f or g by ID) of the lecture's sevenseg module: BCD 0-9, rows 10-15 are X.
- [`ex8/`](week4/ex8/README.md) - timing: the lecture's critical-path circuit in slow motion (1 tick = 0.1 s) with hidden gate delays and a
  stopwatch on HEX3..0; measure gate delays, tpd and tcd; paper circuits with personal tpd / tcd in ps.
- [`ex9/`](week4/ex9/README.md) - glitches: 8 hidden 2-term SOPs in slow motion; find Y, the glitching switch flip, its timing, and the
  consensus term that removes it (SW6 adds it on the board).
- [`ex10/`](week4/ex10/README.md) - `casez` puzzles: value of y, how many inputs reach `default`, the line that never fires, one bit as a minimal SOP.

ex1-ex7 use the week-3 engine (personal truth table, `answer.txt` + Claude, `Qn` bats); ex8-ex10 use the week-2 engine (prebuilt
`board.sof`, wrong answer = new numbers) plus `Get-SopKey` in `tools/common.ps1`: a SOP answer is checked by its truth table and its
number of terms / literals, so every minimal SOP counts. Boards and keys: `C:\DE10_solutions\week4\gen_w4.py` (and `gen_kmap.py` for ex4-ex7).

### [`other/`](other/README.md) - not a lecture

- [`ex0/`](other/ex0/README.md) - week 1: LED wave. No logic - the student changes numbers in a `KNOBS` block
  (step divider, brightness), predicts on a `PREDICT:` line first (run.bat refuses without one, logs to
  `history.txt`), then checks on the board. Traps: 25-bit counter limit (wave freezes), 7-bit brightness overflow.
