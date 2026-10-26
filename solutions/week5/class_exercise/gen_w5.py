# -*- coding: utf-8 -*-
# Week 5 class exercise (lecture 5, Harris ch. 3.1-3.3 + 4.4: latches, flip-flops, registers, enable / reset / set,
# synchronous logic, always_ff, blocking and nonblocking). Instructor only.
#   python gen_w5.py [--compile] [--only Q05] [--id <ID>]
import itertools, math, os, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(5, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0, numq, binl, rv
rng = random.Random(505)
W = []
SW98 = code(["SW9", "SW8"])
SW987 = code(["SW9", "SW8", "SW7"])

# ================================================================ topic 1: latches and flip-flops
# SR latch: NOR (active high S, R) or NAND (active low), which switch sets
def sr_tab(p):					# p = (nand, s_is_sw8); rows = SW9 SW8; outputs Q (LEDG1), Q' (LEDG0)
    nand, s8 = p
    q_, qb = [], []
    for r in range(4):
        s, rr = ((r & 1), (r >> 1)) if s8 else ((r >> 1), (r & 1))
        if nand:
            s, rr = 1 - s, 1 - rr
        if s and rr:
            v = (1, 1) if nand else (0, 0)
        elif s:
            v = (1, 0)
        elif rr:
            v = (0, 1)
        else:
            v = (HOLD, HOLD)
        q_.append(v[0]); qb.append(v[1])
    return [qb, q_]
def sr_row(p, what):				# the row (SW9 SW8) that sets / resets / holds
    for r in range(4):
        t = sr_tab(p)
        if what == "set" and (t[1][r], t[0][r]) == (1, 0):
            return r
        if what == "reset" and (t[1][r], t[0][r]) == (0, 1):
            return r
        if what == "hold" and t[1][r] == HOLD:
            return r
VSR = [(a, b) for a in range(2) for b in range(2)]
ROWQ = ["SW1 = SW9     SW0 = SW8     (the switch positions)"]
W.append(Q(id="SRLATCH", name="SRLATCH", title="תפסן SR - מה קובע, מה מאפס?", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], None, None], variants=VSR,
    tables=sr_tab, answer=lambda p: (p[0], 0x1),
    describe=lambda p: f"{'NAND (active low)' if p[0] else 'NOR'} SR latch, S on SW{8 if p[1] else 9}",
    B=["two switches = SW9 SW8     Q = LEDG1     Q' = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח תפסן קביעה-איפוס על שני מתגים:", "SR latch:   Q = LEDG1     Q' = LEDG0",
             "באיזה מצב של שני המתגים", "Q", "נדלק (קביעה)? העתיקו את המצב:"] + ROWQ, lambda q, p: (sr_row(p, "set"), 0x3)),
           (["באיזה מצב", "Q", "נכבה (איפוס)? העתיקו את המצב:"] + ROWQ, lambda q, p: (sr_row(p, "reset"), 0x3)),
           (["באיזה מצב התפסן זוכר (הנורות לא משתנות)? העתיקו את המצב:"] + ROWQ, lambda q, p: (sr_row(p, "hold"), 0x3)),
           (["תפסן משערי", "NOR", "קובע ומאפס כשהכניסה 1, ותפסן משערי", "NAND", "כשהכניסה 0. איזה זה?"] +
            code(["NOR", "NAND"]), lambda q, p: (p[0], 0x1))]))

# D latch: which switch is CLK, which is D, transparent on CLK = 1 or 0
VDL = [(c, d, lv) for c in range(3) for d in range(3) if d != c for lv in range(2)]
def dl_tab(p):
    c, d, lv = p
    return [[((r >> (2 - d)) & 1) if ((r >> (2 - c)) & 1) == lv else HOLD for r in range(8)]]
W.append(Q(id="DLATCH", name="DLATCH", title="תפסן D - שעון ונתון", inputs=[9, 8, 7], flat=True, seq=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VDL, tables=dl_tab, answer=lambda p: (p[2], 0x1),
    describe=lambda p: f"CLK = SW{9 - p[0]}, D = SW{9 - p[1]}, transparent when CLK = {p[2]}",
    B=["SW9 SW8 SW7     Q = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח תפסן", "D", "על שניים משלושת המתגים (השלישי לא מחובר).",
             "איזה מתג הוא השעון? (כשהוא במצב אחד הנורה הולכת אחרי מתג אחר, ובמצב השני היא קפואה)"] + SW987,
            lambda q, p: (p[0], 0x3)),
           (["איזה מתג הוא הנתון (שהנורה הולכת אחריו)?"] + SW987, lambda q, p: (p[1], 0x3)),
           (["מתי התפסן שקוף (הנורה הולכת אחרי הנתון)?"] + UP0("כשהשעון למעלה", "כשהשעון למטה"), lambda q, p: (p[2], 0x1))]))

# a mix of four latches: which LED is what
KINDS = ["SR, SW9 sets", "SR, SW8 sets", "D latch, SW9 enables", "D latch, SW8 enables"]
def kind_col(k):
    out = []
    for r in range(4):
        a, b = r >> 1, r & 1
        if k == 0:
            out.append(1 if (a, b) == (1, 0) else 0 if (a, b) == (0, 1) else HOLD)
        elif k == 1:
            out.append(1 if (a, b) == (0, 1) else 0 if (a, b) == (1, 0) else HOLD)
        elif k == 2:
            out.append(b if a else HOLD)
        else:
            out.append(a if b else HOLD)
    return out
VMIX = list(itertools.permutations(range(4)))
LEDN = code(["LEDG0", "LEDG1", "LEDG2", "LEDG3"])
W.append(Q(id="LATCHMIX", name="LATCHMIX", title="ארבעה תפסנים - מי זה מי?", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", i) for i in range(4)], hexes=[[9], [8], None, None], variants=VMIX,
    tables=lambda p: [kind_col(p[i]) for i in range(4)], answer=lambda p: (p.index(3), 0x3),
    describe=lambda p: "; ".join(f"LEDG{i}: {KINDS[p[i]]}" for i in range(4)),
    B=["SW9 SW8     four latches = LEDG3..LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח ארבעה תפסנים על שני המתגים. איזו נורה היא תפסן", "SR", "ש-", "SW9", "קובע בו (מדליק)?"] + LEDN,
            lambda q, p: (p.index(0), 0x3)),
           (["איזו נורה היא תפסן", "SR", "ש-", "SW8", "קובע בו?"] + LEDN, lambda q, p: (p.index(1), 0x3)),
           (["איזו נורה היא תפסן", "D", "שהאפשור שלו", "SW9", "(והנתון", "SW8", ")?"] + LEDN, lambda q, p: (p.index(2), 0x3)),
           (["ואיזו נורה היא תפסן", "D", "שהאפשור שלו", "SW8", "?"] + LEDN, lambda q, p: (p.index(3), 0x3))]))

# ================================================================ more questions, topic 1
# an SR latch with an enable (the step from an SR latch to a D latch): which switch is EN, its level, which sets
VSRE = [(pm, lv) for pm in itertools.permutations(range(3)) for lv in range(2)]	# pm = switch index of (S, R, EN)
def sre_tab(p):
    (si, ri, ei), lv = p
    q_, qb = [], []
    for r in range(8):
        s, rr, en = [(r >> (2 - k)) & 1 for k in (si, ri, ei)]
        if en != lv or (s == 0 and rr == 0):
            v = (HOLD, HOLD)
        elif s and rr:
            v = (0, 0)
        else:
            v = (s, rr)
        q_.append(v[0]); qb.append(v[1])
    return [qb, q_]
W.append(Q(id="SRENABLE", name="SRENABLE", title="תפסן קביעה-איפוס עם אפשור", inputs=[9, 8, 7], flat=True, seq=True,
    outs=[("G", 0), ("G", 1)], hexes=[[9], [8], [7], None], variants=VSRE, tables=sre_tab,
    answer=lambda p: (p[0][0], 0x3),
    describe=lambda p: f"S = SW{9 - p[0][0]}, R = SW{9 - p[0][1]}, EN = SW{9 - p[0][2]} active {'high' if p[1] else 'low'}",
    B=["S, R, EN = SW9, SW8, SW7 (in some order)     Q = LEDG1     Q' = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח תפסן קביעה-איפוס עם אפשור על שלושה מתגים:", "S, R, EN = SW9, SW8, SW7 (in some order)",
             "Q = LEDG1     Q' = LEDG0", "איזה מתג הוא האפשור? (במצב אחד שלו הנורות קפואות, מה שלא תעשו בשני האחרים)"] + SW987,
            lambda q, p: (p[0][2], 0x3)),
           (["האפשור פעיל כשהמתג שלו", "EN"] + UP0("למעלה", "למטה"), lambda q, p: (p[1], 0x1)),
           (["כשהאפשור פעיל: איזה מתג מדליק את", "Q = LEDG1", "(קביעה)?"] + SW987, lambda q, p: (p[0][0], 0x3))]))

# the D latch inside (slide 17): S = CLK & D, R = CLK & ~D drive an SR latch
VDI = [(c8, pm) for c8 in range(2) for pm in itertools.permutations(range(3))]	# pm[i] = role on LEDGi: 0 S, 1 R, 2 Q
def di_tab(p):
    c8, pm = p
    cols = [[], [], []]
    for r in range(4):
        clk, d = ((r & 1), (r >> 1)) if c8 else ((r >> 1), (r & 1))
        val = [clk & d, clk & (1 - d), d if clk else HOLD]
        for i in range(3):
            cols[i].append(val[pm[i]])
    return cols
LED3 = code(["LEDG0", "LEDG1", "LEDG2"])
W.append(Q(id="DLATCHIN", name="DLATCHIN", title="תפסן D מבפנים", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0), ("G", 1), ("G", 2)], hexes=[[9], [8], None, None], variants=VDI, tables=di_tab,
    answer=lambda p: (p[1].index(0), 0x3),
    describe=lambda p: f"CLK = SW{8 if p[0] else 9}; " + " ".join(f"LEDG{i}={'SRQ'[p[1][i]]}" for i in range(3)),
    B=["CLK, D = SW9, SW8 (in some order)     S, R, Q = LEDG2..LEDG0 (in some order)     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח תפסן", "D", "שבנוי מתפסן קביעה-איפוס ושני שערי וגם:", "S = CLK & D     R = CLK & ~D",
             "CLK, D = SW9, SW8 (in some order)", "LEDG2 LEDG1 LEDG0 = S, R, Q (in some order)",
             "איזה מתג הוא השעון? (כשהוא למטה שום נורה לא משתנה)"] + SW98, lambda q, p: (p[0], 0x1)),
           (["איזו נורה היא היציאה", "Q", "? (היחידה שזוכרת ערך קודם)"] + LED3, lambda q, p: (p[1].index(2), 0x3)),
           (["איזו נורה היא", "S = CLK & D", "?"] + LED3, lambda q, p: (p[1].index(0), 0x3))]))

