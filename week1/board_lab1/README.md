# Lab 1 board demos: three Quartus projects (DE10-Lite)

| Folder | What it is | Riddles |
|---|---|---|
| `lab1/` | The 8-card board. Powers up in the **warm-up** ("set the switches to ten": LEDs = switches, `HEX2..0` = hex); hold KEY0+KEY1 together to start the cards. `SW9 SW8 SW7` pick the card. Card 7 only shows `SPEEd`: load the `speeddial` project for it. | warm-up, 1, 2, 4, 5, 6, 9 (lights part), 10, 11 |
| `game/` | Reaction-time game: a completely different circuit on the same chip | 3 |
| `speeddial/` | Clock speed vs wrong answers, for 4 operations | 7, 8, 9 |

Status: all three **simulated in Icarus Verilog** (all checks passed before the warm-up was
added). `lab1` **compiles in Quartus 25.1** (2026-10-14, 0 errors, `.sof` and `.pof` made);
the new warm-up checks in `tb_lab1.sv` (now in `../old material/icarus_sim/`) have not been
run yet (no Icarus, and Questa has no license on that machine). `game` and `speeddial` not yet compiled.

## Before the first compile

* **Copy `board_lab1/` to a plain-English path**, e.g. `C:\fpga\board_lab1\`. Quartus is
  unreliable with Hebrew letters or spaces in a path (this folder sits under
  `מאסטר הזדמנויות`).
* Quartus Prime **Lite** with **MAX 10** device support, plus the USB-Blaster driver
  (`<quartus>\drivers\usb-blaster`). The classroom/projector PC needs at least the Quartus
  **Programmer** and the driver.

## Compile and program (same for each project)

1. Quartus → *File → Open Project* → the `.qpf` in the folder.
2. *Processing → Start Compilation*.
3. *Tools → Programmer* → *Hardware Setup* → USB-Blaster.
   * **`.sof` (fast, a few seconds, forgotten at power-off):** add `output_files/<name>.sof`, tick
     *Program/Configure*, *Start*. Use this for every live switch during the demo.
   * **`.pof` (slower, stays in the board's flash):** add `output_files/<name>.pof`, tick
     *Program/Configure*, *Start*. Do this **once, before class, for `lab1`** so the board
     starts as the lab-1 board when it is plugged in.
   * After the first compile, **check that `output_files/` contains a `.pof`**. If it doesn't:
     *File → Convert Programming Files* → output type *Programmer Object File*, *Internal
     Configuration*, add the `.sof`, *Generate*.

## Expected warnings (not problems)

| Project | Warning | Why |
|---|---|---|
| `lab1` | combinational loop / latch on `q`, `qb` | Card 4 is a real SR latch built from two NOR gates, on purpose |
| `lab1`, `game` | input pins with no fanout (`SW` in `game`) | Unused switches |
| `speeddial` | **Timing requirements not met** at 100, 200, 300 MHz | On purpose: the one-cycle path is the thing being tested |

Paste any *errors* or *critical warnings* other than these back to Claude to fix.

## If the speed dial's PLL is rejected

`speeddial/speed_pll.v` follows a Quartus-generated MAX 10 PLL. If Quartus still rejects it:
*IP Catalog → ALTPLL* → name `speed_pll`, input 50 MHz, outputs c0–c4 = 10, 25, 100, 200,
300 MHz, enable the `locked` output. Then make its ports match `speed_pll.v`
(`inclk0`, `c[4:0]`, `locked`) and replace the file. If one PLL cannot make all five
frequencies, the wizard will say so; use two PLLs (the 10M50 has four).

## Prototype the speed dial on one board before class

Fill this table from the board (`SW4..3` operation, `SW2..0` clock):

| Operation | 10 | 25 | 50 | 100 | 200 | 300 MHz |
|---|---|---|---|---|---|---|
| 8-bit add | | | | | | |
| 64-bit add | | | | | | |
| multiply | | | | | | |
| divide | | | | | | |

What you want is a ladder: divide goes wrong first, then multiply, then the 64-bit add,
and the 8-bit add stays at 0%. Real chips are faster than Quartus's report, so the real
ladder may sit higher. If no clear ladder appears, the fallback is to show the
*Timing Analyzer → Fmax Summary* on the projector. It still raises riddles 8 and 9, but
not "faster gives wrong answers".

## One-board demo order (week 1)

1. `lab1` is already in flash (`.pof`). Warm-up ("set the switches to ten"), both keys, then
   cards 1, 2, 3, then the mode-switch question (riddle 2).
2. Program **`game.sof`** live. The class watches the same chip become a game (riddle 3).
3. Program **`lab1.sof`** back. Cards 4, 5, 6 and 8.
4. Program **`speeddial.sof`**. Card 7 last (riddles 7–9).

Each reprogramming step reinforces riddle 3. **Don't power-cycle the board during class.** It
would go back to the flash image and raise "why did it forget?", a question the course
doesn't answer.

## Simulation

The Icarus testbenches (`tb_*.sv`, and `speed_pll_sim.sv` standing in for the PLL) moved to
`../old material/icarus_sim/` on 2026-10-14. They are not part of the Quartus projects.
