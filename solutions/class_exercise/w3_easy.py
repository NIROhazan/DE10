# -*- coding: utf-8 -*-
# Lecture 3: the EASY questions - the circuits of the lecture slides, first in each lesson topic (then the old ones).
# exec'd by gen.py after apply_hebrew (needs Q, bits); the steps are written here in Hebrew directly (he_text.py has no
# entry for these names, so apply_hebrew skips them). Each board holds the slide's circuit; the only personal part is
# the number on HEX0 (a row to set and read). One line = Hebrew OR English.
# EASY_W3[t] = the easy questions of lesson topic t (0, 1, 2); gen.py puts them first in the topic and renumbers.

def _k_out():					# HEX0 shows the variant's number k (4 constant outputs)
    return [("H", (0, b)) for b in range(4)]
def _k_tab(k, n):
    return [[(k >> b) & 1] * (1 << n) for b in range(4)]
def _tt(f, n):					# f(bits MSB first) -> 0/1, for rows 0 .. 2^n - 1
    return [int(f(*bits(r, n))) for r in range(1 << n)]
def _easy(name, title, inputs, outs, hexes, variants, tables, describe, B, steps, **kw):
    q = Q(id="E", name=name, title=title, inputs=inputs, flat=True, outs=outs, hexes=hexes, variants=variants,
          tables=tables, answer=lambda p: steps[-1][1](None, p), describe=describe,
          B=B, L=[], F=[], steps=steps, **kw)
    q.ns = len(q.steps) + 1
    assert q.ns <= 8
    for lines, _ in q.steps:
        for l in lines:
            assert not (any("֐" <= c <= "׿" for c in l) and any(c.isascii() and c.isalpha() for c in l)), (name, l)
    return q

ROW2 = ["SW9 SW8:   0 = 00     1 = 01     2 = 10     3 = 11      (0 = down, 1 = up)"]
ROW3 = ["SW9 SW8 SW7:   0 = 000   1 = 001   2 = 010   3 = 011   4 = 100   5 = 101   6 = 110   7 = 111"]
YESNO = ["כן - הרימו:", "SW0", "לא - השאירו למטה."]
LIT = ["דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."]
SET_K = ["השורה שלכם מוצגת בתצוגה הימנית:", "HEX0", "שימו אותה על המתגים:"]

# ---- topic 1: truth tables, minterms and maxterms, theorems
Y12 = [0, 1, 0, 1]				# slides 11-12: Y = A'B + AB = SIGMA(1, 3)
E_SOP2 = _easy("SOP2", "המעגל של שקופית 12: סכום מכפלות", [9, 8], [("G", 0)] + _k_out(), [[9], [8], None, None],
    [0, 1, 2, 3], lambda k: [Y12] + _k_tab(k, 2), lambda k: f"Y = A'B + AB, row {k:02b} -> Y = {Y12[k]}",
    ["A = SW9     B = SW8     Y = LEDG0 (green)     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגל של שקופית 12:", "Y = A'B + AB = SIGMA(1, 3)", "A = SW9     B = SW8     Y = LEDG0",
       "נסו את 4 המצבים, ובכל אחד רשמו אם הנורה דולקת.", "לכל מצב שהנורה דלקה - הרימו מתג:",
       "A B = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"],
      lambda q, k: (sum(Y12[r] << r for r in range(4)), 0xF)),
     (SET_K + ROW2 + ["הנורה דולקת?"] + LIT, lambda q, k: (Y12[k], 0x1))])

E16 = [0, 0, 1, 0]				# slides 14-16: E = CM' = SIGMA(2) = PI(0, 1, 3)
E_CAFE = _easy("CAFE", "הקפטריה של שקופיות 14-16: מקסטרמים", [9, 8], [("G", 0)] + _k_out(), [[9], [8], None, None],
    [0, 1, 3], lambda k: [E16] + _k_tab(k, 2), lambda k: f"E = CM', maxterm row {k:02b}",
    ["C = SW9 (clean)     M = SW8 (meatloaf)     E = LEDG0 (eat)     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגל של הקפטריה (שקופיות 14-16):", "E = CM' = SIGMA(2) = PI(0, 1, 3)",
       "C = SW9 (clean)     M = SW8 (meatloaf)     E = LEDG0 (eat)",
       "נסו את 4 המצבים. בכמה מהם הנורה כבויה (כמה מקסטרמים)?", "1 = SW0     2 = SW1     3 = SW1+SW0"],
      lambda q, k: (3, 0x3)),
     (SET_K + ROW2 + ["הנורה כבויה: זה מקסטרם. איזה סכום שווה 0 בשורה הזאת? הרימו:",
       "C + M = all down     C + M' = SW0     C' + M = SW1     C' + M' = SW1+SW0"], lambda q, k: (k, 0x3))])

