# -*- coding: utf-8 -*-
# Week 10 class exercise (lecture 10, Harris 5.2.4-5.2.7 + 4.9: the ALU and its flags, comparisons from the flags, SLT,
# shifters, multipliers, dividers; testbenches). Instructor only.
#   python gen_w10.py [--compile] [--only Q05] [--id <ID>]
import itertools, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(10, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0, numq, rv, binl
W = []
def col(f, n):
    return [f(r) for r in range(1 << n)]
def sv(x, n=4):
    return x - (1 << n) if x >> (n - 1) & 1 else x
OPS = ["add", "subtract", "and", "or"]
def alu(op, a, b, n=4):				# result, and the flags N Z C V of the slide's ALU
    m = (1 << n) - 1
    if op in (0, 1):
        bb = b if op == 0 else (~b & m)
        s = a + bb + op
        res, c = s & m, s >> n
        v = int(((a >> (n - 1)) == (bb >> (n - 1))) and ((res >> (n - 1)) != (a >> (n - 1))))
    else:
        res, c, v = (a & b) if op == 2 else (a | b), 0, 0
    return res, res >> (n - 1), int(res == 0), c, v

# ================================================================ topic 1: the ALU and its flags
# the ALUControl codes, in a hidden order
VAC = list(itertools.permutations(range(4)))
W.append(Q(id="ALUCODES", name="ALUCODES", title="הקודים של ה-ALU", inputs=[9, 8, 7, 6, 5, 4], flat=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9, 8], [7, 6], [5, 4], None], variants=VAC,
    tables=lambda p: [col(lambda r: (alu(p[r & 3], r >> 4, (r >> 2) & 3, 2)[0] >> k) & 1, 6) for k in range(2)],
    answer=lambda p: (p.index(0), 0x3), describe=lambda p: " ".join(f"{c:02b}={OPS[p[c]]}" for c in range(4)),
    B=["A = SW9 SW8 (HEX3)     B = SW7 SW6 (HEX2)     ALUControl = SW5 SW4 (HEX1)     Result = LEDG1 LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "של 2 ביטים, אבל הקודים של הפעולות מעורבבים.",
             "A = SW9 SW8     B = SW7 SW6     ALUControl = SW5 SW4     Result = LEDG1 LEDG0",
             "מה הקוד של", "AND", "?", "SW1 SW0"], lambda q, p: (p.index(2), 0x3)),
           (["מה הקוד של", "OR", "?", "SW1 SW0"], lambda q, p: (p.index(3), 0x3)),
           (["מה הקוד של חיבור?", "add:   SW1 SW0"], lambda q, p: (p.index(0), 0x3))]))

# an ALU with a hidden operation and a hidden B
VAF = [(op, b) for op in range(4) for b in range(1, 15)]
_seen, _v = set(), []
for _p in VAF:					# add B and subtract 16 - B look the same: keep one board of each
    _t = tuple(alu(_p[0], a, _p[1])[0] for a in range(16))
    if _t not in _seen:
        _seen.add(_t); _v.append(_p)
VAF = _v
W.append(Q(id="ALUHIDDEN", name="ALUHIDDEN", title="פעולה ומספר מוסתרים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VAF,
    tables=lambda p: [col(lambda a: (alu(p[0], a, p[1])[0] >> k) & 1, 4) for k in range(4)],
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"{OPS[p[0]]} with B = {p[1]}",
    B=["A = SW9..SW6 (HEX0)     Result = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שהפעולה וה-", "B", "שלו מוסתרים.", "A = SW9..SW6     Result = LEDG3..LEDG0",
             "שימו", "A = 0000", "והעתיקו את התוצאה:", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (alu(p[0], 0, p[1])[0], 0xF)),
           (["עכשיו", "A = 1111", "והעתיקו:", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (alu(p[0], 15, p[1])[0], 0xF)),
           (["איזו פעולה?"] + code(["add", "subtract", "and", "or"]), lambda q, p: (p[0], 0x3)),
           (["מה", "B", "?", "SW3..SW0"], lambda q, p: (p[1], 0xF))]))

# the four flags in hidden LEDs, subtracting a hidden B
VFL = [(perm, b) for perm in itertools.permutations(range(4)) for b in (3, 5, 6, 9, 10, 12)]
VFL = random.Random(101).sample(VFL, 144)
FLN = code(["LEDG0", "LEDG1", "LEDG2", "LEDG3"])
W.append(Q(id="FLAGLEDS", name="FLAGLEDS", title="דגלי ה-ALU", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + [("G", 4 + k) for k in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VFL,
    tables=lambda p: [col(lambda a: alu(1, a, p[1])[1 + p[0][i]], 4) for i in range(4)] +
                     [col(lambda a: (alu(1, a, p[1])[0] >> k) & 1, 4) for k in range(4)],
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"A - {p[1]}; " + " ".join(f"LEDG{i}={'NZCV'[p[0][i]]}" for i in range(4)),
    B=["A = SW9..SW6 (HEX0)     Result = LEDG7..LEDG4     flags = LEDG3..LEDG0 (hidden order)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שמחסר מ-", "A", "מספר מוסתר, והדגלים בנורות בסדר מוסתר:",
             "Result = A - B = LEDG7..LEDG4     N Z C V = LEDG3..LEDG0 (in some order)",
             "איזו נורה היא", "Z", "(התוצאה אפס)?"] + FLN, lambda q, p: (p[0].index(1), 0x3)),
           (["איזו נורה היא", "N", "(התוצאה שלילית)?"] + FLN, lambda q, p: (p[0].index(0), 0x3)),
           (["מה המספר המוסתר?", "B = ?     SW3..SW0"], lambda q, p: (p[1], 0xF))]))

# overflow
VOV = list(range(1, 16))
W.append(Q(id="OVERFLOWV", name="OVERFLOWV", title="דגל הגלישה", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + [("G", 4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VOV,
    tables=lambda b: [col(lambda a: (alu(0, a, b)[0] >> k) & 1, 4) for k in range(4)] + [col(lambda a: alu(0, a, b)[4], 4)],
    answer=lambda b: (alu(0, 7, b)[4], 0x1), describe=lambda b: f"A + {b}",
    B=["A = SW9..SW6 (HEX0)     Result = LEDG3..LEDG0     V = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שמחבר ל-", "A", "מספר מוסתר:", "Result = A + B     V = LEDG4", "מה המספר המוסתר?", "B = ?     SW3..SW0"],
            lambda q, b: (b, 0xF)),
           (["שימו", "A = 0111", "(המספר החיובי הגדול). האם יש גלישה?"] + UP0("יש", "אין"), lambda q, b: (alu(0, 7, b)[4], 0x1))]))

# comparisons from the flags (slide 14)
VCF = rv(102, 200, lambda r: (r.randrange(16), r.randrange(16)))
def flags_of(p):
    return alu(1, p[0], p[1])[1:]
W.append(Q(id="CMPFLAGS", name="CMPFLAGS", title="השוואה לפי הדגלים", inputs=[9], flat=True,
    outs=[("G", 3), ("G", 2), ("G", 1), ("G", 0)], hexes=[None, None, None, None], variants=VCF,
    tables=lambda p: const(list(flags_of(p))), answer=lambda p: (int(p[0] < p[1]), 0x1),
    describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}, NZCV {''.join(map(str, flags_of(p)))}",
    B=["N Z C V = LEDG3 LEDG2 LEDG1 LEDG0 (of A - B)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["ה-", "ALU", "חיסר שני מספרים מוסתרים, ורק הדגלים מוצגים:", "A - B:   N = LEDG3   Z = LEDG2   C = LEDG1   V = LEDG0",
             "האם המספרים שווים?", "A == B:  Z"] + UP0("שווים", "לא"), lambda q, p: (int(p[0] == p[1]), 0x1)),
           (["האם", "A < B", "עם סימן?", "signed A < B:  N ^ V"] + UP0("כן", "לא"), lambda q, p: (int(sv(p[0]) < sv(p[1])), 0x1)),
           (["האם", "A < B", "בלי סימן?", "unsigned A < B:  ~C"] + UP0("כן", "לא"), lambda q, p: (int(p[0] < p[1]), 0x1))]))

# SLT: N or N ^ V
VSL = [(b, fx) for b in range(16) for fx in range(2)]
def slt(p, a):
    _, n, _, _, v = alu(1, a, p[0])
    return n ^ v if p[1] else n
VSL = [p for p in VSL if p[1] or any(slt(p, a) != slt((p[0], 1), a) for a in range(16))]
W.append(Q(id="SLTFIX", name="SLTFIX", title="SLT: עם תיקון הגלישה או בלי", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSL,
    tables=lambda p: [col(lambda a: slt(p, a), 4)], answer=lambda p: (p[1], 0x1),
    describe=lambda p: f"B = {p[0]:04b}, SLT = {'N ^ V' if p[1] else 'N (no fix)'}",
    B=["A = SW9..SW6 (HEX0)     SLT result = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הפעולה", "SLT", "של ה-", "ALU", "עם מספר מוסתר:", "Result = (A < B) ? 1 : 0     (signed)",
             "בלי תיקון היא בודקת רק את דגל השלילי, ועם תיקון גם את דגל הגלישה. נסו את כל הכניסות והשוו לחשבון.", "no fix: N     fixed: N ^ V",
             "A = SW9..SW6"] + code(["N (no fix)", "N ^ V (fixed)"]), lambda q, p: (p[1], 0x1))]))

