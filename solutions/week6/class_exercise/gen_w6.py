# -*- coding: utf-8 -*-
# Week 6 class exercise (lecture 6, Harris 3.4 + 4.6: finite state machines - Moore / Mealy, design procedure, the traffic
# light controller, state encodings, FSMs in SystemVerilog, sequence detectors). Instructor only.
#   python gen_w6.py [--compile] [--only Q05] [--id <ID>]
# Only one board button (KEY2 = check): there is no clock. The board holds the COMBINATIONAL part of a hidden FSM - the
# current state and the inputs are set on switches, the LEDs / HEX show the next state and the outputs. One clock =
# the student copies the next state onto the state switches.
import itertools, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(6, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0
rng = random.Random(606)
W = []

def dig(d, v):					# the outputs of HEX digit d showing v
    return {("H", (d, b)): (v >> b) & 1 for b in range(4)}
def ft(outs, nst, ni, f):			# tables: f(state, inb) -> {out: bit}; state = the high switches, inb = the low ones
    rows = [f(r >> ni, r & ((1 << ni) - 1)) for r in range(1 << (nst + ni))]
    return [[d[o] for d in rows] for o in outs]
FOLLOW = "שעון אחד = להציב במתגי המצב את המצב הבא."
NXH = "next state = HEX0"

# ================================================================ topic 1: state machines
# how many flip-flops: binary or one-hot, for a number shown on the board
VFF = list(range(3, 17))
W.append(Q(id="FFCOUNT", name="FFCOUNT", title="כמה דלגלגים?", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=VFF,
    tables=lambda n: const(bitsof(n // 10, 4) + bitsof(n % 10, 4)), answer=lambda n: ((n - 1).bit_length(), 0xF),
    describe=lambda n: f"{n} states: binary {(n - 1).bit_length()}, one-hot {n}",
    B=["the number of states = HEX1 HEX0     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר המצבים של מכונה. כמה דלגלגים צריך בקידוד אחד-חם (ביט לכל מצב)?"] +
            ["16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0"], lambda q, n: (n, 0x1F)),
           (["וכמה בקידוד בינארי?"] + cnt(4), lambda q, n: ((n - 1).bit_length(), 0xF))]))

# divide by N: the next state and the output of each state
VDN = [(n, k) for n in range(2, 10) for k in range(n)]
ODN = [("G", 0)] + hexd(0)
def dn_next(p, s):
    return (s + 1) % p[0] if s < p[0] else 0
LDN = "S = SW9 SW8 SW7 SW6   (HEX3)"
W.append(Q(id="DIVN", name="DIVN", title="מחלק ב-N", inputs=[9, 8, 7, 6], flat=True,
    outs=ODN, hexes=[[9, 8, 7, 6], None, None, None], variants=VDN,
    tables=lambda p: ft(ODN, 4, 0, lambda s, a: {("G", 0): int(s == p[1]), **dig(0, dn_next(p, s))}),
    answer=lambda p: ((p[0] - 1).bit_length(), 0xF), describe=lambda p: f"divide by {p[0]}, q = 1 in S{p[1]}",
    B=[LDN + "     " + NXH + "     q = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מחלק תדר, בלי כניסות: המצב הנוכחי על המתגים, המצב הבא בתצוגה.", LDN + "     " + NXH, FOLLOW,
             "התחילו במצב 0. אחרי כמה שעונים חוזרים ל-0?", "divide by N:   N = ?"] + cnt(9), lambda q, p: (p[0], 0xF)),
           (["באיזה מצב היציאה דולקת? (זה גם מספר השעונים ממצב 0 עד שהיא נדלקת)", LDN + "     q = LEDG0", "0 = all down"] + cnt(8),
            lambda q, p: (p[1], 0xF)),
           (["כמה דלגלגים צריך לפחות לקידוד בינארי של המצבים?"] + cnt(4), lambda q, p: ((p[0] - 1).bit_length(), 0xF))]))

# a machine without inputs that enters a loop after a few states (a "tail" and a cycle)
def rho_var(r):
    t, c = r.randrange(4), r.randrange(2, 6)
    return (t, c, (0,) + tuple(r.sample(range(1, 8), t + c - 1)))
VRH = C.rv(65, 200, rho_var)
ORH = hexd(0)
def rho_next(p, s):
    t, c, o = p
    if s not in o:
        return 0
    i = o.index(s)
    return o[i + 1] if i + 1 < t + c else o[t]
LRH = "S = SW9 SW8 SW7   (HEX3)     " + NXH
W.append(Q(id="RHO", name="RHO", title="שובל ומחזור", inputs=[9, 8, 7], flat=True,
    outs=ORH, hexes=[[9, 8, 7], None, None, None], variants=VRH,
    tables=lambda p: ft(ORH, 3, 0, lambda s, a: dig(0, rho_next(p, s))),
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"tail {p[0]}, cycle {p[1]}, order {p[2]}",
    B=[LRH + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה בלי כניסות: המצב הנוכחי על המתגים, המצב הבא בתצוגה.", LRH, FOLLOW,
             "התחילו במצב 0 ועקבו הרבה שעונים. כמה מצבים שונים אתם פוגשים (כולל 0)?"] + cnt(8), lambda q, p: (p[0] + p[1], 0xF)),
           (["כמה מהם מופיעים רק פעם אחת (לא חוזרים)?", LRH, "0 = all down"] + cnt(3), lambda q, p: (p[0], 0xF)),
           (["האחרים חוזרים במחזור. כל כמה שעונים המחזור חוזר?", LRH] + cnt(5), lambda q, p: (p[1], 0xF))]))

# a 2-state machine: the next-state table
ON2 = [("G", 0)]
LN2 = "S = SW9     a = SW8     next state = LEDG0"
def n2(p, s, a):
    return (p >> (3 - (2 * s + a))) & 1
W.append(Q(id="NEXT2", name="NEXT2", title="טבלת מעברים של שני מצבים", inputs=[9, 8], flat=True,
    outs=ON2, hexes=[None, None, None, None], variants=list(range(16)),
    tables=lambda p: ft(ON2, 1, 1, lambda s, a: {("G", 0): n2(p, s, a)}),
    answer=lambda p: (sum(n2(p, s, a) == s for s in range(2) for a in range(2)), 0x7),
    describe=lambda p: f"next(S, a) for S a = 00 01 10 11: {p:04b}",
    B=[LN2 + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה עם שני מצבים: המצב והכניסה על המתגים, המצב הבא בנורה.", LN2,
             "לכל מצב ולכל ערך של הכניסה: מה המצב הבא? מצב 1 - הרימו:",
             "S=0 a=0 -> SW3     S=0 a=1 -> SW2     S=1 a=0 -> SW1     S=1 a=1 -> SW0"], lambda q, p: (p, 0xF)),
           (["בכמה מארבעת המקרים המכונה נשארת באותו מצב?", "0 = all down"] + cnt(4),
            lambda q, p: (sum(n2(p, s, a) == s for s in range(2) for a in range(2)), 0x7))]))

# the next-state equation of a 2-state machine
EQN = ["a", "~a", "S ^ a", "~(S ^ a)", "~S", "S | a", "~S & a", "S | ~a"]
EQF = [lambda s, a: a, lambda s, a: 1 - a, lambda s, a: s ^ a, lambda s, a: 1 - (s ^ a),
       lambda s, a: 1 - s, lambda s, a: s | a, lambda s, a: (1 - s) & a, lambda s, a: s | (1 - a)]
W.append(Q(id="NEXTEQ", name="NEXTEQ", title="משוואת המצב הבא", inputs=[9, 8], flat=True,
    outs=ON2, hexes=[None, None, None, None], variants=list(range(8)),
    tables=lambda p: ft(ON2, 1, 1, lambda s, a: {("G", 0): EQF[p](s, a)}),
    answer=lambda p: (p, 0x7), describe=lambda p: f"S' = {EQN[p]}",
    B=[LN2 + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה עם שני מצבים: המצב והכניסה על המתגים, המצב הבא בנורה.", LN2,
             "מה המצב הבא ממצב 0? מצב 1 - הרימו:", "S=0 a=0 -> SW1     S=0 a=1 -> SW0"],
            lambda q, p: (EQF[p](0, 0) * 2 + EQF[p](0, 1), 0x3)),
           (["ומה המצב הבא ממצב 1? מצב 1 - הרימו:", LN2, "S=1 a=0 -> SW1     S=1 a=1 -> SW0"],
            lambda q, p: (EQF[p](1, 0) * 2 + EQF[p](1, 1), 0x3)),
           (["מה משוואת המצב הבא?", LN2, "S' = ?"] + code(EQN), lambda q, p: (p, 0x7))]))

# a Moore machine of 4 states: the output table
VO2 = [(y0, y1) for y0 in range(1, 15) for y1 in range(1, 15)]
VO2 = random.Random(61).sample(VO2, 190)
OO2 = [("G", 1), ("G", 0)]
LO2 = "S1 S0 = SW9 SW8   (HEX3)     Y1 Y0 = LEDG1 LEDG0"
SL4 = "S = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"
W.append(Q(id="OUTTAB", name="OUTTAB", title="טבלת יציאות של מכונת מור", inputs=[9, 8], flat=True,
    outs=OO2, hexes=[[9, 8], None, None, None], variants=VO2,
    tables=lambda p: ft(OO2, 2, 0, lambda s, a: {("G", 1): (p[1] >> s) & 1, ("G", 0): (p[0] >> s) & 1}),
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"Y0 by state 0..3: {[(p[0] >> s) & 1 for s in range(4)]}, Y1: {[(p[1] >> s) & 1 for s in range(4)]}",
    B=[LO2 + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של מכונת מור עם 4 מצבים: המצב על המתגים, היציאות בנורות.", LO2,
             "בכל מצב שבו", "Y0 = 1", "הרימו את המתג שלו:", SL4], lambda q, p: (p[0], 0xF)),
           (["אותו דבר בשביל", "Y1 = 1", LO2, SL4], lambda q, p: (p[1], 0xF))]))

# Moore or Mealy: does the output depend on the input switch?
def mm_dep(h):
    return sum(((h >> (2 * s)) & 1) != ((h >> (2 * s + 1)) & 1) for s in range(8))
def mm_vars():
    r = random.Random(62)
    moore = [sum(((o >> s) & 1) * 3 << (2 * s) for s in range(8)) for o in range(1, 255)]
    mealy = [h for h in range(1 << 16) if mm_dep(h)]
    return r.sample(moore, 112) + r.sample(mealy, 112)
OMM = [("G", 0)]
LMM = "S = SW9 SW8 SW7   (HEX3)     a = SW6     y = LEDG0"
W.append(Q(id="MOOREMEALY", name="MOOREMEALY", title="מור או מילי?", inputs=[9, 8, 7, 6], flat=True,
    outs=OMM, hexes=[[9, 8, 7], None, None, None], variants=mm_vars(),
    tables=lambda p: ft(OMM, 3, 1, lambda s, a: {("G", 0): (p >> (2 * s + a)) & 1}),
    answer=lambda p: (mm_dep(p), 0xF), describe=lambda p: f"{'Mealy' if mm_dep(p) else 'Moore'}, y depends on a in {mm_dep(p)} states",
    B=[LMM + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של מכונה עם 8 מצבים: המצב והכניסה על המתגים, היציאה בנורה.", LMM,
             "במור היציאה תלויה רק במצב. במילי - גם בכניסה.",
             "הציבו כמה מצבים, ובכל אחד הזיזו רק את הכניסה. איזו מכונה?"] + code(["Moore", "Mealy"]),
            lambda q, p: (int(mm_dep(p) > 0), 0x1)),
           (["בכמה מצבים היציאה תלויה בכניסה?", LMM, "0 = all down"] + cnt(8), lambda q, p: (mm_dep(p), 0xF))]))

# a 4-state machine with one input: the diagram
def reach(p):
    seen, fr = {0}, [0]
    while fr:
        s = fr.pop()
        for a in range(2):
            if p[2 * s + a] not in seen:
                seen.add(p[2 * s + a]); fr.append(p[2 * s + a])
    return seen
