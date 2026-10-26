# -*- coding: utf-8 -*-
# Week 9 class exercise (lecture 9, Harris 5.2.1-5.2.4 + 4.8: half / full adders, ripple-carry, carry-lookahead and prefix
# adders and their delays, subtracters, comparators, parameterized modules). Instructor only.
#   python gen_w9.py [--compile] [--only Q05] [--id <ID>]
import itertools, math, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(9, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0, numq, rv, binl
W = []
B4 = ["a[3:0] = SW9 SW8 SW7 SW6"]
def col(f, n):					# one output column over n inputs (MSB first)
    return [f(r) for r in range(1 << n)]

# ================================================================ topic 1: adders
# a half adder: which LED is the sum, which the carry
W.append(Q(id="HALFADD", name="HALFADD", title="חצי מחבר", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], None, None], variants=[0, 1],
    tables=lambda p: [col(lambda r: (r >> 1) ^ (r & 1) if p == 0 else (r >> 1) & r & 1, 2),
                      col(lambda r: (r >> 1) & r & 1 if p == 0 else (r >> 1) ^ (r & 1), 2)],
    answer=lambda p: (p, 0x1), describe=lambda p: f"sum on LEDG{p}",
    B=["A = SW9     B = SW8     LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח חצי מחבר של שני ביטים. נורה אחת היא הסכום ואחת הנשא.", "A = SW9     B = SW8",
             "איזו נורה היא הסכום? (דולקת כשבדיוק כניסה אחת 1)"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p, 0x1))]))

# a full adder: Cout in a hidden LED, the majority
VFA = list(itertools.permutations(range(3)))
def fa_out(k, r):				# 0 = sum, 1 = cout, 2 = an extra: A AND B (a half adder's carry)
    a, b, c = (r >> 2) & 1, (r >> 1) & 1, r & 1
    return [a ^ b ^ c, int(a + b + c >= 2), a & b][k]
W.append(Q(id="FULLADD", name="FULLADD", title="מחבר מלא", inputs=[9, 8, 7], flat=True,
    outs=[("G", i) for i in range(3)], hexes=[[9], [8], [7], None], variants=VFA,
    tables=lambda p: [col(lambda r: fa_out(p[i], r), 3) for i in range(3)], answer=lambda p: (p.index(1), 0x3),
    describe=lambda p: " ".join(f"LEDG{i}={['S', 'Cout', 'AB'][p[i]]}" for i in range(3)),
    B=["A = SW9     B = SW8     Cin = SW7     LEDG2 LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר מלא, ועוד נורה של הנשא של חצי המחבר הראשון.", "A = SW9     B = SW8     Cin = SW7",
             "S = A ^ B ^ Cin     Cout = AB + ACin + BCin     extra = AB",
             "איזו נורה היא הסכום?"] + code(["LEDG0", "LEDG1", "LEDG2"]), lambda q, p: (p.index(0), 0x3)),
           (["איזו נורה היא", "Cout", "(דולקת כששתיים או יותר מהכניסות 1)?"] + code(["LEDG0", "LEDG1", "LEDG2"]),
            lambda q, p: (p.index(1), 0x3))]))

# a ripple-carry adder with a hidden B
VRB = list(range(1, 16))
def rb_tab(b):
    t = []
    for k in range(5):
        t.append(col(lambda r: (((r >> 1) + b + (r & 1)) >> k) & 1, 5))
    return t
W.append(Q(id="RIPPLE", name="RIPPLE", title="מחבר אדווה עם מספר מוסתר", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VRB,
    tables=rb_tab, answer=lambda b: (16 - b, 0x1F), describe=lambda b: f"B = {b}",
    B=["A = SW9..SW6 (HEX0)     Cin = SW5     S = LEDG3..LEDG0     Cout = LEDG4     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר אדווה של 4 ביטים:", "S = A + B + Cin", "A = SW9..SW6     Cin = SW5     S = LEDG3..0     Cout = LEDG4",
             "המספר השני מוסתר. שימו", "A = 0000, Cin = 0", "ומה המספר המוסתר?", "B = ?", "SW3..SW0 = LEDG3..LEDG0"], lambda q, b: (b, 0xF)),
           (["מה הכניסה הקטנה ביותר שמדליקה את הנשא?", "the smallest A with Cout = 1 (Cin = 0)"] + binl(5), lambda q, b: (16 - b, 0x1F))]))

# a ripple adder with one broken full adder
VBR = [(k, f, b) for k in range(4) for f in range(2) for b in (5, 6, 7, 9, 10, 11, 13, 14)]
def br_sum(p, a):
    k, f, b = p
    c, s = 0, 0
    for i in range(4):
        x, y = (a >> i) & 1, (b >> i) & 1
        si, ci = x ^ y ^ c, int(x + y + c >= 2)
        if i == k:
            if f == 0:
                ci = 0
            else:
                si ^= 1
        s |= si << i
        c = ci
    return s | (c << 4)
W.append(Q(id="BROKENFA", name="BROKENFA", title="מחבר מלא מקולקל", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)] + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VBR,
    tables=lambda p: [col(lambda a: (br_sum(p, a) >> k) & 1, 4) for k in range(5)] + const(bitsof(p[2], 4), 4),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"B = {p[2]}, FA{p[0]} {'carry stuck at 0' if p[1] == 0 else 'sum inverted'}",
    B=["A = SW9..SW6 (HEX0)     B = HEX2     S = LEDG3..LEDG0     Cout = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר אדווה של 4 מחברים מלאים, והמספר השני מוצג בתצוגה. אחד המחברים המלאים מקולקל.",
             "S = A + B     A = SW9..SW6     B = HEX2     S = LEDG3..0, Cout = LEDG4",
             "נסו כמה ערכים בכניסה והשוו לחשבון. איזה מחבר מלא מקולקל? (0 = הימני)", "0 = all down"] + cnt(3),
            lambda q, p: (p[0], 0x3)),
           (["מה התקלה בו?"] + code(["carry out stuck at 0", "sum inverted"], 2), lambda q, p: (p[1], 0x1))]))

# the ripple-carry delay
numq(W, "RIPPLEDELAY", "השהיה של מחבר אדווה", 3, [(n, t) for n in (4, 8, 16, 32) for t in range(2, 10)],
     lambda p: [[p[0] // 10, p[0] % 10, p[1]]], "HEX3 HEX2 = N bits     HEX1 = tFA",
     [(["בתצוגה מחבר אדווה:", "HEX3 HEX2 = N bits     HEX1 = tFA (ns)", "מה ההשהיה שלו (בננו-שניות)?", "t_ripple = N tFA"] + binl(9),
       lambda q, p: (p[0] * p[1], 0x1FF))],
     lambda p: f"{p[0] * p[1]} ns")

# ================================================================ topic 2: carry-lookahead and prefix adders
def gp(a, b):
    return a & b, a | b
LAB = "HEX3 = A (hex)     HEX2 = B (hex)"
VAB = [(a, b) for a in range(16) for b in range(16)]
VAB = random.Random(91).sample(VAB, 200)
W.append(Q(id="GENKILL", name="GENKILL", title="מייצר, מעביר או הורג", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], None, None], variants=[0, 1],
    tables=lambda p: [col(lambda r: ((r >> 1) & r & 1) if p == 0 else ((r >> 1) | (r & 1)), 2),
                      col(lambda r: ((r >> 1) | (r & 1)) if p == 0 else ((r >> 1) & r & 1), 2)],
    answer=lambda p: (p, 0x1), describe=lambda p: f"G on LEDG{p}",
    B=["Ai = SW9     Bi = SW8     LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח עמודה אחת של מחבר: נורה אחת היא", "Gi = Ai Bi", "(מייצר נשא) והשנייה", "Pi = Ai + Bi", "(מעביר נשא).",
             "Ai = SW9     Bi = SW8", "איזו נורה היא", "Gi", "?"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p, 0x1))]))

numq(W, "GENPROP", "אותות מייצר ומעביר", 2, VAB, lambda p: [[p[0], p[1]]], LAB,
     [(["בתצוגה שני מספרים של 4 ביטים:", LAB, "מה אותות המייצר של כל העמודות?", "Gi = Ai Bi", "SW3..SW0 = G3..G0"],
       lambda q, p: (p[0] & p[1], 0xF)),
      (["ומה אותות המעביר?", "Pi = Ai + Bi", "SW3..SW0 = P3..P0"], lambda q, p: (p[0] | p[1], 0xF))],
     lambda p: f"G {p[0] & p[1]:04b} P {p[0] | p[1]:04b}")

def blockgp(a, b):
    g, p = gp(a, b)
    G_ = 0
    for i in range(4):
        G_ = ((g >> i) & 1) | (((p >> i) & 1) & G_)
    P_ = int(p == 15)
    return G_, P_
numq(W, "BLOCKGP", "מייצר ומעביר של בלוק", 2, VAB, lambda p: [[p[0], p[1]]], LAB,
     [(["בתצוגה שני מספרים של 4 ביטים:", LAB, "האם הבלוק כולו מעביר נשא?", "P3:0 = P3 P2 P1 P0"] + UP0("כן", "לא"),
       lambda q, p: (blockgp(*p)[1], 0x1)),
      (["האם הבלוק כולו מייצר נשא?", "G3:0 = G3 + P3 (G2 + P2 (G1 + P1 G0))"] + UP0("כן", "לא"), lambda q, p: (blockgp(*p)[0], 0x1))],
     lambda p: f"G3:0 {blockgp(*p)[0]} P3:0 {blockgp(*p)[1]}")