# ================================================================ topic 2: shifters, multipliers, dividers
SHN = ["sll (<<)", "srl (>>)", "sra (>>>)"]
def shf(t, k, a):
    if t == 0:
        return (a << k) & 15
    if t == 1:
        return a >> k
    return (sv(a) >> k) & 15
VSH = [(t, k) for t in range(3) for k in (1, 2, 3)]
W.append(Q(id="SHIFTKIND", name="SHIFTKIND", title="איזו הזזה?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSH,
    tables=lambda p: [col(lambda a: (shf(p[0], p[1], a) >> k) & 1, 4) for k in range(4)], answer=lambda p: (p[1], 0x3),
    describe=lambda p: f"{SHN[p[0]]} {p[1]}",
    B=["A = SW9..SW6 (HEX0)     Y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מזיז של 4 ביטים:", "A = SW9..SW6     Y = LEDG3..LEDG0", "איזה סוג הזזה? (נסו גם מספר שהביט השמאלי שלו 1)"] +
            code(SHN, 3), lambda q, p: (p[0], 0x3)),
           (["בכמה מקומות הוא מזיז?"] + cnt(3), lambda q, p: (p[1], 0x3))]))

LSM = "HEX3 = A (hex)     HEX2 = N"
numq(W, "SHIFTMUL", "הזזה שמאלה = כפל", 2, [(a, n) for a in range(1, 16) for n in (1, 2, 3)],
     lambda p: [[p[0], p[1]]], LSM,
     [(["בתצוגה מספר וכמה מקומות להזיז:", LSM, "מה", "A << N", "?", "A << N = A x 2^N"] + binl(7), lambda q, p: (p[0] << p[1], 0x7F))],
     lambda p: f"{p[0]} << {p[1]} = {p[0] << p[1]}")

LSR = "HEX3 = minus if A is negative     HEX2 = |A|     HEX1 = N"
VSR = [(a, n) for a in range(-8, 8) for n in (1, 2) if a < 0]
W.append(Q(id="SRADIV", name="SRADIV", title="הזזה אריתמטית ימינה = חילוק", inputs=[9], flat=True,
    outs=[("M", 3)] + hexd(2) + hexd(1), hexes=[None, None, None, None], variants=VSR,
    tables=lambda p: const([1] + bitsof(-p[0], 4) + bitsof(p[1], 4)), answer=lambda p: ((p[0] >> p[1]) & 15, 0xF),
    describe=lambda p: f"{p[0]} >>> {p[1]} = {p[0] >> p[1]}",
    B=["A = HEX3 HEX2 (decimal, signed)     N = HEX1     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר שלילי וכמה מקומות להזיז:", LSR, "כתבו את המספר במשלים ל-2 ב-4 ביטים:", "SW3..SW0"] + BIN4,
            lambda q, p: (p[0] & 15, 0xF)),
           (["הזיזו אותו אריתמטית ימינה (ממלאים בביט הסימן):", "A >>> N", "SW3..SW0"], lambda q, p: ((p[0] >> p[1]) & 15, 0xF))]))

LSD = "HEX3 HEX2 = A (decimal)     HEX1 = N"
numq(W, "SHIFTDIV", "הזזה לוגית ימינה = חילוק שלם", 3, [(a, n) for a in range(10, 64) for n in (1, 2, 3)][::2],
     lambda p: [[p[0] // 10, p[0] % 10, p[1]]], LSD,
     [(["בתצוגה מספר בלי סימן וכמה מקומות להזיז:", LSD, "מה", "A >> N", "? (חילוק שלם, בלי שארית)", "A >> N = A / 2^N"] + binl(6),
       lambda q, p: (p[0] >> p[1], 0x3F))],
     lambda p: f"{p[0]} >> {p[1]} = {p[0] >> p[1]}")

LMU = "HEX3 = A (hex)     HEX2 = B (hex)"
VMU = random.Random(103).sample([(a, b) for a in range(1, 16) for b in range(1, 16)], 200)
numq(W, "PARTIAL", "מכפלות חלקיות", 2, VMU, lambda p: [[p[0], p[1]]], LMU,
     [(["בתצוגה שני מספרים של 4 ביטים:", LMU, "המכפלה החלקית של ביט 2 של", "B", "היא המספר הראשון אם הביט 1, מוזזת שני מקומות שמאלה. מה היא?",
        "PP2 = (B2 ? A : 0) << 2"] + binl(6), lambda q, p: ((p[0] if (p[1] >> 2) & 1 else 0) << 2, 0x3F)),
      (["מה המכפלה כולה (8 ביטים)?", "A x B"] + binl(8), lambda q, p: (p[0] * p[1], 0xFF))],
     lambda p: f"{p[0]} x {p[1]} = {p[0] * p[1]}")

W.append(Q(id="MULTHIDDEN", name="MULTHIDDEN", title="מכפל עם מספר מוסתר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(2, 16)),
    tables=lambda b: [col(lambda a: ((a * b) >> k) & 1, 4) for k in range(8)], answer=lambda b: (b, 0xF),
    describe=lambda b: f"A x {b}",
    B=["A = SW9..SW6 (HEX0)     P = LEDG7..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מכפל של 4 על 4 ביטים, והמספר השני מוסתר:", "P = A x B     A = SW9..SW6     P = LEDG7..LEDG0",
             "מה המספר המוסתר?", "B = ?     SW3..SW0"], lambda q, b: (b, 0xF)),
           (["כמה ביטים צריך למכפלה של שני מספרים של 4 ביטים?"] + cnt(8), lambda q, b: (8, 0xF))]))