def sd_vars():
    r, out = random.Random(63), []
    while len(out) < 200:
        t = tuple(r.randrange(4) for _ in range(8))	# next[s*2 + a]
        if len(reach(t)) == 4 and t not in out:
            out.append(t)
    return out
OSD = hexd(0)
LSD = "S1 S0 = SW9 SW8   (HEX3)     a = SW7     " + NXH
def sd_tab(p):
    return ft(OSD, 2, 1, lambda s, a: dig(0, p[2 * s + a]))
SDA = "SW3 SW2 = next when a = 0     SW1 SW0 = next when a = 1     (binary)"
W.append(Q(id="STATEDIAG", name="STATEDIAG", title="דיאגרמת מצבים של 4 מצבים", inputs=[9, 8, 7], flat=True,
    outs=OSD, hexes=[[9, 8], None, None, None], variants=sd_vars(), tables=sd_tab,
    answer=lambda p: (p[6] * 4 + p[7], 0xF), describe=lambda p: " ".join(f"S{s}: a0->S{p[2 * s]} a1->S{p[2 * s + 1]}" for s in range(4)),
    B=[LSD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[([("בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה. ציירו את הדיאגרמה."
              if s == 0 else "המצב הבא בדיאגרמה:"), f"S = {s}:   SW9 SW8 = {s:02b}", LSD,
             "לאן עוברים ממנו כש-", "a = 0", "ולאן כש-", "a = 1", "?", SDA],
            (lambda s: lambda q, p: (p[2 * s] * 4 + p[2 * s + 1], 0xF))(s)) for s in range(4)]))

# the shortest way to a state
def bfs(t, goal):
    dist, fr = {0: 0}, [0]
    while fr:
        s = fr.pop(0)
        for a in range(2):
            n_ = t[2 * s + a]
            if n_ not in dist:
                dist[n_] = dist[s] + 1; fr.append(n_)
    return dist[goal]
VSH = [t for t in sd_vars() if bfs(t, 3) >= 2]
W.append(Q(id="SHORTEST", name="SHORTEST", title="הדרך הקצרה ביותר", inputs=[9, 8, 7], flat=True,
    outs=OSD, hexes=[[9, 8], None, None, None], variants=VSH, tables=sd_tab,
    answer=lambda p: (bfs(p, 3), 0xF), describe=lambda p: f"{bfs(p, 3)} clocks from S0 to S3",
    B=[LSD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.", LSD, FOLLOW,
             "מה המספר הקטן ביותר של שעונים שמביא ממצב 0 למצב 3?", "S = 0 -> S = 3"] + cnt(4),
            lambda q, p: (bfs(p, 3), 0xF))]))

# a state that can never be reached from S0
def ur_var(r):
    t = [r.randrange(4) for _ in range(8)]
    seen = reach(t)
    if len(seen) != 3:
        return None
    u = ({0, 1, 2, 3} - seen).pop()
    t[2 * u] = t[2 * u + 1] = 0
    return tuple(t)
VUR = C.rv(66, 200, ur_var)
def ur_u(p):
    return ({0, 1, 2, 3} - reach(p)).pop()
W.append(Q(id="UNREACH", name="UNREACH", title="מצב שאי אפשר להגיע אליו", inputs=[9, 8, 7], flat=True,
    outs=OSD, hexes=[[9, 8], None, None, None], variants=VUR, tables=sd_tab,
    answer=lambda p: (ur_u(p), 0x3), describe=lambda p: f"S{ur_u(p)} unreachable, next {p}",
    B=[LSD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.",
             "S = 0:   SW9 SW8 = 00", LSD, "לאן עוברים ממצב 0 כש-", "a = 0", "ולאן כש-", "a = 1", "?", SDA],
            lambda q, p: (p[0] * 4 + p[1], 0xF)),
           (["לאחד המצבים אין דרך להגיע ממצב 0 (מצב האיפוס), מה שלא תעשו. איזה?", LSD] + code(["S0", "S1", "S2", "S3"]),
            lambda q, p: (ur_u(p), 0x3))]))

# a trap state: no input leaves it
def tr_var(r):
    t = [r.randrange(4) for _ in range(8)]
    x = r.randrange(1, 4)
    t[2 * x] = t[2 * x + 1] = x
    if reach(t) != {0, 1, 2, 3} or any(t[2 * s] == t[2 * s + 1] == s for s in range(4) if s != x):
        return None
    return tuple(t)
VTR = C.rv(67, 200, tr_var)
def tr_x(p):
    return [s for s in range(4) if p[2 * s] == p[2 * s + 1] == s][0]
def tr_loops(p):
    return sum(1 for s in range(4) if s != tr_x(p) and s in (p[2 * s], p[2 * s + 1]))
W.append(Q(id="TRAP", name="TRAP", title="מצב מלכודת", inputs=[9, 8, 7], flat=True,
    outs=OSD, hexes=[[9, 8], None, None, None], variants=VTR, tables=sd_tab,
    answer=lambda p: (tr_loops(p), 0x3), describe=lambda p: f"trap S{tr_x(p)}, {tr_loops(p)} other states with a self loop, next {p}",
    B=[LSD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מכונה עם 4 מצבים וכניסה אחת: המצב והכניסה על המתגים, המצב הבא בתצוגה.", LSD,
             "באחד המצבים המכונה נתקעת: אף ערך של הכניסה לא מוציא ממנו. איזה?"] + code(["S0", "S1", "S2", "S3"]),
            lambda q, p: (tr_x(p), 0x3)),
           (["בכמה מהמצבים האחרים יש חץ לעצמו (לפחות ערך אחד של הכניסה משאיר במקום)?", LSD,
             "0 = all down"] + cnt(3), lambda q, p: (tr_loops(p), 0x3))]))

# state encodings: binary, one-hot, Gray - the state bits on switches, the next state bits on LEDs
ENC = ["binary", "one-hot", "Gray"]
VEN = [(n, e) for n in (3, 4) for e in range(3)]
def enc(e, s):
    return [s, 1 << s, s ^ (s >> 1)][e]
def en_next(p, c):
    cs = [enc(p[1], s) for s in range(p[0])]
    return cs[(cs.index(c) + 1) % p[0]] if c in cs else cs[0]
OEN = [("G", i) for i in (3, 2, 1, 0)]
LEN = "state bits = SW9 SW8 SW7 SW6     next state bits = LEDG3 LEDG2 LEDG1 LEDG0"
W.append(Q(id="ENCODING", name="ENCODING", title="קידוד מצבים", inputs=[9, 8, 7, 6], flat=True,
    outs=OEN, hexes=[None, None, None, None], variants=VEN,
    tables=lambda p: ft(OEN, 4, 0, lambda c, a: {("G", i): (en_next(p, c) >> i) & 1 for i in range(4)}),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"{p[0]} states, {ENC[p[1]]}",
    B=[LEN + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת המצב הבא של מכונה בלי כניסות. ביטי המצב על המתגים, ביטי המצב הבא בנורות (באותו סדר).", LEN,
             "התחילו מכל המתגים למטה, ובכל פעם העתיקו את הנורות למתגים. כמה קודים שונים יש במחזור?"] + cnt(4),
            lambda q, p: (p[0], 0xF)),
           (["כמה ביטים משתנים לפחות פעם אחת במחזור (כמה דלגלגים באמת בשימוש)?", LEN,
             "binary / Gray: 2     one-hot: one per state"] + cnt(4), lambda q, p: (p[0] if p[1] == 1 else 2, 0xF)),
           (["איזה קידוד? באחד-חם ביט אחד דולק, בגריי רק ביט אחד משתנה בכל מעבר.", "binary = all down     one-hot = SW0     Gray = SW1"],
            lambda q, p: (p[1], 0x3))]))

# ================================================================ topic 2: the traffic light controller (slides 8-18)
# states S0..S3 of the slide; LA / LB = green / yellow / red
LIGHTS = ["LA:  green = LEDG7   yellow = LEDG6   red = LEDG5", "LB:  green = LEDG2   yellow = LEDG1   red = LEDG0"]
LA_ONLY = "LA:  green = LEDG7   yellow = LEDG6   red = LEDG5"
TL_OUT = {0: (0, 2), 1: (1, 2), 2: (2, 0), 3: (2, 1)}		# 0 green 1 yellow 2 red
OLT = [("G", i) for i in (7, 6, 5, 2, 1, 0)]
def tl_leds(ph):
    la, lb = TL_OUT[ph]
    d = {("G", 7 - la): 1, ("G", 2 - lb): 1}
    return {("G", i): d.get(("G", i), 0) for i in (7, 6, 5, 2, 1, 0)}
TLS = ["S0: TA -> S0, else S1", "S1 -> S2", "S2: TB -> S2, else S3", "S3 -> S0"]
def tb_next(p, s, inb):				# the slide (p = (9, 9)), or p = (bad state, bad target)
    ta, tb = (inb >> 1) & 1, inb & 1
    n_ = [0 if ta else 1, 2, 2 if tb else 3, 0][s]
    if s == p[0]:
        if s in (0, 2):
            n_ = p[1] if (ta if s == 0 else tb) == 0 else n_
        else:
            n_ = p[1]
    return n_
L3 = "S = SW9 SW8 SW7   (HEX3)     " + NXH
L2 = "S1 S0 = SW9 SW8   (HEX3)     " + NXH

# yellow lasts k clocks, and TA / TB in a hidden order
OTL = OLT + hexd(0)
def tl_states(k):
    return [0] + [1] * k + [2] + [3] * k
def tl_next(p, s, inb):				# p = (swap, k); s = index in tl_states
    sw, k = p
    S = tl_states(k)
    if s >= len(S):
        return 0
    ta, tb = ((inb >> 1) & 1, inb & 1) if not sw else (inb & 1, (inb >> 1) & 1)
    ph = S[s]
    if ph == 0:
        return 0 if ta else 1
    if ph == 2:
        return s if tb else s + 1
    return (s + 1) % len(S)
def tl_ph(S, s):
    return S[s] if s < len(S) else 0
VTL = [(sw, k) for sw in range(2) for k in (1, 2, 3)]
W.append(Q(id="TRAFFIC", name="TRAFFIC", title="בקר הרמזור", inputs=[9, 8, 7, 6, 5], flat=True, small=True,
    outs=OTL, hexes=[[9, 8, 7], None, None, None], variants=VTL,
    tables=lambda p: ft(OTL, 3, 2, lambda s, inb: {**tl_leds(tl_ph(tl_states(p[1]), s)), **dig(0, tl_next(p, s, inb))}),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"TA = SW{5 if p[0] else 6}, yellow lasts {p[1]} clocks",
    B=[L3 + "     TA, TB = SW6, SW5 (in some order)     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של בקר הרמזור מההרצאה, עם כמה מצבים לצהוב: המצב והחיישנים על המתגים, המצב הבא בתצוגה.", L3,
             "TA, TB = SW6, SW5   (in some order)"] + LIGHTS +
            ["במצב 0 הרחוב הראשון ירוק. איזה מתג הוא", "TA", "? (כשהוא למעלה, המצב הבא נשאר 0)"] + code(["SW6", "SW5"]),
            lambda q, p: (p[0], 0x1)),
           (["שני החיישנים למטה. התחילו במצב 0 ועקבו אחרי המצב הבא.", FOLLOW, "כמה שעונים הצהוב של הרחוב הראשון דולק?",
             L3, "SW6 = 0     SW5 = 0     LA yellow = LEDG6"] + cnt(3), lambda q, p: (p[1], 0x3))]))

# yellow of A and of B last different times: the full cycle
VCY = [(ya, yb) for ya in (1, 2, 3) for yb in (1, 2, 3)]
def cy_states(p):
    return [0] + [1] * p[0] + [2] + [3] * p[1]
