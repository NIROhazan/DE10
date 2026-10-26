# Class exercise - answer key (instructor only)

Per student: `python gen.py --id <ID>` (login number, every answer as switches, every code).
Codes: `C:/DE10/solutions/verify.bat <folder>` (lines `ce-Qnn: XXXX` in moodle.txt).

## o01 SEQ - Combinational or sequential? (8 black boxes)

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 50. In 5 steps (0 = login).

- step 1: GOAL: read ONE box. Box 0 = LEDR0 (it has no memory). Try the four rows of A B (SW1 SW0) and write LEDR0 for each row. ANSWER: SW3 = LEDR0 at A B = 11,  SW2 = at 10,  SW1 = at 01,  SW0 = at 00.
- step 2: GOAL: a box that REMEMBERS. Box 1 = LEDR1. 1. A B = 00. Raise SW0, then lower it (back to 00). Write LEDR1. 2. Raise SW1, then lower it (back to 00). Write LEDR1. Both times A B = 00 - but LEDR1 is different: the box remembers what came before. ANSWER: SW1 = LEDR1 after move 1,  SW0 = LEDR1 after move 2.
- step 3: GOAL: which other boxes remember? Test all 8 the same way, on two long paths. Path 1 from 00, one switch at a time: SW0 up, SW1 up, SW0 down, SW1 down. Write LEDR7..LEDR0. Path 2 from 00: SW1 up, SW0 up, SW1 down, SW0 down. Write LEDR7..LEDR0. ANSWER: SWi up for every box whose light is different at the end of the two paths.
- step 4: GOAL: ALL boxes with memory. Some remember only in another row, not at 00. For every row of A B, arrive at it from both neighbours (one switch at a time) and watch whether a light depends on where you came from. ANSWER: SWi up for every box with memory (SW7..SW0).
- example variant 0: box0: comb 0001; box1: SR, A sets, B resets; box2: comb 1010; box3: D latch, A enables, D = B; box4: C-element; box5: comb 1000; box6: D latch, A enables, D = B; box7: inverted C-element -> SW = 0011011010

## o02 LATCH - A box with memory: what sets it, what resets it?

12 variants (npub 1 x nsec 12); fewest different answers per printed text: 12. One step (first format).

- answer: SW3 SW2 = A B of the SET row,  SW1 SW0 = A B of the RESET row.
- example variant 0: set at AB=00, reset at AB=01 -> SW = 0000000001

## o03 PI - Maxterms: write F as a product of sums, F = PI(...)

14 variants (npub 1 x nsec 14); fewest different answers per printed text: 14. One step (first format).

- answer: SWi = 1 if maxterm i is in PI(...), row i = A B in binary (SW3..SW0).
- example variant 0: F rows 00..11 = 0001 -> SW = 0000000111

## o04 SIGMA - Minterms: write F as a sum of products, F = SIGMA(...)

182 variants (npub 1 x nsec 182); fewest different answers per printed text: 182. One step (first format).

- answer: SWi = 1 if minterm i is in SIGMA(...), row i = A B C in binary (SW7..SW0).
- example variant 0: F rows 000..111 = 11100000 -> SW = 0000000111

## o05 MINTERM - Which LEDs are minterms?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 79. One step (first format).

- answer: SWi = 1 if LEDRi is a minterm (SW7..SW0).
- example variant 0: LEDR0 = C;  LEDR1 = A B' C';  LEDR2 = (A + B);  LEDR3 = (B + C);  LEDR4 = A' C';  LEDR5 = (A + B + C);  LEDR6 = (B + C);  LEDR7 = A' B' C' -> SW = 0010000010

## o06 MAXTERM - Which LEDs are maxterms?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 84. One step (first format).

- answer: SWi = 1 if LEDRi is a maxterm (SW7..SW0).
- example variant 0: LEDR0 = C;  LEDR1 = A B' C';  LEDR2 = (A + B);  LEDR3 = (B + C);  LEDR4 = A' C';  LEDR5 = (A + B + C);  LEDR6 = (B + C);  LEDR7 = A' B' C' -> SW = 0000100000

## o07 STORY - From a story to an equation

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. One step (first format).

- answer: SWi = 1 for the LED that implements your story (one switch, SW3..SW0).
- example variant 0: LEDR0 = M + CTX';  LEDR1 = (M + C)TX';  LEDR2 = M + CTX;  LEDR3 = M + C + TX' -> SW = 0000000001

## o08 MATTER - Which inputs does the guard really look at?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 10. One step (first format).

- answer: SW3 = H, SW2 = S, SW1 = T, SW0 = V: 1 if that input matters, 0 if E never depends on it.
- example variant 0: uses HV, table 0101010111111111 -> SW = 0000001001

## o09 EQUAL - Perfect induction: which statements are true?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 28. One step (first format).

- answer: SWk = 1 if statement k is TRUE (LEFT = RIGHT in all 8 rows), SW7..SW0.
- example variant 0: k0: BC + BC' = B;  k1: A(A + B) = A;  k2: A + BC = (A + B)(A + C);  k3: A + BC = (A + B)C;  k4: AB + A'C + BC = AB + A'C;  k5: A + A'B = A + B;  k6: (AB)' = A' + B';  k7: (A + B)' = A' + B' -> SW = 0001110111

## o10 WHERE - Perfect induction: find two statements on the board

256 variants (npub 8 x nsec 32); fewest different answers per printed text: 22. One step (first format).

- answer: SW2 SW1 SW0 = the pair number k of X,  SW5 SW4 SW3 = the pair number k of Y.
- example variant 0: X at k=7, Y at k=6 -> SW = 0000110111

## o11 MINSOP - Simplify: the minimal sum of products

232 variants (npub 1 x nsec 232); fewest different answers per printed text: 12. One step (first format).

- answer: SW2 SW1 SW0 = number of implicants (terms),  SW7 SW6 SW5 SW4 = number of literals (SW3 = 0).
- example variant 0: F rows 000..111 = 11000000, min SOP (terms, literals) = (1, 2) -> SW = 0000100001

## o12 LITERAL - The hidden literal, then simplify

36 variants (npub 6 x nsec 6); fewest different answers per printed text: 6. One step (first format).

- answer: SW2 SW1 SW0 = the hidden literal: 0 = A, 1 = A', 2 = B, 3 = B', 4 = C, 5 = C'.
- answer: SW7 SW6 SW5 SW4 = number of literals in the minimal SOP of Y (SW3 = 0).
- example variant 0: ? = A, min SOP literals 2 -> SW = 0000100000

## o13 ERRORS - Common errors: which simplifications are wrong?

240 variants (npub 6 x nsec 40); fewest different answers per printed text: 10. One step (first format).

- answer: SWi = 1 if LEDRi is WRONG (not equal to Y in some row), SW4..SW0.
- example variant 0: LEDR0 = A' + B (wrong);  LEDR1 = A'BC (wrong);  LEDR2 = A';  LEDR3 = A' + BC (wrong);  LEDR4 = A'B + A' -> SW = 0000001011

## o14 DEMORGAN - De Morgan: which results are right?

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. One step (first format).

- answer: SWi = 1 if LEDRi is RIGHT (equal to Y in all 16 rows), SW3..SW0.
- example variant 0: LEDR0 = A'B' + A'D' + C';  LEDR1 = A'(B' + D') + C';  LEDR2 = A'B'D' + C' (wrong);  LEDR3 = A'(B' + D')C' (wrong) -> SW = 0000000011

## o15 MULTIPLY - Multiplying out (SOP) and factoring (POS)

240 variants (npub 6 x nsec 40); fewest different answers per printed text: 13. One step (first format).

- answer: SWi = 1 if LEDRi is RIGHT (equal to Y in all 16 rows), SW5..SW0.
- example variant 0: LEDR0 = A + BCD (wrong);  LEDR1 = A + BC + BD;  LEDR2 = AB + AC + AD (wrong);  LEDR3 = A + B + CD (wrong);  LEDR4 = AC + BD (wrong);  LEDR5 = A + B(C + D) -> SW = 0000100010

## o16 PRIORITY - Priority circuit: the order

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 24. One step (first format).

- answer: SW1 SW0 = number (0-3) of the HIGHEST input,  SW3 SW2 = the second,
- answer: SW5 SW4 = the third,  SW7 SW6 = the LOWEST.
- example variant 0: order (high->low) A2 A1 A3 A0, active-low mask 0101 -> SW = 0000110110

## o17 ACTIVELOW - Priority circuit: active-low inputs

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 16. One step (first format).

- answer: SWi = 1 if Ai is active low, 0 if active high (SW3..SW0).
- example variant 0: active-low mask 0101, order [2, 1, 3, 0] -> SW = 0000000101