VABC = [(a, b, c) for a in range(16) for b in range(16) for c in range(2)]
VABC = random.Random(92).sample(VABC, 200)
LABC = "HEX3 = A (hex)     HEX2 = B (hex)     HEX1 = Cin"
numq(W, "CARRIES", "הנשאים של כל העמודות", 3, VABC, lambda p: [[p[0], p[1], p[2]]], LABC,
     [(["בתצוגה שני מספרים של 4 ביטים ונשא כניסה:", LABC, "מה הנשא שיוצא מכל עמודה?", "Ci = Gi + Pi C(i-1)",
        "SW3..SW0 = C3 C2 C1 C0"],
       lambda q, p: (sum((((p[0] & ((2 << i) - 1)) + (p[1] & ((2 << i) - 1)) + p[2]) >> (i + 1) & 1) << i for i in range(4)), 0xF)),
      (["ומה הסכום (4 ביטים)?", "SW3..SW0"], lambda q, p: ((p[0] + p[1] + p[2]) & 15, 0xF))],
     lambda p: f"{p[0]} + {p[1]} + {p[2]}")

LCL = "page 1 (SW9 down):  HEX3 = tpg   HEX2 = tpg_block   HEX1 = tAND_OR   HEX0 = tFA"
LCLb = "page 2 (SW9 up):    HEX3 HEX2 = N     HEX1 = k"
VCL = rv(93, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9), r.randint(1, 9), r.choice((8, 16, 32)), r.choice((2, 4))))
def tcla(p):
    return p[0] + p[1] + (p[4] // p[5] - 1) * p[2] + p[5] * p[3]
numq(W, "CLADELAY", "השהיה של מחבר הצצה קדימה", 4, VCL,
     lambda p: [[p[0], p[1], p[2], p[3]], [p[4] // 10, p[4] % 10, p[5], 0]], "tpg tpg_block tAND_OR tFA / N k",
     [(["בתצוגה שני דפים של מחבר הצצה קדימה עם בלוקים:", LCL, LCLb,
        "מה ההשהיה שלו?", "tCLA = tpg + tpg_block + (N/k - 1) tAND_OR + k tFA"] + binl(8), lambda q, p: (tcla(p), 0xFF))],
     lambda p: f"tCLA {tcla(p)}", pages2=True)

LPF = "page 1 (SW9 down):  HEX3 = tpg   HEX2 = tpg_prefix   HEX1 = tXOR"
LPFb = "page 2 (SW9 up):    HEX3 HEX2 = N"
VPF = rv(94, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9), r.choice((4, 8, 16, 32, 64))))
def tpa(p):
    return p[0] + int(math.log2(p[3])) * p[1] + p[2]
numq(W, "PREFIXDELAY", "השהיה של מחבר תחיליות", 3, VPF,
     lambda p: [[p[0], p[1], p[2]], [p[3] // 10, p[3] % 10, 0]], "tpg tpg_prefix tXOR / N",
     [(["בתצוגה שני דפים של מחבר תחיליות:", LPF, LPFb, "מה ההשהיה שלו?", "tPA = tpg + log2(N) tpg_prefix + tXOR"] + binl(7),
       lambda q, p: (tpa(p), 0x7F))],
     lambda p: f"tPA {tpa(p)}", pages2=True)

# ================================================================ topic 3: subtracters, comparators, parameterized modules
VSB = list(range(1, 16))
W.append(Q(id="SUBTRACTER", name="SUBTRACTER", title="מחסר עם מספר מוסתר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSB,
    tables=lambda b: [col(lambda a: ((a + (~b & 15) + 1) >> k) & 1, 4) for k in range(5)],
    answer=lambda b: (b, 0xF), describe=lambda b: f"B = {b}",
    B=["A = SW9..SW6 (HEX0)     Y = LEDG3..LEDG0     Cout = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחסר:", "Y = A - B = A + ~B + 1", "A = SW9..SW6     Y = LEDG3..0     Cout = LEDG4",
             "מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.", "במשלים ל-2 מוצאים את הנגדי כך: הופכים את כל הביטים (0 ל-1 ו-1 ל-0), ואז מוסיפים 1.",
             "שימו", "A = 0000", "מה רואים? זה המספר הנגדי למספר המוסתר. העתיקו:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, b: ((-b) & 15, 0xF)),
           (["מה המספר המוסתר? (מצאו כניסה שנותנת תוצאה 0)", "B = ?     SW3..SW0"], lambda q, b: (b, 0xF))]))

VEQ = [(b, k) for b in range(16) for k in range(4)]
W.append(Q(id="EQBUG", name="EQBUG", title="משווה עם באג", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VEQ,
    tables=lambda p: [col(lambda a: int(((a ^ p[0]) & ~(1 << p[1]) & 15) == 0), 4)],
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"B = {p[0]:04b}, bit {p[1]} not compared",
    B=["A = SW9..SW6 (HEX0)     A == B = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח משווה שוויון:", "LEDG0 = (A == B)", "אבל ביט אחד לא מחובר להשוואה, אז שני ערכים מדליקים את הנורה.",
             "A = SW9..SW6", "איזה ביט לא נבדק? (0 = הימני)", "0 = all down"] + cnt(3), lambda q, p: (p[1], 0x3))]))

VC3 = [(b, perm) for b in range(1, 15) for perm in itertools.permutations(range(3))]
VC3 = random.Random(95).sample(VC3, len(VC3))
def c3(k, a, b):
    return [int(a == b), int(a < b), int(a > b)][k]
LEDS3 = code(["LEDG0", "LEDG1", "LEDG2"])
W.append(Q(id="COMPARE3", name="COMPARE3", title="משווה עם שלוש יציאות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(3)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VC3,
    tables=lambda p: [col(lambda a: c3(p[1][i], a, p[0]), 4) for i in range(3)], answer=lambda p: (p[0], 0xF),
    describe=lambda p: f"B = {p[0]}; " + " ".join(f"LEDG{i}={['==', '<', '>'][p[1][i]]}" for i in range(3)),
    B=["A = SW9..SW6 (HEX0)     LEDG2 LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח משווה של הכניסה עם מספר מוסתר (בלי סימן). שלוש נורות:", "A == B,  A < B,  A > B  (in some order)",
             "A = SW9..SW6", "איזו נורה היא", "A < B", "?"] + LEDS3, lambda q, p: (p[1].index(1), 0x3)),
           (["מה המספר המוסתר?", "B = ?     SW3..SW0"], lambda q, p: (p[0], 0xF))]))

VSU = [(b, sg) for b in range(1, 15) for sg in range(2)]
def sv(x):
    return x - 16 if x & 8 else x
W.append(Q(id="SIGNEDCMP", name="SIGNEDCMP", title="השוואה עם סימן או בלי", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSU,
    tables=lambda p: [col(lambda a: int(sv(a) < sv(p[0])) if p[1] else int(a < p[0]), 4)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"A < {p[0]:04b} {'signed' if p[1] else 'unsigned'}",
    B=["A = SW9..SW6 (HEX0)     A < B = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח משווה:", "LEDG0 = (A < B)", "המספר השני מוסתר.", "A = SW9..SW6",
             "מה המספר המוסתר? (הכניסה הראשונה שהנורה כבתה בה, בסדר המתאים)", "B = ?     SW3..SW0"], lambda q, p: (p[0], 0xF)),
           (["ההשוואה עם סימן (משלים ל-2) או בלי? בדקו", "A = 1000"] + code(["unsigned", "signed"]), lambda q, p: (p[1], 0x1))]))

VSL = [(b, ok) for b in range(16) for ok in range(2)]
def slt(p, a):
    b, ok = p
    d = (a - b) & 15
    if ok:
        return int(sv(a) < sv(b))
    return d >> 3					# the naive version: the sign of A - B (wrong on overflow)
VSL = [p for p in VSL if p[1] == 1 or any(slt(p, a) != int(sv(a) < sv(p[0])) for a in range(16))]
W.append(Q(id="SLT", name="SLT", title="קטן-מ עם סימן: האם יש באג גלישה?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSL,
    tables=lambda p: [col(lambda a: slt(p, a), 4)], answer=lambda p: (p[1], 0x1),
    describe=lambda p: f"B = {p[0]:04b}, {'correct' if p[1] else 'sign of A-B (overflow bug)'}",
    B=["A = SW9..SW6 (HEX0)     A < B = LEDG0 (signed)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח משווה עם סימן:", "A < B  if  A - B < 0", "המספר השני מוסתר. אולי המשווה רק בודק את ביט הסימן של", "A - B",
             "ואז הוא טועה כשיש גלישה. נסו את כל הכניסות והשוו לחשבון.", "A = 1000 ... 0111",
             "האם המשווה נכון תמיד?"] + UP0("נכון תמיד", "טועה לפעמים"), lambda q, p: (p[1], 0x1))]))

# a parameterized adder: what width was it built with
VWD = [2, 3, 4]
W.append(Q(id="WIDTH", name="WIDTH", title="מודול עם פרמטר", inputs=[9, 8, 7, 6, 5, 4], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=VWD,
    tables=lambda w: [col(lambda r: (((r >> 3) + (r & 7)) & ((1 << w) - 1)) >> k & 1 if k < w else 0, 6) for k in range(4)],
    answer=lambda w: (w, 0x7), describe=lambda w: f"adder #(width = {w}), the inputs cut to {w} bits",
    B=["a = SW9 SW8 SW7     b = SW6 SW5 SW4     y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר מודול עם פרמטר:", "module adder #(parameter width = 8) (input logic [width-1:0] a, b, output logic [width-1:0] y);",
             "a = SW9 SW8 SW7     b = SW6 SW5 SW4     y = LEDG3..LEDG0",
             "המודול נבנה עם רוחב קטן יותר. כמה ביטים יש ל-", "y", "?"] + cnt(4), lambda q, w: (w, 0x7))]))

