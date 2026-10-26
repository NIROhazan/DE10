# ex0_eq - personal questions (per student ID), from 2026-10-04
Every student gets their own numbers from their ID, so there is no single answer key.
- `C:/DE10/solutions/answers.bat ex0 <ID>` - that student's 10 questions, every right answer, and the codes.
- `C:/DE10/solutions/verify.bat <folder>` - checks all moodle.txt files downloaded from Moodle (unzipped), writes grades.csv.
  BAD CODES = codes that do not belong to the ID in the file (copied); SAME ID IN 2 FILES = a friend's ID used.
- The code key is in C:/DE10/ex0_eq/tools/student.ps1 ($codeKey). A student who reads the script could
  make codes without solving - change the key before each semester (old codes stop working).
Levels: Q1 read A, Q2 OR, Q3 AND, Q4 ~A backwards, Q5 XOR, Q6 A'B+C, Q7 (A+B)(A+C) find B, Q8 XOR solve A,
Q9 B+C' (C' sets bit 3, A does not matter), Q10 (A+B)(A'+C) per-bit MUX.