# always_latch: the enable level, d or ~d
VLC = [(lv, inv) for lv in range(2) for inv in range(2)]
W.append(Q(id="LATCHCODE", name="LATCHCODE", title="תפסן בקוד", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=VLC,
    tables=lambda p: [[(((r & 1) ^ p[1]) if (r >> 1) == p[0] else HOLD) for r in range(4)]],
    answer=lambda p: (p[0] * 2 + p[1], 0x3), describe=lambda p: f"always_latch if ({'' if p[0] else '!'}clk) q <= {'~' if p[1] else ''}d;",
    B=["clk = SW9     d = SW8     q = LEDG0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח:", "always_latch  if (?clk) q <= ?d;", "clk = SW9     d = SW8     q = LEDG0",
             "מתי התפסן שקוף?"] + UP0("כשהשעון למעלה", "כשהוא למטה"), lambda q, p: (p[0], 0x1)),
           (["כשהוא שקוף, הנורה שווה ל-", "d", "או הפוכה לו?"] + code(["d", "~d"]), lambda q, p: (p[1], 0x1)),
           (["כתבו את הקוד: שני ביטים", "SW1 = 1 if (clk), 0 if (!clk)     SW0 = 1 for ~d, 0 for d"],
            lambda q, p: (p[0] * 2 + p[1], 0x3))]))

# an inadvertent latch: if without else
CIL = ["1:  if (s) y = a; else y = b;", "2:  if (s) y = a;", "3:  if (!s) y = b;",
       "4:  if (s) y = a; else if (b) y = 0;", "5:  if (a) y = 1; else if (b) y = 0;"]
def il_col(c):
    out = []
    for r in range(8):
        s, a, b = r >> 2, (r >> 1) & 1, r & 1
        out.append([a if s else b, a if s else HOLD, HOLD if s else b,
                    a if s else (0 if b else HOLD), 1 if a else (0 if b else HOLD)][c])
    return out
LIL = ["s = SW9     a = SW8     b = SW7     y = LEDG0"]
W.append(Q(id="INFERLATCH", name="INFERLATCH", title="תפסן שנוצר בטעות", inputs=[9, 8, 7], flat=True, seq=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(5)), tables=lambda p: [il_col(p)],
    answer=lambda p: (p, 0x7), describe=lambda p: CIL[p],
    B=["s = SW9     a = SW8     b = SW7     y = LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד הקודים, בתוך", "always_comb begin ... end"] + CIL + LIL +
            ["יש בלוח תפסן? (יש מצב של המתגים שבו הנורה זוכרת ערך קודם)"] + UP0("כן", "לא"), lambda q, p: (int(p != 0), 0x1)),
           (["איזה קוד בלוח?"] + CIL + LIL + code(["1", "2", "3", "4", "5"]), lambda q, p: (p, 0x7))]))

# ================================================================ no clock button: helpers
# The only button is KEY2 (the check). Sequential ideas without a clock: latches (HOLD), the NEXT-STATE logic of a
# flip-flop / register (the state now on switches, the state after the next clock edge on LEDs), and waveforms on LEDs.
def tabf(ni, f):				# tables of a combinational view: f(*bits, MSB first) -> one value per output (outs order)
    rows = [f(*[(r >> (ni - 1 - k)) & 1 for k in range(ni)]) for r in range(1 << ni)]
    return [list(c) for c in zip(*rows)]
def val(*b):					# bits MSB first -> a number
    return sum(x << (len(b) - 1 - i) for i, x in enumerate(b))
def hx(v):					# the 4 outputs of one digit (hexd order: bit 0 first)
    return tuple(bitsof(v, 4))
NOW = "אין שעון: המצב הנוכחי על מתגים, והנורות מראות את המצב אחרי עליית השעון הבאה."
NOW2 = "אין שעון: הערך הקודם על מתג, ושתי נורות מראות את הערך עכשיו ואחרי עליית השעון הבאה."
COPY = "כדי לעבור עליית שעון אחת: העתיקו את מה שאחרי העלייה למתגי המצב, וקראו שוב."
SW87 = code(["SW8", "SW7"])

# waveforms: 8 time slots, slot 1 = the left LED (LEDR7 / LEDG7 / SW7)
def wbits(v):
    return [(v >> (7 - t)) & 1 for t in range(8)]
def wint(l):
    return sum(b << (7 - t) for t, b in enumerate(l))
def latch_w(en, d, lv=1):			# a D latch, transparent when en = lv, starts at 0
    q, out = 0, []
    for e, x in zip(wbits(en), wbits(d)):
        q = x if e == lv else q
        out.append(q)
    return wint(out)
def flop_w(c, d):				# a D flip-flop on the rising edges of c (c = 0 and q = 0 before slot 1)
    q, prev, out = 0, 0, []
    for e, x in zip(wbits(c), wbits(d)):
        q = x if (e and not prev) else q
        prev = e
        out.append(q)
    return wint(out)
def wave_vars(seed):				# clk starts at 0, at least 2 rising edges, d never changes at a rising edge
    def f(r):
        c, d = r.randrange(256), r.randrange(256)
        cb, db = wbits(c), wbits(d)
        ups = [t for t in range(1, 8) if cb[t] and not cb[t - 1]]
        if cb[0] or len(ups) < 2 or any(db[t] != db[t - 1] for t in ups):
            return None
        return (c, d)
    return rv(seed, 200, f)
OWAVE = [("R", i) for i in range(8)] + [("G", i) for i in range(8)]
SLOTS = "SW7..SW0 = Q at times 1..8"

# ================================================================ topic 1: latches and flip-flops
# a D flip-flop: which switch is D, Q or Q' (the LED = the value after the next clock edge)
VDF = [(d, inv) for d in range(3) for inv in range(2)]
LDF = ["SW9 SW8 SW7     LEDG0 = the output after the next clock edge"]
W.append(Q(id="DFF", name="DFF", title="דלגלג D", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=VDF,
    tables=lambda p: tabf(3, lambda *b: (b[p[0]] ^ p[1],)),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"D = SW{9 - p[0]}, LED = {'Q' + chr(39) if p[1] else 'Q'} after the edge",
    B=[LDF[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג", "D", "על אחד משלושת המתגים (השניים האחרים לא מחוברים).",
             "אין שעון: הנורה מראה את היציאה אחרי עליית השעון הבאה."] + LDF +
            ["איזה מתג הוא הנתון? (רק הוא משנה את הנורה)"] + SW987, lambda q, p: (p[0], 0x3)),
           (["הנורה מראה את היציאה או את ההפוכה שלה? השוו אותה למתג הנתון."] + LDF + code(["Q", "Q'"]),
            lambda q, p: (p[1], 0x1))]))

# a latch and a flip-flop on the same waveform
LWV = ["CLK = LEDR7..LEDR0     D = LEDG7..LEDG0     (time 1 = the left LED)"]
W.append(Q(id="LATCHFF", name="LATCHFF", title="תפסן מול דלגלג - צורת גל", inputs=[9], flat=True,
    outs=OWAVE, hexes=[None, None, None, None], variants=wave_vars(57),
    tables=lambda p: const(bitsof(p[0], 8) + bitsof(p[1], 8)), answer=lambda p: (flop_w(*p), 0xFF),
    describe=lambda p: f"CLK {p[0]:08b} D {p[1]:08b}: latch {latch_w(*p):08b}, flop {flop_w(*p):08b}",
    B=[LWV[0] + "     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח צורת גל של שעון ונתון, בשמונה זמנים משמאל לימין:"] + LWV +
            ["לפני זמן 1 השעון 0 והיציאה 0.", "מה היציאה של תפסן", "D", "(שקוף כשהשעון 1) בכל זמן?", SLOTS],
            lambda q, p: (latch_w(*p), 0xFF)),
           (["ומה היציאה של דלגלג", "D", "(דוגם את הנתון רק כשהשעון עולה מ-0 ל-1) בכל זמן?"] + LWV +
            ["לפני זמן 1 השעון 0 והיציאה 0.", SLOTS], lambda q, p: (flop_w(*p), 0xFF))]))

# a flip-flop = two latches (master transparent when CLK = 0, slave when CLK = 1)
def ms_w(c, d):
    n1 = latch_w(c, d, 0)
    return n1, latch_w(c, n1, 1)
assert all(ms_w(*p)[1] == flop_w(*p) for p in wave_vars(58))
W.append(Q(id="MASTERSLAVE", name="MASTERSLAVE", title="דלגלג משני תפסנים", inputs=[9], flat=True,
    outs=OWAVE, hexes=[None, None, None, None], variants=wave_vars(58),
    tables=lambda p: const(bitsof(p[0], 8) + bitsof(p[1], 8)), answer=lambda p: (ms_w(*p)[1], 0xFF),
    describe=lambda p: f"CLK {p[0]:08b} D {p[1]:08b}: N1 {ms_w(*p)[0]:08b}, Q {ms_w(*p)[1]:08b}",
    B=[LWV[0] + "     answer: SW7..SW0"], L=[], F=[],
    steps=[(["דלגלג בנוי משני תפסנים בטור: הראשון שקוף כשהשעון 0, והשני שקוף כשהשעון 1.",
             "D -> L1 -> N1 -> L2 -> Q", "בלוח צורת גל של שעון ונתון, בשמונה זמנים משמאל לימין:"] + LWV +
            ["לפני זמן 1 שני התפסנים 0.", "מה היציאה של התפסן הראשון בכל זמן?", "SW7..SW0 = N1 at times 1..8"],
            lambda q, p: (ms_w(*p)[0], 0xFF)),
           (["ומה היציאה של התפסן השני (שקוף כשהשעון 1, והנתון שלו הוא היציאה של הראשון)?",
             "D -> L1 -> N1 -> L2 -> Q"] + LWV + ["לפני זמן 1 שני התפסנים 0.", SLOTS],
            lambda q, p: (ms_w(*p)[1], 0xFF))]))

# state: how many bits for N states, how many states in k bits
numq(W, "STATEBITS", "כמה מצבים, כמה ביטים?", 3, rv(56, 200, lambda r: (r.randint(2, 40), r.randint(1, 8))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1]]], "HEX3 HEX2 = N states (decimal)     HEX1 = k bits",
     [(["למעגל יש", "N", "מצבים. כמה ביטים של מצב צריך לפחות כדי לזכור אותם?", "HEX3 HEX2 = N (decimal)"] + cnt(6),
       lambda q, p: ((p[0] - 1).bit_length(), 0x7)),
      (["וכמה מצבים לכל היותר אפשר לזכור בעזרת", "k", "ביטים?", "HEX1 = k"] + binl(9), lambda q, p: (1 << p[1], 0x1FF))],
     lambda p: f"{p[0]} states -> {(p[0] - 1).bit_length()} bits; {p[1]} bits -> {1 << p[1]} states")

