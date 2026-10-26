# -*- coding: utf-8 -*-
# Week 4 class exercise (lecture 4: K-maps, don't cares, timing and glitches, always / case / casez).
# Same engine as lecture 3 (C:/DE10/solutions/class_exercise/gen.py, imported): one board design, steps, PC link,
# Hebrew screens. Instructor only.
#   python gen_w4.py                 simulate every question (iverilog) and write the student files
#   python gen_w4.py --compile       also compile with Quartus and copy sof/Qnn.sof to C:/DE10/week4/class_exercise
#   python gen_w4.py --only Q05      one question
#   python gen_w4.py --id <ID>       a student's answers and codes;  --answers <ID> = the student in the guide
import argparse, functools, itertools, os, random, sys
sys.path.insert(0, "C:/DE10/solutions/class_exercise")
import gen as G

HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
G.LECTURE = "4"
G.PREFIX = "w4|"				# other codes / variants than lecture 3 and week 2
G.REPO = "C:/DE10/solutions/de1/week4"	# the DE1 build, not the repo week
G.HERE = HERE					# build/, answers and the guide go here
G.EXPLAIN_FILE = f"{HERE}/explain_w4.py"
Q, HOLD = G.Q, G.HOLD
rng = random.Random(404)

def hexd(d):					# the 4 outputs of one 7-segment digit
    return [("H", (d, b)) for b in range(4)]
def bitsof(v, n):
    return [(v >> b) & 1 for b in range(n)]
def const(vals, n=1):				# outputs that do not depend on the n inputs (a display of data)
    return [[x] * (1 << n) for x in vals]
def cnt(n):					# a count on the switches, as a ready list
    return [" ".join(f"{k} = " + ("+".join(f"SW{b}" for b in range(3, -1, -1) if k >> b & 1)) for k in range(1, n + 1))]
POS4 = ["1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3"]
BIN5 = ["16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
GATES2 = G.GATES				# AND OR XOR NAND NOR XNOR

# ---------------------------------------------------------------- K-map helpers
KO = [0, 1, 3, 2]				# K-map (Gray) order of two variables: 00 01 11 10
@functools.lru_cache(maxsize=None)
def cells(imp):					# the rows an implicant covers; imp = per variable 1 / 0 / None
    n = len(imp)
    return frozenset(r for r in range(1 << n) if all(v is None or G.bits(r, n)[i] == v for i, v in enumerate(imp)))
def nlit(imp):
    return sum(v is not None for v in imp)
def primes(n, on, dc=frozenset()):
    ok = [imp for imp in itertools.product((1, 0, None), repeat=n) if cells(imp) <= on | dc and cells(imp) & on]
    return [p for p in ok if not any(cells(p) < cells(o) for o in ok)]
def covers(n, on, dc=frozenset()):		# all the minimal covers (fewest circles, then fewest literals)
    P = primes(n, on, dc)
    for k in range(1, len(P) + 1):
        best = []
        for c in itertools.combinations(P, k):
            if frozenset().union(*map(cells, c)) >= on:
                best.append(c)
        if best:
            m = min(sum(map(nlit, c)) for c in best)
            return [c for c in best if sum(map(nlit, c)) == m]
    return [()]
def essential(n, on, dc=frozenset()):
    P = primes(n, on, dc)
    return [p for p in P if any(r in cells(p) and not any(r in cells(o) for o in P if o != p) for r in on)]
def litmask(imp):				# A = SW(2n-1), A' = SW(2n-2), ... last variable' = SW0
    n = len(imp)
    return sum(1 << (2 * (n - 1 - i) + (1 if v else 0)) for i, v in enumerate(imp) if v is not None)
def expr(imp):
    return "".join("ABCD"[i] + ("" if v else "'") for i, v in enumerate(imp) if v is not None) or "1"
def sop(c):
    return " + ".join(expr(p) for p in c)
def krow(f, row, n):				# one K-map row: the cells in K-map order on SW3..SW0
    if n == 3:
        rr = [row * 4 + c for c in KO]
    else:
        rr = [KO[row] * 4 + c for c in KO]
    return sum(f[r] << (3 - k) for k, r in enumerate(rr))
LIT2 = ["A = SW3     A' = SW2     B = SW1     B' = SW0"]
LIT3 = ["A = SW5     A' = SW4     B = SW3     B' = SW2     C = SW1     C' = SW0"]
LIT4 = ["A = SW7   A' = SW6   B = SW5   B' = SW4   C = SW3   C' = SW2   D = SW1   D' = SW0"]
# ready lists of a number on SW3..SW0
DIGL = ["0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2",
        "5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0   8 = SW3   9 = SW3+SW0"]
NUM15 = DIGL + ["10 = SW3+SW1   11 = SW3+SW1+SW0   12 = SW3+SW2   13 = SW3+SW2+SW0",
                "14 = SW3+SW2+SW1   15 = SW3+SW2+SW1+SW0"]
# where each segment of a 7-segment digit is (the slide's names)
DRAW = ["a = top     b = top right     c = bottom right     d = bottom", "e = bottom left     f = top left     g = middle"]
ROW3 = ["BC:   00 -> SW3     01 -> SW2     11 -> SW1     10 -> SW0"]
ROW4 = ["CD:   00 -> SW3     01 -> SW2     11 -> SW1     10 -> SW0"]
LITNOTE = "הרימו מתג לכל ליטרל במכפלה (גרש = משתנה עם קו):"
# a 4-variable product is answered in two steps on SW3..SW0 (the inputs are on SW9..SW6): A,B then C,D
LEG4 = "A = SW9     B = SW8     C = SW7     D = SW6"
LITAB = ["A = SW3     A' = SW2     B = SW1     B' = SW0"]
LITCD = ["C = SW3     C' = SW2     D = SW1     D' = SW0"]
def litsteps4(ctx, imp, what="המכפלה"):	# ctx = the lines that say which product; imp(p) = the product
    return [(ctx + [f"1. כתבו על דף את {what}.", "2. הרימו מתג לכל ליטרל של המשתנים האלה (גרש = משתנה עם קו):",
                    "A, B", "משתנה שלא מופיע במכפלה: אף מתג שלו לא למעלה."] + LITAB,
             lambda q, p: (litmask(imp(p)) >> 4, 0xF)),
            (ctx + [f"עכשיו שאר הליטרלים של {what}.", "הרימו מתג לכל ליטרל של המשתנים האלה (גרש = משתנה עם קו):",
                    "C, D", "משתנה שלא מופיע במכפלה: אף מתג שלו לא למעלה."] + LITCD,
             lambda q, p: (litmask(imp(p)) & 0xF, 0xF))]
def rowsteps4(f, first, extra=(), color=""):	# the 4 rows of a 4-variable K-map, one step each; f(p) = the 16 rows
    return [([(first if k == 0 else "השורה הבאה של מפת קרנו (השורות לפי הסדר של מפת קרנו):"), LEG4, "Y = LEDG0"] +
             list(extra) +
             ["1. שימו את שני המתגים השמאליים לפי השורה:", f"AB = {ROWN[k]}  (SW9 SW8 = {ROWN[k]})",
              "2. נסו את 4 המצבים של שני המתגים שלידם:", "CD = SW7 SW6",
              f"3. בכל תא שהנורה{color} דולקת הרימו מתג:"] + ROW4,
             (lambda k: lambda q, p: (krow(f(p), k, 4), 0xF))(k)) for k in range(4)]
CELL3 = [("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))]
CELL4 = [("H", (3, 0))] + CELL3
def tf(f):					# a function (list of rows) as the LED table
    return [list(f)]

W = []
# ================================================================ topic 1: K-maps
# a 2-variable K-map, one circle
IMP2 = [(1, None), (0, None), (None, 1), (None, 0), (1, 1), (1, 0), (0, 1), (0, 0)]
W.append(Q(id="KMAP2", name="KMAP2", title="מפת קרנו של שני משתנים", inputs=[9, 8], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=IMP2,
    tables=lambda p: [[int(r in cells(p)) for r in range(4)]], answer=lambda p: (litmask(p), 0xF),
    describe=lambda p: f"Y = {expr(p)}",
    B=["A = SW9     B = SW8     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח פונקציה של שני משתנים. נסו את 4 המצבים, ובכל מצב שהנורה דולקת הרימו מתג:",
             "A B:   00 -> SW3     01 -> SW2     10 -> SW1     11 -> SW0"],
            lambda q, p: (sum(int(r in cells(p)) << (3 - r) for r in range(4)), 0xF)),
           (["במפת קרנו כל ה-1 נכנסים בעיגול אחד. כותבים רק משתנים שלא מופיעים בעיגול גם רגילים וגם עם קו.",
             LITNOTE] + LIT2, lambda q, p: (litmask(p), 0xF))]))

# a 3-variable K-map, one circle (also around the edge)
IMP3 = [p for p in itertools.product((1, 0, None), repeat=3) if 1 <= nlit(p) <= 2]
ROWSTEPS3 = lambda f: [(["בלוח פונקציה של שלושה משתנים. מלאו את השורה הראשונה של מפת קרנו:", "A = 0  (SW9 down)",
                         "נסו את 4 העמודות לפי הסדר של מפת קרנו, ובכל תא שהנורה דולקת הרימו מתג:"] + ROW3,
                        lambda q, p: (krow(f(p), 0, 3), 0xF)),
                       (["עכשיו השורה השנייה של מפת קרנו:", "A = 1  (SW9 up)", "אותו דבר: בכל תא שהנורה דולקת הרימו מתג:"] + ROW3,
                        lambda q, p: (krow(f(p), 1, 3), 0xF))]
f_imp = lambda p: [int(r in cells(p)) for r in range(8)]
W.append(Q(id="KMAP3A", name="KMAP3A", title="מפת קרנו של שלושה משתנים - עיגול אחד", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=IMP3,
    tables=lambda p: [f_imp(p)], answer=lambda p: (litmask(p), 0x3F), describe=lambda p: f"Y = {expr(p)}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW5..SW0"], L=[], F=[],
    steps=ROWSTEPS3(f_imp) +
          [(["כל ה-1 נכנסים בעיגול אחד (עיגול יכול לעבור מהקצה הימני לשמאלי).",
             "כותבים רק משתנים שלא מופיעים בעיגול גם רגילים וגם עם קו.", LITNOTE] + LIT3,
            lambda q, p: (litmask(p), 0x3F))]))

# a 3-variable K-map, the minimal SOP; the circle of one cell shown on the board
def good3():
    out = []
    for m in range(256):
        f = [m >> r & 1 for r in range(8)]
        on = frozenset(r for r in range(8) if f[r])
        if not 3 <= len(on) <= 6:
            continue
        cv = covers(3, on)
        if len(cv) != 1 or len(cv[0]) < 2:
            continue
        for r in sorted(on):
            hit = [p for p in cv[0] if r in cells(p)]
            if len(hit) == 1:
                out.append((tuple(f), r, hit[0], len(cv[0])))
    return out
_g3 = good3()
V3 = rng.sample(_g3, min(256, len(_g3)))
W.append(Q(id="KMAP3", name="KMAP3", title="מפת קרנו של שלושה משתנים - סכום מכפלות מינימלי", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)] + CELL3, hexes=[None, None, None, None], variants=V3,
    tables=lambda p: [list(p[0])] + const(G.bits(p[1], 3), 3), answer=lambda p: (litmask(p[2]), 0x3F),
    describe=lambda p: f"Y = {sop(covers(3, frozenset(r for r in range(8) if p[0][r]))[0])}; cell {p[1]:03b} -> {expr(p[2])}",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0   the cell = HEX2 HEX1 HEX0 (A B C)   answer: SW5..SW0"], L=[], F=[],
    steps=ROWSTEPS3(lambda p: p[0]) +
          [(["עגלו את ה-1: כל עיגול גדול ככל האפשר (1, 2 או 4 תאים), ומעט עיגולים ככל האפשר.",
             "כמה עיגולים יש בסכום המכפלות המינימלי?"] + cnt(4), lambda q, p: (p[3], 0xF)),
           (["בתצוגה מוצג תא אחד של המפה:", "HEX2 HEX1 HEX0 = A B C",
             "כתבו את המכפלה של העיגול שמכסה אותו.", LITNOTE] + LIT3, lambda q, p: (litmask(p[2]), 0x3F))]))

# implicants, prime implicants, essential
def goodp():
    out = []
    for m in range(256):
        f = [m >> r & 1 for r in range(8)]
        on = frozenset(r for r in range(8) if f[r])
        if 2 <= len(on) <= 6 and len(primes(3, on)) >= 2:
            out.append((tuple(f), len(primes(3, on)), len(essential(3, on))))
    return out
VP = rng.sample(goodp(), min(256, len(goodp())))
W.append(Q(id="PRIMES", name="PRIMES", title="מכפלות ראשוניות וחיוניות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VP,
    tables=lambda p: [list(p[0])], answer=lambda p: (p[2], 0xF),
    describe=lambda p: f"primes: {sop(primes(3, frozenset(r for r in range(8) if p[0][r])))}; essential {p[2]}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=ROWSTEPS3(lambda p: p[0]) +
          [(["מכפלה ראשונית = עיגול הכי גדול שאפשר, שלא נכנס כולו בעיגול גדול יותר.",
             "כמה מכפלות ראשוניות יש לפונקציה?"] + cnt(6), lambda q, p: (p[1], 0xF)),
           (["מכפלה ראשונית חיונית = יש לה תא של 1 שאף מכפלה ראשונית אחרת לא מכסה.",
             "כמה מכפלות ראשוניות חיוניות יש?", "0 = all down"] + cnt(6), lambda q, p: (p[2], 0xF))]))