def cy_next(p, s, inb):
    S = cy_states(p)
    if s >= len(S):
        return 0
    ta, tb = (inb >> 1) & 1, inb & 1
    if S[s] == 0:
        return s if ta else s + 1
    if S[s] == 2:
        return s if tb else s + 1
    return (s + 1) % len(S)
LCY = "TA = SW6     TB = SW5"
W.append(Q(id="TLCYCLE", name="TLCYCLE", title="מחזור שלם של הרמזור", inputs=[9, 8, 7, 6, 5], flat=True, small=True,
    outs=OTL, hexes=[[9, 8, 7], None, None, None], variants=VCY,
    tables=lambda p: ft(OTL, 3, 2, lambda s, inb: {**tl_leds(tl_ph(cy_states(p), s)), **dig(0, cy_next(p, s, inb))}),
    answer=lambda p: ((len(cy_states(p)) - 1).bit_length(), 0x3), describe=lambda p: f"yellow A {p[0]}, yellow B {p[1]}",
    B=[L3 + "     " + LCY + "     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של בקר הרמזור, אבל הצהוב של כל רחוב נמשך זמן אחר. המצב והחיישנים על המתגים, המצב הבא בתצוגה.",
             L3, LCY] + LIGHTS + [FOLLOW, "שני החיישנים למטה. התחילו במצב 0. כמה שעונים הצהוב של הרחוב הראשון דולק?",
             "LA yellow = LEDG6"] + cnt(3), lambda q, p: (p[0], 0x3)),
           (["כמה שעונים הצהוב של הרחוב השני דולק?", L3, "SW6 = 0     SW5 = 0     LB yellow = LEDG1"] + cnt(3),
            lambda q, p: (p[1], 0x3)),
           (["כמה שעונים נמשך מחזור שלם, ממצב 0 עד שחוזרים אליו?", L3, "SW6 = 0     SW5 = 0"] + cnt(8),
            lambda q, p: (len(cy_states(p)), 0xF)),
           (["כל שעון במחזור הוא מצב אחר. כמה דלגלגים צריך לפחות בקידוד בינארי?"] + cnt(3),
            lambda q, p: ((len(cy_states(p)) - 1).bit_length(), 0x3))]))

# the reset state (code 00) and which sensor is which
VTS = [(sw, st) for sw in range(2) for st in range(4)]
def ts_next(p, s, inb):				# stored code = actual - start (mod 4)
    a = (s + p[1]) & 3
    if p[0]:
        inb = ((inb & 1) << 1) | (inb >> 1)
    return (tb_next((9, 9), a, inb) - p[1]) & 3
OTS = OLT + hexd(0)
W.append(Q(id="TRAFFICRESET", name="TRAFFICRESET", title="מצב האיפוס של הרמזור", inputs=[9, 8, 7, 6], flat=True,
    outs=OTS, hexes=[[9, 8], None, None, None], variants=VTS,
    tables=lambda p: ft(OTS, 2, 2, lambda s, inb: {**tl_leds((s + p[1]) & 3), **dig(0, ts_next(p, s, inb))}),
    answer=lambda p: (p[0], 0x1), describe=lambda p: f"code 00 = S{p[1]}, TA = SW{6 if p[0] else 7}",
    B=[L2 + "     TA, TB = SW7, SW6 (in some order)     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של בקר הרמזור, אבל הקידוד של המצבים אולי שונה מהשקופית.",
             "אחרי איפוס אוגר המצב מכיל 00. מה מראה אז הרמזור של הרחוב הראשון?", "S1 S0 = SW9 SW8 = 00", LA_ONLY] +
            code(["green", "yellow", "red"]), lambda q, p: (TL_OUT[(p[1]) & 3][0], 0x3)),
           (["מצאו את המצב שבו הרחוב הראשון ירוק. איזה מתג הוא", "TA", "? (כשהוא למעלה, המצב הבא לא משתנה)",
             L2, "TA, TB = SW7, SW6   (in some order)", "LA green = LEDG7"] + code(["SW7", "SW6"]), lambda q, p: (p[0], 0x1))]))

# active-high or active-low sensors
VPO = [(pa, pb) for pa in range(2) for pb in range(2)]
OPO = OLT + hexd(0)
def po_end(p):
    return 0 if p[0] else 1 if p[1] else 2
LPO = "TA = SW7     TB = SW6"
W.append(Q(id="TLPOLARITY", name="TLPOLARITY", title="חיישן פעיל בנמוך", inputs=[9, 8, 7, 6], flat=True,
    outs=OPO, hexes=[[9, 8], None, None, None], variants=VPO,
    tables=lambda p: ft(OPO, 2, 2, lambda s, inb: {**tl_leds(s), **dig(0, tb_next((9, 9), s, inb ^ (p[0] << 1 | p[1])))}),
    answer=lambda p: (po_end(p), 0x3), describe=lambda p: f"TA active-{'low' if p[0] else 'high'}, TB active-{'low' if p[1] else 'high'}",
    B=[L2 + "     " + LPO + "     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של בקר הרמזור. כל חיישן אולי הפוך: יש תנועה כשהמתג למטה.", L2, LPO] + TLS +
            ["במצב 0: באיזה מצב של המתג יש תנועה ברחוב הראשון (המצב הבא נשאר 0)?", "S = 0     TA = SW7"] + UP0("למעלה", "למטה"),
            lambda q, p: (1 - p[0], 0x1)),
           (["במצב 2: באיזה מצב של המתג יש תנועה ברחוב השני (המצב הבא נשאר 2)?", L2, "S = 2     TB = SW6"] + UP0("למעלה", "למטה"),
            lambda q, p: (1 - p[1], 0x1)),
           (["שני המתגים למטה. התחילו במצב 0 ועקבו אחרי המצב הבא. מה קורה?", FOLLOW, L2, "SW7 = 0     SW6 = 0"] + LIGHTS +
            code(["A green forever", "B green forever", "full cycle"]), lambda q, p: (po_end(p), 0x3))]))

# the output encoding of the lights (slide 13), hidden
VOC = list(itertools.permutations(range(3)))
OOC = [("G", 3), ("G", 2), ("G", 1), ("G", 0)]
LOC = "S1 S0 = SW9 SW8   (HEX3)     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0"
W.append(Q(id="LIGHTCODE", name="LIGHTCODE", title="קידוד הצבעים", inputs=[9, 8], flat=True,
    outs=OOC, hexes=[[9, 8], None, None, None], variants=VOC,
    tables=lambda p: ft(OOC, 2, 0, lambda s, a: {("G", 3): p[TL_OUT[s][0]] >> 1, ("G", 2): p[TL_OUT[s][0]] & 1,
                                                ("G", 1): p[TL_OUT[s][1]] >> 1, ("G", 0): p[TL_OUT[s][1]] & 1}),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"green {p[0]:02b} yellow {p[1]:02b} red {p[2]:02b}",
    B=[LOC + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של בקר הרמזור: המצב על המתגים, וכל רמזור בשני ביטים.", LOC,
             "S0: LA green, LB red", "במצב 0 הרחוב הראשון ירוק. מה הקוד של ירוק?", "S = 0     SW1 SW0 = LA1 LA0"],
            lambda q, p: (p[0], 0x3)),
           (["ובמצב 0 הרחוב השני אדום. מה הקוד של אדום?", LOC, "S = 0     SW1 SW0 = LB1 LB0"], lambda q, p: (p[2], 0x3)),
           (["במצב 1 הרחוב הראשון צהוב. מה הקוד של צהוב?", LOC, "S1: LA yellow     S = 1     SW1 SW0 = LA1 LA0"],
            lambda q, p: (p[1], 0x3))]))

# a hidden binary state encoding: the output equation of LA red
VOE = list(itertools.permutations(range(4)))
OEN6 = ["S1", "~S1", "S0", "~S0", "S1 ^ S0", "~(S1 ^ S0)"]
def oe_eq(p):
    c2, c3 = p[2], p[3]
    if c2 >> 1 == c3 >> 1:
        return 0 if c2 >> 1 else 1
    if c2 & 1 == c3 & 1:
        return 2 if c2 & 1 else 3
    return 4 if c2 in (1, 2) else 5
LOE = "S1 S0 = SW9 SW8   (HEX3)"
W.append(Q(id="TLOUTEQ", name="TLOUTEQ", title="משוואת יציאה של הרמזור", inputs=[9, 8], flat=True,
    outs=OLT, hexes=[[9, 8], None, None, None], variants=VOE,
    tables=lambda p: ft(OLT, 2, 0, lambda c, a: tl_leds(p.index(c))),
    answer=lambda p: (oe_eq(p), 0x7), describe=lambda p: " ".join(f"S{s}={p[s]:02b}" for s in range(4)) + f", LA red = {OEN6[oe_eq(p)]}",
    B=[LOE + "     lights = LEDG7..5, LEDG2..0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של בקר הרמזור בקידוד בינארי, אבל לא בקידוד של השקופית. קוד המצב על המתגים.", LOE] + LIGHTS +
            ["מה הקוד של", "S0", "(הרחוב הראשון ירוק)?", "SW1 SW0 = S1 S0"], lambda q, p: (p[0], 0x3)),
           (["מה הקוד של", "S2", "(הרחוב השני ירוק)?", LOE, "LB green = LEDG2", "SW1 SW0 = S1 S0"], lambda q, p: (p[2], 0x3)),
           (["הרמזור של הרחוב הראשון אדום בדיוק בשני מצבים. מה משוואת היציאה שלו?", LOE,
             "LA red = LEDG5", "LA red = ?"] + code(OEN6, 3), lambda q, p: (oe_eq(p), 0x7))]))

# one-hot state bits of the traffic light, in a hidden order (switch SW6+i = bit i = LEDGi)
VOH = list(itertools.permutations(range(4)))
OOH = [("G", 7), ("G", 6), ("G", 5), ("G", 3), ("G", 2), ("G", 1), ("G", 0)]
def oh_f(p, c, inb):
    d = {o: 0 for o in OOH}
    if c in (1, 2, 4, 8):
        s = p[c.bit_length() - 1]
        d[("G", 7 - TL_OUT[s][0])] = 1
        d[("G", p.index(tb_next((9, 9), s, inb)))] = 1
    return d
LOH = ["state bits = SW9 SW8 SW7 SW6   (one-hot)     next state bits = LEDG3 LEDG2 LEDG1 LEDG0", "TA = SW5     TB = SW4"]
OHC = code(["SW6", "SW7", "SW8", "SW9"])
W.append(Q(id="ONEHOT", name="ONEHOT", title="קידוד אחד-חם של הרמזור", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=OOH, hexes=[None, None, None, None], variants=VOH,
    tables=lambda p: ft(OOH, 4, 2, lambda c, inb: oh_f(p, c, inb)),
    answer=lambda p: (p.index(2), 0x3), describe=lambda p: " ".join(f"SW{6 + i}=S{p[i]}" for i in range(4)),
    B=[LOH[0] + "     " + LOH[1] + "     " + LA_ONLY + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של בקר הרמזור בקידוד אחד-חם: ביט לכל מצב, ובדיוק אחד למעלה. סדר הביטים נסתר."] + LOH + [LA_ONLY] + TLS +
            ["איזה מתג הוא", "S0", "? (כשרק הוא למעלה, הרחוב הראשון ירוק)"] + OHC, lambda q, p: (p.index(0), 0x3)),
           (["איזה מתג הוא", "S1", "? (הרחוב הראשון צהוב)"] + LOH + [LA_ONLY] + OHC, lambda q, p: (p.index(1), 0x3)),
           (["איזה מתג הוא", "S2", "? (הרחוב הראשון אדום, וכש-", "TB = 1", "המצב הבא לא משתנה)"] + LOH + [LA_ONLY] + OHC,
            lambda q, p: (p.index(2), 0x3))]))

# the traffic light with one transition changed
def tb_vars():
    out = []
    for bs in range(4):
        good = [1, 2, 3, 0][bs]
        for t in range(4):
            if t != good and not (bs in (0, 2) and t == bs):
                out.append((bs, t))
    return out
