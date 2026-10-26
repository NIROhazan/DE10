# -*- coding: utf-8 -*-
# Week 11 class exercise (lecture 11, Harris 5.3-5.5: fixed point (Ua.b, Qa.b), saturating arithmetic, IEEE 754 floating
# point and its addition; counters, the digitally controlled oscillator, shift registers; memory arrays, ROM / RAM, logic
# with memories, register files). Instructor only.
#   python gen_w11.py [--compile] [--only Q05] [--id <ID>]
import itertools, math, random, struct, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(11, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0, numq, rv, binl, digs, show
W = []
def col(f, n):
    return [f(r) for r in range(1 << n)]
def f32(v):
    return struct.unpack(">I", struct.pack(">f", v))[0]

# ================================================================ topic 1: fixed and floating point
VFU = rv(111, 200, lambda r: (r.choice((4, 5, 6)), r.randrange(256)))
W.append(Q(id="FIXEDU", name="FIXEDU", title="נקודה קבועה בלי סימן", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=VFU,
    tables=lambda p: const(bitsof(p[1], 8) + bitsof(p[0], 4) + bitsof(8 - p[0], 4)),
    answer=lambda p: ((p[1] & ((1 << (8 - p[0])) - 1)) << (4 - (8 - p[0])), 0xF),
    describe=lambda p: f"U{p[0]}.{8 - p[0]} {p[1]:08b} = {p[1] / (1 << (8 - p[0]))}",
    B=["the bits = LEDG7..LEDG0     a = HEX1     b = HEX0 (the format Ua.b)     answer: SW5..SW0"], L=[], F=[],
    steps=[(["בנורות מספר בנקודה קבועה בלי סימן, ובתצוגה הפורמט:", "Ua.b:   a = HEX1 integer bits     b = HEX0 fraction bits",
             "מה החלק השלם שלו?"] + binl(6), lambda q, p: (p[1] >> (8 - p[0]), 0x3F)),
           (["כמה שישה-עשריות יש בחלק השבור? (למשל 0.75 = 12/16)", "fraction x 16"] + BIN4,
            lambda q, p: ((p[1] & ((1 << (8 - p[0])) - 1)) << (4 - (8 - p[0])), 0xF))]))

VFQ = rv(112, 200, lambda r: r.randrange(256))
def qv(x):
    return (x - 256 if x & 128 else x) / 16
W.append(Q(id="FIXEDQ", name="FIXEDQ", title="נקודה קבועה עם סימן", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=VFQ,
    tables=lambda x: const(bitsof(x, 8)), answer=lambda x: ((-x if x & 128 else x) & 255 & 15, 0xF),
    describe=lambda x: f"Q4.4 {x:08b} = {qv(x)}",
    B=["the bits = LEDG7..LEDG0 (Q4.4)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בנורות מספר", "Q4.4", "(משלים ל-2, 4 ביטים שלמים כולל הסימן, 4 שבורים).", "LEDG7..LEDG0",
             "האם הוא שלילי?"] + UP0("שלילי", "חיובי"), lambda q, x: (x >> 7, 0x1)),
           (["מה החלק השלם של הערך המוחלט שלו? (שלילי: הפכו את כל הביטים והוסיפו 1)"] + BIN4,
            lambda q, x: ((((-x) & 255) if x & 128 else x) >> 4, 0xF)),
           (["וכמה שישה-עשריות בחלק השבור של הערך המוחלט?"] + BIN4, lambda q, x: ((((-x) & 255) if x & 128 else x) & 15, 0xF))]))