LDV = "HEX3 = A (hex)     HEX2 = B (hex)"
VDV = [(a, b) for a in range(16) for b in range(1, 16)]
VDV = random.Random(104).sample(VDV, 200)
numq(W, "DIVIDE", "חילוק: מנה ושארית", 2, VDV, lambda p: [[p[0], p[1]]], LDV,
     [(["בתצוגה מחולק ומחלק:", LDV, "A / B = Q + R / B", "מה המנה?", "Q = ?     SW3..SW0"], lambda q, p: (p[0] // p[1], 0xF)),
      (["ומה השארית?", "R = ?     SW3..SW0"], lambda q, p: (p[0] % p[1], 0xF))],
     lambda p: f"{p[0]} / {p[1]} = {p[0] // p[1]} R {p[0] % p[1]}")

def div_iter(a, b, steps):			# the slide's algorithm, the first `steps` iterations: (Q bits so far, R')
    r_, qb = 0, []
    for i in range(3, 3 - steps, -1):
        r = (r_ << 1) | ((a >> i) & 1)
        d = r - b
        if d < 0:
            qb.append(0)
        else:
            qb.append(1); r = d
        r_ = r
    return qb, r_
VDS = [(a, b) for a in range(8, 16) for b in range(1, 4)]
numq(W, "DIVSTEP", "האלגוריתם של המחלק", 2, VDS, lambda p: [[p[0], p[1]]], LDV,
     [(["בתצוגה מחולק ומחלק. האלגוריתם מהשקופית:", LDV,
        "R' = 0;  for i = 3 to 0:  R = {R' << 1, A[i]};  D = R - B;  if D < 0: Q[i] = 0, R' = R  else: Q[i] = 1, R' = D",
        "אחרי הסיבוב הראשון: מה", "i = 3:   Q[3] = ?"] + UP0("1", "0"), lambda q, p: (div_iter(p[0], p[1], 1)[0][0], 0x1)),
      (["ומה השארית החלקית אחרי שני סיבובים?", "i = 3, 2:   R' = ?     SW3..SW0"], lambda q, p: (div_iter(p[0], p[1], 2)[1], 0xF)),
      (["מה המנה בסוף?", "Q = ?     SW3..SW0"], lambda q, p: (p[0] // p[1], 0xF))],
     lambda p: f"{p[0]} / {p[1]}")

LAR = "HEX3 = N (bits)"
numq(W, "DIVARRAY", "מערך המחלק", 1, [2, 3, 4, 5, 6, 7, 8], lambda n: [[n]], LAR,
     [(["בתצוגה הרוחב של מחלק מערך (כמו המחלק של 4 על 4 בשקופית):", LAR,
        "כל שורה במערך מחשבת סיבוב אחד של האלגוריתם. כמה שורות?"] + cnt(8), lambda q, n: (n, 0xF)),
      (["כמה ביטים במכפלה של שני מספרים ברוחב הזה?", "2N"] + binl(5), lambda q, n: (2 * n, 0x1F))],
     lambda n: f"N = {n}")

# ================================================================ topic 3: testbenches (slides 30-36)
def silly(r):
    a, b, c = (r >> 2) & 1, (r >> 1) & 1, r & 1
    return int((not b and not c) or (a and not b))
VEC = "testvectors (abc_y):   000_1  001_0  010_0  011_0  100_1  101_1  110_0  111_0"
W.append(Q(id="TESTFAIL", name="TESTFAIL", title="איזה וקטור נכשל?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(8)),
    tables=lambda k: [[silly(r) ^ int(r == k) for r in range(8)]], answer=lambda k: (k, 0x7),
    describe=lambda k: f"row {k:03b} is wrong",
    B=["a = SW9     b = SW8     c = SW7     y = LEDG0 (the device under test)     answer: SW2..SW0"], L=[], F=[],
    steps=[(["הלוח הוא המעגל הנבדק", "(dut)", "של", "sillyfunction", ". קובץ הווקטורים מהשקופית:", VEC,
             "a = SW9     b = SW8     c = SW7     y = LEDG0", "באיזה וקטור הבדיקה נכשלת? כתבו את הכניסות שלו:",
             "SW2 SW1 SW0 = a b c"], lambda q, k: (k, 0x7))]))

VER = []
for m in range(256):
    if bin(m).count("1") <= 3:
        VER.append(m)
VER = random.Random(105).sample(VER, 93)
W.append(Q(id="ERRORS", name="ERRORS", title="כמה הודעות שגיאה?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VER,
    tables=lambda m: [[silly(r) ^ ((m >> r) & 1) for r in range(8)]], answer=lambda m: (bin(m).count("1"), 0x7),
    describe=lambda m: f"{bin(m).count('1')} wrong rows: {m:08b}",
    B=["a = SW9     b = SW8     c = SW7     y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הלוח הוא המעגל הנבדק. בודק עצמי מהשקופית בודק את כל 8 השורות של", "y = ~b ~c + a ~b",
             "ומדפיס הודעה על כל שורה שנכשלת:", "if (y !== expected) $display(\"failed.\");",
             "a = SW9     b = SW8     c = SW7     y = LEDG0", "כמה הודעות יודפסו?", "0 = all down"] + cnt(3),
            lambda q, m: (bin(m).count("1"), 0x7))]))

LTB = "HEX3 = high time     HEX2 = low time     (ns)"
numq(W, "TBCLOCK", "שעון בבודק", 2, [(h, l) for h in range(1, 10) for l in range(1, 10)], lambda p: [[p[0], p[1]]], LTB,
     [(["השעון בבודק:", "always begin clk = 1; #H; clk = 0; #L; end", LTB, "מה זמן המחזור?"] + binl(5),
       lambda q, p: (p[0] + p[1], 0x1F)),
      (["השעון עולה בזמן 0. מתי העלייה השלישית?", "0, T, 2T, ..."] + binl(6), lambda q, p: (2 * (p[0] + p[1]), 0x3F))],
     lambda p: f"T = {p[0] + p[1]}")

LNV = "HEX3 = inputs     HEX2 = outputs"
numq(W, "NVECTORS", "כמה וקטורי בדיקה?", 2, [(n, m) for n in range(2, 9) for m in range(1, 5)], lambda p: [[p[0], p[1]]], LNV,
     [(["בתצוגה מעגל צירופי שבודקים אותו עם כל הצירופים:", LNV, "כמה וקטורים בקובץ?", "2^inputs"] + binl(9),
       lambda q, p: (1 << p[0], 0x1FF)),
      (["כמה ביטים בכל שורה של הקובץ (כניסות ויציאות צפויות)?"] + binl(4), lambda q, p: (p[0] + p[1], 0xF))],
     lambda p: f"{1 << p[0]} vectors of {p[0] + p[1]} bits")

# the board is the DUT: write one line of its testvector file
VVL = [(f, k) for f in range(4) for k in range(8)]
FNS = [silly, lambda r: (r >> 2) ^ ((r >> 1) & 1) ^ (r & 1), lambda r: int(((r >> 2) & 1) + ((r >> 1) & 1) + (r & 1) >= 2),
       lambda r: int(r in (1, 2, 4))]
W.append(Q(id="VECLINE", name="VECLINE", title="שורה בקובץ הווקטורים", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0))], hexes=[None, None, None, None], variants=VVL,
    tables=lambda p: [[FNS[p[0]](r) & 1 for r in range(8)]] + const(G.bits(p[1], 3), 3),
    answer=lambda p: ((p[1] << 1) | (FNS[p[0]](p[1]) & 1), 0xF), describe=lambda p: f"function {p[0]}, line {p[1]:03b}",
    B=["a = SW9   b = SW8   c = SW7   y = LEDG0   the line to write = HEX3 HEX2 HEX1 (a b c)   answer: SW3..SW0"], L=[], F=[],
    steps=[(["הלוח הוא מעגל, ואתם כותבים לו קובץ וקטורים. כל שורה היא", "abc_yexpected",
             "a = SW9   b = SW8   c = SW7   y = LEDG0", "כתבו את השורה של הכניסות שבתצוגה:", "HEX3 HEX2 HEX1 = a b c",
             "SW3 SW2 SW1 = a b c     SW0 = y"], lambda q, p: ((p[1] << 1) | (FNS[p[0]](p[1]) & 1), 0xF))]))

# ================================================================ added questions: topic 1
# the Z flag of an AND with a hidden mask
W.append(Q(id="ZEROAND", name="ZEROAND", title="דגל האפס בפעולת וגם", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: alu(2, a, b)[2], 4)], answer=lambda b: (1 << (4 - bin(b).count("1")), 0x1F),
    describe=lambda b: f"Z of A AND {b:04b}",
    B=["A = SW9..SW6 (HEX0)     Z = LEDG0 (of A AND B, B hidden)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שעושה", "AND", "בין", "A", "למספר מוסתר, ורק דגל האפס מוצג:",
             "Result = A AND B     Z = LEDG0     A = SW9..SW6", "שימו", "A = 0001", ". האם", "Z", "דולק?"] + UP0("דולק", "כבוי"),
            lambda q, b: (int(not b & 1), 0x1)),
           (["Z = LEDG0     A = SW9..SW6", "מה המספר המוסתר?", "B = ?     SW3..SW0"], lambda q, b: (b, 0xF)),
           (["Z = LEDG0     A = SW9..SW6", "לכמה ערכים של", "A", "הדגל", "Z", "דולק?"] + binl(5),
            lambda q, b: (1 << (4 - bin(b).count("1")), 0x1F))]))

# the C flag of a subtraction: C = 1 when A >= B (unsigned)
W.append(Q(id="CARRYC", name="CARRYC", title="דגל הנשא בחיסור", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: alu(1, a, b)[3], 4)], answer=lambda b: (16 - b, 0x1F),
    describe=lambda b: f"C of A - {b}",
    B=["A = SW9..SW6 (HEX0)     C = LEDG0 (of A - B, B hidden)     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שמחסר מ-", "A", "מספר מוסתר, ורק דגל הנשא מוצג:",
             "Result = A - B = A + ~B + 1     C = LEDG0     A = SW9..SW6",
             "מה הערך הקטן ביותר של", "A", "שנותן נשא?", "SW3..SW0"], lambda q, b: (b, 0xF)),
           (["C = LEDG0     A = SW9..SW6", "לכמה ערכים של", "A", "יש נשא?"] + binl(5), lambda q, b: (16 - b, 0x1F))]))

# overflow of a subtraction with a hidden signed B
W.append(Q(id="OVFSUB", name="OVFSUB", title="גלישה בחיסור", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 16)),
    tables=lambda b: [col(lambda a: alu(1, a, b)[4], 4)], answer=lambda b: (b, 0xF),
    describe=lambda b: f"V of A - ({sv(b)})",
    B=["A = SW9..SW6 (HEX0, signed)     V = LEDG0 (of A - B, B hidden)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח", "ALU", "שמחסר מ-", "A", "מספר מוסתר עם סימן, ורק דגל הגלישה מוצג:",
             "Result = A - B     V = LEDG0     A = SW9..SW6", "שימו", "A = 1000", "(מינוס 8). האם יש גלישה?"] + UP0("יש", "אין"),
            lambda q, b: (alu(1, 8, b)[4], 0x1)),
           (["V = LEDG0     A = SW9..SW6", "לכמה ערכים של", "A", "יש גלישה?"] + binl(4), lambda q, b: (abs(sv(b)), 0xF)),
           (["V = LEDG0     A = SW9..SW6", "מה המספר המוסתר, במשלים ל-2?", "B = ?     SW3..SW0"], lambda q, b: (b, 0xF))]))

# which row of the slide-14 table drives the LED
FFN = ["N ^ V", "~C", "Z | (N ^ V)", "Z | ~C", "~Z & ~(N ^ V)", "~Z & C", "~(N ^ V)", "C"]
def ffv(f, a, b):
    _, n, z, c, v = alu(1, a, b)
    return [n ^ v, 1 - c, z | (n ^ v), z | (1 - c), (1 - z) & (1 - (n ^ v)), (1 - z) & c, 1 - (n ^ v), c][f]
FFB = [b for b in range(16) if b not in (0, 7, 8, 15)]		# no LED that never lights (A < 0 unsigned, A > 7 signed, ...)
assert all(len({tuple(ffv(f, a, b) for a in range(16)) for f in range(8)}) == 8 for b in FFB)
VFF = [(f, b) for f in range(8) for b in FFB]
W.append(Q(id="FLAGFORM", name="FLAGFORM", title="איזו השוואה בנורה?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)] + hexd(1), hexes=[None, None, None, [9, 8, 7, 6]], variants=VFF,
    tables=lambda p: [col(lambda a: ffv(p[0], a, p[1]), 4)] + const(bitsof(p[1], 4), 4), answer=lambda p: (p[0], 0x7),
    describe=lambda p: f"B = {p[1]:04b}, LED = {FFN[p[0]]}",
    B=["A = SW9..SW6 (HEX0)     B = HEX1     LEDG0 = a comparison of A and B (from the flags of A - B)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השוואה אחת בין", "A", "ל-", "B", ", מחושבת מהדגלים של החיסור:",
             "A = SW9..SW6 (HEX0)     B = HEX1     LEDG0 = (A ? B)",
             "ההשוואה עם סימן או בלי סימן? (נסו גם מספרים שהביט השמאלי שלהם 1)"] + code(["signed", "unsigned"]),
            lambda q, p: (p[0] & 1, 0x1)),
           (["A = SW9..SW6 (HEX0)     B = HEX1     LEDG0 = (A ? B)", "איזה יחס?"] + code(["A < B", "A <= B", "A > B", "A >= B"]),
            lambda q, p: (p[0] >> 1, 0x3)),
           (["איזו נוסחה של הדגלים מדליקה את הנורה?"] + code(FFN), lambda q, p: (p[0], 0x7))]))