COV = _tt(lambda b, c: b & (b | c), 2)		# slides 39-40: T9 covering B(B + C) = B
E_COVER = _easy("COVER", "משפט הכיסוי של שקופית 40: אינדוקציה מלאה", [9, 8], [("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: [COV, _tt(lambda b, c: b, 2)] + _k_tab(k, 2),
    lambda k: f"B(B + C) and B, row {k:02b}",
    ["B = SW9     C = SW8     LEFT = LEDG1     RIGHT = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: משפט הכיסוי (שקופיות 39-40):", "B(B + C) = B",
       "B = SW9     C = SW8     LEFT = B(B + C) = LEDG1     RIGHT = B = LEDG0",
       "אינדוקציה מלאה: נסו את 4 המצבים. האם שתי הנורות שוות בכולם?"] + YESNO, lambda q, k: (1, 0x1)),
     (SET_K + ROW2 + ["העתיקו את שתי הנורות:", "LEDG1 -> SW1     LEDG0 -> SW0"],
      lambda q, k: (3 if k >= 2 else 0, 0x3))])

# ---- topic 2: from words to an equation, De Morgan
P17 = _tt(lambda r, s: (1 - r) & s, 2)		# slide 17: P = R'S
E_PARK = _easy("PARK", "הפארק של שקופית 17: ממילים למשוואה", [9, 8], [("G", 0)] + _k_out(), [[9], [8], None, None],
    [0, 1, 2, 3], lambda k: [P17] + _k_tab(k, 2), lambda k: f"P = R'S, row {k:02b} -> P = {P17[k]}",
    ["R = SW9 (rain)     S = SW8 (sandwiches)     P = LEDG0 (park)     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: הסיפור של שקופית 17 - הולכים לפארק אם לא יורד גשם ויש כריכים:", "P = R'S",
       "R = SW9 (rain)     S = SW8 (sandwiches)     P = LEDG0 (park)",
       "נסו את 4 המצבים. באיזו שורה הנורה דולקת? שימו את מספר השורה:",
       "R S = 00 -> all down     01 -> SW0     10 -> SW1     11 -> SW1+SW0"], lambda q, k: (1, 0x3)),
     (SET_K + ROW2 + ["הנורה דולקת?"] + LIT, lambda q, k: (P17[k], 0x1))])

DM93 = [_tt(lambda a, b: 1 - (a & b), 2), _tt(lambda a, b: (1 - a) | (1 - b), 2),
        _tt(lambda a, b: 1 - (a | b), 2), _tt(lambda a, b: (1 - a) & (1 - b), 2)]	# slide 93: LEDG3..LEDG0
E_DMGATES = _easy("DMGATES", "דה-מורגן בשערים: שקופית 93", [9, 8], [("G", 3), ("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: DM93 + _k_tab(k, 2), lambda k: f"NAND / NOR two forms, row {k:02b}",
    ["A = SW9     B = SW8     NAND: LEDG3 LEDG2     NOR: LEDG1 LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגלים של שקופית 93 - כל שער בשתי צורות:",
       "NAND:   LEDG3 = (AB)'          LEDG2 = A' + B'", "NOR:    LEDG1 = (A + B)'       LEDG0 = A'B'",
       "A = SW9     B = SW8",
       "אינדוקציה מלאה: נסו את 4 המצבים. האם בכל זוג שתי הנורות שוות תמיד?"] + YESNO, lambda q, k: (1, 0x1)),
     (SET_K + ROW2 + ["העתיקו את ארבע הנורות: נורה דולקת = מתג למעלה.", "LEDGi -> SWi"],
      lambda q, k: (sum(DM93[3 - i][k] << i for i in range(4)), 0xF))])