LUQ = "HEX3 = the integer part (hex)     HEX1 HEX0 = the fraction (hundredths)"
numq(W, "TOFIXED", "לכתוב בנקודה קבועה", 3, [(i, f) for i in range(1, 16) for f in (0, 25, 50, 75)],
     lambda p: [[p[0], 0, p[1] // 10, p[1] % 10]] if False else [[p[0], p[1] // 10, p[1] % 10]],
     "HEX3 = integer     HEX2 HEX1 = hundredths",
     [(["בתצוגה מספר עשרוני:", "HEX3 = the integer part (hex)     HEX2 HEX1 = hundredths", "כתבו אותו בפורמט", "U4.4", ":",
        "SW7..SW4 = integer     SW3..SW0 = fraction x 16"], lambda q, p: ((p[0] << 4) | (p[1] * 16 // 100), 0xFF))],
     lambda p: f"{p[0]}.{p[1]:02d}")

LSA = "HEX3 = A (hex)     HEX2 = B (hex)     (unsigned 4 bits)"
numq(W, "SATURATE", "חשבון רוויה", 2, random.Random(113).sample([(a, b) for a in range(16) for b in range(16)], 200),
     lambda p: [[p[0], p[1]]], LSA,
     [(["בתצוגה שני מספרים של 4 ביטים בלי סימן:", LSA, "מה החיבור הרגיל שלהם ב-4 ביטים (הנשא נזרק)?", "SW3..SW0"],
       lambda q, p: ((p[0] + p[1]) & 15, 0xF)),
      (["ומה החיבור ברוויה (אם הסכום גדול מ-15, התוצאה 15)?", "SW3..SW0"], lambda q, p: (min(15, p[0] + p[1]), 0xF))],
     lambda p: f"{p[0]} + {p[1]}: wrap {(p[0] + p[1]) & 15}, saturate {min(15, p[0] + p[1])}")

# IEEE 754 single precision: the 32 bits on two pages of 4 hex digits
def fpages(v):
    b = f32(v)
    return [[(b >> 28) & 15, (b >> 24) & 15, (b >> 20) & 15, (b >> 16) & 15], [(b >> 12) & 15, (b >> 8) & 15, (b >> 4) & 15, b & 15]]
LFP = "page 1 (SW9 down): the high 16 bits (hex)     page 2 (SW9 up): the low 16 bits"
VFD = rv(114, 200, lambda r: r.choice((1, -1)) * r.randint(4, 1020) / 4)
VFD = [v for v in VFD if abs(v) >= 1]
numq(W, "FPDECODE", "לפענח מספר נקודה צפה", 4, VFD, fpages, "the float in hex, high / low 16 bits",
     [(["בתצוגה מספר נקודה צפה של 32 ביטים, בהקס, בשני דפים:", LFP, "sign | biased exponent (8 bits) | fraction (23 bits)",
        "מה ביט הסימן?"] + UP0("1 (שלילי)", "0"), lambda q, v: (int(v < 0), 0x1)),
      (["מה המעריך המוטה (8 הביטים שאחרי הסימן)?"] + binl(8), lambda q, v: ((f32(v) >> 23) & 255, 0xFF)),
      (["מה המעריך האמיתי?", "exponent = biased - 127"] + binl(3), lambda q, v: (((f32(v) >> 23) & 255) - 127, 0x7)),
      (["מה החלק השלם של הערך המוחלט?", "|value| = 1.fraction x 2^exponent"] + binl(8), lambda q, v: (int(abs(v)), 0xFF))],
     lambda v: f"{v} = {f32(v):08X}", pages2=True)

LFE = "HEX2 HEX1 HEX0 = N (decimal)"
VFE = list(range(3, 256, 4))
numq(W, "FPENCODE", "לקודד מספר בנקודה צפה", 3, VFE, lambda n: [[n // 100, (n // 10) % 10, n % 10]], LFE,
     [(["בתצוגה מספר שלם:", LFE, "בנקודה צפה הוא", "1.f x 2^e", ". מה המעריך המוטה?", "biased = 127 + e"] + binl(8),
       lambda q, n: (127 + n.bit_length() - 1, 0xFF)),
      (["מה 8 הביטים הראשונים של השבר (אחרי ה-1 שלא נכתב)?", "SW7 = the first fraction bit"],
       lambda q, n: (((n - (1 << (n.bit_length() - 1))) << (8 - (n.bit_length() - 1))) & 255, 0xFF))],
     lambda n: f"{n} = {f32(n):08X}")

SPN = ["0", "-0", "infinity", "-infinity", "NaN", "a normal number"]
VSP = [(0, 0.0), (1, -0.0), (2, float("inf")), (3, float("-inf"))] + [(4, ("nan", m)) for m in (0x400000, 0x200001, 0x7FFFFF, 1, 0x123456)] + \
      [(5, v) for v in (1.0, -2.5, 228.0, -58.25, 0.375, 1e10, -3e-5)]
def spbits(p):
    if p[0] == 4:
        return 0x7F800000 | p[1][1]
    return f32(p[1])
W.append(Q(id="FPSPECIAL", name="FPSPECIAL", title="מקרים מיוחדים בנקודה צפה", inputs=[9], flat=True,
    outs=digs(4), hexes=[None, None, None, None], variants=VSP,
    tables=lambda p: show([[(spbits(p) >> s) & 15 for s in (28, 24, 20, 16)], [(spbits(p) >> s) & 15 for s in (12, 8, 4, 0)]]),
    answer=lambda p: (p[0], 0x7), describe=lambda p: f"{spbits(p):08X} = {SPN[p[0]]}",
    B=["the float in hex: high 16 bits / low 16 bits (SW9)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר נקודה צפה בהקס, בשני דפים:", LFP,
             "exponent all 0 and fraction 0: zero     exponent all 1: fraction 0 = infinity, else NaN",
             "מה הוא?"] + code(SPN, 3), lambda q, p: (p[0], 0x7))]))

VFA = [(a, b) for a in range(4, 64) for b in range(4, 64) if a != b and a % 2 == 0 and b % 2 == 1][::7]
def fexp(v):
    return math.floor(math.log2(v))
LFA = "page 1 (SW9 down): N1, the high 16 bits     page 2 (SW9 up): N2, the high 16 bits     (the low 16 bits are 0)"
numq(W, "FPADD", "חיבור בנקודה צפה", 4, VFA,
     lambda p: [[(f32(p[0] / 4) >> s) & 15 for s in (28, 24, 20, 16)], [(f32(p[1] / 4) >> s) & 15 for s in (28, 24, 20, 16)]],
     "N1 / N2 high 16 bits",
     [(["בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):", LFA,
        "החיבור: מוציאים מעריכים, מזיזים את הקטן ימינה בהפרש. בכמה מקומות מזיזים?"] + cnt(4, 0),
       lambda q, p: (abs(fexp(p[0] / 4) - fexp(p[1] / 4)), 0x7)),
      (["מה המעריך המוטה של הסכום (אחרי נרמול)?"] + binl(8), lambda q, p: (127 + fexp((p[0] + p[1]) / 4), 0xFF))],
     lambda p: f"{p[0] / 4} + {p[1] / 4} = {(p[0] + p[1]) / 4}", pages2=True)

# ---- new (topic 1): negate in Q4.4, saturating U4.4 addition, comparing floats, rounding modes
VQN = list(range(1, 128))
W.append(Q(id="QNEG", name="QNEG", title="מספר נגדי בנקודה קבועה", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=VQN,
    tables=lambda x: const(bitsof(x, 8)), answer=lambda x: ((-x) & 255, 0xFF),
    describe=lambda x: f"Q4.4 {x:08b} = {x / 16}, negated {(-x) & 255:08b}",
    B=["x = LEDG7..LEDG0 (Q4.4, positive)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בנורות מספר חיובי בפורמט", "Q4.4", "x = LEDG7..LEDG0",
             "מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.", "במשלים ל-2 מוצאים את הנגדי כך: הופכים את כל הביטים (0 ל-1 ו-1 ל-0), ואז מוסיפים 1.",
             "שלב 1 בהיפוך הסימן: הפכו את כל הביטים שלו.", "SW7..SW0 = not x"], lambda q, x: ((~x) & 255, 0xFF)),
           (["בנורות אותו מספר:", "x = LEDG7..LEDG0     (Q4.4)",
             "מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.",
             "שלב 2: הוסיפו 1 לביט הימני. כתבו את המספר הנגדי:", "SW7..SW0 = -x"], lambda q, x: ((-x) & 255, 0xFF))]))

LSU = "HEX3 HEX2 = A (hex)     HEX1 HEX0 = B (hex)     (U4.4)"
VSU = rv(117, 200, lambda r: (r.randrange(16, 256), r.randrange(16, 256)))
numq(W, "SATU44", "חיבור ברוויה בנקודה קבועה", 4, VSU, lambda p: [[p[0] >> 4, p[0] & 15, p[1] >> 4, p[1] & 15]], LSU,
     [(["בתצוגה שני מספרים בנקודה קבועה בלי סימן:", LSU, "האם החיבור שלהם גולש (לא נכנס ב-8 ביטים)?"] + UP0("גולש", "לא גולש"),
       lambda q, p: (int(p[0] + p[1] > 255), 0x1)),
      (["בתצוגה אותם שני מספרים:", LSU, "מה החיבור ברוויה? (בגלישה התוצאה היא הערך הגדול ביותר)",
        "SW7..SW0 = A + B (U4.4, saturated)"], lambda q, p: (min(255, p[0] + p[1]), 0xFF))],
     lambda p: f"{p[0] / 16} + {p[1] / 16}: saturated {min(255, p[0] + p[1]):08b}")

def fpc_gen(r):
    k1 = r.randint(4, 255)
    if r.random() < 0.35:
        e = k1.bit_length() - 1
        k2 = r.randint(1 << e, (2 << e) - 1)
    else:
        k2 = r.randint(4, 255)
    x, y = r.choice((1, -1)) * k1 / 4, r.choice((1, -1)) * k2 / 4
    return None if x == y else (x, y)
VFC = rv(118, 200, fpc_gen)
def fsgn(v):
    return int(v < 0)
def fcmp(p):
    e1, e2 = fexp(abs(p[0])), fexp(abs(p[1]))
    return 2 if e1 == e2 else int(e2 > e1)
numq(W, "FPCOMPARE", "השוואת מספרים בנקודה צפה", 4, VFC,
     lambda p: [[(f32(p[0]) >> s) & 15 for s in (28, 24, 20, 16)], [(f32(p[1]) >> s) & 15 for s in (28, 24, 20, 16)]],
     "N1 / N2 high 16 bits",
     [(["בתצוגה שני מספרים בנקודה צפה (רק 16 הביטים העליונים, השאר 0):", LFA, "מה הסימנים שלהם?"] +
       code(["N1+ N2+", "N1+ N2-", "N1- N2+", "N1- N2-"]), lambda q, p: (fsgn(p[0]) * 2 + fsgn(p[1]), 0x3)),
      (["בתצוגה אותם שני מספרים:", LFA, "למי יש מעריך מוטה גדול יותר?"] + code(["N1", "N2", "equal"]),
       lambda q, p: (fcmp(p), 0x3)),
      (["בתצוגה אותם שני מספרים:", LFA, "מי המספר הגדול יותר (עם הסימן)?"] + code(["N1", "N2"]),
       lambda q, p: (int(p[1] > p[0]), 0x1))],
     lambda p: f"N1 = {p[0]}  N2 = {p[1]}", pages2=True)

VFR = [f for f in range(64) if f >> 3 != 7 and (f & 7) not in (0, 4)]
LFR = "LEDG6 = the leading 1     LEDG5..LEDG0 = the 6 fraction bits"
W.append(Q(id="FPROUND", name="FPROUND", title="עיגול בנקודה צפה", inputs=[9], flat=True,
    outs=[("G", i) for i in range(7)], hexes=[None, None, None, None], variants=VFR,
    tables=lambda f: const(bitsof(64 | f, 7)), answer=lambda f: ((f >> 3) + int((f & 7) > 4), 0x7),
    describe=lambda f: f"1.{f:06b}: down {f >> 3:03b} up {(f >> 3) + 1:03b} nearest {(f >> 3) + int((f & 7) > 4):03b}",
    B=[LFR + "     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בנורות מנטיסה חיובית עם 6 ביטי שבר:", "1.f", LFR,
             "עגלו אותה ל-3 ביטי שבר כלפי מטה. מה 3 ביטי השבר?", "SW2..SW0"], lambda q, f: (f >> 3, 0x7)),
           (["בנורות אותה מנטיסה:", LFR, "עגלו אותה ל-3 ביטי שבר כלפי מעלה:", "SW2..SW0"], lambda q, f: ((f >> 3) + 1, 0x7)),
           (["בנורות אותה מנטיסה:", LFR, "עגלו אותה ל-3 ביטי שבר לקרוב ביותר:", "SW2..SW0"],
            lambda q, f: ((f >> 3) + int((f & 7) > 4), 0x7))]))

# ================================================================ topic 2: counters and shift registers
# No clock button: the next-state logic is combinational - the current value is on switches, and the board shows the
# value after the next clock edge (LEDs / HEX0).
LNX = "q after the next clock edge = LEDG3..LEDG0"
# a digitally controlled oscillator: add p each clock
LDC = "q = SW9..SW6 (HEX3)     " + LNX
W.append(Q(id="DCO", name="DCO", title="מתנד בשליטה ספרתית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9, 8, 7, 6], None, None, None], variants=list(range(1, 16)),
    tables=lambda p: [col(lambda s: (((s + p) & 15) >> i) & 1, 4) for i in range(4)],
    answer=lambda p: (16 // math.gcd(p, 16), 0x1F), describe=lambda p: f"adds {p}",
    B=[LDC + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח מונה של 4 ביטים שמוסיף מספר מוסתר בכל עליית שעון (במקום 1).", "במתגים הערך של המונה עכשיו, ובנורות הערך אחרי עליית השעון הבאה:",
             LDC, "מה המספר שהוא מוסיף?", "p = ?     SW3..SW0"], lambda q, p: (p, 0xF)),
           (["בלוח אותו מונה:", LDC, "הוא מתחיל ב-0. אחרי כמה עליות שעון הוא חוזר ל-0 בפעם הראשונה?"] + binl(5),
            lambda q, p: (16 // math.gcd(p, 16), 0x1F))]))

# which counter bit drives the LED (divide by 2^N)
LD2 = "q = SW9..SW6 (HEX3)     LEDG0 = one bit of q"
W.append(Q(id="DIVBY2N", name="DIVBY2N", title="מחלק ב-2 בחזקת N", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9, 8, 7, 6], None, None, None], variants=[0, 1, 2, 3],
    tables=lambda k: [col(lambda s: (s >> k) & 1, 4)],
    answer=lambda k: (2 << k, 0x1F), describe=lambda k: f"LED = q[{k}]",
    B=[LD2 + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח מונה בינארי, והנורה מחוברת לאחד הביטים שלו.", LD2,
             "שימו במתגים את ערכי המונה לפי הסדר: 0, 1, 2, 3, ... כל כמה ספירות הנורה משתנה?",
             "1 = SW0     2 = SW1     4 = SW2     8 = SW3"], lambda q, k: (1 << k, 0xF)),
           (["בלוח אותו מונה:", LD2, "לאיזה ביט של המונה הנורה מחוברת?", "q[k]:   k = ?"] + cnt(3, 0), lambda q, k: (k, 0x3)),
           (["בלוח אותו מונה:", LD2, "המונה סופר 1 בכל עליית שעון. כמה עליות שעון נמשך מחזור שלם של הנורה (דולקת וכבויה)?"] + binl(5),
            lambda q, k: (2 << k, 0x1F))]))

# a counter with a hidden reset value, up or down
VRC = [(r_, d) for r_ in range(16) for d in range(2)]
LRC = "reset = SW9     q = SW8..SW5 (HEX3)     q after the next clock edge = HEX0"
RCODE = "always_ff @(posedge clk) if (reset) q <= R; else q <= q +- 1;"
def rc_next(p, r):
    return p[0] if r >> 4 else ((r & 15) + (15 if p[1] else 1)) & 15
W.append(Q(id="RESETCNT", name="RESETCNT", title="מונה עם ערך איפוס", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=hexd(0), hexes=[[8, 7, 6, 5], None, None, None], variants=VRC,
    tables=lambda p: [col(lambda r: (rc_next(p, r) >> b) & 1, 5) for b in range(4)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"reset to {p[0]}, counts {'down' if p[1] else 'up'}",
    B=[LRC + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מונה:", RCODE, "במתגים הכניסות עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:", LRC,
             "מה ערך האיפוס?", "R = ?     SW3..SW0"], lambda q, p: (p[0], 0xF)),
           (["בלוח אותו מונה:", RCODE, LRC, "הוא סופר למעלה או למטה?"] + code(["up", "down"]), lambda q, p: (p[1], 0x1))]))

# a shift register: where the new bit enters, inverted or not
VSH = [(d, inv) for d in range(2) for inv in range(2)]
def sh_next(p, s, a):
    a ^= p[1]
    return ((s << 1) | a) & 15 if p[0] == 0 else (s >> 1) | (a << 3)
LSD = "Q = SW9..SW6 (HEX3)     Sin = SW5 (HEX2)     " + LNX
W.append(Q(id="SHIFTDIR", name="SHIFTDIR", title="אוגר הזזה", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9, 8, 7, 6], [5], None, None], variants=VSH,
    tables=lambda p: [col(lambda r: (sh_next(p, r >> 1, r & 1) >> i) & 1, 5) for i in range(4)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"enters at LEDG{0 if p[0] == 0 else 3}, {'inverted' if p[1] else 'as is'}",
    B=[LSD + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר הזזה של 4 ביטים עם כניסה טורית. במתגים הערך עכשיו והכניסה, ובנורות הערך אחרי עליית השעון הבאה:",
             LSD, "באיזו נורה נכנס הביט החדש?"] + code(["LEDG0", "LEDG3"]), lambda q, p: (p[0], 0x1)),
           (["בלוח אותו אוגר:", LSD, "הביט נכנס כמו שהוא, או הפוך?"] + code(["as is", "inverted"]), lambda q, p: (p[1], 0x1))]))