VMX = [(w, s) for w in (1, 2, 3) for s in range(2)]
W.append(Q(id="MUXPARAM", name="MUXPARAM", title="בורר עם פרמטר", inputs=[9, 8, 7, 6, 5, 4, 3], flat=True,
    outs=[("G", i) for i in range(3)], hexes=[None, None, None, None], variants=VMX,
    tables=lambda p: [col(lambda r: (((r >> 1) & 7) if ((r & 1) ^ p[1]) else ((r >> 4) & 7)) >> k & 1 if k < p[0] else 0, 7)
                      for k in range(3)], small=True,
    answer=lambda p: (p[0], 0x3), describe=lambda p: f"mux2 #(width = {p[0]}), s = 0 passes d{p[1]}",
    B=["d0 = SW9 SW8 SW7     d1 = SW6 SW5 SW4     s = SW3     y = LEDG2..LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח בורר עם פרמטר:", "mux2 #(width) (d0, d1, s, y)", "d0 = SW9 SW8 SW7     d1 = SW6 SW5 SW4     s = SW3",
             "כש-", "s = 0", "איזו כניסה עוברת?"] + code(["d0", "d1"]), lambda q, p: (p[1], 0x1)),
           (["מה הרוחב (כמה ביטים עוברים ליציאה)?"] + cnt(3), lambda q, p: (p[0], 0x3))]))

# the carry out of a subtracter = no borrow (A >= B)
W.append(Q(id="NOBORROW", name="NOBORROW", title="הנשא של המחסר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: ((a + (~b & 15) + 1) >> 4) & 1, 4)], answer=lambda b: (b, 0xF),
    describe=lambda b: f"B = {b}: Cout = 1 when A >= B",
    B=["A = SW9..SW6 (HEX0)     Cout = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחסר, ורק הנשא שלו מוצג:", "A - B = A + ~B + 1     Cout = LEDG4", "A = SW9..SW6",
             "הנשא דולק כשאין לווה, כלומר כשהכניסה גדולה או שווה למספר המוסתר. מה המספר המוסתר?",
             "B = the smallest A with Cout = 1     SW3..SW0"], lambda q, b: (b, 0xF))]))

# a prefix cell: black (G and P) or gray (G only), which LED is G
VCE = [(gl, black) for gl in range(2) for black in range(2)]
def cell(p, r):					# r = G_hi P_hi G_lo P_lo (SW9..SW6)
    gh, ph, gl_, pl = (r >> 3) & 1, (r >> 2) & 1, (r >> 1) & 1, r & 1
    return gh | (ph & gl_), (ph & pl) if p[1] else 0
W.append(Q(id="PREFIXCELL", name="PREFIXCELL", title="תא של מחבר תחיליות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], [7], [6]], variants=VCE,
    tables=lambda p: [col(lambda r: cell(p, r)[0] if p[0] == 0 else cell(p, r)[1], 4),
                      col(lambda r: cell(p, r)[1] if p[0] == 0 else cell(p, r)[0], 4)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"G on LEDG{p[0]}, {'black' if p[1] else 'gray'} cell",
    B=["G_i:k = SW9   P_i:k = SW8   G_k-1:j = SW7   P_k-1:j = SW6     LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח תא אחד של מחבר תחיליות:", "G_i:j = G_i:k + P_i:k G_k-1:j     P_i:j = P_i:k P_k-1:j",
             "G_i:k = SW9   P_i:k = SW8   G_k-1:j = SW7   P_k-1:j = SW6",
             "איזו נורה היא", "G_i:j", "?"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p[0], 0x1)),
           (["תא שחור מחשב את שניהם; תא אפור (בשורה האחרונה) רק את", "G", ". איזה תא?"] + code(["gray", "black"]),
            lambda q, p: (p[1], 0x1))]))

# ================================================================ new questions (added): topic 1
# a full adder whose Cin is tied to a hidden constant; S and Cout on hidden LEDs
VFC = [(sl, c) for sl in range(2) for c in range(2)]
def fc(p, r, k):				# k = 0 sum, 1 cout; r = A B
    a, b, c = (r >> 1) & 1, r & 1, p[1]
    return [a ^ b ^ c, int(a + b + c >= 2)][k]
W.append(Q(id="FACIN", name="FACIN", title="מחבר מלא עם נשא כניסה קבוע", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], None, None], variants=VFC,
    tables=lambda p: [col(lambda r: fc(p, r, 0 if i == p[0] else 1), 2) for i in range(2)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"S on LEDG{p[0]}, Cin tied to {p[1]}",
    B=["A = SW9     B = SW8     Cin = hidden constant     LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר מלא. נשא הכניסה מחובר בפנים לקבוע מוסתר (0 או 1).", "A = SW9     B = SW8",
             "S = A ^ B ^ Cin     Cout = AB + ACin + BCin", "נורה אחת היא הסכום ואחת הנשא.",
             "איזו נורה היא הסכום? (משתנה בכל פעם שמזיזים מתג אחד)"] + code(["LEDG0", "LEDG1"]), lambda q, p: (p[0], 0x1)),
           (["מה הקבוע שמחובר לנשא הכניסה?", "Cin = ?"] + code(["0", "1"]), lambda q, p: (p[1], 0x1))]))

# a full adder with a hidden inverter on one of its inputs
VIN = [(sl, k) for sl in range(2) for k in range(3)]
def inv_fa(p, r, kind):				# r = A B Cin; input k (0 = A, 1 = B, 2 = Cin) is inverted
    return fa_out(kind, r ^ (4 >> p[1]))
W.append(Q(id="INVERTEDIN", name="INVERTEDIN", title="מחבר מלא עם מהפך מוסתר", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], [7], None], variants=VIN,
    tables=lambda p: [col(lambda r: inv_fa(p, r, 0 if i == p[0] else 1), 3) for i in range(2)],
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"S on LEDG{p[0]}, input {['A', 'B', 'Cin'][p[1]]} inverted",
    B=["A = SW9     B = SW8     Cin = SW7     LEDG1 LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר מלא, אבל כניסה אחת עוברת דרך מהפך מוסתר.", "A = SW9     B = SW8     Cin = SW7",
             "S = A ^ B ^ Cin     Cout = AB + ACin + BCin", "נורה אחת היא הסכום ואחת הנשא.",
             "כשכל המתגים למטה, המחבר רואה בדיוק כניסה אחת שהיא 1.", "איזו נורה היא", "Cout", "?"] + code(["LEDG0", "LEDG1"]),
            lambda q, p: (1 - p[0], 0x1)),
           (["איזו כניסה עוברת דרך המהפך? הרימו מתג אחד בכל פעם: מתי שתי הנורות כבות?", "A = SW9     B = SW8     Cin = SW7"]
            + code(["A", "B", "Cin"]), lambda q, p: (p[1], 0x3))]))

# signed overflow of a 4-bit adder with a hidden B, only the overflow LED
def ovf(a, b):
    s = (a + b) & 15
    return int((a & 8) == (b & 8) and (s & 8) != (a & 8))
W.append(Q(id="OVERFLOW", name="OVERFLOW", title="גלישה בחיבור עם סימן", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: ovf(a, b), 4)], answer=lambda b: (b, 0xF),
    describe=lambda b: f"B = {b:04b} ({b - 16 if b & 8 else b})",
    B=["A = SW9..SW6 (HEX0)     overflow = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר של 4 ביטים עם סימן (משלים ל-2). המספר השני מוסתר, ורק נורת הגלישה מוצגת.",
             "S = A + B     A = SW9..SW6     overflow = LEDG0",
             "גלישה קורית רק כששני המספרים באותו סימן. נסו את כל הכניסות: האם המספר המוסתר חיובי או שלילי?"]
            + code(["B > 0", "B < 0"]), lambda q, b: (b >> 3, 0x1)),
           (["מה המספר המוסתר? (ספרו כמה כניסות גורמות לגלישה)", "B = ?     SW3..SW0 (4 bits, two's complement)"],
            lambda q, b: (b, 0xF))]))

# ================================================================ new questions: topic 2
# block G and P with a hidden B
W.append(Q(id="BLOCKHIDDEN", name="BLOCKHIDDEN", title="מייצר ומעביר של בלוק עם מספר מוסתר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: int((a | b) == 15), 4), col(lambda a: int(a + b >= 16), 4)],
    answer=lambda b: (16 - b, 0x1F), describe=lambda b: f"B = {b:04b}",
    B=["A = SW9..SW6 (HEX0)     P3:0 = LEDG0     G3:0 = LEDG1     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח בלוק של 4 ביטים, והמספר השני מוסתר:", "P3:0 = P3 P2 P1 P0 = LEDG0     Pi = Ai + Bi", "A = SW9..SW6",
             "באילו ביטים הכניסה חייבת להיות 1 כדי שהבלוק יעביר נשא?", "SW3..SW0 = the bits of A that must be 1"],
            lambda q, b: (~b & 15, 0xF)),
           (["לכמה כניסות שונות הבלוק מעביר נשא?", "P3:0 = LEDG0     A = SW9..SW6"] + binl(5),
            lambda q, b: (1 << bin(b).count("1"), 0x1F)),
           (["מה הכניסה הקטנה ביותר שבה הבלוק מייצר נשא?", "G3:0 = G3 + P3 (G2 + P2 (G1 + P1 G0)) = LEDG1     A = SW9..SW6"]
            + binl(5), lambda q, b: (16 - b, 0x1F))]))

