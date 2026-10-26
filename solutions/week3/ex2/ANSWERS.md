# Week 3 exercise 2 answers (keep out of the student repo)

Y = 1 exactly when A = B = C.

- SOP = A'B'C' + ABC   (already minimal as SOP: 000 and 111 differ in all three variables)
- POS = (A+B+C')(A+B'+C)(A+B'+C')(A'+B+C)(A'+B+C')(A'+B'+C)   - six maxterms, rows 001..110
- MIN (minimal POS, 3 terms) = (A'+B)(B'+C)(C'+A)   or the other cycle (A+B')(B+C')(C+A')
  Each 2-literal sum term covers two 0-rows; six 0-rows -> at least 3 terms. A 1-literal
  term would also zero 000 or 111.
- Q1: the number of 1s vs 0s: SOP has one term per 1 (2 here), POS one per 0 (6 here)
- Q2: no - terms merge only if they differ in exactly one literal; 000 and 111 differ in three
- Q3: Y = 1 when all three inputs are equal
- Q4 (correct answers): A=1 B=1 C=0 -> LEDR0, LEDR1, LEDR2, LEDR9 all off (Y = 0)