# ---- topic 3: building blocks
MUX100 = _tt(lambda s, d1, d0: d1 if s else d0, 3)	# slides 99-100: Y = S'D0 + SD1
E_MUX2 = _easy("MUX2", "מרבב 2:1 משערים: שקופית 100", [9, 8, 7], [("G", 0)] + _k_out(), [[9], [8], [7], None],
    list(range(8)), lambda k: [MUX100] + _k_tab(k, 3), lambda k: f"Y = S'D0 + SD1, row {k:03b} -> Y = {MUX100[k]}",
    ["S = SW9     D1 = SW8     D0 = SW7     Y = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: מרבב 2:1 בנוי משערים (שקופית 100):", "Y = S'D0 + SD1",
       "S = SW9     D1 = SW8     D0 = SW7     Y = LEDG0", "שימו:", "SW9 = down     (S = 0)",
       "הזיזו את שתי כניסות הנתונים. איזו מהן מגיעה לנורה? הרימו:", "D0 = SW0     D1 = SW1"],
      lambda q, k: (1, 0x3)),
     (SET_K + ROW3 + ["הנורה דולקת?"] + LIT, lambda q, k: (MUX100[k], 0x1))])

DEC104 = [_tt(lambda a1, a0, j=j: (a1 << 1 | a0) == j, 2) for j in range(4)]	# slides 104-105: Yj = LEDGj
E_DEC24 = _easy("DEC24", "מפענח 2:4: שקופיות 104-105", [9, 8], [("G", j) for j in range(4)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: DEC104 + _k_tab(k, 2), lambda k: f"2:4 decoder, row {k:02b} -> Y{k}",
    ["A1 = SW9     A0 = SW8     Y3..Y0 = LEDG3..LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: מפענח 2:4 (שקופיות 104-105):", "A1 = SW9     A0 = SW8     Y3..Y0 = LEDG3..LEDG0",
       "נסו את 4 המצבים. כמה נורות דולקות בכל פעם?", "1 = SW0     2 = SW1     3 = SW1+SW0"], lambda q, k: (1, 0x3)),
     (SET_K + ROW2 + ["איזו נורה דולקת? הרימו את המתג שלה:", "LEDGi -> SWi"], lambda q, k: (1 << k, 0xF))])

def _prio(a3, a2, a1, a0, j):			# slide 81: Y3 = A3, Y2 = A3'A2, Y1 = A3'A2'A1, Y0 = A3'A2'A1'A0
    a = [a0, a1, a2, a3]
    return a[j] and not any(a[j + 1:])
PRI81 = [_tt(lambda *x, j=j: _prio(*x, j), 4) for j in range(4)]
E_PRIO4 = _easy("PRIO4", "מעגל העדיפויות של שקופית 81", [9, 8, 7, 6], [("G", j) for j in range(4)] + _k_out(),
    [[9, 8, 7, 6], None, None, None], list(range(1, 16)), lambda k: PRI81 + _k_tab(k, 4),
    lambda k: f"priority, A3..A0 = {k:04b} -> Y{k.bit_length() - 1}",
    ["A3 = SW9     A2 = SW8     A1 = SW7     A0 = SW6 (HEX3)     Y3..Y0 = LEDG3..LEDG0     HEX0 = your inputs     answer: SW3..SW0"],
    [(["בלוח: מעגל העדיפויות של שקופית 81:", "Y3 = A3     Y2 = A3'A2     Y1 = A3'A2'A1     Y0 = A3'A2'A1'A0",
       "A3 = SW9     A2 = SW8     A1 = SW7     A0 = SW6     Y3..Y0 = LEDG3..LEDG0",
       "הרימו את כל ארבעת המתגים. איזו נורה דולקת? הרימו את המתג שלה:", "LEDGi -> SWi"], lambda q, k: (8, 0xF)),
     (["בתצוגה הימנית מוצגת ספרה (הקס). שימו אותה בבינארי על ארבעת המתגים, עד שהתצוגה השמאלית תראה אותה ספרה:",
       "HEX0 -> HEX3",
       "8 = SW9     4 = SW8     2 = SW7     1 = SW6",
       "רק הכניסה החזקה מבין המורמות מדליקה נורה. איזו נורה דולקת? הרימו את המתג שלה:", "LEDGi -> SWi"],
      lambda q, k: (1 << (k.bit_length() - 1), 0xF))])


