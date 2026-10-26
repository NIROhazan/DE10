# week 4 ex8 - critical path: hidden delays (ticks)

Circuit: n1 = A AND B, n2 = NOT C, n3 = n1 OR n2, Y = n3 AND D.  Paths: A/B: AND+OR+AND, C: NOT+OR+AND, D: AND.

| puzzle | AND | OR | NOT | tpd (critical) | tcd (D) | critical inputs |
|---|---|---|---|---|---|---|
| 0 | 9 | 3 | 6 | 21 | 9 | A B |
| 1 | 6 | 9 | 8 | 23 | 6 | C |
| 2 | 7 | 5 | 2 | 19 | 7 | A B |
| 3 | 3 | 4 | 9 | 16 | 3 | C |
| 4 | 4 | 9 | 2 | 17 | 4 | A B |
| 5 | 2 | 3 | 8 | 13 | 2 | C |
| 6 | 3 | 4 | 6 | 13 | 3 | C |
| 7 | 3 | 8 | 9 | 20 | 3 | C |

Measure AND: flip D with n3 = 1 (A=B=1 or C=0).  A/B path: B=1 (or A=1), C=1, D=1, flip A.  C path: A or B = 0, D=1, flip C.
The paper questions (Q3, Q4) are computed in tools/questions.ps1: `answers.bat w4-ex8 <ID>`.