# a shift register with parallel load (slide 31)
VPL = [(ls, dr, d) for ls in range(2) for dr in range(2) for d in range(16)]
def pl_next(p, r):				# r = Q3..Q0 (SW9..SW6), x = SW5, y = SW4
    ls, dr, d = p
    s, x, y = r >> 2, (r >> 1) & 1, r & 1
    load, sin = (x, y) if ls == 0 else (y, x)
    if load:
        return d
    return ((s << 1) | sin) & 15 if dr == 0 else (s >> 1) | (sin << 3)
LPL = ["D = HEX0     Q = SW9..SW6 (HEX3)     Load, Sin = SW5, SW4 (in some order)", LNX]
W.append(Q(id="PARLOAD", name="PARLOAD", title="אוגר הזזה עם טעינה מקבילית", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + hexd(0), hexes=[[9, 8, 7, 6], None, None, None], variants=VPL,
    tables=lambda p: [col(lambda r: (pl_next(p, r) >> i) & 1, 6) for i in range(4)] + const(bitsof(p[2], 4), 6),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"D {p[2]:X}, Load = SW{5 - p[0]}, shifts {'left' if p[1] == 0 else 'right'}",
    B=["     ".join(LPL) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר הזזה עם טעינה מקבילית: כש-", "Load = 1", "הוא טוען את הכניסה המקבילית, ואחרת הוא מזיז ומכניס את הביט הטורי.",
             "Load = 1: Q <= D     Load = 0: shift in Sin", "במתגים הערך עכשיו והכניסות, ובנורות הערך אחרי עליית השעון הבאה:"] + LPL +
            ["איזה מתג הוא", "Load", "?"] + code(["SW5", "SW4"]), lambda q, p: (p[0], 0x1)),
           (["בלוח אותו אוגר:"] + LPL + ["לאיזה כיוון הוא מזיז?"] + code(["left (into LEDG0)", "right (into LEDG3)"]),
            lambda q, p: (p[1], 0x1))]))

# ---- new (topic 2): a counter with a hidden modulus, a shift register as a delay, parallel-to-serial
LMC = "q = SW9..SW6 (HEX3)     q after the next clock edge = HEX0"
W.append(Q(id="MODCNT", name="MODCNT", title="מונה עם מחזור מוסתר", inputs=[9, 8, 7, 6], flat=True,
    outs=hexd(0), hexes=[[9, 8, 7, 6], None, None, None], variants=list(range(3, 17)),
    tables=lambda m: [col(lambda s: ((0 if s == m - 1 else s + 1) & 15) >> b & 1, 4) for b in range(4)],
    answer=lambda m: (m, 0x1F), describe=lambda m: f"counts 0..{m - 1}",
    B=[LMC + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח מונה שחוזר ל-0 אחרי ערך מוסתר. במתגים הערך עכשיו, ובתצוגה הערך אחרי עליית השעון הבאה:", LMC,
             "התחילו ב-0 ועקבו אחרי המונה. מה הערך הגדול ביותר שהוא מגיע אליו?", "SW3..SW0"], lambda q, m: (m - 1, 0xF)),
           (["בלוח אותו מונה:", LMC, "כמה ערכים שונים יש במחזור שלו?"] + binl(5), lambda q, m: (m, 0x1F))]))

SDN = ["Sin", "Q[0]", "Q[1]", "Q[2]"]
LSY = ["Sin = SW9     Q[0] Q[1] Q[2] = SW8 SW7 SW6 (now)", "LEDG0 = one output, after the next clock edge"]
W.append(Q(id="SHIFTDELAY", name="SHIFTDELAY", title="אוגר הזזה כקו השהיה", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, None], variants=[0, 1, 2, 3],
    tables=lambda k: [col(lambda r: (r >> (3 - k)) & 1, 4)],
    answer=lambda k: (k + 1, 0x7), describe=lambda k: f"LEDG0 = Q[{k}]",
    B=["     ".join(LSY) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר הזזה של 4 ביטים. בכל עליית שעון הכניסה הטורית נכנסת לביט הראשון והשאר זזים הלאה.",
             "Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]", "הנורה מחוברת לאחת היציאות, ומראה אותה אחרי עליית השעון הבאה."] + LSY +
            ["את איזה ערך הנורה מעתיקה?"] + code(SDN), lambda q, k: (k, 0x3)),
           (["בלוח אותו אוגר:", "Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]"] + LSY +
            ["לאיזו יציאה מחוברת הנורה?", "Q[k]:   k = ?"] + cnt(3, 0), lambda q, k: (k, 0x3)),
           (["בלוח אותו אוגר:", "Sin -> Q[0] -> Q[1] -> Q[2] -> Q[3]", "LEDG0 = Q[k]",
             "ביט חדש נכנס ב-", "Sin", ". אחרי כמה עליות שעון הוא מגיע לנורה?"] + cnt(4), lambda q, k: (k + 1, 0x7))]))

VPS = [(w, d) for w in range(1, 16) for d in range(2)]
def rev4(w):
    return int(f"{w:04b}"[::-1], 2)
def ps_next(p, r):				# r = Load (SW9), Q3..Q0 (SW8..SW5)
    w, d = p
    s = r & 15
    if r >> 4:
        return w
    return (s << 1) & 15 if d == 0 else s >> 1
LPS = ["Load = SW9     Q = SW8..SW5 (HEX3)", LNX, "Load = 1: Q <= W (hidden)     Load = 0: shift (0 enters)"]
W.append(Q(id="PAR2SER", name="PAR2SER", title="ממקבילי לטורי", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[8, 7, 6, 5], None, None, None], variants=VPS,
    tables=lambda p: [col(lambda r: (ps_next(p, r) >> i) & 1, 5) for i in range(4)],
    answer=lambda p: (p[0] if p[1] == 0 else rev4(p[0]), 0xF), describe=lambda p: f"loads {p[0]:04b}, shifts {'left' if p[1] == 0 else 'right'}",
    B=["     ".join(LPS) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח ממיר ממקבילי לטורי: אוגר הזזה שטוען מילה מוסתרת ומוציא אותה ביט אחרי ביט.",
             "במתגים הכניסות עכשיו, ובנורות הערך אחרי עליית השעון הבאה:"] + LPS + ["מה המילה שנטענת?", "SW3..SW0 = W"],
            lambda q, p: (p[0], 0xF)),
           (["בלוח אותו אוגר:"] + LPS + ["לאיזה כיוון הוא מזיז?"] + code(["left: Sout = Q3", "right: Sout = Q0"]),
            lambda q, p: (p[1], 0x1)),
           (["בלוח אותו אוגר:"] + LPS + ["טוענים את המילה, ואחר כך היא יוצאת ביט אחרי ביט. מה סדר היציאה?",
             "SW3 = the first bit out   ...   SW0 = the last bit out"], lambda q, p: (p[0] if p[1] == 0 else rev4(p[0]), 0xF))]))

# ================================================================ topic 3: memories
LMA = "HEX3 = N address bits     HEX2 = M data bits"
numq(W, "MEMARRAY", "גודל מערך זיכרון", 2, [(n, m) for n in range(1, 6) for m in range(1, 9)], lambda p: [[p[0], p[1]]], LMA,
     [(["בתצוגה מערך זיכרון:", LMA, "כמה מילים יש בו?", "2^N"] + binl(6), lambda q, p: (1 << p[0], 0x3F)),
      (["כמה ביטים בסך הכול?", "M x 2^N"] + binl(9), lambda q, p: (p[1] << p[0], 0x1FF))],
     lambda p: f"{1 << p[0]} words x {p[1]} bits")