## o18 NANDNOR - Two-level logic: NAND or NOR?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 16. One step (first format).

- answer: SW3 = n1, SW2 = n2, SW1 = n3, SW0 = Y:  1 = NAND, 0 = NOR.
- example variant 0: n1 = NOR(A, C'); n2 = NAND(C, A); n3 = NOR(A, B'); Y = NAND(n1, n2, n3) -> SW = 0000000101

## o19 NODE - Two-level logic: the inputs of one gate

255 variants (npub 3 x nsec 85); fewest different answers per printed text: 12. One step (first format).

- answer: Two switches up: SW5 = A, SW4 = A', SW3 = B, SW2 = B', SW1 = C, SW0 = C'.
- example variant 0: node n1: n1 = NAND(A, C); n2 = NOR(B, C'); n3 = NOR(B, A'); Y = NAND(n1, n2, n3) -> SW = 0000100010

## o20 GATES - A multilevel circuit: find the gates

64 variants (npub 1 x nsec 64); fewest different answers per printed text: 64. One step (first format).

- answer: Codes: 0 = AND, 1 = OR, 2 = NAND, 3 = NOR.  SW5 SW4 = G1,  SW3 SW2 = G2,  SW1 SW0 = G3.
- example variant 0: n1 = AND(A, B); n2 = AND(n1, C); Y = AND(n2, D) -> SW = 0000000000

## o21 BUBBLES - Bubble pushing: which circuit is in the board?

64 variants (npub 8 x nsec 8); fewest different answers per printed text: 8. One step (first format).

- answer: SW2 SW1 SW0 = the number of the circuit (0-7).
- example variant 0: circuit 0: n1 = NAND(D', A');  n2 = NAND(B, C');  Y = OR(n1, n2') -> SW = 0000000000

## o22 MUXDATA - A 4:1 mux: what is on its data inputs?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 256. One step (first format).

- answer: Codes: 0 = '0', 1 = '1', 2 = C, 3 = C'.  SW7 SW6 = D3,  SW5 SW4 = D2,  SW3 SW2 = D1,  SW1 SW0 = D0.
- example variant 0: D3 D2 D1 D0 = 0 0 0 0 -> SW = 0000000000

## o23 MUXLOGIC - Logic using a mux: build F with your select lines

255 variants (npub 3 x nsec 85); fewest different answers per printed text: 85. One step (first format).

- answer: Codes: 0 = '0', 1 = '1', 2 = X, 3 = X'.  SW7 SW6 = D3,  SW5 SW4 = D2,  SW3 SW2 = D1,  SW1 SW0 = D0.
- example variant 0: F rows 000..111 = 00000101, D3..D0 = C C 0 0 -> SW = 0010100000

## o24 DECODER - A 3:8 decoder: which LED is which output?

256 variants (npub 8 x nsec 32); fewest different answers per printed text: 23. One step (first format).

- answer: SW2 SW1 SW0 = the LED number (0-7) of your FIRST minterm,  SW5 SW4 SW3 = the LED number of the SECOND.
- example variant 0: row -> LED: 0->0 1->3 2->5 3->2 4->1 5->6 6->7 7->4 -> SW = 0000101110

## o25 DECOR - Logic using a decoder: which outputs go into the gate?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 146. One step (first format).

- answer: SWi = 1 if the output on LEDRi goes into the gate (SW7..SW0).
- example variant 0: Y = SIGMA(2, 4, 5, 6, 7), row -> LED: 0->1 1->4 2->6 3->0 4->2 5->5 6->3 7->7 -> SW = 0011101100

## Q01 SOP2 - המעגל של שקופית 12: סכום מכפלות

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: המעגל של שקופית 12: Y = A'B + AB = SIGMA(1, 3) A = SW9     B = SW8     Y = LEDG0 נסו את 4 המצבים, ובכל אחד רשמו אם הנורה דולקת. לכל מצב שהנורה דלקה - הרימו מתג: A B = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: Y = A'B + AB, row 00 -> Y = 0 -> SW = 0000000000

## Q02 CAFE - הקפטריה של שקופיות 14-16: מקסטרמים

3 variants (npub 1 x nsec 3); fewest different answers per printed text: 3. In 3 steps (0 = login).

- step 1: בלוח: המעגל של הקפטריה (שקופיות 14-16): E = CM' = SIGMA(2) = PI(0, 1, 3) C = SW9 (clean)     M = SW8 (meatloaf)     E = LEDG0 (eat) נסו את 4 המצבים. בכמה מהם הנורה כבויה (כמה מקסטרמים)? 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) הנורה כבויה: זה מקסטרם. איזה סכום שווה 0 בשורה הזאת? הרימו: C + M = all down     C + M' = SW0     C' + M = SW1     C' + M' = SW1+SW0
- example variant 0: E = CM', maxterm row 00 -> SW = 0000000000

## Q03 COVER - משפט הכיסוי של שקופית 40: אינדוקציה מלאה

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: משפט הכיסוי (שקופיות 39-40): B(B + C) = B B = SW9     C = SW8     LEFT = B(B + C) = LEDG1     RIGHT = B = LEDG0 אינדוקציה מלאה: נסו את 4 המצבים. האם שתי הנורות שוות בכולם? כן - הרימו: SW0 לא - השאירו למטה.
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) העתיקו את שתי הנורות: LEDG1 -> SW1     LEDG0 -> SW0
- example variant 0: B(B + C) and B, row 00 -> SW = 0000000000

## Q04 ADDER - המחבר המלא של שקופית 9: שתי יציאות

8 variants (npub 1 x nsec 8); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: הדוגמה של שקופית 9 - שתי יציאות של אותן שלוש כניסות (מחבר מלא): S = F(A, B, Cin)     Cout = F(A, B, Cin) A = SW9     B = SW8     Cin = SW7 Cout = LEDG1     S = LEDG0 הרימו את שלוש הכניסות (שורה 111). העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8 SW7:   0 = 000   1 = 001   2 = 010   3 = 011   4 = 100   5 = 101   6 = 110   7 = 111 Cout = LEDG1     S = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: full adder, row 000 -> Cout S = 00 -> SW = 0000000000

## Q05 POS2 - המעגל של שקופית 13: מכפלת סכומים

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 3. In 3 steps (0 = login).

- step 1: בלוח: המעגל של שקופית 13 - מכפלה של שני מקסטרמים: Y = (A + B)(A' + B) = PI(0, 2) A = SW9     B = SW8 Y = LEDG2     A + B = LEDG1     A' + B = LEDG0 נסו את 4 המצבים. בכמה מהם הנורה של המכפלה כבויה: LEDG2 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) Y = LEDG2     A + B = LEDG1     A' + B = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: Y = (A + B)(A' + B), row 00 -> SW = 0000000001

## Q06 ONEVAR - התיאורמות של משתנה אחד: שקופיות 27-33

2 variants (npub 1 x nsec 2); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: התיאורמות של משתנה אחד (שקופיות 27-33), כל אחת על נורה: B = SW9 LEDG3 = B * 1     LEDG2 = B + 1     LEDG1 = B * B'     LEDG0 = B + B' הזיזו את המתג. איזו נורה תמיד שווה למתג? הרימו את המתג שלה: LEDGi -> SWi
- step 2: הערך שלכם מוצג בתצוגה הימנית: HEX0 שימו אותו על המתג: SW9:   0 or 1      (0 = down, 1 = up) LEDG3 = B * 1     LEDG2 = B + 1     LEDG1 = B * B'     LEDG0 = B + B' העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: B = 0 -> SW = 0000000101

## Q07 SIMPTH - משפט הפישוט של שקופיות 50-51

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 3. In 3 steps (0 = login).

- step 1: בלוח: משפט הפישוט (שקופיות 50-51): A + A'P = A + P A = SW9     P = SW8 A'P = LEDG2     A + A'P = LEDG1     A + P = LEDG0 נסו את 4 המצבים. באיזה מצב דולקת הנורה הזאת: LEDG2 A P = 00 -> all down     01 -> SW0     10 -> SW1     11 -> SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) A'P = LEDG2     A + A'P = LEDG1     A + P = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: A + A'P = A + P, row 00 -> SW = 0000000000

## Q08 GATE - איזה שער מוסתר בלוח?

6 variants (npub 1 x nsec 6); fewest different answers per printed text: 6. In 4 steps (0 = login).

