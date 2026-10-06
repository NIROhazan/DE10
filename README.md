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
`w2-ex3-Q1`, `w3-ex4` (other/ keeps `ex4`, `ex5`, `ex6`), so ex3 of two weeks never share a code or a table.
`student.txt` (the student ID) and `locked/` stay here in the course folder; the scripts find them from
`week3/exN` or `other/exN`.

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

### [`other/`](other/README.md) - not lecture 3

- [`ex0/`](other/ex0/README.md) - week 1: LED wave. No logic - the student changes numbers in a `KNOBS` block
  (step divider, brightness), predicts on a `PREDICT:` line first (run.bat refuses without one, logs to
  `history.txt`), then checks on the board. Traps: 25-bit counter limit (wave freezes), 7-bit brightness overflow.
- [`ex4/`](other/ex4/README.md) - Karnaugh maps: four variables, D on KEY3 (pressed = 1): canonical SOP/POS,
  K-map minimal SOP, and an XOR form. The function is even parity, so the K-map is a checkerboard.
- [`ex5/`](other/ex5/README.md) - Karnaugh maps: four variables, minimal SOP (four-corner group) vs minimal POS;
  POS wins with more 0s than 1s, so the 1s/0s count only predicts the canonical forms.
- [`ex6/`](other/ex6/README.md) - Karnaugh maps with don't-care rows (X): the minimal SOP takes both X as 1,
  the minimal POS takes both as 0, so the two minimal answers differ on the X rows and are both right.