# one column computes P with a hidden gate: OR and XOR are both right, AND is wrong
def pb_sum(p, a):
    b, k, g = p
    c, s = 0, 0
    for i in range(4):
        x, y = (a >> i) & 1, (b >> i) & 1
        gi, pi = x & y, x | y
        if i == k:
            pi = [x | y, x ^ y, x & y][g]
        s |= (x ^ y ^ c) << i
        c = gi | (pi & c)
    return s | (c << 4)
VPB = [(b, k, g) for k in (1, 2, 3) for g in range(3) for b in range(16) if b & ((1 << k) - 1)]
VPB = random.Random(96).sample(VPB, len(VPB))
W.append(Q(id="PBUG", name="PBUG", title="מעביר שנבנה משער אחר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)] + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VPB,
    tables=lambda p: [col(lambda a: (pb_sum(p, a) >> k) & 1, 4) for k in range(5)] + const(bitsof(p[0], 4), 4),
    answer=lambda p: (p[1] + 1 if p[2] == 2 else 0, 0x7),
    describe=lambda p: f"B = {p[0]}, column {p[1]} P = {['OR', 'XOR', 'AND'][p[2]]}",
    B=["A = SW9..SW6 (HEX0)     B = HEX2     S = LEDG3..LEDG0     Cout = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחבר הצצה קדימה של 4 ביטים, והמספר השני מוצג בתצוגה:", "Ci = Gi + Pi C(i-1)     Si = Ai ^ Bi ^ C(i-1)",
             "A = SW9..SW6     B = HEX2     S = LEDG3..0     Cout = LEDG4",
             "בעמודה אחת המעביר נבנה משער מוסתר, אחד מאלה:", "Pi = Ai + Bi     or     Pi = Ai ^ Bi     or     Pi = Ai Bi",
             "נסו כמה ערכים והשוו לחשבון. האם המחבר נכון תמיד?"] + UP0("נכון תמיד", "טועה לפעמים"),
            lambda q, p: (int(p[2] != 2), 0x1)),
           (["באיזו עמודה התקלה? (0 = הימנית)"] + code(["correct", "column 0", "column 1", "column 2", "column 3"]),
            lambda q, p: (p[1] + 1 if p[2] == 2 else 0, 0x7))]))

# level 1 and 2 of a prefix tree
def gpspan(a, b, hi, lo):			# G and P of the block hi:lo
    G_, P_ = 0, 1
    for i in range(lo, hi + 1):
        g, p_ = (a >> i) & (b >> i) & 1, ((a | b) >> i) & 1
        G_ = g | (p_ & G_)
        P_ &= p_
    return G_, P_
def lvl1(p):
    g3, p3 = gpspan(p[0], p[1], 3, 2)
    g1, p1 = gpspan(p[0], p[1], 1, 0)
    return (g3 << 3) | (p3 << 2) | (g1 << 1) | p1
def lvl2(p):
    g, p_ = gpspan(p[0], p[1], 3, 0)
    return (g << 1) | p_
numq(W, "PREFIXTREE", "עץ התחיליות", 2, VAB, lambda p: [[p[0], p[1]]], LAB,
     [(["בתצוגה שני מספרים של 4 ביטים:", LAB, "מחבר תחיליות, רמה 1: מה המייצר והמעביר של זוגות העמודות?",
        "G_i:j = G_i:k + P_i:k G_k-1:j     P_i:j = P_i:k P_k-1:j     Gi = Ai Bi     Pi = Ai + Bi",
        "SW3 = G3:2     SW2 = P3:2     SW1 = G1:0     SW0 = P1:0"], lambda q, p: (lvl1(p), 0xF)),
      (["רמה 2: מה המייצר והמעביר של כל הבלוק?", LAB, "G3:0 = G3:2 + P3:2 G1:0     P3:0 = P3:2 P1:0",
        "SW1 = G3:0     SW0 = P3:0"], lambda q, p: (lvl2(p), 0x3))],
     lambda p: f"level1 {lvl1(p):04b} level2 {lvl2(p):02b}")

# a race: ripple, CLA (4-bit blocks) and prefix from one gate delay and tFA (lecture slide 34)
def race(p):
    n, tg, tfa = p
    tr = n * tfa
    tc = tg + 6 * tg + (n // 4 - 1) * 2 * tg + 4 * tfa
    tp = tg + int(math.log2(n)) * 2 * tg + tg
    return tr, tc, tp
VRC = [(n, tg, tfa) for n in (4, 8, 16, 32) for tg in range(1, 10) for tfa in range(tg, 10)]
VRC = [p for p in VRC if sorted(race(p))[0] < sorted(race(p))[1]]
VRC = random.Random(97).sample(VRC, len(VRC))			# 168 variants, ripple wins in 18 (N = 4, tFA < 1.5 tgate)
LRC = "HEX3 HEX2 = N bits     HEX1 = tgate     HEX0 = tFA"
numq(W, "ADDERRACE", "מרוץ המחברים", 4, VRC, lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]]], LRC,
     [(["בתצוגה מספר הביטים, השהיית שער של 2 כניסות והשהיית מחבר מלא (בננו-שניות):", LRC,
        "מה ההשהיה של מחבר אדווה?", "t_ripple = N tFA"] + binl(9), lambda q, p: (race(p)[0], 0x1FF)),
      (["מה ההשהיה של מחבר תחיליות?", LRC, "tPA = tpg + log2(N) tpg_prefix + tXOR     tpg = tXOR = tgate     tpg_prefix = 2 tgate"]
       + binl(8), lambda q, p: (race(p)[2], 0xFF)),
      (["מה ההשהיה של מחבר הצצה קדימה עם בלוקים של 4 ביטים?", LRC,
        "tCLA = tpg + tpg_block + (N/4 - 1) tAND_OR + 4 tFA     tpg = tgate     tpg_block = 6 tgate     tAND_OR = 2 tgate"]
       + binl(8), lambda q, p: (race(p)[1], 0xFF)),
      (["איזה מחבר הכי מהיר? (לפי שלוש ההשהיות שחישבתם)", LRC] + code(["ripple", "CLA", "prefix"]),
       lambda q, p: (race(p).index(min(race(p))), 0x3))],
     lambda p: "ripple %d CLA %d prefix %d" % race(p))

# ================================================================ new questions: topic 3
# a subtracter with a bug: no +1, or one bit of B not inverted
def sb_y(p, a):
    b, bug = p
    nb = ~b & 15
    cin = 0 if bug == 1 else 1
    if bug >= 2:
        nb ^= 1 << (bug - 2)
    return (a + nb + cin) & 15
SBN = ["correct", "missing +1", "bit 0 of B not inverted", "bit 1 of B not inverted", "bit 2 of B not inverted", "bit 3 of B not inverted"]
VSG = [(b, bug) for b in range(1, 16) for bug in range(6) if bug < 2 or (b >> (bug - 2)) & 1]
VSG = random.Random(98).sample(VSG, len(VSG))
W.append(Q(id="SUBBUG", name="SUBBUG", title="מחסר עם באג", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VSG,
    tables=lambda p: [col(lambda a: (sb_y(p, a) >> k) & 1, 4) for k in range(4)] + const(bitsof(p[0], 4), 4),
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"B = {p[0]}, {SBN[p[1]]}",
    B=["A = SW9..SW6 (HEX0)     B = HEX2     Y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחסר של 4 ביטים, והמספר השני מוצג בתצוגה:", "Y = A - B = A + ~B + 1",
             "A = SW9..SW6     B = HEX2     Y = LEDG3..0", "אולי יש בו באג. נסו כמה ערכים והשוו לחשבון. האם המחסר נכון?"]
            + UP0("נכון", "לא נכון"), lambda q, p: (int(p[1] == 0), 0x1)),
           (["מה הבאג? (בכמה התוצאה רחוקה מהנכונה?)", "A = SW9..SW6     B = HEX2     Y = LEDG3..0"] + code(SBN, 2),
            lambda q, p: (p[1], 0x7))]))

# min or max: a comparator and a mux, hidden B
VMM = [(b, mx) for b in range(1, 15) for mx in range(2)]
def mm(p, a):
    b, mx = p
    return (b if a < b else a) if mx else (a if a < b else b)
W.append(Q(id="MINMAX", name="MINMAX", title="משווה ובורר: מינימום או מקסימום", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VMM,
    tables=lambda p: [col(lambda a: (mm(p, a) >> k) & 1, 4) for k in range(4)], answer=lambda p: (p[0], 0xF),
    describe=lambda p: f"{'max' if p[1] else 'min'}(A, {p[0]})",
    B=["A = SW9..SW6 (HEX0)     y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח משווה ובורר (בלי סימן), והמספר השני מוסתר. אחד משני המעגלים:",
             "y = (A < B) ? A : B     or     y = (A < B) ? B : A", "A = SW9..SW6     y = LEDG3..0",
             "מה המעגל מחשב?"] + code(["min(A, B)", "max(A, B)"]), lambda q, p: (p[1], 0x1)),
           (["מה המספר המוסתר?", "A = SW9..SW6     y = LEDG3..0", "B = ?     SW3..SW0"], lambda q, p: (p[0], 0xF))]))