LMS = "HEX2 HEX1 HEX0 = the number of words"
numq(W, "ADDRBITS", "כמה ביטי כתובת?", 3, [4, 8, 16, 32, 64, 128, 256, 512], lambda w: [[w // 100, (w // 10) % 10, w % 10]], LMS,
     [(["בתצוגה מספר המילים בזיכרון:", LMS, "logic [31:0] mem [words-1:0];", "כמה ביטי כתובת צריך?"] + cnt(9),
       lambda q, w: (int(math.log2(w)), 0xF))],
     lambda w: f"{w} words: {int(math.log2(w))} address bits")

VRR = rv(115, 200, lambda r: tuple(r.randrange(8) for _ in range(4)))
W.append(Q(id="ROMREAD", name="ROMREAD", title="לקרוא זיכרון לקריאה בלבד", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(3)], hexes=[[9, 8], None, None, None], variants=VRR,
    tables=lambda p: [col(lambda a: (p[a] >> k) & 1, 2) for k in range(3)], answer=lambda p: (p[3], 0x7),
    describe=lambda p: " ".join(f"{a:02b}:{p[a]:03b}" for a in range(4)),
    B=["address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0     answer: SW2..SW0"], L=[], F=[],
    steps=[([("בלוח זיכרון לקריאה בלבד של 4 מילים של 3 ביטים. מה כתוב בכתובת:" if a == 0 else "ובכתובת:"), f"address = {a:02b}",
             "SW2..SW0 = LEDG2..LEDG0"], (lambda a: lambda q, p: (p[a], 0x7))(a)) for a in range(4)]))

VRL = list(itertools.permutations(range(3)))
RLF = [lambda a: (a >> 1) ^ (a & 1), lambda a: (a >> 1) | (a & 1), lambda a: (a >> 1) & a & 1]
W.append(Q(id="ROMLOGIC", name="ROMLOGIC", title="לוגיקה בזיכרון", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(3)], hexes=[[9], [8], None, None], variants=VRL,
    tables=lambda p: [col(RLF[p[k]], 2) for k in range(3)], answer=lambda p: (p.index(1), 0x3),
    describe=lambda p: " ".join(f"Data{k}={['XOR', 'OR', 'AND'][p[k]]}" for k in range(3)),
    B=["A1 = SW9     A0 = SW8     Data2..0 = LEDG2..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח זיכרון של 4 מילים של 3 ביטים שמממש שלוש פונקציות של הכתובת (כמו בשקופית):",
             "A1 = SW9     A0 = SW8     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0", "איזה ביט נתונים הוא", "A1 xor A0", "?"] +
            code(["Data0", "Data1", "Data2"]), lambda q, p: (p.index(0), 0x3)),
           (["איזה ביט הוא", "A1 + A0", "(OR)?"] + code(["Data0", "Data1", "Data2"]), lambda q, p: (p.index(1), 0x3))]))

VLU = rv(116, 200, lambda r: r.randrange(1, 255))
LLU = "address = SW9 SW8 SW7     out = LEDG0"
W.append(Q(id="LUT", name="LUT", title="טבלת חיפוש", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VLU,
    tables=lambda m: [col(lambda a: (m >> a) & 1, 3)], answer=lambda m: (m >> 4, 0xF), describe=lambda m: f"LUT {m:08b}",
    B=[LLU + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח טבלת חיפוש", "(LUT)", "של 3 כניסות: זיכרון של 8 ביטים, והכניסות הן הכתובת.", LLU,
             "כתבו את התוכן בכתובות 3 עד 0: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:", "address 3 -> SW3   ...   address 0 -> SW0"],
            lambda q, m: (m & 15, 0xF)),
           (["בלוח אותה טבלה:", LLU, "עכשיו התוכן בכתובות 7 עד 4: לכל כתובת שבה הנורה דולקת הרימו את המתג שלה:",
             "address 7 -> SW3   ...   address 4 -> SW0"], lambda q, m: (m >> 4, 0xF)),
           (["כמה ביטים צריך לטבלת חיפוש של 4 כניסות?", "2^4"] + binl(5), lambda q, m: (16, 0x1F))]))

# a small RAM: 2 words of 2 bits; the read is immediate, the board also shows the word after the write edge
VRA = [(init, we) for init in range(16) for we in range(2)]
ORA = [("G", 1), ("G", 0), ("G", 3), ("G", 2)]
def ram_out(p, r):				# r = a (SW9), wd (SW8 SW7), we (SW6) -> (rd now, the word at a after the edge)
    init, wl = p
    a, wd, we = r >> 3, (r >> 1) & 3, r & 1
    word = (init >> (2 * a)) & 3
    return word, (wd if we == wl else word)
LRA = ["a = SW9     rd = LEDG1 LEDG0 (the word at a, now)"]
LRW = ["a = SW9     wd = SW8 SW7     we = SW6", "LEDG3 LEDG2 = the word at a after the next clock edge"]
W.append(Q(id="RAM", name="RAM", title="זיכרון לקריאה וכתיבה", inputs=[9, 8, 7, 6], flat=True,
    outs=ORA, hexes=[[9], [8, 7], [6], None], variants=VRA,
    tables=lambda p: [col(lambda r: (ram_out(p, r)[0] >> 1) & 1, 4), col(lambda r: ram_out(p, r)[0] & 1, 4),
                      col(lambda r: (ram_out(p, r)[1] >> 1) & 1, 4), col(lambda r: ram_out(p, r)[1] & 1, 4)],
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"word0 {p[0] & 3:02b} word1 {p[0] >> 2:02b}, we active {'high' if p[1] else 'low'}",
    B=["     ".join(LRA + LRW) + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח זיכרון של 2 מילים של 2 ביטים. הקריאה מיידית, והכתיבה קורית בעליית השעון."] + LRA +
            ["מה כתוב עכשיו במילה 0?", "a = 0:   SW1 SW0 = rd"], lambda q, p: (p[0] & 3, 0x3)),
           (["בלוח אותו זיכרון:"] + LRA + ["מה כתוב עכשיו במילה 1?", "a = 1:   SW1 SW0 = rd"], lambda q, p: (p[0] >> 2, 0x3)),
           (["בלוח אותו זיכרון. הנורות העליונות מראות את המילה אחרי עליית השעון הבאה:"] + LRW +
            ["הכתיבה קורית כש-", "we", "?"] + UP0("למעלה", "למטה"), lambda q, p: (p[1], 0x1))]))

# a register file with a hardwired register
VRF = [(z, c) for z in range(4) for c in range(16) if not c >> z & 1] + [(4, c) for c in range(16)]
def rf_next(p, r):				# r = A3 (SW9 SW8), WD3 (SW7), WE3 (SW6), A1 (SW5 SW4)
    z, s = p
    a3, wd, we = r >> 4, (r >> 3) & 1, (r >> 2) & 1
    if we and a3 != z:
        s = (s & ~(1 << a3)) | (wd << a3)
    return s
LRR = "read: A1 = SW5 SW4 (HEX1)     RD1 = LEDG0 (now)"
LRF = ["write: A3 = SW9 SW8 (HEX3)     WD3 = SW7     WE3 = SW6", "LEDG7..LEDG4 = R3..R0 after the next clock edge"]
W.append(Q(id="REGFILE", name="REGFILE", title="קובץ אוגרים", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", 0)] + [("G", 4 + i) for i in range(4)], hexes=[[9, 8], None, [5, 4], None], variants=VRF,
    tables=lambda p: [col(lambda r: (p[1] >> (r & 3)) & 1, 6)] + [col(lambda r: (rf_next(p, r) >> i) & 1, 6) for i in range(4)],
    answer=lambda p: (p[0], 0x7),
    describe=lambda p: (f"register {p[0]} hardwired to 0" if p[0] < 4 else "no hardwired register") + f", now R3..R0 = {p[1]:04b}",
    B=["     ".join([LRR] + LRF) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח קובץ אוגרים של 4 אוגרים של ביט אחד: פורט קריאה ופורט כתיבה.", LRR,
             "מה כתוב עכשיו בארבעת האוגרים? קראו את כולם.", "SW3..SW0 = R3..R0"], lambda q, p: (p[1], 0xF)),
           (["בלוח אותו קובץ אוגרים. הנורות העליונות מראות את האוגרים אחרי עליית השעון הבאה:"] + LRF +
            ["כתבו 1 לכל אחד מארבעת האוגרים. אולי אחד מחובר תמיד ל-0. איזה?"] +
            code(["R0", "R1", "R2", "R3", "none"], 3), lambda q, p: (p[0], 0x7))]))

# ---- new (topic 3): a broken wordline decoder, ROM dots, a ROM from a memfile, a leaking DRAM cell
VWL = [(a, j) for a in range(8) for j in [None] + [j for j in range(8) if j != a]]
def wl(p, r):
    a, j = p
    if r != a:
        return 1 << r
    return 0 if j is None else (1 << r) | (1 << j)
W.append(Q(id="WORDLINE", name="WORDLINE", title="קווי מילה", inputs=[9, 8, 7], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[[9, 8, 7], None, None, None], variants=VWL,
    tables=lambda p: [col(lambda r: (wl(p, r) >> i) & 1, 3) for i in range(8)], answer=lambda p: (p[0], 0x7),
    describe=lambda p: f"address {p[0]}: " + ("no wordline" if p[1] is None else f"wordlines {p[0]} and {p[1]}"),
    B=["address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח מפענח הכתובות של זיכרון של 8 מילים: כל כתובת צריכה להעלות בדיוק קו מילה אחד.",
             "address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi",
             "המפענח שבור בכתובת אחת. עברו על כל הכתובות: מה התקלה?"] +
            code(["no wordline HIGH", "two wordlines HIGH"]), lambda q, p: (int(p[1] is not None), 0x1)),
           (["בלוח אותו מפענח:", "address = SW9 SW8 SW7 (HEX3)     wordline i = LEDGi", "באיזו כתובת התקלה?"] + binl(3),
            lambda q, p: (p[0], 0x7))]))