# a ring of inverters: bistable (even) or oscillating (odd), the period
numq(W, "OSCRING", "טבעת של מהפכים - יציבה או מתנדנדת?", 3, [(n, t) for n in range(1, 9) for t in range(1, 21)],
     lambda p: [[p[0], p[1] // 10, p[1] % 10]], "HEX3 = N inverters     HEX2 HEX1 = tpd (ns, decimal)",
     [(["בלוח טבעת של מהפכים: היציאה של כל מהפך היא הכניסה של הבא.", "HEX3 = N inverters",
        "האם הטבעת מתנדנדת בלי סוף?"] + UP0("כן", "לא"), lambda q, p: (p[0] & 1, 0x1)),
      (["מה זמן המחזור של הנדנוד, בננו-שניות? אם הטבעת יציבה - השאירו הכל למטה.",
        "HEX3 = N inverters     HEX2 HEX1 = tpd of one inverter (ns, decimal)", "T = 2 N tpd"] + binl(9),
       lambda q, p: (2 * p[0] * p[1] if p[0] & 1 else 0, 0x1FF))],
     lambda p: f"{p[0]} inverters, tpd {p[1]}: " + (f"T = {2 * p[0] * p[1]}" if p[0] & 1 else "stable"))

# ================================================================ topic 2: enable, reset, set, registers (next state)
def two(p0, a, b):				# two hidden roles on SW8, SW7: p0 = 0 -> (SW8, SW7), 1 -> (SW7, SW8)
    return (a, b) if p0 == 0 else (b, a)

# enable: which switch, active high or low
LEN = ["Q = SW9 (now)     EN, D = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge"]
W.append(Q(id="ENABLE", name="ENABLE", title="דלגלג עם אפשור", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=[(e, lv) for e in range(2) for lv in range(2)],
    tables=lambda p: tabf(3, lambda q_, a, b: ((lambda en, d: d if en == p[1] else q_)(*two(p[0], a, b)),)),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"EN = SW{8 - p[0]} active {'high' if p[1] else 'low'}",
    B=[LEN[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג עם אפשור: בעליית השעון הוא שומר נתון חדש רק כשהאפשור פעיל.", NOW] + LEN +
            ["איזה מתג הוא האפשור? (כשהוא לא פעיל, הנורה שווה למצב הנוכחי)"] + SW87, lambda q, p: (p[0], 0x1)),
           (LEN + ["מתי האפשור פעיל?"] + UP0("כשהמתג שלו למעלה", "כשהוא למטה"), lambda q, p: (p[1], 0x1))]))

# reset: which switch, synchronous or asynchronous
LRS = ["Q = SW9 (before)     Reset, D = SW8, SW7 (in some order)", "LEDG1 = Q now     LEDG0 = Q after the next clock edge"]
def rs_f(p):
    def f(q_, a, b):
        rs, d = two(p[0], a, b)
        return (0 if (rs and not p[1]) else q_, 0 if rs else d)
    return f
W.append(Q(id="RESETSYNC", name="RESETSYNC", title="איפוס סינכרוני או אסינכרוני", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=[(r_, sy) for r_ in range(2) for sy in range(2)],
    tables=lambda p: tabf(3, rs_f(p)), answer=lambda p: (1 - p[1], 0x1),
    describe=lambda p: f"Reset = SW{8 - p[0]}, {'synchronous' if p[1] else 'asynchronous'}",
    B=["   ".join(LRS) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג עם איפוס (איפוס = 1).", NOW2] + LRS +
            ["איזה מתג הוא האיפוס? (הוא מכבה את הנורה של אחרי העלייה)"] + SW87, lambda q, p: (p[0], 0x1)),
           (["הרימו את הערך הקודם ואת האיפוס. האם הנורה של עכשיו כבתה מיד, עוד לפני עליית השעון?"] + LRS +
            ["asynchronous = at once     synchronous = at the next clock edge"] + UP0("כבתה מיד", "נשארה דולקת"),
            lambda q, p: (1 - p[1], 0x1))]))

# set and reset together: which wins
LSE = ["Q = SW9 (now)     Set, Reset = SW8, SW7 (in some order)     LEDG0 = Q after the next clock edge"]
def se_f(p):
    def f(q_, a, b):
        st_, rs = two(p[0], a, b)
        if st_ and rs:
            return (1 - p[1],)
        return (1 if st_ else 0 if rs else q_,)
    return f
W.append(Q(id="SETRESET", name="SETRESET", title="קביעה ואיפוס - מי מנצח?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=[(se, w) for se in range(2) for w in range(2)],
    tables=lambda p: tabf(3, se_f(p)), answer=lambda p: (p[1], 0x1),
    describe=lambda p: f"Set = SW{8 - p[0]}, {'reset' if p[1] else 'set'} wins",
    B=[LSE[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג עם קביעה ואיפוס סינכרוניים (פועלים בעליית השעון).", NOW] + LSE +
            ["איזה מתג הוא הקביעה (מדליק)?"] + SW87, lambda q, p: (p[0], 0x1)),
           (LSE + ["הרימו את שניהם. מי מנצח?"] + code(["Set", "Reset"]), lambda q, p: (p[1], 0x1))]))

# a toggle flip-flop
LTG = ["Q = SW9 (now)     T = SW8 or SW7 (the other is not connected)     LEDG0 = Q after the next clock edge"]
W.append(Q(id="TOGGLE", name="TOGGLE", title="דלגלג שמתהפך", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=[(t, lv) for t in range(2) for lv in range(2)],
    tables=lambda p: tabf(3, lambda q_, a, b: (q_ ^ int(two(p[0], a, b)[0] == p[1]),)),
    answer=lambda p: (p[1], 0x1), describe=lambda p: f"T = SW{8 - p[0]} active {'high' if p[1] else 'low'}",
    B=[LTG[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג עם משוב:", "q <= q ^ T", "כשהכניסה פעילה, כל עליית שעון הופכת את היציאה.", NOW] + LTG +
            ["איזה מתג הוא הכניסה?"] + SW87, lambda q, p: (p[0], 0x1)),
           (LTG + ["מתי הכניסה פעילה?"] + UP0("כשהמתג שלה למעלה", "כשהוא למטה"), lambda q, p: (p[1], 0x1))]))

# a 4-bit register, wired in a hidden order
VRP = list(itertools.permutations(range(4)))
LRP = ["D[3:0] = SW9..SW6 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge"]
REGNOW = "אין שעון: הנורות מראות את האוגר אחרי עליית השעון הבאה."
W.append(Q(id="REGPERM", name="REGPERM", title="אוגר של 4 ביטים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VRP,
    tables=lambda p: tabf(4, lambda *b: tuple(b[3 - p[i]] for i in range(4))),
    answer=lambda p: (1 << p.index(1), 0xF), describe=lambda p: " ".join(f"Q{i}=D{p[i]}" for i in range(4)),
    B=[LRP[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר של 4 ביטים, אבל החוטים מעורבבים.", REGNOW] + LRP +
            ["שימו", "D = 1000", "והעתיקו את הנורות:", "SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (1 << p.index(3), 0xF)),
           (["עכשיו", "D = 0100", "והעתיקו:"] + LRP + ["SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (1 << p.index(2), 0xF)),
           (["ועכשיו", "D = 0010", "והעתיקו:"] + LRP + ["SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (1 << p.index(1), 0xF))]))

# a 4-bit register: some flip-flops are settable, some resettable, all on one switch
LRI4 = ["D[3:0] = SW9..SW6 (HEX0)     set/reset = SW5     LEDG3..LEDG0 = Q after the next clock edge"]
W.append(Q(id="REGINIT", name="REGINIT", title="אוגר עם קביעה ואיפוס", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(16)),
    tables=lambda p: tabf(5, lambda d3, d2, d1, d0, s: hx(p if s else val(d3, d2, d1, d0))),
    answer=lambda p: (p, 0xF), describe=lambda p: f"SW5 loads {p:04b} (1 = settable flip-flop)",
    B=[LRI4[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר של 4 ביטים. בחלק מהדלגלגים יש קביעה ובחלק איפוס, וכולם מחוברים לאותו מתג (סינכרוני).",
             REGNOW] + LRI4 + ["שימו", "D = 0000     SW5 = 1", "כמה נורות דולקות? (כמה דלגלגים עם קביעה)"] + cnt(4, start=0),
            lambda q, p: (bin(p).count("1"), 0x7)),
           (["אילו דלגלגים עם קביעה? הרימו את מתג הקביעה-איפוס, והעתיקו את הנורות:"] + LRI4 +
            ["SW3..SW0 = LEDG3..LEDG0"], lambda q, p: (p, 0xF))]))

# registers in series: a waveform of the switch and of the LED, how many flip-flops, inverted or not
def pipe_q(d, k, inv):
    db = wbits(d)
    return wint([(db[t - k] if t >= k else 0) ^ inv for t in range(8)])
def pipe_v(r):
    d, k, inv = r.randrange(1, 256), r.randint(1, 4), r.randrange(2)
    ok = [(k2, i2) for k2 in range(1, 5) for i2 in range(2) if pipe_q(d, k2, i2) == pipe_q(d, k, inv)]
    return (d, k, inv) if ok == [(k, inv)] else None
LPI = ["D = LEDR7..LEDR0     Q = LEDG7..LEDG0     (cycle 1 = the left LED)"]
W.append(Q(id="PIPE", name="PIPE", title="אוגרים בטור", inputs=[9], flat=True,
    outs=OWAVE, hexes=[None, None, None, None], variants=rv(59, 200, pipe_v),
    tables=lambda p: const(bitsof(p[0], 8) + bitsof(pipe_q(*p), 8)), answer=lambda p: (p[2], 0x1),
    describe=lambda p: f"D {p[0]:08b}, {p[1]} flip-flops, {'inverted' if p[2] else 'not inverted'}",
    B=[LPI[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בין מתג לנורה יש כמה דלגלגים בטור, עם שעון משותף.",
             "בלוח צורת גל: הנתון בכניסה והיציאה בסוף השרשרת, בכל מחזור שעון משמאל לימין."] + LPI +
            ["לפני מחזור 1 כל הדלגלגים 0.", "כמה דלגלגים יש בטור? (בכמה מחזורים היציאה מאחרת)"] + cnt(4),
            lambda q, p: (p[1], 0xF)),
           (["בסוף השרשרת יש מהפך?"] + LPI + ["לפני מחזור 1 כל הדלגלגים 0."] + UP0("כן", "לא"), lambda q, p: (p[2], 0x1))]))

# a shift register: which switch is the serial input, which end, inverted or not
VSH = [(i, d, v) for i in range(2) for d in range(2) for v in range(2)]
def sh_f(p):
    def f(q3, q2, q1, q0, a, b):
        s, bit = val(q3, q2, q1, q0), (a if p[0] == 0 else b) ^ p[2]
        return hx(((s << 1) | bit) & 15 if p[1] == 0 else (s >> 1) | (bit << 3))
    return f
LSH = ["Q[3:0] = SW9..SW6 (now, HEX0)     serial in = SW5 or SW4", "LEDG3..LEDG0 = Q after the next clock edge"]
W.append(Q(id="SHIFTREG", name="SHIFTREG", title="אוגר הזזה", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VSH,
    tables=lambda p: tabf(6, sh_f(p)), answer=lambda p: (p[2], 0x1),
    describe=lambda p: f"serial in = SW{5 - p[0]}, enters at LEDG{3 * p[1]}, {'inverted' if p[2] else 'not inverted'}",
    B=["   ".join(LSH) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר הזזה: בכל עליית שעון כל ביט זז מקום אחד, וביט חדש נכנס מאחד המתגים.", NOW] + LSH +
            ["איזה מתג הוא הכניסה?"] + code(["SW5", "SW4"]), lambda q, p: (p[0], 0x1)),
           (["באיזו נורה נכנס הביט החדש?"] + LSH + code(["LEDG0", "LEDG3"]), lambda q, p: (p[1], 0x1)),
           (["יש מהפך בכניסה? (נכנס 1 כשמתג הכניסה למטה)"] + LSH + UP0("כן", "לא"), lambda q, p: (p[2], 0x1))]))

# a ring of flip-flops (a plain ring or a twisted ring): how many flip-flops, how many states
VRI = [(n, tw) for n in range(2, 5) for tw in range(2)]
def ring_f(p):
    n, tw = p
    def f(*b):
        s = val(*b) & ((1 << n) - 1)
        return hx(((s << 1) | (((s >> (n - 1)) & 1) ^ tw)) & ((1 << n) - 1))
    return f
LRI = ["Q[3:0] = SW9..SW6 (now, HEX0)     LEDG3..LEDG0 = Q after the next clock edge"]
W.append(Q(id="RING", name="RING", title="טבעת של דלגלגים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VRI,
    tables=lambda p: tabf(4, ring_f(p)), answer=lambda p: (p[0] * (2 if p[1] else 1), 0xF),
    describe=lambda p: f"{p[0]} flip-flops, {'twisted (Johnson)' if p[1] else 'plain'} ring",
    B=[LRI[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח כמה דלגלגים שמחוברים בטבעת: היציאה של כל אחד היא הכניסה של הבא.", NOW] + LRI +
            ["כמה דלגלגים יש? (הנורות של שאר הביטים תמיד כבויות)"] + cnt(4, start=2), lambda q, p: (p[0], 0x7)),
           (["האם הביט שחוזר מהסוף להתחלה עובר מהפך? (טבעת מפותלת)"] + LRI + UP0("כן", "לא"), lambda q, p: (p[1], 0x1)),
           (["התחילו מ-", "Q = 0001", "בטבעת רגילה, או מ-", "Q = 0000", "בטבעת מפותלת.", COPY] + LRI +
            ["אחרי כמה עליות שעון התבנית חוזרת להתחלה?"] + cnt(8), lambda q, p: (p[0] * (2 if p[1] else 1), 0xF))]))

# an accumulator: a register with an adder in the feedback loop
LAC = ["q = SW9..SW6 (now, HEX0)     HEX1 = q after the next clock edge"]
W.append(Q(id="ACCUM", name="ACCUM", title="אוגר עם משוב דרך מחבר", inputs=[9, 8, 7, 6], flat=True,
    outs=hexd(1), hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(1, 10)),
    tables=lambda p: tabf(4, lambda *b: hx((val(*b) + p) % 10)),
    answer=lambda p: (10 // math.gcd(p, 10), 0xF), describe=lambda p: f"q <= (q + {p}) % 10",
    B=[LAC[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר של ספרה, ומחבר במשוב מהיציאה שלו לכניסה שלו:", "always_ff @(posedge clk)  q <= (q + K) % 10;", NOW] +
            LAC + ["שימו", "q = 0", "מה", "K", "?"] + cnt(9), lambda q, p: (p, 0xF)),
           (["מתחילים מאפס. אחרי כמה עליות שעון חוזרים לאפס?", COPY] + LAC + cnt(10),
            lambda q, p: (10 // math.gcd(p, 10), 0xF))]))

# ================================================================ topic 3: always_ff, always_latch, blocking / nonblocking
# always_comb or always_ff
VCF = [(ff, g) for ff in range(2) for g in range(6)]
GT = G.GATES
LCF = ["a = SW9     b = SW8     y before = SW7", "LEDG1 = y now     LEDG0 = y after the next clock edge"]
W.append(Q(id="COMBORFF", name="COMBORFF", title="צירופי או סדרתי?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=VCF,
    tables=lambda p: tabf(3, lambda a, b, y: (y if p[0] else GT[p[1]][1][2 * a + b], GT[p[1]][1][2 * a + b])),
    answer=lambda p: (p[1], 0x7), describe=lambda p: f"{'always_ff' if p[0] else 'always_comb'} y = {GT[p[1]][0]}(a, b)",
    B=["   ".join(LCF) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד מהשניים:", "always_comb                y = a ? b;", "always_ff @(posedge clk)   y <= a ? b;", NOW2] + LCF +
            ["האם הנורה של עכשיו משתנה רק בעליית השעון (ולא מיד כשמשנים את המתגים)?"] + UP0("רק בעליית השעון", "מיד"),
            lambda q, p: (p[0], 0x1)),
           (["איזה שער? הסתכלו על הנורה של אחרי העלייה."] + LCF +
            ["AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"], lambda q, p: (p[1], 0x7))]))

# flopr: synchronous or asynchronous reset, the reset value
CFR = ["A:  always_ff @(posedge clk)              if (reset) q <= R; else q <= d;",
       "B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= d;"]
LFR = ["reset = SW9     d = SW8     q before = SW7", "LEDG1 = q now     LEDG0 = q after the next clock edge"]
W.append(Q(id="FLOPR", name="FLOPR", title="דלגלג עם איפוס בקוד", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=[(asy, v) for asy in range(2) for v in range(2)],
    tables=lambda p: tabf(3, lambda rs, d, q_: (p[1] if (p[0] and rs) else q_, p[1] if rs else d)),
    answer=lambda p: (p[0], 0x1), describe=lambda p: f"{'asynchronous' if p[0] else 'synchronous'} reset to {p[1]}",
    B=["   ".join(LFR) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד משני הקודים:"] + CFR + [NOW2] + LFR +
            ["הרימו את האיפוס. מה הערך שהאיפוס טוען?", "R = ?"] + UP0("1", "0"), lambda q, p: (p[1], 0x1)),
           (["איזה קוד? בדקו: האם האיפוס משנה את הנורה של עכשיו, עוד לפני עליית השעון?"] + CFR + LFR + code(["A", "B"]),
            lambda q, p: (p[0], 0x1))]))

# flopren: the order of reset and enable
CFE = ["A:  always_ff @(posedge clk)  if (reset) q <= 0; else if (en) q <= d;",
       "B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else if (en) q <= d;",
       "C:  always_ff @(posedge clk)  if (en) begin if (reset) q <= 0; else q <= d; end"]
def fe_next(p, rs, en, d, q_):
    if p in (0, 1):
        return 0 if rs else (d if en else q_)
    return (0 if rs else d) if en else q_
LFE = ["reset = SW9     en = SW8     d = SW7     q before = SW6", "LEDG1 = q now     LEDG0 = q after the next clock edge"]
W.append(Q(id="FLOPREN", name="FLOPREN", title="איפוס ואפשור - באיזה סדר?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], [6]], variants=list(range(3)),
    tables=lambda p: tabf(4, lambda rs, en, d, q_: (0 if (p == 1 and rs) else q_, fe_next(p, rs, en, d, q_))),
    answer=lambda p: (p, 0x3), describe=lambda p: CFE[p][:2],
    B=["   ".join(LFE) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד משלושת הקודים:"] + CFE + [NOW2] + LFE +
            ["הרימו את הערך הקודם ואת האיפוס, והורידו את האפשור. הנורה של אחרי העלייה כבתה?"] + UP0("כבתה", "נשארה דולקת"),
            lambda q, p: (int(p != 2), 0x1)),
           (["איזה קוד בלוח? בדקו גם את הנורה של עכשיו כשהאיפוס למעלה."] + CFE + LFE + code(["A", "B", "C"]),
            lambda q, p: (p, 0x3))]))

# a flip-flop with a case: which sel value does which action
OPSN = ["q <= d;", "q <= ~q;", "q <= 0;", "q <= q;"]
SELS = code(["00", "01", "10", "11"])
LFO = ["always_ff @(posedge clk)  case (sel)  2'b00: ...  2'b01: ...  2'b10: ...  2'b11: ...  endcase",
       "the four actions (in a hidden order):   q <= d;   q <= ~q;   q <= 0;   q <= q;",
       "sel = SW9 SW8     d = SW7     q before = SW6     LEDG0 = q after the next clock edge"]
W.append(Q(id="FFOPS", name="FFOPS", title="דלגלג עם ארבע פעולות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=list(itertools.permutations(range(4))),
    tables=lambda p: tabf(4, lambda s1, s0, d, q_: ([d, 1 - q_, 0, q_][p[2 * s1 + s0]],)),
    answer=lambda p: (p.index(0), 0x3), describe=lambda p: "  ".join(f"{v:02b}: {OPSN[p[v]]}" for v in range(4)),
    B=[LFO[2] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח דלגלג שהפעולה שלו נבחרת לפי", "sel", NOW2] + LFO + ["איזה ערך של", "sel", "הופך את היציאה?"] + SELS,
            lambda q, p: (p.index(1), 0x3)),
           (["איזה ערך שומר את היציאה כמו שהיא? הרימו קודם את הערך הקודם - אחרת אי אפשר להבדיל מאיפוס."] + LFO + SELS,
            lambda q, p: (p.index(3), 0x3)),
           (["איזה ערך טוען את הנתון?"] + LFO + SELS, lambda q, p: (p.index(0), 0x3))]))

# a counter with a reset value R: R, synchronous or asynchronous, edges back to 0
VCR = [(r_, a) for r_ in range(1, 16) for a in range(2)]
CCR = ["A:  always_ff @(posedge clk)  if (reset) q <= R; else q <= q + 1;",
       "B:  always_ff @(posedge clk, posedge reset)  if (reset) q <= R; else q <= q + 1;"]
LCR = ["reset = SW9     q before = SW8..SW5 (HEX0)", "HEX3 = q now     HEX2 = q after the next clock edge"]
def cr_f(p):
    def f(rs, *b):
        v = val(*b)
        return hx(p[0] if (p[1] and rs) else v) + hx(p[0] if rs else (v + 1) & 15)
    return f
W.append(Q(id="COUNTR", name="COUNTR", title="מונה עם ערך איפוס", inputs=[9, 8, 7, 6, 5], flat=True, small=True,
    outs=hexd(3) + hexd(2), hexes=[None, None, None, [8, 7, 6, 5]], variants=VCR,
    tables=lambda p: tabf(5, cr_f(p)),
    answer=lambda p: (16 - p[0], 0xF), describe=lambda p: f"{'B (asynchronous)' if p[1] else 'A (synchronous)'}, R = {p[0]:X}",
    B=["   ".join(LCR) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מונה של 4 ביטים עם איפוס לערך", "R", "(ולא לאפס).",
             "אין שעון: הערך הקודם על מתגים, והתצוגה מראה את המונה עכשיו ואחרי עליית השעון הבאה."] + LCR +
            ["הרימו את האיפוס. מה", "R", "? (בבינארי)"] + BIN4, lambda q, p: (p[0], 0xF)),
           (["בלוח אחד הקודים:"] + CCR + LCR +
            ["האם האיפוס משנה את המונה של עכשיו, עוד לפני עליית השעון? איזה קוד?"] + code(["A", "B"]),
            lambda q, p: (p[1], 0x1)),
           (["הורידו את האיפוס. אחרי כמה עליות שעון מהערך", "R", "המונה מגיע לאפס?", COPY] + LCR + cnt(15),
            lambda q, p: (16 - p[0], 0xF))]))

# blocking and nonblocking: the values after one clock edge, how many edges from d to q
CBL = ["1:  n1 <= d; q <= n1;", "2:  q <= n1; n1 <= d;", "3:  n1 = d; q = n1;", "4:  q = n1; n1 = d;"]
DBL = [2, 2, 1, 2]
LBL = ["d = SW9     n1 before = SW8     q before = SW7", "LEDG1 = n1 after one clock edge     LEDG0 = q after one clock edge"]
ONE = "אין שעון: הערכים הקודמים על מתגים, והנורות מראות אותם אחרי עליית שעון אחת."
W.append(Q(id="BLOCKING", name="BLOCKING", title="השמה חוסמת ולא חוסמת", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(4)),
    tables=lambda p: tabf(3, lambda d, n1, q_: (d, d if DBL[p] == 1 else n1)),
    answer=lambda p: (sum(1 << k for k in range(4) if DBL[k] == DBL[p]), 0xF), describe=lambda p: CBL[p],
    B=["   ".join(LBL) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד מארבעת הקודים, בתוך", "always_ff @(posedge clk) begin ... end"] + CBL + [ONE] + LBL +
            ["מאיפה היציאה מקבלת את הערך שלה?"] + code(["n1 before", "d"]), lambda q, p: (int(DBL[p] == 1), 0x1)),
           (["אחרי כמה עליות שעון שינוי בנתון מגיע ליציאה?"] + LBL + cnt(2), lambda q, p: (DBL[p], 0x3)),
           (["אילו מהקודים מתנהגים כך? הרימו מתג לכל קוד מתאים:"] + CBL + ["1 -> SW0     2 -> SW1     3 -> SW2     4 -> SW3"],
            lambda q, p: (sum(1 << k for k in range(4) if DBL[k] == DBL[p]), 0xF))]))

# swap with nonblocking, or the blocking mistake
CSW = ["1:  a <= b; b <= a;", "2:  a = b; b = a;", "3:  b = a; a = b;"]
def sw_after(c, a, b):
    return [(b, a), (b, b), (a, a)][c]
LSW = ["a before = SW9     b before = SW8", "LEDG1 = a after one clock edge     LEDG0 = b after one clock edge"]
W.append(Q(id="NBSWAP", name="NBSWAP", title="החלפה בין שני אוגרים", inputs=[9, 8], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], None, None], variants=list(range(3)),
    tables=lambda p: tabf(2, lambda a, b: sw_after(p, a, b)),
    answer=lambda p: (p, 0x3), describe=lambda p: CSW[p],
    B=["   ".join(LSW) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שני אוגרים, ואחד הקודים בתוך", "always_ff @(posedge clk) begin ... end"] + CSW + [ONE] + LSW +
            ["שימו", "a = 1     b = 0", "והעתיקו את הנורות:", "SW1 SW0 = LEDG1 LEDG0"], lambda q, p: (val(*sw_after(p, 1, 0)), 0x3)),
           (["עכשיו", "a = 0     b = 1", "והעתיקו:"] + LSW + ["SW1 SW0 = LEDG1 LEDG0"], lambda q, p: (val(*sw_after(p, 0, 1)), 0x3)),
           (["איזה קוד בלוח?"] + CSW + code(["1", "2", "3"]), lambda q, p: (p, 0x3))]))