# ---- more easy slide questions (after the ones above in each topic, before the challenge questions)
ROW1 = ["SW9:   0 or 1      (0 = down, 1 = up)"]
HEX4 = ["בתצוגה הימנית מוצגת ספרה (הקס). שימו אותה בבינארי על ארבעת המתגים, עד שהתצוגה השמאלית תראה אותה ספרה:",
        "HEX0 -> HEX3"]
COPY = ["העתיקו את הנורות: נורה דולקת = מתג למעלה.", "LEDGi -> SWi"]
COUNT3 = ["1 = SW0     2 = SW1     3 = SW1+SW0"]

# topic 1
S9 = _tt(lambda a, b, c: a ^ b ^ c, 3)			# slide 9: S, Cout = F(A, B, Cin) - the full adder
CO9 = _tt(lambda a, b, c: (a & b) | (a & c) | (b & c), 3)
L9 = ["Cout = LEDG1     S = LEDG0"]
E_ADDER = _easy("ADDER", "המחבר המלא של שקופית 9: שתי יציאות", [9, 8, 7], [("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], [7], None], list(range(8)), lambda k: [CO9, S9] + _k_tab(k, 3),
    lambda k: f"full adder, row {k:03b} -> Cout S = {CO9[k]}{S9[k]}",
    ["A = SW9     B = SW8     Cin = SW7     Cout = LEDG1     S = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: הדוגמה של שקופית 9 - שתי יציאות של אותן שלוש כניסות (מחבר מלא):", "S = F(A, B, Cin)     Cout = F(A, B, Cin)",
       "A = SW9     B = SW8     Cin = SW7"] + L9 + ["הרימו את שלוש הכניסות (שורה 111)."] + COPY,
      lambda q, k: (3, 0x3)),
     (SET_K + ROW3 + L9 + COPY, lambda q, k: (CO9[k] << 1 | S9[k], 0x3))])

Y13 = _tt(lambda a, b: (a | b) & ((1 - a) | b), 2)	# slide 13: Y = (A + B)(A' + B) = PI(0, 2)
M13 = [_tt(lambda a, b: a | b, 2), _tt(lambda a, b: (1 - a) | b, 2)]
L13 = ["Y = LEDG2     A + B = LEDG1     A' + B = LEDG0"]
E_POS2 = _easy("POS2", "המעגל של שקופית 13: מכפלת סכומים", [9, 8], [("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: [Y13] + M13 + _k_tab(k, 2),
    lambda k: f"Y = (A + B)(A' + B), row {k:02b}",
    ["A = SW9     B = SW8     Y = LEDG2     A + B = LEDG1     A' + B = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגל של שקופית 13 - מכפלה של שני מקסטרמים:", "Y = (A + B)(A' + B) = PI(0, 2)", "A = SW9     B = SW8"]
      + L13 + ["נסו את 4 המצבים. בכמה מהם הנורה של המכפלה כבויה:", "LEDG2"] + COUNT3, lambda q, k: (2, 0x3)),
     (SET_K + ROW2 + L13 + COPY, lambda q, k: (Y13[k] << 2 | M13[0][k] << 1 | M13[1][k], 0x7))])

