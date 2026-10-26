# Week 3 exercise 8 answers (keep out of the student repo)

1s: 011 100 101 111      0s: 000 001 010 110

- SOP  = AB' + BC                    2 terms, 4 literals, unique
- POS  = (A + B)(B' + C)             2 sums, 4 literals, unique
- NAND = ((AB')'(BC)')'              4 NANDs (one is the NOT for B')
- NOR  = ((A + B)' + (B' + C)')'     4 NORs (one is the NOT for B')
- Q1: a NAND is an OR with bubbles on its inputs (De Morgan); the two bubbles on each internal wire cancel (Involution)
- Q2: 4 and 4 (2 first-level gates + 1 output gate + 1 inverter for B')
- Q3: NOT A = (AA)'; A AND B = ((AB)')' ; A OR B = (A'B')' = ((AA)'(BB)')'
- Q4 (correct answers): A=1 B=1 C=0 -> Y = 0: LEDG0 off, LEDR0-3 off, LEDR9 off