# four instances of one less-than module: which wiring
VLT = [(b, w) for b in range(1, 15) for w in range(4)]
VLT = random.Random(99).sample(VLT, len(VLT))
LTW = ["lt(A, B)", "lt(B, A)", "~lt(A, B)", "~lt(B, A)"]	# the wirings (p[1]), in the order of the step-1 relations
LTN = ["lt(B, A)", "~lt(A, B)", "lt(A, B)", "~lt(B, A)"]	# the step-2 list (another order)
def ltw(p, a):
    b, w = p
    return [int(a < b), int(b < a), int(not a < b), int(not b < a)][w]
W.append(Q(id="LTWIRING", name="LTWIRING", title="ארבעה מופעים של משווה קטן-מ", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)] + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VLT,
    tables=lambda p: [col(lambda a: ltw(p, a), 4)] + const(bitsof(p[0], 4), 4),
    answer=lambda p: (LTN.index(LTW[p[1]]), 0x3), describe=lambda p: f"B = {p[0]}, LEDG0 = {LTW[p[1]]}",
    B=["A = SW9..SW6 (HEX0)     B = HEX2     LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מודול משווה (בלי סימן), והמספר השני מוצג בתצוגה:", "lt(x, y) = (x < y)",
             "A = SW9..SW6     B = HEX2     LEDG0", "הנורה מחוברת למופע אחד של המודול, אולי עם מהפך. איזה יחס היא מראה?"]
            + code(["A < B", "A > B", "A >= B", "A <= B"]), lambda q, p: (p[1], 0x3)),
           (["איזה מופע מחובר לנורה?", "lt(x, y) = (x < y)"] + code(LTN), lambda q, p: (LTN.index(LTW[p[1]]), 0x3))]))

# ================================================================ easy questions from the lecture slides (start of each topic)
def show_c(vals, n):				# per-student constant digits on the display (one list per digit)
    return [c for v in vals for c in const(bitsof(v, 4), n)]
# topic 1, slide 5: the half adder; set the A B shown on HEX1 HEX0, read Cout and S
W.append(Q(id="HATABLE", name="HATABLE", title="חצי המחבר מהשקף", inputs=[9, 8], flat=True,
    outs=[("G", 1), ("G", 0)] + hexd(1) + hexd(0), hexes=[[9], [8], None, None], variants=[(a, b) for a in range(2) for b in range(2)],
    tables=lambda p: [[(r >> 1) & r & 1 for r in range(4)], [((r >> 1) ^ r) & 1 for r in range(4)]] + show_c(p, 2),
    answer=lambda p: (((p[0] & p[1]) << 1) | (p[0] ^ p[1]), 0x3), describe=lambda p: f"row A B = {p[0]}{p[1]}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     row = HEX1 HEX0     Cout = LEDG1     S = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 5: חצי מחבר. בלוח בדיוק המעגל של השקף.", "S = A ^ B     Cout = AB",
             "A = SW9 (HEX3)     B = SW8 (HEX2)     Cout = LEDG1     S = LEDG0",
             "שימו בכניסות את השורה שמוצגת בתצוגה:", "HEX1 = A     HEX0 = B", "מה היציאות?", "SW1 = Cout     SW0 = S"],
            lambda q, p: (((p[0] & p[1]) << 1) | (p[0] ^ p[1]), 0x3))]))

# topic 1, slide 5: the full adder; set the A B Cin shown on HEX3 HEX2 HEX1, read Cout and S
def fa_cs(p):
    r = (p[0] << 2) | (p[1] << 1) | p[2]
    return (fa_out(1, r) << 1) | fa_out(0, r)
W.append(Q(id="FATABLE", name="FATABLE", title="המחבר המלא מהשקף", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1), hexes=[None, None, None, None],
    variants=list(itertools.product(range(2), repeat=3)),
    tables=lambda p: [col(lambda r: fa_out(1, r), 3), col(lambda r: fa_out(0, r), 3)] + show_c(p, 3),
    answer=lambda p: (fa_cs(p), 0x3), describe=lambda p: f"row A B Cin = {p[0]}{p[1]}{p[2]}",
    B=["A = SW9     B = SW8     Cin = SW7     row = HEX3 HEX2 HEX1     Cout = LEDG1     S = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 5: מחבר מלא. בלוח בדיוק המעגל של השקף.", "S = A ^ B ^ Cin     Cout = AB + ACin + BCin",
             "A = SW9     B = SW8     Cin = SW7     Cout = LEDG1     S = LEDG0",
             "שימו בכניסות את השורה שמוצגת בתצוגה:", "HEX3 = A     HEX2 = B     HEX1 = Cin", "מה היציאות?", "SW1 = Cout     SW0 = S"],
            lambda q, p: (fa_cs(p), 0x3))]))

# topic 1, slide 8: a 4-bit ripple-carry chain; set the A shown on HEX3, B on HEX2, read S and Cout
VR4 = random.Random(81).sample([(a, b) for a in range(16) for b in range(16)], 200)
W.append(Q(id="RIPPLE4", name="RIPPLE4", title="שרשרת האדווה מהשקף", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VR4,
    tables=lambda p: [col(lambda a: ((a + p[1]) >> k) & 1, 4) for k in range(5)] + show_c(p, 4),
    answer=lambda p: ((p[0] + p[1]) >> 4, 0x1), describe=lambda p: f"{p[0]} + {p[1]} = {p[0] + p[1]}",
    B=["A = SW9..SW6 (HEX0)     HEX3 = the A to set     B = HEX2     S = LEDG3..LEDG0     Cout = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 8: מחבר אדווה, שרשרת של מחברים מלאים. בלוח שרשרת של 4 מהם, ונשא הכניסה 0.", "S = A + B     Cin = 0",
             "A = SW9..SW6 (HEX0)     B = HEX2     S = LEDG3..LEDG0", "שימו במתגים את המספר שמוצג ב-", "HEX3",
             "מה הסכום?", "SW3..SW0 = S3..S0"], lambda q, p: ((p[0] + p[1]) & 15, 0xF)),
           (["האם יוצא נשא מהמחבר המלא האחרון?", "A = SW9..SW6 = HEX3     B = HEX2     Cout = LEDG4"] + UP0("כן", "לא"),
            lambda q, p: ((p[0] + p[1]) >> 4, 0x1))]))

# topic 2, slide 12: the column P and G of 4 columns, B hidden; A = 0000 shows P = B, then the slide's A = 1011
W.append(Q(id="GPCOLUMNS", name="GPCOLUMNS", title="מעביר ומייצר של כל עמודה מהשקף", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(16)),
    tables=lambda b: [col(lambda a: ((a | b) >> k) & 1, 4) for k in range(4)] + [col(lambda a: ((a & b) >> k) & 1, 4) for k in range(4)],
    answer=lambda b: (b & 11, 0xF), describe=lambda b: f"B = {b:04b}",
    B=["A = SW9..SW6 (HEX0)     P3..P0 = LEDG3..LEDG0     G3..G0 = LEDG7..LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 12: אותות מעביר ומייצר לכל עמודה. בלוח המעגל של 4 עמודות, והמספר השני מוסתר.", "Pi = Ai + Bi     Gi = Ai Bi",
             "A = SW9..SW6 (HEX0)     P3..P0 = LEDG3..LEDG0", "שימו", "A = 0000", "מה אותות המעביר?", "SW3..SW0 = P3..P0"],
            lambda q, b: (b, 0xF)),
           (["עכשיו שימו את המספר מהדוגמה בשקף:", "A = 1011", "מה אותות המייצר?", "Gi = Ai Bi     A = SW9..SW6 (HEX0)     G3..G0 = LEDG7..LEDG4",
             "SW3..SW0 = G3..G0"], lambda q, b: (b & 11, 0xF))]))

# topic 2, slides 14-16: the block P3:0 and G3:0; set the A shown on HEX3, B on HEX2
VB4 = random.Random(82).sample([(a, b) for a in range(16) for b in range(16)], 200)
W.append(Q(id="BLOCK4", name="BLOCK4", title="הבלוק של 4 ביטים מהשקף", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0), ("G", 1)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VB4,
    tables=lambda p: [col(lambda a: blockgp(a, p[1])[1], 4), col(lambda a: blockgp(a, p[1])[0], 4)] + show_c(p, 4),
    answer=lambda p: ((blockgp(*p)[0] << 1) | blockgp(*p)[1], 0x3), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}",
    B=["A = SW9..SW6 (HEX0)     HEX3 = the A to set     B = HEX2     P3:0 = LEDG0     G3:0 = LEDG1     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקפים 14-16: מעביר ומייצר של בלוק של 4 ביטים. בלוח המעגל של השקף.",
             "P3:0 = P3 P2 P1 P0     G3:0 = G3 + P3 (G2 + P2 (G1 + P1 G0))",
             "A = SW9..SW6 (HEX0)     B = HEX2     P3:0 = LEDG0     G3:0 = LEDG1", "שימו במתגים את המספר שמוצג ב-", "HEX3",
             "מה אותות הבלוק?", "SW1 = G3:0     SW0 = P3:0"], lambda q, p: ((blockgp(*p)[0] << 1) | blockgp(*p)[1], 0x3))]))

# topic 2, slide 30: one black cell of the prefix adder; set the 4 inputs shown on HEX3..HEX0
def bc(p):
    g, p_ = cell((0, 1), (p[0] << 3) | (p[1] << 2) | (p[2] << 1) | p[3])
    return (g << 1) | p_
