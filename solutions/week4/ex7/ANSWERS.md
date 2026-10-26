# Week 4 exercise 7 answers - seven-segment BCD digit with don't-cares (keep out of the student repo)

One segment per student (a, d, f, g - tools/stories.txt), from the lecture's sevenseg table; rows 1010-1111 are X.
A = SW3 (MSB) ... D = SW0. The expression lines below are computed from the student's own segment by answers.bat.

- MSOP = @MSOP
- MPOS = @MPOS
- Per segment, with X:   a: A + C + BD + B'D' (4/6)          MPOS (A + B + C + D')(B' + C + D) (2/7)
                         d: B'D' + CD' + B'C + BC'D (4/9)    MPOS (B + C + D')(B' + C + D)(B' + C' + D') (3/9)
                         f: A + C'D' + BC' + BD' (4/7)       MPOS (A + B + D')(B + C')(C' + D') (3/7)
                         g: A + B'C + BC' + CD' (4/7), or BD' instead of CD'   MPOS (A + B + C)(B' + C' + D') (2/6)
- Without X (all 0):     a 4 terms 11 literals, d 4/13, f 4/12, g 4/12
- Q1: BCD codes only 0-9; 1010-1111 never arrive from a BCD source, so the segment may be anything there
- Q2: the X rows the student's own MSOP covers (compute from it); costs without X as above
- Q3: no - default: segments = 7'b000_0000 fixes rows 10-15 to 0 (blank). default: segments = 7'bxxx_xxxx (an x value) lets the tool choose; the default line itself is still needed (no default = latch)
- Q4: 1100 is an X row: HEX0 shows "-", LEDG0 off, LEDR9 off; LEDR0 / LEDR1 = what the student's own MSOP / MPOS give on 1100 (e.g. segment a, f, g: an MSOP with the term A gives 1)
