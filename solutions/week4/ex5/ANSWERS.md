# Week 4 exercise 5 answers - implicants, prime implicants, essential (keep out of the student repo)

Original table: 1s 000 001 010 101 110 111, 0s 011 100 (they differ in all three variables).

- MSOP = A'B' + BC' + AC        3 terms, 6 literals. The other minimal SOP: A'C' + B'C + AB
- MPOS = (A + B' + C')(A' + B + C)   2 sums, 6 literals = the canonical POS (the two 0s cannot be grouped)
- The 1s form a ring of 6 squares on the K-map: 6 prime implicants, each a pair:
  A'B' (000 001), A'C' (000 010), B'C (001 101), BC' (010 110), AC (101 111), AB (110 111)
- Q1: 6 prime implicants (the six pairs above); no group of 4 exists
- Q2: none is essential - every 1 is covered by exactly two prime implicants (a cyclic cover)
- Q3: A'B' + BC' + AC and A'C' + B'C + AB; once one pair is chosen the rest of the ring is forced, and there are two ways to take every second pair
- Q4: yes, A'B'C' implies Y = 1 (row 000 is a 1), so it is an implicant; it is not prime - it grows into A'B' or A'C'
