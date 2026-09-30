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

## Exercises

- [`ex1/`](ex1/README.md) - SOP / POS: the student writes expressions in `answer.txt`, `run.bat` has
  Claude turn them into Verilog (mistakes kept) plus tutoring feedback, then programs the board.
- [`ex2/`](ex2/README.md) - SOP / POS with three variables (Y = 1 when A = B = C): canonical SOP,
  canonical POS, minimal POS. Same run.bat flow; SW2 = C shown on HEX1.
- [`ex3/`](ex3/README.md) - minimal SOP vs minimal POS (five 1s, three 0s): four answers on LEDR0-3;
  the minimal SOP is not unique. The board checks correctness, the feedback checks minimality.
- [`ex4/`](ex4/README.md) - four variables, D on KEY3 (pressed = 1): canonical SOP/POS, K-map minimal SOP,
  and an XOR form. The function is even parity, so the K-map is a checkerboard and nothing merges.