T1V = [[0, 1], [1, 1], [0, 0], [1, 1]]			# slides 27-33: B*1 = B, B+1 = 1, B*B' = 0, B+B' = 1
L27 = ["LEDG3 = B * 1     LEDG2 = B + 1     LEDG1 = B * B'     LEDG0 = B + B'"]
E_ONEVAR = _easy("ONEVAR", "התיאורמות של משתנה אחד: שקופיות 27-33", [9], [("G", 3), ("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], None, None, None], [0, 1], lambda k: T1V + _k_tab(k, 1), lambda k: f"B = {k}",
    ["B = SW9     LEDG3..LEDG0 = B*1, B+1, B*B', B+B'     HEX0 = your B     answer: SW3..SW0"],
    [(["בלוח: התיאורמות של משתנה אחד (שקופיות 27-33), כל אחת על נורה:", "B = SW9"] + L27
      + ["הזיזו את המתג. איזו נורה תמיד שווה למתג? הרימו את המתג שלה:", "LEDGi -> SWi"], lambda q, k: (8, 0xF)),
     (["הערך שלכם מוצג בתצוגה הימנית:", "HEX0", "שימו אותו על המתג:"] + ROW1 + L27 + COPY,
      lambda q, k: (sum(T1V[3 - i][k] << i for i in range(4)), 0xF))])

P51 = [_tt(lambda a, p: (1 - a) & p, 2), _tt(lambda a, p: a | ((1 - a) & p), 2), _tt(lambda a, p: a | p, 2)]	# slides 50-51
L51 = ["A'P = LEDG2     A + A'P = LEDG1     A + P = LEDG0"]
E_SIMPTH = _easy("SIMPTH", "משפט הפישוט של שקופיות 50-51", [9, 8], [("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: P51 + _k_tab(k, 2), lambda k: f"A + A'P = A + P, row {k:02b}",
    ["A = SW9     P = SW8     A'P = LEDG2     A + A'P = LEDG1     A + P = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: משפט הפישוט (שקופיות 50-51):", "A + A'P = A + P", "A = SW9     P = SW8"] + L51
      + ["נסו את 4 המצבים. באיזה מצב דולקת הנורה הזאת:", "LEDG2",
         "A P = 00 -> all down     01 -> SW0     10 -> SW1     11 -> SW1+SW0"], lambda q, k: (1, 0x3)),
     (SET_K + ROW2 + L51 + COPY, lambda q, k: (sum(P51[2 - i][k] << i for i in range(3)), 0x7))])

# topic 2
W18 = _tt(lambda m, n: m | n, 2)			# slide 18: W = M + N
E_WINNER = _easy("WINNER", "הזוכה של שקופית 18: ממילים למשוואה", [9, 8], [("G", 0)] + _k_out(), [[9], [8], None, None],
    [0, 1, 2, 3], lambda k: [W18] + _k_tab(k, 2), lambda k: f"W = M + N, row {k:02b} -> W = {W18[k]}",
    ["M = SW9 (million)     N = SW8 (notepad)     W = LEDG0 (winner)     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: הסיפור של שקופית 18 - זוכים אם שולחים לכם מיליון דולר או פנקס קטן:", "W = M + N",
       "M = SW9 (million)     N = SW8 (notepad)     W = LEDG0 (winner)",
       "נסו את 4 המצבים. בכמה מהם הנורה דולקת?"] + COUNT3, lambda q, k: (3, 0x3)),
     (SET_K + ROW2 + ["W = LEDG0", "הנורה דולקת?"] + LIT, lambda q, k: (W18[k], 0x1))])

E19 = _tt(lambda m, c, t, x: m | (c & t & (1 - x)), 4)	# slide 19: E = M + CTX'
E_CHEF = _easy("CHEF", "השף של שקופית 19: ממילים למשוואה", [9, 8, 7, 6], [("G", 0)] + _k_out(),
    [[9, 8, 7, 6], None, None, None], list(range(16)), lambda k: [E19] + _k_tab(k, 4),
    lambda k: f"E = M + CTX', M C T X = {k:04b} -> E = {E19[k]}",
    ["M = SW9     C = SW8     T = SW7     X = SW6 (HEX3)     E = LEDG0     HEX0 = your inputs     answer: SW3..SW0"],
    [(["בלוח: הסיפור של שקופית 19 - אוכלים טוב אם מבשלים לבד, או שיש שף מוכשר שאינו יקר:", "E = M + CTX'",
       "M = SW9 (make)     C = SW8 (chef)     T = SW7 (talented)     X = SW6 (expensive)     E = LEDG0 (eat)",
       "שימו:", "SW9 = 0     SW8 = 1     SW7 = 1      (0 = down, 1 = up)",
       "הזיזו את המתג של היוקר. מתי הנורה דולקת? הרימו:", "X = 0 -> SW0     X = 1 -> SW1"], lambda q, k: (1, 0x3)),
     (HEX4 + ["8 = SW9 (M)     4 = SW8 (C)     2 = SW7 (T)     1 = SW6 (X)", "E = LEDG0", "הנורה דולקת?"] + LIT,
      lambda q, k: (E19[k], 0x1))])