# a 4-variable K-map
def good4(k):
    r4, out, seen = random.Random(44), [], set()
    while len(out) < k:
        m = r4.randrange(1 << 16)
        f = tuple(m >> r & 1 for r in range(16))
        on = frozenset(r for r in range(16) if f[r])
        if f in seen or not 5 <= len(on) <= 10:
            continue
        seen.add(f)
        cv = covers(4, on)
        if len(cv) != 1 or not 2 <= len(cv[0]) <= 4:
            continue
        cand = [(r, [p for p in cv[0] if r in cells(p)]) for r in sorted(on)]
        cand = [(r, h[0]) for r, h in cand if len(h) == 1 and nlit(h[0]) <= 3]
        if cand:
            r, p = r4.choice(cand)
            out.append((f, r, p, len(cv[0])))
    return out
V4 = good4(200)
ROWN = ["00", "01", "11", "10"]
W.append(Q(id="KMAP4", name="KMAP4", title="מפת קרנו של ארבעה משתנים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)] + CELL4, hexes=[None, None, None, None], variants=V4,
    tables=lambda p: [list(p[0])] + const(G.bits(p[1], 4), 4), answer=lambda p: (litmask(p[2]) & 0xF, 0xF),
    describe=lambda p: f"Y = {sop(covers(4, frozenset(r for r in range(16) if p[0][r]))[0])}; cell {p[1]:04b} -> {expr(p[2])}",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  the cell = HEX3..HEX0 (A B C D)  answer: SW3..SW0"], L=[], F=[],
    steps=rowsteps4(lambda p: p[0], "בלוח פונקציה של ארבעה משתנים. מלאו את מפת קרנו, שורה אחרי שורה.") +
          [(["עגלו את ה-1 בעיגולים גדולים ככל האפשר (1, 2, 4 או 8 תאים), גם מעבר לקצוות.",
             "כמה עיגולים יש בסכום המכפלות המינימלי?"] + cnt(4), lambda q, p: (p[3], 0xF))] +
          litsteps4(["בתצוגה מוצג תא אחד של המפה:", "HEX3 HEX2 HEX1 HEX0 = A B C D",
                     "מצאו את העיגול של סכום המכפלות המינימלי שמכסה אותו."], lambda p: p[2], "המכפלה של העיגול")))

# ================================================================ topic 2: don't cares, timing, glitches
# a 3-variable K-map with don't cares
def gooddc():
    out = []
    for m in range(6561):
        f, x = [], m
        for r in range(8):
            f.append(x % 3); x //= 3			# 0, 1, 2 = X
        on = frozenset(r for r in range(8) if f[r] == 1)
        dc = frozenset(r for r in range(8) if f[r] == 2)
        if not (1 <= len(dc) <= 2 and 2 <= len(on) <= 5):
            continue
        cv = covers(3, on, dc)
        if len(cv) != 1 or len(cv[0]) < 2:
            continue
        if covers(3, on) and len(covers(3, on)[0]) + sum(map(nlit, covers(3, on)[0])) == len(cv[0]) + sum(map(nlit, cv[0])):
            continue					# the X must help
        for r in sorted(on):
            hit = [p for p in cv[0] if r in cells(p)]
            if len(hit) == 1 and cells(hit[0]) & dc:
                out.append((tuple(f), r, hit[0], len(cv[0])))
    return out
_gd = gooddc()
VD = rng.sample(_gd, min(256, len(_gd)))
W.append(Q(id="DC3", name="DC3", title="מפת קרנו עם לא אכפת", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("G", 1)] + CELL3, hexes=[None, None, None, None], variants=VD,
    tables=lambda p: [[int(v == 1) for v in p[0]], [int(v == 2) for v in p[0]]] + const(G.bits(p[1], 3), 3),
    answer=lambda p: (litmask(p[2]), 0x3F),
    describe=lambda p: f"rows {''.join('01X'[v] for v in p[0])}; Y = {sop(covers(3, frozenset(r for r in range(8) if p[0][r] == 1), frozenset(r for r in range(8) if p[0][r] == 2))[0])}; cell {p[1]:03b} -> {expr(p[2])}",
    B=["A = SW9  B = SW8  C = SW7  Y = LEDG0  X = LEDG1  the cell = HEX2 HEX1 HEX0  answer: SW5..SW0 (rows: SW3..SW0)"], L=[], F=[],
    steps=[(["בלוח פונקציה של שלושה משתנים עם תאים של לא אכפת.",
             "1. שימו מצב על שלושת המתגים:", "A = SW9     B = SW8     C = SW7",
             "2. הנורה הימנית דולקת = 1. הנורה שלידה דולקת = לא אכפת.", "Y = LEDG0 (1)     X = LEDG1 (don't care)",
             "3. מלאו את השורה הראשונה של מפת קרנו:", "A = 0  (SW9 down)",
             "בכל תא שבו הנורה הימנית דולקת הרימו מתג:"] + ROW3,
            lambda q, p: (krow([int(v == 1) for v in p[0]], 0, 3), 0xF)),
           (["עכשיו השורה השנייה: בכל תא שבו הנורה הימנית דולקת הרימו מתג.", "A = 1  (SW9 up)",
             "A = SW9     B = SW8     C = SW7", "Y = LEDG0 (1)"] + ROW3,
            lambda q, p: (krow([int(v == 1) for v in p[0]], 1, 3), 0xF)),
           (["עכשיו התאים של לא אכפת (הנורה השנייה דולקת), בשורה הראשונה:", "A = 0  (SW9 down)",
             "A = SW9     B = SW8     C = SW7", "X = LEDG1 (don't care)"] + ROW3,
            lambda q, p: (krow([int(v == 2) for v in p[0]], 0, 3), 0xF)),
           (["והתאים של לא אכפת בשורה השנייה:", "A = 1  (SW9 up)",
             "A = SW9     B = SW8     C = SW7", "X = LEDG1 (don't care)"] + ROW3,
            lambda q, p: (krow([int(v == 2) for v in p[0]], 1, 3), 0xF)),
           (["לא אכפת נכנס לעיגול רק אם הוא עוזר להגדיל אותו. כמה עיגולים יש בסכום המכפלות המינימלי?"] + cnt(4),
            lambda q, p: (p[3], 0xF)),
           (["בתצוגה מוצג תא אחד של המפה:", "HEX2 HEX1 HEX0 = A B C",
             "כתבו את המכפלה של העיגול שמכסה אותו.", LITNOTE] + LIT3, lambda q, p: (litmask(p[2]), 0x3F))]))

# a segment of the BCD 7-segment decoder (slide 28), with don't cares for 10-15
SEGS = [0b1111110, 0b0110000, 0b1101101, 0b1111001, 0b0110011, 0b1011011, 0b1011111, 0b1110000, 0b1111111, 0b1110011]
def segf(s):					# s = 0..6 = a..g
    return [((SEGS[d] >> (6 - s)) & 1) if d < 10 else 2 for d in range(16)]
def segcv(s):
    f = segf(s)
    return covers(4, frozenset(r for r in range(16) if f[r] == 1), frozenset(range(10, 16)))[0]
SEGN = ["a = all down   b = SW0   c = SW1   d = SW1+SW0   e = SW2   f = SW2+SW0   g = SW2+SW1"]
W.append(Q(id="SEGX", name="SEGX", title="מקטע של תצוגה עם לא אכפת", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[None, None, None, None], variants=list(range(7)),
    tables=lambda s: [[int(v == 1) for v in segf(s)], [int(v == 2) for v in segf(s)]],
    answer=lambda s: (sum(map(nlit, segcv(s))), 0xF),
    describe=lambda s: f"segment {'abcdefg'[s]}: Y = {sop(segcv(s))}",
    B=["data = SW9..SW6 (BCD digit)     Y = LEDG0     X = LEDG1     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מקטע אחד של תצוגת 7 מקטעים, למספר בין 0 ל-9. מעל 9 - לא אכפת:", "Y = LEDG0     X = LEDG1",
             "שימו ספרות על המתגים ובדקו בשביל אילו ספרות הוא דולק. איזה מקטע זה?",
             "data = SW9 SW8 SW7 SW6"] + DRAW + SEGN, lambda q, s: (s, 0x7)),
           (["מלאו מפת קרנו של ארבעה משתנים (10 עד 15 = לא אכפת), ועגלו.",
             "כמה עיגולים יש בסכום המכפלות המינימלי?"] + cnt(5), lambda q, s: (len(segcv(s)), 0xF)),
           (["כמה ליטרלים יש בכל הביטוי המינימלי יחד? (ספרו כל אות, גם עם קו)"] + cnt(9) + ["10 = SW3+SW1"],
            lambda q, s: (sum(map(nlit, segcv(s))), 0xF))]))

# timing of the circuit of slide 17
def tvar(k):
    r, out = random.Random(17 + k), set()
    while len(out) < 256:
        pa, pb = r.randint(2, 9), r.randint(2, 9)
        if k and pa == pb:
            continue
        out.add((pa, r.randint(1, pa - 1), pb, r.randint(1, pb - 1)))
    return sorted(out)
CIRC1 = ["n1 = A AND B     n2 = n1 OR C     Y = n2 AND D"]
DELAYS = ["HEX3 = tpd AND     HEX2 = tcd AND     HEX1 = tpd OR     HEX0 = tcd OR"]
W.append(Q(id="TIMING", name="TIMING", title="השהיה: מסלול קריטי ומסלול קצר", inputs=[9], flat=True,
    outs=hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=tvar(0),
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[2], 4) + bitsof(p[3], 4)),
    answer=lambda p: (p[1], 0x1F), describe=lambda p: f"tpd = {2 * p[0] + p[2]}, tcd = {p[1]}",
    B=["delays = HEX3..HEX0 (tpd AND, tcd AND, tpd OR, tcd OR)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["המעגל:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["מה ההשהיה של המסלול הקריטי (הארוך) - מהכניסה הרחוקה ביותר ליציאה?", "tpd = ?"] + BIN5,
            lambda q, p: (2 * p[0] + p[2], 0x1F)),
           (["המעגל:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["מה ההשהיה של המסלול הקצר - מהכניסה הקרובה ביותר ליציאה?", "tcd = ?"] + BIN5,
            lambda q, p: (p[1], 0x1F))]))

CIRC2 = ["n1 = A AND B     n2 = C OR D     Y = n1 AND n2"]
W.append(Q(id="TIMING2", name="TIMING2", title="איזה מסלול קריטי?", inputs=[9], flat=True,
    outs=hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=tvar(1),
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[2], 4) + bitsof(p[3], 4)),
    answer=lambda p: (min(p[1], p[3]) + p[1], 0x1F),
    describe=lambda p: f"critical {'AB' if p[0] > p[2] else 'CD'}, tpd = {max(p[0], p[2]) + p[0]}, tcd = {min(p[1], p[3]) + p[1]}",
    B=["delays = HEX3..HEX0 (tpd AND, tcd AND, tpd OR, tcd OR)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["המעגל:"] + CIRC2 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["איזה מסלול קריטי (ארוך יותר)?", "A, B (through n1) = all down     C, D (through n2) = SW0"],
            lambda q, p: (int(p[2] > p[0]), 0x1)),
           (["המעגל:"] + CIRC2 + ["בתצוגה ההשהיות של השערים:"] + DELAYS + ["מה ההשהיה של המעגל?", "tpd = ?"] + BIN5,
            lambda q, p: (max(p[0], p[2]) + p[0], 0x1F)),
           (["המעגל:"] + CIRC2 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["מה ההשהיה המינימלית של המעגל?", "tcd = ?"] + BIN5, lambda q, p: (min(p[1], p[3]) + p[1], 0x1F))]))

# a glitch: Y = x y + x' z, fixed by the consensus y z (slides 18-21)
def gl_vars():
    out = []
    for x in range(3):
        o = [i for i in range(3) if i != x]
        for py, pz in itertools.product((0, 1), repeat=2):
            t1 = [None] * 3; t1[x] = 1; t1[o[0]] = py
            t2 = [None] * 3; t2[x] = 0; t2[o[1]] = pz
            fix = [None] * 3; fix[o[0]] = py; fix[o[1]] = pz
            out.append((x, tuple(t1), tuple(t2), tuple(fix)))
            t1b = [None] * 3; t1b[x] = 1; t1b[o[1]] = pz
            t2b = [None] * 3; t2b[x] = 0; t2b[o[0]] = py
            out.append((x, tuple(t1b), tuple(t2b), tuple(fix)))
    return out