# a 4-bit register with a concatenation: shift or rotate, which way
CCC = ["1:  q <= {q[2:0], d};", "2:  q <= {d, q[3:1]};", "3:  q <= {q[2:0], q[3]};", "4:  q <= {q[0], q[3:1]};"]
def cc_f(c):
    def f(d, *b):
        a = val(*b)
        return hx([((a << 1) | d) & 15, (a >> 1) | (d << 3), ((a << 1) | (a >> 3)) & 15, (a >> 1) | ((a & 1) << 3)][c])
    return f
LCC = ["d = SW9     q[3:0] before = SW8..SW5 (HEX0)", "LEDG3..LEDG0 = q after one clock edge"]
W.append(Q(id="CONCAT", name="CONCAT", title="הזזה וסיבוב בשרשור", inputs=[9, 8, 7, 6, 5], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [8, 7, 6, 5]], variants=list(range(4)),
    tables=lambda p: tabf(5, cc_f(p)), answer=lambda p: (p, 0x3), describe=lambda p: CCC[p],
    B=["   ".join(LCC) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר של 4 ביטים עם אחד הקודים, בתוך", "always_ff @(posedge clk)"] + CCC + [ONE] + LCC +
            ["הזזה או סיבוב? בסיבוב הנתון לא משפיע, והביט שיוצא חוזר מהצד השני."] + code(["shift", "rotate"]),
            lambda q, p: (int(p >= 2), 0x1)),
           (["לאיזה כיוון הביטים זזים?"] + LCC + code(["LEDG0 -> LEDG3", "LEDG3 -> LEDG0"]), lambda q, p: (p & 1, 0x1)),
           (["איזה קוד בלוח?"] + CCC + LCC + code(["1", "2", "3", "4"]), lambda q, p: (p, 0x3))]))

