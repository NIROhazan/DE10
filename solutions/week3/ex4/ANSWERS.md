# Week 3 exercise 4 answers (keep out of the student repo) - one of 8 stories per ID, keys computed by answers.ps1

Every story is "X and (Y or Z)" (sometimes with a NOT): 3 ones, MSOP 2 terms / 4 literals, MPOS (X)(Y + Z).

- SOP  = @CSOP
- MSOP = @MSOP
- MPOS = @MPOS
- Q1: the 8 values of Y from the story; row 111: every condition of the story is true, check each word
- Q2: X is the condition every case needs; e.g. X = 0 with Z = 1: X(Y + Z) = 0 but XY + Z = 1
- Q3: Sigma lists the rows with Y = 1, Pi the rows with Y = 0 - every row is exactly one of the two
- Q4 (correct answers): A=1 B=0 C=1 -> read Y of that row: LEDG0 = Y, LEDR0-2 = Y, LEDR9 off