- step 1: בלוח מוסתר שער אחד. שתי כניסות, יציאה אחת - הנורה הירוקה. שימו את שני המתגים למטה: SW9 = down   SW8 = down האם הנורה הירוקה דולקת? דולקת - הרימו: SW0 כבויה - השאירו הכל למטה.
- step 2: בלוח מוסתר שער אחד. שתי כניסות, יציאה אחת - הנורה הירוקה. נסו את 4 המצבים של שני המתגים, ורשמו בכל אחד אם הנורה דולקת: SW9 SW8:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 3: בלוח מוסתר שער אחד. שתי כניסות, יציאה אחת - הנורה הירוקה. איזה שער זה? השוו את מה שרשמתם לשערים: AND = 1 only if both are 1      OR = 0 only if both are 0 NAND = 0 only if both are 1     NOR = 1 only if both are 0 XOR = 1 when they differ        XNOR = 1 when they are equal הרימו את המתגים של השער: AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0
- example variant 0: gate AND -> SW = 0000000000

## Q09 SIGMA - מינטרמים ומקסטרמים של פונקציה מוסתרת

182 variants (npub 1 x nsec 182); fewest different answers per printed text: 3. In 6 steps (0 = login).

- step 1: בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down הנורה הירוקה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- step 2: בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה. סבב 1 מתוך 2. החזיקו למטה: SW9 = down נסו 4 מצבים, ובכל אחד רשמו אם הנורה דולקת: SW8 SW7:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 3: בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה. סבב 2 מתוך 2. אותו דבר, אבל החזיקו למעלה: SW9 = up SW8 SW7:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 4: בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה. כמה פעמים הנורה דלקה, בשני הסבבים יחד (מתוך 8)? כל מצב כזה נקרא מינטרם. שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 5: בלוח מוסתרת פונקציה של שלוש כניסות. הפונקציה היא הנורה הירוקה. כמה פעמים הנורה הייתה כבויה (8 פחות התשובה הקודמת)? כל מצב כזה נקרא מקסטרם. שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- example variant 0: F rows 000..111 = 11100000 -> SW = 0000000101

## Q10 TERMS - איזו נורה היא מינטרם, ואיזו מקסטרם?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 4. In 5 steps (0 = login).

- step 1: בלוח 4 נורות ירוקות. כל נורה היא איבר אחד (מכפלה או סכום) של שלוש הכניסות. כל נורה ירוקה היא איבר אחד (מכפלה או סכום) של האותיות: A, B, C הרימו את שלושת המתגים: SW9 SW8 SW7 = up up up העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: בלוח 4 נורות ירוקות. כל נורה היא איבר אחד (מכפלה או סכום) של שלוש הכניסות. עברו על 8 המצבים, ובכל מצב רשמו אילו נורות דולקות: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) בכמה מצבים דולקת הנורה LEDG0? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 3: בלוח 4 נורות ירוקות. כל נורה היא איבר אחד (מכפלה או סכום) של שלוש הכניסות. מינטרם דולק במצב אחד בלבד. איזו נורה דלקה רק פעם אחת? הרימו את המתג שלה: LEDGi -> SWi
- step 4: בלוח 4 נורות ירוקות. כל נורה היא איבר אחד (מכפלה או סכום) של שלוש הכניסות. מקסטרם כבוי במצב אחד בלבד. איזו נורה כבתה רק פעם אחת? הרימו את המתג שלה: LEDGi -> SWi
- example variant 0: LEDG0 s2 11111010, LEDG1 min 00000001, LEDG2 lit 01010101, LEDG3 max 11011111 -> SW = 0000001000

## Q11 MATTER - איזו כניסה לא משנה?

30 variants (npub 1 x nsec 30); fewest different answers per printed text: 3. In 5 steps (0 = login).

- step 1: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. כניסה אחת לא משפיעה עליה אף פעם. עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) בכמה מצבים היא דלקה? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. כניסה אחת לא משפיעה עליה אף פעם. האם הכניסה הזו משנה משהו? A (SW9) השוו זוגות של מצבים שנבדלים רק בה: 000-100    001-101    010-110    011-111 אם הנורה שונה באחד הזוגות - הרימו: SW0 אם היא תמיד אותו דבר - השאירו למטה.
- step 3: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. כניסה אחת לא משפיעה עליה אף פעם. אותו דבר בשביל B (SW8): 000-010    001-011    100-110    101-111 משנה - הרימו: SW0 לא משנה - השאירו למטה.
- step 4: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. כניסה אחת לא משפיעה עליה אף פעם. כניסה אחת אף פעם לא משנה. איזו? (בדקו גם את C:  000-001   010-011   100-101   110-111 ) הרימו מתג אחד: A = SW2     B = SW1     C = SW0
- example variant 0: unused A, F rows 000..111 = 10001000 -> SW = 0000000100

## Q12 SIGMA4 - מינטרמים ומקסטרמים - ארבע כניסות

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 6. In 7 steps (0 = login).

- step 1: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. יש 16 מצבים, אז עובדים ב-4 סבבים של 4 מצבים. סבב 1. החזיקו כל הסבב: SW9 = down   SW8 = down נסו 4 מצבים ורשמו בכל אחד אם הנורה דולקת: SW7 SW6:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 2: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. סבב 2 - כמו סבב 1, רק החזיקו: SW9 = down   SW8 = up SW7 SW6:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 3: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. סבב 3 - כמו סבב 1, רק החזיקו: SW9 = up   SW8 = down SW7 SW6:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 4: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. סבב 4 - כמו סבב 1, רק החזיקו: SW9 = up   SW8 = up SW7 SW6:   down-down,   down-up,   up-down,   up-up לכל מצב שהנורה דלקה - הרימו מתג: 1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3
- step 5: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. כמה פעמים הנורה דלקה, בכל 4 הסבבים (מתוך 16)? אלה המינטרמים. שימו את המספר: 1 = SW0          2 = SW1          3 = SW1+SW0       4 = SW2           5 = SW2+SW0       6 = SW2+SW1 7 = SW2+SW1+SW0  8 = SW3          9 = SW3+SW0      10 = SW3+SW1      11 = SW3+SW1+SW0  12 = SW3+SW2
- step 6: בלוח פונקציה של ארבע כניסות - הנורה הירוקה. יש לה 16 מצבים. כמה פעמים היא הייתה כבויה (16 פחות התשובה הקודמת)? אלה המקסטרמים. שימו את המספר: 1 = SW0          2 = SW1          3 = SW1+SW0       4 = SW2           5 = SW2+SW0       6 = SW2+SW1 7 = SW2+SW1+SW0  8 = SW3          9 = SW3+SW0      10 = SW3+SW1      11 = SW3+SW1+SW0  12 = SW3+SW2
- example variant 0: F rows 0000..1111 = 0010011010100111 -> SW = 0000001000

## Q13 THEOREMS - אינדוקציה מלאה: אילו טענות נכונות?

96 variants (npub 4 x nsec 24); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: בלוח 4 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. כל טענה היא: צד שמאל = צד ימין. הלוח מראה את שני הצדדים בשתי נורות. טענה נכונה = שתי הנורות תמיד שוות (שתיהן דולקות או שתיהן כבויות). בחרו טענה 0: SW9 = down   SW8 = down נסו את 4 המצבים, ובכל אחד בדקו אם שתי הנורות שוות: SW7 SW6:   down-down,   down-up,   up-down,   up-up שוות תמיד - הרימו: SW0 שונות אפילו פעם אחת - השאירו למטה.
- step 2: בלוח 4 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. אותה בדיקה לכל 4 הטענות: statement 0 = down-down   1 = down-up   2 = up-down   3 = up-up הרימו מתג לכל טענה נכונה: statement 0 -> SW0   1 -> SW1   2 -> SW2   3 -> SW3
- step 3: בלוח 4 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. הטענה שלכם: @P חשבו על דף את שני הצדדים שלה ב-4 המצבים: A B    LEFT   RIGHT 0 0 0 1 1 0 1 1 מצאו את מספר הטענה שהנורות שלה מראות בדיוק את זה. שימו את המספר: 0 = all down    1 = SW0    2 = SW1    3 = SW1+SW0
- example variant 0: pairs k0..k3 = A + AB = A, A + A'B = A + B, (AB)' = A' + B', (A + B)' = A' + B' -> SW = 0000000000

## Q14 THEOREMS8 - אינדוקציה מלאה: 8 טענות

256 variants (npub 8 x nsec 32); fewest different answers per printed text: 7. In 4 steps (0 = login).