E21 = _tt(lambda h, s: (h & s) | (h & (1 - s)), 2)	# slide 21: E = HS + HS' (= H)
E_HATS = _easy("HATS", "הכובע של שקופית 21: משתנה שלא משנה", [9, 8], [("G", 0)] + _k_out(), [[9], [8], None, None],
    [0, 1, 2, 3], lambda k: [E21] + _k_tab(k, 2), lambda k: f"E = HS + HS', row {k:02b} -> E = {E21[k]}",
    ["H = SW9 (hat)     S = SW8 (shoes)     E = LEDG0 (enter)     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: הסיפור של שקופית 21 - נכנסים עם כובע ונעליים, או עם כובע ובלי נעליים:", "E = HS + HS'",
       "H = SW9 (hat)     S = SW8 (shoes)     E = LEDG0 (enter)",
       "נסו את 4 המצבים. איזה מתג אף פעם לא משנה את הנורה? הרימו:", "H -> SW1     S -> SW0"], lambda q, k: (1, 0x3)),
     (SET_K + ROW2 + ["E = LEDG0", "הנורה דולקת?"] + LIT, lambda q, k: (E21[k], 0x1))])

D90 = [_tt(lambda a, b, c: 1 - (b & c), 3), _tt(lambda a, b, c: a | (1 - (b & c)), 3),
       _tt(lambda a, b, c: (1 - a) & b & c, 3)]	# slide 90: Y = (A + (BC)')' = A'BC