VRD = rv(119, 200, lambda r: tuple(r.randrange(16) for _ in range(4)))
def pop(x):
    return bin(x).count("1")
LRD = "address = SW9 SW8 (HEX3)     data = LEDG3..LEDG0"
W.append(Q(id="ROMDOTS", name="ROMDOTS", title="סימון נקודות בזיכרון", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9, 8], None, None, None], variants=VRD,
    tables=lambda p: [col(lambda a: (p[a] >> k) & 1, 2) for k in range(4)], answer=lambda p: (sum(map(pop, p)), 0x1F),
    describe=lambda p: " ".join(f"{a:02b}:{p[a]:04b}" for a in range(4)),
    B=[LRD + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח זיכרון לקריאה בלבד של 4 מילים של 4 ביטים. בסימון נקודות, נקודה היא ביט 1.", LRD,
             "כמה נקודות יש בשורה של כתובת 00?"] + cnt(4, 0), lambda q, p: (pop(p[0]), 0x7)),
           (["בלוח אותו זיכרון:", LRD, "כמה נקודות יש בעמודה של", "Data0 = LEDG0", "(בכל 4 הכתובות)?"] + cnt(4, 0),
            lambda q, p: (sum(x & 1 for x in p), 0x7)),
           (["בלוח אותו זיכרון:", LRD, "כמה נקודות יש בכל הזיכרון?"] + binl(5), lambda q, p: (sum(map(pop, p)), 0x1F))]))

VMF = rv(120, 200, lambda r: tuple(r.sample(range(16), 16)))
LMF = "address = SW9..SW6 (HEX3)     data = HEX0"
W.append(Q(id="MEMFILE", name="MEMFILE", title="זיכרון מקובץ", inputs=[9, 8, 7, 6], flat=True,
    outs=hexd(0), hexes=[[9, 8, 7, 6], None, None, None], variants=VMF,
    tables=lambda p: [col(lambda a: (p[a] >> b) & 1, 4) for b in range(4)], answer=lambda p: (p.index(15), 0xF),
    describe=lambda p: "memfile " + "".join(f"{x:X}" for x in p),
    B=[LMF + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח זיכרון לקריאה בלבד של 16 מילים של 4 ביטים, שאותחל מקובץ:",
             "logic [3:0] ROM[15:0];     initial $readmemh(\"memfile.dat\", ROM);", LMF,
             "מה כתוב בשורה הראשונה של הקובץ (כתובת 0)?", "SW3..SW0"], lambda q, p: (p[0], 0xF)),
           (["בלוח אותו זיכרון:", LMF, "מה כתוב בשורה האחרונה של הקובץ (השורה ה-16)?", "SW3..SW0"], lambda q, p: (p[15], 0xF)),
           (["בלוח אותו זיכרון:", LMF, "כל ערך מופיע בקובץ פעם אחת. באיזו כתובת כתוב", "F", "?", "SW3..SW0 = the address"],
            lambda q, p: (p.index(15), 0xF))]))

LDL = ["the bit written = SW9     clock edges since the write = SW8..SW6 (HEX3)", "the bit read = LEDG0"]
W.append(Q(id="DRAMLEAK", name="DRAMLEAK", title="תא זיכרון דינמי", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[8, 7, 6], None, None, None], variants=list(range(2, 8)),
    tables=lambda L: [col(lambda r: (r >> 3) & int((r & 7) < L), 4)],
    answer=lambda L: (L - 1, 0x7), describe=lambda L: f"the charge leaks after {L} clocks",
    B=["     ".join(LDL) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח תא זיכרון דינמי: הביט נשמר בקבל, והמטען דולף אחרי כמה עליות שעון בלי כתיבה.",
             "במתגים הביט שנכתב, וכמה עליות שעון עברו מאז הכתיבה. בנורה מה שנקרא עכשיו:"] + LDL +
            ["כתבו 1. אחרי כמה עליות שעון הביט נעלם?"] + cnt(7), lambda q, L: (L, 0x7)),
           (["בלוח אותו תא:"] + LDL + ["כדי לא לאבד את הביט צריך לרענן אותו (לכתוב שוב).",
             "אחרי כמה עליות שעון בלי כתיבה, לכל היותר, צריך לרענן?"] + cnt(7), lambda q, L: (L - 1, 0x7))]))

# ================================================================ easy questions straight from the slides (the slide's
# circuit / example is on the board; the per-student data - a format, a number, an address, inputs - only on the board)
# ---- topic 1
VSF = [3, 5, 6]					# a of Ua.b (6.75 needs 3 integer and 2 fraction bits; U4.4 is printed)
W.append(Q(id="SLIDEFMT", name="SLIDEFMT", title="6.75 בפורמט אחר", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=VSF,
    tables=lambda a: const(bitsof(a, 4) + bitsof(8 - a, 4)), answer=lambda a: (int(6.75 * (1 << (8 - a))), 0xFF),
    describe=lambda a: f"6.75 in U{a}.{8 - a} = {int(6.75 * (1 << (8 - a))):08b}",
    B=["a = HEX1     b = HEX0 (the format Ua.b)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בשקופית 5 המספר 6.75 בפורמט", "U4.4 = 0110.1100 = 01101100", "בתצוגה פורמט אחר:",
             "Ua.b:   a = HEX1 integer bits     b = HEX0 fraction bits", "כתבו את 6.75 בפורמט הזה:", "SW7..SW0"],
            lambda q, a: (int(6.75 * (1 << (8 - a))), 0xFF))]))

VSS = [b for b in rv(121, 60, lambda r: r.randrange(1, 256)) if b != 0x78]
LSS = "A = 11000000 (12)     B = LEDG7..LEDG0"
W.append(Q(id="SLIDESAT", name="SLIDESAT", title="המחבר ברוויה מהשקופית", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=VSS,
    tables=lambda b: const(bitsof(b, 8)), answer=lambda b: (min(255, 192 + b), 0xFF),
    describe=lambda b: f"11000000 + {b:08b}: saturated {min(255, 192 + b):08b}",
    B=[LSS + "     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בשקופית 7 חיבור ברוויה בפורמט", "U4.4", ":", "11000000 + 01111000 = 11111111     (12 + 7.5 = 15.9375)",
             "בלוח אותו חיבור, עם אותו מספר ראשון ומספר שני אחר:", LSS, "האם החיבור גולש (לא נכנס ב-8 ביטים)?"] +
            UP0("גולש", "לא גולש"), lambda q, b: (int(192 + b > 255), 0x1)),
           (["בלוח אותו חיבור:", LSS, "מה התוצאה ברוויה? (בגלישה התוצאה היא הערך הגדול ביותר)", "SW7..SW0 = A + B (saturated)"],
            lambda q, b: (min(255, 192 + b), 0xFF))]))

SFV = [228.0, -58.25, 1.5, 3.25, 4.75]
LFH = "HEX3..HEX0 = the high 16 bits (hex)     the low 16 bits are 0"
numq(W, "SLIDEFP", "מספרי נקודה צפה מהשקופיות", 4, list(range(5)),
     lambda k: [[(f32(SFV[k]) >> s) & 15 for s in (28, 24, 20, 16)]], LFH,
     [(["בתצוגה אחד המספרים מהשקופיות 14, 15 ו-21 עד 24, בנקודה צפה:", LFH, "sign | biased exponent (8 bits) | fraction (23 bits)",
        "מה ביט הסימן?"] + UP0("1 (שלילי)", "0"), lambda q, k: (int(SFV[k] < 0), 0x1)),
      (["בתצוגה אותו מספר:", LFH, "sign | biased exponent (8 bits) | fraction (23 bits)", "מה המעריך המוטה?"] + binl(8),
       lambda q, k: ((f32(SFV[k]) >> 23) & 255, 0xFF)),
      (["בתצוגה אותו מספר:", LFH, "איזה מספר מהשקופיות הוא?"] + code(["228", "-58.25", "1.5", "3.25", "4.75"], 3),
       lambda q, k: (k, 0x7))],
     lambda k: f"{SFV[k]} = {f32(SFV[k]):08X}")

# ---- topic 2 (the next state on LEDs, the current one on switches)
def cnt_next(r):				# r = reset (SW9), q (SW8..SW6)
    return 0 if r >> 3 else ((r & 7) + 1) & 7
LSC = ["reset = SW9     q = SW8..SW6 (HEX3)", "q after the next clock edge = LEDG2..LEDG0"]
W.append(Q(id="SLIDECNT", name="SLIDECNT", title="המונה מהשקופית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(3)] + hexd(0), hexes=[[8, 7, 6], None, None, None], variants=list(range(8)),
    tables=lambda v: [col(lambda r: (cnt_next(r) >> i) & 1, 4) for i in range(3)] + const(bitsof(v, 4), 4),
    answer=lambda v: ((v + 2) & 7, 0x7), describe=lambda v: f"q = {v:03b}: next {(v + 1) & 7:03b}, then {(v + 2) & 7:03b}",
    B=["     ".join(LSC) + "     the q to set = HEX0     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בשקופית 27 המונה:", "if (reset) q <= 0; else q <= q + 1;",
             "בלוח המונה הזה, של 3 ביטים. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:"] + LSC +
            ["שימו במתגים:", "reset = 0     q = HEX0", "מה הערך אחרי עליית השעון הבאה?", "SW2..SW0"], lambda q, v: ((v + 1) & 7, 0x7)),
           (["בלוח אותו מונה:"] + LSC + ["מתחילים מ:", "reset = 0     q = HEX0", "מה הערך אחרי שתי עליות שעון?", "SW2..SW0"],
            lambda q, v: ((v + 2) & 7, 0x7))]))

