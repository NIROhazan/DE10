# -*- coding: utf-8 -*-
# Week 7 class exercise (lecture 7, Harris 3.4.3-3.4.5: the snail - Moore vs Mealy, state / output tables, timing;
# factored FSMs - the traffic light with a parade mode; FSM design problems). Instructor only.
#   python gen_w7.py [--compile] [--only Q05] [--id <ID>]
# No clock: only one board button (KEY2, the check button) is used. Every FSM question puts the COMBINATIONAL part of a
# hidden FSM on the board: the current state and the inputs on switches, the next state and the outputs on LEDs / HEX.
# The student reconstructs the tables, and follows a machine step by step by copying the next state to the state switches.
import itertools, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(7, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, BIN5, UP0, binl
W = []
def dig(d, v):
    return {("H", (d, b)): (v >> b) & 1 for b in range(4)}

def kmp(bits):					# the next prefix length after seeing a, for a pattern (overlapping)
    L = len(bits)
    def nx(k, a):
        s = bits[:k] + [a] if k < L else bits[1:] + [a]
        for m in range(min(len(s), L), -1, -1):
            if s[len(s) - m:] == bits[:m]:
                return m
        return 0
    return nx
def pbits(p, L):
    return [(p >> (L - 1 - i)) & 1 for i in range(L)]
def fld(r, *w):					# split a row into fields (widths MSB first)
    out, tot = [], sum(w)
    for x in w:
        tot -= x
        out.append((r >> tot) & ((1 << x) - 1))
    return out
def tab(outs, n, f):				# the tables: f(row) -> {out: bit}, one list per output
    rows = [f(r) for r in range(1 << n)]
    return [[d[o] for d in rows] for o in outs]
def add(id_, title, inputs, outs, hexes, variants, f, describe, B, steps):
    """A question on the combinational part of an FSM: f(p, row) -> {out: bit}; the answer = the last step's."""
    W.append(Q(id=id_, name=id_, title=title, inputs=inputs, flat=True, small=True, outs=outs, hexes=hexes,
               variants=variants, tables=lambda p: tab(outs, len(inputs), lambda r: f(p, r)),
               answer=lambda p: steps[-1][1](None, p), describe=describe, B=[B + "     answer: SW4..SW0"], L=[], F=[],
               steps=steps))

PATH = "SW1 = first bit     SW0 = second bit"
PATH3 = "SW2 = first bit     SW1 = second     SW0 = third"
NOCLK = "בלי שעון: במתגים שמים מצב נוכחי וכניסה, ובלוח רואים את המצב הבא ואת היציאה."
NOCLK0 = "בלי שעון ובלי כניסות: במתגים שמים מצב נוכחי, ובלוח רואים את המצב הבא."
FWD = "צעד קדימה: מעבירים את המצב הבא אל מתגי המצב."
MMQ = "השאירו את מתגי המצב והזיזו רק את מתג הכניסה. היציאה משתנה?"
MM = code(["Moore (no)", "Mealy (yes)"])
LS = "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)"
LN = "next S = HEX0     Y = LEDG0"
OSN = [("G", 0)] + hexd(0)
H98_7 = [[9, 8], [7], None, None]

# ================================================================ topic 1: the snail - Moore and Mealy
# how many states for a pattern shown on the board
VSN2 = [(L, pat) for L in (2, 3, 4) for pat in range(1 << L)]
W.append(Q(id="NSTATES", name="NSTATES", title="כמה מצבים לגלאי?", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(0), hexes=[None, None, None, None], variants=VSN2,
    tables=lambda p: const(bitsof(p[1], 4) + bitsof(p[0], 4)), answer=lambda p: (p[0], 0xF),
    describe=lambda p: f"pattern {p[1]:0{p[0]}b}: Moore {p[0] + 1}, Mealy {p[0]}",
    B=["the pattern length = HEX0     the pattern = the right LEDs of LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בתצוגה האורך של רצף, ובנורות הירוקות הרצף עצמו.", "length = HEX0",
             "כמה מצבים צריך גלאי מור של הרצף הזה?"] + cnt(5), lambda q, p: (p[0] + 1, 0xF)),
           (["וכמה מצבים צריך גלאי מילי?"] + cnt(5), lambda q, p: (p[0], 0xF))]))

# the snail: Moore or Mealy, which pattern (Moore: state = matched prefix 0..2; Mealy: SW8 = the previous bit)
def sn_f(p, r):
    t, pat = p
    s, a = fld(r, 2, 1)
    if t == 0:
        ns, y = (kmp(pbits(pat, 2))(s, a) if s < 3 else 0), int(s == 2)
    else:
        ns, y = a, int((((s & 1) << 1) | a) == pat)
    return {("G", 0): y, **dig(0, ns)}
add("SNAIL", "החילזון: מתי הוא מחייך?", [9, 8, 7], OSN, H98_7, [(t, p) for t in range(2) for p in range(4)], sn_f,
    lambda p: f"{'Mealy' if p[0] else 'Moore'} snail, pattern {p[1]:02b}",
    "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)     next S = HEX0     smile Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון שמחייך אחרי רצף מסוים של שני ביטים.", NOCLK, LS, LN, MMQ] + MM,
      lambda q, p: (p[0], 0x1)),
     (["מה הרצף שמחייך?", "במור: מהמצב 0, איזה ביט מוביל למצב 1, ומשם איזה ביט למצב 2 (שבו הוא מחייך)?",
       "במילי: מתג המצב הימני הוא הביט הקודם. מתי היציאה דולקת?", LS, LN, PATH], lambda q, p: (p[1], 0x3))])

# the Moore snail's state codes (slide 4), in a hidden encoding (11 not used)
LSS = "S1 S0 = SW9 SW8     A = SW7"
LNS = "next S1 S0 = LEDG3 LEDG2     Y = LEDG0"
OSS = [("G", 3), ("G", 2), ("G", 0)]
def ss_f(p, r):
    e, pat = p
    s, a = fld(r, 2, 1)
    if s == 3:
        ns, y = 3, 0
    else:
        i = e.index(s)
        ns, y = e[kmp(pbits(pat, 2))(i, a)], int(i == 2)
    return {("G", 3): ns >> 1, ("G", 2): ns & 1, ("G", 0): y}
add("SNAILSTATES", "המצבים של חילזון מור", [9, 8, 7], OSS, H98_7,
    [(e, pat) for e in itertools.permutations(range(3)) for pat in range(4)], ss_f,
    lambda p: f"pattern {p[1]:02b}, S0 S1 S2 = {[f'{c:02b}' for c in p[0]]}",
    "S1 S0 = SW9 SW8     A = SW7     next S1 S0 = LEDG3 LEDG2     Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון מור: שלושה מצבים בקידוד נסתר. הקוד 11 לא בשימוש.", NOCLK, LSS, LNS,
       "באיזה קוד הוא מחייך?", "SW1 SW0 = S1 S0"], lambda q, p: (p[0][2], 0x3)),
     (["איזה קוד אחר מוביל אל הקוד המחייך? (זה המצב שראה את הביט הראשון של הרצף)", LSS, LNS, "SW1 SW0 = S1 S0"],
      lambda q, p: (p[0][1], 0x3)),
     (["ומה הקוד של מצב ההתחלה (הקוד השלישי שבשימוש)?", "SW1 SW0 = S1 S0"], lambda q, p: (p[0][0], 0x3)),
     (["מה הרצף שמחייך? (ממצב ההתחלה, ביט ועוד ביט, עד הקוד המחייך)", LSS, LNS, PATH], lambda q, p: (p[1], 0x3))])

# the Moore snail's next-state table (slide 4): the lecture's encoding, hidden pattern
def sx_next(p, s, a):
    return kmp(pbits(p, 2))(s, a) if s < 3 else 0
add("SNAILNEXT", "טבלת המעברים של חילזון מור", [9, 8, 7], OSS, H98_7, list(range(4)),
    lambda p, r: {("G", 3): sx_next(p, *fld(r, 2, 1)) >> 1, ("G", 2): sx_next(p, *fld(r, 2, 1)) & 1,
                  ("G", 0): int(fld(r, 2, 1)[0] == 2)},
    lambda p: f"pattern {p:02b}: S2 -A=0-> {sx_next(p, 2, 0):02b}, -A=1-> {sx_next(p, 2, 1):02b}",
    "S1 S0 = SW9 SW8     A = SW7     next S1 S0 = LEDG3 LEDG2     Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון מור, עם הקידוד של ההרצאה.", NOCLK, "S0 = 00     S1 = 01     S2 = 10", LSS, LNS,
       "מה הרצף שמחייך? (מ-00 ל-01, ומשם ל-10)", PATH], lambda q, p: (p, 0x3)),
     (["במצב", "S2 = 10", "שימו 0 בכניסה. מה המצב הבא?", LSS, LNS, "SW1 SW0 = next S1 S0"],
      lambda q, p: (sx_next(p, 2, 0), 0x3)),
     (["במצב", "S2 = 10", "שימו 1 בכניסה. מה המצב הבא?", LSS, LNS, "SW1 SW0 = next S1 S0"],
      lambda q, p: (sx_next(p, 2, 1), 0x3))])

# the Mealy snail: one state bit (the previous tape bit), the output table (slide 6)
LME = "S0 = SW9     A = SW8     next S0 = LEDG1     Y = LEDG0"
add("SNAILMEALY", "טבלת היציאה של חילזון מילי", [9, 8], [("G", 1), ("G", 0)], [[9], [8], None, None], list(range(4)),
    lambda p, r: {("G", 1): r & 1, ("G", 0): int(r == p)}, lambda p: f"Y = 1 when (S0, A) = {p:02b}",
    "S0 = SW9 (HEX3)     A = SW8 (HEX2)     next S0 = LEDG1     Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון מילי: ביט מצב אחד, והיציאה תלויה בו ובכניסה.", NOCLK, LME,
       "מה המצב הבא?", "S0' = ?"] + code(["0", "1", "A", "S0"]), lambda q, p: (2, 0x3)),
     (["מתי היציאה דולקת? הרימו את המתג של כל מקרה שבו היא דולקת:", LME,
       "S0 A = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"], lambda q, p: (1 << p, 0xF))])

# the timing (slide 9): the tape bit during which the snail first smiles (Mealy: one bit before Moore)
TAPE2 = [1, 1, 0, 1, 0, 0, 1, 1]
def first_hit(pat):				# the 1-based index of the tape bit that completes the pattern first
    for k in range(2, len(TAPE2) + 1):
        if TAPE2[k - 2] * 2 + TAPE2[k - 1] == pat:
            return k
def st_f(p, r):					# Moore: s = prefix 0..2; Mealy: s = 0 none / 1 last 0 / 2 last 1
    t, pat = p
    s, a = fld(r, 2, 1)
    if t == 0:
        ns, y = (kmp(pbits(pat, 2))(s, a) if s < 3 else 0), int(s == 2)
    else:
        ns, y = 1 + a, int(0 < s < 3 and ((s - 1) << 1 | a) == pat)
    return {("G", 0): y, **dig(0, ns)}
