# Week 3 exercise 10 answers (keep out of the student repo) - computed from each student's own table by answers.ps1

1s: 001 010 100 110 111      original: D0 = C, D1 = C', D2 = C', D3 = 1, DEC = y1 + y2 + y4 + y6 + y7

- D0  = @MUX0
- D1  = @MUX1
- D2  = @MUX2
- D3  = @MUX3
- DEC = @DEC
- Q1: AB = 00 selects rows 000 and 001; there only C changes, so D0 is Y as a function of C (0, 1, C or C')
- Q2: one decoder output per row with Y = 1 - the canonical SOP: each yi is one minterm
- Q3: log2 N select inputs (2 for 4:1); with an 8:1 mux A B C are all selects and each Di is 0 or 1 - the table itself
- Q4 (correct answers): A=1 B=0 C=1 -> D2 is selected; LEDR0 and LEDR1 both show Y of that row
