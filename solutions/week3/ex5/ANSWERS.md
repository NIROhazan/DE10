# Week 3 exercise 5 answers (keep out of the student repo) - original expression Y = AB + A(B + C)' + A'BC

1s: 011 100 110 111      0s: 000 001 010 101

- S1 = AB + AB'C' + A'BC          [T12' De Morgan]
- S2 = A(B + B'C') + A'BC         [T8 Distributivity]
- S3 = A(B + C') + A'BC           [Simplification]
- S4 = AB + AC' + A'BC            [T8 Distributivity]
- S5 = AC' + B(A + A'C)           [T8 Distributivity]
- S6 = AC' + B(A + C)             [Simplification]
- S7 = AC' + AB + BC              [T8 Distributivity]
- S8 = AC' + BC                   [T11 Consensus]
- MIN = AC' + BC                  2 terms, 4 literals, unique (BC only covers 011, AC' only 100)
- Q1: S1: T12' (B + C)' = B'C' - the complement of a sum is the product of the complements
- Q2: AB, by T11 consensus: AC' + BC + AB = AC' + BC; AB is 1 only where AC' or BC already is
- Q3: 4 rows (A, P = 00 01 10 11); both sides are 0 1 1 1, every combination is checked so the identity holds
- Q4 (correct answers): A=1 B=0 C=1 -> Y = 0: LEDG0 off, LEDR0-8 off, LEDR9 off