# ================================================================ added questions: topic 2
# a register that shifts itself on every clock edge (no clock button: q now on switches, q after the next edge on the
# LEDs; the start value is on HEX3)
VSS = [(0, r) for r in range(1, 16)] + [(1, r) for r in range(8, 16)] + [(2, r) for r in range(8, 15)]
def ss_stop(p):
    q_, k = p[1], 0
    while shf(p[0], 1, q_) != q_:
        q_, k = shf(p[0], 1, q_), k + 1
    return k
LSS = "q = SW9..SW6 (HEX0)     q after the next clock edge = LEDG3..LEDG0"
W.append(Q(id="SHIFTSEQ", name="SHIFTSEQ", title="הזזה בכל עליית שעון", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3), hexes=[None, None, None, [9, 8, 7, 6]], variants=VSS,
    tables=lambda p: [col(lambda s: (shf(p[0], 1, s) >> i) & 1, 4) for i in range(4)] + const(bitsof(p[1], 4), 4),
    answer=lambda p: (ss_stop(p), 0x7), describe=lambda p: f"start {p[1]:04b}, {SHN[p[0]]} 1 per clock edge",
    B=[LSS + "     HEX3 = the start value     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר שמזיז את עצמו במקום אחד בכל עליית שעון. במתגים הערך עכשיו, ובנורות הערך אחרי עליית השעון הבאה:",
             LSS, "איזו הזזה?"] + code(SHN, 3), lambda q, p: (p[0], 0x3)),
           (["בלוח אותו אוגר:", LSS, "HEX3 = the start value",
             "מתחילים בערך שבתצוגה. מה הערך אחרי שתי עליות שעון?", "SW3..SW0 = q"], lambda q, p: (shf(p[0], 2, p[1]), 0xF)),
           (["בלוח אותו אוגר:", LSS, "HEX3 = the start value",
             "מתחילים בערך שבתצוגה. אחרי כמה עליות שעון הוא מפסיק להשתנות?"] + cnt(4, 0), lambda q, p: (ss_stop(p), 0x7))]))

# shifting a negative number left (slide 21, 5 bits)
LSN = "HEX3 = minus     HEX2 = |A|     HEX1 = N"
VSN = [(a, n) for a in range(-9, 0) for n in (1, 2, 3)]
W.append(Q(id="SLLNEG", name="SLLNEG", title="הזזה שמאלה של מספר שלילי", inputs=[9], flat=True,
    outs=[("M", 3)] + hexd(2) + hexd(1), hexes=[None, None, None, None], variants=VSN,
    tables=lambda p: const([1] + bitsof(-p[0], 4) + bitsof(p[1], 4)), answer=lambda p: (int(p[0] << p[1] >= -16), 0x1),
    describe=lambda p: f"{p[0]} << {p[1]} = {((p[0] << p[1]) & 31):05b} ({p[0] << p[1]})",
    B=["A = HEX3 HEX2 (decimal, negative)     N = HEX1     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר שלילי וכמה מקומות להזיז:", LSN, "כתבו אותו במשלים ל-2 ב-5 ביטים:", "A"] + binl(5),
            lambda q, p: (p[0] & 31, 0x1F)),
           (["הזיזו אותו שמאלה (5 ביטים, ממלאים ב-0):", LSN, "A << N"] + binl(5), lambda q, p: ((p[0] << p[1]) & 31, 0x1F)),
           (["האם התוצאה ב-5 ביטים עדיין שווה לכפל?", LSN, "A << N == A x 2^N"] + UP0("שווה", "לא (גלישה)"),
            lambda q, p: (int(p[0] << p[1] >= -16), 0x1))]))

# a shifter with one stuck output
VSB = [(t, k, s) for t in range(2) for k in range(4) for s in range(2)]
def sbug(p, r):
    a, sh = r >> 2, r & 3
    y = (a << sh) & 15 if p[0] == 0 else a >> sh
    return (y & ~(1 << p[1])) | (p[2] << p[1])
W.append(Q(id="SHIFTBUG", name="SHIFTBUG", title="מזיז עם יציאה תקועה", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, [5, 4], [9, 8, 7, 6]], variants=VSB,
    tables=lambda p: [col(lambda r: (sbug(p, r) >> k) & 1, 6) for k in range(4)], answer=lambda p: (p[2], 0x1),
    describe=lambda p: f"{SHN[p[0]]}, LEDG{p[1]} stuck at {p[2]}",
    B=["A = SW9..SW6 (HEX0)     shamt = SW5 SW4 (HEX1)     Y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מזיז של 4 ביטים, ואחת היציאות שלו תקועה:", "A = SW9..SW6     shamt = SW5 SW4     Y = LEDG3..LEDG0",
             "לאיזה כיוון הוא מזיז?"] + code(SHN[:2]), lambda q, p: (p[0], 0x1)),
           (["A = SW9..SW6     shamt = SW5 SW4     Y = LEDG3..LEDG0", "איזו יציאה תקועה?"] + FLN, lambda q, p: (p[1], 0x3)),
           (["A = SW9..SW6     shamt = SW5 SW4     Y = LEDG3..LEDG0", "על איזה ערך היא תקועה?"] + code(["0", "1"]), lambda q, p: (p[2], 0x1))]))

# an array multiplier with one broken partial-product row
VAB = [(k, m) for k in range(4) for m in range(2)]
def abug(p, a, b):
    return a * ((b & ~(1 << p[0])) | (p[1] << p[0]))
W.append(Q(id="ARRAYBUG", name="ARRAYBUG", title="מכפל מערך עם שורה שבורה", inputs=[9, 8, 7, 6, 5, 4, 3, 2], flat=True, small=True,
    outs=[("G", i) for i in range(8)], hexes=[[9, 8, 7, 6], [5, 4, 3, 2], None, None], variants=VAB,
    tables=lambda p: [col(lambda r: (abug(p, r >> 4, r & 15) >> k) & 1, 8) for k in range(8)], answer=lambda p: (p[1], 0x1),
    describe=lambda p: f"row PP{p[0]} is always {'A << k' if p[1] else '0'}",
    B=["A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDG7..LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח מכפל מערך של 4 על 4, ואחת מארבע השורות של המכפלות החלקיות שבורה:",
             "A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDG7..LEDG0", "PPk = (Bk ? A : 0) << k",
             "איזו שורה שבורה?"] + code(["PP0", "PP1", "PP2", "PP3"]), lambda q, p: (p[0], 0x3)),
           (["A = SW9..SW6 (HEX3)     B = SW5..SW2 (HEX2)     P = LEDG7..LEDG0", "PPk = (Bk ? A : 0) << k", "השורה השבורה תמיד אפס, או תמיד מוסיפה את המספר הראשון?"] + code(["PPk = 0", "PPk = A << k"]),
            lambda q, p: (p[1], 0x1))]))