# which module from the slides is on the board
MODS = ["flop", "flopr", "flopren", "latch"]
CWM = ["flop:     always_ff @(posedge clk) q <= d;",
       "flopr:    always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else q <= d;",
       "flopren:  always_ff @(posedge clk, posedge reset) if (reset) q <= 0; else if (en) q <= d;",
       "latch:    always_latch if (clk) q <= d;     (clk = SW7, both LEDs show the latch)"]
LWM = ["reset = SW9     d = SW8     en (or the latch clk) = SW7     q before = SW6",
       "LEDG1 = q now     LEDG0 = q after the next clock edge"]
def wm_f(p):
    def f(rs, d, en, q_):
        if p == 3:
            v = d if en else HOLD
            return (v, v)
        now = 0 if (p and rs) else q_
        if p == 0:
            return (now, d)
        if p == 1:
            return (now, 0 if rs else d)
        return (now, 0 if rs else (d if en else q_))
    return f
W.append(Q(id="WHICHMOD", name="WHICHMOD", title="איזה מודול מהשקופיות?", inputs=[9, 8, 7, 6], flat=True, seq=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], [6]], variants=list(range(4)),
    tables=lambda p: tabf(4, wm_f(p)), answer=lambda p: (p, 0x3), describe=lambda p: MODS[p],
    B=["   ".join(LWM) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אחד המודולים מהשקופיות:"] + CWM + [NOW2] + LWM +
            ["האם הנורה של עכשיו הולכת אחרי הנתון כשמתג האפשור למעלה, גם כשלא נוגעים בערך הקודם?"] + UP0("כן", "לא"),
            lambda q, p: (int(p == 3), 0x1)),
           (["איזה מודול?"] + CWM + LWM + code(MODS), lambda q, p: (p, 0x3))]))

# ================================================================ EASY questions: the circuits of the slides, at the start of each topic
SW1SW0 = ["SW1 SW0 = LEDG1 LEDG0"]
SW3SW0 = ["SW3..SW0 = LEDG3..LEDG0"]

# topic 1, slides 11-14: the SR latch of two NOR gates; the board shows two cases (S R) to set one after the other
SRV = {2: (1, 0), 1: (0, 1), 3: (0, 0)}			# case S*2+R -> (Q, Q'); 0 = memory
VSRN = [(c1, c2) for c1 in (2, 1, 3) for c2 in range(4) if c2 != c1 and (c1, c2) != (3, 0)]	# 11 -> 00 is a race
def srn_tab(p):
    v = [SRV.get(r, (HOLD, HOLD)) for r in range(4)]
    return [[x[1] for x in v], [x[0] for x in v]] + const([p[0] >> 1, p[0] & 1, p[1] >> 1, p[1] & 1], 2)
def srn_after(p, k):					# Q Q' after case 1 (k = 1) or after case 2 (k = 2)
    return val(*SRV.get(p[1], SRV[p[0]])) if k == 2 else val(*SRV[p[0]])
LSRN = ["S = SW9     R = SW8     Q = LEDG1     Q' = LEDG0"]
W.append(Q(id="SRNOR", name="SRNOR", title="תפסן קביעה-איפוס מהשקופיות", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0), ("G", 1), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))], hexes=[None] * 4,
    variants=VSRN, tables=srn_tab, answer=lambda p: (srn_after(p, 2), 0x3),
    describe=lambda p: f"NOR SR latch: S R = {p[0]:02b} then {p[1]:02b}",
    B=[LSRN[0] + "     case 1 = HEX3 HEX2     case 2 = HEX1 HEX0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח תפסן הקביעה-איפוס מהשקופיות, משני שערים:", "SR latch:   N1 = NOR(R, Q')     N2 = NOR(S, Q)"] + LSRN +
            ["שימו את המתגים כמו במצב 1 שבתצוגה, והעתיקו את הנורות:", "case 1:   S = HEX3     R = HEX2"] + SW1SW0,
            lambda q, p: (srn_after(p, 1), 0x3)),
           (["עכשיו שימו את המתגים כמו במצב 2 שבתצוגה, והעתיקו שוב:", "case 2:   S = HEX1     R = HEX0"] + LSRN + SW1SW0,
            lambda q, p: (srn_after(p, 2), 0x3))]))

# topic 1, slides 16-17: the D latch inside (an SR latch and two AND gates); two cases (CLK D) from the display
VDS = [(d, c2) for d in range(2) for c2 in ((1, 1 - d), (0, d), (0, 1 - d))]
def ds_tab(p):
    cols = tabf(2, lambda clk, d: (1 - d if clk else HOLD, d if clk else HOLD, clk & (1 - d), clk & d))
    return cols + const([1, p[0], p[1][0], p[1][1]], 2)
def ds_after(p, k):					# S R Q Q' after case 1 / case 2
    d1, (c2, d2) = p[0], p[1]
    if k == 1:
        return val(d1, 1 - d1, d1, 1 - d1)
    qv = d2 if c2 else d1
    return val(c2 & d2, c2 & (1 - d2), qv, 1 - qv)
LDS = ["CLK = SW9     D = SW8", "S = LEDG3     R = LEDG2     Q = LEDG1     Q' = LEDG0"]
W.append(Q(id="DLATCHSR", name="DLATCHSR", title="תפסן D מהשקופיות", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0), ("G", 1), ("G", 2), ("G", 3), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))],
    hexes=[None] * 4, variants=VDS, tables=ds_tab, answer=lambda p: (ds_after(p, 2), 0xF),
    describe=lambda p: f"D latch: CLK D = 1{p[0]} then {p[1][0]}{p[1][1]}",
    B=["   ".join(LDS) + "     case 1 = HEX3 HEX2     case 2 = HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח תפסן", "D", "מהשקופיות: תפסן קביעה-איפוס ושני שערי וגם.", "S = CLK & D     R = CLK & ~D"] + LDS +
            ["שימו את המתגים כמו במצב 1 שבתצוגה, והעתיקו את הנורות:", "case 1:   CLK = HEX3     D = HEX2"] + SW3SW0,
            lambda q, p: (ds_after(p, 1), 0xF)),
           (["עכשיו שימו את המתגים כמו במצב 2 שבתצוגה (קודם את השעון, אחר כך את הנתון), והעתיקו שוב:",
             "case 2:   CLK = HEX1     D = HEX0"] + LDS + SW3SW0, lambda q, p: (ds_after(p, 2), 0xF))]))

