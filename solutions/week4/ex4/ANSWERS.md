# Week 4 exercise 4 answers - a K-map with three variables (keep out of the student repo)

Original table: 1s 000 010 011 111, 0s 001 100 101 110. Each student's table is renamed (answers.bat w4-ex4 <ID>).

- MSOP = A'C' + BC        2 terms, 4 literals, unique. A'C' = 000 + 010 (wraps around the left/right edge), BC = 011 + 111
- MPOS = (B + C')(A' + C)   2 sums, 4 literals, unique. (B + C') kills 001 101, (A' + C) kills 100 110
- Prime implicants of the 1s: A'C', BC, A'B (010 011). A'B is NOT needed: 010 is in A'C', 011 in BC (it is the consensus term).
- Q1: Gray order - neighbouring columns differ in exactly one bit, so a circle of neighbours drops one variable; 10 and 00 differ only in the first bit, so the first and last columns are neighbours across the edge (the map is a cylinder)
- Q2: A'B (rows 010 011): both its 1s are already covered by the two essential prime implicants A'C' and BC
- Q3: A'C' removes B (B is 0 in 000 and 1 in 010); BC removes A (A is 0 in 011 and 1 in 111)
- Q4: A=1 B=1 C=0 is a 0 row: LEDG0 off; with correct answers LEDR0 LEDR1 off and LEDR9 off