VG = gl_vars()
f_gl = lambda p: [int(r in cells(p[1]) or r in cells(p[2])) for r in range(8)]
W.append(Q(id="GLITCH", name="GLITCH", title="תקלה רגעית (גליץ') ותיקון", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VG,
    tables=lambda p: [f_gl(p)], answer=lambda p: (litmask(p[3]), 0x3F),
    describe=lambda p: f"Y = {expr(p[1])} + {expr(p[2])}; glitch on {'ABC'[p[0]]}; fix {expr(p[3])}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW5..SW0"], L=[], F=[],
    steps=ROWSTEPS3(f_gl) +
          [(["בסכום המכפלות המינימלי יש שני עיגולים שנוגעים זה בזה.",
             "משתנה אחד מופיע בעיגול אחד רגיל ובשני עם קו. כשהוא משתנה, היציאה יכולה לקפוץ לרגע ל-0. איזה משתנה?",
             "A = SW2     B = SW1     C = SW0"], lambda q, p: (4 >> p[0], 0x7)),
           (["התיקון: מוסיפים עיגול שמכסה את שני התאים שבגבול בין שני העיגולים.",
             "כתבו את המכפלה שלו.", LITNOTE] + LIT3, lambda q, p: (litmask(p[3]), 0x3F))]))

# ================================================================ topic 3: always, case, casez
# read a 7-segment pattern (abc_defg, slide 28)
LSEG = ["segments = LEDG6..LEDG0     a = LEDG6   b = LEDG5   c = LEDG4   d = LEDG3   e = LEDG2   f = LEDG1   g = LEDG0"]
W.append(Q(id="SEGREAD", name="SEGREAD", title="לקרוא את המקטעים", inputs=[9], flat=True,
    outs=[("G", i) for i in range(7)], hexes=[None, None, None, None], variants=list(range(9)),
    tables=lambda d: const(bitsof(SEGS[d], 7)), answer=lambda d: (SEGS[d + 1], 0x7F),
    describe=lambda d: f"digit {d}, next {SEGS[d + 1]:07b}",
    B=["segments = LEDG6..LEDG0 (abc_defg)     answer: SW6..SW0"], L=[], F=[],
    steps=[(["בלוח מפענח של תצוגת 7 מקטעים, אבל במקום התצוגה כל מקטע הוא נורה ירוקה:",
             "a = LEDG6   b = LEDG5   c = LEDG4   d = LEDG3   e = LEDG2   f = LEDG1   g = LEDG0",
             "1. כמה נורות ירוקות דולקות? (כמה מקטעים דולקים)"] + cnt(7), lambda q, d: (bin(SEGS[d]).count("1"), 0x7)),
           (["2. ציירו ספרה של 7 מקטעים, וסמנו בה את המקטעים שדולקים. המקום של כל מקטע:"] + DRAW +
            ["a = LEDG6   b = LEDG5   c = LEDG4   d = LEDG3   e = LEDG2   f = LEDG1   g = LEDG0",
             "איזו ספרה יצאה? שימו אותה:"] + DIGL, lambda q, d: (d, 0xF)),
           (["3. עכשיו הספרה הבאה (הספרה שמצאתם ועוד 1). אילו מקטעים דולקים בה?",
             "לכל מקטע שצריך לדלוק - הרימו את המתג שלו:"] + DRAW +
            ["a -> SW6   b -> SW5   c -> SW4   d -> SW3   e -> SW2   f -> SW1   g -> SW0"],
            lambda q, d: (SEGS[d + 1], 0x7F))]))

# if / else in always_comb
VI = [(a, b) for a in range(6) for b in range(6) if a != b]
W.append(Q(id="IFELSE", name="IFELSE", title="if / else בתוך always", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VI,
    tables=lambda p: [[GATES2[p[0]][1][r & 3] if r >> 2 else GATES2[p[1]][1][r & 3] for r in range(8)]],
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"if (s) y = {GATES2[p[0]][0]}(a, b); else y = {GATES2[p[1]][0]}(a, b);",
    B=["s = SW9     a = SW8     b = SW7     y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח:", "always_comb  if (s) y = ...(a, b);  else y = ...(a, b);",
             "החזיקו את", "s = 1  (SW9 up)", "נסו את 4 המצבים, ולכל מצב שהנורה דלקה הרימו מתג:",
             "a b (SW8 SW7):   00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"],
            lambda q, p: (sum(GATES2[p[0]][1][r] << r for r in range(4)), 0xF)),
           (["איזה שער כתוב אחרי", "if (s)",
             "AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"], lambda q, p: (p[0], 0x7)),
           (["עכשיו", "s = 0  (SW9 down)", "נסו את 4 המצבים, ולכל מצב שהנורה דלקה הרימו מתג:",
             "a b (SW8 SW7):   00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"],
            lambda q, p: (sum(GATES2[p[1]][1][r] << r for r in range(4)), 0xF)),
           (["איזה שער כתוב אחרי", "else",
             "AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"], lambda q, p: (p[1], 0x7))]))

# a case statement with one wrong line
def bugseg(p):
    return [SEGS[d] ^ (1 << (6 - p[1])) if d == p[0] else SEGS[d] for d in range(10)] + [0] * 6
VB = [(d, s) for d in range(10) for s in range(7)]
W.append(Q(id="CASEBUG", name="CASEBUG", title="שורה שגויה ב-case", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(7)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VB,
    tables=lambda p: [[(bugseg(p)[r] >> b) & 1 for r in range(16)] for b in range(7)], answer=lambda p: (p[1], 0x7),
    describe=lambda p: f"digit {p[0]}, segment {'abcdefg'[p[1]]} wrong",
    B=["data = SW9..SW6 (HEX0)     segments = LEDG6..LEDG0 (abc_defg)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המפענח של השקופית, עם", "case (data)", "אבל באחת השורות 0..9 יש מקטע אחד שגוי.",
             "מה היציאה כשהקלט גדול מ-9? זו השורה של", "default",
             "1. שימו קלט 12:", "data = SW9 SW8 SW7 SW6 = 1100     (HEX0 = C)",
             "2. ספרו כמה נורות דולקות:", "segments = LEDG6..LEDG0",
             "3. הרימו את המספר:", "0 = all down"] + cnt(4), lambda q, p: (0, 0x7)),
           (["עברו על הספרות 0 עד 9 והשוו לטבלה של השקופית. באיזו ספרה יש טעות?",
             "1. שימו ספרה על המתגים:", "data = SW9 SW8 SW7 SW6     (HEX0)",
             "2. השוו את הנורות למקטעים של הספרה:"] + LSEG + DRAW +
            ["3. הרימו את הספרה השגויה:"] + DIGL, lambda q, p: (p[0], 0xF)),
           (["בספרה השגויה מקטע אחד הפוך. איזה מקטע?",
             "1. שימו את הספרה השגויה על המתגים:", "data = SW9 SW8 SW7 SW6     (HEX0)",
             "2. מצאו את הנורה שלא כמו בטבלה:"] + LSEG + DRAW +
            ["3. הרימו את המקטע:",
             "a = all down   b = SW0   c = SW1   d = SW1+SW0   e = SW2   f = SW2+SW0   g = SW2+SW1"], lambda q, p: (p[1], 0x7))]))

# a priority casez with a hidden order
PRI = list(itertools.permutations(range(4)))
def prio(order, a):				# order = input bits from the highest priority; y = one-hot of the winner
    for b in order:
        if a >> b & 1:
            return 1 << b
    return 0
W.append(Q(id="CASEZ", name="CASEZ", title="casez עם עדיפות מוסתרת", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=PRI,
    tables=lambda p: [[(prio(p, r) >> b) & 1 for r in range(16)] for b in range(4)],
    answer=lambda p: (1 << p[2], 0xF), describe=lambda p: "priority " + " > ".join(f"a[{b}]" for b in p),
    B=["a[3:0] = SW9..SW6     y[3:0] = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מקודד עדיפות עם", "casez", "כמו בשקופית, אבל סדר העדיפות מוסתר.",
             "הרימו את כל 4 הכניסות. רק הכניסה שמנצחת דולקת ביציאה. העתיקו:",
             "SW9 SW8 SW7 SW6 = 1111", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (1 << p[0], 0xF)),
           (["הורידו את הכניסה שניצחה (שאר הכניסות למעלה). מי מנצחת עכשיו? העתיקו:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, p: (1 << p[1], 0xF)),
           (["הורידו גם אותה. מי מנצחת עכשיו? העתיקו:", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (1 << p[2], 0xF))]))

# a casez pattern with ? bits
VZ = [p for p in itertools.product((0, 1, None), repeat=4) if any(v is not None for v in p)]
VZ = random.Random(30).sample(VZ, len(VZ))
def zmatch(p, r):				# p = a[3] .. a[0]
    return int(all(v is None or (r >> (3 - i) & 1) == v for i, v in enumerate(p)))
W.append(Q(id="CASEZQ", name="CASEZQ", title="תבנית של casez עם סימני שאלה", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=VZ,
    tables=lambda p: [[zmatch(p, r) for r in range(16)]],
    answer=lambda p: (sum((v or 0) << (3 - i) for i, v in enumerate(p)), 0xF),
    describe=lambda p: "4'b" + "".join("?" if v is None else str(v) for v in p),
    B=["a[3:0] = SW9..SW6     match = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שורה אחת של", "casez (a)", "הנורה דולקת כשהקלט מתאים לתבנית של השורה. סימן שאלה = כל ערך מתאים.",
             "a[3:0] = SW9 SW8 SW7 SW6",
             "מצאו קלט אחד שמדליק את הנורה, והעתיקו אותו:", "SW3..SW0 = SW9..SW6"],
            lambda q, p: (sum((v or 0) << (3 - i) for i, v in enumerate(p)), sum((v is not None) << (3 - i) for i, v in enumerate(p)))),
           (["אילו ביטים בתבנית הם סימן שאלה? (שינוי שלהם לא מכבה את הנורה) הרימו מתג לכל אחד:",
             "a[3] -> SW3     a[2] -> SW2     a[1] -> SW1     a[0] -> SW0"],
            lambda q, p: (sum((v is None) << (3 - i) for i, v in enumerate(p)), 0xF)),
           (["כתבו את התבנית: כל ביט שהוא לא סימן שאלה - הערך שלו; סימן שאלה - למטה.",
             "a[3] -> SW3     a[2] -> SW2     a[1] -> SW1     a[0] -> SW0"],
            lambda q, p: (sum((v or 0) << (3 - i) for i, v in enumerate(p)), 0xF))]))

# ================================================================ more questions (ids set below, in lesson order)
# a 4-variable K-map, one circle of 2, 4 or 8 cells (also the edges and the corners)
IMP4 = [p for p in itertools.product((1, 0, None), repeat=4) if 1 <= nlit(p) <= 3]
f_imp4 = lambda p: [int(r in cells(p)) for r in range(16)]
W.append(Q(id="KMAP4A", name="KMAP4A", title="מפת קרנו של ארבעה משתנים - עיגול אחד", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, None], variants=IMP4,
    tables=lambda p: [f_imp4(p)], answer=lambda p: (litmask(p) & 0xF, 0xF), describe=lambda p: f"Y = {expr(p)}",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח פונקציה של ארבעה משתנים, וכל ה-1 שלה נכנסים בעיגול אחד.",
             "1. נסו את 16 המצבים של ארבעת המתגים:", LEG4,
             "2. סמנו על דף מפת קרנו: תא לכל מצב שהנורה דולקת.", "Y = LEDG0",
             "3. בכמה מצבים הנורה דולקת? הרימו את המספר:", "2 = SW1     4 = SW2     8 = SW3"],
            lambda q, p: (1 << (4 - nlit(p)), 0xF))] +
          litsteps4(["במפה של ארבעה משתנים גם הקצוות סמוכים, וגם ארבע הפינות.",
                     "המכפלה של העיגול: כותבים רק משתנים שקבועים בכל העיגול."], lambda p: p, "המכפלה של העיגול")))

# which don't cares the minimal SOP uses
def dcf(p):
    on = frozenset(r for r in range(8) if p[0][r] == 1)
    dc = frozenset(r for r in range(8) if p[0][r] == 2)
    return on, dc, covers(3, on, dc)[0]
def kpos8(rows):				# a set of rows as K-map cells: A=0 on SW7..SW4, A=1 on SW3..SW0
    f = [int(r in rows) for r in range(8)]
    return (krow(f, 0, 3) << 4) | krow(f, 1, 3)
VU = random.Random(55).sample(_gd, 256)
def used_x(p):					# the don't-care rows inside the circles of the minimal SOP
    on, dc, cv = dcf(p)
    return dc & frozenset().union(*map(cells, cv))
DCLEG = ["A = SW9     B = SW8     C = SW7", "Y = LEDG0 (1)     X = LEDG1 (don't care)"]
def dc_row(k, what):				# one K-map row (A = k) of the 1 cells / the X cells, on SW3..SW0
    return lambda q, p: (krow([int(v == what) for v in p[0]], k, 3), 0xF)
