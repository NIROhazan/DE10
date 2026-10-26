# Week 3 exercise 3 answers (keep out of the student repo)

1s: 000 010 100 101 111    0s: 001 011 110

- SOP  = A'B'C' + A'BC' + AB'C' + AB'C + ABC            (5 minterms)
- POS  = (A+B+C')(A+B'+C')(A'+B'+C)                     (3 maxterms)
- MSOP = AC + A'C' + B'C'   or   AC + A'C' + AB'        (3 terms, 6 literals - two minimal covers)
  AC (101,111) and A'C' (000,010) are essential; row 100 is covered by either B'C' or AB'.
- MPOS = (A+C')(A'+B'+C)                                (2 terms, 5 literals)
  (A+C') covers 001,011; row 110 has no 0-neighbour -> its full maxterm stays.
- Q1: the other of the two covers above; both cover every 1, both 3 x 2 literals
- Q2: MSOP 6 literals, MPOS 5; only three 0s (and 001/011 pair up) vs five 1s
- Q3: with the B'C' cover, yes: A'C' and B'C' both cover 000; overlap is fine because 1 + 1 = 1
- Q4 (correct answers): A=1 B=1 C=0 -> Y = 0, LEDR0-3 off, LEDR9 off
