# Week 3 exercise 7 answers (keep out of the student repo) - priority circuit, active-low inputs per ID

Original (all inputs active high): Y3 = A, Y2 = A'B, Y1 = A'B'C, Y0 = A'B'C'D. An active-low input flips its literals.

- Y3 = @MSOP
- Y2 = @MSOP
- Y1 = @MSOP
- Y0 = @MSOP
- Q1: the most important active request wins; on A=0 B=1 C=1 D=0 every output is checked against it
- Q2: the inputs that light their output when they are 0 (the first rows of the table show it)
- Q3: Y3 checks only A; Y0 must check that A, B and C are all off and D is on - 4 literals
- Q4: after the winning request, the lower requests do not matter: X; the equations do not use them