# topic 2, slide 24: the enabled flip-flop inside (a mux: EN = 1 -> D, EN = 0 -> Q); the case comes from the display
VEM = [(e, d, q_) for e in range(2) for d in range(2) for q_ in range(2)]
mux = lambda e, d, q_: d if e else q_
LEM = ["EN = SW9     D = SW8     Q now = SW7     LEDG0 = Q after the next clock edge"]
W.append(Q(id="ENMUX", name="ENMUX", title="דלגלג עם אפשור מהשקופיות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0))], hexes=[None] * 4, variants=VEM,
    tables=lambda p: tabf(3, lambda e, d, q_: (mux(e, d, q_),)) + const(list(p), 3),
    answer=lambda p: (mux(1 - p[0], p[1], p[2]), 0x1), describe=lambda p: f"EN D Q = {p[0]}{p[1]}{p[2]}",
    B=[LEM[0] + "     case = HEX3 HEX2 HEX1     answer: SW0"], L=[], F=[],
    steps=[(["בלוח הדלגלג עם אפשור מהשקופיות: בורר לפני הדלגלג בוחר מה ייכנס בעליית השעון.",
             "mux:   EN = 1 -> D     EN = 0 -> Q", NOW] + LEM +
            ["שימו את המתגים כמו בתצוגה, ומה הנורה מראה?", "EN = HEX3     D = HEX2     Q now = HEX1"] +
            UP0("הנורה דולקת", "הנורה כבויה"), lambda q, p: (mux(*p), 0x1)),
           (["עכשיו הפכו רק את מתג האפשור. מה הנורה מראה?"] + LEM + UP0("הנורה דולקת", "הנורה כבויה"),
            lambda q, p: (mux(1 - p[0], p[1], p[2]), 0x1))]))

# topic 2, slides 25-27: a resettable or a settable flip-flop (hidden which, and on which switch)
LRS2 = ["D = SW9     Reset or Set = SW8     LEDG0 = Q after the next clock edge"]
rsv = lambda p: p[0] if p[2] else p[1]			# p = (settable, D, Reset/Set)
W.append(Q(id="RSTORSET", name="RSTORSET", title="דלגלג עם איפוס או עם קביעה", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("H", (3, 0)), ("H", (2, 0))], hexes=[None] * 4,
    variants=[(st_, d, c) for st_ in range(2) for d in range(2) for c in range(2)],
    tables=lambda p: tabf(2, lambda d, c: (p[0] if c else d,)) + const([p[1], p[2]], 2),
    answer=lambda p: (p[0], 0x1), describe=lambda p: f"{'settable' if p[0] else 'resettable'}, case D = {p[1]}, ctl = {p[2]}",
    B=[LRS2[0] + "     case = HEX3 HEX2     answer: SW0"], L=[], F=[],
    steps=[(["בלוח אחד משני הדלגלגים מהשקופיות: דלגלג עם איפוס, או דלגלג עם קביעה.", NOW] + LRS2 +
            ["שימו את המתגים כמו בתצוגה. מה הנורה מראה?", "D = HEX3     Reset or Set = HEX2"] +
            UP0("הנורה דולקת", "הנורה כבויה"), lambda q, p: (rsv(p), 0x1)),
           (["איזה שער יש לפני הכניסה של הדלגלג? נסו גם מצבים אחרים של המתגים."] + LRS2 +
            code(["AND:  D & ~Reset  (resettable)", "OR:  D | Set  (settable)"]), lambda q, p: (p[0], 0x1))]))

# topic 2, slide 23: the 4-bit register, one flip-flop is stuck at 0 or 1
VRS = [(k, v) for k in range(4) for v in range(2)]
def stuck(p, d):
    k, v = p
    return (d | (1 << k)) if v else (d & ~(1 << k))
W.append(Q(id="REGSTUCK", name="REGSTUCK", title="אוגר של 4 ביטים מהשקופיות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=VRS,
    tables=lambda p: tabf(4, lambda *b: hx(stuck(p, val(*b)))), answer=lambda p: (p[0], 0x3),
    describe=lambda p: f"Q{p[0]} stuck at {p[1]}",
    B=[LRP[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח האוגר של 4 ביטים מהשקופיות: ארבעה דלגלגים עם שעון משותף.",
             "אבל דלגלג אחד מקולקל: היציאה שלו תקועה.", REGNOW] + LRP +
            ["שימו", "D = 0000", "והעתיקו את הנורות:"] + SW3SW0, lambda q, p: (stuck(p, 0), 0xF)),
           (["עכשיו", "D = 1111", "והעתיקו:"] + LRP + SW3SW0, lambda q, p: (stuck(p, 15), 0xF)),
           (["איזה דלגלג מקולקל?"] + LRP + code(["Q0", "Q1", "Q2", "Q3"]), lambda q, p: (p[0], 0x3))]))

# topic 3, slides 36-37: flopr with a synchronous or an asynchronous reset (reset to 0), one bit
CFR2 = ["36:  always_ff @(posedge clk)              if (reset) q <= 0; else q <= d;",
        "37:  always_ff @(posedge clk, posedge reset)  if (reset) q <= 0; else q <= d;"]
W.append(Q(id="FLOPRSLIDE", name="FLOPRSLIDE", title="flopr מהשקופיות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=[0, 1],
    tables=lambda p: tabf(3, lambda rs, d, q_: (0 if (p and rs) else q_, 0 if rs else d)),
    answer=lambda p: (p, 0x1), describe=lambda p: "slide 37 (asynchronous)" if p else "slide 36 (synchronous)",
    B=["   ".join(LFR) + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח הדלגלג עם איפוס מהשקופיות, באחד משני הקודים:"] + CFR2 + [NOW2] + LFR +
            ["שימו", "reset = 1     d = 1     q before = 1", "והעתיקו את הנורות:"] + SW1SW0,
            lambda q, p: (0 if p else 2, 0x3)),
           (["איזה קוד בלוח?"] + CFR2 + LFR + code(["36", "37"]), lambda q, p: (p, 0x1))]))

# topic 3, slide 41: syncgood (nonblocking) or syncbad (blocking)
CSG = ["syncgood:  n1 <= d;  q <= n1;", "syncbad:   n1 = d;   q = n1;"]
W.append(Q(id="SYNCGOOD", name="SYNCGOOD", title="syncgood או syncbad?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=[0, 1],
    tables=lambda p: tabf(3, lambda d, n1, q_: (d, d if p else n1)),
    answer=lambda p: (p, 0x1), describe=lambda p: "syncbad" if p else "syncgood",
    B=["   ".join(LBL) + "     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח אחד משני המודולים מהשקופיות, בתוך", "always_ff @(posedge clk) begin ... end"] + CSG + [ONE] + LBL +
            ["שימו", "d = 1     n1 before = 0     q before = 0", "והעתיקו את הנורות:"] + SW1SW0,
            lambda q, p: (3 if p else 2, 0x3)),
           (["איזה מודול בלוח?"] + CSG + LBL + code(["syncgood", "syncbad"]), lambda q, p: (p, 0x1))]))

# topic 3, slide 39: the latch module, 4 bits; two numbers from the display
VLS = rv(539, 60, lambda r: (lambda a, b: (a, b) if a != b else None)(r.randint(1, 15), r.randint(1, 15)))
LLS = ["clk = SW9     d[3:0] = SW8..SW5 (HEX0)     q = LEDG3..LEDG0"]
W.append(Q(id="LATCHSLIDE", name="LATCHSLIDE", title="מודול ה-latch מהשקופיות", inputs=[9, 8, 7, 6, 5], flat=True, seq=True,
    small=True, outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [8, 7, 6, 5]], variants=VLS,
    tables=lambda p: tabf(5, lambda c, *b: tuple(x if c else HOLD for x in hx(val(*b)))) + const(bitsof(p[0], 4) + bitsof(p[1], 4), 5),
    answer=lambda p: (p[0], 0xF), describe=lambda p: f"numbers {p[0]:X}, {p[1]:X}",
    B=[LLS[0] + "     HEX3, HEX2 = two numbers     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מודול ה-", "latch", "מהשקופיות, של 4 ביטים:", "always_latch  if (clk) q <= d;"] + LLS +
            ["הרימו את השעון, שימו ב-", "d", "את המספר שב-", "HEX3", "והעתיקו את הנורות:"] + SW3SW0,
            lambda q, p: (p[0], 0xF)),
           (["הורידו את השעון, ואז שימו ב-", "d", "את המספר שב-", "HEX2", "והעתיקו שוב את הנורות:"] + LLS + SW3SW0,
            lambda q, p: (p[0], 0xF))]))

# ================================================================ EASY questions (2): more circuits of the slides
LIT = UP0("הנורה דולקת", "הנורה כבויה")
CASEN = lambda k: [("H", (d, 0)) for d in (3, 2, 1, 0)[:k]]	# a case of k bits on HEX3.. (one bit per digit)

# topic 1, slides 8-9: the bistable circuit (two inverters back to back); the stored bit Q is on HEX3
W.append(Q(id="BISTABLE", name="BISTABLE", title="המעגל הדו-יציב מהשקופיות", inputs=[9], flat=True,
    outs=CASEN(1), hexes=[None] * 4, variants=[0, 1],
    tables=lambda p: const([p]), answer=lambda p: (2 if p else 1, 0x3), describe=lambda p: f"bistable, Q = {p}",
    B=["HEX3 = Q     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח המעגל הדו-יציב מהשקופיות: שני מהפכים, היציאה של כל אחד היא הכניסה של השני.",
             "I1: Q -> Q'     I2: Q' -> Q", "HEX3 = Q (the stored bit)", "מה היציאה של המהפך הראשון?", "Q' = ?"] + UP0("1", "0"),
            lambda q, p: (1 - p, 0x1)),
           (["העתיקו את שני הצמתים של המעגל:", "HEX3 = Q", "SW1 = Q     SW0 = Q'"], lambda q, p: (2 if p else 1, 0x3))]))

# topic 1, slide 19: the D flip-flop samples D only when CLK rises (CLK before and CLK now on switches)
VFE = [(cb, d, qb) for cb in range(2) for d in range(2) for qb in range(2)]		# CLK now = 1
fedge = lambda cb, cn, d, qb: d if (cn and not cb) else qb
LDE = ["CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6     Q now = LEDG0"]
CDE = ["case:   CLK before = HEX3     CLK now = HEX2     D = HEX1     Q before = HEX0"]
W.append(Q(id="DFFEDGE", name="DFFEDGE", title="דלגלג D מהשקופיות - עליית השעון", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)] + CASEN(4), hexes=[None] * 4, variants=VFE,
    tables=lambda p: tabf(4, lambda cb, cn, d, qb: (fedge(cb, cn, d, qb),)) + const([p[0], 1, p[1], p[2]], 4),
    answer=lambda p: (fedge(1 - p[0], 1, p[1], p[2]), 0x1), describe=lambda p: f"CLK before, now, D, Q before = {p[0]}1{p[1]}{p[2]}",
    B=[LDE[0] + "     case = HEX3..HEX0     answer: SW0"], L=[], F=[],
    steps=[(["בלוח הדלגלג", "D", "מהשקופיות: הוא דוגם את הנתון רק כשהשעון עולה מ-0 ל-1.",
             "D flip-flop:   Q = D only on the rising edge of CLK",
             "אין שעון: השעון לפני ועכשיו על מתגים, והנורה מראה את היציאה עכשיו."] + LDE +
            ["שימו את המתגים כמו בתצוגה. מה הנורה מראה?"] + CDE + LIT, lambda q, p: (fedge(p[0], 1, p[1], p[2]), 0x1)),
           (["עכשיו הפכו רק את המתג של השעון לפני. מה הנורה מראה?"] + LDE + LIT,
            lambda q, p: (fedge(1 - p[0], 1, p[1], p[2]), 0x1))]))