LSO = ["q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0", "p = HEX0"]
W.append(Q(id="SLIDEDCO", name="SLIDEDCO", title="המתנד מהשקופית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(1) + hexd(0), hexes=[[9, 8, 7, 6], None, None, None],
    variants=[(p, v) for p in range(1, 16) for v in range(16)],
    tables=lambda pv: [col(lambda s: (((s + pv[0]) & 15) >> i) & 1, 4) for i in range(4)] + const(bitsof(pv[1], 4) + bitsof(pv[0], 4), 4),
    answer=lambda pv: ((pv[1] + 2 * pv[0]) & 15, 0xF),
    describe=lambda pv: f"p = {pv[0]}, from q = {pv[1]}: {(pv[1] + pv[0]) & 15}, {(pv[1] + 2 * pv[0]) & 15}",
    B=["     ".join(LSO) + "     the q to set = HEX1     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקופית 29 מתנד בשליטה ספרתית: מונה שמוסיף בכל עליית שעון את", "p", "במקום 1.", "q <= q + p",
             "בלוח מונה כזה, של 4 ביטים. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:"] + LSO +
            ["שימו במתגים:", "q = HEX1", "מה הערך אחרי עליית השעון הבאה?", "SW3..SW0"], lambda q, pv: ((pv[1] + pv[0]) & 15, 0xF)),
           (["בלוח אותו מונה:"] + LSO + ["מתחילים מ:", "q = HEX1", "מה הערך אחרי שתי עליות שעון?", "SW3..SW0"],
            lambda q, pv: ((pv[1] + 2 * pv[0]) & 15, 0xF))]))

VSL = rv(122, 64, lambda r: (r.randrange(16), r.randrange(16), r.randrange(2)))	# (the Q to set, D, the Sin to set)
def spl_next(d, r):				# r = Load (SW9), Sin (SW8), Q3..Q0 (SW7..SW4)
    return d if r >> 5 else (((r & 15) << 1) | ((r >> 4) & 1)) & 15
LSP = ["Load = SW9     Sin = SW8     Q3..Q0 = SW7..SW4 (HEX3)", LNX]
SPC = "Load = 1: Q <= D     Load = 0: Q <= {Q[2:0], Sin}"
W.append(Q(id="SLIDEPL", name="SLIDEPL", title="אוגר הזזה עם טעינה מהשקופית", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + hexd(1) + hexd(0) + [("R", 0)], hexes=[[7, 6, 5, 4], None, None, None], variants=VSL,
    tables=lambda p: [col(lambda r: (spl_next(p[1], r) >> i) & 1, 6) for i in range(4)] +
                     const(bitsof(p[0], 4) + bitsof(p[1], 4) + [p[2]], 6),
    answer=lambda p: (((p[0] << 1) | p[2]) & 15, 0xF),
    describe=lambda p: f"D = {p[1]:04b}; Q = {p[0]:04b}, Sin = {p[2]}: shift -> {((p[0] << 1) | p[2]) & 15:04b}",
    B=["     ".join(LSP) + "     D = HEX0     the Q to set = HEX1     the Sin to set = LEDR0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקופיות 31-32 אוגר הזזה עם טעינה מקבילית:", SPC,
             "בלוח האוגר הזה, של 4 ביטים. במתגים הכניסות והערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:"] + LSP +
            ["D = HEX0", "שימו במתגים:", "Load = 1", "מה הערך אחרי עליית השעון הבאה?", "SW3..SW0"], lambda q, p: (p[1], 0xF)),
           (["בלוח אותו אוגר:", SPC] + LSP + ["שימו במתגים:", "Load = 0     Sin = LEDR0     Q = HEX1",
             "מה הערך אחרי עליית השעון הבאה?", "SW3..SW0"], lambda q, p: (((p[0] << 1) | p[2]) & 15, 0xF))]))

# ---- topic 3
PAIRS = [(a, b) for a in range(4) for b in range(4) if a != b]
ARR36 = [0b011, 0b110, 0b100, 0b010]			# slide 36 (and the dots of slide 51)
LAR = "address = SW9 SW8 (HEX3)     data = LEDG2..LEDG0"
W.append(Q(id="SLIDEARR", name="SLIDEARR", title="מערך הזיכרון מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(3)] + hexd(1) + hexd(0), hexes=[[9, 8], None, None, None], variants=PAIRS,
    tables=lambda p: [col(lambda a: (ARR36[a] >> k) & 1, 2) for k in range(3)] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 2),
    answer=lambda p: (ARR36[p[1]], 0x7),
    describe=lambda p: f"address {p[0]:02b}: {ARR36[p[0]]:03b}, address {p[1]:02b}: {ARR36[p[1]]:03b}",
    B=[LAR + "     the addresses to read = HEX1, HEX0     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בשקופית 36 מערך זיכרון של 4 מילים של 3 ביטים. בלוח המערך הזה:", LAR,
             "מה המילה בכתובת שבתצוגה?", "address = HEX1", "SW2..SW0"], lambda q, p: (ARR36[p[0]], 0x7)),
           (["בלוח אותו מערך:", LAR, "ומה המילה בכתובת:", "address = HEX0", "SW2..SW0"], lambda q, p: (ARR36[p[1]], 0x7))]))

R54 = [((a >> 1) ^ (a & 1)) << 2 | ((a >> 1) | (a & 1)) << 1 | ((a >> 1) & a & 1) for a in range(4)]
L54 = "A1 A0 = SW9 SW8 (HEX3)     Data2 Data1 Data0 = LEDG2 LEDG1 LEDG0"
W.append(Q(id="SLIDEROM54", name="SLIDEROM54", title="הזיכרון מהשקופית: שלוש פונקציות", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(3)] + hexd(1) + hexd(0), hexes=[[9, 8], None, None, None], variants=PAIRS,
    tables=lambda p: [col(lambda a: (R54[a] >> k) & 1, 2) for k in range(3)] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 2),
    answer=lambda p: (R54[p[1]], 0x7),
    describe=lambda p: f"address {p[0]:02b}: {R54[p[0]]:03b}, address {p[1]:02b}: {R54[p[1]]:03b}",
    B=[L54 + "     the addresses to read = HEX1, HEX0     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בשקופית 54 זיכרון של 4 מילים של 3 ביטים שמממש שלוש פונקציות של הכתובת:",
             "Data2 = A1 xor A0     Data1 = A1 + A0     Data0 = A1 A0", "בלוח הזיכרון הזה:", L54,
             "מה המילה בכתובת שבתצוגה?", "A1 A0 = HEX1", "SW2..SW0"], lambda q, p: (R54[p[0]], 0x7)),
           (["בלוח אותו זיכרון:", L54, "ומה המילה בכתובת:", "A1 A0 = HEX0", "SW2..SW0"], lambda q, p: (R54[p[1]], 0x7))]))

XYZ = [((a >> 1) & a & 1) << 2 | ((a >> 1) | (a & 1)) << 1 | ((a >> 1) & (1 - (a & 1))) for a in range(4)]
LXY = "A = SW9     B = SW8     X Y Z = LEDG2 LEDG1 LEDG0"
W.append(Q(id="SLIDEXYZ", name="SLIDEXYZ", title="לוגיקה בזיכרון מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(3)] + digs(4), hexes=[None, None, None, None], variants=PAIRS,
    tables=lambda p: [col(lambda a: (XYZ[a] >> k) & 1, 2) for k in range(3)] +
                     const([b for v in (p[0] >> 1, p[0] & 1, p[1] >> 1, p[1] & 1) for b in bitsof(v, 4)], 2),
    answer=lambda p: (XYZ[p[1]], 0x7),
    describe=lambda p: f"AB {p[0]:02b}: XYZ {XYZ[p[0]]:03b}, AB {p[1]:02b}: XYZ {XYZ[p[1]]:03b}",
    B=[LXY + "     the inputs to set: HEX3 HEX2, then HEX1 HEX0     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בשקופיות 55 ו-57 מימוש שלוש פונקציות בזיכרון של 4 מילים של 3 ביטים:", "X = AB     Y = A + B     Z = AB'",
             "בלוח הזיכרון הזה:", LXY, "שימו במתגים:", "A = HEX3     B = HEX2", "מה היציאות?", "SW2 SW1 SW0 = X Y Z"],
            lambda q, p: (XYZ[p[0]], 0x7)),
           (["בלוח אותו זיכרון:", "X = AB     Y = A + B     Z = AB'", LXY, "שימו במתגים:", "A = HEX1     B = HEX0",
             "מה היציאות?", "SW2 SW1 SW0 = X Y Z"], lambda q, p: (XYZ[p[1]], 0x7))]))

# ---- more easy questions from the slides (the slide's example on the board, the per-student data only on the board)
# topic 1
LU8 = "HEX3 HEX2 = the integer part (hex)     HEX1 HEX0 = the fraction (hex)"
numq(W, "SLIDEU88", "קריאת חיישן בנקודה קבועה", 4, rv(124, 200, lambda r: r.randrange(256, 65536)),
     lambda v: [[v >> 12, (v >> 8) & 15, (v >> 4) & 15, v & 15]], LU8,
     [(["בשקופית 5: הפורמט", "U8.8", "משמש לנתוני חיישנים. בתצוגה קריאה של חיישן בפורמט הזה:", LU8,
        "מה החלק השלם שלה?"] + binl(8), lambda q, v: (v >> 8, 0xFF)),
      (["בתצוגה אותה קריאה:", LU8, "כמה רבעים שלמים יש בחלק השבור?", "fraction x 4, rounded down"] + cnt(3, 0),
       lambda q, v: ((v >> 6) & 3, 0x3))],
     lambda v: f"U8.8 {v:04X} = {v / 256}")