OTB = hexd(0)
LTB = "TA = SW7     TB = SW6"
W.append(Q(id="TRAFFICBUG", name="TRAFFICBUG", title="מעבר שגוי ברמזור", inputs=[9, 8, 7, 6], flat=True,
    outs=OTB, hexes=[[9, 8], None, None, None], variants=tb_vars(),
    tables=lambda p: ft(OTB, 2, 2, lambda s, inb: dig(0, tb_next(p, s, inb))),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"{TLS[p[0]]} goes to S{p[1]} instead",
    B=[L2 + "     " + LTB + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת המצב הבא של בקר הרמזור, אבל מעבר אחד שונה מהשקופית:"] + TLS + [L2, LTB,
             "מאיזה מצב יוצא המעבר השגוי?"] + code(["S0", "S1", "S2", "S3"]), lambda q, p: (p[0], 0x3)),
           (["ולאיזה מצב הוא הולך במקום?", L2, LTB] + code(["S0", "S1", "S2", "S3"]), lambda q, p: (p[1], 0x3))]))

# ================================================================ topic 3: FSMs in SystemVerilog, sequence detectors
# a detector of a 3-bit pattern, Moore or Mealy; the state = the last three bits
VSQ = [(t, pat) for t in range(2) for pat in range(1, 8)]
OSQ = [("G", 0)]
def sq_out(p, s, a):
    return int(s == p[1]) if p[0] == 0 else int((((s & 3) << 1) | a) == p[1])
LSQ = "S = SW9 SW8 SW7 = the last three bits (SW9 = the oldest)     a = SW6     smile = LEDG0"
W.append(Q(id="SEQDET", name="SEQDET", title="גלאי רצף", inputs=[9, 8, 7, 6], flat=True,
    outs=OSQ, hexes=[None, None, None, None], variants=VSQ,
    tables=lambda p: ft(OSQ, 3, 1, lambda s, a: {("G", 0): sq_out(p, s, a)}),
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"{'Mealy' if p[0] else 'Moore'} detector of {p[1]:03b}",
    B=[LSQ + "     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של גלאי רצף של 3 ביטים. המצב הוא שלושת הביטים האחרונים, והכניסה היא הביט הבא.", LSQ,
             "הציבו כמה מצבים והזיזו רק את הכניסה. האם החיוך משתנה?"] + code(["Moore (no)", "Mealy (yes)"]), lambda q, p: (p[0], 0x1)),
           (["מה הרצף? במור: המצב שבו החיוך דולק. במילי: שני הביטים האחרונים והכניסה.", LSQ,
             "SW2 = first bit     SW1 = second     SW0 = last"], lambda q, p: (p[1], 0x7))]))

# a Moore detector (overlapping, as KMP) with hidden state numbers: count the hits on a given string
def kmp(pat, k, a, ov=True):
    s = (pat[:k] if (k < len(pat) or ov) else "") + str(a)
    while s and not pat.startswith(s):
        s = s[1:]
    return len(s)
SQS = "1001001010"
def sc_lab(p):					# p = (pattern, labels of matched 1..3)
    return (0,) + p[1]
def sc_next(p, s, a):
    pat, lab = f"{p[0]:03b}", sc_lab(p)
    return lab[kmp(pat, lab.index(s), a)]
def sc_hits(p, k):
    st, h, lab = 0, 0, sc_lab(p)
    for b in SQS[:k]:
        st = sc_next(p, st, int(b))
        h += int(lab.index(st) == 3)
    return h
VSC = [(pat, perm) for pat in range(8) for perm in itertools.permutations((1, 2, 3))]
OSC = [("G", 0)] + hexd(0)
LSC = "S1 S0 = SW9 SW8   (HEX3)     a = SW7     " + NXH + "     smile = LEDG0"
W.append(Q(id="SEQCOUNT", name="SEQCOUNT", title="כמה פעמים הגלאי מזהה?", inputs=[9, 8, 7], flat=True,
    outs=OSC, hexes=[[9, 8], None, None, None], variants=VSC,
    tables=lambda p: ft(OSC, 2, 1, lambda s, a: {("G", 0): int(sc_lab(p).index(s) == 3), **dig(0, sc_next(p, s, a))}),
    answer=lambda p: (sc_hits(p, 10), 0xF), describe=lambda p: f"Moore detector of {p[0]:03b}, labels {sc_lab(p)}: {sc_hits(p, 5)} hits in 5, {sc_hits(p, 10)} in 10",
    B=[LSC + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של גלאי מור של רצף של 3 ביטים (חופף): המצב והכניסה על המתגים, המצב הבא בתצוגה.",
             "החיוך דולק לפי המצב הנוכחי בלבד.", LSC, FOLLOW,
             "התחילו במצב 0, והכניסו את 5 הביטים האלה, ביט בכל שעון. כמה פעמים הגעתם למצב עם חיוך?", "a = 1 0 0 1 0",
             "0 = all down"] + cnt(5), lambda q, p: (sc_hits(p, 5), 0xF)),
           (["התחילו שוב במצב 0 והכניסו את כל 10 הביטים. כמה פעמים הגעתם למצב עם חיוך?", "a = 1 0 0 1 0 0 1 0 1 0",
             LSC, "0 = all down"] + cnt(6), lambda q, p: (sc_hits(p, 10), 0xF))]))

# the same detector as Moore and as Mealy, side by side
VTD = [(m, pat) for m in range(2) for pat in range(4)]
OTD = [("G", 1), ("G", 0)]
def td_out(p, s, a):				# s = the last two bits; Moore = s == pat, Mealy = (last bit, a) == pat
    mo, me = int(s == p[1]), int((((s & 1) << 1) | a) == p[1])
    return {("G", 1 - p[0]): mo, ("G", p[0]): me}
LTD = "S = SW9 SW8 = the last two bits (SW9 = the older)     a = SW7     LEDG1 LEDG0"
W.append(Q(id="TWODET", name="TWODET", title="מור ומילי זה ליד זה", inputs=[9, 8, 7], flat=True,
    outs=OTD, hexes=[None, None, None, None], variants=VTD,
    tables=lambda p: ft(OTD, 2, 1, lambda s, a: td_out(p, s, a)),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"Mealy on LEDG{p[0]}, pattern {p[1]:02b}",
    B=[LTD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של שני גלאים של אותו רצף של 2 ביטים: אחד מור ואחד מילי.", LTD,
             "איזו נורה היא גלאי המילי (משתנה כשמזיזים רק את הכניסה)?"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p[0], 0x1)),
           (["מה הרצף?", LTD, "SW1 = first bit     SW0 = second bit"], lambda q, p: (p[1], 0x3))]))

# overlapping or not: a 2-bit Moore detector (00 or 11) with hidden state numbers
VOV = [(pat, ov, lab) for pat in (0, 3) for ov in range(2) for lab in itertools.permutations((1, 2, 3), 2)]
OOV = [("G", 0)] + hexd(0)
def ov_lab(p):
    return (0,) + p[2]
def ov_f(p, s, a):
    lab = ov_lab(p)
    if s not in lab:
        return {("G", 0): 0, **dig(0, 0)}
    k = lab.index(s)
    return {("G", 0): int(k == 2), **dig(0, lab[kmp(f"{p[0]:02b}", k, a, p[1])])}
W.append(Q(id="OVERLAP", name="OVERLAP", title="רצף חופף או לא?", inputs=[9, 8, 7], flat=True,
    outs=OOV, hexes=[[9, 8], None, None, None], variants=VOV,
    tables=lambda p: ft(OOV, 2, 1, lambda s, a: ov_f(p, s, a)),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"Moore detector of {p[0]:02b}, {'overlapping' if p[1] else 'not overlapping'}, labels {ov_lab(p)}",
    B=[LSC + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של גלאי מור של רצף של 2 ביטים: המצב והכניסה על המתגים, המצב הבא בתצוגה.", LSC, FOLLOW,
             "מצאו את המצב עם החיוך ואת הדרך אליו ממצב 0. מה הרצף?", "SW1 = first bit     SW0 = second bit"],
            lambda q, p: (p[0], 0x3)),
           (["במצב עם החיוך, הכניסו שוב את הביט של הרצף. האם המצב הבא שוב עם חיוך (חופף)?", LSC,
             "overlapping: 1111 -> hit, hit, hit     not overlapping: hit, -, hit"] + UP0("חופף", "לא חופף"),
            lambda q, p: (p[1], 0x1))]))

# a Mealy machine: the output table
VME = [h for h in range(16) if any(((h >> (2 * s)) & 1) != ((h >> (2 * s + 1)) & 1) for s in range(2))]
OME = [("G", 0)]
LME = "S = SW9     a = SW8     y = LEDG0"
W.append(Q(id="MEALYOUT", name="MEALYOUT", title="טבלת יציאות של מכונת מילי", inputs=[9, 8], flat=True,
    outs=OME, hexes=[None, None, None, None], variants=VME,
    tables=lambda p: ft(OME, 1, 1, lambda s, a: {("G", 0): (p >> (2 * s + a)) & 1}),
    answer=lambda p: (p, 0xF), describe=lambda p: f"y by (S a) = 00 01 10 11: {[(p >> i) & 1 for i in range(4)]}",
    B=[LME + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של מכונת מילי עם שני מצבים: המצב והכניסה על המתגים, היציאה בנורה.", LME,
             "לכל מצב וכניסה: מתי", "y = 1", "? הרימו את המתג שלו:",
             "S=0 a=0 -> SW0     S=0 a=1 -> SW1     S=1 a=0 -> SW2     S=1 a=1 -> SW3"], lambda q, p: (p, 0xF))]))

# the Mealy detector of slide 26 without the default smile = 0: a latch
VLA = [(b, pat) for b in range(2) for pat in range(4)]
OLA = [("G", 1), ("G", 0)]
def la_out(p, s, a):
    hit = int(((s << 1) | a) == p[1])
    return {("G", 1 - p[0]): hit, ("G", p[0]): 1 if hit else HOLD}
LLA = "S = SW9 = the last bit     a = SW8     two Mealy detectors = LEDG1 LEDG0"
W.append(Q(id="LATCH", name="LATCH", title="שכחו את ברירת המחדל", inputs=[9, 8], flat=True, seq=True,
    outs=OLA, hexes=[None, None, None, None], variants=VLA,
    tables=lambda p: ft(OLA, 1, 1, lambda s, a: la_out(p, s, a)),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"pattern {p[1]:02b}, the latch (no default) on LEDG{p[0]}",
    B=[LLA + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת היציאה של שני גלאי מילי של אותו רצף של 2 ביטים, כמו בשקופית. באחד מהם חסרה השורה", "smile = 1'b0;",
             "בתחילת", "always_comb", "ולכן היציאה נשמרת (תפס).", LLA,
             "איזו נורה היא הגלאי עם הבאג (נדלקת ולא נכבית יותר)?"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p[0], 0x1)),
           (["מה הרצף? (לפי הגלאי התקין)", LLA, "SW1 = first bit     SW0 = second bit"], lambda q, p: (p[1], 0x3))]))

# enum: the order of the names decides the codes; q = 1 in S0 (the divide by 3 of the slide)
VEU = list(itertools.permutations(range(3)))
OEU = [("G", 2), ("G", 1), ("G", 0)]
def eu_f(p, c):
    if c in p:
        s = p.index(c)
        return {("G", 2): int(s == 0), ("G", 1): p[(s + 1) % 3] >> 1, ("G", 0): p[(s + 1) % 3] & 1}
    return {("G", 2): 0, ("G", 1): p[0] >> 1, ("G", 0): p[0] & 1}