# topic 1, slide 20: the flip-flop inside (L1 transparent when CLK = 0, L2 when CLK = 1); the case comes from the display
def msi(c, d, n1b, qb):
    n1 = d if c == 0 else n1b
    return (n1, n1 if c else qb)
LMI = ["CLK = SW9     D = SW8     N1 before = SW7     Q before = SW6", "N1 = LEDG1     Q = LEDG0"]
W.append(Q(id="MSINSIDE", name="MSINSIDE", title="דלגלג D מבפנים - שני תפסנים", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 1), ("G", 0)] + CASEN(4), hexes=[None] * 4, variants=[(d, n, q_) for d in range(2) for n in range(2) for q_ in range(2)],
    tables=lambda p: tabf(4, msi) + const([0, p[0], p[1], p[2]], 4),
    answer=lambda p: (val(p[0], p[0]), 0x3), describe=lambda p: f"CLK 0, D {p[0]}, N1 before {p[1]}, Q before {p[2]}",
    B=["   ".join(LMI) + "     case = HEX3..HEX0     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח הדלגלג מהשקופיות: שני תפסנים בטור עם שעונים הפוכים.",
             "D -> L1 -> N1 -> L2 -> Q     L1: transparent when CLK = 0     L2: transparent when CLK = 1"] + LMI +
            ["שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:",
             "case:   CLK = HEX3     D = HEX2     N1 before = HEX1     Q before = HEX0"] + SW1SW0,
            lambda q, p: (val(p[0], p[2]), 0x3)),
           (["עכשיו השעון עולה: העתיקו את הנורה של", "N1", "למתג שלה, הרימו את השעון, והעתיקו שוב:",
             "SW7 = LEDG1     SW9 = 1"] + LMI + SW1SW0, lambda q, p: (val(p[0], p[0]), 0x3))]))

# topic 1, slide 21: a D latch and a D flip-flop on the same inputs (which LED is which is hidden)
def lvf(p):
    def f(cb, cn, d, qb):
        lat, ff = (d if cn else qb), fedge(cb, cn, d, qb)
        return (ff, lat) if p[0] else (lat, ff)
    return f
LLF = ["CLK before = SW9     CLK now = SW8     D = SW7     Q before = SW6",
       "LEDG1, LEDG0 = D latch, D flip-flop (in some order)"]
W.append(Q(id="LATCHVSFF", name="LATCHVSFF", title="תפסן D מול דלגלג D מהשקופיות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 1), ("G", 0)] + CASEN(4), hexes=[None] * 4, variants=[(r, d) for r in range(2) for d in range(2)],
    tables=lambda p: tabf(4, lvf(p)) + const([1, 1, p[1], 1 - p[1]], 4),
    answer=lambda p: (p[0], 0x1), describe=lambda p: f"flip-flop on LEDG{p[0]}, case 11{p[1]}{1 - p[1]}",
    B=["   ".join(LLF) + "     case = HEX3..HEX0     answer: SW0"], L=[], F=[],
    steps=[(["בלוח תפסן", "D", "ודלגלג", "D", "מהשקופיות, על אותן כניסות.",
             "D latch: Q = D while CLK = 1     D flip-flop: Q = D only when CLK rises from 0 to 1"] + LLF +
            ["שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:",
             "case:   CLK before = HEX3     CLK now = HEX2     D = HEX1     Q before = HEX0"] + SW1SW0,
            lambda q, p: (val(*(lvf(p)(1, 1, p[1], 1 - p[1]))), 0x3)),
           (["איזו נורה היא הדלגלג? (השעון לא עלה עכשיו - הוא היה 1 גם לפני)"] + LLF + code(["LEDG0", "LEDG1"]),
            lambda q, p: (p[0], 0x1))]))

# topic 2, slides 23, 25: a 4-bit resettable register; the data from HEX3
LRR = ["Reset = SW9     D[3:0] = SW8..SW5 (HEX0)     LEDG3..LEDG0 = Q after the next clock edge", "HEX3 = a number"]
W.append(Q(id="REGRESET", name="REGRESET", title="אוגר עם איפוס מהשקופיות", inputs=[9, 8, 7, 6, 5], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + hexd(3), hexes=[None, None, None, [8, 7, 6, 5]], variants=list(range(1, 16)),
    tables=lambda p: tabf(5, lambda rs, *b: hx(0 if rs else val(*b))) + const(bitsof(p, 4), 5),
    answer=lambda p: (bin(p).count("1"), 0x7), describe=lambda p: f"number {p:X}",
    B=[LRR[0] + "     HEX3 = a number     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח אוגר של 4 ביטים מהשקופיות: ארבעה דלגלגים עם שעון משותף ואיפוס משותף.", REGNOW] + LRR +
            ["הורידו את האיפוס, שימו ב-", "D", "את המספר שב-", "HEX3", "והעתיקו את הנורות:"] + SW3SW0, lambda q, p: (p, 0xF)),
           (["עכשיו הרימו את האיפוס, והעתיקו שוב:"] + LRR + SW3SW0, lambda q, p: (0, 0xF)),
           (["כמה נורות כבו כשהרמתם את האיפוס?"] + LRR + cnt(4), lambda q, p: (bin(p).count("1"), 0x7))]))

# topic 2, slide 24: an enabled flip-flop over four clock edges (EN and D from LEDs)
def en_w(e, d):					# 4 edges, edge 1 = bit 3; Q starts at 0
    q_, out = 0, 0
    for t in range(4):
        if (e >> (3 - t)) & 1:
            q_ = (d >> (3 - t)) & 1
        out |= q_ << (3 - t)
    return out
VEW = rv(524, 120, lambda r: (lambda e, d: (e, d) if e not in (0, 15) and en_w(e, d) != d else None)(r.randrange(16), r.randrange(16)))
LEW = ["EN = LEDR3..LEDR0     D = LEDG3..LEDG0     (edge 1 = the left LED)"]
W.append(Q(id="ENWAVE", name="ENWAVE", title="דלגלג עם אפשור - ארבע עליות שעון", inputs=[9], flat=True,
    outs=[("R", i) for i in range(4)] + [("G", i) for i in range(4)], hexes=[None] * 4, variants=VEW,
    tables=lambda p: const(bitsof(p[0], 4) + bitsof(p[1], 4)), answer=lambda p: (en_w(*p), 0xF),
    describe=lambda p: f"EN {p[0]:04b} D {p[1]:04b}: Q {en_w(*p):04b}",
    B=[LEW[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הדלגלג עם אפשור מהשקופיות, בארבע עליות שעון משמאל לימין:",
             "EN = 1: Q = D at the edge     EN = 0: Q keeps its value"] + LEW +
            ["באילו עליות האפשור פעיל? העתיקו:", "SW3..SW0 = LEDR3..LEDR0"], lambda q, p: (p[0], 0xF)),
           (["מה היציאה אחרי כל עלייה? לפני עלייה 1 היציאה 0."] + LEW + ["SW3..SW0 = Q after edges 1..4"],
            lambda q, p: (en_w(*p), 0xF))]))

# topic 2, slide 29: the astable circuit (three inverters in a ring) - X Y Z now on the display
ast = lambda s: val(1 - (s & 1), 1 - (s >> 2), 1 - ((s >> 1) & 1))	# X' = ~Z, Y' = ~X, Z' = ~Y
LAS = ["X -> Y -> Z -> X  (three inverters)     HEX3 = X     HEX2 = Y     HEX1 = Z  (now)"]
W.append(Q(id="ASTABLE", name="ASTABLE", title="המעגל המתנדנד מהשקופיות", inputs=[9], flat=True,
    outs=CASEN(3), hexes=[None] * 4, variants=list(range(8)),
    tables=lambda p: const([p >> 2, (p >> 1) & 1, p & 1]), answer=lambda p: (ast(ast(p)), 0x7),
    describe=lambda p: f"XYZ {p:03b} -> {ast(p):03b} -> {ast(ast(p)):03b}",
    B=[LAS[0] + "     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח המעגל הבעייתי מהשקופיות: שלושה מהפכים במסלול מעגלי, בלי כניסות.",
             "כל מהפך הופך את הכניסה שלו אחרי השהיית שער אחת."] + LAS +
            ["מה הצמתים אחרי השהיית שער אחת?", "SW2 = X     SW1 = Y     SW0 = Z"], lambda q, p: (ast(p), 0x7)),
           (["ואחרי עוד השהיית שער אחת?"] + LAS + ["SW2 = X     SW1 = Y     SW0 = Z"], lambda q, p: (ast(ast(p)), 0x7))]))

# topic 2, slides 30-31: synchronous logic - two registers with an inverter between them, one clock
LS2 = ["A = SW9     R1 now = SW8     R2 now = SW7", "LEDG1 = R1 after the next clock edge     LEDG0 = R2 after the next clock edge"]
W.append(Q(id="SYNC2REG", name="SYNC2REG", title="לוגיקה סינכרונית - שני אוגרים", inputs=[9, 8, 7], flat=True,
    outs=[("G", 1), ("G", 0)] + CASEN(3), hexes=[None] * 4, variants=list(range(8)),
    tables=lambda p: tabf(3, lambda a, r1, r2: (a, 1 - r1)) + const([p >> 2, (p >> 1) & 1, p & 1], 3),
    answer=lambda p: (val(p >> 2, 1 - (p >> 2)), 0x3), describe=lambda p: f"A R1 R2 = {p:03b}",
    B=["   ".join(LS2) + "     case = HEX3..HEX1     answer: SW1 SW0"], L=[], F=[],
    steps=[(["בלוח מעגל סינכרוני מהשקופיות: שני אוגרים עם אותו שעון, ומהפך ביניהם.",
             "R1 <= A;     R2 <= ~R1;", NOW] + LS2 +
            ["שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:", "case:   A = HEX3     R1 = HEX2     R2 = HEX1"] + SW1SW0,
            lambda q, p: (val(p >> 2, 1 - ((p >> 1) & 1)), 0x3)),
           (["עוד עליית שעון: העתיקו את הנורות למתגי האוגרים, והעתיקו שוב את הנורות:",
             "SW8 = LEDG1     SW7 = LEDG0"] + LS2 + SW1SW0, lambda q, p: (val(p >> 2, 1 - (p >> 2)), 0x3))]))

# topic 3, slide 38: flopren, 4 bits; q now and a number for d on the display
VFS = rv(538, 40, lambda r: (lambda a, b: (a, b) if a != b else None)(r.randint(1, 15), r.randint(1, 15)))
CFS = ["flopren:  always_ff @(posedge clk, posedge reset)", "  if (reset) q <= 4'b0;  else if (en) q <= d;"]
LFS = ["reset = SW9     en = SW8     d[3:0] = SW7..SW4 (HEX0)     HEX3 = q now     HEX2 = a number",
       "LEDG3..LEDG0 = q after the next clock edge"]