L90 = ["(BC)' = LEDG2     A + (BC)' = LEDG1     Y = LEDG0"]
E_DMD1 = _easy("DMD1", "דה-מורגן מבחוץ פנימה: שקופית 90", [9, 8, 7], [("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], [7], None], list(range(8)), lambda k: D90 + _k_tab(k, 3), lambda k: f"Y = (A + (BC)')' = A'BC, row {k:03b}",
    ["A = SW9     B = SW8     C = SW7     (BC)' = LEDG2     A + (BC)' = LEDG1     Y = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: דה-מורגן, הדוגמה הראשונה של שקופית 90 (מבחוץ פנימה):", "Y = (A + (BC)')' = A'BC", "A = SW9     B = SW8     C = SW7"] + L90
      + ["נסו את 8 המצבים. בכמה מהם הנורה הזאת דולקת:", "LEDG0"] + COUNT3, lambda q, k: (1, 0x3)),
     (SET_K + ROW3 + L90 + COPY, lambda q, k: (sum(D90[2 - i][k] << i for i in range(3)), 0x7))])

# topic 3
M78 = [_tt(lambda a, b, c, r=r: (a << 2 | b << 1 | c) == r, 3) for r in (0, 4, 5)]	# slide 78: Y = SIGMA(0, 4, 5)
Y78 = [max(t) for t in zip(*M78)]
L78 = ["A'B'C' = LEDG3     AB'C' = LEDG2     AB'C = LEDG1     Y = LEDG0"]
E_SOP78 = _easy("SOP78", "לוגיקה בשתי רמות: המעגל של שקופית 78", [9, 8, 7], [("G", 3), ("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9], [8], [7], None], list(range(8)), lambda k: M78 + [Y78] + _k_tab(k, 3),
    lambda k: f"Y = A'B'C' + AB'C' + AB'C, row {k:03b}",
    ["A = SW9     B = SW8     C = SW7     AND: LEDG3 LEDG2 LEDG1     Y = LEDG0     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגל של שקופית 78 - שלושה שערי מכפלה ואחריהם סכום:", "Y = A'B'C' + AB'C' + AB'C",
       "A = SW9     B = SW8     C = SW7"] + L78 + ["נסו את 8 המצבים. בכמה מהם הנורה הזאת דולקת:", "LEDG0"] + COUNT3,
      lambda q, k: (3, 0x3)),
     (SET_K + ROW3 + L78 + COPY, lambda q, k: (sum(([Y78] + M78[::-1])[i][k] << i for i in range(4)), 0xF))])

DEC106 = [_tt(lambda a, b, j=j: (a << 1 | b) == j, 2) for j in range(4)]	# slide 106: Y = AB + A'B' = OR of Y3, Y0
Y106 = _tt(lambda a, b: int(a == b), 2)
L106 = ["decoder:   11 = LEDG3     10 = LEDG2     01 = LEDG1     00 = LEDG0", "Y = LEDG4"]
E_DECOR = _easy("DECOR", "לוגיקה בעזרת מפענח: שקופית 106", [9, 8], [("G", j) for j in range(5)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: DEC106 + [Y106] + _k_tab(k, 2),
    lambda k: f"Y = AB + A'B', row {k:02b} -> Y = {Y106[k]}",
    ["A = SW9     B = SW8     decoder = LEDG3..LEDG0     Y = LEDG4     HEX0 = your row     answer: SW3..SW0"],
    [(["בלוח: המעגל של שקופית 106 - מפענח 2:4, ושער סכום על שתיים מהיציאות שלו:", "Y = AB + A'B'",
       "A = SW9     B = SW8"] + L106
      + ["נסו את 4 המצבים. אילו יציאות של המפענח נדלקות יחד עם הנורה הזאת:", "LEDG4", "הרימו את המתגים שלהן:",
         "LEDGi -> SWi"], lambda q, k: (9, 0xF)),
     (SET_K + ROW2 + ["Y = LEDG4", "הנורה דולקת?"] + LIT, lambda q, k: (Y106[k], 0x1))])

N95 = [_tt(lambda a, b, c, d: 1 - (a & b), 4), _tt(lambda a, b, c, d: 1 - (c & d), 4),
       _tt(lambda a, b, c, d: (a & b) | (c & d), 4)]	# slide 95: Y = AB + CD (NAND, NAND, OR with bubbles)
L95 = ["A = SW9     B = SW8     C = SW7     D = SW6", "(AB)' = LEDG2     (CD)' = LEDG1     Y = LEDG0"]
E_NAND95 = _easy("NAND95", "דחיפת בועות: המעגל של שקופית 95", [9, 8, 7, 6], [("G", 2), ("G", 1), ("G", 0)] + _k_out(),
    [[9, 8, 7, 6], None, None, None], list(range(16)), lambda k: N95 + _k_tab(k, 4),
    lambda k: f"Y = AB + CD, A B C D = {k:04b}",
    ["A = SW9     B = SW8     C = SW7     D = SW6 (HEX3)     (AB)' = LEDG2     (CD)' = LEDG1     Y = LEDG0     HEX0 = your inputs     answer: SW3..SW0"],
    [(["בלוח: המעגל של שקופית 95 (דחיפת בועות) - שתי מכפלות עם בועה, ואחריהן סכום עם בועות בכניסות:", "Y = AB + CD"]
      + L95 + ["שימו את ארבעת המתגים למטה."] + COPY, lambda q, k: (6, 0x7)),
     (HEX4 + ["8 = SW9 (A)     4 = SW8 (B)     2 = SW7 (C)     1 = SW6 (D)", "(AB)' = LEDG2     (CD)' = LEDG1     Y = LEDG0"]
      + COPY, lambda q, k: (sum(N95[2 - i][k] << i for i in range(3)), 0x7))])

MUX101 = _tt(lambda s1, s0, d3, d2, d1, d0: [d0, d1, d2, d3][s1 * 2 + s0], 6)	# slide 101: 4:1 mux
L101 = ["S1 = SW9     S0 = SW8     Y = LEDG0", "D3 = SW7     D2 = SW6     D1 = SW5     D0 = SW4"]
PICK = ["הזיזו את כניסות הנתונים. איזו מהן מגיעה לנורה? הרימו:", "D0 -> SW0     D1 -> SW1     D2 -> SW2     D3 -> SW3"]
E_MUX4 = _easy("MUX4", "מרבב 4:1: שקופית 101", [9, 8, 7, 6, 5, 4], [("G", 0)] + _k_out(),
    [[9], [8], None, None], [0, 1, 2, 3], lambda k: [MUX101] + _k_tab(k, 6), lambda k: f"4:1 mux, S1 S0 = {k:02b} -> D{k}",
    ["S1 = SW9     S0 = SW8     D3..D0 = SW7..SW4     Y = LEDG0     HEX0 = your S1 S0     answer: SW3..SW0"],
    [(["בלוח: מרבב 4:1 (שקופית 101):"] + L101 + ["שימו:", "SW9 = 0     SW8 = 0      (S1 S0 = 00)"] + PICK,
      lambda q, k: (1, 0xF)),
     (["קווי הבחירה שלכם מוצגים בתצוגה הימנית:", "HEX0", "שימו אותם על המתגים:"] + ROW2 + L101 + PICK,
      lambda q, k: (1 << k, 0xF))], small=True)

EASY_W3 = [[E_SOP2, E_CAFE, E_COVER, E_ADDER, E_POS2, E_ONEVAR, E_SIMPTH],
           [E_PARK, E_DMGATES, E_WINNER, E_CHEF, E_HATS, E_DMD1],
           [E_MUX2, E_DEC24, E_PRIO4, E_SOP78, E_DECOR, E_NAND95, E_MUX4]]