# a divider that shows only the remainder, the divisor hidden
W.append(Q(id="REMHIDDEN", name="REMHIDDEN", title="מחלק שמראה רק שארית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(2, 16)),
    tables=lambda b: [col(lambda a: ((a % b) >> k) & 1, 4) for k in range(4)], answer=lambda b: (15 // b, 0xF),
    describe=lambda b: f"A mod {b}",
    B=["A = SW9..SW6 (HEX0)     R = LEDG3..LEDG0 (A / B, B hidden)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מחלק עם מחלק מוסתר, ורק השארית מוצגת:", "A / B = Q + R / B     A = SW9..SW6     R = LEDG3..LEDG0",
             "מה השארית הגדולה ביותר שרואים?", "SW3..SW0"], lambda q, b: (b - 1, 0xF)),
           (["A = SW9..SW6     R = LEDG3..LEDG0", "מה המחלק המוסתר?", "B = ?     SW3..SW0"], lambda q, b: (b, 0xF)),
           (["מה המנה כשהמחולק הוא 15?", "A = 1111:   Q = ?     SW3..SW0"], lambda q, b: (15 // b, 0xF))]))

# ================================================================ added questions: topic 3
# the simple testbench (slide 32): which vector is applied at time t, and what the dut answers
VTT = rv(106, 200, lambda r: (r.randrange(1, 255), r.randrange(80)))
TTL = "000 at #0     001 at #10     010 at #20     ...     111 at #70"
TTD = "a = SW9   b = SW8   c = SW7   y = LEDG0 (dut)"
W.append(Q(id="TBTIME", name="TBTIME", title="מה הבודק רואה בזמן נתון?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)] + hexd(3) + hexd(2), hexes=[None, None, None, None], variants=VTT,
    tables=lambda p: [[(p[0] >> r) & 1 for r in range(8)]] + const(bitsof(p[1] // 10, 4) + bitsof(p[1] % 10, 4), 3),
    answer=lambda p: ((p[0] >> (p[1] // 10)) & 1, 0x1),
    describe=lambda p: f"t = {p[1]}: abc {p[1] // 10:03b}, y {(p[0] >> (p[1] // 10)) & 1}",
    B=["a = SW9   b = SW8   c = SW7   y = LEDG0 (dut)     t = HEX3 HEX2 (decimal)     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בודק פשוט נותן את הכניסות אחת אחרי השנייה, כל אחת אחרי 10 יחידות זמן:", TTL,
             "בתצוגה זמן:", "t = HEX3 HEX2 (decimal)", "אילו כניסות מקבל המעגל בזמן הזה?", "SW2 SW1 SW0 = a b c"],
            lambda q, p: (p[1] // 10, 0x7)),
           (["הלוח הוא המעגל הנבדק:", TTD, "מה היציאה בזמן שבתצוגה?", "t = HEX3 HEX2 (decimal)"] + UP0("1", "0"),
            lambda q, p: ((p[0] >> (p[1] // 10)) & 1, 0x1))]))

# testvector testbench clock (slide 35): assign on the rising edge, compare on the falling edge
LTC = "HEX3 = high time     HEX2 = low time     HEX1 = k     (ns)"
TCK = "always begin clk = 1; #H; clk = 0; #L; end"
numq(W, "TBCOMPARE", "מתי הבודק משווה?", 3, rv(107, 200, lambda r: (r.randrange(1, 10), r.randrange(1, 10), r.randrange(2, 6))),
     lambda p: [[p[0], p[1], p[2]]], LTC,
     [(["השעון בבודק עם וקטורים:", TCK, LTC, "הכניסות נכנסות בעלייה, והיציאות נבדקות בירידה.",
        "מתי הבדיקה הראשונה?"] + binl(4), lambda q, p: (p[0], 0xF)),
      (["השעון עולה בזמן 0, ואז נכנס הווקטור הראשון.", TCK, LTC, "מתי נכנס הווקטור", "k", "?"] + binl(7),
       lambda q, p: ((p[2] - 1) * (p[0] + p[1]), 0x7F)),
      (["מתי נבדקת היציאה של הווקטור", "k", "?", TCK, LTC] + binl(7),
       lambda q, p: ((p[2] - 1) * (p[0] + p[1]) + p[0], 0x7F))],
     lambda p: f"T = {p[0] + p[1]}, vector {p[2]}: in at {(p[2] - 1) * (p[0] + p[1])}, check at {(p[2] - 1) * (p[0] + p[1]) + p[0]}")

# ================================================================ easy questions straight from the slides (at the start of each topic)
# topic 1: the slide's ALU (slides 3-5), 4 bits: A and B on the display, ALUControl on the switches
LAE = "A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDG3..LEDG0"
def alu_board(p):
    return [col(lambda r: (alu(r, p[0], p[1])[0] >> k) & 1, 2) for k in range(4)] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 2)
W.append(Q(id="ALUEX", name="ALUEX", title="ה-ALU מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8]],
    variants=rv(201, 200, lambda r: (r.randrange(16), r.randrange(16))), tables=alu_board,
    answer=lambda p: (alu(1, p[0], p[1])[0], 0xF), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}",
    B=[LAE + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח ה-", "ALU", "של שקופיות 3-5, ב-4 ביטים:", LAE,
             "הדוגמה של שקופית 5: חיבור.", "A + B:   ALUControl = 00", "מה התוצאה?", "SW3..SW0 = Result"],
            lambda q, p: (alu(0, p[0], p[1])[0], 0xF)),
           (["הדוגמה של שקופיות 3-4:", "A OR B:   ALUControl = 11", LAE, "מה התוצאה?", "SW3..SW0 = Result"],
            lambda q, p: (alu(3, p[0], p[1])[0], 0xF)),
           (["חיסור:", "A - B:   ALUControl = 01", LAE, "מה התוצאה?", "SW3..SW0 = Result"],
            lambda q, p: (alu(1, p[0], p[1])[0], 0xF))]))

# the same ALU, the flags of slides 8-10 (no flag LEDs: the student finds them from Result)
W.append(Q(id="FLAGEX", name="FLAGEX", title="הדגלים מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8]],
    variants=rv(202, 200, lambda r: (r.randrange(16), r.randrange(16))), tables=alu_board,
    answer=lambda p: (alu(0, p[0], p[1])[3], 0x1), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}",
    B=[LAE + "     answer: SW0"], L=[], F=[],
    steps=[(["בלוח ה-", "ALU", "של שקופית 6, בלי נורות לדגלים:", LAE,
             "שקופית 8: הדגל", "N", "הוא הביט השמאלי של התוצאה.", "A - B:   ALUControl = 01",
             "האם", "N = 1", "?"] + UP0("כן", "לא"), lambda q, p: (alu(1, p[0], p[1])[1], 0x1)),
           (["שקופית 9: הדגל", "Z = 1", "כשכל הביטים של התוצאה 0.", "A AND B:   ALUControl = 10", LAE,
             "האם", "Z = 1", "?"] + UP0("כן", "לא"), lambda q, p: (alu(2, p[0], p[1])[2], 0x1)),
           (["שקופית 10: הדגל", "C", "הוא הנשא שיוצא מהמחבר.", "A + B:   ALUControl = 00", LAE,
             "האם", "C = 1", "? (האם הסכום גדול מ-15)"] + UP0("כן", "לא"), lambda q, p: (alu(0, p[0], p[1])[3], 0x1))]))

# the ALU with SLT (slides 16-17, with the overflow fix): ALUControl on 3 switches
def alu3(c, a, b):
    if c in (0, 1, 2, 3):
        return alu(c, a, b)[0]
    if c == 5:
        _, n, _, _, v = alu(1, a, b)
        return n ^ v
    return 0
def _slt_pair(r):
    a, b = r.randrange(16), r.randrange(16)
    if r.random() < 0.4 and not alu(1, a, b)[4]:	# more boards that overflow (slide 17)
        return None
    return (a, b)
LSE = "A = HEX3     B = HEX2     ALUControl = SW9 SW8 SW7 (HEX0)     Result = LEDG3..LEDG0"
W.append(Q(id="SLTEX", name="SLTEX", title="SLT מהשקופית", inputs=[9, 8, 7], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8, 7]],
    variants=rv(203, 200, _slt_pair),
    tables=lambda p: [col(lambda r: (alu3(r, p[0], p[1]) >> k) & 1, 3) for k in range(4)] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 3),
    answer=lambda p: (alu3(5, p[0], p[1]), 0xF), describe=lambda p: f"A {sv(p[0])} B {sv(p[1])}",
    B=[LSE + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח ה-", "ALU", "של שקופיות 16-17, עם", "SLT", "ועם תיקון הגלישה:", LSE,
             "000 add     001 subtract     010 and     011 or     101 slt",
             "חיסור: מה התוצאה?", "A - B:   ALUControl = 001", "SW3..SW0 = Result"], lambda q, p: (alu(1, p[0], p[1])[0], 0xF)),
           (["עכשיו", "SLT", "(עם סימן):", "Result = (A < B) ? 0001 : 0000     ALUControl = 101", LSE,
             "מה התוצאה?", "SW3..SW0 = Result"], lambda q, p: (alu3(5, p[0], p[1]), 0xF))]))

# topic 2: the slide's shifters (slides 19-20), 4 bits, shamt on the switches
LSXA = "A = HEX3     shamt = SW9 SW8 (HEX0)"
W.append(Q(id="SHIFTEX", name="SHIFTEX", title="ההזזות מהשקופית", inputs=[9, 8], flat=True,
    outs=[("R", i) for i in range(4)] + [("G", 4 + i) for i in range(4)] + [("G", i) for i in range(4)] + hexd(3),
    hexes=[None, None, None, [9, 8]], variants=list(range(1, 16)),
    tables=lambda a: [col(lambda s: (shf(0, s, a) >> k) & 1, 2) for k in range(4)] +
                     [col(lambda s: (shf(1, s, a) >> k) & 1, 2) for k in range(4)] +
                     [col(lambda s: (shf(2, s, a) >> k) & 1, 2) for k in range(4)] + const(bitsof(a, 4), 2),
    answer=lambda a: (shf(0, 2, a), 0xF), describe=lambda a: f"A {a:04b}",
    B=[LSXA + "     << = LEDR3..LEDR0     >> = LEDG7..LEDG4     >>> = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המזיזים של שקופית 20, ב-4 ביטים.", "הדוגמה של שקופית 19:", "11001 >> 2 = 00110",
             LSXA + "     A >> shamt = LEDG7..LEDG4", "מה", "A >> 2", "?", "SW3..SW0"], lambda q, a: (shf(1, 2, a), 0xF)),
           (["הדוגמה של שקופית 19 בהזזה אריתמטית:", "11001 >>> 2 = 11110",
             LSXA + "     A >>> shamt = LEDG3..LEDG0", "מה", "A >>> 2", "?", "SW3..SW0"], lambda q, a: (shf(2, 2, a), 0xF)),
           (["הדוגמה של שקופית 19 בהזזה שמאלה:", "11001 << 2 = 00100",
             LSXA + "     A << shamt = LEDR3..LEDR0", "מה", "A << 2", "?", "SW3..SW0"], lambda q, a: (shf(0, 2, a), 0xF))]))

# the 4 x 4 multiplier (slides 22-23): A and B on the display, P on the LEDs
LMX = "A = HEX3     B = HEX2     P = A x B = LEDG7..LEDG0"
W.append(Q(id="MULEX", name="MULEX", title="המכפל מהשקופית", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2), hexes=[None, None, None, None],
    variants=random.Random(204).sample([(a, b) for a in range(1, 16) for b in range(1, 16)], 200),
    tables=lambda p: const(bitsof(p[0] * p[1], 8) + bitsof(p[0], 4) + bitsof(p[1], 4)),
    answer=lambda p: (p[0] * p[1], 0xFF), describe=lambda p: f"{p[0]:04b} x {p[1]:04b} = {p[0] * p[1]:08b}",
    B=[LMX + "     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח המכפל של 4 על 4 משקופית 23.", "הדוגמה של שקופית 22:", "0101 x 0111:   0101 + 0101 << 1 + 0101 << 2 + 0000 << 3",
             "לכל ביט של", "B", "יש מכפלה חלקית:", "A", "אם הביט 1, ואפס אם הביט 0.", "A = HEX3     B = HEX2",
             "כמה מכפלות חלקיות אינן אפס?"] + cnt(4, 0), lambda q, p: (bin(p[1]).count("1"), 0xF)),
           (["מה המכפלה? (בדקו בנורות)", LMX] + binl(8), lambda q, p: (p[0] * p[1], 0xFF))]))

# the divider (slides 25-27) with the slide's dividend 1101 and a divisor on the display
LDX = "A = SW9..SW6 (HEX0)     B = HEX3     Q = LEDG7..LEDG4     R = LEDG3..LEDG0"
W.append(Q(id="DIVEX", name="DIVEX", title="המחלק מהשקופית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + [("G", 4 + i) for i in range(4)] + hexd(3), hexes=[None, None, None, [9, 8, 7, 6]],
    variants=[1] + list(range(3, 16)),
    tables=lambda b: [col(lambda a: ((a % b) >> k) & 1, 4) for k in range(4)] + [col(lambda a: ((a // b) >> k) & 1, 4) for k in range(4)]
                     + const(bitsof(b, 4), 4),
    answer=lambda b: (13 % b, 0xF), describe=lambda b: f"1101 / {b:04b} = {13 // b:04b} R {13 % b}",
    B=[LDX + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המחלק של 4 על 4 משקופית 27.", "הדוגמה של שקופית 25:", "1101 / 0010 = 0110 R1",
             LDX, "שימו את המחולק של השקופית:", "A = 1101", "מה המנה?", "Q = ?     SW3..SW0"], lambda q, b: (13 // b, 0xF)),
           (["A = 1101", LDX, "מה השארית?", "R = ?     SW3..SW0"], lambda q, b: (13 % b, 0xF))]))

# topic 3: sillyfunction (slide 31) is the board; the vector to apply on the display
LSI = "a = SW9     b = SW8     c = SW7     y = LEDG0"
W.append(Q(id="SILLYEX", name="SILLYEX", title="sillyfunction בלוח", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0))], hexes=[None, None, None, None], variants=list(range(8)),
    tables=lambda k: [[silly(r) for r in range(8)]] + const(G.bits(k, 3), 3),
    answer=lambda k: (10 * k, 0x7F), describe=lambda k: f"abc {k:03b}, y {silly(k)}, t = {10 * k}",
    B=[LSI + "     the inputs to apply = HEX3 HEX2 HEX1 (a b c)     answer: SW6..SW0"], L=[], F=[],
    steps=[(["הלוח הוא", "sillyfunction", "של שקופית 31:", "y = ~b & ~c | a & ~b", LSI,
             "שימו את הכניסות שבתצוגה:", "HEX3 HEX2 HEX1 = a b c", "מה", "y", "?"] + UP0("1", "0"), lambda q, k: (silly(k), 0x1)),
           (["הבודק הפשוט של שקופית 32 נותן כניסה חדשה כל 10 יחידות זמן:", "000 at #0     001 at #10     010 at #20     ...     111 at #70",
             "מתי הוא נותן את הכניסות שבתצוגה?", "HEX3 HEX2 HEX1 = a b c"] + binl(7), lambda q, k: (10 * k, 0x7F))]))

# one line of example.txt (slide 36) on the display; the board is the dut, sometimes wrong in that line
LTX = "HEX3 HEX2 HEX1 = a b c     HEX0 = yexpected"
W.append(Q(id="VECEX", name="VECEX", title="שורה מקובץ הווקטורים", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))], hexes=[None, None, None, None],
    variants=[(k, e) for k in range(8) for e in range(2)],
    tables=lambda p: [[silly(r) ^ int(p[1] and r == p[0]) for r in range(8)]] + const(G.bits(p[0], 3) + [silly(p[0])], 3),
    answer=lambda p: (1 - p[1], 0x1), describe=lambda p: f"line {p[0]:03b}_{silly(p[0])}, dut {'wrong' if p[1] else 'right'}",
    B=[LSI + "     " + LTX + "     answer: SW0"], L=[], F=[],
    steps=[(["בתצוגה שורה מהקובץ", "example.txt", "של שקופית 36:", "abc_yexpected", LTX,
             "הלוח הוא המעגל הנבדק:", LSI, "שימו את הכניסות של השורה. מה", "y", "?"] + UP0("1", "0"),
            lambda q, p: (silly(p[0]) ^ p[1], 0x1)),
           (["הבודק של שקופית 35 משווה את", "y", "ל-", "yexpected", ".", LSI, LTX,
             "האם הבדיקה עוברת?"] + UP0("עוברת", "שגיאה"), lambda q, p: (1 - p[1], 0x1))]))