W.append(Q(id="DCUSE", name="DCUSE", title="אילו לא אכפת הפכו ל-1?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], [7], None], variants=VU,
    tables=lambda p: [[int(v == 1) for v in p[0]], [int(v == 2) for v in p[0]]],
    answer=lambda p: (len(used_x(p)), 0x3),
    describe=lambda p: f"rows {''.join('01X'[v] for v in p[0])}; Y = {sop(dcf(p)[2])}; {len(used_x(p))} X used",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     X = LEDG1 (don't care)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח פונקציה של שלושה משתנים. בחלק מהמצבים לא אכפת מה היא נותנת.",
             "1. שימו מצב על שלושת המתגים:", DCLEG[0],
             "2. הנורה הימנית דולקת = 1. הנורה שלידה דולקת = לא אכפת.", DCLEG[1],
             "3. מלאו את השורה הראשונה של מפת קרנו:", "A = 0  (SW9 down)",
             "בכל תא שבו הנורה הימנית דולקת הרימו מתג:"] + ROW3, dc_row(0, 1)),
           (["עכשיו השורה השנייה: בכל תא שבו הנורה הימנית דולקת הרימו מתג.", "A = 1  (SW9 up)"] + DCLEG + ROW3,
            dc_row(1, 1)),
           (["עכשיו התאים של לא אכפת (הנורה השנייה דולקת), בשורה הראשונה:", "A = 0  (SW9 down)"] + DCLEG + ROW3,
            dc_row(0, 2)),
           (["והתאים של לא אכפת בשורה השנייה:", "A = 1  (SW9 up)"] + DCLEG + ROW3, dc_row(1, 2)),
           (["עגלו את ה-1 שבמפה בעיגולים גדולים ככל האפשר.",
             "תא של לא אכפת נכנס לעיגול רק אם הוא עוזר להגדיל אותו - ואז הוא נחשב 1. אחרת הוא נחשב 0.",
             "כמה תאים של לא אכפת נכנסו לעיגולים?", "0 = all down     1 = SW0     2 = SW1"],
            lambda q, p: (len(used_x(p)), 0x3))]))

# the delays from one input (the circuit of slide 17)
W.append(Q(id="PATHC", name="PATHC", title="השהיה מכניסה מסוימת", inputs=[9], flat=True,
    outs=hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=tvar(2),
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[2], 4) + bitsof(p[3], 4)),
    answer=lambda p: (p[0], 0x1F), describe=lambda p: f"C: max {p[2] + p[0]}, min {p[3] + p[1]}; D: max {p[0]}",
    B=["delays = HEX3..HEX0 (tpd AND, tcd AND, tpd OR, tcd OR)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["המעגל:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["הכניסה משתנה. אחרי כמה זמן לכל היותר היציאה מתייצבת?", "C -> Y:   max = ?"] + BIN5,
            lambda q, p: (p[2] + p[0], 0x1F)),
           (["המעגל:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["אחרי כמה זמן לכל הפחות היציאה יכולה להתחיל להשתנות?", "C -> Y:   min = ?"] + BIN5,
            lambda q, p: (p[3] + p[1], 0x1F)),
           (["המעגל:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["ומהכניסה הזו - אחרי כמה זמן לכל היותר?", "D -> Y:   max = ?"] + BIN5, lambda q, p: (p[0], 0x1F))]))

# where exactly the glitch happens
def glcell(p):					# the input values of the glitch, the glitch variable left out
    return sum((p[3][i] or 0) << (2 - i) for i in range(3) if i != p[0])
W.append(Q(id="GLITCHAT", name="GLITCHAT", title="איפה בדיוק קורה הגליץ'?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VG,
    tables=lambda p: [f_gl(p)], answer=lambda p: (glcell(p), 0x7 & ~(4 >> p[0])),
    describe=lambda p: f"Y = {expr(p[1])} + {expr(p[2])}; glitch on {'ABC'[p[0]]} when {expr(p[3])}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW2..SW0"], L=[], F=[],
    steps=ROWSTEPS3(f_gl) +
          [(["איזה משתנה מופיע בעיגול אחד רגיל ובשני עם קו?", "A = SW2     B = SW1     C = SW0"],
            lambda q, p: (4 >> p[0], 0x7)),
           (["הגליץ' קורה כשהמשתנה הזה משתנה, ושני המשתנים האחרים שומרים את היציאה 1 משני הצדדים.",
             "כתבו את הערכים של שני המשתנים האחרים (המתג של המשתנה שמשתנה - לא משנה):",
             "A -> SW2     B -> SW1     C -> SW0"], lambda q, p: (glcell(p), 0x7 & ~(4 >> p[0])))]))

# always_comb on 4-bit vectors (slide 27): y = a OP b with a hidden b
VOPS = ["AND", "OR", "XOR", "NAND", "NOR"]
def vop(o, a, b):
    return [a & b, a | b, a ^ b, ~(a & b), ~(a | b)][o] & 15
VV = [(o, b) for o in range(5) for b in range(1, 15)]
W.append(Q(id="VECOPS", name="VECOPS", title="פעולה על וקטור של 4 ביטים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VV,
    tables=lambda p: [[(vop(p[0], r, p[1]) >> k) & 1 for r in range(16)] for k in range(4)],
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"y = a {VOPS[p[0]]} b, b = {p[1]:04b}",
    B=["a[3:0] = SW9..SW6 (HEX0)     y[3:0] = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שורה אחת מהשקופית, על וקטורים של 4 ביטים:", "y = a OP b",
             "הפעולה והמספר השני מוסתרים. שימו", "a = 0000", "והעתיקו את היציאה:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, p: (vop(p[0], 0, p[1]), 0xF)),
           (["עכשיו", "a = 1111", "והעתיקו את היציאה:", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (vop(p[0], 15, p[1]), 0xF)),
           (["איזו פעולה זו? (כל ביט של היציאה הוא שער על אותו ביט של שני הוקטורים)",
             "AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2"], lambda q, p: (p[0], 0x7)),
           (["מה הוקטור המוסתר?", "b = ?", "SW3..SW0"], lambda q, p: (p[1], 0xF))]))

# a mux written with case (sel), in a hidden order
VM = list(itertools.permutations(range(4)))
INN = ["a = all down     b = SW0     c = SW1     d = SW1 + SW0"]
W.append(Q(id="CASEMUX", name="CASEMUX", title="בורר שכתוב עם case", inputs=[9, 8, 7, 6, 5, 4], flat=True,
    outs=[("G", 0)], hexes=[[9, 8], None, None, None], variants=VM,
    tables=lambda p: [[(r >> (3 - p[r >> 4])) & 1 for r in range(64)]], answer=lambda p: (p[2], 0x3),
    describe=lambda p: "; ".join(f"{s:02b}: y = {'abcd'[p[s]]}" for s in range(4)),
    B=["sel = SW9 SW8 (HEX3)     a b c d = SW7 SW6 SW5 SW4     y = LEDG0     answer: SW1..SW0"], L=[], F=[],
    steps=[(["בלוח:", "case (sel)  2'b00: y = ?;  2'b01: y = ?;  2'b10: y = ?;  default: y = ?;",
             "a = SW7     b = SW6     c = SW5     d = SW4     y = LEDG0",
             "שימו", "sel = 00  (SW9 SW8 down)", "הזיזו את מתגי הכניסות אחד אחד. אחרי איזו כניסה הנורה הולכת?"] + INN,
            lambda q, p: (p[0], 0x3)),
           (["עכשיו", "sel = 01  (SW8 up)", "אחרי איזו כניסה הנורה הולכת?"] + INN, lambda q, p: (p[1], 0x3)),
           (["עכשיו", "sel = 10  (SW9 up)", "אחרי איזו כניסה הנורה הולכת?"] + INN, lambda q, p: (p[2], 0x3))]))

# ================================================================ new questions (round 2; ids set below, in lesson order)
def onset(f):
    return frozenset(r for r in range(len(f)) if f[r] == 1)

# the minimal product of sums of 3 variables: circle the 0s
def sumlit(imp):				# a sum term: a variable fixed at 0 is written plain, fixed at 1 with a bar
    return litmask(tuple(None if v is None else 1 - v for v in imp))
def sexpr(imp):
    return "(" + " + ".join("ABC"[i] + ("'" if v else "") for i, v in enumerate(imp) if v is not None) + ")"
def goodpos():
    out = []
    for m in range(256):
        f = [m >> r & 1 for r in range(8)]
        off = frozenset(r for r in range(8) if not f[r])
        if not 3 <= len(off) <= 6:
            continue
        cv = covers(3, off)
        if len(cv) != 1 or len(cv[0]) < 2:
            continue
        for r in sorted(off):
            hit = [p for p in cv[0] if r in cells(p)]
            if len(hit) == 1:
                out.append((tuple(f), r, hit[0], len(cv[0])))
    return out
_gpos = goodpos()
VPOS = random.Random(61).sample(_gpos, min(256, len(_gpos)))
ZROW3 = lambda p, k: krow([1 - v for v in p[0]], k, 3)
W.append(Q(id="POS3", name="POS3", title="מכפלת סכומים מינימלית - עיגול של האפסים", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)] + CELL3, hexes=[None, None, None, None], variants=VPOS,
    tables=lambda p: [list(p[0])] + const(G.bits(p[1], 3), 3), answer=lambda p: (sumlit(p[2]), 0x3F),
    describe=lambda p: f"Y = {''.join(sexpr(c) for c in covers(3, frozenset(r for r in range(8) if not p[0][r]))[0])}; cell {p[1]:03b} -> {sexpr(p[2])}",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0   the cell = HEX2 HEX1 HEX0 (A B C)   answer: SW5..SW0"], L=[], F=[],
    steps=[(["בלוח פונקציה של שלושה משתנים. הפעם מחפשים את האפסים. השורה הראשונה של מפת קרנו:", "A = 0  (SW9 down)",
             "בכל תא שהנורה כבויה הרימו מתג:"] + ROW3, lambda q, p: (ZROW3(p, 0), 0xF)),
           (["עכשיו השורה השנייה:", "A = 1  (SW9 up)", "בכל תא שהנורה כבויה הרימו מתג:"] + ROW3,
            lambda q, p: (ZROW3(p, 1), 0xF)),
           (["עגלו את האפסים: עיגולים גדולים ככל האפשר, ומעט עיגולים ככל האפשר.",
             "כל עיגול הוא סכום, והפונקציה היא מכפלה של הסכומים. כמה עיגולים יש?"] + cnt(4), lambda q, p: (p[3], 0xF)),
           (["בתצוגה מוצג תא של 0:", "HEX2 HEX1 HEX0 = A B C",
             "כתבו את הסכום של העיגול שמכסה אותו: משתנה שקבוע 0 בעיגול נכתב רגיל, משתנה שקבוע 1 נכתב עם קו.",
             "הרימו מתג לכל ליטרל בסכום (גרש = משתנה עם קו):"] + LIT3, lambda q, p: (sumlit(p[2]), 0x3F))]))

# a 4-variable K-map that is exactly two circles of different sizes
def goodtwo():
    r2, out = random.Random(62), []
    pairs = [(a, b) for a in IMP4 for b in IMP4 if nlit(a) < nlit(b) and not cells(b) <= cells(a)]
    r2.shuffle(pairs)
    for a, b in pairs:
        on = cells(a) | cells(b)
        cv = covers(4, on)
        if len(cv) == 1 and set(cv[0]) == {a, b}:
            out.append((a, b))
            if len(out) == 256:
                break
    return out
VTWO = goodtwo()
f_two = lambda p: [int(r in cells(p[0]) or r in cells(p[1])) for r in range(16)]
W.append(Q(id="KMAP4TWO", name="KMAP4TWO", title="מפת קרנו של ארבעה משתנים - שני עיגולים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=VTWO,
    tables=lambda p: [f_two(p)], answer=lambda p: (litmask(p[1]) & 0xF, 0xF), describe=lambda p: f"Y = {expr(p[0])} + {expr(p[1])}",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח פונקציה של ארבעה משתנים. סכום המכפלות המינימלי שלה הוא שני עיגולים בגדלים שונים.",
             "1. נסו את 16 המצבים של ארבעת המתגים:", LEG4,
             "2. סמנו על דף מפת קרנו: תא לכל מצב שהנורה דולקת.", "Y = LEDG0",
             "3. בכמה מצבים הנורה דולקת? הרימו את המספר:"] + NUM15,
            lambda q, p: (sum(f_two(p)), 0xF)),
           (["עגלו את ה-1 שבמפה בשני עיגולים גדולים ככל האפשר (גם מעבר לקצוות ולפינות).",
             "כמה תאים יש בעיגול הגדול? הרימו את המספר:", "2 = SW1     4 = SW2     8 = SW3"],
            lambda q, p: (1 << (4 - nlit(p[0])), 0xF))] +
          litsteps4(["סכום המכפלות המינימלי הוא שני עיגולים בגדלים שונים.",
                     "העיגול הגדול = פחות ליטרלים."], lambda p: p[0], "המכפלה של העיגול הגדול") +
          litsteps4(["סכום המכפלות המינימלי הוא שני עיגולים בגדלים שונים.",
                     "העיגול הקטן = יותר ליטרלים."], lambda p: p[1], "המכפלה של העיגול הקטן")))

# prime and essential implicants of 4 variables
def goodp4(k):
    r4, out, seen = random.Random(63), [], set()
    while len(out) < k:
        m = r4.randrange(1 << 16)
        f = tuple(m >> r & 1 for r in range(16))
        on = onset(f)
        if f in seen or not 4 <= len(on) <= 9:
            continue
        seen.add(f)
        np_, ne = len(primes(4, on)), len(essential(4, on))
        if 2 <= np_ <= 8:
            out.append((f, np_, ne))
    return out