W.append(Q(id="BLACKCELL", name="BLACKCELL", title="התא השחור מהשקף", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", 1), ("G", 0)] + hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None],
    variants=list(itertools.product(range(2), repeat=4)),
    tables=lambda p: [col(lambda r: cell((0, 1), r)[0], 4), col(lambda r: cell((0, 1), r)[1], 4)] + show_c(p, 4),
    answer=lambda p: (bc(p), 0x3), describe=lambda p: "G_i:k P_i:k G_k-1:j P_k-1:j = " + "".join(map(str, p)),
    B=["G_i:k = SW9   P_i:k = SW8   G_k-1:j = SW7   P_k-1:j = SW6     G_i:j = LEDG1     P_i:j = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 30: תא שחור של מחבר תחיליות. בלוח המעגל של התא.", "G_i:j = G_i:k + P_i:k G_k-1:j     P_i:j = P_i:k P_k-1:j",
             "G_i:k = SW9   P_i:k = SW8   G_k-1:j = SW7   P_k-1:j = SW6     G_i:j = LEDG1     P_i:j = LEDG0",
             "שימו במתגים את הערכים שבתצוגה:", "HEX3 = G_i:k   HEX2 = P_i:k   HEX1 = G_k-1:j   HEX0 = P_k-1:j",
             "מה יציאות התא?", "SW1 = G_i:j     SW0 = P_i:j"], lambda q, p: (bc(p), 0x3))]))

# topic 3, slide 36: the subtracter A + ~B + 1; set the B shown on HEX2, read ~B and Y
VNB = random.Random(83).sample([(a, b) for a in range(16) for b in range(16)], 200)
W.append(Q(id="SUBNOTB", name="SUBNOTB", title="המחסר מהשקף", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VNB,
    tables=lambda p: [col(lambda b: (~b >> k) & 1, 4) for k in range(4)]
                     + [col(lambda b: ((p[0] - b) >> k) & 1, 4) for k in range(4)] + show_c(p, 4),
    answer=lambda p: ((p[0] - p[1]) & 15, 0xF), describe=lambda p: f"{p[0]} - {p[1]}: ~B {~p[1] & 15:04b}, Y {(p[0] - p[1]) & 15:04b}",
    B=["B = SW9..SW6 (HEX0)     HEX2 = the B to set     A = HEX3     ~B = LEDG3..LEDG0     Y = LEDG7..LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 36: מחסר, מהפכים ואחריהם מחבר עם נשא כניסה 1. בלוח המעגל של השקף.", "Y = A - B = A + ~B + 1",
             "B = SW9..SW6 (HEX0)     ~B = LEDG3..LEDG0", "שימו במתגים את המספר שמוצג ב-", "HEX2",
             "מה יוצא מהמהפכים?", "SW3..SW0 = ~B"], lambda q, p: (~p[1] & 15, 0xF)),
           (["ומה התוצאה של המחסר?", "A = HEX3     B = SW9..SW6 = HEX2     Y = LEDG7..LEDG4", "SW3..SW0 = Y"],
            lambda q, p: ((p[0] - p[1]) & 15, 0xF))]))

# topic 3, slide 37: the equality comparator (an XNOR per bit, an AND), B hidden
W.append(Q(id="EQXNOR", name="EQXNOR", title="משווה השוויון מהשקף", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(16)),
    tables=lambda b: [col(lambda a: (~(a ^ b) >> k) & 1, 4) for k in range(4)] + [col(lambda a: int(a == b), 4)],
    answer=lambda b: (b, 0xF), describe=lambda b: f"B = {b:04b}",
    B=["A = SW9..SW6 (HEX0)     XNOR3..XNOR0 = LEDG3..LEDG0     Equal = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 37: משווה שוויון. בלוח המעגל של השקף, והמספר השני מוסתר.",
             "Xi = Ai XNOR Bi = LEDGi     Equal = X3 X2 X1 X0 = LEDG4", "A = SW9..SW6 (HEX0)", "שימו", "A = 0000",
             "אילו נורות דולקות?", "SW3..SW0 = LEDG3..LEDG0"], lambda q, b: (~b & 15, 0xF)),
           (["מה המספר המוסתר? מצאו כניסה שמדליקה את כל הנורות.", "A = SW9..SW6     Equal = LEDG4", "B = ?     SW3..SW0"],
            lambda q, b: (b, 0xF))]))

# topic 3, slide 40: an instance mux2 #(4), d0 and d1 hidden
VM2 = rv(84, 200, lambda r: (lambda d0, d1: (d0, d1) if d0 != d1 else None)(r.randrange(16), r.randrange(16)))
W.append(Q(id="MUX2W4", name="MUX2W4", title="הבורר עם הפרמטר מהשקף", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9], None, None, None], variants=VM2,
    tables=lambda p: [[(p[0] >> k) & 1, (p[1] >> k) & 1] for k in range(4)],
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"d0 = {p[0]:04b}, d1 = {p[1]:04b}",
    B=["s = SW9 (HEX3)     y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 40: בורר עם פרמטר. בלוח מופע ברוחב 4, ושתי הכניסות מוסתרות.", "mux2 #(4) m (d0, d1, s, y);     y = s ? d1 : d0",
             "s = SW9 (HEX3)     y = LEDG3..LEDG0", "שימו", "s = 0", "מה עובר ליציאה?", "SW3..SW0 = y = d0"], lambda q, p: (p[0], 0xF)),
           (["עכשיו שימו", "s = 1", "מה עובר ליציאה?", "y = s ? d1 : d0     s = SW9 (HEX3)     y = LEDG3..LEDG0", "SW3..SW0 = y = d1"],
            lambda q, p: (p[1], 0xF))]))

# ================================================================ more easy questions from the lecture slides
# topic 1, slide 5: the half adder; the display shows an output pair Cout S - how many input rows give it
W.append(Q(id="HAROWS", name="HAROWS", title="חצי המחבר: כמה שורות", inputs=[9, 8], flat=True,
    outs=[("G", 1), ("G", 0)] + hexd(1) + hexd(0), hexes=[[9], [8], None, None], variants=[(c, s) for c in range(2) for s in range(2)],
    tables=lambda p: [[(r >> 1) & r & 1 for r in range(4)], [((r >> 1) ^ r) & 1 for r in range(4)]] + show_c(p, 2),
    answer=lambda p: ([1, 2, 1, 0][2 * p[0] + p[1]], 0x3), describe=lambda p: f"Cout S = {p[0]}{p[1]}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     Cout = LEDG1     S = LEDG0     HEX1 HEX0 = the outputs     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 5: חצי מחבר. בלוח בדיוק המעגל של השקף.", "S = A ^ B     Cout = AB",
             "A = SW9 (HEX3)     B = SW8 (HEX2)     Cout = LEDG1     S = LEDG0",
             "בתצוגה זוג יציאות:", "HEX1 = Cout     HEX0 = S",
             "נסו את ארבע השורות. בכמה שורות היציאות בדיוק כמו בתצוגה?", "0 = all down"] + cnt(3),
            lambda q, p: ([1, 2, 1, 0][2 * p[0] + p[1]], 0x3))]))
# topic 1, slide 5: the full adder counts the 1 inputs; the display shows how many inputs to raise
W.append(Q(id="FACOUNT", name="FACOUNT", title="המחבר המלא סופר אחדות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)] + hexd(0), hexes=[[9], [8], [7], None], variants=[0, 1, 2, 3],
    tables=lambda k: [col(lambda r: fa_out(1, r), 3), col(lambda r: fa_out(0, r), 3)] + show_c([k], 3),
    answer=lambda k: (k, 0x3), describe=lambda k: f"{k} ones",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     Cin = SW7 (HEX1)     HEX0 = how many ones     Cout = LEDG1     S = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 5: מחבר מלא. בלוח בדיוק המעגל של השקף.", "S = A ^ B ^ Cin     Cout = AB + ACin + BCin",
             "A = SW9 (HEX3)     B = SW8 (HEX2)     Cin = SW7 (HEX1)     Cout = LEDG1     S = LEDG0",
             "הרימו בדיוק כמה כניסות כמו המספר שבתצוגה (אילו שתרצו):", "HEX0 = how many inputs are 1",
             "מה היציאות?", "SW1 = Cout     SW0 = S"], lambda q, k: (k, 0x3))]))
# topic 1, slide 8: the ripple chain with its carry in; the A shown on HEX3, B on HEX2
VRC1 = random.Random(85).sample([(a, b) for a in range(16) for b in range(16)], 100)
LRC1 = "A = SW9..SW6 (HEX0)     Cin = SW5 (HEX1)     B = HEX2     S = LEDG3..LEDG0     Cout = LEDG4"
W.append(Q(id="RIPPLECIN", name="RIPPLECIN", small=True, title="נשא הכניסה של שרשרת האדווה", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(5)] + hexd(3) + hexd(2), hexes=[None, None, [5], [9, 8, 7, 6]], variants=VRC1,
    tables=lambda p: [col(lambda r: (((r >> 1) + p[1] + (r & 1)) >> k) & 1, 5) for k in range(5)] + show_c(p, 5),
    answer=lambda p: (p[0] + p[1] + 1, 0x1F), describe=lambda p: f"{p[0]} + {p[1]} + Cin",
    B=[LRC1 + "     HEX3 = the A to set     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בשקף 8: מחבר אדווה, שרשרת של מחברים מלאים. בלוח שרשרת של 4 מהם, עם נשא כניסה.", "S = A + B + Cin", LRC1,
             "שימו במתגים את המספר שמוצג ב-", "HEX3", "ונשא כניסה 0. מה היציאות?", "SW4 = Cout     SW3..SW0 = S3..S0"],
            lambda q, p: (p[0] + p[1], 0x1F)),
           (["עכשיו הרימו את נשא הכניסה:", "Cin = SW5 = 1", LRC1, "מה היציאות עכשיו?", "SW4 = Cout     SW3..SW0 = S3..S0"],
            lambda q, p: (p[0] + p[1] + 1, 0x1F))]))