VSC = rv(125, 200, lambda r: r.randrange(2, 256))
LSC1 = "n = LEDG7..LEDG0 (unsigned)"
W.append(Q(id="SLIDESCI", name="SLIDESCI", title="כתיב מדעי בינארי", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=VSC,
    tables=lambda n: const(bitsof(n, 8)), answer=lambda n: (n - (1 << (n.bit_length() - 1)), 0x7F),
    describe=lambda n: f"{n} = {n:08b} = 1.f x 2^{n.bit_length() - 1}",
    B=[LSC1 + "     answer: SW6..SW0"], L=[], F=[],
    steps=[(["בשקופית 12 המספר 228 בכתיב מדעי בינארי:", "228 = 11100100 = 1.11001 x 2^7", "בנורות מספר אחר:", LSC1,
             "כתבו אותו כך. מה המעריך?", "n = 1.f x 2^E:   E = ?"] + cnt(7, 0), lambda q, n: (n.bit_length() - 1, 0x7)),
           (["בנורות אותו מספר:", LSC1, "מה נשאר אחרי שמורידים את ה-1 השמאלי? (הביטים של השבר)", "SW6..SW0 = n - 2^E"],
            lambda q, n: (n - (1 << (n.bit_length() - 1)), 0x7F))]))

LPR = "HEX3 HEX2 = the total number of bits (decimal)"
numq(W, "SLIDEPREC", "דיוק יחיד ודיוק כפול", 2, [32, 64], lambda w: [[w // 10, w % 10]], LPR,
     [(["בשקופית 17 שני פורמטים של נקודה צפה: דיוק יחיד ודיוק כפול. בתצוגה מספר הביטים של אחד מהם:", LPR,
        "כמה ביטים יש למעריך שלו?"] + binl(4), lambda q, w: (8 if w == 32 else 11, 0xF)),
      (["בתצוגה אותו פורמט:", LPR, "כמה ביטים יש לשבר שלו?", "total = 1 sign + exponent + fraction"] + binl(6),
       lambda q, w: (23 if w == 32 else 52, 0x3F))],
     lambda w: f"{w} bits: " + ("1 + 8 + 23" if w == 32 else "1 + 11 + 52"))

VNM = rv(126, 200, lambda r: (r.randrange(16, 64), r.randrange(7)))
LNM = "LEDG5..LEDG0 = the sum mantissa xx.xxxx     HEX0 = its exponent E"
def nfrac(m):
    return m & 31 if m >> 5 else (m & 15) << 1
W.append(Q(id="SLIDENORM", name="SLIDENORM", title="נרמול אחרי חיבור", inputs=[9], flat=True,
    outs=[("G", i) for i in range(6)] + hexd(0), hexes=[None, None, None, None], variants=VNM,
    tables=lambda p: const(bitsof(p[0], 6) + bitsof(p[1], 4)), answer=lambda p: (nfrac(p[0]), 0x1F),
    describe=lambda p: f"{p[0] >> 4:02b}.{p[0] & 15:04b} x 2^{p[1]} = 1.{nfrac(p[0]):05b} x 2^{p[1] + (p[0] >> 5)}",
    B=[LNM + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בשקופית 24 מנרמלים את הסכום:", "10.011 x 2^1 = 1.0011 x 2^2", "בנורות סכום אחר של מנטיסות, עם 2 ביטים שלמים:", LNM,
             "האם צריך לנרמל אותו (הביטים השלמים הם 10 או 11)?"] + UP0("צריך", "לא צריך"), lambda q, p: (p[0] >> 5, 0x1)),
           (["בנורות אותו סכום:", LNM, "מה המעריך אחרי הנרמול?", "SW2..SW0 = the new E"], lambda q, p: (p[1] + (p[0] >> 5), 0x7)),
           (["בנורות אותו סכום:", LNM, "מה 5 ביטי השבר אחרי הנרמול (אחרי ה-1 שלפני הנקודה)?", "SW4..SW0 = 1.f:  f = ?"],
            lambda q, p: (nfrac(p[0]), 0x1F))]))

# topic 2
def rev4b(b):
    return int(f"{b:04b}"[::-1], 2)
LS2P = ["Q3..Q0 = SW9..SW6 (HEX3)     Sin = SW5", LNX, "the bits to send = LEDR3..LEDR0 (LEDR0 first)"]
W.append(Q(id="SLIDES2P", name="SLIDES2P", title="מטורי למקבילי מהשקופית", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)] + [("R", i) for i in range(4)], hexes=[[9, 8, 7, 6], None, None, None],
    variants=list(range(1, 16)),
    tables=lambda b: [col(lambda r: ((r & 15) >> i) & 1, 5) for i in range(4)] + const(bitsof(b, 4), 5),
    answer=lambda b: (rev4b(b), 0xF), describe=lambda b: f"send {b & 1}{b >> 1 & 1}{b >> 2 & 1}{b >> 3}: Q = {rev4b(b):04b}",
    B=["     ".join(LS2P) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקופית 30 אוגר הזזה הוא ממיר מטורי למקבילי: בכל עליית שעון הביט החדש נכנס ל-", "Q0", "והשאר זזים.",
             "Q <= {Q[2:0], Sin}", "בלוח האוגר הזה, של 4 ביטים. במתגים הערך עכשיו והכניסה, ובנורות הערך אחרי עליית השעון הבאה:"] + LS2P +
            ["שימו במתגים:", "Q = 0000     Sin = LEDR0", "מה הערך אחרי עליית השעון הבאה?", "SW3..SW0"], lambda q, b: (b & 1, 0xF)),
           (["בלוח אותו אוגר:", "Q <= {Q[2:0], Sin}"] + LS2P +
            ["שולחים את 4 הביטים, אחד בכל עליית שעון. מה הערך אחרי 4 עליות שעון?", "SW3..SW0"], lambda q, b: (rev4b(b), 0xF))]))

LFO = "q = SW9..SW6 (HEX3)     q after the next clock edge = LEDG3..LEDG0"
W.append(Q(id="SLIDEFOUT", name="SLIDEFOUT", title="התדר של המתנד", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9, 8, 7, 6], None, None, None], variants=list(range(1, 16)),
    tables=lambda p: [col(lambda s: (((s + p) & 15) >> i) & 1, 4) for i in range(4)],
    answer=lambda p: (2 * p, 0x1F), describe=lambda p: f"p = {p}: f_out = {2 * p} Hz",
    B=[LFO + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בשקופית 29 התדר של הביט העליון במתנד בשליטה ספרתית:", "f_out = f_clk x p / 2^N",
             "בלוח מתנד של 4 ביטים עם", "p", "מוסתר. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:", LFO,
             "השעון הוא 32 הרץ. מה התדר של הביט העליון, בהרץ?", "f_clk = 32 Hz     N = 4     f_out = ?"] + binl(5),
            lambda q, p: (2 * p, 0x1F))]))

LMB = ["q = SW9..SW7 (HEX3)     q after the next clock edge = LEDG2..LEDG0", "the start value = HEX0"]
W.append(Q(id="SLIDEMSB", name="SLIDEMSB", title="הביט העליון של המונה", inputs=[9, 8, 7], flat=True,
    outs=[("G", i) for i in range(3)] + hexd(0), hexes=[[9, 8, 7], None, None, None], variants=list(range(8)),
    tables=lambda s: [col(lambda r: (((r + 1) & 7) >> i) & 1, 3) for i in range(3)] + const(bitsof(s, 4), 3),
    answer=lambda s: ((s & 4) ^ 4, 0x7),
    describe=lambda s: f"from {s:03b}: q[2] changes after {4 - (s & 3)} edges, to {(s & 4) ^ 4:03b}",
    B=["     ".join(LMB) + "     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בשקופיות 26 ו-28 מונה של 3 ביטים: 000, 001, ..., 111, 000. הביט העליון שלו משמש לחלוקת תדר.",
             "בלוח המונה הזה. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:"] + LMB +
            ["מתחילים מ:", "q = HEX0", "אחרי כמה עליות שעון הביט העליון משתנה בפעם הראשונה?", "q[2] = LEDG2"] + cnt(4),
            lambda q, s: (4 - (s & 3), 0x7)),
           (["בלוח אותו מונה:"] + LMB + ["מתחילים מ:", "q = HEX0", "מה הערך ברגע שהביט העליון משתנה?", "SW2..SW0"],
            lambda q, s: ((s & 4) ^ 4, 0x7))]))

# topic 3
MF62 = [0x01234567, 0x89ABCDEF, 0xFFFFFFFF, 0xA5A5A5A5]
MFN = ["01234567", "89ABCDEF", "FFFFFFFF", "A5A5A5A5"]
LMF2 = ["address = SW9 SW8     SW7 = 0: HEX3..HEX0 = the high 16 bits     SW7 = 1: the low 16 bits"]
def mf_digit(p, r, k):			# r = a (SW9 SW8), half (SW7); k = 0..3 for HEX3..HEX0
    return (MF62[p[r >> 1]] >> (16 * (1 - (r & 1)) + 4 * (3 - k))) & 15
W.append(Q(id="SLIDEMEMF", name="SLIDEMEMF", title="קובץ הזיכרון מהשקופית", inputs=[9, 8, 7], flat=True,
    outs=digs(4), hexes=[None, None, None, None], variants=list(itertools.permutations(range(4))),
    tables=lambda p: [col(lambda r: (mf_digit(p, r, k) >> b) & 1, 3) for k in range(4) for b in range(4)],
    answer=lambda p: (p.index(2), 0x3), describe=lambda p: " ".join(f"{a:02b}:{MFN[p[a]]}" for a in range(4)),
    B=[LMF2[0] + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בשקופית 62 ארבע שורות של קובץ זיכרון. בלוח זיכרון לקריאה בלבד שאותחל מהשורות האלה, בסדר אחר:",
             "01234567     89ABCDEF     FFFFFFFF     A5A5A5A5"] + LMF2 + ["מה כתוב בכתובת 00?"] + code(MFN),
            lambda q, p: (p[0], 0x3)),
           (["בלוח אותו זיכרון:"] + LMF2 + ["באיזו כתובת כתוב", "FFFFFFFF", "?", "SW1 SW0 = the address"],
            lambda q, p: (p.index(2), 0x3))]))