VP4 = goodp4(200)
W.append(Q(id="PRIMES4", name="PRIMES4", title="מכפלות ראשוניות וחיוניות - ארבעה משתנים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=VP4,
    tables=lambda p: [list(p[0])], answer=lambda p: (p[2], 0xF),
    describe=lambda p: f"primes: {sop(primes(4, onset(p[0])))}; essential {p[2]}",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=rowsteps4(lambda p: p[0], "בלוח פונקציה של ארבעה משתנים. מלאו את מפת קרנו, שורה אחרי שורה.") +
          [(["מכפלה ראשונית = עיגול הכי גדול שאפשר, שלא נכנס כולו בעיגול גדול יותר (גם מעבר לקצוות).",
             "כמה מכפלות ראשוניות יש לפונקציה?"] + cnt(8), lambda q, p: (p[1], 0xF)),
           (["מכפלה ראשונית חיונית = יש לה תא של 1 שאף מכפלה ראשונית אחרת לא מכסה.",
             "כמה מכפלות ראשוניות חיוניות יש?", "0 = all down"] + cnt(8), lambda q, p: (p[2], 0xF))]))

# a 4-variable K-map with don't cares
def gooddc4(k):
    r4, out, seen = random.Random(64), [], set()
    while len(out) < k:
        f = tuple(r4.choice((0, 0, 0, 1, 1, 2)) for _ in range(16))
        on = onset(f)
        dc = frozenset(r for r in range(16) if f[r] == 2)
        if f in seen or not (4 <= len(on) <= 8 and 2 <= len(dc) <= 4):
            continue
        seen.add(f)
        cv = covers(4, on, dc)
        if len(cv) != 1 or not 2 <= len(cv[0]) <= 4:
            continue
        c0 = covers(4, on)[0]
        if len(c0) + sum(map(nlit, c0)) == len(cv[0]) + sum(map(nlit, cv[0])):
            continue					# the X must help
        cand = [(r, [p for p in cv[0] if r in cells(p)]) for r in sorted(on)]
        cand = [(r, h[0]) for r, h in cand if len(h) == 1 and cells(h[0]) & dc]
        if cand:
            r, p = r4.choice(cand)
            out.append((f, r, p, len(cv[0])))
    return out
VD4 = gooddc4(200)
def dcrow(p, k):				# one row: the 1 cells on SW7..SW4, the X cells on SW3..SW0
    return (krow([int(v == 1) for v in p[0]], k, 4) << 4) | krow([int(v == 2) for v in p[0]], k, 4)
W.append(Q(id="DC4", name="DC4", title="מפת קרנו של ארבעה משתנים עם לא אכפת", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0), ("G", 1)] + CELL4, hexes=[None, None, None, None], variants=VD4,
    tables=lambda p: [[int(v == 1) for v in p[0]], [int(v == 2) for v in p[0]]] + const(G.bits(p[1], 4), 4),
    answer=lambda p: (litmask(p[2]) & 0xF, 0xF),
    describe=lambda p: f"rows {''.join('01X'[v] for v in p[0])}; Y = {sop(covers(4, onset(p[0]), frozenset(r for r in range(16) if p[0][r] == 2))[0])}; cell {p[1]:04b} -> {expr(p[2])}",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  X = LEDG1  the cell = HEX3..HEX0  answer: SW3..SW0"], L=[], F=[],
    steps=rowsteps4(lambda p: [int(v == 1) for v in p[0]],
                    "בלוח פונקציה של ארבעה משתנים עם לא אכפת. מלאו את המפה, שורה אחרי שורה.",
                    ["הנורה הימנית דולקת = 1. הנורה שלידה דולקת = לא אכפת.", "X = LEDG1 (don't care)",
                     "בכל שורה סמנו על הדף גם את התאים של לא אכפת. את התשובה נותנים רק על תאי ה-1."],
                    " הימנית") +
          [(["לא אכפת נכנס לעיגול רק אם הוא עוזר להגדיל אותו. כמה עיגולים יש בסכום המכפלות המינימלי?"] + cnt(4),
            lambda q, p: (p[3], 0xF))] +
          litsteps4(["בתצוגה מוצג תא של 1:", "HEX3 HEX2 HEX1 HEX0 = A B C D",
                     "מצאו את העיגול של סכום המכפלות המינימלי שמכסה אותו."], lambda p: p[2], "המכפלה של העיגול")))

# timing of a circuit where the short path depends on the delays
def tvar3():
    r, out = random.Random(65), set()
    while len(out) < 256:
        pa, po = r.randint(2, 9), r.randint(2, 9)
        ca, co = r.randint(1, pa - 1), r.randint(1, po - 1)
        if ca != co:
            out.add((pa, ca, po, co))
    return sorted(out)
CIRC3 = ["n1 = A OR B     n2 = n1 OR C     n3 = D AND E     Y = n2 AND n3"]
W.append(Q(id="TIMING3", name="TIMING3", title="איזה מסלול קצר?", inputs=[9], flat=True,
    outs=hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=tvar3(),
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[2], 4) + bitsof(p[3], 4)),
    answer=lambda p: (p[1] + min(p[1], p[3]), 0x1F),
    describe=lambda p: f"tpd = {2 * p[2] + p[0]}, short path from {'C' if p[3] < p[1] else 'D'}, tcd = {p[1] + min(p[1], p[3])}",
    B=["delays = HEX3..HEX0 (tpd AND, tcd AND, tpd OR, tcd OR)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["המעגל:"] + CIRC3 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["מה ההשהיה של המסלול הקריטי?", "tpd = ?"] + BIN5, lambda q, p: (2 * p[2] + p[0], 0x1F)),
           (["המעגל:"] + CIRC3 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["המסלול הקצר מתחיל באחת משתי כניסות. באיזו?", "C (through n2) = all down     D (through n3) = SW0"],
            lambda q, p: (int(p[1] < p[3]), 0x1)),
           (["המעגל:"] + CIRC3 + ["בתצוגה ההשהיות של השערים:"] + DELAYS +
            ["מה ההשהיה המינימלית של המעגל?", "tcd = ?"] + BIN5, lambda q, p: (p[1] + min(p[1], p[3]), 0x1F))]))

# a glitch in a 4-variable function: Y = x y + x' z w, fixed by y z w
def gl4_vars():
    out = []
    for x in range(4):
        o = [i for i in range(4) if i != x]
        for y in o:
            z, w = [i for i in o if i != y]
            for sx, py, pz, pw in itertools.product((0, 1), repeat=4):
                t1 = [None] * 4; t1[x] = sx; t1[y] = py
                t2 = [None] * 4; t2[x] = 1 - sx; t2[z] = pz; t2[w] = pw
                fix = [None] * 4; fix[y] = py; fix[z] = pz; fix[w] = pw
                out.append((x, tuple(t1), tuple(t2), tuple(fix)))
    return random.Random(66).sample(out, 192)
VG4 = gl4_vars()
f_gl4 = lambda p: [int(r in cells(p[1]) or r in cells(p[2])) for r in range(16)]
for _p in VG4:
    assert covers(4, onset(f_gl4(_p))) in ([(_p[1], _p[2])], [(_p[2], _p[1])]), _p
W.append(Q(id="GLITCH4", name="GLITCH4", title="גליץ' בפונקציה של ארבעה משתנים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=VG4,
    tables=lambda p: [f_gl4(p)], answer=lambda p: (litmask(p[3]) & 0xF, 0xF),
    describe=lambda p: f"Y = {expr(p[1])} + {expr(p[2])}; glitch on {'ABCD'[p[0]]}; fix {expr(p[3])}",
    B=["A = SW9     B = SW8     C = SW7     D = SW6     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=rowsteps4(f_gl4, "בלוח פונקציה של ארבעה משתנים. מלאו את מפת קרנו, שורה אחרי שורה.") +
          [(["בסכום המכפלות המינימלי שני עיגולים שנוגעים זה בזה. משתנה אחד מופיע בעיגול אחד רגיל ובשני עם קו.",
             "כשהוא משתנה, היציאה יכולה לקפוץ לרגע ל-0. איזה משתנה?", "A = SW3     B = SW2     C = SW1     D = SW0"],
            lambda q, p: (8 >> p[0], 0xF))] +
          litsteps4(["התיקון: עיגול נוסף שמכסה את התאים שבגבול בין שני העיגולים הנוגעים.",
                     "במכפלה שלו אין את המשתנה שגורם לגליץ'."], lambda p: p[3], "המכפלה של עיגול התיקון")))

# two segment wires swapped in the decoder of slide 28
def swapseg(p, d):
    i, j = p
    v = SEGS[d]
    bi, bj = v >> (6 - i) & 1, v >> (6 - j) & 1
    return v & ~((1 << (6 - i)) | (1 << (6 - j))) | (bj << (6 - i)) | (bi << (6 - j))
VS = [(i, j) for i in range(7) for j in range(i + 1, 7) if any(swapseg((i, j), d) != SEGS[d] for d in range(10))]
SEGL = ["a = all down   b = SW0   c = SW1   d = SW1+SW0   e = SW2   f = SW2+SW0   g = SW2+SW1"]
W.append(Q(id="SEGSWAP", name="SEGSWAP", title="שני חוטים מוחלפים במפענח", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(7)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VS,
    tables=lambda p: [[(swapseg(p, r) >> b) & 1 if r < 10 else 0 for r in range(16)] for b in range(7)],
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"segments {'abcdefg'[p[0]]} and {'abcdefg'[p[1]]} swapped",
    B=["data = SW9..SW6 (HEX0)     segments = LEDG6..LEDG0 (abc_defg)     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח המפענח של השקופית, אבל שני חוטים של מקטעים הוחלפו ביניהם.",
             "שימו ספרות והשוו לטבלה:", "data = SW9..SW6"] + LSEG + DRAW +
            ["איזה מקטע מוחלף? מבין השניים - זה שבא קודם בסדר:", "a b c d e f g"] + SEGL, lambda q, p: (p[0], 0x7)),
           (["ואיזה המקטע השני?"] + LSEG + DRAW + SEGL, lambda q, p: (p[1], 0x7))]))

# if / else if / else
IFV = ["0", "1", "c", "~c"]
def ifv(v, c):
    return [0, 1, c, 1 - c][v]
VIF = list(itertools.product(range(4), repeat=3))
IFL = ["y = 0 -> all down     y = 1 -> SW0     y = c -> SW1     y = ~c -> SW1+SW0"]
W.append(Q(id="IFCHAIN", name="IFCHAIN", title="if / else if / else", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VIF,
    tables=lambda p: [[ifv(p[0] if r >> 2 else p[1] if r >> 1 & 1 else p[2], r & 1) for r in range(8)]],
    answer=lambda p: (p[2], 0x3),
    describe=lambda p: f"if (a) y = {IFV[p[0]]}; else if (b) y = {IFV[p[1]]}; else y = {IFV[p[2]]};",
    B=["a = SW9     b = SW8     c = SW7     y = LEDG0     answer: SW1..SW0"], L=[], F=[],
    steps=[(["בלוח:", "always_comb  if (a) y = ?;  else if (b) y = ?;  else y = ?;",
             "a = SW9     b = SW8     c = SW7     y = LEDG0",
             "כל ענף כותב אחד מארבעה דברים. שימו", "a = 1  (SW9 up)", "והזיזו את שאר המתגים. מה כתוב בענף הראשון?"] + IFL,
            lambda q, p: (p[0], 0x3)),
           (["עכשיו", "a = 0     b = 1", "מה כתוב בענף השני?"] + IFL, lambda q, p: (p[1], 0x3)),
           (["ועכשיו", "a = 0     b = 0", "מה כתוב בענף האחרון?"] + IFL, lambda q, p: (p[2], 0x3))]))

# case (op) choosing an operation (a small ALU)
VALU = random.Random(67).sample(list(itertools.permutations(range(6), 4)), 256)
GATEL = ["AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"]
ABL = ["a b (SW7 SW6):   00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"]
W.append(Q(id="CASEALU", name="CASEALU", title="case שבוחר פעולה", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9, 8], None, [7], [6]], variants=VALU,
    tables=lambda p: [[GATES2[p[r >> 2]][1][r & 3] for r in range(16)]], answer=lambda p: (p[3], 0x7),
    describe=lambda p: "; ".join(f"{s:02b}: y = {GATES2[p[s]][0]}(a, b)" for s in range(4)),
    B=["op = SW9 SW8 (HEX3)     a = SW7     b = SW6     y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח:", "case (op)  2'b00: y = a OP b;  2'b01: y = a OP b;  2'b10: y = a OP b;  2'b11: y = a OP b;",
             "op = SW9 SW8     a = SW7     b = SW6     y = LEDG0", "בכל שורה שער אחר. שימו", "op = 00",
             "נסו את 4 המצבים, ולכל מצב שהנורה דלקה הרימו מתג:"] + ABL,
            lambda q, p: (sum(GATES2[p[0]][1][r] << r for r in range(4)), 0xF)),
           (["איזה שער בשורה של", "op = 00"] + GATEL, lambda q, p: (p[0], 0x7)),
           (["איזה שער בשורה של", "op = 01"] + GATEL, lambda q, p: (p[1], 0x7)),
           (["איזה שער בשורה של", "op = 10"] + GATEL, lambda q, p: (p[2], 0x7)),
           (["איזה שער בשורה של", "op = 11"] + GATEL, lambda q, p: (p[3], 0x7))]))

# a case with a missing line and no default: the output keeps its value (a latch)
ND = ["0", "1", "a", "~a"]
def ndrhs(p, s):				# p = (missing sel value, the rhs of the other 3 lines in sel order)
    return p[1][[v for v in range(4) if v != p[0]].index(s)]