add("SNAILTIME", "מתי החיוך הראשון?", [9, 8, 7], OSN, H98_7, [(t, p) for t in range(2) for p in range(4)], st_f,
    lambda p: f"{'Mealy' if p[0] else 'Moore'} snail, pattern {p[1]:02b}: first smile at tape bit {first_hit(p[1]) + 1 - p[0]}",
    "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)     next S = HEX0     Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון (רצף נסתר של שני ביטים).", NOCLK, LS, LN, MMQ] + MM, lambda q, p: (p[0], 0x1)),
     (["עקבו אחריו על הסרט מהמצב 0. בכל ביט: שימו אותו בכניסה, הסתכלו על היציאה, ואז עברו למצב הבא.",
       "the tape:   " + " ".join(map(str, TAPE2)), LS, LN, "בזמן איזה ביט בסרט (המספר שלו) היציאה נדלקת בפעם הראשונה?"]
      + cnt(8), lambda q, p: (first_hit(p[1]) + 1 - p[0], 0xF))])

# a tape: how many smiles (Moore, hidden overlapping pattern of 2 or 3 bits; the smiling state = the length)
TAPE = [0, 1, 1, 0, 1, 0, 0, 1, 1, 1]
def smiles(pat, L):
    nx, k, n = kmp(pbits(pat, L)), 0, 0
    for a in TAPE:
        k = nx(k, a)
        n += k == L
    return n
VTA = [(L, pat) for L in (2, 3) for pat in range(1 << L) if 0 < smiles(pat, L)]
def ta_f(p, r):
    L, pat = p
    s, a = fld(r, 2, 1)
    return {("G", 0): int(s == L), **dig(0, kmp(pbits(pat, L))(s, a) if s <= L else 0)}
add("TAPE", "כמה חיוכים על הסרט?", [9, 8, 7], OSN, H98_7, VTA, ta_f,
    lambda p: f"pattern {p[1]:0{p[0]}b}: {smiles(p[1], p[0])} smiles",
    "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)     next S = HEX0     Y = LEDG0",
    [(["בלוח החלק הצירופי של חילזון מור (רצף נסתר, חופף).", NOCLK, LS, LN, "באיזה מצב הוא מחייך?",
       "2 = SW1     3 = SW1+SW0"], lambda q, p: (p[0], 0x3)),
     (["העבירו אותו על הסרט מהמצב 0: בכל ביט שימו אותו בכניסה ועברו למצב הבא.",
       "the tape:   " + " ".join(map(str, TAPE)), LS, LN, "כמה פעמים עברתם אל המצב המחייך?", "0 = all down"] + cnt(6),
      lambda q, p: (smiles(p[1], p[0]), 0xF))])

# two snails on one 3-bit pattern: which LED is the Mealy one, and the pattern
LTW = "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)     next S = HEX0     snails: LEDG1, LEDG0"
def tw_f(p, r):
    w, pat = p
    s, a = fld(r, 2, 1)
    ns = kmp(pbits(pat, 3))(s, a)
    moore, mealy = int(s == 3), int(ns == 3)
    return {("G", 1): mealy if w == 0 else moore, ("G", 0): moore if w == 0 else mealy, **dig(0, ns)}
add("TWOSNAILS", "שני חלזונות על אותו סרט", [9, 8, 7], [("G", 1), ("G", 0)] + hexd(0), H98_7,
    [(w, pat) for w in range(2) for pat in range(8)], tw_f, lambda p: f"Mealy = LEDG{1 - p[0]}, pattern {p[1]:03b}", LTW,
    [(["בלוח החלק הצירופי של שני חלזונות על אותו רצף של שלושה ביטים: אחד מור ואחד מילי.", NOCLK, LTW,
       "איזו נורה היא חילזון מילי? (משתנה עם הכניסה כשמתגי המצב לא זזים)"] + code(["LEDG1", "LEDG0"]),
      lambda q, p: (p[0], 0x1)),
     (["מה הרצף? (מהמצב 0, ביט אחר ביט, עד המצב 3)", LTW, PATH3], lambda q, p: (p[1], 0x7))])

# a run of ones: how long, and how many states for Moore and Mealy
L1 = "S = SW9 SW8 SW7 (HEX3)     A = SW6 (HEX2)     next S = HEX0     Y = LEDG0"
def on_f(L, r):
    s, a = fld(r, 3, 1)
    ns = 0 if s > L else (min(s + 1, L) if a else 0)
    return {("G", 0): int(s == L), **dig(0, ns)}
add("ONES", "כמה אחדות ברצף?", [9, 8, 7, 6], OSN, [[9, 8, 7], [6], None, None], list(range(2, 6)), on_f,
    lambda L: f"{L} ones in a row", L1,
    [(["בלוח החלק הצירופי של גלאי מור: היציאה נדלקת אחרי כמה אחדות ברצף.", NOCLK, L1,
       "כמה אחדות ברצף צריך? (מהמצב 0, עם כניסה 1, עד שהיציאה דולקת)"] + cnt(5), lambda q, L: (L, 0xF)),
     (["כמה מצבים יש לגלאי הזה כמכונת מור? (מצב לכל מספר אחדות שנראו, כולל 0)"] + cnt(6), lambda q, L: (L + 1, 0xF)),
     (["וכמה מצבים היו צריכים כמכונת מילי? (היציאה נקבעת כבר עם הביט האחרון)"] + cnt(6), lambda q, L: (L, 0xF))])

# an edge detector: which change, Moore or Mealy (Moore: S1 = a hit was seen; S0 = the previous bit)
EDG = ["rising (0 -> 1)", "falling (1 -> 0)", "any change"]
LE = "S1 S0 = SW9 SW8     A = SW7     next S1 S0 = LEDG3 LEDG2     Y = LEDG0"
def ed_hit(e, prev, a):
    return [int(prev == 0 and a == 1), int(prev == 1 and a == 0), int(prev != a)][e]
def ed_f(p, r):
    e, t = p
    s1, s0, a = fld(r, 1, 1, 1)
    h = ed_hit(e, s0, a)
    ns, y = ((h << 1) | a, s1) if t == 0 else (a, h)
    return {("G", 3): ns >> 1, ("G", 2): ns & 1, ("G", 0): y}
add("EDGE", "גלאי שינוי", [9, 8, 7], OSS, H98_7, [(e, t) for e in range(3) for t in range(2)], ed_f,
    lambda p: f"{EDG[p[0]]}, {'Mealy' if p[1] else 'Moore'}", LE,
    [(["בלוח החלק הצירופי של גלאי שינוי: היציאה נדלקת כשהכניסה משתנה בדרך מסוימת.", NOCLK, LE,
       "S0 = the previous bit", MMQ] + MM, lambda q, p: (p[1], 0x1)),
     (["איזה שינוי הוא מגלה? במילי - לפי היציאה. במור - לפי ביט המצב הבא", "S1", "(הוא היציאה בצעד הבא).", LE,
       "S0 = the previous bit"] + code(EDG, 3), lambda q, p: (p[0], 0x3))])

# overlapping or not: a Moore detector of a 3-bit pattern that has a border (000, 010, 101, 111)
def ov_f(p, r):
    pat, ov = p
    s, a = fld(r, 2, 1)
    nx = kmp(pbits(pat, 3))
    return {("G", 0): int(s == 3), **dig(0, nx(s, a) if (s < 3 or ov) else nx(0, a))}
add("OVERLAP", "גלאי חופף או לא חופף", [9, 8, 7], OSN, H98_7,
    [(pat, ov) for pat in (0b000, 0b010, 0b101, 0b111) for ov in range(2)], ov_f,
    lambda p: f"pattern {p[0]:03b}, {'overlapping' if p[1] else 'non-overlapping'}",
    "S = SW9 SW8 (HEX3)     A = SW7 (HEX2)     next S = HEX0     Y = LEDG0",
    [(["בלוח החלק הצירופי של גלאי מור לרצף של שלושה ביטים. במצב 3 הוא מחייך.", NOCLK, LS, LN,
       "מה הרצף? (מהמצב 0, ביט אחר ביט, עד המצב 3)", PATH3], lambda q, p: (p[0], 0x7)),
     (["ממצב 3: האם סוף הרצף נספר גם כהתחלה של הרצף הבא (חפיפה)?",
       "בדקו לאן הוא עובר ממצב 3 עם הביט שממשיך את הרצף.", LS, LN] + UP0("חופף", "לא חופף"), lambda q, p: (p[1], 0x1))])

# ================================================================ topic 2: factored FSMs - the parade
LIGHTS = ["LA:  green = LEDG7   yellow = LEDG6   red = LEDG5", "LB:  green = LEDG2   yellow = LEDG1   red = LEDG0"]
LPH = "0 = A green     1 = A yellow     2 = B green     3 = B yellow"
LGT = [("G", i) for i in (7, 6, 5, 2, 1, 0)]
TL_OUT = {0: (0, 2), 1: (1, 2), 2: (2, 0), 3: (2, 1)}
def tl_leds(ph):				# ph = None: all off (a code not in use)
    if ph is None:
        return {o: 0 for o in LGT}
    la, lb = TL_OUT[ph]
    return {("G", i): int(i in (7 - la, 2 - lb)) for i in (7, 6, 5, 2, 1, 0)}
def lights_next(s, ta, tb, m, street):		# street: the green street in a parade (0 = A stays, 1 = B stays)
    if s == 0:
        return 0 if (ta or (m and street == 0)) else 1
    if s == 2:
        return 2 if (tb or (m and street == 1)) else 3
    return (s + 1) & 3
def mode_next(m, p_, r_, pw):			# pw: who wins when both (0 = P, 1 = R)
    if p_ and r_:
        return 1 if pw == 0 else 0
    return 1 if p_ else 0 if r_ else m

# the mode FSM alone: which switch is R, memory, who wins when both are up
LM = "M = SW9     P, R = SW8, SW7 (in some order)     next M = LEDG0"
def mo_f(p, r):
    pr, pw = p
    m, x, y = fld(r, 1, 1, 1)
    p_, r_ = (x, y) if pr == 0 else (y, x)
    return {("G", 0): mode_next(m, p_, r_, pw)}
add("MODEFSM", "מכונת המצב של התהלוכה", [9, 8, 7], [("G", 0)], [[9], [8], [7], None],
    [(pr, pw) for pr in range(2) for pw in range(2)], mo_f,
    lambda p: f"P = SW{7 if p[0] else 8}, both up -> {'R' if p[1] else 'P'} wins", LM,
    [(["בלוח החלק הצירופי של מכונת המצב בבקר הרמזור: ביט מצב אחד (יש תהלוכה או אין) ושתי כניסות.", NOCLK, LM,
       "איזה מתג מפסיק תהלוכה (המצב הבא כבוי)?", "R = ?"] + code(["SW8", "SW7"]), lambda q, p: (1 - p[0], 0x1)),
     (["הורידו את שתי הכניסות. האם המצב הבא שווה למצב הנוכחי (זיכרון)?", LM] + UP0("כן", "לא"), lambda q, p: (1, 0x1)),
     (["הרימו את שתי הכניסות. מי מנצח?", LM] + code(["P", "R"]), lambda q, p: (p[1], 0x1))])