W.append(Q(id="FLOPRENSLIDE", name="FLOPRENSLIDE", title="flopren מהשקופיות", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(4)] + hexd(3) + hexd(2), hexes=[None, None, None, [7, 6, 5, 4]], variants=VFS,
    tables=lambda p: tabf(6, lambda rs, en, *b: hx(0 if rs else (val(*b) if en else p[0]))) + const(bitsof(p[0], 4) + bitsof(p[1], 4), 6),
    answer=lambda p: (p[0], 0xF), describe=lambda p: f"q now {p[0]:X}, number {p[1]:X}",
    B=["   ".join(LFS) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח המודול", "flopren", "מהשקופיות, של 4 ביטים:"] + CFS + [REGNOW] + LFS +
            ["הרימו את האיפוס, והעתיקו את הנורות:"] + SW3SW0, lambda q, p: (0, 0xF)),
           (["הורידו את האיפוס, הרימו את האפשור, שימו ב-", "d", "את המספר שב-", "HEX2", "והעתיקו:"] + CFS + LFS + SW3SW0,
            lambda q, p: (p[1], 0xF)),
           (["עכשיו הורידו את האפשור, והעתיקו שוב:"] + CFS + LFS + SW3SW0, lambda q, p: (p[0], 0xF))]))

# topic 3, slide 41: syncgood over four clock edges (d from LEDs)
LSW4 = ["d = LEDR3..LEDR0  (d at edges 1..4, edge 1 = the left LED)     before edge 1: n1 = 0, q = 0"]
W.append(Q(id="SYNCWAVE", name="SYNCWAVE", title="syncgood בארבע עליות שעון", inputs=[9], flat=True,
    outs=[("R", i) for i in range(4)], hexes=[None] * 4, variants=list(range(1, 16)),
    tables=lambda p: const(bitsof(p, 4)), answer=lambda p: (p >> 1, 0xF), describe=lambda p: f"d {p:04b}: q {p >> 1:04b}",
    B=[LSW4[0] + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח הנתון של", "syncgood", "מהשקופיות, בארבע עליות שעון:",
             "always_ff @(posedge clk) begin  n1 <= d;  q <= n1;  end"] + LSW4 +
            ["מה", "n1", "אחרי כל עלייה?", "SW3..SW0 = n1 after edges 1..4"], lambda q, p: (p, 0xF)),
           (["ומה", "q", "אחרי כל עלייה? (הוא מקבל את", "n1", "של לפני העלייה)"] + LSW4 + ["SW3..SW0 = q after edges 1..4"],
            lambda q, p: (p >> 1, 0xF))]))

# topic 3, slides 34, 42: assign (combinational, at once) and always_ff (at the clock edge) together
CAF = ["assign y = a & b;", "always_ff @(posedge clk)  q <= y;"]
LAF = ["a = SW9     b = SW8     q now = SW7", "LEDG2 = y     LEDG1 = q now     LEDG0 = q after the next clock edge"]
W.append(Q(id="ASSIGNFF", name="ASSIGNFF", title="assign ו-always_ff מהשקופיות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 2), ("G", 1), ("G", 0)] + CASEN(3), hexes=[None] * 4, variants=list(range(8)),
    tables=lambda p: tabf(3, lambda a, b, q_: (a & b, q_, a & b)) + const([p >> 2, (p >> 1) & 1, p & 1], 3),
    answer=lambda p: (val(((p >> 2) ^ 1) & (p >> 1) & 1, p & 1, ((p >> 2) ^ 1) & (p >> 1) & 1), 0x7),
    describe=lambda p: f"a b q = {p:03b}",
    B=["   ".join(LAF) + "     case = HEX3..HEX1     answer: SW2..SW0"], L=[], F=[],
    steps=[(["בלוח הכללים מהשקופיות: לוגיקה צירופית ב-", "assign", "ודלגלג ב-", "always_ff", ":"] + CAF + [NOW2] + LAF +
            ["שימו את המתגים כמו בתצוגה, והעתיקו את הנורות:", "case:   a = HEX3     b = HEX2     q now = HEX1",
             "SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0"],
            lambda q, p: (val((p >> 2) & (p >> 1) & 1, p & 1, (p >> 2) & (p >> 1) & 1), 0x7)),
           (["עכשיו הפכו רק את", "a", "והעתיקו שוב:"] + CAF + LAF + ["SW2 SW1 SW0 = LEDG2 LEDG1 LEDG0"],
            lambda q, p: (val(((p >> 2) ^ 1) & (p >> 1) & 1, p & 1, ((p >> 2) ^ 1) & (p >> 1) & 1), 0x7))]))

ORDER = ["SRNOR", "DLATCHSR", "BISTABLE", "DFFEDGE", "MSINSIDE", "LATCHVSFF", "SRLATCH", "SRENABLE", "DLATCH", "DLATCHIN", "LATCHMIX", "DFF", "LATCHFF", "MASTERSLAVE", "STATEBITS", "OSCRING",
         "ENMUX", "RSTORSET", "REGSTUCK", "REGRESET", "ENWAVE", "ASTABLE", "SYNC2REG", "ENABLE", "RESETSYNC", "SETRESET", "TOGGLE", "REGPERM", "REGINIT", "PIPE", "SHIFTREG", "RING", "ACCUM",
         "FLOPRSLIDE", "SYNCGOOD", "LATCHSLIDE", "FLOPRENSLIDE", "SYNCWAVE", "ASSIGNFF", "LATCHCODE", "INFERLATCH", "COMBORFF", "FLOPR", "FLOPREN", "FFOPS", "COUNTR", "BLOCKING", "NBSWAP", "CONCAT", "WHICHMOD"]
TOPICS = [(40, "תפסנים, דלגלגים ומצב", 16), (40, "אפשור, איפוס, קביעה ואוגרים", 17), (40, "תיאור חומרה סדרתי", 17)]
DESC = {"SRNOR": "קל, מהשקופיות: תפסן קביעה-איפוס משערי NOR - שני מצבים מהתצוגה, מה הנורות",
        "DLATCHSR": "קל, מהשקופיות: תפסן D מתפסן קביעה-איפוס ושני שערי וגם - S, R, Q בשני מצבים",
        "ENMUX": "קל, מהשקופיות: דלגלג עם אפשור (בורר לפני הדלגלג) - המצב הבא במצב מהתצוגה",
        "RSTORSET": "קל, מהשקופיות: דלגלג עם איפוס או עם קביעה - מצב מהתצוגה, ואיזה שער לפניו",
        "REGSTUCK": "קל, מהשקופיות: אוגר של 4 ביטים עם דלגלג תקוע - איזה",
        "FLOPRSLIDE": "קל, מהשקופיות: flopr עם איפוס סינכרוני או אסינכרוני - איזה קוד",
        "SYNCGOOD": "קל, מהשקופיות: syncgood או syncbad - השמה לא חוסמת מול חוסמת",
        "LATCHSLIDE": "קל, מהשקופיות: מודול ה-latch של 4 ביטים - שקוף ואז זוכר",
        "BISTABLE": "קל, מהשקופיות: המעגל הדו-יציב - Q מהתצוגה, מה Q'",
        "DFFEDGE": "קל, מהשקופיות: דלגלג D דוגם רק בעליית השעון - מצב מהתצוגה",
        "MSINSIDE": "קל, מהשקופיות: דלגלג משני תפסנים - N1 ו-Q במצב מהתצוגה ובעליית השעון",
        "LATCHVSFF": "קל, מהשקופיות: תפסן D מול דלגלג D באותו מצב - איזו נורה הדלגלג",
        "REGRESET": "קל, מהשקופיות: אוגר של 4 ביטים עם איפוס - מספר מהתצוגה, וכמה נורות כבו",
        "ENWAVE": "קל, מהשקופיות: דלגלג עם אפשור בארבע עליות שעון",
        "ASTABLE": "קל, מהשקופיות: שלושה מהפכים במעגל - הצמתים אחרי כל השהיית שער",
        "SYNC2REG": "קל, מהשקופיות: שני אוגרים עם מהפך ביניהם - שתי עליות שעון",
        "FLOPRENSLIDE": "קל, מהשקופיות: flopren של 4 ביטים - איפוס, טעינה ושמירה",
        "SYNCWAVE": "קל, מהשקופיות: syncgood בארבע עליות שעון - n1 ו-q",
        "ASSIGNFF": "קל, מהשקופיות: assign מול always_ff - מה משתנה מיד",
        "SRLATCH": "תפסן SR: איזה מצב קובע, מאפס, זוכר; משערי NOR או NAND",
        "DLATCH": "תפסן D: איזה מתג השעון, איזה הנתון, ומתי שקוף",
        "LATCHMIX": "ארבעה תפסנים בארבע נורות - מי זה מי",
        "LATCHFF": "צורת גל של שעון ונתון: היציאה של תפסן ושל דלגלג בכל זמן",
        "MASTERSLAVE": "דלגלג משני תפסנים: היציאה של כל תפסן בצורת גל",
        "DFF": "דלגלג D: איזה מתג הנתון, והאם הנורה מראה את היציאה או את ההפוכה",
        "STATEBITS": "כמה ביטים צריך למספר מצבים, וכמה מצבים יש במספר ביטים",
        "ENABLE": "דלגלג עם אפשור: איזה מתג, ומתי פעיל (המצב הבא)",
        "RESETSYNC": "איפוס סינכרוני או אסינכרוני: המצב עכשיו ואחרי עליית השעון",
        "SETRESET": "קביעה ואיפוס יחד - מי מנצח",
        "TOGGLE": "דלגלג שמתהפך: איזו כניסה הופכת אותו",
        "PIPE": "צורת גל: כמה דלגלגים בטור בין המתג לנורה",
        "RING": "טבעת דלגלגים (רגילה או מפותלת): כמה דלגלגים, וכמה מצבים",
        "REGPERM": "אוגר של 4 ביטים עם חוטים מעורבבים",
        "FLOPR": "קוד של דלגלג עם איפוס: ערך האיפוס, סינכרוני או אסינכרוני",
        "FLOPREN": "קוד עם איפוס ואפשור: באיזה סדר הם נבדקים",
        "LATCHCODE": "always_latch: מתי שקוף, d או ~d",
        "COMBORFF": "always_comb או always_ff, ואיזה שער",
        "BLOCKING": "השמה חוסמת ולא חוסמת: הערכים אחרי עליית שעון אחת",
        "NBSWAP": "החלפה בין שני אוגרים: לא חוסמת מול חוסמת",
        "WHICHMOD": "איזה מודול מהשקופיות בלוח: flop, flopr, flopren או latch",
        "SRENABLE": "תפסן קביעה-איפוס עם אפשור: איזה מתג האפשור, מתי פעיל, איזה קובע",
        "DLATCHIN": "תפסן D מבפנים: השעון, היציאה, והאות S",
        "OSCRING": "טבעת מהפכים: יציבה (זוגי) או מתנדנדת (אי-זוגי), ומה המחזור",
        "REGINIT": "אוגר שבו חלק מהדלגלגים עם קביעה וחלק עם איפוס",
        "SHIFTREG": "אוגר הזזה: איזה מתג נכנס, מאיזה צד, ועם מהפך או בלי",
        "ACCUM": "אוגר עם מחבר במשוב: הצעד, וכמה עליות שעון עד שחוזרים ל-0",
        "COUNTR": "מונה עם ערך איפוס: הערך, סינכרוני או אסינכרוני, וכמה עליות שעון עד 0",
        "INFERLATCH": "if בלי else יוצר תפסן: איזה קוד בלוח",
        "FFOPS": "דלגלג עם case: איזה ערך של sel עושה איזו פעולה",
        "CONCAT": "אוגר עם שרשור: הזזה או סיבוב, ולאיזה כיוון"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "תפסנים, דלגלגים ואוגרים - מהקל אל הקשה, ואי אפשר בלי הלוח")