def nodef(p, s, a):
    return HOLD if s == p[0] else [0, 1, a, 1 - a][ndrhs(p, s)]
def ndans(p, s):
    return 4 if s == p[0] else ndrhs(p, s)
VND = [(m, rhs) for m in range(4) for rhs in itertools.permutations(range(4), 3)]
NDL = ["y = 0 -> all down     y = 1 -> SW0     y = a -> SW1     y = ~a -> SW1+SW0"]
NDN = ["אין שורה (הנורה שומרת את הערך הקודם):", "SW2"]
W.append(Q(id="CASENODEF", name="CASENODEF", title="case בלי default", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)], hexes=[[9, 8], None, None, [7]], variants=VND,
    tables=lambda p: [[nodef(p, r >> 1, r & 1) for r in range(8)]], answer=lambda p: (ndans(p, 3), 0x7),
    describe=lambda p: "; ".join(f"{s:02b}: " + ("(no line)" if s == p[0] else f"y = {ND[ndrhs(p, s)]}") for s in range(4)),
    B=["sel = SW9 SW8 (HEX3)     a = SW7     y = LEDG0     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח:", "always_comb  case (sel)  ...  endcase",
             "בשלוש שורות כתוב אחד מאלה, ולערך אחד של", "sel", "אין שורה בכלל, ואין", "default",
             "שם הנורה לא משתנה ושומרת את הערך הקודם (נוצר תפס). כדי לזהות: הגיעו אליו פעם מנורה דולקת ופעם מכבויה.",
             "sel = SW9 SW8     a = SW7     y = LEDG0", "שימו", "sel = 00", "מה כתוב בשורה שלו?"] + NDL + NDN,
            lambda q, p: (ndans(p, 0), 0x7)),
           (["עכשיו", "sel = 01", "מה כתוב בשורה שלו?"] + NDL + NDN, lambda q, p: (ndans(p, 1), 0x7)),
           (["עכשיו", "sel = 10", "מה כתוב בשורה שלו?"] + NDL + NDN, lambda q, p: (ndans(p, 2), 0x7)),
           (["עכשיו", "sel = 11", "מה כתוב בשורה שלו?"] + NDL + NDN, lambda q, p: (ndans(p, 3), 0x7))]))

# ================================================================ easy questions from the slides (round 3; first in each topic)
# the 3-variable K-map examples of the slides (slide 3: A'B', slide 4: A'B + BC, slide 19: A'B' + BC), the slide's layout
SLIDEMAPS = [frozenset({0, 1}), frozenset({2, 3, 7}), frozenset({0, 1, 3, 7})]
def slide_cells(on, n, dc=frozenset()):		# (cell, its circle): the cells covered by exactly one circle of the minimal cover
    cv = covers(n, on, dc)[0]
    return [(r, [p for p in cv if r in cells(p)][0]) for r in sorted(on | dc) if sum(r in cells(p) for p in cv) == 1]
VKS = [(e, r, p) for e, on in enumerate(SLIDEMAPS) for r, p in slide_cells(on, 3)]
f_ks = lambda p: [int(r in SLIDEMAPS[p[0]]) for r in range(8)]
def srow3(f, c):				# a row of the slide's map (C = c), AB in the order 00 01 11 10, on SW3..SW0
    return sum(f[ab * 2 + c] << (3 - k) for k, ab in enumerate(KO))
ROWAB = ["AB:   00 -> SW3     01 -> SW2     11 -> SW1     10 -> SW0"]
KSL = "A = SW9     B = SW8     C = SW7     Y = LEDG0"
W.append(Q(id="KSLIDE3", name="KSLIDE3", title="מפת קרנו מהשקופיות - שלושה משתנים", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)] + CELL3, hexes=[None, None, None, None], variants=VKS,
    tables=lambda p: [f_ks(p)] + const(G.bits(p[1], 3), 3), answer=lambda p: (litmask(p[2]), 0x3F),
    describe=lambda p: f"slide map Y = {sop(covers(3, SLIDEMAPS[p[0]])[0])}; cell {p[1]:03b} -> {expr(p[2])}",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0   the cell = HEX2 HEX1 HEX0 (A B C)   answer: SW5..SW0"], L=[], F=[],
    steps=[(["בלוח אחת ממפות קרנו של שלושה משתנים מהשקופיות (שקופיות 3, 4, 19).",
             "המפה כמו בשקופית: העמודות לפי", "AB", "והשורות לפי", "C", KSL,
             "1. שימו", "C = 0  (SW7 down)",
             "2. נסו את 4 העמודות, ובכל תא שהנורה דולקת הרימו מתג:"] + ROWAB,
            lambda q, p: (srow3(f_ks(p), 0), 0xF)),
           (["עכשיו השורה השנייה של המפה:", KSL, "C = 1  (SW7 up)",
             "בכל תא שהנורה דולקת הרימו מתג:"] + ROWAB,
            lambda q, p: (srow3(f_ks(p), 1), 0xF)),
           (["עגלו את ה-1 כמו בשקופית. בתצוגה מוצג תא של 1:", "HEX2 HEX1 HEX0 = A B C",
             "כתבו את המכפלה של העיגול שמכסה אותו.", LITNOTE] + LIT3, lambda q, p: (litmask(p[2]), 0x3F))]))

# the 4-variable K-map of slide 8 (Y = A'C + A'BD + AB'C' + B'D'); a cell on the display
F8 = [1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
VK8 = slide_cells(onset(F8), 4)
W.append(Q(id="KSLIDE8", name="KSLIDE8", title="מפת קרנו של ארבעה משתנים מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 0)] + CELL4, hexes=[None, None, None, None], variants=VK8,
    tables=lambda p: [F8] + const(G.bits(p[0], 4), 4), answer=lambda p: (litmask(p[1]) & 0xF, 0xF),
    describe=lambda p: f"slide 8: Y = {sop(covers(4, onset(F8))[0])}; cell {p[0]:04b} -> {expr(p[1])}",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  the cell = HEX3..HEX0 (A B C D)  answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מפת קרנו של ארבעה משתנים מהשקופית (שקופית 8). בתצוגה מוצג תא אחד שלה:",
             "HEX3 HEX2 HEX1 HEX0 = A B C D", LEG4, "Y = LEDG0",
             "1. שימו את שני המתגים השמאליים כמו בתצוגה:", "SW9 SW8 = HEX3 HEX2  (A B)",
             "2. נסו את 4 המצבים של שני המתגים שלידם, ובכל תא שהנורה דולקת הרימו מתג:", "CD = SW7 SW6"] + ROW4,
            lambda q, p: (krow(F8, KO.index(p[0] >> 2), 4), 0xF))] +
          litsteps4(["עגלו את המפה כמו בשקופית. בתצוגה מוצג תא של 1:", "HEX3 HEX2 HEX1 HEX0 = A B C D",
                     "מצאו את העיגול שמכסה אותו."], lambda p: p[1], "המכפלה של העיגול")))

# the don't-care K-map of slide 12 (Y = A + B'D' + C); a cell (1 or X) on the display
F12 = [1, 0, 1, 1, 0, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]
DC12 = frozenset(r for r in range(16) if F12[r] == 2)
VD12 = slide_cells(onset(F12), 4, DC12)
W.append(Q(id="DCSLIDE", name="DCSLIDE", title="מפת קרנו עם לא אכפת מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 0), ("G", 1)] + CELL4, hexes=[None, None, None, None], variants=VD12,
    tables=lambda p: [[int(v == 1) for v in F12], [int(v == 2) for v in F12]] + const(G.bits(p[0], 4), 4),
    answer=lambda p: (litmask(p[1]) & 0xF, 0xF),
    describe=lambda p: f"slide 12: Y = {sop(covers(4, onset(F12), DC12)[0])}; cell {p[0]:04b} ({'01X'[F12[p[0]]]}) -> {expr(p[1])}",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  X = LEDG1  the cell = HEX3..HEX0  answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מפת קרנו עם לא אכפת מהשקופית (שקופית 12). בתצוגה מוצג תא אחד שלה:",
             "HEX3 HEX2 HEX1 HEX0 = A B C D", LEG4,
             "1. שימו את התא על המתגים.", "2. הנורה הימנית דולקת = 1. הנורה שלידה דולקת = לא אכפת.",
             "Y = LEDG0 (1)     X = LEDG1 (don't care)", "3. מה יש בתא?", "1 = SW0     X = SW1"],
            lambda q, p: (1 << (F12[p[0]] - 1), 0x3))] +
          litsteps4(["עגלו את המפה כמו בשקופית: לא אכפת נכנס לעיגול רק אם הוא עוזר.", "בתצוגה התא:",
                     "HEX3 HEX2 HEX1 HEX0 = A B C D", "מצאו את העיגול שמכסה אותו."], lambda p: p[1], "המכפלה של העיגול")))

# the critical path of the circuit of slide 17, gate by gate
VTS = [(a, o) for a in range(1, 6) for o in range(1, 10) if 2 * a + o <= 15]
DEL2 = ["HEX3 = tpd AND     HEX2 = tpd OR"]
TSL = ["המעגל של שקופית 17:"] + CIRC1 + ["בתצוגה ההשהיות של השערים:"] + DEL2
W.append(Q(id="TSLIDE", name="TSLIDE", title="המסלול הקריטי של השקופית, שער אחרי שער", inputs=[9], flat=True, small=True,
    outs=hexd(3) + hexd(2), hexes=[None, None, None, None], variants=VTS,
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4)),
    answer=lambda p: (2 * p[0] + p[1], 0xF), describe=lambda p: f"n1 {p[0]}, n2 {p[0] + p[1]}, tpd = {2 * p[0] + p[1]}",
    B=["delays = HEX3 HEX2 (tpd AND, tpd OR)     answer: SW3..SW0"], L=[], F=[],
    steps=[(TSL + ["1. הכניסה משתנה. אחרי כמה זמן לכל היותר מתייצב", "n1 = ?"] + NUM15,
            lambda q, p: (p[0], 0xF)),
           (TSL + ["2. ואחרי כמה זמן לכל היותר מתייצב", "n2 = ?"] + NUM15, lambda q, p: (p[0] + p[1], 0xF)),
           (TSL + ["3. וההשהיה של כל המעגל (המסלול הקריטי):", "Y:   tpd = ?"] + NUM15,
            lambda q, p: (2 * p[0] + p[1], 0xF))]))

# the glitch circuit of slides 19-21: n1 = A'B', n2 = BC, Y = n1 + n2; flip B from the inputs on the display
def glsl(r):					# (n1, n2) of the slide's circuit, r = A B C
    a, b, c = G.bits(r, 3)
    return (1 - a) & (1 - b), b & c
GLS = ["n1 = A'B'     n2 = BC     Y = n1 + n2", "A = SW9   B = SW8   C = SW7   n1 = LEDG1   n2 = LEDG0"]
glyes = lambda r: int(r >> 2 == 0 and r & 1 == 1)
W.append(Q(id="GLSLIDE", name="GLSLIDE", title="מעגל הגליץ' מהשקופית", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0), ("G", 1)] + CELL3, hexes=[None, None, None, None], variants=list(range(8)),
    tables=lambda r: [[glsl(x)[1] for x in range(8)], [glsl(x)[0] for x in range(8)]] + const(G.bits(r, 3), 3),
    answer=lambda r: (glyes(r), 0x1),
    describe=lambda r: f"inputs {r:03b}: n1 n2 {glsl(r)} -> {glsl(r ^ 2)}; glitch {glyes(r)}",
    B=["A = SW9   B = SW8   C = SW7   n1 = LEDG1   n2 = LEDG0   inputs = HEX2 HEX1 HEX0   answer: SW1..SW0"], L=[], F=[],
    steps=[(["בלוח מעגל הגליץ' מהשקופיות (שקופיות 19-21):"] + GLS +
            ["1. שימו על המתגים את הכניסות שבתצוגה:", "HEX2 HEX1 HEX0 = A B C",
             "2. העתיקו את היציאות של שני שערי וגם:", "SW1 SW0 = LEDG1 LEDG0  (n1 n2)"],
            lambda q, r: (glsl(r)[0] << 1 | glsl(r)[1], 0x3)),
           (["מהכניסות שבתצוגה הפכו רק את הכניסה הזו (כמו בשקופית):", "B = SW8", "HEX2 HEX1 HEX0 = A B C"] + GLS +
            ["העתיקו שוב:", "SW1 SW0 = LEDG1 LEDG0  (n1 n2)"],
            lambda q, r: (glsl(r ^ 2)[0] << 1 | glsl(r ^ 2)[1], 0x3)),
           (["גליץ' יכול לקרות כשיציאה אחת עולה מ-0 ל-1 והשנייה יורדת מ-1 ל-0, והיציאה צריכה להישאר 1.",
             GLS[1], "שימו את הכניסות שבתצוגה, והפכו הלוך ושוב את", "B = SW8", "HEX2 HEX1 HEX0 = A B C",
             "יכול לקרות כאן גליץ'?", "no = all down     yes = SW0"],
            lambda q, r: (glyes(r), 0x1))]))