LEU = "state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0"
W.append(Q(id="ENUM", name="ENUM", title="קידוד של enum", inputs=[9, 8], flat=True,
    outs=OEU, hexes=[None, None, None, None], variants=VEU,
    tables=lambda p: ft(OEU, 2, 0, lambda c, a: eu_f(p, c)),
    answer=lambda p: (p[2], 0x3), describe=lambda p: "typedef enum logic [1:0] {" + ", ".join(f"S{p.index(c)}" for c in range(3)) + "}",
    B=[LEU + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של המחלק ב-3 מהשקופית: ביטי המצב על המתגים, ביטי המצב הבא בנורות.",
             "S0 -> S1 -> S2 -> S0     q = 1 in S0",
             "typedef enum logic [1:0] {?, ?, ?} statetype;     (the first name = 00, the second = 01, the third = 10)", LEU,
             "מה הקוד של", "S0", "?", "SW1 SW0"], lambda q, p: (p[0], 0x3)),
           (["מה הקוד של", "S1", "?", LEU, "SW1 SW0"], lambda q, p: (p[1], 0x3)),
           (["ומה הקוד של", "S2", "?", LEU, "SW1 SW0"], lambda q, p: (p[2], 0x3))]))

# the unused code 11 of a 2-bit enum and the default of the case
VDF = list(range(4))
ODF = [("G", 2), ("G", 1), ("G", 0)]
def df_next(p, s):
    return (s + 1) % 3 if s < 3 else p
def df_press(p):
    return [1, 3, 2, 0][p]
W.append(Q(id="DEFAULT", name="DEFAULT", title="הקוד שאין לו שם", inputs=[9, 8], flat=True,
    outs=ODF, hexes=[None, None, None, None], variants=VDF,
    tables=lambda p: ft(ODF, 2, 0, lambda s, a: {("G", 2): int(s == 0), ("G", 1): df_next(p, s) >> 1, ("G", 0): df_next(p, s) & 1}),
    answer=lambda p: (df_press(p), 0x3), describe=lambda p: "default: nextstate = " + ["S0", "S1", "S2", "state (stuck)"][p],
    B=[LEU + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של המחלק ב-3 מהשקופית. לקוד 11 אין שם, ומה שקורה בו נקבע בשורה", "default: nextstate = ?;",
             "S0 = 00     S1 = 01     S2 = 10     q = 1 in S0", LEU,
             "הציבו את הקוד 11. מה המצב הבא?", "SW9 SW8 = 11"] + code(["S0", "S1", "S2", "stays 11"]),
            lambda q, p: (p, 0x3)),
           (["התחילו בקוד 11 ועקבו אחרי המצב הבא. אחרי כמה שעונים", "q", "נדלקת?", FOLLOW, LEU] +
            code(["never", "1", "2", "3"]), lambda q, p: (df_press(p), 0x3))]))

# divide-by-N code with one wrong next-state line
def dc_vars():
    out = []
    for n in (3, 4, 5):
        for k in range(n):
            for t in range(n):
                if t != (k + 1) % n and not (k == n - 1 < 4 and t) and not (k == n - 2 >= 2 and 0 < t <= k):
                    out.append((n, k, t))		# the last two cases: the same board as a divide by N - 1 or N + 1
    return out
ODC = hexd(0)
def dc_next(p, s):
    n, k, t = p
    if s >= n:
        return 0
    return t if s == k else (s + 1) % n
W.append(Q(id="DIVCODE", name="DIVCODE", title="שורה שגויה במכונת המצבים", inputs=[9, 8, 7], flat=True,
    outs=ODC, hexes=[[9, 8, 7], None, None, None], variants=dc_vars(),
    tables=lambda p: ft(ODC, 3, 0, lambda s, a: dig(0, dc_next(p, s))),
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"divide by {p[0]}: S{p[1]} goes to S{p[2]}",
    B=[LRH + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח לוגיקת המצב הבא של מחלק כמו בשקופית, אבל באחת השורות של", "S0 -> S1 -> ... -> S0     case (state)",
             "המצב הבא שגוי. לכל קוד אחר יש", "default: nextstate = S0;", LRH,
             "כמה מצבים יש בקוד? (בין 3 ל-5: המצב הגדול שיש לו שורה משלו ועוד 1)"] + cnt(5), lambda q, p: (p[0], 0x7)),
           (["מאיזה מצב יש מעבר שגוי?", LRH, "0 = all down"] + cnt(4), lambda q, p: (p[1], 0x7)),
           (["ולאיזה מצב הוא הולך במקום?", LRH, "0 = all down"] + cnt(4), lambda q, p: (p[2], 0x7))]))

# the three blocks of an FSM (slide 20): which one is broken; reset = a switch (a synchronous reset)
def bb_vars():
    out = [("reg", 1), ("reg", 2), ("out", 1), ("out", 2)]
    out += [("next", k, t) for k in range(3) for t in range(3) if t != (k + 1) % 3]
    return out
BLK = ["state register", "next state logic", "output logic"]
OBB = [("G", 0)] + hexd(0)
def bb_rst(p):
    return p[1] if p[0] == "reg" else 0
def bb_q(p):
    return p[1] if p[0] == "out" else 0
def bb_f(p, s, r):
    if r:
        n_ = bb_rst(p)
    elif s >= 3:
        n_ = 0
    else:
        n_ = p[2] if p[0] == "next" and s == p[1] else (s + 1) % 3
    return {("G", 0): int(s == bb_q(p)), **dig(0, n_)}
LBB = "S1 S0 = SW9 SW8   (HEX3)     reset = SW7     " + NXH + "     q = LEDG0"
W.append(Q(id="BLOCKBUG", name="BLOCKBUG", title="איזה בלוק שבור?", inputs=[9, 8, 7], flat=True,
    outs=OBB, hexes=[[9, 8], None, None, None], variants=bb_vars(),
    tables=lambda p: ft(OBB, 2, 1, lambda s, r: bb_f(p, s, r)),
    answer=lambda p: (["reg", "next", "out"].index(p[0]), 0x3), describe=lambda p: f"bug {p}",
    B=[LBB + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של המחלק ב-3 מהשקופית, אבל אחד משלושת הבלוקים שלו שבור. המצב והאיפוס על המתגים, המצב הבא בתצוגה.",
             LBB, "הרימו את האיפוס. מה המצב הבא?"] + code(["S0", "S1", "S2"]), lambda q, p: (bb_rst(p), 0x3)),
           (["באיזה מצב", "q", "דולקת?", LBB] + code(["S0", "S1", "S2"]), lambda q, p: (bb_q(p), 0x3)),
           (["השוו לשקופית. איזה בלוק שבור?", "S0 -> S1 -> S2 -> S0     reset -> S0     q = 1 in S0", LBB] + code(BLK),
            lambda q, p: (["reg", "next", "out"].index(p[0]), 0x3))]))

# an up / down counter: which switch counts up, modulo what
VUD = [(u, n) for u in range(2) for n in range(4, 10)]
OUD = hexd(0)
def ud_next(p, s, inb):
    u, n = p
    up, dn = (inb >> (1 - u)) & 1, (inb >> u) & 1
    if s >= n:
        return 0
    if up and not dn:
        return (s + 1) % n
    if dn and not up:
        return (s - 1) % n
    return s
LUD = "S = SW9 SW8 SW7 SW6   (HEX3)     up, down = SW5, SW4 (in some order)     " + NXH
W.append(Q(id="UPDOWN", name="UPDOWN", title="מונה למעלה ולמטה", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=OUD, hexes=[[9, 8, 7, 6], None, None, None], variants=VUD,
    tables=lambda p: ft(OUD, 4, 2, lambda s, inb: dig(0, ud_next(p, s, inb))),
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"up = SW{5 - p[0]}, modulo {p[1]}",
    B=[LUD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הלוגיקה של מונה: מתג אחד סופר למעלה ואחד למטה. המצב והכניסות על המתגים, המצב הבא בתצוגה.", LUD,
             "איזה מתג סופר למעלה?"] + code(["SW5", "SW4"]), lambda q, p: (p[0], 0x1)),
           (["כמה מצבים יש? (ממצב 0 כלפי מטה הולכים למצב הגדול)", LUD] + cnt(9), lambda q, p: (p[1], 0xF))]))

# ================================================================ easy questions straight from the slides
# The board holds the slide's own logic; the state / inputs to set are shown on HEX (the per-student variation).
SET = "הציבו במתגים את מה שבתצוגה."

# topic 1: the divide by 3 of slide 21 (S0 -> S1 -> S2 -> S0, q = 1 in S0)
OD3 = [("G", 0)] + hexd(1) + hexd(0)
LD3 = "S = SW9 SW8   (HEX3)     next state = HEX0     q = LEDG0"
TD3 = "HEX1 = the state to set"
W.append(Q(id="DIV3NEXT", name="DIV3NEXT", title="המחלק ב-3 מהשקופית", inputs=[9, 8], flat=True,
    outs=OD3, hexes=[[9, 8], None, None, None], variants=[0, 1, 2],
    tables=lambda p: ft(OD3, 2, 0, lambda s, a: {("G", 0): int(s == 0), **dig(1, p), **dig(0, (s + 1) % 3 if s < 3 else 0)}),
    answer=lambda p: ((3 - p) % 3 or 3, 0x3), describe=lambda p: f"start S{p}: next S{(p + 1) % 3}, q after {(3 - p) % 3 or 3} clocks",
    B=[LD3 + "     " + TD3 + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["המחלק ב-3 של שקופית 21. בלוח לוגיקת המצב הבא והיציאה שלו.", "S0 -> S1 -> S2 -> S0     q = 1 in S0", LD3, TD3,
             "הציבו במתגים את המצב שבתצוגה. מה המצב הבא?"] + code(["S0", "S1", "S2"]), lambda q, p: ((p + 1) % 3, 0x3)),
           (["התחילו במצב שבתצוגה. אחרי כמה שעונים", "q", "נדלקת?", FOLLOW, LD3, TD3] + cnt(3),
            lambda q, p: ((3 - p) % 3 or 3, 0x3))]))

# topic 1: slide 17 - binary and one-hot codes of 4 states
OOH17 = [("G", i) for i in (3, 2, 1, 0)] + hexd(3) + hexd(2) + hexd(1) + hexd(0)
LOH17 = "binary code = SW9 SW8     one-hot code = LEDG3 LEDG2 LEDG1 LEDG0"
TOH17 = "HEX3 HEX2 HEX1 HEX0 = a one-hot code"
W.append(Q(id="ONEHOT17", name="ONEHOT17", title="בינארי ואחד-חם מהשקופית", inputs=[9, 8], flat=True,
    outs=OOH17, hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda p: ft(OOH17, 2, 0, lambda s, a: {**{("G", i): int(s == i) for i in range(4)},
                                                    **{o: v for d in range(4) for o, v in dig(d, int(d == p)).items()}}),
    answer=lambda p: (p, 0x3), describe=lambda p: f"one-hot {1 << p:04b} = S{p} = binary {p:02b}",
    B=[LOH17 + "     " + TOH17 + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["קידוד מצבים של שקופית 17: בבינארי 2 ביטים, באחד-חם ביט לכל מצב.", "S0 = 00 / 0001     S1 = 01 / 0010     S2 = 10 / 0100     S3 = 11 / 1000",
             "בלוח ממיר מקוד בינארי לקוד אחד-חם.", LOH17, TOH17,
             "מצאו את הקוד הבינארי שנותן בנורות את הקוד שבתצוגה.", "SW1 SW0 = the binary code"], lambda q, p: (p, 0x3))]))

# topic 2: the encoded state transition table of slides 11-12
TSET = "the state to set = HEX3     TA = HEX1     TB = HEX0"
STC = "S0 = 00     S1 = 01     S2 = 10     S3 = 11"
VTN = [(s, ta, tb) for s in range(4) for ta in range(2) for tb in range(2)]
def tgt(p):					# the state / TA / TB to set, on HEX3 / HEX1 / HEX0
    return {**dig(3, p[0]), **dig(1, p[1]), **dig(0, p[2])}
def tn_nx(p):
    return tb_next((9, 9), p[0], p[1] << 1 | p[2])