- step 1: בלוח 8 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. כל טענה היא: צד שמאל = צד ימין. טענה נכונה = שתי הנורות תמיד שוות. בחרו טענה 0: SW9 SW8 SW7 = down down down נסו את 8 המצבים, ובכל אחד בדקו אם שתי הנורות שוות: SW6 SW5 SW4:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) שוות תמיד - הרימו: SW0 שונות אפילו פעם אחת - השאירו למטה.
- step 2: בלוח 8 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. אותה בדיקה לכל 8 הטענות. מספר הטענה: SW9 SW8 SW7:   0 = ddd   1 = ddu   2 = dud   3 = duu   4 = udd   5 = udu   6 = uud   7 = uuu כמה טענות נכונות? שימו את המספר: 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- step 3: בלוח 8 טענות מהצורה: צד שמאל = צד ימין. כל טענה מוצגת בשתי נורות. הטענה שלכם: @P חשבו על דף את שני הצדדים שלה ב-8 המצבים: A B C    LEFT   RIGHT 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 מצאו את מספר הטענה שהנורות שלה מראות בדיוק את זה. שימו את המספר: 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- example variant 0: k0..k7 = (A + B)' = A' + B', (AB)' = A' + B', A + BC = (A + B)(A + C), BC + BC' = B, A(A + B) = A, A + BC = (A + B)C, A + A'B = A + B, AB + A'C + BC = AB + A'C -> SW = 0000000100

## Q15 MINSOP - סכום מכפלות מינימלי

186 variants (npub 1 x nsec 186); fewest different answers per printed text: 6. In 4 steps (0 = login).

- step 1: הפונקציה בשאלה היא הנורה הירוקה. טבלת האמת שלה: הנורה בכל אחד מ-8 המצבים: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) הפונקציה בשאלה הזו היא הנורה הירוקה: F = LEDG0 עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) זו טבלת האמת של הפונקציה. בכמה מצבים היא 1? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: הפונקציה בשאלה היא הנורה הירוקה. טבלת האמת שלה: הנורה בכל אחד מ-8 המצבים: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) מהטבלה שלכם: כתבו איבר אחד לכל מצב שבו הנורה דלקה. למשל המצב 101 הוא האיבר: A B' C עכשיו אחדו כל שני איברים שנבדלים באות אחת בלבד, למשל: A B C  +  A B C'   =   A B חזרו על זה עד שאי אפשר יותר. כמה איברים נשארו? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 3: הפונקציה בשאלה היא הנורה הירוקה. טבלת האמת שלה: הנורה בכל אחד מ-8 המצבים: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) כמה אותיות יש בכל האיברים שנשארו, יחד? למשל: A'B + C   ->   3 שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- example variant 0: F rows 000..111 = 11000000, min SOP (terms, literals) = (1, 2) -> SW = 0000000010

## Q16 LITERAL - הליטרל המוסתר

36 variants (npub 6 x nsec 6); fewest different answers per printed text: 3. In 4 steps (0 = login).

- step 1: עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) בכמה מצבים היא דלקה? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: הלוח מחשב את הביטוי שלכם, עם האות המוסתרת. התוצאה היא הנורה הירוקה. הביטוי שלכם: @P יש בו אות מוסתרת במקום ? נסו כל אחת מהאפשרויות, חשבו את הטבלה על דף, והשוו לטבלה מהלוח. רק אחת מתאימה. הרימו את המתגים שלה: A = SW0    A' = SW1    B = SW1+SW0    B' = SW2    C = SW2+SW0    C' = SW2+SW1
- step 3: הלוח מחשב את הביטוי שלכם, עם האות המוסתרת. התוצאה היא הנורה הירוקה. הביטוי שלכם: @P פשטו את הביטוי (עם האות הנכונה) כמה שאפשר. כמה אותיות נשארו? למשל A'B + C  ->  3 שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- example variant 0: ? = A, min SOP literals 2 -> SW = 0000000010

## Q17 PARK - הפארק של שקופית 17: ממילים למשוואה

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: הסיפור של שקופית 17 - הולכים לפארק אם לא יורד גשם ויש כריכים: P = R'S R = SW9 (rain)     S = SW8 (sandwiches)     P = LEDG0 (park) נסו את 4 המצבים. באיזו שורה הנורה דולקת? שימו את מספר השורה: R S = 00 -> all down     01 -> SW0     10 -> SW1     11 -> SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: P = R'S, row 00 -> P = 0 -> SW = 0000000000

## Q18 DMGATES - דה-מורגן בשערים: שקופית 93

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 3. In 3 steps (0 = login).

- step 1: בלוח: המעגלים של שקופית 93 - כל שער בשתי צורות: NAND:   LEDG3 = (AB)'          LEDG2 = A' + B' NOR:    LEDG1 = (A + B)'       LEDG0 = A'B' A = SW9     B = SW8 אינדוקציה מלאה: נסו את 4 המצבים. האם בכל זוג שתי הנורות שוות תמיד? כן - הרימו: SW0 לא - השאירו למטה.
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) העתיקו את ארבע הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: NAND / NOR two forms, row 00 -> SW = 0000001111

## Q19 WINNER - הזוכה של שקופית 18: ממילים למשוואה

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: הסיפור של שקופית 18 - זוכים אם שולחים לכם מיליון דולר או פנקס קטן: W = M + N M = SW9 (million)     N = SW8 (notepad)     W = LEDG0 (winner) נסו את 4 המצבים. בכמה מהם הנורה דולקת? 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) W = LEDG0 הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: W = M + N, row 00 -> W = 0 -> SW = 0000000000

## Q20 CHEF - השף של שקופית 19: ממילים למשוואה

16 variants (npub 1 x nsec 16); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: הסיפור של שקופית 19 - אוכלים טוב אם מבשלים לבד, או שיש שף מוכשר שאינו יקר: E = M + CTX' M = SW9 (make)     C = SW8 (chef)     T = SW7 (talented)     X = SW6 (expensive)     E = LEDG0 (eat) שימו: SW9 = 0     SW8 = 1     SW7 = 1      (0 = down, 1 = up) הזיזו את המתג של היוקר. מתי הנורה דולקת? הרימו: X = 0 -> SW0     X = 1 -> SW1
- step 2: בתצוגה הימנית מוצגת ספרה (הקס). שימו אותה בבינארי על ארבעת המתגים, עד שהתצוגה השמאלית תראה אותה ספרה: HEX0 -> HEX3 8 = SW9 (M)     4 = SW8 (C)     2 = SW7 (T)     1 = SW6 (X) E = LEDG0 הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: E = M + CTX', M C T X = 0000 -> E = 0 -> SW = 0000000000

## Q21 HATS - הכובע של שקופית 21: משתנה שלא משנה

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: הסיפור של שקופית 21 - נכנסים עם כובע ונעליים, או עם כובע ובלי נעליים: E = HS + HS' H = SW9 (hat)     S = SW8 (shoes)     E = LEDG0 (enter) נסו את 4 המצבים. איזה מתג אף פעם לא משנה את הנורה? הרימו: H -> SW1     S -> SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) E = LEDG0 הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: E = HS + HS', row 00 -> E = 0 -> SW = 0000000000

## Q22 DMD1 - דה-מורגן מבחוץ פנימה: שקופית 90

8 variants (npub 1 x nsec 8); fewest different answers per printed text: 3. In 3 steps (0 = login).

- step 1: בלוח: דה-מורגן, הדוגמה הראשונה של שקופית 90 (מבחוץ פנימה): Y = (A + (BC)')' = A'BC A = SW9     B = SW8     C = SW7 (BC)' = LEDG2     A + (BC)' = LEDG1     Y = LEDG0 נסו את 8 המצבים. בכמה מהם הנורה הזאת דולקת: LEDG0 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8 SW7:   0 = 000   1 = 001   2 = 010   3 = 011   4 = 100   5 = 101   6 = 110   7 = 111 (BC)' = LEDG2     A + (BC)' = LEDG1     Y = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: Y = (A + (BC)')' = A'BC, row 000 -> SW = 0000000110

## Q23 STORY - מסיפור למשוואה

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: בלוח 4 מעגלים של סטודנטים לסיפור שלכם. רק אחד מהם נכון. הסיפור שלכם: @P כתבו אותו על דף כמשוואה. הרימו את שלושת המתגים: SW9 SW8 SW7 = up up up העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: הסיפור שלכם: @P לפי המשוואה שלכם (על דף): מה יוצא במצב הזה? SW9 = up   SW8 = down   SW7 = up יוצא 1 - הרימו: SW0 יוצא 0 - השאירו למטה.
- step 3: בלוח 4 מעגלים של סטודנטים לסיפור שלכם. רק אחד מהם נכון. הסיפור שלכם: @P איזו נורה היא המשוואה שלכם? מלאו את הטבלה לפי המשוואה: A B C    Y 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 והשוו לכל נורה ב-8 המצבים. הרימו את המתג של הנורה שמתאימה בכולם: LEDGi -> SWi
- example variant 0: LEDG0 = R'(S + D); LEDG1 = R'S + D; LEDG2 = R'SD; LEDG3 = R + S + D -> SW = 0000000001