# topic 1, slide 8: the carry out of every full adder in the chain
def carries(a, b, c=0):
    return sum((((a & ((2 << i) - 1)) + (b & ((2 << i) - 1)) + c) >> (i + 1) & 1) << i for i in range(4))
VRC2 = random.Random(86).sample([(a, b) for a in range(16) for b in range(16)], 200)
W.append(Q(id="RIPPLEC", name="RIPPLEC", title="הנשא עובר בשרשרת", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VRC2,
    tables=lambda p: [col(lambda a: (carries(a, p[1]) >> k) & 1, 4) for k in range(4)] + show_c(p, 4),
    answer=lambda p: (carries(*p), 0xF), describe=lambda p: f"{p[0]} + {p[1]}: carries {carries(*p):04b}",
    B=["A = SW9..SW6 (HEX0)     HEX3 = the A to set     B = HEX2     C3..C0 = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 8: מחבר אדווה. הנשא עובר מכל מחבר מלא לבא אחריו. בלוח שרשרת של 4, ונשא הכניסה 0.",
             "Ci = the carry out of full adder i     C3 = Cout",
             "A = SW9..SW6 (HEX0)     B = HEX2     C3..C0 = LEDG3..LEDG0", "שימו במתגים את המספר שמוצג ב-", "HEX3",
             "מה הנשאים שיוצאים מהמחברים המלאים?", "SW3..SW0 = C3..C0"], lambda q, p: (carries(*p), 0xF))]))

# topic 2, slide 11: one column's G and P; set the Ai Bi shown on HEX1 HEX0
W.append(Q(id="GPROW", name="GPROW", title="מייצר ומעביר של עמודה מהשקף", inputs=[9, 8], flat=True,
    outs=[("G", 1), ("G", 0)] + hexd(1) + hexd(0), hexes=[[9], [8], None, None], variants=[(a, b) for a in range(2) for b in range(2)],
    tables=lambda p: [[(r >> 1) & r & 1 for r in range(4)], [((r >> 1) | r) & 1 for r in range(4)]] + show_c(p, 2),
    answer=lambda p: (((p[0] & p[1]) << 1) | (p[0] | p[1]), 0x3), describe=lambda p: f"Ai Bi = {p[0]}{p[1]}",
    B=["Ai = SW9 (HEX3)     Bi = SW8 (HEX2)     row = HEX1 HEX0     Gi = LEDG1     Pi = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקף 11: אותות מייצר ומעביר של עמודה אחת. בלוח המעגל של השקף.", "Gi = Ai Bi     Pi = Ai + Bi",
             "Ai = SW9 (HEX3)     Bi = SW8 (HEX2)     Gi = LEDG1     Pi = LEDG0",
             "שימו בכניסות את הערכים שמוצגים בתצוגה:", "HEX1 = Ai     HEX0 = Bi", "מה האותות?", "SW1 = Gi     SW0 = Pi"],
            lambda q, p: (((p[0] & p[1]) << 1) | (p[0] | p[1]), 0x3))]))
# topic 2, slide 18: the block carry out C3 = G3:0 + P3:0 Cin; A shown on HEX3, B on HEX2
VBC = random.Random(87).sample([(a, b) for a in range(16) for b in range(16)], 100)
LBC = "A = SW9..SW6 (HEX0)     Cin = SW5 (HEX1)     B = HEX2     C3 = LEDG0"
def c3b(p, c):
    g, p_ = blockgp(*p)
    return g | (p_ & c)
W.append(Q(id="BLOCKCIN", name="BLOCKCIN", small=True, title="הנשא שיוצא מהבלוק", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", 0)] + hexd(3) + hexd(2), hexes=[None, None, [5], [9, 8, 7, 6]], variants=VBC,
    tables=lambda p: [col(lambda r: c3b(((r >> 1), p[1]), r & 1), 5)] + show_c(p, 5),
    answer=lambda p: (c3b(p, 1), 0x1), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}: G3:0 {blockgp(*p)[0]} P3:0 {blockgp(*p)[1]}",
    B=[LBC + "     HEX3 = the A to set     answer: SW0"], L=[], F=[],
    steps=[(["בשקף 18: הנשא שיוצא מבלוק של 4 ביטים. בלוח המעגל של השקף.", "C3 = G3:0 + P3:0 Cin", LBC,
             "שימו במתגים את המספר שמוצג ב-", "HEX3", "ונשא כניסה 0. האם יוצא נשא?"] + UP0("כן", "לא"), lambda q, p: (c3b(p, 0), 0x1)),
           (["עכשיו הרימו את נשא הכניסה:", "Cin = SW5 = 1", LBC, "האם יוצא נשא עכשיו?"] + UP0("כן", "לא"),
            lambda q, p: (c3b(p, 1), 0x1))]))
# topic 2, slides 19 and 25: the carry chain between two 4-bit CLA blocks; the blocks' G and P hidden
def chain(p, c):
    g0, p0, g1, p1 = p
    c3 = g0 | (p0 & c)
    return ((g1 | (p1 & c3)) << 1) | c3
W.append(Q(id="CLACHAIN", name="CLACHAIN", title="שרשרת הבלוקים מהשקף", inputs=[9], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], None, None, None], variants=list(itertools.product(range(2), repeat=4)),
    tables=lambda p: [[chain(p, c) >> 1 for c in range(2)], [chain(p, c) & 1 for c in range(2)]],
    answer=lambda p: (chain(p, 1), 0x3), describe=lambda p: "G3:0 P3:0 G7:4 P7:4 = " + "".join(map(str, p)),
    B=["Cin = SW9 (HEX3)     C3 = LEDG0     C7 = LEDG1     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקפים 19 ו-25: מחבר הצצה קדימה עם בלוקים של 4 ביטים. בלוח שני הבלוקים הראשונים, והמספרים מוסתרים.",
             "C3 = G3:0 + P3:0 Cin     C7 = G7:4 + P7:4 C3", "Cin = SW9 (HEX3)     C3 = LEDG0     C7 = LEDG1",
             "שימו", "Cin = 0", "מה הנשאים שיוצאים מהבלוקים?", "SW1 = C7     SW0 = C3"], lambda q, p: (chain(p, 0), 0x3)),
           (["עכשיו שימו", "Cin = 1", "מה הנשאים עכשיו?", "Cin = SW9 (HEX3)     C3 = LEDG0     C7 = LEDG1", "SW1 = C7     SW0 = C3"],
            lambda q, p: (chain(p, 1), 0x3))]))
# topic 2, slide 29: in the prefix adder Cin is G_-1, and C_i = G_i:-1; A shown on HEX3, B on HEX2, Cin = 1
VPC = random.Random(88).sample([(a, b) for a in range(16) for b in range(16)], 100)
LPC = "A = SW9..SW6 (HEX0)     G_-1 = Cin = SW5 (HEX1)     B = HEX2     G_3:-1 .. G_0:-1 = LEDG3..LEDG0"
W.append(Q(id="PREFIXCIN", name="PREFIXCIN", small=True, title="נשא הכניסה של מחבר התחיליות", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, [5], [9, 8, 7, 6]], variants=VPC,
    tables=lambda p: [col(lambda r: (carries(r >> 1, p[1], r & 1) >> k) & 1, 5) for k in range(4)] + show_c(p, 5),
    answer=lambda p: (carries(p[0], p[1], 1), 0xF), describe=lambda p: f"{p[0]} + {p[1]} + 1: G_i:-1 {carries(p[0], p[1], 1):04b}",
    B=[LPC + "     HEX3 = the A to set     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 29: מחבר תחיליות. עמודה מינוס 1 מחזיקה את נשא הכניסה, ונשא הכניסה לעמודה הבאה הוא מייצר של בלוק.",
             "G_-1 = Cin     C_i = G_i:-1", LPC, "שימו במתגים את המספר שמוצג ב-", "HEX3", "ונשא כניסה 1. מה הנשאים?",
             "Cin = SW5 = 1     SW3..SW0 = G_3:-1 G_2:-1 G_1:-1 G_0:-1"], lambda q, p: (carries(p[0], p[1], 1), 0xF))]))

# topic 3, slide 36: the subtracter's +1 is the adder's carry in; A shown on HEX3, B on HEX2
VSC = random.Random(89).sample([(a, b) for a in range(16) for b in range(16) if a != b], 100)
LSC = "A = SW9..SW6 (HEX0)     Cin = SW5 (HEX1)     B = HEX2     Y = LEDG3..LEDG0"
W.append(Q(id="SUBCIN", name="SUBCIN", small=True, title="ה-1 של המחסר", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, [5], [9, 8, 7, 6]], variants=VSC,
    tables=lambda p: [col(lambda r: (((r >> 1) + (~p[1] & 15) + (r & 1)) >> k) & 1, 5) for k in range(4)] + show_c(p, 5),
    answer=lambda p: ((p[0] - p[1] - 1) & 15, 0xF), describe=lambda p: f"{p[0]} - {p[1]}",
    B=[LSC + "     HEX3 = the A to set     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 36: מחסר, מהפכים ומחבר. ה-1 נכנס בנשא הכניסה של המחבר. בלוח המעגל, ונשא הכניסה במתג.",
             "Y = A + ~B + Cin", LSC, "שימו במתגים את המספר שמוצג ב-", "HEX3", "ונשא כניסה 1. מה התוצאה?", "SW3..SW0 = Y"],
            lambda q, p: ((p[0] - p[1]) & 15, 0xF)),
           (["עכשיו הורידו את נשא הכניסה:", "Cin = SW5 = 0", LSC, "מה התוצאה עכשיו?", "SW3..SW0 = Y"],
            lambda q, p: ((p[0] - p[1] - 1) & 15, 0xF))]))
