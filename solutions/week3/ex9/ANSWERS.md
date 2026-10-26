# Week 3 exercise 9 answers (keep out of the student repo) - original circuit n1 = (AB')', n2 = (A' + C)', n3 = (n1 n2')', Y = (n3 + BC)'

1s: 000 001 010.  n1 = A' + B, n2 = AC', n3 = (A' + BC)' = A(B' + C'), Y = (A' + BC)(B' + C') = A'B' + A'C'

- MSOP = @MSOP
- MPOS = @MPOS
- Q1: n3 = A(B' + C')  (De Morgan twice, T8' (A' + B)(A' + C) = A' + BC)
- Q2: the bubble of n2 and the inverter on n2 at the input of n3; the output bubble of n3 and the NOR at Y
- Q3: 4 levels (n1/n2, n3, Y and the inverters); the minimal SOP needs 2 - same function, fewer levels
- Q4 (correct answers): A=0 B=1 C=1 -> Y = 0: LEDG0 off, LEDR0-1 off, LEDR9 off
