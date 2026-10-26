# Week 4 exercise 1 (was other/ex4) answers (keep out of the student repo)

Y = 1 when an even number of A, B, C, D are 1 (even parity). 1s: 0000 0011 0101 0110 1001 1010 1100 1111.

- SOP  = A'B'C'D' + A'B'CD + A'BC'D + A'BCD' + AB'C'D + AB'CD' + ABC'D' + ABCD        (8 x 4 = 32 literals)
- POS  = (A+B+C+D')(A+B+C'+D)(A+B'+C+D)(A+B'+C'+D')(A'+B+C+D)(A'+B+C'+D')(A'+B'+C+D')(A'+B'+C'+D)
- MSOP = the same as SOP: checkerboard K-map, no two 1s adjacent (every neighbour differs in one bit
  -> flips the parity), so no merging is possible
- XOR  = (A^B^C^D)'   or any one input complemented: A'^B^C^D, A^B^C^D', ...   (4 literals)
- Q1: zero adjacent pairs -> minimal SOP = canonical SOP
- Q2: every Y=1 row has an even number of 1s (0, 2 or 4)
- Q3: 32 literals vs 4; XOR "counts" 1s mod 2, exactly what Y is, while SOP must list every row
- Q4 (correct answers): A=1 B=0 C=1 D=1 -> three 1s -> Y = 0: LEDG0 off, LEDR0-3 off, LEDR9 off