## Q24 DEMORGAN - דה-מורגן: איזו תשובה נכונה?

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: הביטוי שלכם: @P הורידו על דף את הקו העליון (מבחוץ פנימה): (XY)' = X' + Y'        (X + Y)' = X'Y' ומלאו את הטבלה של התוצאה: A B C    Y 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 כמה פעמים יצא 1? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח 4 תשובות של סטודנטים לביטוי שלכם. רק אחת נכונה. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את 4 הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 3: בלוח 4 תשובות של סטודנטים לביטוי שלכם. רק אחת נכונה. השוו כל נורה לטבלה שלכם, בכל 8 המצבים. הרימו את המתג של הנורה הנכונה: LEDGi -> SWi
- example variant 0: LEDG0 = A'B + C'; LEDG1 = A'B' + C'; LEDG2 = A'BC'; LEDG3 = (A' + B)C' -> SW = 0000000001

## Q25 ERRORS - טעויות נפוצות: אילו פישוטים שגויים?

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 6. In 4 steps (0 = login).

- step 1: הביטוי שלכם: @P פתרו אותו בעצמכם, על דף, ומלאו את הטבלה: A B C    Y 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 כמה פעמים יצא 1? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח 4 פישוטים של הביטוי שלכם. שניים מהם שגויים. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את 4 הנורות למתגים: נורה דולקת = מתג למעלה.
- step 3: בלוח 4 פישוטים של הביטוי שלכם. שניים מהם שגויים. השוו כל נורה לטבלה שלכם, בכל 8 המצבים. הרימו מתג לכל נורה שגויה (שונה מהטבלה שלכם במצב כלשהו) - שתי נורות: LEDGi -> SWi
- example variant 0: LEDG0 = A'; LEDG1 = A'B + A'; LEDG2 = A'BC (wrong); LEDG3 = A' + BC (wrong) -> SW = 0000001100

## Q26 MULTIPLY - הכפלה ופירוק: אילו תשובות נכונות?

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 6. In 4 steps (0 = login).

- step 1: הביטוי שלכם: @P פתרו אותו בעצמכם, על דף, ומלאו את הטבלה: A B C    Y 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 כמה פעמים יצא 1? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח 4 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את 4 הנורות למתגים: נורה דולקת = מתג למעלה.
- step 3: בלוח 4 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות. השוו כל נורה לטבלה שלכם, בכל 8 המצבים. הרימו מתג לכל נורה נכונה (שווה לטבלה שלכם בכל המצבים) - שתי נורות: LEDGi -> SWi
- example variant 0: LEDG0 = A + B'C; LEDG1 = AA + AC + AB' + B'C; LEDG2 = AB' + AC (wrong); LEDG3 = A + B' + C (wrong) -> SW = 0000000011

## Q27 STORY4 - מסיפור למשוואה - ארבע אותיות

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: בלוח 4 מעגלים לסיפור שלכם (ארבע אותיות). רק אחד נכון. הסיפור שלכם: @P כתבו אותו על דף כמשוואה. הרימו את ארבעת המתגים: SW9 SW8 SW7 SW6 = up up up up העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: הסיפור שלכם: @P לפי המשוואה שלכם (על דף): מה יוצא במצב הזה? SW9 = up   SW8 = down   SW7 = up   SW6 = down יוצא 1 - הרימו: SW0 יוצא 0 - השאירו למטה.
- step 3: בלוח 4 מעגלים לסיפור שלכם (ארבע אותיות). רק אחד נכון. הסיפור שלכם: @P איזו נורה היא המשוואה שלכם? השוו כל נורה למשוואה ב-16 המצבים (מצב שבו הם שונים פוסל את הנורה). הרימו את המתג של הנורה שמתאימה בכולם: LEDGi -> SWi
- example variant 0: LEDG0 = M + CTX'; LEDG1 = (M + C)TX'; LEDG2 = M + CTX; LEDG3 = M + C + TX' -> SW = 0000000001

## Q28 DEMORGAN4 - דה-מורגן עם ארבע אותיות

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: בלוח 4 תשובות לביטוי שלכם. אחת או שתיים נכונות. שימו את ארבעת המתגים למטה: SW9 SW8 SW7 SW6 = down down down down העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: בלוח 4 תשובות לביטוי שלכם. אחת או שתיים נכונות. עכשיו את ארבעת המתגים למעלה: SW9 SW8 SW7 SW6 = up up up up העתיקו את הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 3: בלוח 4 תשובות לביטוי שלכם. אחת או שתיים נכונות. הביטוי שלכם: @P הורידו על דף את הקו העליון, והשוו כל נורה לתוצאה. הרימו מתג לכל נורה נכונה (אחת או שתיים): LEDGi -> SWi
- example variant 0: LEDG0 = A'B' + A'D' + C'; LEDG1 = A'(B' + D') + C'; LEDG2 = A'B'D' + C' (wrong); LEDG3 = A'(B' + D')C' (wrong) -> SW = 0000000011

## Q29 ERRORS5 - טעויות נפוצות - חמישה פישוטים

240 variants (npub 6 x nsec 40); fewest different answers per printed text: 10. In 4 steps (0 = login).

- step 1: הביטוי שלכם: @P פתרו אותו בעצמכם, על דף, ומלאו את הטבלה: A B C    Y 0 0 0 0 0 1 0 1 0 0 1 1 1 0 0 1 0 1 1 1 0 1 1 1 כמה פעמים יצא 1? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח 5 פישוטים של הביטוי שלכם. חלקם שגויים. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את 5 הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 3: בלוח 5 פישוטים של הביטוי שלכם. חלקם שגויים. השוו כל נורה לטבלה שלכם, בכל 8 המצבים. הרימו מתג לכל נורה שגויה: LEDGi -> SWi
- example variant 0: LEDG0 = A' + B (wrong); LEDG1 = A'B + A'; LEDG2 = A' + BC (wrong); LEDG3 = A'; LEDG4 = A'BC (wrong) -> SW = 0000010101

## Q30 MULTIPLY4 - הכפלה ופירוק - שש תשובות

240 variants (npub 6 x nsec 40); fewest different answers per printed text: 12. In 4 steps (0 = login).

- step 1: בלוח 6 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות. שימו את ארבעת המתגים למטה: SW9 SW8 SW7 SW6 = down down down down העתיקו את 6 הנורות למתגים: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: בלוח 6 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות. עכשיו את ארבעת המתגים למעלה: SW9 SW8 SW7 SW6 = up up up up העתיקו את 6 הנורות למתגים. LEDGi -> SWi
- step 3: בלוח 6 תשובות להכפלה או לפירוק של הביטוי שלכם. שתיים נכונות. הביטוי שלכם: @P הכפילו או פרקו אותו על דף, והשוו כל נורה לתוצאה. הרימו מתג לכל נורה נכונה (שתיים): LEDGi -> SWi
- example variant 0: LEDG0 = A + B(C + D); LEDG1 = A + BC + BD; LEDG2 = A + BCD (wrong); LEDG3 = AB + AC + AD (wrong); LEDG4 = A + B + CD (wrong); LEDG5 = AC + BD (wrong) -> SW = 0000000011

## Q31 MUX2 - מרבב 2:1 משערים: שקופית 100

8 variants (npub 1 x nsec 8); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: מרבב 2:1 בנוי משערים (שקופית 100): Y = S'D0 + SD1 S = SW9     D1 = SW8     D0 = SW7     Y = LEDG0 שימו: SW9 = down     (S = 0) הזיזו את שתי כניסות הנתונים. איזו מהן מגיעה לנורה? הרימו: D0 = SW0     D1 = SW1
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8 SW7:   0 = 000   1 = 001   2 = 010   3 = 011   4 = 100   5 = 101   6 = 110   7 = 111 הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: Y = S'D0 + SD1, row 000 -> Y = 0 -> SW = 0000000000

## Q32 DEC24 - מפענח 2:4: שקופיות 104-105

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: מפענח 2:4 (שקופיות 104-105): A1 = SW9     A0 = SW8     Y3..Y0 = LEDG3..LEDG0 נסו את 4 המצבים. כמה נורות דולקות בכל פעם? 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) איזו נורה דולקת? הרימו את המתג שלה: LEDGi -> SWi
- example variant 0: 2:4 decoder, row 00 -> Y0 -> SW = 0000000001

## Q33 PRIO4 - מעגל העדיפויות של שקופית 81