# the sevenseg decoder of slide 28: write the line of the digit on the display
W.append(Q(id="SEGSLIDE", name="SEGSLIDE", title="שורה של המפענח מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(7)] + hexd(3), hexes=[None, None, None, None], variants=list(range(10)),
    tables=lambda d: [[(SEGS[r] >> b) & 1 if r < 10 else 0 for r in range(16)] for b in range(7)] + const(bitsof(d, 4), 4),
    answer=lambda d: (SEGS[d] & 0xF, 0xF), describe=lambda d: f"digit {d}: 7'b{SEGS[d] >> 4:03b}_{SEGS[d] & 15:04b}",
    B=["data = SW9..SW6     digit = HEX3     segments = LEDG6..LEDG0 (abc_defg)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המפענח של תצוגת 7 מקטעים מהשקופית (שקופית 28):", "case (data)   segments = 7'b abc_defg",
             "1. שימו על המתגים את הספרה שבתצוגה:", "data = SW9 SW8 SW7 SW6     digit = HEX3",
             "2. כתבו את תחילת השורה שלה. לכל מקטע דולק הרימו מתג:",
             "a = LEDG6 -> SW2     b = LEDG5 -> SW1     c = LEDG4 -> SW0"],
            lambda q, d: (SEGS[d] >> 4, 0x7)),
           (["עכשיו שאר השורה של אותה ספרה. לכל מקטע דולק הרימו מתג:", "data = SW9 SW8 SW7 SW6     digit = HEX3",
             "d = LEDG3 -> SW3     e = LEDG2 -> SW2     f = LEDG1 -> SW1     g = LEDG0 -> SW0"],
            lambda q, d: (SEGS[d] & 0xF, 0xF))]))

# the priority_casez of slide 30: which line matches the input on the display
SLPRIO = [3, 2, 1, 0]
def zline(a):					# the casez line that matches: 0 = 1???, 1 = 01??, 2 = 001?, 3 = 0001, 4 = default
    return next((k for k, b in enumerate(SLPRIO) if a >> b & 1), 4)
W.append(Q(id="PRIOSLIDE", name="PRIOSLIDE", title="מקודד העדיפות מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + CELL4, hexes=[None, None, None, None], variants=list(range(16)),
    tables=lambda a: [[(prio(SLPRIO, r) >> b) & 1 for r in range(16)] for b in range(4)] + const(G.bits(a, 4), 4),
    answer=lambda a: (zline(a), 0x7), describe=lambda a: f"a = {a:04b}: y = {prio(SLPRIO, a):04b}, line {zline(a)}",
    B=["a[3:0] = SW9..SW6     y[3:0] = LEDG3..LEDG0     input = HEX3..HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מקודד העדיפות מהשקופית (שקופית 30), בדיוק כמו בקוד:", "casez (a)",
             "1. שימו על המתגים את הקלט שבתצוגה:", "HEX3 HEX2 HEX1 HEX0 = a[3] a[2] a[1] a[0]", "a[3:0] = SW9 SW8 SW7 SW6",
             "2. העתיקו את היציאה:", "SW3..SW0 = LEDG3..LEDG0  (y)"], lambda q, a: (prio(SLPRIO, a), 0xF)),
           (["איזו שורה של", "casez (a)", "התאימה לקלט שבתצוגה?", "HEX3 HEX2 HEX1 HEX0 = a[3] a[2] a[1] a[0]",
             "4'b1??? = all down     4'b01?? = SW0     4'b001? = SW1", "4'b0001 = SW1+SW0     default = SW2"],
            lambda q, a: (zline(a), 0x7))]))

# ================================================================ easy questions from the slides (round 4; after the round-3 ones)
# slide 5: an implicant of all three variables (like ABC) lights one cell
W.append(Q(id="KMINT", name="KMINT", title="מכפלה של שלושה משתנים מהשקופית", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(8)),
    tables=lambda r: [[int(x == r) for x in range(8)]], answer=lambda r: (litmask(tuple(G.bits(r, 3))), 0x3F),
    describe=lambda r: f"Y = {expr(tuple(G.bits(r, 3)))}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW5..SW0"], L=[], F=[],
    steps=[(["שקופית 5: מכפלה של שלושת המשתנים, כמו", "ABC",
             "דולקת בתא אחד בלבד. בלוח מכפלה כזו, וחלק מהמשתנים בה עם קו.", KSL,
             "1. נסו את 8 המצבים. באיזה מצב הנורה דולקת? הרימו אותו:", "A -> SW2     B -> SW1     C -> SW0"],
            lambda q, r: (r, 0x7)),
           (["2. כתבו את המכפלה: משתנה שהוא 0 בתא הזה נכתב עם קו, משתנה שהוא 1 נכתב רגיל.", KSL, LITNOTE] + LIT3,
            lambda q, r: (litmask(tuple(G.bits(r, 3))), 0x3F))]))

# slide 2: PA + PA' = P - two neighbouring cells become one product
IMPP = [p for p in itertools.product((1, 0, None), repeat=3) if nlit(p) == 2]
VCOMB = [(p, r) for p in IMPP for r in sorted(cells(p))]
W.append(Q(id="KCOMB", name="KCOMB", title="שני תאים שכנים הופכים למכפלה אחת", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)] + CELL3, hexes=[None, None, None, None], variants=VCOMB,
    tables=lambda p: [f_imp(p[0])] + const(G.bits(p[1], 3), 3), answer=lambda p: (litmask(p[0]), 0x3F),
    describe=lambda p: f"Y = {expr(p[0])}, shown cell {p[1]:03b}",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0   a cell = HEX2 HEX1 HEX0 (A B C)   answer: SW5..SW0"], L=[], F=[],
    steps=[(["שקופית 2:", "PA + PA' = P",
             "בלוח פונקציה של שלושה משתנים שדולקת בשני תאים שכנים בלבד. בתצוגה אחד מהם:",
             "HEX2 HEX1 HEX0 = A B C", KSL,
             "1. שימו את התא על המתגים, והפכו כל פעם מתג אחד.",
             "2. איזה משתנה אפשר להפוך והנורה נשארת דולקת? הוא מתבטל, כמו בשקופית:",
             "A = SW2     B = SW1     C = SW0"],
            lambda q, p: (sum(4 >> i for i in range(3) if p[0][i] is None), 0x7)),
           (["שקופית 2:", "PA + PA' = P", "מה שנשאר משני התאים הוא", "P",
             "התא שבתצוגה:", "HEX2 HEX1 HEX0 = A B C", LITNOTE] + LIT3, lambda q, p: (litmask(p[0]), 0x3F))]))

# slide 4 (Y = A'B + BC) with one cell flipped
ON4 = SLIDEMAPS[1]
f_k4 = lambda r: [int(x in ON4) ^ int(x == r) for x in range(8)]
W.append(Q(id="KFIX4", name="KFIX4", title="תא הפוך במפה של השקופית", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(8)),
    tables=lambda r: [f_k4(r)], answer=lambda r: (r, 0x7), describe=lambda r: f"slide 4, cell {r:03b} flipped",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המפה של שקופית 4, אבל תא אחד בה הפוך:", "Y = A'B + BC", KSL,
             "1. נסו את 8 המצבים. בכמה מצבים הנורה דולקת?"] + cnt(5), lambda q, r: (sum(f_k4(r)), 0xF)),
           (["2. באיזה מצב הנורה לא כמו בביטוי של השקופית? הרימו אותו:", "Y = A'B + BC", KSL,
             "A -> SW2     B -> SW1     C -> SW0"], lambda q, r: (r, 0x7))]))

# slides 7-8: the order of the rows and the columns of a 4-variable K-map
VGR = [(a, c) for a in range(4) for c in range(4)]
GRL = ["HEX3 = row (AB)     HEX2 = column (CD)"]
W.append(Q(id="KGRAY8", name="KGRAY8", title="שורה ועמודה במפה של ארבעה משתנים", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 0)] + hexd(3) + hexd(2), hexes=[None, None, None, None], variants=VGR,
    tables=lambda p: [F8] + const(bitsof(p[0] + 1, 4) + bitsof(p[1] + 1, 4), 4),
    answer=lambda p: (F8[KO[p[0]] * 4 + KO[p[1]]], 0x1),
    describe=lambda p: f"row {p[0] + 1} col {p[1] + 1}: ABCD = {KO[p[0]]:02b}{KO[p[1]]:02b}, Y = {F8[KO[p[0]] * 4 + KO[p[1]]]}",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  row = HEX3  column = HEX2  answer: SW1..SW0"], L=[], F=[],
    steps=[(["מפת קרנו של ארבעה משתנים כמו בשקופיות 7-8. השורות לפי", "AB", "והעמודות לפי", "CD",
             "בסדר:", "00 01 11 10", "בתצוגה מספר של שורה ומספר של עמודה (1 עד 4):"] + GRL +
            ["1. מה הערכים של שני המשתנים בשורה הזו?", "A -> SW1     B -> SW0"],
            lambda q, p: (KO[p[0]], 0x3)),
           (["2. ומה הערכים של שני המשתנים בעמודה?", "00 01 11 10"] + GRL + ["C -> SW1     D -> SW0"],
            lambda q, p: (KO[p[1]], 0x3)),
           (["3. בלוח המפה של שקופית 8. שימו את התא על המתגים. מה יש בו?"] + GRL +
            [LEG4, "Y = LEDG0", "0 = all down     1 = SW0"],
            lambda q, p: (F8[KO[p[0]] * 4 + KO[p[1]]], 0x1))]))

# slides 11-12: the don't cares of one row, and how many of them the slide's circles use
F12X = [int(v == 2) for v in F12]
def used12(ab):					# the X cells of row AB inside the circles of Y = A + B'D' + C
    cv = covers(4, onset(F12), DC12)[0]
    return sum(1 for c in range(4) if F12X[ab * 4 + c] and any(ab * 4 + c in cells(p) for p in cv))
W.append(Q(id="DCROW12", name="DCROW12", title="לא אכפת בשורה של המפה מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 0), ("G", 1)] + hexd(3) + hexd(2), hexes=[None, None, None, None], variants=list(range(4)),
    tables=lambda ab: [[int(v == 1) for v in F12], F12X] + const([ab >> 1, 0, 0, 0] + [ab & 1, 0, 0, 0], 4),
    answer=lambda ab: (used12(ab), 0x7), describe=lambda ab: f"slide 12, row AB = {ab:02b}: {used12(ab)} X used",
    B=["A = SW9  B = SW8  C = SW7  D = SW6  Y = LEDG0  X = LEDG1  row = HEX3 HEX2 (A B)  answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מפת קרנו עם לא אכפת של שקופיות 11-12.", LEG4, "Y = LEDG0 (1)     X = LEDG1 (don't care)",
             "1. שימו את השורה שבתצוגה:", "SW9 SW8 = HEX3 HEX2  (A B)",
             "2. נסו את 4 העמודות. בכל תא של לא אכפת (הנורה השנייה דולקת) הרימו מתג:"] + ROW4,
            lambda q, ab: (krow(F12X, KO.index(ab), 4), 0xF)),
           (["העיגולים של שקופית 12:", "Y = A + B'D' + C", "השורה:", "SW9 SW8 = HEX3 HEX2  (A B)",
             "כמה מתאי הלא אכפת של השורה הזו נכנסו לעיגולים?", "0 = all down"] + cnt(4),
            lambda q, ab: (used12(ab), 0x7))]))

# slides 15, 17: the short path of the slide's circuit
DELC = ["HEX3 = tcd AND     HEX2 = tcd OR", "tcd = min"]
TCL = ["המעגל של שקופית 17:"] + CIRC1 + ["בתצוגה ההשהיות המינימליות של השערים (שקופית 15):"] + DELC
W.append(Q(id="TCDSLIDE", name="TCDSLIDE", title="המסלול הקצר של השקופית", inputs=[9], flat=True, small=True,
    outs=hexd(3) + hexd(2), hexes=[None, None, None, None], variants=VTS,
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4)),
    answer=lambda p: (p[0], 0xF), describe=lambda p: f"A -> Y min {2 * p[0] + p[1]}, tcd = {p[0]}",
    B=["delays = HEX3 HEX2 (tcd AND, tcd OR)     answer: SW3..SW0"], L=[], F=[],
    steps=[(TCL + ["1. הכניסה משתנה. אחרי כמה זמן לכל הפחות היציאה יכולה להתחיל להשתנות?", "A -> Y:   min = ?"] + NUM15,
            lambda q, p: (2 * p[0] + p[1], 0xF)),
           (TCL + ["2. ומהכניסה הזו (רק דרך השער האחרון)? זו ההשהיה המינימלית של כל המעגל.", "D -> Y:   min = ?"] + NUM15,
            lambda q, p: (p[0], 0xF))]))

# slide 21: the fixed glitch circuit, n3 = A'C
def glfx(r):
    a, b, c = G.bits(r, 3)
    return (1 - a) & (1 - b), b & c, (1 - a) & c
def glfx3(r):					# n1 n2 n3 as SW2 SW1 SW0
    n1, n2, n3 = glfx(r)
    return n1 << 2 | n2 << 1 | n3
GLF = ["n1 = A'B'     n2 = BC     n3 = A'C     Y = n1 + n2 + n3",
       "A = SW9   B = SW8   C = SW7   n1 = LEDG2   n2 = LEDG1   n3 = LEDG0"]