# ================================================================ more easy questions from the slides (after the first easy ones)
# topic 1: the adder inside the ALU (slide 5): ALUControl0 picks B or ~B and Cin
LAC = "A = HEX3     B = HEX2     ALUControl0 = SW9 (HEX0)     2nd input = LEDG3..LEDG0     Sum = LEDG7..LEDG4     Cin = LEDR0"
def _addc(p, c):
    bb = p[1] if c == 0 else (~p[1] & 15)
    return bb, (p[0] + bb + c) & 15
W.append(Q(id="ADDCEX", name="ADDCEX", title="המחבר שבתוך ה-ALU", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)] + [("R", 0)] + hexd(3) + hexd(2), hexes=[None, None, None, [9]],
    variants=rv(205, 200, lambda r: (r.randrange(16), r.randrange(16))),
    tables=lambda p: [col(lambda c: (_addc(p, c)[0] >> k) & 1, 1) for k in range(4)] +
                     [col(lambda c: (_addc(p, c)[1] >> k) & 1, 1) for k in range(4)] + [[0, 1]] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 1),
    answer=lambda p: (alu(1, p[0], p[1])[0], 0xF), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b}",
    B=[LAC + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המחבר שבתוך ה-", "ALU", "של שקופית 5:", LAC,
             "הדוגמה של שקופית 5: בחיבור", "ALUControl0 = 0:   Cin = 0,   2nd input = B",
             "בחיסור:", "ALUControl0 = 1", "מה הכניסה השנייה של המחבר?", "SW3..SW0 = 2nd input"], lambda q, p: (~p[1] & 15, 0xF)),
           (["ומה הסכום בחיסור?", "ALUControl0 = 1:   Sum = A + ~B + Cin", LAC, "SW3..SW0 = Sum"],
            lambda q, p: (alu(1, p[0], p[1])[0], 0xF))]))

# the ALU with the four flags (slides 11-13): V of an addition and of a subtraction
LOV = "A = HEX3     B = HEX2     ALUControl = SW9 SW8 (HEX0)     Result = LEDG3..LEDG0     N Z C V = LEDG7 LEDG6 LEDG5 LEDG4"
def _ovf_pair(r):
    a, b = r.randrange(16), r.randrange(16)
    if r.random() < 0.5 and not (alu(0, a, b)[4] or alu(1, a, b)[4]):
        return None
    return (a, b)
W.append(Q(id="OVFEX", name="OVFEX", title="דגל הגלישה מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2), hexes=[None, None, None, [9, 8]],
    variants=rv(206, 200, _ovf_pair),
    tables=lambda p: [col(lambda r: (alu(r, p[0], p[1])[0] >> k) & 1, 2) for k in range(4)] +
                     [col(lambda r: alu(r, p[0], p[1])[f], 2) for f in (4, 3, 2, 1)] + const(bitsof(p[0], 4) + bitsof(p[1], 4), 2),
    answer=lambda p: (alu(1, p[0], p[1])[4], 0x1), describe=lambda p: f"A {sv(p[0])} B {sv(p[1])}",
    B=[LOV + "     answer: SW0"], L=[], F=[],
    steps=[(["בלוח ה-", "ALU", "עם הדגלים של שקופית 13, מספרים עם סימן:", LOV,
             "שקופית 11: גלישה כשמחברים שני מספרים עם אותו סימן ומקבלים תוצאה עם סימן הפוך.",
             "A + B:   ALUControl = 00", "האם", "V = 1", "?"] + UP0("כן", "לא"), lambda q, p: (alu(0, p[0], p[1])[4], 0x1)),
           (["שקופית 12: גם בחיסור.", "A - B:   ALUControl = 01", LOV, "האם", "V = 1", "?"] + UP0("כן", "לא"),
            lambda q, p: (alu(1, p[0], p[1])[4], 0x1))]))