15 variants (npub 1 x nsec 15); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: מעגל העדיפויות של שקופית 81: Y3 = A3     Y2 = A3'A2     Y1 = A3'A2'A1     Y0 = A3'A2'A1'A0 A3 = SW9     A2 = SW8     A1 = SW7     A0 = SW6     Y3..Y0 = LEDG3..LEDG0 הרימו את כל ארבעת המתגים. איזו נורה דולקת? הרימו את המתג שלה: LEDGi -> SWi
- step 2: בתצוגה הימנית מוצגת ספרה (הקס). שימו אותה בבינארי על ארבעת המתגים, עד שהתצוגה השמאלית תראה אותה ספרה: HEX0 -> HEX3 8 = SW9     4 = SW8     2 = SW7     1 = SW6 רק הכניסה החזקה מבין המורמות מדליקה נורה. איזו נורה דולקת? הרימו את המתג שלה: LEDGi -> SWi
- example variant 0: priority, A3..A0 = 0001 -> Y0 -> SW = 0000000001

## Q34 SOP78 - לוגיקה בשתי רמות: המעגל של שקופית 78

8 variants (npub 1 x nsec 8); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: המעגל של שקופית 78 - שלושה שערי מכפלה ואחריהם סכום: Y = A'B'C' + AB'C' + AB'C A = SW9     B = SW8     C = SW7 A'B'C' = LEDG3     AB'C' = LEDG2     AB'C = LEDG1     Y = LEDG0 נסו את 8 המצבים. בכמה מהם הנורה הזאת דולקת: LEDG0 1 = SW0     2 = SW1     3 = SW1+SW0
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8 SW7:   0 = 000   1 = 001   2 = 010   3 = 011   4 = 100   5 = 101   6 = 110   7 = 111 A'B'C' = LEDG3     AB'C' = LEDG2     AB'C = LEDG1     Y = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: Y = A'B'C' + AB'C' + AB'C, row 000 -> SW = 0000001001

## Q35 DECOR - לוגיקה בעזרת מפענח: שקופית 106

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 3 steps (0 = login).

- step 1: בלוח: המעגל של שקופית 106 - מפענח 2:4, ושער סכום על שתיים מהיציאות שלו: Y = AB + A'B' A = SW9     B = SW8 decoder:   11 = LEDG3     10 = LEDG2     01 = LEDG1     00 = LEDG0 Y = LEDG4 נסו את 4 המצבים. אילו יציאות של המפענח נדלקות יחד עם הנורה הזאת: LEDG4 הרימו את המתגים שלהן: LEDGi -> SWi
- step 2: השורה שלכם מוצגת בתצוגה הימנית: HEX0 שימו אותה על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) Y = LEDG4 הנורה דולקת? דולקת - הרימו: SW0 כבויה - השאירו למטה.
- example variant 0: Y = AB + A'B', row 00 -> Y = 1 -> SW = 0000000001

## Q36 NAND95 - דחיפת בועות: המעגל של שקופית 95

16 variants (npub 1 x nsec 16); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: המעגל של שקופית 95 (דחיפת בועות) - שתי מכפלות עם בועה, ואחריהן סכום עם בועות בכניסות: Y = AB + CD A = SW9     B = SW8     C = SW7     D = SW6 (AB)' = LEDG2     (CD)' = LEDG1     Y = LEDG0 שימו את ארבעת המתגים למטה. העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- step 2: בתצוגה הימנית מוצגת ספרה (הקס). שימו אותה בבינארי על ארבעת המתגים, עד שהתצוגה השמאלית תראה אותה ספרה: HEX0 -> HEX3 8 = SW9 (A)     4 = SW8 (B)     2 = SW7 (C)     1 = SW6 (D) (AB)' = LEDG2     (CD)' = LEDG1     Y = LEDG0 העתיקו את הנורות: נורה דולקת = מתג למעלה. LEDGi -> SWi
- example variant 0: Y = AB + CD, A B C D = 0000 -> SW = 0000000110

## Q37 MUX4 - מרבב 4:1: שקופית 101

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: בלוח: מרבב 4:1 (שקופית 101): S1 = SW9     S0 = SW8     Y = LEDG0 D3 = SW7     D2 = SW6     D1 = SW5     D0 = SW4 שימו: SW9 = 0     SW8 = 0      (S1 S0 = 00) הזיזו את כניסות הנתונים. איזו מהן מגיעה לנורה? הרימו: D0 -> SW0     D1 -> SW1     D2 -> SW2     D3 -> SW3
- step 2: קווי הבחירה שלכם מוצגים בתצוגה הימנית: HEX0 שימו אותם על המתגים: SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up) S1 = SW9     S0 = SW8     Y = LEDG0 D3 = SW7     D2 = SW6     D1 = SW5     D0 = SW4 הזיזו את כניסות הנתונים. איזו מהן מגיעה לנורה? הרימו: D0 -> SW0     D1 -> SW1     D2 -> SW2     D3 -> SW3
- example variant 0: 4:1 mux, S1 S0 = 00 -> D0 -> SW = 0000000001

## Q38 MUX - מה מחובר למרבב?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 4. In 6 steps (0 = login).

- step 1: בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה. המרבב שולח ליציאה כניסה אחת. שימו: SW9 = down   SW8 = down     (Y shows D0) הסתכלו על הנורה פעמיים: SW7 = down, then SW7 = up הרימו מתג אם הנורה דלקה: SW0 = with SW7 down      SW1 = with SW7 up
- step 2: בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה. מה מחובר ל- D0? שימו: SW9 SW8 = down down ובדקו את הנורה פעם עם SW7 = down, then SW7 = up הכלל, לפי שתי הבדיקות: 0,0 -> 0      1,1 -> 1      0,1 -> C      1,0 -> C' הרימו: 0 = both down     1 = SW0     C = SW1     C' = SW1 + SW0
- step 3: בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה. מה מחובר ל- D1? שימו: SW9 SW8 = down up ובדקו את הנורה פעם עם SW7 = down, then SW7 = up הכלל, לפי שתי הבדיקות: 0,0 -> 0      1,1 -> 1      0,1 -> C      1,0 -> C' הרימו: 0 = both down     1 = SW0     C = SW1     C' = SW1 + SW0
- step 4: בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה. מה מחובר ל- D2? שימו: SW9 SW8 = up down ובדקו את הנורה פעם עם SW7 = down, then SW7 = up הכלל, לפי שתי הבדיקות: 0,0 -> 0      1,1 -> 1      0,1 -> C      1,0 -> C' הרימו: 0 = both down     1 = SW0     C = SW1     C' = SW1 + SW0
- step 5: בלוח מרבב: שני קווי בחירה בוחרים איזו מ-4 הכניסות תגיע לנורה הירוקה. מה מחובר ל- D3? שימו: SW9 SW8 = up up ובדקו את הנורה פעם עם SW7 = down, then SW7 = up הכלל, לפי שתי הבדיקות: 0,0 -> 0      1,1 -> 1      0,1 -> C      1,0 -> C' הרימו: 0 = both down     1 = SW0     C = SW1     C' = SW1 + SW0
- example variant 0: D3 D2 D1 D0 = 0 0 0 0 -> SW = 0000000000

## Q39 DECODER - מפענח: איזו נורה היא איזו יציאה?

144 variants (npub 6 x nsec 24); fewest different answers per printed text: 6. In 6 steps (0 = login).

- step 1: בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר. בכל מצב דולקת בדיוק נורה אחת. שימו: SW9 SW8 = down down איזו נורה דולקת? הרימו את המתג שלה, ורשמו על דף: LEDGi -> SWi        (row 00 -> LEDG?)
- step 2: בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר. אותו דבר במצב הבא. שימו: SW9 SW8 = down up איזו נורה דולקת? הרימו את המתג שלה, ורשמו על דף: LEDGi -> SWi        (row 01 -> LEDG?)
- step 3: בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר. אותו דבר במצב הבא. שימו: SW9 SW8 = up down איזו נורה דולקת? הרימו את המתג שלה, ורשמו על דף: LEDGi -> SWi        (row 10 -> LEDG?)
- step 4: בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר. אותו דבר במצב הבא. שימו: SW9 SW8 = up up איזו נורה דולקת? הרימו את המתג שלה, ורשמו על דף: LEDGi -> SWi        (row 11 -> LEDG?)
- step 5: בלוח מפענח: בכל מצב דולקת בדיוק נורה אחת, אבל הסדר של הנורות מוסתר. הפונקציה שלכם: @P היא שער או של שתי יציאות. לפי מה שרשמתם: אילו שתי נורות? הרימו את המתגים שלהן: LEDGi -> SWi
- example variant 0: F = SIGMA(0, 1), row -> LED: 00->LEDG3 01->LEDG2 10->LEDG0 11->LEDG1 -> SW = 0000001100