OTN = [("G", 1), ("G", 0)] + hexd(3) + hexd(1) + hexd(0)
LTN = "S1 S0 = SW9 SW8     TA = SW7     TB = SW6     S'1 S'0 = LEDG1 LEDG0"
W.append(Q(id="TLNEXT", name="TLNEXT", title="טבלת המעברים של הרמזור", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=OTN, hexes=[None, None, None, None], variants=VTN,
    tables=lambda p: ft(OTN, 2, 2, lambda s, inb: {("G", 1): tb_next((9, 9), s, inb) >> 1, ("G", 0): tb_next((9, 9), s, inb) & 1, **tgt(p)}),
    answer=lambda p: (int(tn_nx(p) == p[0]), 0x1), describe=lambda p: f"S{p[0]} TA={p[1]} TB={p[2]} -> S{tn_nx(p)}",
    B=[LTN + "     " + TSET + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בקר הרמזור, טבלת המעברים המקודדת של שקופיות 11-12. בלוח לוגיקת המצב הבא שלו.", STC, LTN, TSET,
             SET, "מה המצב הבא?", "SW1 SW0 = S'1 S'0"], lambda q, p: (tn_nx(p), 0x3)),
           (["האם המכונה נשארת באותו מצב (חץ לעצמו)?", LTN, TSET] + UP0("נשארת", "עוברת"),
            lambda q, p: (int(tn_nx(p) == p[0]), 0x1))]))

# topic 2: the output table of slide 13
COLORS = ["green", "yellow", "red"]
OTO = [("G", i) for i in (3, 2, 1, 0)] + hexd(3)
LTO = "S1 S0 = SW9 SW8     LA1 LA0 = LEDG3 LEDG2     LB1 LB0 = LEDG1 LEDG0"
TTO = "HEX3 = the state to set"
CTO = "green = 00     yellow = 01     red = 10"
W.append(Q(id="TLOUT", name="TLOUT", title="טבלת היציאות של הרמזור", inputs=[9, 8], flat=True,
    outs=OTO, hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda p: ft(OTO, 2, 0, lambda s, a: {("G", 3): TL_OUT[s][0] >> 1, ("G", 2): TL_OUT[s][0] & 1,
                                                ("G", 1): TL_OUT[s][1] >> 1, ("G", 0): TL_OUT[s][1] & 1, **dig(3, p)}),
    answer=lambda p: (TL_OUT[p][1], 0x3), describe=lambda p: f"S{p}: LA {COLORS[TL_OUT[p][0]]}, LB {COLORS[TL_OUT[p][1]]}",
    B=[LTO + "     " + TTO + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בקר הרמזור, טבלת היציאות של שקופית 13. בלוח לוגיקת היציאה שלו, וכל רמזור בשני ביטים.", STC, CTO, LTO, TTO,
             "הציבו במתגים את המצב שבתצוגה. מה הצבע של הרחוב הראשון?", "LA = ?"] + code(COLORS),
            lambda q, p: (TL_OUT[p][0], 0x3)),
           (["ומה הצבע של הרחוב השני באותו מצב?", CTO, LTO, TTO, "LB = ?"] + code(COLORS), lambda q, p: (TL_OUT[p][1], 0x3))]))

# topic 2: the one-hot table of slide 18
O1H = [("G", i) for i in (3, 2, 1, 0)] + hexd(3) + hexd(1) + hexd(0)
L1H = "S3 S2 S1 S0 = SW9 SW8 SW7 SW6   (one-hot)     TA = SW5     TB = SW4     S'3 S'2 S'1 S'0 = LEDG3 LEDG2 LEDG1 LEDG0"
C1H = "S0 = 0001     S1 = 0010     S2 = 0100     S3 = 1000"
def h1_f(p, c, inb):
    nx = 1 << tb_next((9, 9), c.bit_length() - 1, inb) if c in (1, 2, 4, 8) else 0
    return {**{("G", i): (nx >> i) & 1 for i in range(4)}, **tgt(p)}
W.append(Q(id="TL1HOT", name="TL1HOT", title="הרמזור באחד-חם מהשקופית", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=O1H, hexes=[None, None, None, None], variants=VTN,
    tables=lambda p: ft(O1H, 4, 2, lambda c, inb: h1_f(p, c, inb)),
    answer=lambda p: (tn_nx(p), 0x3), describe=lambda p: f"S{p[0]} TA={p[1]} TB={p[2]} -> S{tn_nx(p)} = {1 << tn_nx(p):04b}",
    B=[L1H + "     " + TSET + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בקר הרמזור בקידוד אחד-חם, הטבלה של שקופית 18. בלוח לוגיקת המצב הבא שלו.", C1H, L1H, TSET,
             SET, "מה המצב הבא?", "SW3 SW2 SW1 SW0 = S'3 S'2 S'1 S'0"], lambda q, p: (1 << tn_nx(p), 0xF)),
           (["איזה מצב זה?", C1H, L1H] + code(["S0", "S1", "S2", "S3"]), lambda q, p: (tn_nx(p), 0x3))]))

# topic 3: the Moore detector of slides 23-24 (S0 = 00, S1 = 01, S2 = 10; smile in S2)
def mo_nx(s, a):
    return [0 if a else 1, 2 if a else 1, 0 if a else 1, 0][s]
def mo_f(p, s, a):
    nx = mo_nx(s, a)
    return {("G", 2): int(s == 2), ("G", 1): nx >> 1, ("G", 0): nx & 1, **dig(3, p[0]), **dig(0, p[1])}
OMO = [("G", 2), ("G", 1), ("G", 0)] + hexd(3) + hexd(0)
LMO = "state bits = SW9 SW8     a = SW7     smile = LEDG2     next state bits = LEDG1 LEDG0"
TMO = "the state to set = HEX3     a = HEX0"
CMO = "S0 = 00     S1 = 01     S2 = 10"
W.append(Q(id="MOORE01", name="MOORE01", title="גלאי המור מהשקופית", inputs=[9, 8, 7], flat=True,
    outs=OMO, hexes=[None, None, None, None], variants=[(s, a) for s in range(3) for a in range(2)],
    tables=lambda p: ft(OMO, 2, 1, lambda s, a: mo_f(p, s, a)),
    answer=lambda p: (mo_nx(*p), 0x3), describe=lambda p: f"S{p[0]} a={p[1]} -> S{mo_nx(*p)}, smile {int(p[0] == 2)}",
    B=[LMO + "     " + TMO + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["גלאי הרצף של מור בקוד של שקופית 24. בלוח הלוגיקה שלו.", "typedef enum logic [1:0] {S0, S1, S2}     assign smile = (state == S2);",
             CMO, LMO, TMO, SET, "האם החיוך דולק?"] + UP0("דולק", "כבוי"), lambda q, p: (int(p[0] == 2), 0x1)),
           (["מה המצב הבא?", CMO, LMO, TMO] + code(["S0", "S1", "S2"]), lambda q, p: (mo_nx(*p), 0x3))]))

# topic 3: the Mealy detector of slides 25-26 (S0 = 0, S1 = 1; smile when S1 and a)
OML = [("G", 1), ("G", 0)] + hexd(3) + hexd(0)
LML = "state = SW9     a = SW8     smile = LEDG1     next state = LEDG0"
W.append(Q(id="MEALY01", name="MEALY01", title="גלאי המילי מהשקופית", inputs=[9, 8], flat=True,
    outs=OML, hexes=[None, None, None, None], variants=[(s, a) for s in range(2) for a in range(2)],
    tables=lambda p: ft(OML, 1, 1, lambda s, a: {("G", 1): s & a, ("G", 0): 1 - a, **dig(3, p[0]), **dig(0, p[1])}),
    answer=lambda p: (1 - p[1], 0x1), describe=lambda p: f"S{p[0]} a={p[1]} -> S{1 - p[1]}, smile {p[0] & p[1]}",
    B=[LML + "     " + TMO + "     answer: SW0"], L=[], F=[],
    steps=[(["גלאי הרצף של מילי בקוד של שקופית 26. בלוח הלוגיקה שלו.", "typedef enum logic {S0, S1}     S0 = 0     S1 = 1",
             LML, TMO, SET, "האם החיוך דולק?"] + UP0("דולק", "כבוי"), lambda q, p: (p[0] & p[1], 0x1)),
           (["מה המצב הבא?", LML, TMO] + code(["S0", "S1"]), lambda q, p: (1 - p[1], 0x1))]))

# topic 3: the case of the divide by 3 in code (slide 22), with its default line
OD3C = [("G", 2), ("G", 1), ("G", 0)] + hexd(3) + hexd(2)
LD3C = "state bits = SW9 SW8     q = LEDG2     next state bits = LEDG1 LEDG0"
TD3C = "HEX3 HEX2 = the state bits to set"
D3N = [1, 2, 0, 0]
W.append(Q(id="DIV3CASE", name="DIV3CASE", title="ה-case של המחלק ב-3", inputs=[9, 8], flat=True,
    outs=OD3C, hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda p: ft(OD3C, 2, 0, lambda s, a: {("G", 2): int(s == 0), ("G", 1): D3N[s] >> 1, ("G", 0): D3N[s] & 1,
                                                  **dig(3, p >> 1), **dig(2, p & 1)}),
    answer=lambda p: (D3N[p], 0x3), describe=lambda p: f"code {p:02b}: line {['S0', 'S1', 'S2', 'default'][p]}, next {D3N[p]:02b}",
    B=[LD3C + "     " + TD3C + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["המחלק ב-3 בקוד של שקופית 22. בלוח לוגיקת המצב הבא והיציאה שלו.",
             "typedef enum logic [1:0] {S0, S1, S2}     S0: nextstate = S1;   S1: nextstate = S2;   S2: nextstate = S0;   default: nextstate = S0;",
             LD3C, TD3C, "איזו שורה של ה-", "case", "מתבצעת בקוד שבתצוגה?"] + code(["S0", "S1", "S2", "default"]),
            lambda q, p: (p, 0x3)),
           (["הציבו את הקוד במתגים. מה המצב הבא?", LD3C, TD3C, "SW1 SW0 = next state bits"], lambda q, p: (D3N[p], 0x3))]))

# ================================================================ more easy questions straight from the slides (1-2 steps)
# topic 1: the divide by 3 of slide 21 - where it is after k clocks (k on HEX1)
LKA = "HEX1 = the number of clocks"
W.append(Q(id="D3AFTER", name="D3AFTER", title="המחלק ב-3 אחרי כמה שעונים", inputs=[9, 8], flat=True,
    outs=OD3, hexes=[[9, 8], None, None, None], variants=list(range(2, 10)),
    tables=lambda p: ft(OD3, 2, 0, lambda s, a: {("G", 0): int(s == 0), **dig(1, p), **dig(0, (s + 1) % 3 if s < 3 else 0)}),
    answer=lambda p: (int(p % 3 == 0), 0x1), describe=lambda p: f"{p} clocks from S0 -> S{p % 3}, q {int(p % 3 == 0)}",
    B=[LD3 + "     " + LKA + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["המחלק ב-3 של שקופית 21. בלוח לוגיקת המצב הבא והיציאה שלו.", "S0 -> S1 -> S2 -> S0     q = 1 in S0", LD3, LKA, FOLLOW,
             "התחילו במצב 0 ותנו את מספר השעונים שבתצוגה. באיזה מצב אתם?"] + code(["S0", "S1", "S2"]), lambda q, p: (p % 3, 0x3)),
           (["האם היציאה", "q", "דולקת במצב הזה?", LD3, LKA] + UP0("דולקת", "כבויה"), lambda q, p: (int(p % 3 == 0), 0x1))]))

# topic 1: the divide by 3 with its reset (slide 22: if (reset) state <= S0)
ORS = [("G", 2), ("G", 1), ("G", 0)] + hexd(3) + hexd(0)
LRS = "state bits = SW9 SW8     reset = SW7     q = LEDG2     next state bits = LEDG1 LEDG0"
TRS = "the state to set = HEX3     reset = HEX0"
CD3 = "S0 = 00     S1 = 01     S2 = 10"
def rs_nx(s, r):
    return 0 if r else D3N[s]
