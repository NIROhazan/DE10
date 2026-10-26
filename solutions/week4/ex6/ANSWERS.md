# Week 4 exercise 6 answers - a K-map with four variables, groups of 8 and 4 (keep out of the student repo)

Original table: 0s 0100 1100 1101 1111, all other 12 rows are 1s.

- MSOP = B' + CD' + A'D        3 terms, 5 literals, unique, all essential (A'C is a 4th prime implicant, not needed)
  B' = the 8 rows with B = 0 (top and bottom rows of the map, wrapping); CD' = column CD = 10; A'D = 0001 0011 0101 0111
- MPOS = (B' + C + D)(A' + B' + D')   2 sums, 6 literals, unique. (B'+C+D) kills 0100 1100, (A'+B'+D') kills 1101 1111
- Q1: 8 squares; a circle must be a rectangle of 1, 2, 4 or 8 squares (a power of two in each direction) so that whole variables drop out - 6 squares do not drop a variable (8 squares drop 3 of the 4 variables)
- Q2: MPOS has fewer terms (2 vs 3), MSOP fewer literals (5 vs 6); either choice with a reason (fewer gates vs fewer gate inputs)
- Q3: any smaller circle inside one of the terms, e.g. B'C' (4 squares) instead of B' - more literals and then more terms are needed to cover the rest
- Q4: A=1 B=1 C=0 D=1 is a 0 row: LEDG0 off; with correct answers LEDR0 LEDR1 off and LEDR9 off