## Q40 PRIORITY - מעגל עדיפויות: מי מנצח?

24 variants (npub 1 x nsec 24); fewest different answers per printed text: 4. In 5 steps (0 = login).

- step 1: בלוח מעגל עדיפויות: כשכמה כניסות למעלה, רק החזקה מביניהן מדליקה את הנורה שלה. הרימו רק את SW9 (כל השאר למטה). איזו נורה דולקת? הרימו את המתג שלה: LEDGi -> SWi
- step 2: בלוח מעגל עדיפויות: כשכמה כניסות למעלה, רק החזקה מביניהן מדליקה את הנורה שלה. הרימו שניים: SW9 + SW8 רק החזק מביניהם מדליק נורה. איזו? הרימו את המתג שלה: LEDGi -> SWi
- step 3: בלוח מעגל עדיפויות: כשכמה כניסות למעלה, רק החזקה מביניהן מדליקה את הנורה שלה. הרימו את כל הארבעה: SW9 SW8 SW7 SW6 הנורה שדולקת שייכת לחזק ביותר. הרימו את המתג שלה: LEDGi -> SWi
- step 4: בלוח מעגל עדיפויות: כשכמה כניסות למעלה, רק החזקה מביניהן מדליקה את הנורה שלה. מי החלש ביותר? מכל הארבעה למעלה: הורידו את המנצח, ראו מי מנצח עכשיו, הורידו גם אותו... האחרון שנשאר הוא החלש. הרימו מתג אחד: A3 = SW3     A2 = SW2     A1 = SW1     A0 = SW0
- example variant 0: order high -> low: A0 A1 A2 A3 -> SW = 0000001000

## Q41 MUXLOGIC - בונים פונקציה ממרבב

255 variants (npub 3 x nsec 85); fewest different answers per printed text: 4. In 6 steps (0 = login).

- step 1: עברו על 8 המצבים, ובכל מצב רשמו אם הנורה דולקת: SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up) בכמה מצבים היא דלקה? שימו את המספר: 1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2    5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0
- step 2: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. בונים אותה ממרבב עם קווי הבחירה שלכם. קווי הבחירה שלכם: @P מה צריך להיות ב- D0? בטבלה שלכם, מצאו את שני המצבים שבהם קווי הבחירה שלכם (למעלה) הם S1 S0 = 0 0 (one with X = 0, one with X = 1) הכלל, לפי שני המצבים: 0,0 -> 0      1,1 -> 1      0,1 -> X      1,0 -> X' הרימו: 0 = both down     1 = SW0     X = SW1     X' = SW1 + SW0
- step 3: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. בונים אותה ממרבב עם קווי הבחירה שלכם. קווי הבחירה שלכם: @P מה צריך להיות ב- D1? בטבלה שלכם, מצאו את שני המצבים שבהם קווי הבחירה שלכם (למעלה) הם S1 S0 = 0 1 (one with X = 0, one with X = 1) הכלל, לפי שני המצבים: 0,0 -> 0      1,1 -> 1      0,1 -> X      1,0 -> X' הרימו: 0 = both down     1 = SW0     X = SW1     X' = SW1 + SW0
- step 4: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. בונים אותה ממרבב עם קווי הבחירה שלכם. קווי הבחירה שלכם: @P מה צריך להיות ב- D2? בטבלה שלכם, מצאו את שני המצבים שבהם קווי הבחירה שלכם (למעלה) הם S1 S0 = 1 0 (one with X = 0, one with X = 1) הכלל, לפי שני המצבים: 0,0 -> 0      1,1 -> 1      0,1 -> X      1,0 -> X' הרימו: 0 = both down     1 = SW0     X = SW1     X' = SW1 + SW0
- step 5: בלוח פונקציה של שלוש כניסות - הנורה הירוקה. בונים אותה ממרבב עם קווי הבחירה שלכם. קווי הבחירה שלכם: @P מה צריך להיות ב- D3? בטבלה שלכם, מצאו את שני המצבים שבהם קווי הבחירה שלכם (למעלה) הם S1 S0 = 1 1 (one with X = 0, one with X = 1) הכלל, לפי שני המצבים: 0,0 -> 0      1,1 -> 1      0,1 -> X      1,0 -> X' הרימו: 0 = both down     1 = SW0     X = SW1     X' = SW1 + SW0
- example variant 0: F rows 000..111 = 10111011, D3..D0 = 1 C' 1 C' -> SW = 0000000001

## Q42 DEC38 - מפענח 3:8: איזו נורה היא איזו יציאה?

256 variants (npub 8 x nsec 32); fewest different answers per printed text: 7. In 4 steps (0 = login).

- step 1: בלוח מפענח עם 8 יציאות: בכל מצב דולקת נורה אחת, בסדר מוסתר. שימו את שלושת המתגים למטה. דולקת בדיוק נורה אחת. SW9 SW8 SW7 = down down down מה המספר שלה? שימו אותו: (for example LEDG5 -> 5) 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- step 2: בלוח מפענח עם 8 יציאות: בכל מצב דולקת נורה אחת, בסדר מוסתר. עכשיו את שלושתם למעלה: SW9 SW8 SW7 = up up up איזו נורה דולקת? שימו את המספר שלה: 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- step 3: בלוח מפענח עם 8 יציאות: בכל מצב דולקת נורה אחת, בסדר מוסתר. המינטרם שלכם: @P שימו את המצב שלו על המתגים. איזו נורה דולקת? שימו את המספר שלה: 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- example variant 0: row -> LED: 000->2 001->0 010->7 011->1 100->5 101->6 110->3 111->4; minterm 0 -> SW = 0000000010

## Q43 NANDNOR - שתי רמות: NAND או NOR?

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 12. In 4 steps (0 = login).

- step 1: בלוח מעגל של שתי רמות: שני שערים ראשונים, ושער אחרון שמקבל אותם. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את שלוש הנורות: SW2 = n1 (LEDG2)     SW1 = n2 (LEDG1)     SW0 = Y (LEDG0)
- step 2: בלוח מעגל של שתי רמות: שני שערים ראשונים, ושער אחרון שמקבל אותם. עברו על 8 המצבים והסתכלו על n1 (LEDG2) שער של שתי כניסות: אם הוא כבוי רק ב-2 מצבים - הוא NAND ואם הוא דולק רק ב-2 מצבים - הוא NOR הרימו: NAND = SW0 up     NOR = SW0 down
- step 3: בלוח מעגל של שתי רמות: שני שערים ראשונים, ושער אחרון שמקבל אותם. מה נכנס ל- n1? הסתכלו על 2 המצבים המיוחדים שלו: שתי אותיות לא משתנות בהם - הן הכניסות. NAND:  1 there -> X     0 there -> X' NOR:   0 there -> X     1 there -> X' הרימו שני מתגים: SW5 = A   SW4 = A'   SW3 = B   SW2 = B'   SW1 = C   SW0 = C'
- example variant 0: NOR-NOR: n1 = (A', C), n2 = (A, C') -> SW = 0000010010

## Q44 GATES - מעגל רב-שלבי: מצאו את השערים

64 variants (npub 1 x nsec 64); fewest different answers per printed text: 4. In 5 steps (0 = login).

- step 1: בלוח שלושה שערים בשרשרת. כל צומת מוצג בנורה. שימו את ארבעת המתגים למטה: SW9 SW8 SW7 SW6 = down down down down העתיקו את שלוש הנורות: SW2 = n1 (LEDG2)     SW1 = n2 (LEDG1)     SW0 = Y (LEDG0)
- step 2: בלוח שלושה שערים בשרשרת. כל צומת מוצג בנורה. השער הראשון: נסו את 4 המצבים ותראו את n1 (LEDG2) SW9 SW8:   down-down,   down-up,   up-down,   up-up AND = 1 only if both are 1      OR = 0 only if both are 0 NAND = 0 only if both are 1     NOR = 1 only if both are 0 הרימו: AND = both down     OR = SW0     NAND = SW1     NOR = SW1 + SW0
- step 3: בלוח שלושה שערים בשרשרת. כל צומת מוצג בנורה. השער השני: הכניסות שלו הן n1 (LEDG2)  and  C (SW7) והיציאה n2 (LEDG1) נסו את 4 הצירופים: AND = 1 only if both are 1      OR = 0 only if both are 0 NAND = 0 only if both are 1     NOR = 1 only if both are 0 הרימו: AND = both down     OR = SW0     NAND = SW1     NOR = SW1 + SW0
- step 4: בלוח שלושה שערים בשרשרת. כל צומת מוצג בנורה. השער השלישי: הכניסות שלו הן n2 (LEDG1)  and  D (SW6) והיציאה Y (LEDG0) נסו את 4 הצירופים: AND = 1 only if both are 1      OR = 0 only if both are 0 NAND = 0 only if both are 1     NOR = 1 only if both are 0 הרימו: AND = both down     OR = SW0     NAND = SW1     NOR = SW1 + SW0
- example variant 0: n1 = AND(A, B); n2 = AND(n1, C); Y = AND(n2, D) -> SW = 0000000000