# topic 3, slide 37: the XNOR of each bit; A shown on HEX3, B on HEX2 - how many bits are equal
VEC = random.Random(90).sample([(a, b) for a in range(16) for b in range(16)], 200)
W.append(Q(id="EQCOUNT", name="EQCOUNT", title="משווה השוויון: כמה ביטים שווים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VEC,
    tables=lambda p: [col(lambda a: (~(a ^ p[1]) >> k) & 1, 4) for k in range(4)] + show_c(p, 4),
    answer=lambda p: (4 - bin(p[0] ^ p[1]).count("1"), 0x7), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}",
    B=["A = SW9..SW6 (HEX0)     HEX3 = the A to set     B = HEX2     Xi = LEDGi     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 37: משווה שוויון. לכל ביט שער", "XNOR", "ואחריהם", "AND", ". בלוח שערי הביטים של השקף.",
             "Xi = Ai XNOR Bi = LEDGi", "A = SW9..SW6 (HEX0)     B = HEX2     X3..X0 = LEDG3..LEDG0",
             "שימו במתגים את המספר שמוצג ב-", "HEX3", "בכמה ביטים המספרים שווים?", "0 = all down"] + cnt(4),
            lambda q, p: (4 - bin(p[0] ^ p[1]).count("1"), 0x7))]))
# topic 3, slide 38: signed less-than = the sign bit of A - B; A shown on HEX3, B on HEX2
VSS = random.Random(91).sample([(a, b) for a in range(16) for b in range(16)], 200)
LSS = "A = SW9..SW6 (HEX0)     B = HEX2     Y = A - B = LEDG3..LEDG0     A < B = Y3 = LEDG4"
W.append(Q(id="SLTSIGN", name="SLTSIGN", title="קטן-מ מהשקף: ביט הסימן", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7, 6]], variants=VSS,
    tables=lambda p: [col(lambda a: ((a - p[1]) >> k) & 1, 4) for k in range(4)] + [col(lambda a: ((a - p[1]) >> 3) & 1, 4)] + show_c(p, 4),
    answer=lambda p: (((p[0] - p[1]) >> 3) & 1, 0x1), describe=lambda p: f"{p[0]:04b} - {p[1]:04b} = {(p[0] - p[1]) & 15:04b}",
    B=[LSS + "     HEX3 = the A to set     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקף 38: קטן-מ עם סימן. מחסר, והיציאה היא ביט הסימן של ההפרש. בלוח המעגל של השקף.",
             "A < B  if  A - B < 0", LSS, "שימו במתגים את המספר שמוצג ב-", "HEX3", "מה ההפרש?", "SW3..SW0 = Y"],
            lambda q, p: ((p[0] - p[1]) & 15, 0xF)),
           (["מה המעגל אומר: האם", "A < B", "?", "A < B = Y3 = LEDG4"] + UP0("כן", "לא"), lambda q, p: (((p[0] - p[1]) >> 3) & 1, 0x1))]))

ORDER = ["HATABLE", "FATABLE", "RIPPLE4", "HAROWS", "FACOUNT", "RIPPLECIN", "RIPPLEC", "HALFADD", "FULLADD", "FACIN", "INVERTEDIN", "RIPPLE", "BROKENFA", "RIPPLEDELAY", "OVERFLOW",
         "GPCOLUMNS", "BLOCK4", "BLACKCELL", "GPROW", "BLOCKCIN", "CLACHAIN", "PREFIXCIN", "GENKILL", "GENPROP", "BLOCKGP", "BLOCKHIDDEN", "CARRIES", "PBUG", "CLADELAY", "PREFIXCELL", "PREFIXTREE",
         "PREFIXDELAY", "ADDERRACE",
         "SUBNOTB", "EQXNOR", "MUX2W4", "SUBCIN", "EQCOUNT", "SLTSIGN", "SUBTRACTER", "NOBORROW", "SUBBUG", "EQBUG", "COMPARE3", "MINMAX", "LTWIRING", "SIGNEDCMP", "SLT", "WIDTH",
         "MUXPARAM"]
TOPICS = [(40, "מחברים: חצי, מלא ואדווה", 15), (40, "הצצה קדימה ותחיליות", 18), (40, "מחסרים, משווים ופרמטרים", 17)]
DESC = {"HAROWS": "חצי המחבר מהשקף: כמה שורות נותנות את היציאות שבתצוגה",
        "FACOUNT": "המחבר המלא מהשקף סופר אחדות",
        "RIPPLECIN": "שרשרת האדווה מהשקף: עם נשא כניסה 0 ו-1",
        "RIPPLEC": "שרשרת האדווה מהשקף: הנשא מכל מחבר מלא",
        "GPROW": "מייצר ומעביר של עמודה מהשקף: השורה שבתצוגה",
        "BLOCKCIN": "הנשא שיוצא מהבלוק מהשקף: עם נשא כניסה 0 ו-1",
        "CLACHAIN": "שרשרת הבלוקים מהשקף: הנשאים בין הבלוקים",
        "PREFIXCIN": "מחבר התחיליות מהשקף: נשא הכניסה הוא עמודה מינוס 1",
        "SUBCIN": "המחסר מהשקף: ה-1 בנשא הכניסה",
        "EQCOUNT": "משווה השוויון מהשקף: כמה ביטים שווים",
        "SLTSIGN": "קטן-מ מהשקף: ההפרש וביט הסימן",
        "HATABLE": "חצי המחבר מהשקף: השורה שבתצוגה",
        "FATABLE": "המחבר המלא מהשקף: השורה שבתצוגה",
        "RIPPLE4": "שרשרת האדווה מהשקף: הסכום והנשא",
        "GPCOLUMNS": "מעביר ומייצר של כל עמודה מהשקף, מספר מוסתר",
        "BLOCK4": "מעביר ומייצר של הבלוק מהשקף",
        "BLACKCELL": "התא השחור מהשקף: הערכים שבתצוגה",
        "SUBNOTB": "המחסר מהשקף: המהפכים והתוצאה",
        "EQXNOR": "משווה השוויון מהשקף: הנורות, ומה המספר",
        "MUX2W4": "הבורר עם הפרמטר מהשקף: שתי הכניסות המוסתרות",
        "HALFADD": "חצי מחבר: איזו נורה הסכום",
        "FULLADD": "מחבר מלא: איזו נורה הסכום ואיזו הנשא",
        "RIPPLE": "מחבר אדווה עם מספר מוסתר: המספר, ומתי יש נשא",
        "BROKENFA": "מחבר אדווה עם מחבר מלא מקולקל: איזה ומה התקלה",
        "RIPPLEDELAY": "השהיה של מחבר אדווה",
        "GENKILL": "עמודה אחת: מייצר ומעביר",
        "GENPROP": "אותות מייצר ומעביר של 4 עמודות",
        "BLOCKGP": "מייצר ומעביר של בלוק של 4 ביטים",
        "CARRIES": "הנשאים של כל העמודות, והסכום",
        "CLADELAY": "השהיה של מחבר הצצה קדימה",
        "PREFIXDELAY": "השהיה של מחבר תחיליות",
        "SUBTRACTER": "מחסר עם מספר מוסתר",
        "NOBORROW": "הנשא של המחסר: מתי אין לווה",
        "PREFIXCELL": "תא של מחבר תחיליות: שחור או אפור",
        "EQBUG": "משווה שוויון שביט אחד שלו לא מחובר",
        "COMPARE3": "משווה עם שלוש יציאות: איזו נורה, ומה המספר",
        "SIGNEDCMP": "השוואה עם סימן או בלי",
        "SLT": "קטן-מ עם סימן: האם יש באג גלישה",
        "WIDTH": "מחבר עם פרמטר: איזה רוחב",
        "MUXPARAM": "בורר עם פרמטר: איזו כניסה, איזה רוחב",
        "FACIN": "מחבר מלא עם נשא כניסה קבוע מוסתר",
        "INVERTEDIN": "מחבר מלא עם מהפך מוסתר באחת הכניסות",
        "OVERFLOW": "גלישה בחיבור עם סימן: מה המספר המוסתר",
        "BLOCKHIDDEN": "מייצר ומעביר של בלוק עם מספר מוסתר",
        "PBUG": "מעביר שנבנה משער אחר: האם המחבר נכון",
        "PREFIXTREE": "עץ התחיליות: רמה 1 ורמה 2",
        "ADDERRACE": "מרוץ המחברים: אדווה, הצצה קדימה ותחיליות",
        "SUBBUG": "מחסר עם באג: איזה",
        "MINMAX": "משווה ובורר: מינימום או מקסימום, ומה המספר",
        "LTWIRING": "ארבעה מופעים של משווה קטן-מ: איזה מחובר"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "מחברים, משווים ומודולים עם פרמטר - מהקל אל הקשה, ואי אפשר בלי הלוח")
