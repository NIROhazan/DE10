# Week 4 exercise 2 (was other/ex5) answers (keep out of the student repo)

1s: 0000 0001 0010 0011 1000 1010 1110      0s: 0100 0101 0110 0111 1001 1011 1100 1101 1111

- SOP  = A'B'C'D' + A'B'C'D + A'B'CD' + A'B'CD + AB'C'D' + AB'CD' + ABCD'        (7 minterms)
- POS  = (A+B'+C+D)(A+B'+C+D')(A+B'+C'+D)(A+B'+C'+D')(A'+B+C+D')(A'+B+C'+D')(A'+B'+C+D)(A'+B'+C+D')(A'+B'+C'+D')   (9 maxterms)
         (A'+B'+C+D)(A'+B'+C+D')(A'+B'+C'+D')                                    (9 maxterms)
- MSOP = A'B' + B'D' + ACD'          3 terms, 7 literals, unique, all essential
         A'B' = row 00 (0000-0011); B'D' = the four corners 0000 0010 1000 1010; ACD' = 1010 1110
- MPOS = (A+B')(A'+D')(B'+C)          3 terms, 6 literals, unique, all essential
         (A+B') = 0100-0111; (A'+D') = 1001 1011 1101 1111; (B'+C) = 0100 0101 1100 1101
- Common non-minimal MSOP: A'B' + AB'D' + ACD' (pair instead of the corner quad, 8 literals)
- Q1: the four corners 0000, 0010, 1000, 1010: the map wraps left-right and top-bottom
- Q2: A'B' only covers 0001 (or 0011); B'D' only 1000; ACD' only 1110 -> all three essential
- Q3: MSOP 7 literals, MPOS 6 -> POS wins; 1s/0s count fixes the canonical length, the minimal
      length depends on how big the groups can be (the 0s form three quads, the 1s need a pair)
- Q4 (correct answers): A=1 B=1 C=1 D=0 -> 1110, Y = 1: LEDG0 on, LEDR0-3 on, LEDR9 off