# the whole controller: M on SW9, lights state on SW8 SW7, TA TB, P / R in a hidden order
LP1 = "M = SW9     lights state = SW8 SW7 (HEX2)"
LP3 = "next M = LEDG4     next lights state = HEX0"
OPA = [("G", 4)] + hexd(0)
HPA = [[9], [8, 7], None, None]
def par_f(sig, street, r):			# sig(inb) -> (ta, tb, p, r)
    m, l, inb = fld(r, 1, 2, 4)
    ta, tb, p_, r_ = sig(inb)
    return {("G", 4): mode_next(m, p_, r_, 0), **dig(0, lights_next(l, ta, tb, m, street))}
def pr_sig(pr):
    def sig(inb):
        ta, tb, x, y = fld(inb, 1, 1, 1, 1)
        return (ta, tb, x, y) if pr == 0 else (ta, tb, y, x)
    return sig
LP2 = "TA = SW6     TB = SW5     P, R = SW4, SW3 (in some order)"
add("PARADE", "מצב תהלוכה", [9, 8, 7, 6, 5, 4, 3], OPA, HPA, [(pr, st) for pr in range(2) for st in range(2)],
    lambda p, r: par_f(pr_sig(p[0]), p[1], r),
    lambda p: f"P = SW{3 if p[0] else 4}, in a parade street {'AB'[p[1]]} stays green",
    "M = SW9, lights state SW8 SW7, TA SW6, TB SW5, P / R on SW4 SW3     next M = LEDG4     next lights = HEX0",
    [(["בלוח החלק הצירופי של בקר הרמזור עם תהלוכה: שתי מכונות, מכונת המצב ומכונת הרמזורים.", NOCLK, LP1, LP2, LP3,
       "איזה מתג מתחיל תהלוכה (מדליק את המצב הבא של מכונת המצב)?", "P = ?"] + code(["SW4", "SW3"]),
      lambda q, p: (p[0], 0x1)),
     (["בזמן תהלוכה ובלי מכוניות, איזה רחוב נשאר ירוק?", "M = 1     TA = 0     TB = 0", LP1, LP3, LPH] + code(["A", "B"]),
      lambda q, p: (p[1], 0x1))])

# which switch is which: TA, TB, P, R in a hidden order (the parade keeps B green)
VPP = list(itertools.permutations(range(4)))	# perm[i] = the signal (0 TA, 1 TB, 2 P, 3 R) on switch 6 - i
def pp_sig(perm):
    def sig(inb):
        v = [0] * 4
        for i in range(4):
            v[perm[i]] = (inb >> (3 - i)) & 1
        return tuple(v)
    return sig
SW4 = code(["SW6", "SW5", "SW4", "SW3"])
LPP = "TA, TB, P, R = SW6, SW5, SW4, SW3 (in some order)"
add("PARADEPINS", "מי מחובר לאיזה מתג?", [9, 8, 7, 6, 5, 4, 3], OPA, HPA, VPP, lambda p, r: par_f(pp_sig(p), 1, r),
    lambda p: "SW6..SW3 = " + " ".join(["TA", "TB", "P", "R"][x] for x in p),
    "M = SW9, lights state SW8 SW7, TA TB P R on SW6..SW3 (hidden order)     next M = LEDG4     next lights = HEX0",
    [(["בלוח החלק הצירופי של בקר הרמזור עם תהלוכה, אבל ארבע הכניסות מחוברות בסדר נסתר.", NOCLK, LP1, LPP, LP3,
       "איזה מתג הוא", "P", "? (מדליק את המצב הבא של מכונת המצב)"] + SW4, lambda q, p: (p.index(2), 0x3)),
     (["איזה מתג הוא", "R", "? (מכבה את המצב הבא של מכונת המצב)", LP1, LPP, LP3] + SW4, lambda q, p: (p.index(3), 0x3)),
     (["בלי תהלוכה ובמצב 0 של הרמזורים: איזה מתג משאיר את המצב הבא של הרמזורים 0?", "M = 0", LP1, LPP, LP3, LPH] + SW4,
      lambda q, p: (p.index(0), 0x3))])

# lights with long yellows: k yellow states on each street (ka, kb); index -> phase
def yl_seq(ka, kb):
    return [0] + [1] * ka + [2] + [3] * kb
def yl_next(S, l, ta, tb, m):			# the parade keeps B green
    ph = S[l]
    if ph == 0:
        return 0 if (ta and not m) else 1
    if ph == 2:
        return l if (tb or m) else l + 1
    return (l + 1) % len(S)
# when a parade starts while A is green: how many steps until B is green
LW1 = "M = SW9     lights state = SW8 SW7 SW6 (HEX2)     TA = SW5     TB = SW4"
LW2 = "next lights state = HEX0"
def pw_f(p, r):
    S = yl_seq(*p)
    m, l, ta, tb = fld(r, 1, 3, 1, 1)
    if l >= len(S):
        return {**tl_leds(None), **dig(0, 0)}
    return {**tl_leds(S[l]), **dig(0, yl_next(S, l, ta, tb, m))}
add("PARADEWAIT", "כמה זמן עד שהתהלוכה עוברת?", [9, 8, 7, 6, 5, 4], LGT + hexd(0), [[9], [8, 7, 6], None, None],
    [(a, b) for a in (1, 2, 3) for b in (1, 2, 3)], pw_f,
    lambda p: f"yellow A {p[0]}, yellow B {p[1]}: B green {p[0] + 1} steps after state 0",
    "M = SW9, lights state SW8..SW6, TA SW5, TB SW4     lights LEDG7..5, LEDG2..0     next lights state = HEX0",
    [(["בלוח החלק הצירופי של מכונת הרמזורים, שבה כל צהוב נמשך כמה מצבים. התהלוכה ברחוב השני.", NOCLK, LW1, LW2]
      + LIGHTS + ["במצב 0 הרחוב הראשון ירוק. הרימו את", "M", "ואת", "TA", ". מה המצב הבא?"] + cnt(3),
      lambda q, p: (1, 0x3)),
     (["כמה צעדים מהמצב 0 עד שהרחוב השני ירוק?", FWD, LW1, LW2] + LIGHTS + cnt(4), lambda q, p: (p[0] + 1, 0xF))])

# factored vs unfactored: how many states
LFC = "lights state = SW9 SW8 SW7 (HEX3)     TA = SW6     TB = SW5     next = HEX0"
def fc_f(p, r):
    S = yl_seq(*p)
    l, ta, tb = fld(r, 3, 1, 1)
    if l >= len(S):
        return {**tl_leds(None), **dig(0, 0)}
    return {**tl_leds(S[l]), **dig(0, yl_next(S, l, ta, tb, 0))}
add("FACTORCOUNT", "כמה מצבים עם פירוק ובלי?", [9, 8, 7, 6, 5], LGT + hexd(0), [[9, 8, 7], None, None, None],
    [(a, b) for a in (1, 2, 3) for b in (1, 2, 3)], fc_f,
    lambda p: f"yellow {p[0]} + {p[1]}: lights {2 + p[0] + p[1]} states", LFC + "     lights LEDG7..5, LEDG2..0",
    [(["בלוח החלק הצירופי של מכונת הרמזורים, שבה כל צהוב נמשך כמה מצבים. קוד שלא מדליק אף רמזור לא בשימוש.", NOCLK, LFC]
      + LIGHTS + ["כמה מצבים יש למכונת הרמזורים?"] + cnt(8), lambda q, p: (2 + p[0] + p[1], 0xF)),
     (["מוסיפים מצב תהלוכה (שני מצבים: יש או אין). כמה מצבים צריך מכונה אחת בלי פירוק?"] + BIN5,
      lambda q, p: (2 * (2 + p[0] + p[1]), 0x1F)),
     (["וכמה מצבים בסך הכול בשתי מכונות נפרדות (פירוק)?"] + cnt(9) + ["10 = SW3+SW1"],
      lambda q, p: (2 + p[0] + p[1] + 2, 0xF))])

# factoring out a timer: the lights FSM waits for a timer FSM
LT1 = "lights = SW9 SW8 (HEX3)     timer = SW7 SW6 SW5 (HEX2)"
LT2 = "next lights = HEX1     next timer = HEX0"
def tl_len(p, ph):
    return [p[0], 1, p[1], 1][ph]
def tl_f(p, r):
    ph, t = fld(r, 2, 3)
    if t >= tl_len(p, ph):
        t = 0
    nph, nt = (((ph + 1) & 3), 0) if t == tl_len(p, ph) - 1 else (ph, t + 1)
    return {**dig(1, nph), **dig(0, nt)}
add("TIMERLIGHT", "רמזור עם מכונת טיימר", [9, 8, 7, 6, 5], hexd(1) + hexd(0), [[9, 8], [7, 6, 5], None, None],
    [(ga, gb) for ga in range(2, 6) for gb in range(2, 6)], tl_f,
    lambda p: f"A green {p[0]}, B green {p[1]}, timer {max(p)} states", LT1 + "     " + LT2,
    [(["בלוח החלק הצירופי של רמזור מפורק לשתי מכונות: מכונת הרמזורים, ומכונת טיימר שאומרת לה מתי לעבור.", NOCLK0,
       LT1, LT2, LPH, "מרמזור 0 וטיימר 0: כמה צעדים עד שהרמזור משתנה?", FWD] + cnt(5), lambda q, p: (p[0], 0xF)),
     (["מרמזור 2 וטיימר 0: כמה צעדים עד שהרמזור משתנה?", LT1, LT2] + cnt(5), lambda q, p: (p[1], 0xF)),
     (["כמה מצבים צריך מכונת הטיימר? (היא סופרת את הירוק הארוך)"] + cnt(5), lambda q, p: (max(p), 0xF))])

# a two-digit counter as two FSMs (units, tens): states with and without factoring
LD1 = "tens = SW9 SW8 (HEX3)     units = SW7 SW6 SW5 (HEX2)"
LD2 = "next tens = HEX1     next units = HEX0"
def td_f(p, r):
    u, t = p
    tn, un = fld(r, 2, 3)
    if un >= u or tn >= t:
        ntn, nun = 0, 0
    elif un == u - 1:
        ntn, nun = (tn + 1) % t, 0
    else:
        ntn, nun = tn, un + 1
    return {**dig(1, ntn), **dig(0, nun)}