W.append(Q(id="D3RESET", name="D3RESET", title="המחלק ב-3 והאיפוס", inputs=[9, 8, 7], flat=True,
    outs=ORS, hexes=[None, None, None, None], variants=[(s, r) for s in range(3) for r in range(2)],
    tables=lambda p: ft(ORS, 2, 1, lambda s, r: {("G", 2): int(s == 0), ("G", 1): rs_nx(s, r) >> 1, ("G", 0): rs_nx(s, r) & 1,
                                                 **dig(3, p[0]), **dig(0, p[1])}),
    answer=lambda p: (rs_nx(*p), 0x3), describe=lambda p: f"S{p[0]} reset={p[1]} -> S{rs_nx(*p)}",
    B=[LRS + "     " + TRS + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["המחלק ב-3 של שקופיות 21-22, עם האיפוס. בלוח לוגיקת המצב הבא והיציאה שלו.",
             "if (reset) state <= S0;     S0 -> S1 -> S2 -> S0     q = 1 in S0", CD3, LRS, TRS, SET,
             "האם היציאה", "q", "דולקת?"] + UP0("דולקת", "כבויה"), lambda q, p: (int(p[0] == 0), 0x1)),
           (["מה המצב הבא?", CD3, LRS, TRS, "SW1 SW0 = next state bits"], lambda q, p: (rs_nx(*p), 0x3))]))

# topic 1: the design procedure (slides 5-6) on the divide by 3: from the encoded table to an equation
EQ3 = ["~S1 & S0", "~S1 & ~S0", "S1 & ~S0", "S1 ^ S0"]
def eq3_bit(i, c):				# LEDG i at code c: q (i = 2) and the next state bits (11 = default -> S0)
    return int(c == 0) if i == 2 else (D3N[c] >> i) & 1
def eq3_mask(i):
    return sum(eq3_bit(i, c) << c for c in range(4))
OEQ = [("G", 2), ("G", 1), ("G", 0)] + hexd(0)
LEQ = "S1 S0 = SW9 SW8     q = LEDG2     S'1 = LEDG1     S'0 = LEDG0"
TEQ = "HEX0 = the LED to study (LEDG0, LEDG1 or LEDG2)"
W.append(Q(id="D3EQ", name="D3EQ", title="משוואה של המחלק ב-3", inputs=[9, 8], flat=True,
    outs=OEQ, hexes=[None, None, None, None], variants=[0, 1, 2],
    tables=lambda p: ft(OEQ, 2, 0, lambda c, a: {**{("G", i): eq3_bit(i, c) for i in range(3)}, **dig(0, p)}),
    answer=lambda p: (EQ3.index("~S1 & S0" if p == 1 else "~S1 & ~S0"), 0x3),
    describe=lambda p: f"LEDG{p}: codes {eq3_mask(p):04b}, " + ("~S1 & S0" if p == 1 else "~S1 & ~S0"),
    B=[LEQ + "     " + TEQ + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["שלבי התכנון של שקופית 5 על המחלק ב-3 של שקופיות 21-22: מהטבלה המקודדת למשוואה.",
             CD3 + "     11 = default -> S0", LEQ, TEQ,
             "הציבו כל קוד. בכל קוד שבו הנורה שבתצוגה דולקת, הרימו את המתג שלו:",
             "S1 S0 = 00 -> SW0     01 -> SW1     10 -> SW2     11 -> SW3"], lambda q, p: (eq3_mask(p), 0xF)),
           (["מה המשוואה של הנורה הזאת?", LEQ, TEQ, "LED = ?"] + code(EQ3),
            lambda q, p: (EQ3.index("~S1 & S0" if p == 1 else "~S1 & ~S0"), 0x3))]))

# topic 2: the diagram of slide 10 - which sensor keeps the state
OST = OLT + hexd(3) + hexd(0)
LST = "S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0"
TST = "HEX3 = the state to set"
STAY = ["none", "TA", "TB"]
W.append(Q(id="TLSTAY", name="TLSTAY", title="חץ לעצמו בדיאגרמת הרמזור", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=OST, hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda p: ft(OST, 2, 2, lambda s, inb: {**tl_leds(s), **dig(3, p), **dig(0, tb_next((9, 9), s, inb))}),
    answer=lambda p: ([1, 0, 2, 0][p], 0x3), describe=lambda p: f"S{p}: stays with {STAY[[1, 0, 2, 0][p]]}",
    B=[LST + "     " + TST + "     lights = LEDG7..5, LEDG2..0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בקר הרמזור, דיאגרמת המעברים של שקופית 10. בלוח לוגיקת המצב הבא שלו.", STC, LST, TST, SET,
             "שני החיישנים למטה. מה המצב הבא?", "TA = 0     TB = 0"] + code(["S0", "S1", "S2", "S3"]),
            lambda q, p: ([1, 2, 3, 0][p], 0x3)),
           (["באותו מצב: הרימו כל חיישן לבד. איזה חיישן משאיר את המכונה במקום (חץ לעצמו)?", LST, TST] + code(STAY),
            lambda q, p: ([1, 0, 2, 0][p], 0x3))]))

# topic 2: one output equation of slides 13-14 (LA1 = S1, LA0 = ~S1 S0, LB1 = ~S1, LB0 = S1 S0)
OB = [(1, 1), (1, 0), (0, 1), (0, 0)]		# (street A = 1 / B = 0, bit) -> LEDG 3 2 1 0
EQB = ["S1", "~S1", "~S1 & S0", "S1 & S0"]
def ob_bit(k, s):
    street, b = OB[k]
    col = TL_OUT[s][0 if street else 1]
    return (col >> b) & 1
def ob_eq(k):
    return [0, 2, 1, 3][k]
OOB = [("G", i) for i in (3, 2, 1, 0)] + hexd(1) + hexd(0)
TOB = "HEX1 = the street (A or b)     HEX0 = the bit (1 or 0)"
W.append(Q(id="TLOUTBIT", name="TLOUTBIT", title="משוואת יציאה מהשקופית", inputs=[9, 8], flat=True,
    outs=OOB, hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda p: ft(OOB, 2, 0, lambda s, a: {**{("G", 3 - k): ob_bit(k, s) for k in range(4)},
                                                **dig(1, 10 if OB[p][0] else 11), **dig(0, OB[p][1])}),
    answer=lambda p: (ob_eq(p), 0x3), describe=lambda p: f"{'LA' if OB[p][0] else 'LB'}{OB[p][1]} = {EQB[ob_eq(p)]}",
    B=[LTO + "     " + TOB + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בקר הרמזור, טבלת היציאות ומשוואות היציאה של שקופיות 13-14. בלוח לוגיקת היציאה שלו.", STC, CTO, LTO, TOB,
             "הציבו כל מצב. בכל מצב שבו הביט שבתצוגה דולק, הרימו את המתג שלו:", SL4.replace("S = ", "S1 S0 = ")],
            lambda q, p: (sum(ob_bit(p, s) << s for s in range(4)), 0xF)),
           (["מה המשוואה של הביט הזה?", LTO, TOB, "bit = ?"] + code(EQB), lambda q, p: (ob_eq(p), 0x3))]))

# topic 2: the timing of slides 15-16 - two clocks with fixed sensors
OTT = hexd(3) + hexd(2) + hexd(1) + hexd(0)
LTT = "S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX2"
TTT = "the start state = HEX3     TA = HEX1     TB = HEX0"
def tt_after(p, k):
    s = p[0]
    for _ in range(k):
        s = tb_next((9, 9), s, p[1] << 1 | p[2])
    return s
W.append(Q(id="TLTRACE", name="TLTRACE", title="שני שעונים ברמזור", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=OTT, hexes=[None, None, None, None], variants=VTN,
    tables=lambda p: ft(OTT, 2, 2, lambda s, inb: {**dig(3, p[0]), **dig(2, tb_next((9, 9), s, inb)), **dig(1, p[1]), **dig(0, p[2])}),
    answer=lambda p: (tt_after(p, 2), 0x3), describe=lambda p: f"S{p[0]} TA={p[1]} TB={p[2]}: S{tt_after(p, 1)}, S{tt_after(p, 2)}",
    B=[LTT + "     " + TTT + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בקר הרמזור, דיאגרמת הזמנים של שקופיות 15-16. בלוח לוגיקת המצב הבא שלו.", STC, LTT, TTT, SET,
             "החיישנים לא משתנים. באיזה מצב תהיו אחרי שעון אחד?"] + code(["S0", "S1", "S2", "S3"]), lambda q, p: (tt_after(p, 1), 0x3)),
           (["ואחרי שעון נוסף?", FOLLOW, LTT, TTT] + code(["S0", "S1", "S2", "S3"]), lambda q, p: (tt_after(p, 2), 0x3))]))

# topic 2: how long until a street is green (sensors down)
OWT = OLT + hexd(3) + hexd(1) + hexd(0)
LWT = "S1 S0 = SW9 SW8     TA = SW7     TB = SW6     next state = HEX0"
TWT = "HEX3 = the start state     HEX1 = the street (A or b)"
def wt(p):
    s, k = p[0], 0
    while TL_OUT[s][0 if p[1] else 1] != 0:
        s = tb_next((9, 9), s, 0); k += 1
    return k
W.append(Q(id="TLWAIT", name="TLWAIT", title="מתי יהיה ירוק?", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=OWT, hexes=[None, None, None, None], variants=[(s, st) for s in range(4) for st in (1, 0)],
    tables=lambda p: ft(OWT, 2, 2, lambda s, inb: {**tl_leds(s), **dig(3, p[0]), **dig(1, 10 if p[1] else 11),
                                                   **dig(0, tb_next((9, 9), s, inb))}),
    answer=lambda p: (wt(p), 0x3), describe=lambda p: f"from S{p[0]}, street {'A' if p[1] else 'B'} green after {wt(p)} clocks",
    B=[LWT + "     " + TWT + "     lights = LEDG7..5, LEDG2..0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בקר הרמזור של שקופיות 8-10. בלוח לוגיקת המצב הבא והיציאות שלו.", STC, LWT, TWT] + LIGHTS +
            ["הציבו את מצב ההתחלה. מה הצבע עכשיו של הרחוב שבתצוגה?"] + code(COLORS),
            lambda q, p: (TL_OUT[p[0]][0 if p[1] else 1], 0x3)),
           (["שני החיישנים למטה. אחרי כמה שעונים הרחוב שבתצוגה ירוק?", FOLLOW, LWT, TWT, "TA = 0     TB = 0",
             "0 = green now = all down"] + cnt(3), lambda q, p: (wt(p), 0x3))]))

# topic 3: the Moore detector of slide 24 - which value of a keeps the state
OMS = [("G", 2), ("G", 1), ("G", 0)] + hexd(3)
TMS = "HEX3 = the state to set"
STAYM = ["none", "a=0", "a=1"]
def ms_stay(s):
    return [2, 1, 0][s]
W.append(Q(id="MOORESTAY", name="MOORESTAY", title="מתי גלאי המור נשאר במקום?", inputs=[9, 8, 7], flat=True,
    outs=OMS, hexes=[None, None, None, None], variants=[0, 1, 2],
    tables=lambda p: ft(OMS, 2, 1, lambda s, a: {("G", 2): int(s == 2), ("G", 1): mo_nx(s, a) >> 1, ("G", 0): mo_nx(s, a) & 1, **dig(3, p)}),
    answer=lambda p: (ms_stay(p), 0x3), describe=lambda p: f"S{p}: smile {int(p == 2)}, stays with {STAYM[ms_stay(p)]}",
    B=[LMO + "     " + TMS + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["גלאי הרצף של מור בקוד של שקופית 24. בלוח הלוגיקה שלו.", "S0: if (a) S0 else S1     S1: if (a) S2 else S1     S2: if (a) S0 else S1",
             CMO, LMO, TMS, SET, "האם החיוך דולק?"] + UP0("דולק", "כבוי"), lambda q, p: (int(p == 2), 0x1)),
           (["הזיזו רק את הכניסה. באיזה ערך שלה המצב הבא שווה למצב הנוכחי?", CMO, LMO, TMS] + code(STAYM),
            lambda q, p: (ms_stay(p), 0x3))]))