## Q45 BUBBLES - דחיפת בועות: איזה מעגל בלוח?

32 variants (npub 8 x nsec 4); fewest different answers per printed text: 4. In 3 steps (0 = login).

- step 1: שני מבטים מהירים. כל המתגים למטה, ואז כולם למעלה: SW9..SW6 = all down, then all up הרימו מתג אם הנורה דלקה: SW0 = all down      SW1 = all up
- step 2: הלוח מחזיק אחד מארבעת המעגלים שלכם. התוצאה היא הנורה הירוקה. המעגלים: @P איזה מהם בלוח? חשבו את Y של כל מעגל בכמה מצבים (התחילו מ-0000 ו-1111), והשוו ללוח עד שנשאר מעגל אחד. שימו את המספר שלו: 0 = all down    1 = SW0    2 = SW1    3 = SW1+SW0
- example variant 0: circuit 0: n1 = NAND(D', A');  n2 = NAND(B, C');  Y = OR(n1, n2') -> SW = 0000000000

## Q46 NANDNOR3 - שתי רמות: שלושה שערים, NAND או NOR

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 16. In 4 steps (0 = login).

- step 1: בלוח מעגל של שתי רמות: שלושה שערים ראשונים, ושער אחרון שמקבל אותם. שימו את שלושת המתגים למטה: SW9 SW8 SW7 = down down down העתיקו את ארבע הנורות: SW3 = n1     SW2 = n2     SW1 = n3     SW0 = Y
- step 2: בלוח מעגל של שתי רמות: שלושה שערים ראשונים, ושער אחרון שמקבל אותם. עברו על 8 המצבים והסתכלו על n1 (LEDG3) כבוי רק ב-2 מצבים - NAND דולק רק ב-2 מצבים - NOR הרימו: NAND = SW0 up     NOR = SW0 down
- step 3: בלוח מעגל של שתי רמות: שלושה שערים ראשונים, ושער אחרון שמקבל אותם. אותו דבר בשביל n2, n3 ובשביל Y: חפשו מצב שבו שלושת הצמתים לא שווים - NAND gives 1 there     NOR gives 0 there הרימו: SW3 = n1   SW2 = n2   SW1 = n3   SW0 = Y      (1 = NAND, 0 = NOR)
- example variant 0: n1 = NOR(A, C'); n2 = NAND(C, A); n3 = NOR(A, B'); Y = NAND(n1, n2, n3) -> SW = 0000000101

## Q47 BUBBLES8 - דחיפת בועות: איזה מ-8 מעגלים?

64 variants (npub 8 x nsec 8); fewest different answers per printed text: 8. In 3 steps (0 = login).

- step 1: שני מבטים מהירים. כל המתגים למטה, ואז כולם למעלה: SW9..SW6 = all down, then all up הרימו מתג אם הנורה דלקה: SW0 = all down      SW1 = all up
- step 2: הלוח מחזיק אחד משמונת המעגלים שלכם. התוצאה היא הנורה הירוקה. המעגלים: @P איזה מהם בלוח? חשבו את Y של כל מעגל בכמה מצבים, והשוו ללוח עד שנשאר אחד. שימו את המספר שלו: 0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0
- example variant 0: circuit 0: n1 = NAND(D', A');  n2 = NAND(B, C');  Y = OR(n1, n2') -> SW = 0000000000

## Q48 LATCH - קופסה עם זיכרון: מה מדליק ומה מכבה?

12 variants (npub 1 x nsec 12); fewest different answers per printed text: 4. In 4 steps (0 = login).

- step 1: בלוח קופסה עם זיכרון: מצב אחד מדליק אותה, מצב אחד מכבה, ובשני האחרים היא זוכרת. הזיזו מתג אחד בכל פעם ועברו בדרך הזו, תוך כדי הסתכלות על הנורה: 00  ->  01  ->  11  ->  10  ->  00          (SW9 SW8) הנורה השתנתה לפחות פעם אחת? הרימו: SW0
- step 2: בלוח קופסה עם זיכרון: מצב אחד מדליק אותה, מצב אחד מכבה, ובשני האחרים היא זוכרת. רק מצב אחד מדליק את הקופסה. באיזה מצב הייתם כשהנורה נדלקה? הרימו: 00 = both down     01 = SW0     10 = SW1     11 = SW1 + SW0
- step 3: בלוח קופסה עם זיכרון: מצב אחד מדליק אותה, מצב אחד מכבה, ובשני האחרים היא זוכרת. ורק מצב אחד מכבה אותה (בשני האחרים היא זוכרת). איזה? הרימו: 00 = both down     01 = SW0     10 = SW1     11 = SW1 + SW0
- example variant 0: ON at AB=00, OFF at AB=01 -> SW = 0000000001

## Q49 DLATCH - נועל D: מי האפשור?

4 variants (npub 1 x nsec 4); fewest different answers per printed text: 2. In 4 steps (0 = login).

- step 1: בלוח נועל: כשהאפשור פעיל הוא מעתיק את הנתון; כשלא - הוא זוכר. לנועל יש כניסת אפשור וכניסת נתון. כשהאפשור פעיל - הוא מעתיק את הנתון; אחרת - הוא זוכר. עברו בדרך הזו: 00  ->  01  ->  11  ->  10  ->  00          (SW9 SW8) הנורה השתנתה לפחות פעם אחת? הרימו: SW0
- step 2: בלוח נועל: כשהאפשור פעיל הוא מעתיק את הנתון; כשלא - הוא זוכר. מי האפשור? קבעו כניסה אחת והזיזו את השנייה למעלה ולמטה. האפשור הוא הכניסה שבאחד המצבים שלה הנורה הולכת אחרי השנייה, ובמצב השני לא זזה. הרימו: A (SW9) = SW1      B (SW8) = SW0
- step 3: בלוח נועל: כשהאפשור פעיל הוא מעתיק את הנתון; כשלא - הוא זוכר. האפשור פעיל כשהוא 1 או כשהוא 0? הרימו: SW0 = 1: active when 1      (SW0 = 0: active when 0)
- example variant 0: D latch, A enables, D = B -> SW = 0000000001

## Q50 SEQ - צירופי או סדרתי? (8 קופסאות)

256 variants (npub 1 x nsec 256); fewest different answers per printed text: 50. In 5 steps (0 = login).

- step 1: בלוח 8 קופסאות עם אותן שתי כניסות. לחלק מהן יש זיכרון. קופסה 0 בלי זיכרון. נסו את 4 המצבים ורשמו את LEDG0: SW9 SW8:   00   01   10   11 לכל מצב שהנורה דלקה - הרימו: 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3
- step 2: בלוח 8 קופסאות עם אותן שתי כניסות. לחלק מהן יש זיכרון. קופסה 1 זוכרת. התחילו ב- 00: 1)  SW8 up, SW8 down      2)  SW9 up, SW9 down בשתי הפעמים חזרתם ל-00, אבל הנורה שונה - היא זוכרת מה היה קודם. הרימו מתג אם הנורה דלקה: SW1 = after 1)      SW0 = after 2)
- step 3: בלוח 8 קופסאות עם אותן שתי כניסות. לחלק מהן יש זיכרון. אילו עוד קופסאות זוכרות? עברו בשתי הדרכים ורשמו את כל הנורות בסוף: path 1:  00 -> 01 -> 11 -> 10 -> 00 path 2:  00 -> 10 -> 11 -> 01 -> 00 הרימו מתג לכל קופסה שהנורה שלה שונה בסוף: LEDGi -> SWi
- step 4: בלוח 8 קופסאות עם אותן שתי כניסות. לחלק מהן יש זיכרון. יש קופסאות שזוכרות רק במצב אחר. הגיעו לכל מצב משני השכנים שלו, ובדקו אם נורה תלויה במאיפה באתם. הרימו מתג לכל קופסה עם זיכרון: LEDGi -> SWi
- example variant 0: box0: comb 0001; box1: SR, A sets, B resets; box2: comb 1010; box3: D latch, A enables, D = B; box4: C-element; box5: comb 1000; box6: D latch, A enables, D = B; box7: inverted C-element -> SW = 0011011010
