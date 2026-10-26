# Week 3 exercise 1 answers (keep out of the student repo)

- SOP = A'B' + AB' + AB
- POS = (A + B')   - one 0 row -> one maxterm; the canonical POS is already minimal
- MIN = A + B'
- Q1: three minterms, one per row with Y = 1
- Q2: a maxterm must be 0 on its row; OR is 0 only when every literal is 0, so B (=1) is complemented, A (=0) is not
- Q3: only one row has Y = 0 (vs three with Y = 1), so POS has one term and SOP three
- Q4 (correct answers): A=0 B=1 -> LEDR0, LEDR1, LEDR2 all off, LEDR9 off