add("TWODIGITS", "מונה של שתי ספרות: שתי מכונות", [9, 8, 7, 6, 5], hexd(1) + hexd(0), [[9, 8], [7, 6, 5], None, None],
    [(u, t) for u in range(3, 8) for t in range(2, 5)], td_f, lambda p: f"units mod {p[0]}, tens mod {p[1]}",
    LD1 + "     " + LD2,
    [(["בלוח החלק הצירופי של מונה של שתי ספרות: מכונת היחידות מודיעה למכונת העשרות מתי להתקדם.", NOCLK0, LD1, LD2,
       "כמה מצבים יש למכונת היחידות? (מ-0, צעד אחר צעד, עד שהיא חוזרת ל-0)", FWD] + cnt(7), lambda q, p: (p[0], 0xF)),
     (["כמה מצבים יש למכונת העשרות?", LD1, LD2] + cnt(4), lambda q, p: (p[1], 0xF)),
     (["כמה מצבים צריך מכונה אחת בלי פירוק (כל צירוף של שתי הספרות)?"] + binl(5), lambda q, p: (p[0] * p[1], 0x1F)),
     (["וכמה מצבים בסך הכול בשתי המכונות המפורקות?"] + BIN4, lambda q, p: (p[0] + p[1], 0xF))])

# ================================================================ topic 3: designing FSMs
# a blinker: on for a states, off for b states
LB = "S = SW9 SW8 SW7 (HEX3)     next S = HEX0     Y = LEDG0"
def bl_f(p, r):
    n = p[0] + p[1]
    return {("G", 0): int(r < p[0]), **dig(0, (r + 1) % n if r < n else 0)}
add("BLINK", "מהבהב", [9, 8, 7], OSN, [[9, 8, 7], None, None, None], [(a, b) for a in range(1, 5) for b in range(1, 5)],
    bl_f, lambda p: f"on {p[0]}, off {p[1]}", LB,
    [(["בלוח החלק הצירופי של מכונה מהבהבת: היציאה דולקת כמה מצבים וכבויה כמה מצבים, וחוזר חלילה.", NOCLK0, LB,
       "מהמצב 0: בכמה מצבים ברצף היא דולקת?", FWD] + cnt(4), lambda q, p: (p[0], 0xF)),
     (["בכמה מצבים ברצף היא כבויה?", LB] + cnt(4), lambda q, p: (p[1], 0xF)),
     (["כמה מצבים יש במחזור?"] + cnt(8), lambda q, p: (p[0] + p[1], 0xF))])

# serial parity
LPR = "S = SW9     SW8, SW7 (one is the input)     next S = LEDG1     Y = LEDG0"
def pa_f(p, r):
    sw, ev = p
    s, x, y = fld(r, 1, 1, 1)
    return {("G", 1): s ^ (x if sw == 0 else y), ("G", 0): s ^ ev}
add("PARITY", "זוגיות טורית", [9, 8, 7], [("G", 1), ("G", 0)], [[9], [8], [7], None],
    [(sw, ev) for sw in range(2) for ev in range(2)], pa_f,
    lambda p: f"input SW{8 - p[0]}, LED = {'even' if p[1] else 'odd'} parity", LPR,
    [(["בלוח החלק הצירופי של מכונה שזוכרת אם נכנס מספר זוגי של אחדות. אחד המתגים לא מחובר.", NOCLK, LPR,
       "איזה מתג הוא הכניסה? (משנה את המצב הבא)"] + code(["SW8", "SW7"]), lambda q, p: (p[0], 0x1)),
     (["היציאה תלויה רק במצב?", LPR] + code(["Moore (yes)", "Mealy (no)"]), lambda q, p: (0, 0x1)),
     (["במצב 0 עוד לא נכנסו אחדות (זוגי). היציאה דולקת במצב 0?", LPR] + UP0("דולקת", "כבויה"), lambda q, p: (p[1], 0x1))])

# a counter of ones, modulo N
LCO = "S = SW9 SW8 SW7 SW6 (HEX3)     SW5, SW4 (one is the input)     next S = HEX0"
def co_f(p, r):
    sw, n = p
    s, x, y = fld(r, 4, 1, 1)
    return dig(0, (s + (x if sw == 0 else y)) % n if s < n else 0)
add("COUNTONES", "מונה אחדות", [9, 8, 7, 6, 5, 4], hexd(0), [[9, 8, 7, 6], None, None, None],
    [(sw, n) for sw in range(2) for n in range(3, 10)], co_f, lambda p: f"counts SW{5 - p[0]} modulo {p[1]}", LCO,
    [(["בלוח החלק הצירופי של מונה: הוא מתקדם ב-1 כשהכניסה 1. אחד המתגים הוא הכניסה.", NOCLK, LCO, "איזה מתג?"]
      + code(["SW5", "SW4"]), lambda q, p: (p[0], 0x1)),
     (["אחרי איזה מצב הוא חוזר ל-0? כתבו כמה מצבים יש.", LCO] + cnt(9), lambda q, p: (p[1], 0xF))])

