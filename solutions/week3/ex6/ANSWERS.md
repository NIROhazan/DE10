# Week 3 exercise 6 answers (keep out of the student repo) - original expression Y = ((A + B'C)' + A'B)'

1s: 001 100 101 110 111      0s: 000 010 011

- DM  = (A + B'C)(A + B')          Involution on (A + B'C)'', T12 on (A'B)'
- SOP = A + B'C                    2 terms, 3 literals, unique
- POS = (A + B')(A + C)            2 sums, 4 literals, unique
- Q1: (BC)' = B' + C' (T12) and (B + C)' = B'C' (T12')
- Q2: the outer bar covers everything; from the inside the inner bar is undone again later (extra steps, lost bars)
- Q3: W = A, X = B', Z = C:  A + B'C = (A + B')(A + C)
- Q4 (correct answers): A=0 B=1 C=1 -> Y = 0: LEDG0 off, LEDR0-2 off, LEDR9 off