VRF2 = rv(127, 200, lambda r: (r.randrange(16), r.randrange(16), r.randrange(16)))
LRF2 = "A1 = SW9 SW8 (HEX2)     RD1 = HEX3     A2 = SW7 SW6 (HEX1)     RD2 = HEX0"
def rf2(p, a):
    return 0 if a == 0 else p[a - 1]
W.append(Q(id="SLIDERF2", name="SLIDERF2", title="קובץ אוגרים עם שני פורטי קריאה", inputs=[9, 8, 7, 6], flat=True,
    outs=hexd(3) + hexd(0), hexes=[None, [9, 8], [7, 6], None], variants=VRF2,
    tables=lambda p: [col(lambda r: (rf2(p, r >> 2) >> b) & 1, 4) for b in range(4)] +
                     [col(lambda r: (rf2(p, r & 3) >> b) & 1, 4) for b in range(4)],
    answer=lambda p: (p[1] + p[2], 0x1F), describe=lambda p: f"R0 = 0  R1 = {p[0]:X}  R2 = {p[1]:X}  R3 = {p[2]:X}",
    B=[LRF2 + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בשקופיות 63-64 קובץ אוגרים עם שני פורטי קריאה, ואוגר 0 תמיד נקרא כ-0. בלוח קובץ כזה של 4 אוגרים של 4 ביטים:", LRF2,
             "מה כתוב באוגר 1?", "SW3..SW0 = R1"], lambda q, p: (p[0], 0xF)),
           (["בלוח אותו קובץ:", LRF2, "קראו את אוגר 2 ואת אוגר 3 בבת אחת, בשני הפורטים. מה הסכום שלהם?", "SW4..SW0 = R2 + R3"],
            lambda q, p: (p[1] + p[2], 0x1F))]))

LVO = "SW9 = 0: power on     SW9 = 1: after power off and on again     HEX0 = the word in the memory"
W.append(Q(id="SLIDEVOL", name="SLIDEVOL", title="זיכרון נדיף או לא", inputs=[9], flat=True,
    outs=hexd(0), hexes=[None, None, None, None], variants=[(t, c) for t in range(2) for c in range(1, 16)],
    tables=lambda p: [[(p[1] >> b) & 1, ((p[1] if p[0] else 0) >> b) & 1] for b in range(4)],
    answer=lambda p: (p[0], 0x1), describe=lambda p: f"{['RAM', 'ROM'][p[0]]} holding {p[1]:X}",
    B=[LVO + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בשקופיות 40-42: זיכרון לקריאה וכתיבה נדיף (מאבד את המידע כשהמתח נופל), וזיכרון לקריאה בלבד שומר עליו.",
             "בלוח זיכרון של מילה אחת:", LVO, "מה כתוב בו עכשיו (המתח דלוק)?", "SW3..SW0"], lambda q, p: (p[1], 0xF)),
           (["בלוח אותו זיכרון:", LVO, "כבו והדליקו את המתח. איזה סוג זיכרון זה?"] + code(["RAM", "ROM"]),
            lambda q, p: (p[0], 0x1))]))

ORDER = ["SLIDEFMT", "SLIDESAT", "SLIDEFP", "SLIDEU88", "SLIDESCI", "SLIDEPREC", "SLIDENORM",
         "FIXEDU", "FIXEDQ", "QNEG", "TOFIXED", "SATURATE", "SATU44", "FPDECODE", "FPENCODE", "FPSPECIAL", "FPCOMPARE",
         "FPROUND", "FPADD",
         "SLIDECNT", "SLIDEDCO", "SLIDEPL", "SLIDES2P", "SLIDEFOUT", "SLIDEMSB",
         "DIVBY2N", "RESETCNT", "MODCNT", "DCO", "SHIFTDIR", "SHIFTDELAY", "PAR2SER", "PARLOAD",
         "SLIDEARR", "SLIDEROM54", "SLIDEXYZ", "SLIDEMEMF", "SLIDERF2", "SLIDEVOL", "MEMARRAY", "ADDRBITS", "WORDLINE", "ROMREAD", "ROMDOTS", "MEMFILE", "ROMLOGIC", "LUT", "RAM", "DRAMLEAK", "REGFILE"]
TOPICS = [(40, "נקודה קבועה ונקודה צפה", 19), (40, "מונים ואוגרי הזזה", 14), (40, "זיכרונות", 17)]
DESC = {"FIXEDU": "נקודה קבועה בלי סימן: החלק השלם והשבור",
        "FIXEDQ": "נקודה קבועה עם סימן: סימן, שלם ושבור",
        "TOFIXED": "לכתוב מספר עשרוני בנקודה קבועה",
        "SATURATE": "חיבור רגיל מול חיבור ברוויה",
        "FPDECODE": "לפענח מספר נקודה צפה: סימן, מעריך, ערך",
        "FPENCODE": "לקודד מספר שלם בנקודה צפה: מעריך ושבר",
        "FPSPECIAL": "מקרים מיוחדים: אפס, אינסוף, NaN",
        "FPADD": "חיבור בנקודה צפה: הזזה ומעריך הסכום",
        "DIVBY2N": "מחלק ב-2 בחזקת N: איזה ביט של המונה ומחזור הנורה",
        "RESETCNT": "מונה: ערך האיפוס והכיוון",
        "DCO": "מתנד בשליטה ספרתית: כמה מוסיפים, מתי חוזר ל-0",
        "SHIFTDIR": "אוגר הזזה: הערך אחרי עליית שעון - איפה נכנס הביט, הפוך או לא",
        "PARLOAD": "אוגר הזזה עם טעינה מקבילית",
        "MEMARRAY": "גודל מערך זיכרון: מילים וביטים",
        "ADDRBITS": "כמה ביטי כתובת למספר מילים",
        "ROMREAD": "לקרוא זיכרון לקריאה בלבד",
        "ROMLOGIC": "לוגיקה בזיכרון: איזה ביט איזו פונקציה",
        "LUT": "טבלת חיפוש: התוכן בשני חצאים",
        "RAM": "זיכרון לקריאה וכתיבה: התוכן, ובאיזו רמה של we כותבים",
        "REGFILE": "קובץ אוגרים: התוכן ואיזה אוגר מחובר ל-0",
        "QNEG": "מספר נגדי בנקודה קבועה עם סימן: היפוך ועוד 1",
        "SATU44": "חיבור ברוויה בנקודה קבועה: גלישה והתוצאה",
        "FPCOMPARE": "השוואת מספרים בנקודה צפה: סימן, מעריך, מי גדול",
        "FPROUND": "עיגול מנטיסה: למטה, למעלה, לקרוב ביותר",
        "MODCNT": "מונה עם מחזור מוסתר: הערך הגדול ואורך המחזור",
        "SHIFTDELAY": "אוגר הזזה כקו השהיה: איזו יציאה ואחרי כמה עליות שעון",
        "PAR2SER": "ממקבילי לטורי: המילה, הכיוון וסדר היציאה",
        "WORDLINE": "מפענח כתובות שבור: איזו כתובת ומה התקלה",
        "ROMDOTS": "סימון נקודות: נקודות בשורה, בעמודה ובסך הכול",
        "MEMFILE": "זיכרון שאותחל מקובץ: שורות ואיפה כתוב הערך הגדול",
        "DRAMLEAK": "תא זיכרון דינמי: מתי הביט נעלם ומתי לרענן",
        "SLIDEFMT": "מהשקופית: 6.75 בפורמט נקודה קבועה אחר",
        "SLIDESAT": "מהשקופית: חיבור ברוויה עם 12 - גלישה והתוצאה",
        "SLIDEFP": "מהשקופיות: סימן, מעריך מוטה, ואיזה מספר",
        "SLIDECNT": "מהשקופית: המונה - הערך אחרי עלייה אחת ושתיים",
        "SLIDEDCO": "מהשקופית: המתנד - הערך אחרי עלייה אחת ושתיים",
        "SLIDEPL": "מהשקופית: אוגר הזזה עם טעינה - טעינה והזזה",
        "SLIDEARR": "מהשקופית: מערך הזיכרון - המילה בשתי כתובות",
        "SLIDEROM54": "מהשקופית: שלוש פונקציות בזיכרון - המילה בשתי כתובות",
        "SLIDEXYZ": "מהשקופית: לוגיקה בזיכרון - היציאות לשתי כניסות",
        "SLIDEU88": "מהשקופית: קריאת חיישן בפורמט U8.8 - השלם והרבעים",
        "SLIDESCI": "מהשקופית: כתיב מדעי בינארי - המעריך והשבר",
        "SLIDEPREC": "מהשקופית: דיוק יחיד או כפול - ביטי המעריך והשבר",
        "SLIDENORM": "מהשקופית: נרמול הסכום - האם צריך, המעריך והשבר",
        "SLIDES2P": "מהשקופית: מטורי למקבילי - ביט ראשון וארבעה ביטים",
        "SLIDEFOUT": "מהשקופית: התדר של המתנד בשעון של 32 הרץ",
        "SLIDEMSB": "מהשקופית: מתי הביט העליון של המונה משתנה, ולאיזה ערך",
        "SLIDEMEMF": "מהשקופית: קובץ הזיכרון בסדר אחר - מה בכתובת 00 ואיפה FFFFFFFF",
        "SLIDERF2": "מהשקופית: קובץ אוגרים עם שני פורטי קריאה - אוגר וסכום",
        "SLIDEVOL": "מהשקופית: נדיף או לא - התוכן ואחרי כיבוי המתח"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "נקודה קבועה וצפה, מונים, אוגרי הזזה וזיכרונות - מהקל אל הקשה, ואי אפשר בלי הלוח")