# the comparison table (slide 14): the flags of A - B with A on the switches
LCE = "A = SW9..SW6     B = HEX3     A - B:   N = LEDG3   Z = LEDG2   C = LEDG1   V = LEDG0"
W.append(Q(id="CMPEX", name="CMPEX", title="השוואה מהטבלה של השקופית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 3), ("G", 2), ("G", 1), ("G", 0)] + hexd(3), hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(16)),
    tables=lambda b: [col(lambda a: alu(1, a, b)[f], 4) for f in (1, 2, 3, 4)] + const(bitsof(b, 4), 4),
    answer=lambda b: (int(3 < b), 0x1), describe=lambda b: f"B = {b:04b} ({sv(b)})",
    B=[LCE + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח ה-", "ALU", "של שקופית 14 מחסר, ורק הדגלים בנורות:", LCE,
             "שימו", "A = 0011", "והעתיקו את הדגלים:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, b: (sum(f << (3 - i) for i, f in enumerate(alu(1, 3, b)[1:])), 0xF)),
           (["הטבלה של שקופית 14:", "signed A < B:  N ^ V", LCE, "עם", "A = 0011", ", האם", "A < B", "עם סימן?"] + UP0("כן", "לא"),
            lambda q, b: (int(3 < sv(b)), 0x1)),
           (["הטבלה של שקופית 14:", "unsigned A < B:  ~C", LCE, "עם", "A = 0011", ", האם", "A < B", "בלי סימן?"] + UP0("כן", "לא"),
            lambda q, b: (int(3 < b), 0x1))]))

# XOR (slide 15) with B on the display
LXE = "A = SW9..SW6     B = HEX3     Result = A XOR B = LEDG3..LEDG0"
W.append(Q(id="XOREX", name="XOREX", title="XOR מהשקופית", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3), hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(16)),
    tables=lambda b: [col(lambda a: ((a ^ b) >> k) & 1, 4) for k in range(4)] + const(bitsof(b, 4), 4),
    answer=lambda b: (b, 0xF), describe=lambda b: f"B = {b:04b}",
    B=[LXE + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["שקופית 15: פעולה נוספת של ה-", "ALU", ":", "Result = A XOR B", LXE,
             "שימו", "A = 1111", ". מה התוצאה?", "SW3..SW0 = Result"], lambda q, b: (~b & 15, 0xF)),
           (["איזה", "A", "נותן תוצאה אפס?", "Result = 0000", LXE, "SW3..SW0 = A"], lambda q, b: (b, 0xF))]))

# topic 2: the rotator (slide 19)
LRO = "A = HEX3     shamt = SW9 SW8 (HEX0)     A ROR shamt = LEDG7..LEDG4     A ROL shamt = LEDG3..LEDG0"
def ror(a, k):
    return ((a >> k) | (a << (4 - k))) & 15
W.append(Q(id="ROTEX", name="ROTEX", title="המסובב מהשקופית", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(4)] + [("G", 4 + i) for i in range(4)] + hexd(3), hexes=[None, None, None, [9, 8]],
    variants=list(range(1, 15)),
    tables=lambda a: [col(lambda s: (ror(a, (4 - s) % 4) >> k) & 1, 2) for k in range(4)] +
                     [col(lambda s: (ror(a, s) >> k) & 1, 2) for k in range(4)] + const(bitsof(a, 4), 2),
    answer=lambda a: (ror(a, 3), 0xF), describe=lambda a: f"A {a:04b}",
    B=[LRO + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מסובב של 4 ביטים: הביטים שיוצאים מצד אחד נכנסים מהצד השני.", "הדוגמה של שקופית 19:", "11001 ROR 2 = 01110",
             LRO, "מה", "A ROR 2", "?", "SW3..SW0"], lambda q, a: (ror(a, 2), 0xF)),
           (["הדוגמה של שקופית 19 לצד השני:", "11001 ROL 2 = 00111", LRO, "מה", "A ROL 1", "?", "SW3..SW0"],
            lambda q, a: (ror(a, 3), 0xF))]))

# shift left = multiply (slide 21), 8 bits wide
LSM8 = "A = HEX3     shamt = SW9 SW8     Y = A << shamt = LEDG7..LEDG0"
W.append(Q(id="SHMULEX", name="SHMULEX", title="הזזה שמאלה ככפל", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2) + hexd(1), hexes=[None, None, None, None],
    variants=[(a, k) for a in range(1, 16) for k in range(4)],
    tables=lambda p: [col(lambda s: ((p[0] << s) >> k) & 1, 2) for k in range(8)] +
                     const(bitsof(p[0], 4) + bitsof((p[0] << p[1]) >> 4, 4) + bitsof((p[0] << p[1]) & 15, 4), 2),
    answer=lambda p: (p[1], 0x3), describe=lambda p: f"A {p[0]}, target {p[0] << p[1]} = A << {p[1]}",
    B=[LSM8 + "     target = HEX2 HEX1 (hex)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח מזיז שמאלה של 8 ביטים, ככפל.", "הדוגמה של שקופית 21:", "00001 << 3 = 01000     (1 x 8 = 8)", LSM8,
             "שימו", "shamt = 3", ". מה", "Y", "?"] + binl(8), lambda q, p: (p[0] << 3, 0xFF)),
           (["באיזו הזזה", "Y", "שווה למספר שבתצוגה?", "Y = HEX2 HEX1 (hex)", LSM8, "SW1 SW0 = shamt"] + cnt(3, 0),
            lambda q, p: (p[1], 0x3))]))

# arithmetic shift right = divide (slide 21), 5 bits
LSA = "A = SW9..SW5     shamt = HEX3     Y = A >>> shamt = LEDG4..LEDG0"
W.append(Q(id="SRAEX", name="SRAEX", title="הזזה אריתמטית ימינה כחילוק", inputs=[9, 8, 7, 6, 5], flat=True, small=True,
    outs=[("G", i) for i in range(5)] + hexd(3), hexes=[None, None, None, None], variants=[1, 2, 3, 4],
    tables=lambda k: [col(lambda a: (((a - 32 if a >> 4 else a) >> k) >> i) & 1, 5) for i in range(5)] + const(bitsof(k, 4), 5),
    answer=lambda k: (8 >> k, 0x1F), describe=lambda k: f"shamt {k}",
    B=[LSA + "     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח מזיז אריתמטי ימינה של 5 ביטים, כחילוק.", "הדוגמה של שקופית 21:", "10000 >>> 2 = 11100     (-16 / 4 = -4)", LSA,
             "שימו", "A = 10000", "(מינוס 16). מה", "Y", "?"] + binl(5), lambda q, k: ((-16 >> k) & 31, 0x1F)),
           (["הדוגמה של שקופית 21:", "01000 >>> 1 = 00100     (8 / 2 = 4)", LSA, "שימו", "A = 01000", ". מה", "Y", "?"] + binl(5),
            lambda q, k: (8 >> k, 0x1F))]))

# the multiplier (slides 22-23) with a 2-bit B: the partial products, one at a time
LMP = "A = HEX3     B = SW9 SW8 (HEX0)     P = A x B = LEDG7..LEDG0"
W.append(Q(id="MULPPEX", name="MULPPEX", title="מכפלות חלקיות בלוח", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(8)] + hexd(3), hexes=[None, None, None, [9, 8]], variants=list(range(1, 16)),
    tables=lambda a: [col(lambda b: ((a * b) >> k) & 1, 2) for k in range(8)] + const(bitsof(a, 4), 2),
    answer=lambda a: (3 * a, 0x3F), describe=lambda a: f"A {a:04b}",
    B=[LMP + "     answer: SW5..SW0"], L=[], F=[],
    steps=[(["בלוח המכפל של שקופית 23, והמכפיל רק 2 ביטים:", LMP,
             "שקופית 22: לכל ביט 1 של", "B", "יש מכפלה חלקית, מוזזת לפי מקום הביט.", "שימו", "B = 10", ". מה", "P", "?"] + binl(6),
            lambda q, a: (2 * a, 0x3F)),
           (["שתי מכפלות חלקיות:", "B = 11:   P = A + (A << 1)", LMP, "מה", "P", "?"] + binl(6), lambda q, a: (3 * a, 0x3F))]))

# topic 3: a testvector file for the ALU (slides 5, 34): which ALUControl does the line test?
LAT = "HEX3 = A     HEX2 = B     HEX1 = Result expected"
LAT2 = "ALUControl = SW9 SW8 (HEX0)     Result = LEDG3..LEDG0"
def _alutv(r):
    a, b, op = r.randrange(16), r.randrange(16), r.randrange(4)
    rs = [alu(o, a, b)[0] for o in range(4)]
    return (a, b, op) if rs.count(rs[op]) == 1 else None
W.append(Q(id="ALUTVEX", name="ALUTVEX", title="שורה בקובץ הווקטורים של ה-ALU", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2) + hexd(1), hexes=[None, None, None, [9, 8]],
    variants=rv(207, 200, _alutv),
    tables=lambda p: [col(lambda r: (alu(r, p[0], p[1])[0] >> k) & 1, 2) for k in range(4)] +
                     const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(alu(p[2], p[0], p[1])[0], 4), 2),
    answer=lambda p: (p[2], 0x3), describe=lambda p: f"A {p[0]:04b} B {p[1]:04b} {OPS[p[2]]}",
    B=[LAT + "     " + LAT2 + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["קובץ וקטורים (שקופית 34) ל-", "ALU", "של שקופית 5. כל שורה:", "A_B_ALUControl_Result",
             "בשורה שבתצוגה חסר הקוד:", LAT, "הלוח הוא ה-", "ALU", "הנבדק:", LAT2,
             "איזה קוד נותן את התוצאה הצפויה?"] + code(["00 add", "01 subtract", "10 and", "11 or"]), lambda q, p: (p[2], 0x3))]))