# topic 3: the Moore detector of slides 23-24 on 4 input bits (HEX3 = the first)
OMQ = [("G", 2), ("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1) + hexd(0)
TSQ = "the input bits = HEX3 HEX2 HEX1 HEX0   (HEX3 = the first)"
def bits4(v, n=4):
    return [(v >> (n - 1 - i)) & 1 for i in range(n)]
def seqhex(v, n=4):				# bit i (the first = 0) on HEX(3 - i)
    return {o: x for i, b in enumerate(bits4(v, n)) for o, x in dig(3 - i, b).items()}
def mo_run(v):
    s, st = 0, []
    for a in bits4(v):
        s = mo_nx(s, a); st.append(s)
    return st
W.append(Q(id="MOORESEQ", name="MOORESEQ", title="ארבעה ביטים לגלאי המור", inputs=[9, 8, 7], flat=True, small=True,
    outs=OMQ, hexes=[None, None, None, None], variants=list(range(16)),
    tables=lambda p: ft(OMQ, 2, 1, lambda s, a: {("G", 2): int(s == 2), ("G", 1): mo_nx(s, a) >> 1, ("G", 0): mo_nx(s, a) & 1, **seqhex(p)}),
    answer=lambda p: (mo_run(p).count(2), 0x3), describe=lambda p: f"{p:04b}: states {mo_run(p)}, smile {mo_run(p).count(2)} times",
    B=[LMO + "     " + TSQ + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["גלאי הרצף של מור של שקופיות 23-24. בלוח הלוגיקה שלו.", CMO, LMO, TSQ, FOLLOW,
             "התחילו במצב 0 והכניסו את הביטים שבתצוגה, ביט בכל שעון. באיזה מצב אתם בסוף?"] + code(["S0", "S1", "S2"]),
            lambda q, p: (mo_run(p)[-1], 0x3)),
           (["אחרי כמה מארבעת השעונים החיוך דלק?", LMO, TSQ, "0 = all down"] + cnt(2), lambda q, p: (mo_run(p).count(2), 0x3))]))

# topic 3: the Mealy detector of slides 25-26 on 4 input bits
OLQ = [("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1) + hexd(0)
def me_run(v, n=4):
    s, sm = 0, []
    for a in bits4(v, n):
        sm.append(s & a); s = 1 - a
    return sm
def me_first(v, n=4):
    sm = me_run(v, n)
    return sm.index(1) + 1 if 1 in sm else 0
W.append(Q(id="MEALYSEQ", name="MEALYSEQ", title="ארבעה ביטים לגלאי המילי", inputs=[9, 8], flat=True, small=True,
    outs=OLQ, hexes=[None, None, None, None], variants=list(range(16)),
    tables=lambda p: ft(OLQ, 1, 1, lambda s, a: {("G", 1): s & a, ("G", 0): 1 - a, **seqhex(p)}),
    answer=lambda p: (sum(me_run(p)), 0x3), describe=lambda p: f"{p:04b}: smiles {me_run(p)}",
    B=[LML + "     " + TSQ + "     answer: SW2..SW0"], L=[], F=[],
    steps=[(["גלאי הרצף של מילי של שקופיות 25-26. בלוח הלוגיקה שלו.", "S0 = 0     S1 = 1", LML, TSQ, FOLLOW,
             "התחילו במצב 0. בכל ביט: הציבו אותו בכניסה, הסתכלו על החיוך, ואז שעון. באיזה ביט החיוך דולק לראשונה?",
             "0 = never = all down"] + cnt(4), lambda q, p: (me_first(p), 0x7)),
           (["בכמה מארבעת הביטים החיוך דלק?", LML, TSQ, "0 = all down"] + cnt(2), lambda q, p: (sum(me_run(p)), 0x3))]))

# topic 3: the Moore and the Mealy detectors of slides 23-26 side by side, on 3 input bits
OBD = [("G", 7), ("G", 6), ("G", 5), ("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1)
LBD = ["Moore:  state bits = SW9 SW8     smile = LEDG7     next state bits = LEDG6 LEDG5",
       "Mealy:  state = SW7     smile = LEDG1     next state = LEDG0", "a = SW6"]
TBD = "the input bits = HEX3 HEX2 HEX1   (HEX3 = the first)"
def bd_f(p, st, a):
    ms, me = st >> 1, st & 1
    nx = mo_nx(ms, a)
    return {("G", 7): int(ms == 2), ("G", 6): nx >> 1, ("G", 5): nx & 1, ("G", 1): me & a, ("G", 0): 1 - a, **seqhex(p, 3)}
W.append(Q(id="BOTHDET", name="BOTHDET", title="מור ומילי של השקופיות על אותם ביטים", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=OBD, hexes=[None, None, None, None], variants=list(range(8)),
    tables=lambda p: ft(OBD, 3, 1, lambda st, a: bd_f(p, st, a)),
    answer=lambda p: (me_first(p, 3), 0x3), describe=lambda p: f"{p:03b}: Mealy smiles in bit {me_first(p, 3)}, Moore after clock {me_first(p, 3)}",
    B=[LBD[0] + "     " + LBD[1] + "     " + LBD[2] + "     " + TBD + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["שני גלאי הרצף של שקופיות 23-26, מור ומילי, על אותה כניסה. בלוח הלוגיקה של שניהם.", "Moore:  " + CMO] + LBD + [TBD, FOLLOW,
             "התחילו את שניהם במצב 0. בכל ביט: הציבו אותו בכניסה, הסתכלו, ואז שעון.",
             "באיזה ביט החיוך של המילי דולק לראשונה (לפני השעון)?", "0 = never = all down"] + cnt(3), lambda q, p: (me_first(p, 3), 0x3)),
           (["ואחרי כמה שעונים החיוך של המור דולק לראשונה?"] + LBD + [TBD, "0 = never = all down"] + cnt(3),
            lambda q, p: (me_first(p, 3), 0x3))]))


ORDER = ["DIV3NEXT", "ONEHOT17", "D3AFTER", "D3RESET", "D3EQ", "FFCOUNT", "DIVN", "RHO", "NEXT2", "NEXTEQ", "OUTTAB", "MOOREMEALY", "STATEDIAG", "SHORTEST", "UNREACH", "TRAP",
         "ENCODING",
         "TLNEXT", "TLOUT", "TL1HOT", "TLSTAY", "TLOUTBIT", "TLTRACE", "TLWAIT", "TRAFFIC", "TLCYCLE", "TRAFFICRESET", "TLPOLARITY", "LIGHTCODE", "TLOUTEQ", "ONEHOT", "TRAFFICBUG",
         "MOORE01", "MEALY01", "DIV3CASE", "MOORESTAY", "MOORESEQ", "MEALYSEQ", "BOTHDET", "SEQDET", "SEQCOUNT", "TWODET", "OVERLAP", "MEALYOUT", "LATCH", "ENUM", "DEFAULT", "DIVCODE", "BLOCKBUG", "UPDOWN"]
TOPICS = [(40, "מכונות מצבים: מצבים, מעברים ויציאות", 17), (40, "בקר הרמזור מההרצאה", 15), (40, "מכונות מצבים בקוד וגלאי רצף", 18)]
DESC = {"DIV3NEXT": "המחלק ב-3 של השקופית: המצב הבא, ומתי היציאה נדלקת",
        "ONEHOT17": "קידוד בינארי ואחד-חם של השקופית: מקוד לקוד",
        "TLNEXT": "בקר הרמזור: המצב הבא מטבלת המעברים של השקופית",
        "TLOUT": "בקר הרמזור: הצבעים מטבלת היציאות של השקופית",
        "TL1HOT": "בקר הרמזור באחד-חם: המצב הבא מהטבלה של השקופית",
        "MOORE01": "גלאי המור של השקופית: החיוך והמצב הבא",
        "MEALY01": "גלאי המילי של השקופית: החיוך והמצב הבא",
        "DIV3CASE": "המחלק ב-3 בקוד: איזו שורה של ה-case והמצב הבא",
        "D3AFTER": "המחלק ב-3 של השקופית: באיזה מצב אחרי כמה שעונים",
        "D3RESET": "המחלק ב-3 של השקופית: האיפוס והמצב הבא",
        "D3EQ": "המחלק ב-3: מהטבלה המקודדת למשוואה של ביט",
        "TLSTAY": "בקר הרמזור: המצב הבא, ואיזה חיישן משאיר במקום",
        "TLOUTBIT": "בקר הרמזור: משוואת יציאה מטבלת השקופית",
        "TLTRACE": "בקר הרמזור: שני שעונים עם חיישנים קבועים",
        "TLWAIT": "בקר הרמזור: אחרי כמה שעונים רחוב ירוק",
        "MOORESTAY": "גלאי המור של השקופית: החיוך, ומתי נשארים במקום",
        "MOORESEQ": "גלאי המור של השקופית על ארבעה ביטים",
        "MEALYSEQ": "גלאי המילי של השקופית על ארבעה ביטים",
        "BOTHDET": "גלאי המור והמילי של השקופיות על אותם ביטים",
        "FFCOUNT": "כמה דלגלגים למספר מצבים שבתצוגה: אחד-חם ובינארי",
        "DIVN": "מחלק ב-N: מעקב אחרי המצב הבא, איפה היציאה, כמה דלגלגים",
        "RHO": "מכונה בלי כניסות: שובל ומחזור לפי המצב הבא",
        "NEXT2": "מכונה של שני מצבים: טבלת המעברים",
        "NEXTEQ": "מכונה של שני מצבים: משוואת המצב הבא",
        "OUTTAB": "מכונת מור של 4 מצבים: טבלת היציאות",
        "MOOREMEALY": "מור או מילי - האם היציאה תלויה בכניסה",
        "STATEDIAG": "דיאגרמה של 4 מצבים: לאן עוברים מכל מצב",
        "SHORTEST": "הדרך הקצרה ביותר ממצב 0 למצב 3",
        "UNREACH": "מצב שאי אפשר להגיע אליו ממצב 0",
        "TRAP": "מצב מלכודת, ומצבים עם חץ לעצמם",
        "ENCODING": "קידוד מצבים: בינארי, אחד-חם או גריי",
        "TRAFFIC": "בקר הרמזור: איזה מתג הוא החיישן, כמה זמן צהוב",
        "TLCYCLE": "בקר הרמזור: אורך הצהוב, מחזור שלם, כמה דלגלגים",
        "TRAFFICRESET": "בקר הרמזור: מצב האיפוס 00 והחיישנים",
        "TLPOLARITY": "בקר הרמזור: חיישן פעיל בגבוה או בנמוך",
        "LIGHTCODE": "בקר הרמזור: הקוד של ירוק, צהוב ואדום",
        "TLOUTEQ": "בקר הרמזור בקידוד נסתר: משוואת היציאה",
        "ONEHOT": "בקר הרמזור באחד-חם: איזה ביט לכל מצב",
        "TRAFFICBUG": "בקר הרמזור עם מעבר שגוי: מאיפה ולאן",
        "SEQDET": "גלאי רצף של 3 ביטים: מור או מילי, ומה הרצף",
        "SEQCOUNT": "גלאי רצף: כמה זיהויים ברצף כניסה נתון",
        "TWODET": "גלאי מור וגלאי מילי של אותו רצף, זה ליד זה",
        "OVERLAP": "גלאי רצף: מה הרצף, חופף או לא",
        "MEALYOUT": "מכונת מילי: טבלת היציאות",
        "LATCH": "גלאי מילי בלי ברירת מחדל ליציאה: תפס",
        "ENUM": "enum: הקודים של המצבים לפי סדר השמות",
        "DEFAULT": "הקוד שאין לו שם ושורת ברירת המחדל",
        "DIVCODE": "מחלק ב-N עם שורה שגויה ב-case",
        "BLOCKBUG": "שלושת הבלוקים של מכונת מצבים: איזה שבור",
        "UPDOWN": "מונה למעלה ולמטה: איזה מתג, כמה מצבים"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "מכונות מצבים - מהקל אל הקשה, ואי אפשר בלי הלוח")