W.append(Q(id="GLFIX", name="GLFIX", title="המעגל המתוקן מהשקופית", inputs=[9, 8, 7], flat=True, small=True,
    outs=[("G", 0), ("G", 1), ("G", 2)] + CELL3, hexes=[None, None, None, None], variants=list(range(8)),
    tables=lambda r: [[glfx(x)[k] for x in range(8)] for k in (2, 1, 0)] + const(G.bits(r, 3), 3),
    answer=lambda r: (glfx3(r ^ 2), 0x7),
    describe=lambda r: f"inputs {r:03b}: n1 n2 n3 {glfx3(r):03b} -> {glfx3(r ^ 2):03b}",
    B=["A = SW9   B = SW8   C = SW7   n1 n2 n3 = LEDG2..LEDG0   inputs = HEX2 HEX1 HEX0   answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח המעגל המתוקן של שקופית 21 (נוסף שער וגם שלישי):"] + GLF +
            ["1. שימו על המתגים את הכניסות שבתצוגה:", "HEX2 HEX1 HEX0 = A B C",
             "2. העתיקו את היציאות של שלושת שערי וגם:", "SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0  (n1 n2 n3)"],
            lambda q, r: (glfx3(r), 0x7)),
           (["מהכניסות שבתצוגה הפכו רק את הכניסה הזו (כמו בשקופית):", "B = SW8", "HEX2 HEX1 HEX0 = A B C"] + GLF +
            ["העתיקו שוב:", "SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0  (n1 n2 n3)"],
            lambda q, r: (glfx3(r ^ 2), 0x7))]))

# slides 19-20: the timing of the glitch (B falls, A = 0, C = 1)
VGT = [(n, a, o) for n in range(1, 6) for a in range(1, 6) for o in range(1, 6)]
GTL = ["מעגל הגליץ' של שקופיות 19-20:", "B' = NOT B     n1 = A' AND B'     n2 = B AND C     Y = n1 OR n2",
       "בתצוגה ההשהיות של השערים:", "HEX3 = tpd NOT     HEX2 = tpd AND     HEX1 = tpd OR",
       "כמו בשקופית:", "A = 0     C = 1     B falls at t = 0"]
W.append(Q(id="GLTIME", name="GLTIME", title="כמה זמן נמשך הגליץ' של השקופית?", inputs=[9], flat=True, small=True,
    outs=hexd(3) + hexd(2) + hexd(1), hexes=[None, None, None, None], variants=VGT,
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[2], 4)),
    answer=lambda p: (p[0], 0xF), describe=lambda p: f"n2 falls {p[1]}, n1 rises {p[0] + p[1]}, glitch {p[0]}",
    B=["delays = HEX3 HEX2 HEX1 (tpd NOT, tpd AND, tpd OR)     answer: SW3..SW0"], L=[], F=[],
    steps=[(GTL + ["1. מתי היציאה של השער הזה יורדת ל-0?", "n2 falls at t = ?"] + NUM15, lambda q, p: (p[1], 0xF)),
           (GTL + ["2. מתי היציאה של השער הזה עולה ל-1? (קודם צריכה לעלות היציאה של שער ההיפוך)", "n1 rises at t = ?"] + NUM15,
            lambda q, p: (p[0] + p[1], 0xF)),
           (GTL + ["3. בין שני הרגעים האלה שתי הכניסות של שער או הן 0. כמה זמן היציאה ב-0 (אורך הגליץ')?",
                   "Y = 0 for ? time units"] + NUM15, lambda q, p: (p[0], 0xF))]))

# slide 27: the module gates (y1 = a & b, y3 = a ^ b), a and b on the display
VG27 = random.Random(68).sample([(a, b) for a in range(10) for b in range(10)], 100)
BIN10 = ["0 = 0000   1 = 0001   2 = 0010   3 = 0011   4 = 0100", "5 = 0101   6 = 0110   7 = 0111   8 = 1000   9 = 1001"]
G27 = ["y1 = a & b     y3 = a ^ b", "a[3:0] = SW9..SW6 (HEX0)     b = HEX3     the number for a = HEX2",
       "y1 = LEDG7..LEDG4     y3 = LEDG3..LEDG0"]
W.append(Q(id="GATES27", name="GATES27", title="המודול gates מהשקופית", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VG27,
    tables=lambda p: [[((r ^ p[1]) >> k) & 1 for r in range(16)] for k in range(4)] +
                     [[((r & p[1]) >> k) & 1 for r in range(16)] for k in range(4)] + const(bitsof(p[1], 4) + bitsof(p[0], 4), 4),
    answer=lambda p: (p[0] ^ p[1], 0xF), describe=lambda p: f"a = {p[0]:04b}, b = {p[1]:04b}: y1 {p[0] & p[1]:04b}, y3 {p[0] ^ p[1]:04b}",
    B=["a = SW9..SW6 (HEX0)     b = HEX3     a to set = HEX2     y1 = LEDG7..4     y3 = LEDG3..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המודול של שקופית 27 (שתי יציאות מתוכו):"] + G27 +
            ["1. שימו על המתגים את המספר שבתצוגה (בדקו בתצוגה הימנית):", "a = HEX2"] + BIN10 +
            ["2. העתיקו את היציאה הראשונה:", "SW3..SW0 = LEDG7..LEDG4  (y1 = a AND b)"],
            lambda q, p: (p[0] & p[1], 0xF)),
           (["עכשיו היציאה השנייה, עם אותו קלט:"] + G27 + ["a = HEX2", "SW3..SW0 = LEDG3..LEDG0  (y3 = a XOR b)"],
            lambda q, p: (p[0] ^ p[1], 0xF))]))

# slides 28-29: the sevenseg decoder without its default line - the output keeps its value (a latch)
W.append(Q(id="NODEF28", name="NODEF28", title="המפענח מהשקופית בלי default", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(7)] + hexd(3), hexes=[None, None, None, None], variants=list(range(2, 8)),
    tables=lambda d: [[(SEGS[r] >> b) & 1 if r < 10 else HOLD for r in range(16)] for b in range(7)] + const(bitsof(d, 4), 4),
    answer=lambda d: (SEGS[d] & 0xF, 0xF), describe=lambda d: f"digit {d}, kept 7'b{SEGS[d] >> 4:03b}_{SEGS[d] & 15:04b}",
    B=["data = SW9..SW6     digit = HEX3     segments = LEDG6..LEDG0 (abc_defg)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המפענח של שקופית 28, אבל בלי השורה:", "default: segments = 7'b000_0000;",
             "data = SW9 SW8 SW7 SW6     digit = HEX3", "segments = LEDG6..LEDG0  (abc_defg)",
             "1. שימו על המתגים את הספרה שבתצוגה. כמה מקטעים דולקים?"] + cnt(7),
            lambda q, d: (bin(SEGS[d]).count("1"), 0x7)),
           (["2. עכשיו הרימו רק את המתג הזה (הקלט גדול מ-9, ואין לו שורה):", "SW9",
             "שקופית 29: בלי שורה לקלט, היציאה שומרת את הערך הקודם (תפס). העתיקו את סוף היציאה:",
             "data = SW9 SW8 SW7 SW6     digit = HEX3",
             "d = LEDG3 -> SW3     e = LEDG2 -> SW2     f = LEDG1 -> SW1     g = LEDG0 -> SW0"],
            lambda q, d: (SEGS[d] & 0xF, 0xF))]))

# slide 30: which inputs give the output on the display (a line of casez and its ? bits)
VPR = [8, 4, 2, 1, 0]
def prfix(y):					# (the fixed bits of the casez line of y, their mask)
    return (y, 0xF) if y == 0 else (y, (0xF << (y.bit_length() - 1)) & 0xF)
W.append(Q(id="PRIOROW", name="PRIOROW", title="אילו קלטים נותנים את היציאה?", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + CELL4, hexes=[None, None, None, None], variants=VPR,
    tables=lambda y: [[(prio(SLPRIO, r) >> b) & 1 for r in range(16)] for b in range(4)] + const(G.bits(y, 4), 4),
    answer=lambda y: (max(y, 1), 0xF), describe=lambda y: f"y = {y:04b}: {max(y, 1)} inputs",
    B=["a[3:0] = SW9..SW6     y[3:0] = LEDG3..LEDG0     y wanted = HEX3..HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מקודד העדיפות של שקופית 30:", "casez (a)",
             "a[3:0] = SW9 SW8 SW7 SW6     y[3:0] = LEDG3..LEDG0", "בתצוגה יציאה אחת:",
             "HEX3 HEX2 HEX1 HEX0 = y[3] y[2] y[1] y[0]",
             "1. מצאו קלט שנותן את היציאה הזו, והעתיקו אותו:", "SW3..SW0 = SW9..SW6"],
            lambda q, y: prfix(y)),
           (["2. כמה קלטים שונים נותנים את היציאה הזו? (סימן שאלה בשורה = כל ערך)",
             "a[3:0] = SW9 SW8 SW7 SW6     y[3:0] = LEDG3..LEDG0", "HEX3 HEX2 HEX1 HEX0 = y[3] y[2] y[1] y[0]",
             "1 = SW0     2 = SW1     4 = SW2     8 = SW3"], lambda q, y: (max(y, 1), 0xF))]))

# slide 30, the synthesis picture: one bit of y is one AND gate; which inputs enter it with a bubble
W.append(Q(id="PRIOSYN", name="PRIOSYN", title="הסינתזה של מקודד העדיפות", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=list(range(4)),
    tables=lambda k: [[(prio(SLPRIO, r) >> k) & 1 for r in range(16)]], answer=lambda k: ((0xF << (k + 1)) & 0xF, 0xF),
    describe=lambda k: f"y[{k}]: a[{k}] plain, bubbles {(0xF << (k + 1)) & 0xF:04b}",
    B=["a[3:0] = SW9..SW6     y[?] = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["שקופית 30: בסינתזה של מקודד העדיפות כל ביט של היציאה הוא שער וגם (או חוט ישר).",
             "בלוח ביט אחד מוסתר של היציאה:", "a[3:0] = SW9 SW8 SW7 SW6     y[?] = LEDG0",
             "1. איזו כניסה נכנסת לשער ישר (בלי עיגול)? בלעדיה הנורה לא נדלקת אף פעם.",
             "a[3] -> SW3     a[2] -> SW2     a[1] -> SW1     a[0] -> SW0"], lambda q, k: (1 << k, 0xF)),
           (["2. אילו כניסות נכנסות לשער עם עיגול (כשאחת מהן 1, הנורה כבויה)? הרימו מתג לכל אחת:",
             "a[3:0] = SW9 SW8 SW7 SW6     y[?] = LEDG0",
             "a[3] -> SW3     a[2] -> SW2     a[1] -> SW1     a[0] -> SW0", "none = all down"],
            lambda q, k: ((0xF << (k + 1)) & 0xF, 0xF))]))

ORDER = ["KSLIDE3", "KSLIDE8", "KMINT", "KCOMB", "KFIX4", "KGRAY8",
         "KMAP2", "KMAP3A", "KMAP3", "PRIMES", "POS3", "KMAP4A", "KMAP4TWO", "KMAP4", "PRIMES4",
         "DCSLIDE", "TSLIDE", "GLSLIDE", "DCROW12", "TCDSLIDE", "GLFIX", "GLTIME",
         "DC3", "DCUSE", "SEGX", "DC4", "TIMING", "PATHC", "TIMING2", "TIMING3", "GLITCH", "GLITCHAT", "GLITCH4",
         "SEGSLIDE", "PRIOSLIDE", "GATES27", "NODEF28", "PRIOROW", "PRIOSYN", "SEGREAD", "SEGSWAP", "IFELSE", "IFCHAIN", "VECOPS", "CASEMUX", "CASEALU", "CASEBUG", "CASENODEF",
         "CASEZ", "CASEZQ"]
_by = {q.name: q for q in W}
assert sorted(_by) == sorted(ORDER)
W = [_by[n] for n in ORDER]
for i, q in enumerate(W):
    q.id = f"Q{i + 1:02d}"

for q in W:
    q.ns = len(q.steps) + 1
    for lines, _ in q.steps:
        for l in lines:
            he = any("\u0590" <= c <= "\u05ff" for c in l)
            lat = any(c.isascii() and c.isalpha() for c in l)
            assert not (he and lat), (q.name, l)
G.QS = W
G.QBY = {q.id: q for q in W}

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--id")
    ap.add_argument("--nosim", action="store_true")
    ap.add_argument("--answers", default="316009489")
    a = ap.parse_args()
    if a.id:
        G.show_id(a.id); sys.exit(0)
    for q in W:
        G.check_question(q)
    sel = [G.QBY[a.only]] if a.only else W
    bad = []
    for q in sel:
        d = G.build(q)
        print(f"{q.id} {q.name}: {len(q.variants)} variants, {q.ns} steps")
        if not a.nosim and not G.simulate(q, d):
            bad.append(q.id); continue
        if a.compile and not G.compile_q(q, d):
            bad.append(q.id)
    G.write(f"{G.REPO}/questions.txt", G.questions_txt())
    G.write(f"{G.REPO}/QUESTIONS.md", G.questions_md())
    G.write(f"{HERE}/QUESTIONS_ANSWERS.md", G.questions_md(a.answers))
    os.makedirs(f"{HERE}/instructor_guide", exist_ok=True)
    G.write(f"{HERE}/instructor_guide/guide.html", G.answers_guide(a.answers))
    print("FAILED: " + " ".join(bad) if bad else "all OK")
    sys.exit(1 if bad else 0)