# a vending machine: nickel and dime (state = paid / 5, starts over after a drink)
LV1 = "S = SW9 SW8 SW7 (HEX3)     coins = SW6, SW5"
LV2 = "next S = HEX2     paid now = HEX1 HEX0     drink = LEDG0"
def ve_f(p, r):
    d, pr = p
    s, inb = fld(r, 3, 2)
    n_, di = (inb >> d) & 1, (inb >> (1 - d)) & 1
    v = s * 5
    ns = min((0 if v >= pr else s) + n_ + 2 * di, 7)
    return {("G", 0): int(v >= pr), **dig(2, ns), **dig(1, v // 10), **dig(0, v % 10)}
add("VENDING", "מכונת שתייה", [9, 8, 7, 6, 5], [("G", 0)] + hexd(2) + hexd(1) + hexd(0), [[9, 8, 7], None, None, None],
    [(d, pr) for d in range(2) for pr in (15, 20, 25, 30)], ve_f, lambda p: f"dime = SW{6 - p[0]}, price {p[1]}",
    LV1 + "     " + LV2,
    [(["בלוח החלק הצירופי של מכונת שתייה: מטבע של 5 ומטבע של 10, כל אחד על מתג. המצב הוא כמה שולם.", NOCLK, LV1, LV2,
       "איזה מתג הוא המטבע של 10?"] + code(["SW6", "SW5"]), lambda q, p: (p[0], 0x1)),
     (["כמה עולה שתייה (מתי היציאה דולקת)? כתבו את המחיר חלקי 5.", LV1, LV2,
       "15 = SW1+SW0     20 = SW2     25 = SW2+SW0     30 = SW2+SW1"], lambda q, p: (p[1] // 5, 0xF))])

# saturate or wrap
LSA = "S = SW9 SW8 SW7 SW6 (HEX3)     next S = HEX0"
add("SATURATE", "מונה שנעצר או חוזר", [9, 8, 7, 6], hexd(0), [[9, 8, 7, 6], None, None, None],
    [(n, sat) for n in range(4, 10) for sat in range(2)],
    lambda p, s: dig(0, (min(s + 1, p[0] - 1) if p[1] else (s + 1) % p[0]) if s < p[0] else 0),
    lambda p: f"0..{p[0] - 1}, {'saturates' if p[1] else 'wraps'}", LSA,
    [(["בלוח החלק הצירופי של מונה בלי כניסות.", NOCLK0, LSA, "מהמצב 0, צעד אחר צעד: מה המצב הגדול ביותר שהוא מגיע אליו?",
       FWD] + cnt(9), lambda q, p: (p[0] - 1, 0xF)),
     (["וממנו - הוא נשאר שם, או חוזר ל-0?", LSA] + UP0("נשאר", "חוזר ל-0"), lambda q, p: (p[1], 0x1))])

# an up / down counter: which switch enables, which way is up
LUD = "S = SW9 SW8 SW7 SW6 (HEX3)     SW5, SW4 (enable, direction)     next S = HEX0"
def ud_f(p, r):
    e, up, n = p
    s, inb = fld(r, 4, 2)
    if s >= n:
        return dig(0, 0)
    en, d = (inb >> (1 - e)) & 1, (inb >> e) & 1
    return dig(0, s if not en else (s + 1) % n if d == up else (s - 1) % n)
add("UPDOWN", "מונה למעלה ולמטה", [9, 8, 7, 6, 5, 4], hexd(0), [[9, 8, 7, 6], None, None, None],
    [(e, up, n) for e in range(2) for up in range(2) for n in range(4, 10)], ud_f,
    lambda p: f"enable SW{5 - p[0]}, up when dir = {p[1]}, modulo {p[2]}", LUD,
    [(["בלוח החלק הצירופי של מונה עם שתי כניסות: אחת מאפשרת לספור, והשנייה קובעת כיוון.", NOCLK, LUD,
       "איזה מתג מאפשר לספור? (כשהוא למטה המצב הבא שווה למצב הנוכחי)"] + code(["SW5", "SW4"]), lambda q, p: (p[0], 0x1)),
     (["כשמתג הכיוון למעלה, המונה סופר למעלה?", LUD] + UP0("כן", "לא, למטה"), lambda q, p: (p[1], 0x1)),
     (["מהמצב 0, צעד אחד למטה: מה המצב הבא?", LUD] + cnt(9), lambda q, p: (p[2] - 1, 0xF))])

# a sequence counter: binary, Gray or one-hot, 3 or 4 bits (a code not in use goes to the start)
LSQ = "S = SW9 SW8 SW7 SW6     next S = LEDG3 LEDG2 LEDG1 LEDG0"
def sq_len(p):
    k, b = p
    return b if k == 2 else 1 << b
def sq_code(p, i):
    return [i, i ^ (i >> 1), 1 << i][p[0]]
def sq_f(p, c):
    cyc = [sq_code(p, i) for i in range(sq_len(p))]
    nc = cyc[(cyc.index(c) + 1) % len(cyc)] if c in cyc else cyc[0]
    return {("G", j): (nc >> j) & 1 for j in range(4)}
add("SEQCOUNT", "באיזה קוד המונה סופר?", [9, 8, 7, 6], [("G", i) for i in range(4)], [None, None, None, None],
    [(k, b) for k in range(3) for b in (3, 4)], sq_f, lambda p: f"{['binary', 'Gray', 'one-hot'][p[0]]}, {p[1]} bits", LSQ,
    [(["בלוח החלק הצירופי של מונה בלי כניסות. קוד שלא בשימוש עובר למצב ההתחלה.", NOCLK0, LSQ,
       "מהקוד 0000, צעד אחר צעד: כמה מצבים שונים יש במחזור?", FWD] + binl(5), lambda q, p: (sq_len(p), 0x1F)),
     (["באיזה קוד הוא סופר?", "binary: +1     Gray: one bit changes     one-hot: one bit on", LSQ]
      + code(["binary", "Gray", "one-hot"], 3), lambda q, p: (p[0], 0x3))])

# a debouncer: the clean output Y flips only after the input differs from it for N steps in a row (on / off)
LDB = "Y = SW9     count = SW8 SW7     A = SW6     next Y = LEDG1     next count = HEX0"
def db_f(p, r):
    non, noff = p
    y, c, a = fld(r, 1, 2, 1)
    n = noff if y else non
    if c >= n or a == y:
        ny, nc = y, 0
    elif c + 1 == n:
        ny, nc = 1 - y, 0
    else:
        ny, nc = y, c + 1
    return {("G", 1): ny, **dig(0, nc)}
add("DEBOUNCE", "מסנן קפיצות", [9, 8, 7, 6], [("G", 1)] + hexd(0), [[9], [8, 7], [6], None],
    [(a, b) for a in range(2, 5) for b in range(2, 5)], db_f, lambda p: f"on after {p[0]} ones, off after {p[1]} zeros", LDB,
    [(["בלוח החלק הצירופי של מסנן: היציאה הנקייה מתהפכת רק אחרי כמה צעדים ברצף שבהם הכניסה שונה ממנה.", NOCLK, LDB,
       "מהמצב שבו היציאה כבויה והמונה 0, עם כניסה 1: כמה צעדים עד שהיציאה הבאה דולקת?", FWD] + cnt(4),
      lambda q, p: (p[0], 0xF)),
     (["מהמצב שבו היציאה דולקת והמונה 0, עם כניסה 0: כמה צעדים עד שהיציאה הבאה כבויה?", LDB] + cnt(4),
      lambda q, p: (p[1], 0xF)),
     (["כמה מצבים בשימוש יש למכונה? (שני המונים יחד)"] + cnt(8), lambda q, p: (p[0] + p[1], 0xF))])

# a lock of 3 single bits that starts over on a wrong bit
LL3 = "S = SW9 SW8 (HEX3)     bit = SW7 (HEX2)     next S = HEX0     open = LEDG0"
def l3_f(p, r):
    s, a = fld(r, 2, 1)
    return {("G", 0): int(s == 3), **dig(0, 3 if s == 3 else (s + 1 if a == pbits(p, 3)[s] else 0))}
add("LOCK3", "מנעול של שלושה ביטים", [9, 8, 7], OSN, H98_7, list(range(8)), l3_f,
    lambda p: f"code {p:03b}, a wrong bit starts over", LL3,
    [(["בלוח החלק הצירופי של מנעול: שלושה ביטים נכונים ברצף פותחים אותו, וביט שגוי מחזיר להתחלה.", NOCLK, LL3,
       "באיזה מצב המנעול פתוח?", "1 = SW0     2 = SW1     3 = SW1+SW0"], lambda q, p: (3, 0x3)),
     (["מה הקוד? (מהמצב 0, ביט אחר ביט, עד המצב הפתוח)", LL3, PATH3], lambda q, p: (p, 0x7))])

# a combination lock: two 2-bit symbols
LLK = "S = SW9 SW8 (HEX3)     symbol = SW7 SW6     next S = HEX0     open = LEDG0"
def lk_f(p, r):
    s, inb = fld(r, 2, 2)
    ns = (1 if inb == p[0] else 0) if s == 0 else (2 if inb == p[1] else (1 if inb == p[0] else 0)) if s == 1 else 2
    return {("G", 0): int(s == 2), **dig(0, ns)}
add("LOCK", "מנעול צירופים", [9, 8, 7, 6], OSN, [[9, 8], [7, 6], None, None], [(a, b) for a in range(4) for b in range(4)],
    lk_f, lambda p: f"code {p[0]:02b} then {p[1]:02b}", LLK,
    [(["בלוח החלק הצירופי של מנעול: שני סמלים (כל אחד שני מתגים) בצעדים, והיציאה דולקת אחרי הצירוף הנכון.", NOCLK, LLK,
       "מה הסמל הראשון? (מעביר מהמצב 0 למצב 1)", "SW1 SW0 = SW7 SW6"], lambda q, p: (p[0], 0x3)),
     (["ומה הסמל השני? (מעביר מהמצב 1 למצב 2)", LLK, "SW1 SW0 = SW7 SW6"], lambda q, p: (p[1], 0x3))])

# serial divisibility: a binary number enters MSB first; state = the remainder, the LED = divisible by m
LDV = "S = SW9 SW8 SW7 (HEX3)     bit = SW6 (HEX2)     next S = HEX0     Y = LEDG0"
def dv_f(m, r):
    s, a = fld(r, 3, 1)
    return {("G", 0): int(s == 0), **dig(0, (2 * s + a) % m if s < m else 0)}
add("DIVISIBLE", "מתחלק או לא?", [9, 8, 7, 6], OSN, [[9, 8, 7], [6], None, None], list(range(2, 8)), dv_f,
    lambda m: f"divisible by {m}", LDV,
    [(["בלוח החלק הצירופי של מכונה שקוראת מספר בינארי מהביט הגבוה. המצב הוא השארית, והיציאה דולקת כשהמספר עד עכשיו מתחלק.",
       NOCLK, LDV, "מהמצב 0 הכניסו 1, 1, 0 (המספר 6), בכל פעם עם מעבר למצב הבא. היציאה דולקת במצב שהגעתם אליו?"]
      + UP0("דולקת", "כבויה"), lambda q, m: (int(6 % m == 0), 0x1)),
     (["במה המספר מתחלק כשהיציאה דולקת?", LDV] + cnt(7, 2), lambda q, m: (m, 0xF)),
     (["כמה מצבים יש למכונה? (מצב לכל שארית)"] + cnt(8), lambda q, m: (m, 0xF))])

# two interacting FSMs: A flips every step, B counts only when A is in a certain state
LTF = "A = SW9 (HEX3)     B = SW8 SW7 SW6 (HEX2)     next A = LEDG0     next B = HEX0"
def tf_f(p, r):
    ph, n = p
    t, b = fld(r, 1, 3)
    if b >= n:
        b = 0
    return {("G", 0): 1 - t, **dig(0, (b + 1) % n if t == ph else b)}
add("TWOFSM", "שתי מכונות שמדברות", [9, 8, 7, 6], [("G", 0)] + hexd(0), [[9], [8, 7, 6], None, None],
    [(ph, n) for ph in range(2) for n in range(3, 8)], tf_f, lambda p: f"B counts when A = {p[0]}, modulo {p[1]}", LTF,
    [(["בלוח החלק הצירופי של שתי מכונות: מכונה א' מתהפכת בכל צעד, ומכונה ב' סופרת, אבל רק כשמכונה א' במצב מסוים.",
       NOCLK0, LTF, "כמה מצבים יש למכונה ב'? (מ-0, צעד אחר צעד, עד שהיא חוזרת ל-0)", FWD] + cnt(7),
      lambda q, p: (p[1], 0xF)),
     (["מכונה ב' מתקדמת כשמכונה א' במצב", LTF] + UP0("1", "0"), lambda q, p: (p[0], 0x1))])

# a round-robin or fixed-priority arbiter (state = V: someone has the grant, W: who)
LAR1 = "V = SW9 (a grant)     W = SW8 (who)     requests: SW7 (1), SW6 (0)"
LAR2 = "next V W = LEDG3 LEDG2     grants now: LEDG1 (1), LEDG0 (0)"
def ar_next(p, s, r1, r0):
    fx, first = p
    if r1 and r0:
        g = first if fx else (1 - (s & 1) if s >> 1 else first)
    elif r1 or r0:
        g = r1
    else:
        return s & 1
    return 2 | g
def ar_f(p, r):
    s, r1, r0 = fld(r, 2, 1, 1)
    ns = ar_next(p, s, r1, r0)
    return {("G", 3): ns >> 1, ("G", 2): ns & 1, ("G", 1): int(s == 3), ("G", 0): int(s == 2)}
add("ARBITER", "בורר בקשות", [9, 8, 7, 6], [("G", 3), ("G", 2), ("G", 1), ("G", 0)], [None, None, None, None],
    [(fx, first) for fx in range(2) for first in range(2)], ar_f,
    lambda p: f"{'fixed priority' if p[0] else 'round robin'}, first = {p[1]}", LAR1 + "     " + LAR2,
    [(["בלוח החלק הצירופי של בורר: שתי בקשות, ובכל צעד הוא נותן אישור לאחת.", NOCLK, LAR1, LAR2,
       "במצב 00 (עוד אין אישור) ושתי הבקשות למעלה: מי מקבל את האישור בצעד הבא?"] + code(["0", "1"]),
      lambda q, p: (p[1], 0x1)),
     (["עם שתי הבקשות למעלה, צעד אחר צעד: האישור מתחלף (סבב) או נשאר לאותה בקשה (עדיפות קבועה)?", FWD, LAR1, LAR2]
      + code(["round robin", "fixed"]), lambda q, p: (p[0], 0x1))])

# ================================================================ easy questions straight from the slides
# the case to try is shown on HEX (a constant per variant); the board = the slide's logic, exactly
NOCLKN = "בלי שעון: במתגים שמים מצב נוכחי וכניסות, ובלוח רואים את המצב הבא."
CASE = "שימו במתגים את המקרה שבתצוגה. מה המצב הבא?"
ENC = "S0 = 00     S1 = 01     S2 = 10"
LMO = "S1 S0 = SW9 SW8     A = SW7     next S1 S0 = LEDG3 LEDG2     Y = LEDG0"
SMILE = UP0("מחייך", "לא מחייך")
def moore_ns(s, a):				# slides 4, 7: S1' = S0 A, S0' = A' (code 11 too, by the equations)
    return ((s & 1 & a) << 1) | (1 - a)
def moore_eq(r):				# + slide 5: Y = S1
    s, a = fld(r, 2, 1)
    ns = moore_ns(s, a)
    return {("G", 3): ns >> 1, ("G", 2): ns & 1, ("G", 0): s >> 1}

# topic 1: the Moore snail's next-state circuit (slides 4, 7), one case from the HEX
add("MOORESLIDE", "חילזון מור מהשקופית", [9, 8, 7], OSS + hexd(1) + hexd(0), [None] * 4,
    [(s, a) for s in range(3) for a in range(2)], lambda p, r: {**moore_eq(r), **dig(1, p[0]), **dig(0, p[1])},
    lambda p: f"case S{p[0]}, A = {p[1]}: next {moore_ns(p[0], p[1]):02b}, Y = {int(p[0] == 2)}",
    LMO + "     case: state = HEX1, A = HEX0",
    [(["חילזון מור, שקופיות 4 ו-7: המעגל של המצב הבא.", "S1' = S0 A     S0' = A'     Y = S1", NOCLK, ENC, LMO,
       "the case:   state = HEX1     A = HEX0", CASE, "SW1 SW0 = next S1 S0"], lambda q, p: (moore_ns(*p), 0x3)),
     (["החילזון מחייך במצב הזה?", "Y = LEDG0"] + SMILE, lambda q, p: (int(p[0] == 2), 0x1))])

# topic 1: the Mealy snail (slides 6, 8): S0' = A', Y = S0 A, one case from the HEX
LMEA = "S0 = SW9     A = SW8     next S0 = LEDG1     Y = LEDG0"
def mealy_eq(r):
    s, a = fld(r, 1, 1)
    return {("G", 1): 1 - a, ("G", 0): s & a}
add("MEALYSLIDE", "חילזון מילי מהשקופית", [9, 8], [("G", 1), ("G", 0)] + hexd(1) + hexd(0), [None] * 4,
    [(s, a) for s in range(2) for a in range(2)], lambda p, r: {**mealy_eq(r), **dig(1, p[0]), **dig(0, p[1])},
    lambda p: f"case S0 = {p[0]}, A = {p[1]}: next {1 - p[1]}, Y = {p[0] & p[1]}", LMEA + "     case: S0 = HEX1, A = HEX0",
    [(["חילזון מילי, שקופיות 6 ו-8: ביט מצב אחד.", "S0' = A'     Y = S0 A", NOCLK, LMEA,
       "the case:   S0 = HEX1     A = HEX0", CASE] + UP0("1", "0"), lambda q, p: (1 - p[1], 0x1)),
     (["החילזון מחייך עכשיו?", "Y = LEDG0"] + SMILE, lambda q, p: (p[0] & p[1], 0x1))])

# topic 1: the Moore snail on two tape bits from the HEX (slides 3-4)
def moore_run(bits):
    s = 0
    for a in bits:
        s = moore_ns(s, a)
    return s
add("MOORESTEP", "חילזון מור על שני ביטים", [9, 8, 7], OSS + hexd(1) + hexd(0), [None] * 4, list(range(4)),
    lambda p, r: {**moore_eq(r), **dig(1, p >> 1), **dig(0, p & 1)},
    lambda p: f"tape {p:02b}: ends in {moore_run(pbits(p, 2)):02b}", LMO + "     tape: HEX1, HEX0",
    [(["חילזון מור, שקופית 4: שני ביטים על הסרט.", NOCLK, LMO, "the tape:   first bit = HEX1     second bit = HEX0",
       "מתחילים במצב 00. שימו בכניסה את הביט הראשון, והעבירו את המצב הבא אל מתגי המצב.",
       "אחר כך אותו דבר עם הביט השני. לאיזה מצב הגעתם?", "SW1 SW0 = S1 S0"],
      lambda q, p: (moore_run(pbits(p, 2)), 0x3)),
     (["החילזון מחייך במצב הזה?", "Y = LEDG0"] + SMILE, lambda q, p: (int(moore_run(pbits(p, 2)) == 2), 0x1))])

# topic 2: the mode FSM of slide 14 (S0 -P-> S1, S1 -R-> S0), one case from the HEX
LMS = "M = SW9     P = SW8     R = SW7     next M = LEDG0"
def mode14(m, p_, r_):
    return 1 - r_ if m else p_
def mode2(p):
    return mode14(mode14(*p), p[1], p[2])
add("MODESLIDE", "מכונת מצב התהלוכה מהשקופית", [9, 8, 7], [("G", 0)] + hexd(2) + hexd(1) + hexd(0), [None] * 4,
    list(itertools.product(range(2), repeat=3)),
    lambda p, r: {("G", 0): mode14(*fld(r, 1, 1, 1)), **dig(2, p[0]), **dig(1, p[1]), **dig(0, p[2])},
    lambda p: f"case M P R = {p[0]}{p[1]}{p[2]}: next M {mode14(*p)}, then {mode2(p)}", LMS + "     case: HEX2 HEX1 HEX0",
    [(["מכונת מצב התהלוכה, שקופית 14: ביט מצב אחד.", NOCLKN, LMS, "the case:   M = HEX2     P = HEX1     R = HEX0", CASE]
      + UP0("1", "0"), lambda q, p: (mode14(*p), 0x1)),
     ([FWD, "השאירו את הכניסות. מה המצב הבא עכשיו?", LMS] + UP0("1", "0"), lambda q, p: (mode2(p), 0x1))])

# topic 2: the lights FSM of slide 14 (S0 stays on TA, S2 stays on M + TB), one case from the HEX
LLS = "S = SW9 SW8     M = SW7     TA = SW6     TB = SW5     next S = LEDG1 LEDG0"
S4 = code(["S0", "S1", "S2", "S3"])
def lights1(p):
    s, m, ta, tb = p
    return lights_next(s, ta, tb, m, 1)
def lights2(p):
    return lights1((lights1(p),) + tuple(p[1:]))
def ls_f(p, r):
    ns = lights1(fld(r, 2, 1, 1, 1))
    return {("G", 1): ns >> 1, ("G", 0): ns & 1, **dig(3, p[0]), **dig(2, p[1]), **dig(1, p[2]), **dig(0, p[3])}
add("LIGHTSSLIDE", "מכונת הרמזורים מהשקופית", [9, 8, 7, 6, 5], [("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1) + hexd(0),
    [None] * 4, list(itertools.product(range(4), range(2), range(2), range(2))), ls_f,
    lambda p: f"case S{p[0]} M{p[1]} TA{p[2]} TB{p[3]}: next S{lights1(p)}, then S{lights2(p)}",
    LLS + "     case: HEX3..HEX0",
    [(["מכונת הרמזורים, שקופית 14.", NOCLKN, LLS, "the case:   S = HEX3     M = HEX2     TA = HEX1     TB = HEX0", CASE]
      + S4, lambda q, p: (lights1(p), 0x3)),
     ([FWD, "השאירו את הכניסות. מה המצב הבא עכשיו?", LLS] + S4, lambda q, p: (lights2(p), 0x3))])

# topic 3: the design of the Moore snail leaves code 11 unused - what do the equations of slide 7 do there?
add("CODE11", "הקוד שלא בשימוש", [9, 8, 7], OSS + hexd(0), [None] * 4, [0, 1],
    lambda p, r: {**moore_eq(r), **dig(0, p)}, lambda p: f"A = {p}: 11 -> {moore_ns(3, p):02b}", LMO + "     A to try = HEX0",
    [(["תכנון חילזון מור, שקופית 7: בקידוד הקוד 11 לא בשימוש. מה המעגל עושה בו?", "S1' = S0 A     S0' = A'     Y = S1",
       NOCLK, LMO, "שימו במתגי המצב 11. החילזון מחייך?", "Y = LEDG0"] + SMILE, lambda q, p: (1, 0x1)),
     (["the input to try:   A = HEX0", "שימו בכניסה את הערך שבתצוגה. מה המצב הבא?", LMO, "SW1 SW0 = next S1 S0"],
      lambda q, p: (moore_ns(3, p), 0x3)),
     (["לאיזה מצב של החילזון הוא עבר?", ENC] + code(["S0", "S1", "S2"]), lambda q, p: (2 if p else 1, 0x3))])

# topic 3: the schematic of slide 7 - the three outputs on LEDs in a hidden order
LSG = "S1 S0 = SW9 SW8     A = SW7     Y, S0', S1' = LEDG2, LEDG1, LEDG0 (in some order)"
L3 = code(["LEDG2", "LEDG1", "LEDG0"])
def sg_f(perm, r):				# perm[i] = the signal on LEDG(2 - i): 0 Y, 1 S0', 2 S1'
    e = moore_eq(r)
    sig = [e[("G", 0)], e[("G", 2)], e[("G", 3)]]
    return {("G", 2 - i): sig[perm[i]] for i in range(3)}
add("MOOREGATES", "השרטוט של חילזון מור", [9, 8, 7], [("G", 2), ("G", 1), ("G", 0)], [None] * 4,
    list(itertools.permutations(range(3))), sg_f,
    lambda p: "LEDG2..0 = " + " ".join(["Y", "S0'", "S1'"][x] for x in p), LSG,
    [(["השרטוט של חילזון מור, שקופית 7: שלוש היציאות של המעגל על נורות בסדר נסתר.", "Y = S1     S0' = A'     S1' = S0 A",
       NOCLK, LSG, "איזו נורה היא היציאה? היא תלויה רק במתג השמאלי."] + L3, lambda q, p: (p.index(0), 0x3)),
     (["איזו נורה היא המצב הבא הימני (המהפך)? היא דולקת כשהכניסה 0.", LSG] + L3, lambda q, p: (p.index(1), 0x3)),
     (["איזו נורה היא המצב הבא השמאלי (שער וגם)?", LSG] + L3, lambda q, p: (p.index(2), 0x3))])

# topic 3: the Mealy snail (slide 8) on three tape bits from the HEX
def mealy_run(bits):
    s, n = 0, 0
    for a in bits:
        n += s & a
        s = 1 - a
    return n
TP3 = "the tape:   first bit = HEX2     second = HEX1     third = HEX0"
add("MEALYTAPE", "חילזון מילי על שלושה ביטים", [9, 8], [("G", 1), ("G", 0)] + hexd(2) + hexd(1) + hexd(0), [None] * 4,
    list(range(8)), lambda p, r: {**mealy_eq(r), **dig(2, p >> 2), **dig(1, (p >> 1) & 1), **dig(0, p & 1)},
    lambda p: f"tape {p:03b}: {mealy_run(pbits(p, 3))} smiles", LMEA + "     tape: HEX2 HEX1 HEX0",
    [(["חילזון מילי, שקופית 8: שלושה ביטים על הסרט.", NOCLK, LMEA, TP3,
       "מתחילים במצב 0. שימו בכניסה את הביט הראשון. מה המצב הבא?"] + UP0("1", "0"), lambda q, p: (1 - (p >> 2), 0x1)),
     (["בכל ביט: שימו אותו בכניסה, הסתכלו על היציאה, והעבירו את המצב הבא אל מתג המצב.", TP3, LMEA,
       "כמה פעמים החילזון חייך לאורך שלושת הביטים?"] + cnt(3, 0), lambda q, p: (mealy_run(pbits(p, 3)), 0xF))])

# ================================================================ more easy questions straight from the slides
# topic 1: the Moore snail's encoding (slide 4) and its self-loops (slide 3); the state number is on HEX0
add("MOORECODE", "הקוד של מצב בחילזון מור", [9, 8, 7], OSS + hexd(0), [None] * 4, [0, 1, 2],
    lambda k, r: {**moore_eq(r), **dig(0, k)},
    lambda k: f"S{k} = {k:02b}, stays with {['A = 1', 'A = 0', 'none'][k]}", LMO + "     the state: HEX0",
    [(["חילזון מור, שקופיות 3-4: טבלת הקידוד.", ENC, "the state:   S = HEX0 (its number)",
       "מה הקוד של המצב שבתצוגה?", "SW1 SW0 = S1 S0"], lambda q, k: (k, 0x3)),
     (["שימו את הקוד במתגי המצב ונסו את שני ערכי הכניסה. באיזה ערך המצב הבא שווה למצב הנוכחי?", LMO]
      + code(["0", "1", "none"], 3), lambda q, k: ([1, 0, 2][k], 0x3))])

# topic 1: one arrow of the Moore snail's diagram (slide 3): from the state on HEX1 to the state on HEX0
ARR = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 1)]
def arr_a(s, t):
    return [a for a in range(2) if moore_ns(s, a) == t][0]
add("MOOREARROW", "חץ בדיאגרמה של חילזון מור", [9, 8, 7], OSS + hexd(1) + hexd(0), [None] * 4, ARR,
    lambda p, r: {**moore_eq(r), **dig(1, p[0]), **dig(0, p[1])},
    lambda p: f"S{p[0]} -> S{p[1]} with A = {arr_a(*p)}", LMO + "     the arrow: HEX1 -> HEX0",
    [(["חילזון מור, שקופיות 3-4: חץ אחד בדיאגרמת המצבים.", NOCLK, ENC, LMO, "the arrow:   from state HEX1 to state HEX0",
       "שימו במתגי המצב את הקוד של מצב המוצא. איזה ערך כניסה מוביל אל מצב היעד?"] + UP0("1", "0"),
      lambda q, p: (arr_a(*p), 0x1)),
     (["ובמצב היעד - החילזון מחייך?", ENC, LMO] + SMILE, lambda q, p: (int(p[1] == 2), 0x1))])

# topic 1: one arrow of the Mealy snail (slide 6): which input, and a smile on the way
add("MEALYARROW", "חץ בחילזון מילי", [9, 8], [("G", 1), ("G", 0)] + hexd(1) + hexd(0), [None] * 4,
    [(s, t) for s in range(2) for t in range(2)], lambda p, r: {**mealy_eq(r), **dig(1, p[0]), **dig(0, p[1])},
    lambda p: f"S{p[0]} -> S{p[1]} with A = {1 - p[1]}, Y = {p[0] & (1 - p[1])}", LMEA + "     the arrow: HEX1 -> HEX0",
    [(["חילזון מילי, שקופית 6: חץ אחד בדיאגרמה.", NOCLK, "S0 = 0     S1 = 1", LMEA,
       "the arrow:   from state HEX1 to state HEX0", "שימו את מצב המוצא. איזה ערך כניסה מוביל אל מצב היעד?"] + UP0("1", "0"),
      lambda q, p: (1 - p[1], 0x1)),
     (["בחץ הזה (מצב המוצא והכניסה שמצאתם) - החילזון מחייך?", LMEA] + SMILE, lambda q, p: (p[0] & (1 - p[1]), 0x1))])

# topic 1: the timing diagram (slide 9): Moore smiles one bit after Mealy; a 4-bit tape on HEX3..HEX0
def moore_first(t):				# the 1-based tape bit during which Y (= S1) is first on, or None
    s = 0
    for j, a in enumerate(pbits(t, 4), 1):
        if s >> 1:
            return j
        s = moore_ns(s, a)
TP4 = "the tape:   bit 1 = HEX3     bit 2 = HEX2     bit 3 = HEX1     bit 4 = HEX0"
add("MOORETIME", "מתי מחייך מור ומתי מילי?", [9, 8, 7], OSS + hexd(3) + hexd(2) + hexd(1) + hexd(0), [None] * 4,
    [t for t in range(16) if moore_first(t)],
    lambda t, r: {**moore_eq(r), **dig(3, t >> 3), **dig(2, (t >> 2) & 1), **dig(1, (t >> 1) & 1), **dig(0, t & 1)},
    lambda t: f"tape {t:04b}: Moore at bit {moore_first(t)}, Mealy at bit {moore_first(t) - 1}", LMO + "     tape: HEX3..HEX0",
    [(["חילזון מור, שקופית 9: דיאגרמת הזמנים על סרט של ארבעה ביטים.", NOCLK, LMO, TP4,
       "מתחילים במצב 00. בכל ביט: שימו אותו בכניסה, הסתכלו על היציאה, והעבירו את המצב הבא אל מתגי המצב.",
       "בזמן איזה ביט (המספר שלו) היציאה דולקת בפעם הראשונה?"] + cnt(4), lambda q, t: (moore_first(t), 0xF)),
     (["לפי שקופית 9 חילזון מילי מחייך ביט אחד קודם. בזמן איזה ביט הוא מחייך בפעם הראשונה?", TP4] + cnt(4),
      lambda q, t: (moore_first(t) - 1, 0xF))])

# topic 2: the unfactored FSM of slide 13 (S0..S7 = 4 M + lights): the lights of a state from HEX0
LUF = "S = SW9 SW8 SW7 (state number 0-7)"
COL = code(["green", "yellow", "red"], 3)
S4 = code(["S0", "S1", "S2", "S3"])
add("UNFACTLIGHTS", "הרמזורים במכונה הלא מפורקת", [9, 8, 7], LGT + hexd(0), [None] * 4, list(range(8)),
    lambda k, r: {**tl_leds(r & 3), **dig(0, k)},
    lambda k: f"S{k}: lights state {k & 3}, M = {k >> 2}", LUF + "     lights LEDG7..5, LEDG2..0     the state: HEX0",
    [(["המכונה הלא מפורקת של שקופית 13: שמונה מצבים, ובכל אחד צבע לכל רחוב.", LUF, "the state:   HEX0"] + LIGHTS
      + ["שימו את המצב שבתצוגה. מה הצבע של רחוב א'?", "LA = ?"] + COL, lambda q, k: (TL_OUT[k & 3][0], 0x3)),
     (["ומה הצבע של רחוב ב'?", "LB = ?"] + LIGHTS + COL, lambda q, k: (TL_OUT[k & 3][1], 0x3)),
     (["באיזה מצב של מכונת הרמזורים המפורקת (שקופית 14) יש אותם צבעים?", "the state:   HEX0", LPH] + S4, lambda q, k: (k & 3, 0x3))])

# topic 2: the unfactored FSM of slide 13 - its next state, read from the diagram
def unf_next(s, p_, r_, ta, tb):
    m, l = s >> 2, s & 3
    nm = p_ if m == 0 else 1 - r_
    return 4 * nm + lights_next(l, ta, tb, m and nm, 1)
LUN = "S = SW9 SW8 SW7     P = SW6     R = SW5     TA = SW4     TB = SW3     next S = HEX0"
NUM8 = cnt(7, 0)
def unf_row(r):
    return unf_next(*fld(r, 3, 1, 1, 1, 1))
add("UNFACTPR", "מתי בודקים כל כניסה?", [9, 8, 7, 6, 5, 4, 3], hexd(1) + hexd(0), [None] * 4, list(range(8)),
    lambda k, r: {**dig(1, k), **dig(0, unf_row(r))},
    lambda k: f"S{k}: {'PR'[k >> 2]} matters, idle next S{unf_next(k, 0, 0, 0, 0)}", LUN + "     the state: HEX1",
    [(["המכונה הלא מפורקת של שקופית 13.", NOCLKN, LUN, "the state:   HEX1",
       "שימו את המצב שבתצוגה. איזו מבין שתי הכניסות האלה משנה את המצב הבא?"] + code(["P", "R"]),
      lambda q, k: (k >> 2, 0x1)),
     (["כל הכניסות למטה. מה המצב הבא?", LUN, "SW2 SW1 SW0 = next S"] + NUM8,
      lambda q, k: (unf_next(k, 0, 0, 0, 0), 0x7))])

def unf2(p):
    s, x, t = p
    return unf_next(unf_next(s, x, x, t, t), x, x, t, t)
add("UNFACTNEXT", "צעד במכונה הלא מפורקת", [9, 8, 7, 6, 5, 4, 3], hexd(3) + hexd(2) + hexd(1) + hexd(0), [None] * 4,
    [(s, x, t) for s in range(8) for x in range(2) for t in range(2)],
    lambda p, r: {**dig(3, p[0]), **dig(2, p[1]), **dig(1, p[2]), **dig(0, unf_row(r))},
    lambda p: f"case S{p[0]} P=R={p[1]} TA=TB={p[2]}: next S{unf_next(p[0], p[1], p[1], p[2], p[2])}, then S{unf2(p)}",
    LUN + "     case: HEX3 HEX2 HEX1",
    [(["המכונה הלא מפורקת של שקופית 13.", NOCLKN, LUN, "the case:   S = HEX3     P = R = HEX2     TA = TB = HEX1",
       CASE, "SW2 SW1 SW0 = next S"] + NUM8, lambda q, p: (unf_next(p[0], p[1], p[1], p[2], p[2]), 0x7)),
     ([FWD, "השאירו את הכניסות. מה המצב הבא עכשיו?", LUN, "SW2 SW1 SW0 = next S"] + NUM8, lambda q, p: (unf2(p), 0x7))])

# topic 2: the factored controller of slide 14: a parade starts (P for one step), how long until B is green
LPS1 = "M = SW9     lights = SW8 SW7     TA = SW6     TB = SW5     P = SW4     R = SW3"
LPS2 = "next M = LEDG4     next lights = HEX0"
LPS3 = "the start:   M = 0     lights = HEX2     TA = TB = 0 (no cars)"
def ps_row(r):
    m, l, ta, tb, p_, r_ = fld(r, 1, 2, 1, 1, 1, 1)
    return {("G", 4): mode14(m, p_, r_), **dig(0, lights_next(l, ta, tb, m, 1))}
def ps_steps(k):
    m, l, n = 0, k, 0
    while True:
        p_ = int(n == 0)
        m, l, n = mode14(m, p_, 0), lights_next(l, 0, 0, m, 1), n + 1
        if l == 2:
            return n
add("PARADESTART", "התהלוכה מתחילה", [9, 8, 7, 6, 5, 4, 3], [("G", 4)] + hexd(2) + hexd(0), [None] * 4, list(range(4)),
    lambda k, r: {**ps_row(r), **dig(2, k)}, lambda k: f"start lights {k}: first next {(k + 1) & 3}, B green after {ps_steps(k)}",
    LPS1 + "     " + LPS2 + "     start: HEX2",
    [(["בקר הרמזור המפורק של שקופית 14: מכונת המצב ומכונת הרמזורים יחד.", NOCLKN, LPS1, LPS2, LPS3,
       "שימו את ההתחלה והרימו את המתג של התהלוכה. מה המצב הבא של הרמזורים?", "P = 1"] + S4,
      lambda q, k: ((k + 1) & 3, 0x3)),
     ([FWD, "בצעד הבא הורידו את המתג של התהלוכה, והמשיכו צעד אחר צעד.", "P = 0     next M -> SW9     next lights -> SW8 SW7",
       LPS2, "כמה צעדים בסך הכול (כולל הראשון) עד שהמצב הבא של הרמזורים הוא 2 (רחוב ב' ירוק)?"] + cnt(4),
      lambda q, k: (ps_steps(k), 0x7))])

# topic 3: a machine of one state bit (like the Mealy snail's S0' = A' of slide 8): which next-state equation?
EQ1 = ["S' = A", "S' = A'", "S' = S xor A", "S' = S + A", "S' = S A"]
def eq1(e, s, a):
    return [a, 1 - a, s ^ a, s | a, s & a][e]
LE1 = "S = SW9     A = SW8     next S = LEDG0"
add("TWOSTATE", "מכונה של ביט מצב אחד", [9, 8], [("G", 0)], [[9], [8], None, None], list(range(5)),
    lambda e, r: {("G", 0): eq1(e, *fld(r, 1, 1))}, lambda e: EQ1[e], LE1,
    [(["מכונה של ביט מצב אחד, כמו החילזון של שקופית 8 (שם המצב הבא הוא היפוך הכניסה).", NOCLK, LE1,
       "במצב 0 עם כניסה 1: מה המצב הבא?"] + UP0("1", "0"), lambda q, e: (eq1(e, 0, 1), 0x1)),
     (["נסו את ארבעת המקרים. מה משוואת המצב הבא?", LE1] + code(EQ1, 3), lambda q, e: (e, 0x7))])

# topic 3: the snail of slide 4 designed again with a one-hot encoding
LOH1 = "state bits = SW9 SW8 SW7 (one-hot)     A = SW6"
LOH2 = "next state bits = LEDG2 LEDG1 LEDG0     Y = LEDG4"
OHE = "S0 = 001     S1 = 010     S2 = 100"
def oh_f(p, r):
    b2, b1, b0, a = fld(r, 1, 1, 1, 1)
    n = (b1 & a) << 2 | (1 - a) << 1 | ((b0 | b2) & a)
    return {("G", 4): b2, ("G", 2): n >> 2, ("G", 1): (n >> 1) & 1, ("G", 0): n & 1, **dig(1, p[0]), **dig(0, p[1])}
add("ONEHOTSNAIL", "חילזון מור בקידוד אחד-חם", [9, 8, 7, 6], [("G", 4), ("G", 2), ("G", 1), ("G", 0)] + hexd(1) + hexd(0),
    [None] * 4, [(k, a) for k in range(3) for a in range(2)], oh_f,
    lambda p: f"S{p[0]}, A = {p[1]}: next S{moore_ns(*p)} = {1 << moore_ns(*p):03b}, binary {moore_ns(*p):02b}",
    LOH1 + "     " + LOH2 + "     case: HEX1 HEX0",
    [(["החילזון של שקופית 4 בקידוד אחר: ביט מצב לכל מצב (אחד-חם).", NOCLK, OHE, LOH1, LOH2,
       "the case:   state number = HEX1     A = HEX0", "שימו את המקרה. מה המצב הבא?", "SW2 SW1 SW0 = next (one-hot)"],
      lambda q, p: (1 << moore_ns(*p), 0x7)),
     (["אותו מעבר בקידוד הבינארי של שקופית 4: מה הקוד של המצב הבא?", ENC, "SW1 SW0 = next S1 S0"],
      lambda q, p: (moore_ns(*p), 0x3))])

# topic 3: a counter modulo 3 with an enable, designed like the snail (Y = S1 as in slide 5, code 11 -> 00)
def en3(s, a):
    return 0 if s == 3 else (s + a) % 3
def en3_f(k, r):
    s, a = fld(r, 2, 1)
    ns = en3(s, a)
    return {("G", 3): ns >> 1, ("G", 2): ns & 1, ("G", 0): s >> 1, **dig(0, k)}
add("ENABLE3", "מונה של שלושה מצבים עם אפשור", [9, 8, 7], OSS + hexd(0), [None] * 4, [0, 1, 2], en3_f,
    lambda k: f"start {k:02b}: {(3 - k) % 3 or 3} steps back to 00", LMO + "     the start: HEX0",
    [(["מכונה בתכנון כמו החילזון של שקופיות 4-5: מונה של שלושה מצבים שמתקדם רק כשהכניסה 1.", NOCLK, LMO,
       "the start:   state number = HEX0", "שימו את ההתחלה וכניסה 0. מה המצב הבא?", "SW1 SW0 = next S1 S0"],
      lambda q, k: (k, 0x3)),
     (["עם כניסה 1, צעד אחר צעד: כמה צעדים עד שחוזרים למצב 00?", FWD, LMO] + cnt(3), lambda q, k: ((3 - k) % 3 or 3, 0x3))])

ORDER = ["MOORESLIDE", "MEALYSLIDE", "MOORESTEP", "MOORECODE", "MOOREARROW", "MEALYARROW", "MOORETIME", "NSTATES", "SNAIL", "SNAILSTATES", "SNAILNEXT", "SNAILMEALY", "SNAILTIME", "TAPE", "TWOSNAILS", "ONES", "EDGE", "OVERLAP",
         "MODESLIDE", "LIGHTSSLIDE", "UNFACTLIGHTS", "UNFACTPR", "UNFACTNEXT", "PARADESTART", "MODEFSM", "PARADE", "PARADEPINS", "PARADEWAIT", "FACTORCOUNT", "TIMERLIGHT", "TWODIGITS",
         "CODE11", "MOOREGATES", "MEALYTAPE", "TWOSTATE", "ONEHOTSNAIL", "ENABLE3", "BLINK", "PARITY", "COUNTONES", "SATURATE", "UPDOWN", "SEQCOUNT", "DEBOUNCE", "LOCK3", "LOCK", "DIVISIBLE", "VENDING",
         "TWOFSM", "ARBITER"]
TOPICS = [(40, "החילזון: מור ומילי", 18), (40, "פירוק מכונות: התהלוכה", 13), (40, "תכנון מכונות מצבים", 19)]
DESC = {"MOORECODE": "חילזון מור: הקוד של המצב שבתצוגה, ובאיזו כניסה הוא נשאר",
        "MOOREARROW": "חילזון מור: איזו כניסה על החץ שבתצוגה",
        "MEALYARROW": "חילזון מילי: איזו כניסה על החץ שבתצוגה, והאם מחייך",
        "MOORETIME": "דיאגרמת הזמנים: מתי מחייך מור ומתי מילי על הסרט שבתצוגה",
        "UNFACTLIGHTS": "המכונה הלא מפורקת: הצבעים של המצב שבתצוגה",
        "UNFACTPR": "המכונה הלא מפורקת: איזו כניסה חשובה במצב שבתצוגה",
        "UNFACTNEXT": "המכונה הלא מפורקת: המצב הבא, צעד ועוד צעד",
        "PARADESTART": "הבקר המפורק: כמה צעדים מהתחלת התהלוכה עד ירוק ברחוב ב'",
        "TWOSTATE": "מכונה של ביט מצב אחד: מה משוואת המצב הבא",
        "ONEHOTSNAIL": "חילזון מור בקידוד אחד-חם: המצב הבא בשני הקידודים",
        "ENABLE3": "מונה של שלושה מצבים עם אפשור: כמה צעדים חזרה ל-00",
        "MOORESLIDE": "חילזון מור מהשקופית: המצב הבא והיציאה במקרה שבתצוגה",
        "MEALYSLIDE": "חילזון מילי מהשקופית: המצב הבא והיציאה במקרה שבתצוגה",
        "MOORESTEP": "חילזון מור מהשקופית על שני ביטים: לאיזה מצב מגיעים",
        "MODESLIDE": "מכונת מצב התהלוכה מהשקופית: המצב הבא, צעד ועוד צעד",
        "LIGHTSSLIDE": "מכונת הרמזורים מהשקופית: המצב הבא, צעד ועוד צעד",
        "CODE11": "חילזון מור: מה המשוואות עושות בקוד 11 שלא בשימוש",
        "MOOREGATES": "השרטוט של חילזון מור: איזו נורה היא כל יציאה",
        "MEALYTAPE": "חילזון מילי מהשקופית על שלושה ביטים: כמה חיוכים",
"NSTATES": "כמה מצבים צריך גלאי מור וגלאי מילי לרצף שבלוח",
        "SNAIL": "החילזון בלי שעון: מור או מילי, ועל איזה רצף הוא מחייך",
        "SNAILSTATES": "חילזון מור: הקודים של המצבים מתוך טבלת המעברים",
        "SNAILNEXT": "חילזון מור: טבלת המעברים מהמצב שבו הוא מחייך",
        "SNAILMEALY": "חילזון מילי: המצב הבא וטבלת היציאה",
        "SNAILTIME": "מור או מילי, ובאיזה ביט של סרט נתון החיוך הראשון",
        "TAPE": "מעקב צעד אחר צעד: כמה פעמים החילזון מחייך על סרט נתון",
        "TWOSNAILS": "שני חלזונות: איזה מהם מילי, ועל איזה רצף",
        "ONES": "גלאי של כמה אחדות ברצף: האורך, ומספר המצבים במור ובמילי",
        "EDGE": "גלאי שינוי: מור או מילי; עלייה, ירידה או כל שינוי",
        "OVERLAP": "גלאי רצף: הרצף, וחופף או לא חופף",
        "MODEFSM": "מכונת מצב התהלוכה: איפוס, זיכרון, מי מנצח",
        "PARADE": "הרמזור עם תהלוכה: איזה מתג מתחיל, איזה רחוב נשאר ירוק",
        "PARADEPINS": "הרמזור עם תהלוכה: איזה מתג הוא כל כניסה",
        "PARADEWAIT": "כמה צעדים עד שהתהלוכה מקבלת ירוק",
        "FACTORCOUNT": "כמה מצבים עם פירוק ובלי",
        "TIMERLIGHT": "רמזור עם מכונת טיימר: כמה זמן כל ירוק",
        "TWODIGITS": "מונה של שתי ספרות: מצבים עם פירוק ובלי",
        "BLINK": "מהבהב: כמה דולק, כמה כבוי, כמה מצבים",
        "PARITY": "זוגיות טורית: איזה מתג, מור, זוגי או אי-זוגי",
        "COUNTONES": "מונה אחדות: איזה מתג, כמה מצבים",
        "SATURATE": "מונה שנעצר או חוזר ל-0",
        "UPDOWN": "מונה למעלה ולמטה: איזה מתג, איזה כיוון, כמה מצבים",
        "SEQCOUNT": "מונה בקוד בינארי, גריי או אחד-חם",
        "DEBOUNCE": "מסנן קפיצות: כמה צעדים להדלקה ולכיבוי, כמה מצבים",
        "LOCK3": "מנעול של שלושה ביטים שמתחיל מחדש בטעות",
        "LOCK": "מנעול צירופים של שני סמלים",
        "DIVISIBLE": "מכונה שבודקת התחלקות של מספר טורי",
        "VENDING": "מכונת שתייה: איזה מטבע, מה המחיר",
        "TWOFSM": "שתי מכונות שמדברות: מתי השנייה מתקדמת",
        "ARBITER": "בורר בקשות: סבב או עדיפות קבועה"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "מור ומילי, פירוק מכונות ותכנון - מהקל אל הקשה, ואי אפשר בלי הלוח")