# a testvector line for the 4 x 4 multiplier (slide 23): the dut on the board, sometimes wrong in that line
LMT = "HEX3 = A     HEX2 = B     HEX1 HEX0 = Pexpected (hex)"
LMT2 = "A = SW9..SW6     B = HEX2     P = LEDG7..LEDG0"
def _multv(r):
    return (r.randrange(1, 16), r.randrange(1, 16), r.randrange(2), r.randrange(8))
def _mdut(p, a):
    return a * p[1] ^ ((1 << p[3]) if p[2] and a == p[0] else 0)
W.append(Q(id="MULTVEX", name="MULTVEX", title="בדיקת המכפל עם וקטור", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None],
    variants=rv(208, 60, _multv),
    tables=lambda p: [col(lambda a: (_mdut(p, a) >> k) & 1, 4) for k in range(8)] +
                     const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof((p[0] * p[1]) >> 4, 4) + bitsof((p[0] * p[1]) & 15, 4), 4),
    answer=lambda p: (1 - p[2], 0x1), describe=lambda p: f"{p[0]} x {p[1]}, dut {'wrong (bit ' + str(p[3]) + ')' if p[2] else 'right'}",
    B=[LMT + "     " + LMT2 + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["שורה מקובץ הווקטורים של המכפל של שקופית 23:", "A_B_Pexpected", LMT, "הלוח הוא המכפל הנבדק:", LMT2,
             "שימו את", "A", "של השורה. מה ארבעת הביטים הימניים של המכפלה בלוח?", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, p: (_mdut(p, p[0]) & 15, 0xF)),
           (["הבודק משווה את", "P", "ל-", "Pexpected", ".", LMT, LMT2, "האם הבדיקה עוברת?"] + UP0("עוברת", "שגיאה"),
            lambda q, p: (1 - p[2], 0x1))]))

# a testvector line for the divider (slide 27): the dut on the board, sometimes wrong in that line
LDT = "HEX3 = A     HEX2 = B     HEX1 = Qexpected     HEX0 = Rexpected"
LDT2 = "A = SW9..SW6     B = HEX2     Q = LEDG7..LEDG4     R = LEDG3..LEDG0"
def _divtv(r):
    return (r.randrange(16), r.randrange(1, 16), r.randrange(2), r.randrange(8))
def _ddut(p, a):
    v = ((a // p[1]) << 4) | (a % p[1])
    return v ^ ((1 << p[3]) if p[2] and a == p[0] else 0)
W.append(Q(id="DIVTVEX", name="DIVTVEX", title="בדיקת המחלק עם וקטור", inputs=[9, 8, 7, 6], flat=True, small=True,
    outs=[("G", i) for i in range(8)] + hexd(3) + hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None],
    variants=rv(209, 60, _divtv),
    tables=lambda p: [col(lambda a: (_ddut(p, a) >> k) & 1, 4) for k in range(8)] +
                     const(bitsof(p[0], 4) + bitsof(p[1], 4) + bitsof(p[0] // p[1], 4) + bitsof(p[0] % p[1], 4), 4),
    answer=lambda p: (1 - p[2], 0x1), describe=lambda p: f"{p[0]} / {p[1]}, dut {'wrong (bit ' + str(p[3]) + ')' if p[2] else 'right'}",
    B=[LDT + "     " + LDT2 + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["שורה מקובץ הווקטורים של המחלק של שקופית 27:", "A_B_Qexpected_Rexpected", LDT, "הלוח הוא המחלק הנבדק:", LDT2,
             "שימו את", "A", "של השורה. מה המנה בלוח?", "SW3..SW0 = Q"], lambda q, p: (_ddut(p, p[0]) >> 4, 0xF)),
           (["הבודק משווה את", "Q", "ואת", "R", "לערכים הצפויים.", LDT, LDT2, "האם הבדיקה עוברת?"] + UP0("עוברת", "שגיאה"),
            lambda q, p: (1 - p[2], 0x1))]))

ORDER = ["ALUEX", "FLAGEX", "SLTEX", "ADDCEX", "OVFEX", "CMPEX", "XOREX",
         "ALUCODES", "ALUHIDDEN", "ZEROAND", "FLAGLEDS", "CARRYC", "OVERFLOWV", "OVFSUB", "CMPFLAGS", "FLAGFORM", "SLTFIX",
         "SHIFTEX", "MULEX", "DIVEX", "ROTEX", "SHMULEX", "SRAEX", "MULPPEX",
         "SHIFTKIND", "SHIFTSEQ", "SHIFTMUL", "SHIFTDIV", "SRADIV", "SLLNEG", "SHIFTBUG",
         "PARTIAL", "MULTHIDDEN", "ARRAYBUG", "DIVIDE", "REMHIDDEN", "DIVSTEP", "DIVARRAY",
         "SILLYEX", "VECEX", "ALUTVEX", "MULTVEX", "DIVTVEX",
         "VECLINE", "TBTIME", "TESTFAIL", "ERRORS", "TBCLOCK", "TBCOMPARE", "NVECTORS"]
TOPICS = [(40, "יחידת חישוב ודגלים", 17), (40, "הזזות, כפל וחילוק", 21), (40, "בודקים", 12)]
DESC = {"ALUEX": "ה-ALU של השקופית: חיבור, OR וחיסור",
        "ADDCEX": "המחבר שבתוך ה-ALU בחיסור: ~B ו-Cin",
        "OVFEX": "דגל הגלישה V בחיבור ובחיסור",
        "CMPEX": "הדגלים של A-B והטבלה של ההשוואות",
        "XOREX": "פעולת XOR של השקופית",
        "ROTEX": "המסובב של השקופית: ROR ו-ROL",
        "SHMULEX": "הזזה שמאלה ככפל: הדוגמה 00001 << 3",
        "SRAEX": "הזזה אריתמטית ימינה כחילוק: הדוגמה 10000 >>> 2",
        "MULPPEX": "מכפלות חלקיות במכפל שבלוח",
        "ALUTVEX": "שורה בקובץ וקטורים של ה-ALU: איזה קוד",
        "MULTVEX": "שורה בקובץ וקטורים של המכפל: עוברת או שגיאה",
        "DIVTVEX": "שורה בקובץ וקטורים של המחלק: עוברת או שגיאה",
        "FLAGEX": "הדגלים N, Z, C של השקופית",
        "SLTEX": "ה-ALU עם SLT של השקופית",
        "SHIFTEX": "הדוגמה 11001 >> 2 של השקופית במזיז שבלוח",
        "MULEX": "המכפל 4x4 של השקופית",
        "DIVEX": "הדוגמה 1101 / 0010 של השקופית במחלק שבלוח",
        "SILLYEX": "sillyfunction של השקופית בלוח",
        "VECEX": "שורה מ-example.txt של השקופית: עוברת או שגיאה",
        "ALUCODES": "הקודים של פעולות ה-ALU",
        "ALUHIDDEN": "ALU עם פעולה ומספר מוסתרים",
        "FLAGLEDS": "דגלי N Z C V בנורות בסדר מוסתר",
        "OVERFLOWV": "דגל הגלישה",
        "CMPFLAGS": "השוואה (שווה, קטן עם סימן ובלי) לפי הדגלים",
        "SLTFIX": "SLT עם תיקון הגלישה או בלי",
        "SHIFTKIND": "איזו הזזה ובכמה",
        "SHIFTMUL": "הזזה שמאלה = כפל ב-2 בחזקת N",
        "SHIFTDIV": "הזזה לוגית ימינה = חילוק שלם",
        "SRADIV": "הזזה אריתמטית ימינה של מספר שלילי",
        "PARTIAL": "מכפלות חלקיות והמכפלה",
        "MULTHIDDEN": "מכפל עם מספר מוסתר",
        "DIVIDE": "חילוק: מנה ושארית",
        "DIVSTEP": "האלגוריתם של המחלק, צעד אחרי צעד",
        "DIVARRAY": "מערך המחלק: כמה שורות",
        "VECLINE": "שורה בקובץ הווקטורים של הלוח",
        "TESTFAIL": "איזה וקטור נכשל",
        "ERRORS": "כמה הודעות שגיאה ידפיס הבודק",
        "TBCLOCK": "שעון בבודק: מחזור ועליות",
        "NVECTORS": "כמה וקטורים וכמה ביטים בכל שורה",
        "ZEROAND": "דגל האפס של AND עם מסכה מוסתרת",
        "CARRYC": "דגל הנשא בחיסור של מספר מוסתר",
        "OVFSUB": "גלישה בחיסור של מספר מוסתר עם סימן",
        "FLAGFORM": "איזו השוואה ואיזו נוסחת דגלים בנורה",
        "SHIFTSEQ": "אוגר שמזיז את עצמו: סוג ההזזה, הערך אחרי שתי עליות שעון, מתי נעצר",
        "SLLNEG": "הזזה שמאלה של מספר שלילי, וגלישה",
        "SHIFTBUG": "מזיז עם יציאה תקועה",
        "ARRAYBUG": "מכפל מערך עם שורה שבורה",
        "REMHIDDEN": "מחלק מוסתר שמראה רק שארית",
        "TBTIME": "בודק פשוט: הכניסות והיציאה בזמן נתון",
        "TBCOMPARE": "שעון הבודק: מתי נכנס ומתי נבדק וקטור"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "ALU, הזזות, כפל, חילוק ובודקים - מהקל אל הקשה, ואי אפשר בלי הלוח")
