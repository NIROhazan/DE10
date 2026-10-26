# Exercise 0 answers (keep out of the student repo)

All numbers checked: iverilog (duty cycles, freeze over 70M cycles) and Quartus 13.0sp1 (fit, warnings, errors).

## Part 1 - as shipped
- 1.2  15,000,000 / 50,000,000 = 0.3 s per step -> 10 steps = 3.0 s
- 1.3  stopwatch error is human reaction time (~0.2 s at start and stop); timing 10 steps, not 1, divides it by 10

## Part 2 - by ID digit d:  T = 100 + 60 d ms,  MOVE_DIV = 50,000 x T(ms)

| d | T | MOVE_DIV | hex | bits | 10 steps |
|---|---|---|---|---|---|
| 0 | 100 ms | 5,000,000 | 0x4C4B40 | 23 | 1.0 s |
| 1 | 160 ms | 8,000,000 | 0x7A1200 | 23 | 1.6 s |
| 2 | 220 ms | 11,000,000 | 0xA7D8C0 | 24 | 2.2 s |
| 3 | 280 ms | 14,000,000 | 0xD59F80 | 24 | 2.8 s |
| 4 | 340 ms | 17,000,000 | 0x1036640 | 25 | 3.4 s |
| 5 | 400 ms | 20,000,000 | 0x1312D00 | 25 | 4.0 s |
| 6 | 460 ms | 23,000,000 | 0x15EF3C0 | 25 | 4.6 s |
| 7 | 520 ms | 26,000,000 | 0x18CBA80 | 25 | 5.2 s |
| 8 | 580 ms | 29,000,000 | 0x1BA8140 | 25 | 5.8 s |
| 9 | 640 ms | 32,000,000 | 0x1E84800 | 25 | 6.4 s |

Common mistake: MOVE_DIV = T / 20 ns with T in ms (off by 10^6), or 50 x T.

## Part 3 - bits
- 3.1  15,000,000 = 0xE4E1C0 = 1110 0100 1110 0001 1100 0000
- 3.2  24 bits (2^23 = 8,388,608 <= 15M < 2^24 = 16,777,216)
- 3.4  2^25 - 1 = 33,554,431
- 3.5  the counter counts 0 .. MOVE_DIV-1, so MOVE_DIV <= 2^25 = 33,554,432 -> 0.671 s
- 3.6  50,000,000 - 1 never fits in 25 bits: the compare is never true, the counter wraps forever,
       the wave FREEZES with the peak on LEDR9 (where it starts). Static picture:
       LEDR9 99 %, LEDR8 + LEDR0 60 %, LEDR7 + LEDR1 30 %, LEDR6 + LEDR2 10 %, LEDR5-3 off.
       The typical chatbot answer "one step per second" is wrong.
- 3.7  238 -> 52 LEs, 54 -> 27 registers: Quartus proved the step never happens and deleted that hardware
       (only the PWM part is left)
- 3.8  LEDR3, LEDR4, LEDR5 stuck at GND: ring distance 4, 5, 4 from LEDR9 -> brightness 0 forever

## Part 4 - brightness
- 4.1  60 of 100 counts (counts 0..59) = 60 %
- 4.2  count runs 0..99, on while count < value: 99 -> on for 99 of 100; 100 (or 101..127) -> always on (100 %)
- 4.3  127 (111 1111)
- 4.4  130 = 1000 0010 -> 7 bits keep 000 0010 = 2
- 4.5  B1 = 130 -> 2 %: the two LEDs next to the peak are almost DARK, darker than the 30 % LEDs beyond them
       (checked: LEDR8 / LEDR0 at 2.0 %). Expected answer before the run: "full brightness".
- 4.6  Warning (10230): ... truncated value with size 32 to match size of target (7) at led_wave.v(19)
       - line 19 is `parameter [6:0] B1`: the 32-bit number was cut to 7 bits. No warning with legal values.
- 4.7  B2 = B3 = 0: three LEDs lit at any time (peak + two neighbours)

## Part 5 - too fast
- 5.1  10 cycles x 20 ns = 200 ns per step (whole loop 2 us)
- 5.2  all ten LEDs glow evenly, dim, no motion
- 5.3  (99 + 2x60 + 2x30 + 2x10 + 2x0 + 0) / 10 = 29.9 %  (simulation: 29.9 % on every LED)
- 5.4  the eye averages anything faster than ~50 Hz; the loop repeats 500,000 times a second
- Do NOT use 5000: loop period 50,000 cycles = the PWM period (1 ms), so LEDs lock to the PWM and differ (20-50 %).

## Part 6 - tool and board
- 6.1  238 logic elements, 54 registers (Fmax 175.3 MHz Slow model, not asked)
- 6.2  the wave is gone: the FPGA configuration is in SRAM and is lost at power-off; the DE1 boots its
       factory design from the EPCS flash instead
- 6.3  Error (10170): Verilog HDL syntax error at ex0_top.v(19) near text "localparam"; expecting ";"
       It points at line 19, not 18: Quartus only notices the missing ; when the next word arrives.

## Live check answers
- twice as fast: half their MOVE_DIV (or "x2" means half the time per step - ask them which)
- 40,000,000 -> freezes (> 33,554,432); 30,000,000 -> 0.6 s per step, runs
- LE count: output_files\ex0.fit.summary or the run.bat printout
- history.txt: every run should have a PREDICT line written before it; a run of 3.6 whose prediction
  says "freezes" is the sign they did 3.4 / 3.5 first
