# -*- coding: utf-8 -*-
# Week 8 class exercise (lecture 8, Harris 3.5-3.6 + 4.9: sequential timing - setup / hold, tpcq / tccq, the setup and hold
# constraints, clock skew, synchronizers; parallelism - latency and throughput; delays in SystemVerilog). Instructor only.
# The numbers of each student are on the board (HEX digits; SW9 = the second page when there are more than four).
#   python gen_w8.py [--compile] [--only Q05] [--id <ID>]
import itertools, math, random, sys
sys.path.insert(0, "C:/DE10/solutions")
import wk_common as C
G, Q, HOLD = C.setup(8, __file__)
from wk_common import hexd, bitsof, const, cnt, code, BIN4, UP0, binl
W = []
BIN6 = ["32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
BIN7 = ["64 = SW6     32 = SW5     16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
UNIT = "all times in units of 10 ps (5 = 50 ps)"

def digs(n):					# the outputs of the n left digits (HEX3 first)
    return [o for d in (3, 2, 1, 0)[:n] for o in hexd(d)]
def show(pages):				# pages = [[d3, d2, ...], [..]] -> the table; 2 pages = SW9 down / up
    n = len(pages[0])
    cols = []
    for k, d in enumerate((3, 2, 1, 0)[:n]):
        for b in range(4):
            cols.append([(pg[k] >> b) & 1 for pg in (pages if len(pages) == 2 else pages * 2)])
    return cols
def numq(id_, title, n, variants, pages, legend, steps, describe, pages2=False):
    W.append(Q(id=id_, name=id_, title=title, inputs=[9], flat=True, outs=digs(n), hexes=[None, None, None, None],
               variants=variants, tables=lambda p: show(pages(p)), answer=lambda p: steps[-1][1](None, p),
               describe=describe, B=[legend + ("     SW9 = page 2" if pages2 else "") + "     answer: SW8..SW0"], L=[], F=[],
               steps=steps))
def rv(seed, k, f):				# k distinct random variants from a generator f(rng), kept if not None
    r, out = random.Random(seed), []
    for _ in range(20000):				# as many as the ranges allow, up to k
        v = f(r)
        if v is not None and v not in out:
            out.append(v)
            if len(out) == k:
                break
    return out

# ================================================================ topic 1: the setup and hold constraints
SETUP = "Tc >= tpcq + tpd + tsetup"
HOLDC = "tccq + tcd >= thold"
L3 = "HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup"
numq("TCMIN", "זמן המחזור המינימלי", 3, rv(81, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [list(p)], L3,
     [(["בתצוגה ההשהיות של מסלול בין שני אוגרים:", L3, UNIT,
        "מה זמן המחזור הקצר ביותר שעוד עובד?", SETUP] + BIN6, lambda q, p: (sum(p), 0x3F))],
     lambda p: f"tpcq {p[0]} tpd {p[1]} tsetup {p[2]}: Tc {sum(p)}")

L4 = "HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tsetup"
numq("TPDMAX", "כמה זמן מותר ללוגיקה?", 4,
     rv(82, 200, lambda r: (lambda tc, a, c: (tc, a, c) if tc > a + c + 1 else None)(r.randint(10, 40), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]]], L4,
     [(["בתצוגה זמן המחזור וההשהיות של האוגרים:", L4, UNIT,
        "מה ההשהיה הגדולה ביותר שמותרת ללוגיקה הצירופית בין שני האוגרים?", "tpd <= Tc - tpcq - tsetup"] + BIN6,
       lambda q, p: (p[0] - p[1] - p[2], 0x3F))],
     lambda p: f"Tc {p[0]} tpcq {p[1]} tsetup {p[2]}: tpd max {p[0] - p[1] - p[2]}")

L5 = "HEX3 = tccq     HEX2 = tcd     HEX1 = thold"
numq("HOLDOK", "אילוץ ההחזקה", 3, rv(83, 200, lambda r: (r.randint(1, 9), r.randint(0, 9), r.randint(1, 9))),
     lambda p: [list(p)], L5,
     [(["בתצוגה ההשהיות של מסלול בין שני אוגרים:", L5, UNIT, "האם אילוץ ההחזקה מתקיים?", HOLDC] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] + p[1] >= p[2]), 0x1)),
      (["מה ההשהיה הקטנה ביותר שמותרת ללוגיקה כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)", "tcd >= thold - tccq"] + BIN6,
       lambda q, p: (max(0, p[2] - p[0]), 0x3F))],
     lambda p: f"tccq {p[0]} tcd {p[1]} thold {p[2]}")

L6 = "page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 = tpcq     HEX0 = tpd"
L6b = "page 2 (SW9 up):    HEX1 = tsetup"
numq("SLACK", "האם המעגל עומד בזמן?", 4,
     rv(84, 200, lambda r: (r.randint(10, 30), r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]], [0, 0, p[3], 0]], "Tc, tpcq, tpd on page 1; tsetup on page 2",
     [(["בתצוגה שני דפים (המתג השמאלי מחליף):", L6, L6b, UNIT, "האם אילוץ ההתקנה מתקיים?", SETUP] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] >= p[1] + p[2] + p[3]), 0x1)),
      (["בכמה זמן המחזור גדול (או קטן) מהדרוש? כתבו את ההפרש בערך מוחלט:", "| Tc - (tpcq + tpd + tsetup) |"] + BIN6,
       lambda q, p: (abs(p[0] - p[1] - p[2] - p[3]), 0x3F))],
     lambda p: f"Tc {p[0]} needs {p[1] + p[2] + p[3]}", pages2=True)

# two gates between the registers (slides 10-11)
LG = "page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd gate   HEX0 = tcd gate"
LGb = "page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold"
numq("EXAMPLE", "הדוגמה מהשקופית: שני שערים בטור", 4,
     rv(85, 200, lambda r: (lambda tpcq, tsu, tpd, tcd, tccq, th: (tpcq, tsu, tpd, tcd, tccq, th) if tcd <= tpd and tccq <= tpcq else None)(
         r.randint(2, 9), r.randint(2, 9), r.randint(2, 9), r.randint(1, 5), r.randint(1, 6), r.randint(2, 9))),
     lambda p: [[p[0], p[1], p[2], p[3]], [p[4], p[5], 0, 0]], "tpcq tsetup tpd tcd / tccq thold",
     [(["בין שני האוגרים שני שערים בטור. בתצוגה שני דפים:", LG, LGb, UNIT,
        "מה זמן המחזור המינימלי?", "Tc >= tpcq + 2 tpd + tsetup"] + BIN6, lambda q, p: (p[0] + 2 * p[2] + p[1], 0x3F)),
      (["האם אילוץ ההחזקה מתקיים?", "tccq + 2 tcd >= thold"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[4] + 2 * p[3] >= p[5]), 0x1))],
     lambda p: f"Tc {p[0] + 2 * p[2] + p[1]}, hold {'ok' if p[4] + 2 * p[3] >= p[5] else 'violated'}", pages2=True)

# fixing a hold violation with buffers
LB = "HEX3 = tccq     HEX2 = thold     HEX1 = tcd of one buffer"
numq("BUFFERS", "כמה מאגרים לתקן את ההחזקה?", 3,
     rv(86, 120, lambda r: (lambda a, h, b: (a, h, b) if h > a else None)(r.randint(0, 5), r.randint(3, 9), r.randint(1, 3))),
     lambda p: [list(p)], LB,
     [(["בתצוגה מסלול בלי לוגיקה בין שני אוגרים (חוט ישר):", LB, UNIT,
        "האם אילוץ ההחזקה מתקיים בלי שום דבר באמצע?", HOLDC] + UP0("מתקיים", "לא מתקיים"), lambda q, p: (int(p[0] >= p[1]), 0x1)),
      (["כמה מאגרים צריך לפחות להוסיף בדרך כדי שיתקיים?", "tccq + n tcd >= thold"] + cnt(9),
       lambda q, p: (math.ceil((p[1] - p[0]) / p[2]), 0xF))],
     lambda p: f"n = {math.ceil((p[1] - p[0]) / p[2])}")

# ================================================================ topic 2: clock skew, metastability, synchronizers
LS = "page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tpd   HEX1 = tsetup   HEX0 = tskew"
LSb = "page 2 (SW9 up):    HEX3 = tccq   HEX2 = tcd   HEX1 = thold"
VSK = rv(87, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9), r.randint(1, 5), r.randint(1, 9), r.randint(0, 9), r.randint(1, 9)))
numq("SKEWSETUP", "זמן המחזור עם הטיית שעון", 4, VSK,
     lambda p: [[p[0], p[1], p[2], p[3]], [p[4], p[5], p[6], 0]], "tpcq tpd tsetup tskew / tccq tcd thold",
     [(["בתצוגה שני דפים של מסלול עם הטיית שעון:", LS, LSb, UNIT, "מה זמן המחזור המינימלי עם ההטיה?",
        "Tc >= tpcq + tpd + tsetup + tskew"] + BIN6, lambda q, p: (p[0] + p[1] + p[2] + p[3], 0x3F)),
      (["האם אילוץ ההחזקה מתקיים עם ההטיה?", "tccq + tcd >= thold + tskew"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[4] + p[5] >= p[6] + p[3]), 0x1))],
     lambda p: f"Tc {p[0] + p[1] + p[2] + p[3]}, hold {'ok' if p[4] + p[5] >= p[6] + p[3] else 'violated'}", pages2=True)

LK = "HEX3 = tccq     HEX2 = tcd     HEX1 = thold"
numq("SKEWMAX", "כמה הטיה מותרת?", 3, rv(88, 150, lambda r: (lambda a, b, c: (a, b, c) if a + b >= c else None)(r.randint(1, 9), r.randint(0, 9), r.randint(1, 9))),
     lambda p: [list(p)], LK,
     [(["בתצוגה ההשהיות של מסלול קצר:", LK, UNIT, "מה הטיית השעון הגדולה ביותר שאילוץ ההחזקה עוד עומד בה?",
        "tskew <= tccq + tcd - thold"] + BIN6, lambda q, p: (p[0] + p[1] - p[2], 0x3F))],
     lambda p: f"tskew max {p[0] + p[1] - p[2]}")

LT = "HEX3 HEX2 = Tc     HEX1 = tpcq + tpd + tsetup (together)"
numq("SKEWSLACK", "הטיה מותרת לפי אילוץ ההתקנה", 3,
     rv(89, 150, lambda r: (lambda tc, s: (tc, s) if tc >= s else None)(r.randint(10, 19), r.randint(3, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1]]], LT,
     [(["בתצוגה זמן המחזור, וסכום ההשהיות של המסלול:", LT, UNIT,
        "מה הטיית השעון הגדולה ביותר שאילוץ ההתקנה עוד עומד בה?", "Tc >= tpcq + tpd + tsetup + tskew"] + BIN6,
       lambda q, p: (p[0] - p[1], 0x3F))],
     lambda p: f"tskew max {p[0] - p[1]}")

# a synchronizer: how many flip-flops between the switch and the LED (no clock button: the flip-flops' values are on
# switches, and the LED shows the synchronized output after the next clock edge)
SYN = ["A", "Q1", "Q2"]
LSY = ["A = SW9 (the asynchronous input)     Q1 Q2 Q3 = SW8 SW7 SW6 (the flip-flops, now)",
       "Y = LEDG0 = the synchronized output after the next clock edge"]
W.append(Q(id="SYNC", name="SYNC", title="מסנכרן", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[None, None, None, None], variants=[1, 2, 3],
    tables=lambda n: [[(r >> (4 - n)) & 1 for r in range(16)]],
    answer=lambda n: (int(n >= 2), 0x1), describe=lambda n: f"{n} flip-flops",
    B=["     ".join(LSY) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מסנכרן: שרשרת של דלגלגים. הכניסה האסינכרונית נכנסת לדלגלג הראשון, והיציאה היא הדלגלג האחרון.",
             "A -> Q1 -> Q2 -> Q3 -> ..."] + LSY + ["את איזה ערך היציאה מעתיקה בעליית השעון הבאה?"] + code(SYN),
            lambda q, n: (n - 1, 0x3)),
           (["בלוח אותו מסנכרן:", "A -> Q1 -> Q2 -> Q3 -> ..."] + LSY +
            ["כמה דלגלגים יש במסנכרן? (היציאה היא הדלגלג האחרון)"] + cnt(3), lambda q, n: (n, 0xF)),
           (["בלוח אותו מסנכרן.", "מסנכרן טוב בנוי משני דלגלגים לפחות. הוא מספיק?"] + UP0("כן", "לא"),
            lambda q, n: (int(n >= 2), 0x1))]))

# metastability: the resolution time grows with each extra flip-flop
LM = "HEX3 HEX2 = Tc     HEX1 = tsetup"
numq("RESOLVE", "כמה זמן יש להתייצבות?", 3,
     rv(90, 120, lambda r: (lambda tc, su: (tc, su) if tc > su else None)(r.randint(10, 30), r.randint(1, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1]]], LM,
     [(["בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:", LM, UNIT,
        "כמה זמן יש ליציאה של הדלגלג הראשון להתייצב לפני שהשני דוגם אותה?", "tres = Tc - tsetup"] + BIN6,
       lambda q, p: (p[0] - p[1], 0x3F)),
      (["הסיכוי לכשל קטן פי", "e^(tres / tau)", "כשהזמן גדל. אם מוסיפים עוד דלגלג אחד, כמה זמן התייצבות יש בסך הכול?",
        "2 (Tc - tsetup)"] + BIN7, lambda q, p: (2 * (p[0] - p[1]), 0x7F))],
     lambda p: f"tres {p[0] - p[1]}")

# ================================================================ topic 3: parallelism, delays in SystemVerilog
def per_hour(minutes):
    return 60 // minutes
LC = "HEX3 = minutes of step 1     HEX2 HEX1 = minutes of step 2"
VCK = [(a, b) for a in range(1, 10) for b in range(10, 60) if 60 % (a + b) == 0 and 60 % b == 0]
numq("LATENCY", "זמן אחזור וקצב: עוגיות", 3, VCK, lambda p: [[p[0], p[1] // 10, p[1] % 10]], LC,
     [(["אפייה בשני שלבים (הכנה ואפייה), מגש אחד בכל פעם. הזמנים בתצוגה:", LC,
        "מה זמן האחזור של מגש אחד (בדקות)?", "latency = step 1 + step 2"] + BIN6, lambda q, p: (p[0] + p[1], 0x3F)),
      (["כמה מגשים בשעה, בלי מקביליות?", "throughput = 60 / latency"] + BIN6, lambda q, p: (per_hour(p[0] + p[1]), 0x3F)),
      (["עם צנרת (מגש חדש מתחיל הכנה כשהקודם בתנור): כמה מגשים בשעה?", "throughput = 60 / the longest step"] + BIN6,
       lambda q, p: (per_hour(max(p)), 0x3F))],
     lambda p: f"latency {p[0] + p[1]}, {per_hour(p[0] + p[1])}/h, pipelined {per_hour(max(p))}/h")

LP = "HEX3 = workers     HEX2 HEX1 = minutes for one tray (latency)"
VSP = [(n, l) for n in range(2, 6) for l in (10, 12, 15, 20, 30)]
numq("SPATIAL", "מקביליות מרחבית", 3, VSP, lambda p: [[p[0], p[1] // 10, p[1] % 10]], LP,
     [(["כמה עובדים, כל אחד עם תנור משלו. בתצוגה:", LP, "כמה מגשים בשעה כולם יחד?", "throughput = workers x 60 / latency"] + BIN6,
       lambda q, p: (p[0] * 60 // p[1], 0x3F)),
      (["ומה זמן האחזור של מגש אחד?"] + BIN6, lambda q, p: (p[1], 0x3F))],
     lambda p: f"{p[0] * 60 // p[1]}/h")

LPC = "HEX3 HEX2 HEX1 = the delays of 3 pipeline stages     HEX0 = tpcq + tsetup"
VPC = rv(91, 200, lambda r: (r.randint(2, 9), r.randint(2, 9), r.randint(2, 9), r.randint(1, 4)))
numq("PIPECLK", "צנרת: זמן מחזור וזמן אחזור", 4, VPC, lambda p: [list(p)], LPC,
     [(["מעגל מחולק ל-3 שלבים עם אוגרים ביניהם. בתצוגה:", LPC, UNIT,
        "מה זמן המחזור הקצר ביותר?", "Tc = the longest stage + tpcq + tsetup"] + BIN6, lambda q, p: (max(p[:3]) + p[3], 0x3F)),
      (["מה זמן האחזור (מהכניסה עד היציאה, 3 מחזורים)?", "latency = 3 Tc"] + BIN6, lambda q, p: (3 * (max(p[:3]) + p[3]), 0x3F))],
     lambda p: f"Tc {max(p[:3]) + p[3]}")

# a pipeline on the board: tokens move one stage each clock (no clock button: the stages now are on switches, and the
# LEDs show the stages after the next clock edge)
def pipe_next(n, r, k):				# r = new token (SW9), stages 1..5 (SW8..SW4); stage k after the edge
    if k > n:
        return 0
    return (r >> 5) & 1 if k == 1 else (r >> (6 - k)) & 1
LPS = ["new token = SW9     stages 1..5 now = SW8..SW4 (1 = a token)", "stages 1..5 after the next clock edge = LEDG4..LEDG0"]
W.append(Q(id="PIPESIM", name="PIPESIM", title="צנרת על הלוח", inputs=[9, 8, 7, 6, 5, 4], flat=True, small=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, None], variants=[2, 3, 4, 5],
    tables=lambda n: [[pipe_next(n, r, 5 - i) for r in range(64)] for i in range(5)],
    answer=lambda n: (n, 0xF), describe=lambda n: f"{n} stages",
    B=["     ".join(LPS) + "     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח צנרת: בכל עליית שעון כל אסימון עובר לשלב הבא. במתגים השלבים עכשיו, ובנורות השלבים אחרי עליית השעון הבאה.",
             "בלוח יש מקום ל-5 שלבים, אבל רק חלק מהם קיימים."] + LPS + ["כמה שלבים יש?"] + cnt(5), lambda q, n: (n, 0xF)),
           (["בלוח אותה צנרת:"] + LPS +
            ["מכניסים אסימון חדש בכל עליית שעון. כמה אסימונים נמצאים בצנרת בבת אחת, כשהיא מלאה?"] + cnt(5), lambda q, n: (n, 0xF))]))

# delays in SystemVerilog (slides 36-41)
LD = "HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)"
CODE = ["assign #d1 {ab, bb, cb} = ~{a, b, c};", "assign #d2 n1 = ab & bb & cb;   (and n2, n3 the same)", "assign #d3 y = n1 | n2 | n3;"]
numq("HDLDELAY", "השהיות בקוד", 3, rv(92, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [list(p)], LD,
     [(["הקוד מהשקופית, וההשהיות בתצוגה:"] + CODE + [LD,
        "הכניסה הראשונה משתנה בזמן 0 ומשנה את היציאה. מתי היציאה משתנה (בננו-שניות)?", "a -> y", "t = d1 + d2 + d3"] + BIN6, lambda q, p: (sum(p), 0x3F)),
      (["ואם רק", "n1", "משתנה בזמן 0 - מתי", "y", "משתנה?"] + BIN6, lambda q, p: (p[2], 0x3F))],
     lambda p: f"y after {sum(p)} ns")

# the maximum clock frequency
LF = "HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     (ns)"
VFM = [p for p in itertools.product(range(1, 10), repeat=3) if 1000 % sum(p) == 0 and sum(p) >= 4]
numq("FMAX", "תדר השעון המקסימלי", 3, VFM, lambda p: [list(p)], LF,
     [(["בתצוגה ההשהיות של המסלול הארוך, בננו-שניות:", LF, "מה זמן המחזור המינימלי (ננו-שניות)?", SETUP] + BIN6,
       lambda q, p: (sum(p), 0x3F)),
      (["מה התדר המקסימלי, במגה-הרץ?", "f = 1000 / Tc", "256 = SW8   128 = SW7   64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0"],
       lambda q, p: (1000 // sum(p), 0x1FF))],
     lambda p: f"Tc {sum(p)} ns, {1000 // sum(p)} MHz")

# the aperture: setup + hold around the edge
LA = "HEX3 = tsetup     HEX2 = thold     HEX1 = when D changes, before the edge"
VAP = rv(93, 150, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(0, 9)))
numq("APERTURE", "חלון הדגימה", 3, VAP, lambda p: [list(p)], LA,
     [(["בתצוגה זמני הדלגלג:", LA, UNIT, "מה רוחב חלון הדגימה סביב עליית השעון?", "ta = tsetup + thold"] + BIN6,
       lambda q, p: (p[0] + p[1], 0x3F)),
      (["הנתון משתנה כמה זמן לפני העלייה (הספרה השלישית). האם זה בתוך החלון (סכנה)?",
        "inside the aperture: change time < tsetup"] + UP0("בתוך החלון", "בסדר"), lambda q, p: (int(p[2] < p[0]), 0x1))],
     lambda p: f"aperture {p[0] + p[1]}, change {p[2]} before the edge: {'violation' if p[2] < p[0] else 'ok'}")

# the latency a synchronizer adds
LY = "HEX3 = flip-flops in the synchronizer     HEX2 HEX1 = Tc (ns)"
VSL = [(n, tc) for n in (2, 3) for tc in (2, 4, 5, 8, 10, 20, 25, 40, 50)]
numq("SYNCLAT", "כמה זמן לוקח לסנכרן?", 3, VSL, lambda p: [[p[0], p[1] // 10, p[1] % 10]], LY,
     [(["בתצוגה מסנכרן:", LY, "כמה זמן לכל היותר עובר עד שהכניסה האסינכרונית מגיעה ליציאה (בננו-שניות)?",
        "about (flip-flops) x Tc", "128 = SW7"] + BIN7, lambda q, p: (p[0] * p[1], 0xFF))],
     lambda p: f"{p[0] * p[1]} ns")

# spatial and temporal together (slide 33)
LBO = "HEX3 = workers     HEX2 = minutes of step 1     HEX1 HEX0 = minutes of step 2"
VBO = [(n, a, b) for n in (2, 3, 4) for a in range(1, 10) for b in (10, 12, 15, 20, 30) if a < b]
numq("BOTH", "מקביליות מרחבית וזמנית יחד", 4, VBO, lambda p: [[p[0], p[1], p[2] // 10, p[2] % 10]], LBO,
     [(["כמה עובדים, וכל אחד עובד בצנרת (הכנה של מגש חדש בזמן שהקודם בתנור). בתצוגה:", LBO,
        "כמה מגשים בשעה, כולם יחד?", "throughput = workers x 60 / the longest step"] + BIN7,
       lambda q, p: (p[0] * 60 // max(p[1], p[2]), 0x7F))],
     lambda p: f"{p[0] * 60 // max(p[1], p[2])}/h")

# ================================================================ new questions (topic 1)
# two paths between the same registers: the longer one sets the cycle time
LTP = "HEX3 = tpcq     HEX2 = tpd of path A     HEX1 = tpd of path B     HEX0 = tsetup"
numq("TWOPATHS", "שני מסלולים: מי קובע?", 4,
     rv(101, 200, lambda r: (lambda a, b, c, d: (a, b, c, d) if b != c else None)(r.randint(1, 9), r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [list(p)], LTP,
     [(["בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:", "HEX2 = tpd of path A     HEX1 = tpd of path B", UNIT,
        "איזה מסלול קובע את זמן המחזור?"] + code(["path A", "path B"]), lambda q, p: (int(p[2] > p[1]), 0x1)),
      (["בין שני אוגרים יש שני מסלולים של לוגיקה. בתצוגה:", LTP, UNIT,
        "מה זמן המחזור המינימלי?", "Tc >= tpcq + max(tpd A, tpd B) + tsetup"] + BIN6,
       lambda q, p: (p[0] + max(p[1], p[2]) + p[3], 0x3F))],
     lambda p: f"path {'AB'[p[2] > p[1]]}, Tc {p[0] + max(p[1], p[2]) + p[3]}")

# how many gates fit in series in one cycle
LGM = "HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)     HEX0 = tpd of one gate"
numq("GATESMAX", "כמה שערים נכנסים במחזור?", 4,
     rv(102, 200, lambda r: (lambda tc, o, g: (tc, o, g) if tc - o >= 2 * g else None)(r.randint(10, 40), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]]], LGM,
     [(["בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:", "HEX3 HEX2 = Tc     HEX1 = tpcq + tsetup (together)", UNIT,
        "כמה זמן נשאר ללוגיקה?", "tpd <= Tc - (tpcq + tsetup)"] + BIN6, lambda q, p: (p[0] - p[1], 0x3F)),
      (["בתצוגה זמן המחזור, התקורה של האוגרים, וההשהיה של שער אחד:", LGM, UNIT,
        "כמה שערים כאלה אפשר לשים בטור לכל היותר?", "n x tpd(gate) <= Tc - (tpcq + tsetup)"] + BIN6,
       lambda q, p: ((p[0] - p[1]) // p[2], 0x3F))],
     lambda p: f"{(p[0] - p[1]) // p[2]} gates")

# the slide 10-11 example with any number of gates on the long and on the short path
LE3 = "page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd of a gate   HEX0 = gates on the long path"
LE3b = "page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path"
LE3s = "page 1 (SW9 down):  HEX3 = tpcq   HEX2 = tsetup   HEX1 = tpd of a gate   HEX0 = gates on the long path"
LE3h = "page 2 (SW9 up):    HEX3 = tccq   HEX2 = thold   HEX1 = tcd of a gate   HEX0 = gates on the short path"
numq("EXAMPLE3", "הדוגמה מהשקופית עם יותר שערים", 4,
     rv(103, 220, lambda r: (lambda pc, su, pd, nl, cc, th, cd, ns: (pc, su, pd, nl, cc, th, cd, ns)
                             if cd <= pd and cc <= pc and ns <= nl else None)(
         r.randint(2, 9), r.randint(2, 9), r.randint(2, 9), r.randint(2, 5), r.randint(1, 6), r.randint(2, 9), r.randint(1, 4), r.randint(1, 3))),
     lambda p: [[p[0], p[1], p[2], p[3]], [p[4], p[5], p[6], p[7]]], "tpcq tsetup tpd n_long / tccq thold tcd n_short",
     [(["כמו בדוגמה מהשקופית, עם מספר אחר של שערים. הנתונים בדף הראשון:", LE3s, UNIT,
        "מה זמן המחזור המינימלי?", "Tc >= tpcq + n_long x tpd + tsetup"] + BIN6, lambda q, p: (p[0] + p[3] * p[2] + p[1], 0x3F)),
      (["הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):", LE3h, UNIT,
        "האם אילוץ ההחזקה מתקיים?", "tccq + n_short x tcd >= thold"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[4] + p[7] * p[6] >= p[5]), 0x1)),
      (["הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):", LE3h, UNIT,
        "מה ההשהיה הקטנה ביותר של שער במסלול הקצר כדי שהאילוץ יתקיים? (0 אם כל השהיה מספיקה)",
        "tcd >= (thold - tccq) / n_short     (round up)"] + BIN6,
       lambda q, p: (max(0, math.ceil((p[5] - p[4]) / p[7])), 0x3F))],
     lambda p: f"Tc {p[0] + p[3] * p[2] + p[1]}, tcd min {max(0, math.ceil((p[5] - p[4]) / p[7]))}", pages2=True)

# ================================================================ new questions (topic 2)
# a hold violation caused by skew, fixed with buffers
LSF = "page 1 (SW9 down):  HEX3 = tccq   HEX2 = tcd   HEX1 = thold   HEX0 = tskew"
LSFb = "page 2 (SW9 up):    HEX3 = tcd of one buffer"
numq("SKEWFIX", "מאגרים נגד הטיית שעון", 4,
     rv(104, 200, lambda r: (r.randint(1, 6), r.randint(0, 5), r.randint(1, 9), r.randint(1, 5), r.randint(1, 3))),
     lambda p: [[p[0], p[1], p[2], p[3]], [p[4], 0, 0, 0]], "tccq tcd thold tskew / tcd of a buffer",
     [(["השעון של האוגר השני מגיע מאוחר. הנתונים בדף הראשון:", LSF, UNIT,
        "האם אילוץ ההחזקה מתקיים עם ההטיה?", "tccq + tcd >= thold + tskew"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] + p[1] >= p[2] + p[3]), 0x1)),
      (["מוסיפים מאגרים במסלול. בתצוגה שני דפים:", LSF, LSFb, UNIT,
        "כמה מאגרים צריך לפחות כדי שהאילוץ יתקיים? (0 אם כבר מתקיים)",
        "tccq + tcd + n x tcd(buffer) >= thold + tskew"] + BIN4,
       lambda q, p: (max(0, math.ceil((p[2] + p[3] - p[0] - p[1]) / p[4])), 0xF))],
     lambda p: f"{max(0, math.ceil((p[2] + p[3] - p[0] - p[1]) / p[4]))} buffers", pages2=True)

# skew both ways: CLK2 early hurts setup, CLK2 late hurts hold
LSC = "page 1 (SW9 down):  HEX3 HEX2 = Tc     HEX1 HEX0 = tpcq + tpd + tsetup (together)"
LSCb = "page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew"
LSCs = "page 2 (SW9 up):    HEX1 = tskew"
LSCh = "page 2 (SW9 up):    HEX3 = tccq + tcd (together)   HEX2 = thold   HEX1 = tskew"
numq("SKEWCHECK", "הטיה לשני הכיוונים", 4,
     rv(105, 220, lambda r: (lambda tc, s, h, th, sk: (tc, s, h, th, sk) if abs(tc - s) <= 6 and abs(h - th) <= 6 else None)(
         r.randint(10, 30), r.randint(10, 30), r.randint(1, 9), r.randint(1, 9), r.randint(1, 5))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1] // 10, p[1] % 10], [p[2], p[3], p[4], 0]], "Tc, setup path / hold path, thold, tskew",
     [(["ההטיה יכולה להיות לשני הכיוונים. בתצוגה שני דפים:", LSC, LSCs, UNIT,
        "אם השעון של האוגר השני מקדים - האם אילוץ ההתקנה מתקיים?", "Tc >= tpcq + tpd + tsetup + tskew"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] >= p[1] + p[4]), 0x1)),
      (["הנתונים של המסלול הקצר בדף השני (המתג השמאלי למעלה):", LSCh, UNIT,
        "אם השעון של האוגר השני מאחר - האם אילוץ ההחזקה מתקיים?", "tccq + tcd >= thold + tskew"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[2] >= p[3] + p[4]), 0x1)),
      (["ההטיה יכולה להיות לשני הכיוונים. בתצוגה שני דפים:", LSC, LSCb, UNIT,
        "מה ההטיה הגדולה ביותר ששני האילוצים יחד עומדים בה? (0 אם אפילו בלי הטיה לא)",
        "tskew <= min(Tc - (tpcq + tpd + tsetup), tccq + tcd - thold)"] + BIN4,
       lambda q, p: (max(0, min(p[0] - p[1], p[2] - p[3])), 0xF))],
     lambda p: f"setup {'ok' if p[0] >= p[1] + p[4] else 'bad'}, hold {'ok' if p[2] >= p[3] + p[4] else 'bad'}, "
               f"max skew {max(0, min(p[0] - p[1], p[2] - p[3]))}", pages2=True)

# MTBF grows by e^(tres/tau) with each extra flip-flop
LMG = "HEX3 HEX2 = Tc     HEX1 = tsetup     HEX0 = tau"
numq("MTBFGROW", "כמה עוזר עוד דלגלג?", 4,
     rv(106, 200, lambda r: (lambda tc, su, tau: (tc, su, tau) if (tc - su) % tau == 0 and 2 <= (tc - su) // tau <= 15 else None)(
         r.randint(10, 40), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]]], LMG,
     [(["בתצוגה זמן המחזור וזמן ההתקנה של הדלגלגים במסנכרן:", "HEX3 HEX2 = Tc     HEX1 = tsetup", UNIT,
        "כמה זמן התייצבות נותן כל דלגלג נוסף?", "tres = Tc - tsetup"] + BIN6, lambda q, p: (p[0] - p[1], 0x3F)),
      (["בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:", LMG, UNIT,
        "כל דלגלג נוסף מגדיל את הזמן הממוצע בין כשלים פי", "e^(tres / tau)",
        "מה החזקה?", "tres / tau = (Tc - tsetup) / tau"] + BIN6, lambda q, p: ((p[0] - p[1]) // p[2], 0x3F)),
      (["בתצוגה זמן המחזור, זמן ההתקנה, וקבוע הזמן של הדלגלגים:", LMG, UNIT,
        "מסנכרן של 4 דלגלגים במקום 2: פי", "e", "בחזקת כמה גדל הזמן הממוצע בין כשלים?",
        "2 x (Tc - tsetup) / tau"] + BIN6, lambda q, p: (2 * ((p[0] - p[1]) // p[2]), 0x3F))],
     lambda p: f"tres {p[0] - p[1]}, e^{(p[0] - p[1]) // p[2]} per flip-flop")

# the mean time between failures from the failure probability per event
LMT = "HEX3 HEX2 = N (input changes per second)     HEX1 HEX0 = K"
LMP = "P(failure) per change = 1 / (K x 1000)"
numq("MTBF", "הזמן הממוצע בין כשלים", 4,
     rv(107, 220, lambda r: (lambda n, k: (n, k) if (1000 * k) % (2 * n) == 0 and 1000 * k // n <= 511 else None)(
         r.randint(10, 99), r.randint(1, 20))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1] // 10, p[1] % 10]], LMT,
     [(["בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:", LMT, LMP,
        "כל כמה שניות, בממוצע, המסנכרן נכשל?", "MTBF = 1 / (N x P) = K x 1000 / N"] + binl(9),
       lambda q, p: (1000 * p[1] // p[0], 0x1FF)),
      (["בתצוגה כמה פעמים בשנייה הכניסה האסינכרונית משתנה, והסיכוי לכשל בכל שינוי:", LMT, LMP,
        "ואם הכניסה משתנה פי 2 יותר פעמים בשנייה?", "MTBF = K x 1000 / (2 N)"] + binl(9),
       lambda q, p: (500 * p[1] // p[0], 0x1FF))],
     lambda p: f"MTBF {1000 * p[1] // p[0]} s, doubled N: {500 * p[1] // p[0]} s")

# ================================================================ new questions (topic 3)
# splitting a circuit into equal pipeline stages
LPS = "HEX3 HEX2 = tpd of the whole logic     HEX1 = stages     HEX0 = tpcq + tsetup (together)"
numq("PIPESPLIT", "חלוקה לשלבים שווים", 4,
     rv(112, 220, lambda r: (lambda k, d, o: (d, k, o) if d % k == 0 else None)(r.randint(2, 4), r.randint(12, 60), r.randint(1, 5))),
     lambda p: [[p[0] // 10, p[0] % 10, p[1], p[2]]], LPS,
     [(["מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:", "HEX3 HEX2 = tpd of the whole logic     HEX0 = tpcq + tsetup (together)", UNIT,
        "מה זמן המחזור בלי צנרת?", "Tc = tpd + tpcq + tsetup"] + binl(7), lambda q, p: (p[0] + p[2], 0x7F)),
      (["מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:", LPS, UNIT,
        "מה זמן המחזור עם הצנרת?", "Tc = tpd / stages + tpcq + tsetup"] + binl(7), lambda q, p: (p[0] // p[1] + p[2], 0x7F)),
      (["מעגל צירופי בין שני אוגרים. רוצים לחלק אותו לשלבים שווים עם אוגרים ביניהם. בתצוגה:", LPS, UNIT,
        "מה זמן האחזור עם הצנרת? (הוא גדל בגלל האוגרים)", "latency = stages x Tc"] + binl(7),
       lambda q, p: (p[1] * (p[0] // p[1] + p[2]), 0x7F))],
     lambda p: f"Tc {p[0] + p[2]} -> {p[0] // p[1] + p[2]}, latency {p[1] * (p[0] // p[1] + p[2])}")

# N tokens through a k-stage pipeline
LNT = "HEX3 = stages     HEX2 HEX1 = tokens     HEX0 = Tc (ns)"
numq("NTOKENS", "כמה זמן לכמה אסימונים?", 4,
     rv(108, 220, lambda r: (lambda k, n, tc: (k, n, tc) if (k + n - 1) * tc <= 511 else None)(r.randint(2, 5), r.randint(10, 40), r.randint(1, 9))),
     lambda p: [[p[0], p[1] // 10, p[1] % 10, p[2]]], LNT,
     [(["צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:", "HEX3 = stages", "אחרי כמה מחזורים יוצא האסימון הראשון?", "latency = stages"] + cnt(5),
       lambda q, p: (p[0], 0xF)),
      (["צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:", "HEX3 = stages     HEX2 HEX1 = tokens",
        "אחרי כמה מחזורים יוצא האסימון האחרון?", "cycles = stages + tokens - 1"] + binl(6), lambda q, p: (p[0] + p[1] - 1, 0x3F)),
      (["צנרת: אסימון חדש נכנס בכל מחזור. בתצוגה:", LNT,
        "כמה ננו-שניות עד שהאסימון האחרון יוצא?", "t = (stages + tokens - 1) x Tc"] + binl(9),
       lambda q, p: ((p[0] + p[1] - 1) * p[2], 0x1FF))],
     lambda p: f"{p[0] + p[1] - 1} cycles, {(p[0] + p[1] - 1) * p[2]} ns")

# where to put one pipeline register in a chain of 4 gates
def best_cut(p):				# the longer stage for a register after gate 1, 2, 3
    return [max(sum(p[:c]), sum(p[c:4])) for c in (1, 2, 3)]
LRT = "page 1 (SW9 down):  HEX3 HEX2 HEX1 HEX0 = tpd of gates 1, 2, 3, 4 (in series)"
LRTb = "page 2 (SW9 up):    HEX3 = tpcq + tsetup (together)"
numq("RETIME", "איפה לשים את האוגר?", 4,
     rv(109, 220, lambda r: (lambda g, o: g + (o,) if sorted(best_cut(g))[0] < sorted(best_cut(g))[1] else None)(
         tuple(r.randint(1, 9) for _ in range(4)), r.randint(1, 5))),
     lambda p: [list(p[:4]), [p[4], 0, 0, 0]], "the 4 gate delays / tpcq + tsetup",
     [(["שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה שני דפים:", LRT, LRTb, UNIT,
        "מה זמן המחזור עכשיו?", "Tc = tpd1 + tpd2 + tpd3 + tpd4 + tpcq + tsetup"] + BIN6, lambda q, p: (sum(p), 0x3F)),
      (["שרשרת של ארבעה שערים בין שני אוגרים. בתצוגה:", LRT,
        "מוסיפים אוגר אחד בתוך השרשרת. אחרי איזה שער כדאי לשים אותו כדי שזמן המחזור יהיה הקצר ביותר?"] + cnt(3),
       lambda q, p: (1 + best_cut(p).index(min(best_cut(p))), 0xF)),
      (["שרשרת של ארבעה שערים, ואוגר במקום הטוב ביותר. בתצוגה שני דפים:", LRT, LRTb, UNIT,
        "מה זמן המחזור אז?", "Tc = max(stage 1, stage 2) + tpcq + tsetup"] + BIN6,
       lambda q, p: (min(best_cut(p)) + p[4], 0x3F))],
     lambda p: f"cut after {1 + best_cut(p).index(min(best_cut(p)))}, Tc {min(best_cut(p)) + p[4]}", pages2=True)

# the latency of a hidden pipeline, in clocks and in ns (no clock button: the stage registers are on switches, and the
# LED is the output of the last stage)
OPL = [("G", 0)] + hexd(0)
VPL = [(n, tc) for n in (2, 3, 4) for tc in range(2, 10)]
LPL = "stage registers 1..4 = SW9 SW8 SW7 SW6 (1 = a token)     Y = LEDG0 = the output of the last stage"
W.append(Q(id="PIPELAT", name="PIPELAT", title="זמן האחזור של צנרת נסתרת", inputs=[9, 8, 7, 6], flat=True,
    outs=OPL, hexes=[None, None, None, None], variants=VPL,
    tables=lambda p: [[(r >> (4 - p[0])) & 1 for r in range(16)]] + const(bitsof(p[1], 4), 4),
    answer=lambda p: (p[0] * p[1], 0x3F), describe=lambda p: f"{p[0]} stages, Tc {p[1]} ns: {p[0] * p[1]} ns",
    B=[LPL + "     HEX0 = Tc (ns)     answer: SW5..SW0"], L=[], F=[],
    steps=[(["בלוח צנרת נסתרת: בכל עליית שעון אסימון עובר שלב אחד, והיציאה היא האוגר של השלב האחרון.",
             "בלוח מקום ל-4 שלבים, אבל רק חלק מהם קיימים.", LPL,
             "כמה שלבים יש? (כמה עליות שעון לוקח לאסימון לעבור מהכניסה ליציאה)"] + cnt(4), lambda q, p: (p[0], 0xF)),
           (["בתצוגה זמן המחזור:", "HEX0 = Tc (ns)", "מה זמן האחזור בננו-שניות?", "latency = stages x Tc"] + BIN6,
            lambda q, p: (p[0] * p[1], 0x3F))]))

# the shortest and the longest path in the slide code
LHF = "HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     (ns)"
CODE2 = ["assign #d1 {ab, bb, cb} = ~{a, b, c};", "assign #d2 n1 = ab & bb & cb;", "assign #d2 n2 = a & bb & cb;",
         "assign #d2 n3 = a & bb & c;", "assign #d3 y = n1 | n2 | n3;"]
numq("HDLFIRST", "המסלול הקצר בקוד", 3, rv(110, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [list(p)], LHF,
     [(["הקוד מהשקופית, וההשהיות בתצוגה:"] + CODE2 + [LHF,
        "הכניסה השנייה משתנה בזמן 0. מתי היציאה משתנה (בננו-שניות)?", "b -> bb -> n1, n2, n3 -> y"] + BIN6,
       lambda q, p: (sum(p), 0x3F)),
      (["הקוד מהשקופית, וההשהיות בתצוגה:"] + CODE2 + ["HEX2 = #d2     HEX1 = #d3     (ns)",
        "עכשיו הכניסה הראשונה משתנה בזמן 0. מה הרגע המוקדם ביותר שבו היציאה יכולה להשתנות?",
        "the shortest path: a -> n2 -> y"] + BIN6, lambda q, p: (p[1] + p[2], 0x3F))],
     lambda p: f"b: {sum(p)} ns, a earliest: {p[1] + p[2]} ns")

# delays in a testbench: the times add up
LTB = "HEX3 = #d1     HEX2 = #d2     HEX1 = #d3     HEX0 = #dg     (ns)"
TB = ["initial begin", "  a = 0; b = 0;", "  #d1 a = 1;", "  #d2 b = 1;", "  #d3 a = 0;", "end", "assign #dg y = a & b;"]
numq("TBDELAY", "השהיות בקוד בדיקה", 4,
     rv(111, 220, lambda r: (lambda a, b, c, g: (a, b, c, g) if c > g else None)(r.randint(1, 9), r.randint(1, 9), r.randint(2, 9), r.randint(1, 8))),
     lambda p: [list(p)], LTB,
     [(["קוד בדיקה ושער, וההשהיות בתצוגה:"] + TB + ["HEX3 = #d1     HEX2 = #d2     (ns)", "באיזה זמן", "b", "עולה ל-1?", "t = d1 + d2"] + BIN6,
       lambda q, p: (p[0] + p[1], 0x3F)),
      (["קוד בדיקה ושער, וההשהיות בתצוגה:"] + TB + ["HEX3 = #d1     HEX2 = #d2     HEX0 = #dg     (ns)", "באיזה זמן", "y", "עולה ל-1?", "t = d1 + d2 + dg"] + BIN6,
       lambda q, p: (p[0] + p[1] + p[3], 0x3F)),
      (["קוד בדיקה ושער, וההשהיות בתצוגה:"] + TB + [LTB, "באיזה זמן", "y", "חוזרת ל-0?", "t = d1 + d2 + d3 + dg"] + BIN6,
       lambda q, p: (sum(p), 0x3F))],
     lambda p: f"b at {p[0] + p[1]}, y 1 at {p[0] + p[1] + p[3]}, y 0 at {sum(p)}")

# ================================================================ easy questions straight from the slides (first in each topic)
# topic 1: the slide 10-11 circuit (A, B -> AND -> OR -> NOR -> Y'; the short path C -> OR -> X')
LONG10 = "A -> AND -> OR -> NOR -> Y'"
LT10 = "HEX3 = tpcq     HEX2 = tpd of one gate     HEX1 = tsetup"
numq("SLIDE10TC", "המעגל משקופית 10: זמן המחזור", 3, rv(121, 200, lambda r: (r.randint(1, 9), r.randint(1, 9), r.randint(1, 9))),
     lambda p: [list(p)], LT10,
     [(["המעגל משקופית 10: המסלול הארוך עובר דרך שלושה שערים.", LONG10, "בתצוגה ההשהיה של שער אחד:", "HEX2 = tpd of one gate", UNIT,
        "מה ההשהיה של כל המסלול הארוך?", "tpd = 3 x tpd(gate)"] + binl(5), lambda q, p: (3 * p[1], 0x1F)),
      (["המעגל משקופית 10, וההשהיות בתצוגה:", LONG10, LT10, UNIT,
        "מה זמן המחזור המינימלי?", "Tc >= tpcq + 3 x tpd(gate) + tsetup"] + BIN6, lambda q, p: (p[0] + 3 * p[1] + p[2], 0x3F))],
     lambda p: f"tpd {3 * p[1]}, Tc {p[0] + 3 * p[1] + p[2]}")

LH10 = "HEX3 = tccq     HEX2 = tcd of one gate     HEX1 = thold"
VH10 = rv(122, 200, lambda r: (lambda a, b, c: (a, b, c) if a + b != c and a + 2 * b != c else None)(r.randint(1, 6), r.randint(1, 5), r.randint(2, 9)))
numq("SLIDE10HOLD", "המעגל משקופית 10: אילוץ ההחזקה", 3, VH10, lambda p: [list(p)], LH10,
     [(["המעגל משקופית 10: המסלול הקצר עובר דרך שער אחד בלבד.", "C -> OR -> X'", "בתצוגה:", LH10, UNIT,
        "האם אילוץ ההחזקה מתקיים?", "tccq + tcd > thold"] + UP0("מתקיים", "לא מתקיים"), lambda q, p: (int(p[0] + p[1] > p[2]), 0x1))],
     lambda p: f"tccq + tcd = {p[0] + p[1]} vs thold {p[2]}")

numq("SLIDE11FIX", "התיקון משקופית 11: מאגר במסלול הקצר", 3, VH10, lambda p: [list(p)], LH10,
     [(["התיקון משקופית 11: מוסיפים מאגר במסלול הקצר, ועכשיו יש בו שני שערים.", "C -> BUF -> OR -> X'",
        "בתצוגה ההשהיה של שער אחד:", "HEX2 = tcd of one gate", UNIT,
        "מה ההשהיה הקצרה ביותר של המסלול הקצר עכשיו?", "tcd = 2 x tcd(gate)"] + BIN4, lambda q, p: (2 * p[1], 0xF)),
      (["התיקון משקופית 11: במסלול הקצר שני שערים.", "C -> BUF -> OR -> X'", "בתצוגה:", LH10, UNIT,
        "האם אילוץ ההחזקה מתקיים עכשיו?", "tccq + 2 x tcd(gate) > thold"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] + 2 * p[1] > p[2]), 0x1))],
     lambda p: f"tcd {2 * p[1]}, tccq + tcd = {p[0] + 2 * p[1]} vs thold {p[2]}")

# topic 2: skew (slides 14, 15) and the synchronizer example (slides 22, 26)
L14a = "HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup"
L14 = "HEX3 = tpcq     HEX2 = tpd     HEX1 = tsetup     HEX0 = tskew"
numq("SKEW14", "שקופית 14: השעון השני מקדים", 4, rv(123, 200, lambda r: tuple(r.randint(1, 9) for _ in range(3)) + (r.randint(1, 5),)),
     lambda p: [list(p)], L14,
     [(["השקופית של הטיית שעון (14): מסלול בין שני אוגרים. בתצוגה:", L14a, UNIT,
        "מה זמן המחזור המינימלי בלי הטיה?", "Tc >= tpcq + tpd + tsetup"] + binl(5), lambda q, p: (p[0] + p[1] + p[2], 0x1F)),
      (["השקופית של הטיית שעון (14): השעון של האוגר השני מקדים.", "CLK2 is earlier than CLK1", "בתצוגה:", L14, UNIT,
        "מה זמן המחזור המינימלי עם ההטיה?", "Tc >= tpcq + tpd + tsetup + tskew"] + BIN6, lambda q, p: (sum(p), 0x3F))],
     lambda p: f"Tc {p[0] + p[1] + p[2]} -> {sum(p)}")

L15a = "HEX3 = tccq     HEX2 = tcd     HEX1 = thold"
L15 = "HEX3 = tccq     HEX2 = tcd     HEX1 = thold     HEX0 = tskew"
numq("SKEW15", "שקופית 15: השעון השני מאחר", 4,
     rv(124, 200, lambda r: (lambda a, b, c, s: (a, b, c, s) if a + b > c and a + b != c + s else None)(r.randint(1, 6), r.randint(0, 6), r.randint(1, 9), r.randint(1, 5))),
     lambda p: [list(p)], L15,
     [(["השקופית של הטיית שעון (15): מסלול קצר בין שני אוגרים. בתצוגה:", L15a, UNIT,
        "כמה זמן אחרי עליית השעון הנתון בכניסה של האוגר השני עוד יציב?", "tccq + tcd"] + BIN4, lambda q, p: (p[0] + p[1], 0xF)),
      (["השקופית של הטיית שעון (15): השעון של האוגר השני מאחר.", "CLK2 is later than CLK1", "בתצוגה:", L15, UNIT,
        "האם אילוץ ההחזקה מתקיים עם ההטיה?", "tccq + tcd > thold + tskew"] + UP0("מתקיים", "לא מתקיים"),
       lambda q, p: (int(p[0] + p[1] > p[2] + p[3]), 0x1))],
     lambda p: f"tccq + tcd {p[0] + p[1]} vs thold + tskew {p[2] + p[3]}")

L26a = "HEX3 HEX2 HEX1 = f (MHz)"
L26 = "HEX3 HEX2 HEX1 = f (MHz)     HEX0 = tsetup (ns)"
V26 = [(f, su) for f in (500, 250, 200, 125, 100, 50) for su in range(1, min(9, 1000 // f - 1) + 1)]
numq("SYNC26", "המסנכרן משקופיות 22 ו-26", 4, V26, lambda p: [[p[0] // 100, p[0] // 10 % 10, p[0] % 10, p[1]]], L26,
     [(["המסנכרן משקופיות 22 ו-26: שני דלגלגים בטור, עם שעון בתדר שבתצוגה.", "D -> F1 -> D2 -> F2 -> Q", "בתצוגה:", L26a,
        "מה זמן המחזור (בננו-שניות)? בשקופית 26:", "Tc = 1 / 500 MHz = 2 ns", "Tc = 1000 / f"] + binl(5), lambda q, p: (1000 // p[0], 0x1F)),
      (["המסנכרן משקופיות 22 ו-26: שני דלגלגים בטור.", "D -> F1 -> D2 -> F2 -> Q", "בתצוגה:", L26,
        "כמה זמן יש לאות", "D2", "להתייצב (בננו-שניות)?", "tres = Tc - tsetup = 1000 / f - tsetup"] + binl(5),
       lambda q, p: (1000 // p[0] - p[1], 0x1F))],
     lambda p: f"Tc {1000 // p[0]} ns, tres {1000 // p[0] - p[1]} ns")

# topic 3: Ben's cookies (slides 32, 33) and the slide-36 code with its own delays
LCK = "HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake"
V32 = [(a, b) for a in range(1, 10) for b in range(10, 31) if 120 % (a + b) == 0]
numq("COOKIE32", "העוגיות משקופית 32: בן ואליסה", 3, V32, lambda p: [[p[0], p[1] // 10, p[1] % 10]], LCK,
     [(["העוגיות משקופית 32: בן ואליסה, כל אחד עם תנור משלו, מכינים מגש בבת אחת. בתצוגה:", LCK,
        "מה זמן האחזור של מגש אחד (בדקות)?", "latency = roll + bake"] + BIN6, lambda q, p: (p[0] + p[1], 0x3F)),
      (["העוגיות משקופית 32: בן ואליסה, כל אחד עם תנור משלו. בתצוגה:", LCK,
        "כמה מגשים בשעה שניהם יחד?", "throughput = 2 x 60 / (roll + bake)"] + BIN4, lambda q, p: (120 // (p[0] + p[1]), 0xF))],
     lambda p: f"latency {p[0] + p[1]}, {120 // (p[0] + p[1])}/h")

V33 = [(a, b) for a in range(1, 10) for b in range(10, 21)]
numq("COOKIE33", "העוגיות משקופית 33: צנרת", 3, V33, lambda p: [[p[0], p[1] // 10, p[1] % 10]], LCK,
     [(["העוגיות משקופית 33: בן לבד עם שני מגשים. בזמן שמגש אחד בתנור, הוא מכין את הבא. בתצוגה:", LCK,
        "מתי מגש 1 יוצא מהתנור (בדקות מההתחלה)?", "t1 = roll + bake"] + BIN6, lambda q, p: (p[0] + p[1], 0x3F)),
      (["העוגיות משקופית 33: מגש 2 נכנס לתנור כשמגש 1 יוצא. בתצוגה:", LCK,
        "מתי מגש 2 יוצא מהתנור?", "t2 = roll + 2 x bake"] + BIN6, lambda q, p: (p[0] + 2 * p[1], 0x3F))],
     lambda p: f"tray 1 at {p[0] + p[1]}, tray 2 at {p[0] + 2 * p[1]}")

CODE36 = ["assign #1 {ab, bb, cb} = ~{a, b, c};", "assign #2 n1 = ab & bb & cb;", "assign #2 n2 = a & bb & cb;",
          "assign #2 n3 = a & bb & c;", "assign #4 y = n1 | n2 | n3;"]
L36 = "HEX3 HEX2 = the time c changes (ns)"
SC36 = "a = 0     b = 0     c: 0 -> 1"
numq("HDL36", "הקוד משקופית 36: מתי היציאה משתנה", 2, list(range(10, 90)), lambda p: [[p // 10, p % 10]], L36,
     [(["הקוד משקופית 36, עם ההשהיות שלו:"] + CODE36 + ["כמו בסימולציה בשקופית:", SC36, "בתצוגה:", L36,
        "באיזה זמן", "cb", "משתנה?", "t + 1"] + binl(7), lambda q, p: (p + 1, 0x7F)),
      (["הקוד משקופית 36, עם ההשהיות שלו:"] + CODE36 + ["כמו בסימולציה בשקופית:", SC36, "בתצוגה:", L36,
        "השינוי עובר דרך", "n1", "ומשנה את היציאה. באיזה זמן", "y", "משתנה?", "c -> cb -> n1 -> y", "t + 1 + 2 + 4"] + binl(7),
       lambda q, p: (p + 7, 0x7F))],
     lambda p: f"c at {p}: cb {p + 1}, y {p + 7}")

# ================================================================ more easy questions from the slides (after the slide questions above)
# topic 1: tccq / tpcq (slide 4), the sequencing overhead (slide 7), the min / max path (slide 6)
L4Q = "HEX3 = tccq     HEX2 = tpcq"
numq("TCQ4", "שקופית 4: מתי היציאה משתנה", 2,
     rv(131, 200, lambda r: (lambda a, b: (a, b) if a < b else None)(r.randint(1, 8), r.randint(2, 9))),
     lambda p: [list(p)], L4Q,
     [(["השקופית של זמני היציאה של דלגלג (4): אחרי עליית השעון", "Q",
        "יכול להתחיל להשתנות אחרי", "tccq", "ובטוח יציב אחרי", "tpcq", "בשקופית 10:", "tccq = 30 ps     tpcq = 50 ps  ->  20 ps",
        "בתצוגה:", L4Q, UNIT, "כמה זמן", "Q", "עלול להשתנות?", "t = tpcq - tccq"] + BIN4,
       lambda q, p: (p[1] - p[0], 0xF))],
     lambda p: f"tccq {p[0]} tpcq {p[1]}: {p[1] - p[0]}")

L7a = "HEX3 = tpcq     HEX2 = tsetup"
L7 = "HEX3 = tpcq     HEX2 = tsetup     HEX1 = tpd of the logic"
numq("OVERHEAD7", "שקופית 7: התקורה של האוגרים", 3,
     rv(132, 200, lambda r: (lambda a, b, c: (a, b, c) if a + b != c else None)(r.randint(1, 7), r.randint(1, 7), r.randint(2, 14))),
     lambda p: [list(p)], L7,
     [(["השקופית של אילוץ ההתקנה (7): החלק של האוגרים בזמן המחזור נקרא תקורה.", "sequencing overhead = tpcq + tsetup",
        "בתצוגה:", L7a, UNIT, "מה התקורה?"] + binl(5), lambda q, p: (p[0] + p[1], 0x1F)),
      (["בדוגמה משקופית 10 התקורה גדולה מהלוגיקה:", "50 + 60 = 110 ps > tpd = 105 ps", "בתצוגה:", L7, UNIT,
        "האם התקורה גדולה מההשהיה של הלוגיקה?", "tpcq + tsetup > tpd"] + UP0("גדולה", "לא גדולה"),
       lambda q, p: (int(p[0] + p[1] > p[2]), 0x1))],
     lambda p: f"overhead {p[0] + p[1]} vs tpd {p[2]}")

L6P = "HEX3 = delay of path A     HEX2 = delay of path B     HEX1 = delay of path C"
numq("PATHS6", "שקופית 6: איזה מסלול לכל אילוץ", 3,
     rv(135, 200, lambda r: tuple(r.sample(range(1, 10), 3))),
     lambda p: [list(p)], L6P,
     [(["השקופית של המשמעת הדינמית (6): בין שני אוגרים יש השהיה מקסימלית ומינימלית.", "R1 -> CL -> R2",
        "בתצוגה ההשהיות של שלושה מסלולים בין שני האוגרים:", L6P, UNIT,
        "איזה מסלול בודקים באילוץ ההתקנה?", "setup: the maximum delay"] + code(["path A", "path B", "path C"]),
       lambda q, p: (p.index(max(p)), 0x3)),
      (["אותם שלושה מסלולים בין שני האוגרים:", L6P, UNIT,
        "איזה מסלול בודקים באילוץ ההחזקה?", "hold: the minimum delay"] + code(["path A", "path B", "path C"]),
       lambda q, p: (p.index(min(p)), 0x3))],
     lambda p: f"setup path {'ABC'[p.index(max(p))]}, hold path {'ABC'[p.index(min(p))]}")

# topic 2: the skew between clock edges (slide 13), an asynchronous input (slide 17), failures per second (slide 26)
L13 = "HEX3 = CLK arrives at R1     HEX2 = CLK arrives at R2     HEX1 = CLK arrives at R3"
L13b = "HEX3 = CLK arrives at R1     HEX2 = CLK arrives at R2"
numq("SKEW13", "שקופית 13: מה ההטיה?", 3,
     rv(133, 200, lambda r: (lambda a, b, c: (a, b, c) if a != b else None)(r.randint(0, 9), r.randint(0, 9), r.randint(0, 9))),
     lambda p: [list(p)], L13,
     [(["השקופית של הטיית שעון (13): השעון לא מגיע לכל האוגרים באותו זמן.", "tskew = the difference between two clock edges",
        "בתצוגה מתי השעון מגיע לשלושה אוגרים:", L13, UNIT,
        "מה ההטיה במקרה הגרוע ביותר?", "tskew = latest - earliest"] + BIN4, lambda q, p: (max(p) - min(p), 0xF)),
      (["מסלול מהאוגר הראשון לשני. בתצוגה:", L13b, UNIT,
        "איזה אילוץ בסכנה? (השעון השני מקדים - התקנה, שקופית 14; מאחר - החזקה, שקופית 15)"] + code(["setup", "hold"]),
       lambda q, p: (int(p[1] > p[0]), 0x1))],
     lambda p: f"skew {max(p) - min(p)}, R1->R2: {'hold' if p[1] > p[0] else 'setup'}")

L17 = "HEX3 = thold     HEX2 = when the button changes, after the clock edge"
numq("ASYNC17", "שקופית 17: לחצן אסינכרוני", 2,
     rv(134, 200, lambda r: (lambda h, t: (h, t) if h != t else None)(r.randint(1, 9), r.randint(0, 9))),
     lambda p: [list(p)], L17,
     [(["השקופית של הפרת המשמעת הדינמית (17): משתמש לוחץ על לחצן בזמן אקראי, בלי קשר לשעון.",
        "בתצוגה זמן ההחזקה של הדלגלג, ומתי הלחצן משתנה אחרי עליית השעון:", L17, UNIT,
        "האם השינוי מפר את אילוץ ההחזקה?", "violation: change time < thold"] + UP0("מפר", "בסדר"),
       lambda q, p: (int(p[1] < p[0]), 0x1))],
     lambda p: f"thold {p[0]}, change {p[1]}: {'violation' if p[1] < p[0] else 'ok'}")

L26P = "HEX3 = N (input changes per second)     HEX2 = K"
L26K = "P(failure) per change = K x 10^-6"
numq("SLIDE26P", "שקופית 26: כשלים בשנייה", 2,
     [(n, k) for n in range(1, 10) for k in range(1, 10)],
     lambda p: [list(p)], L26P,
     [(["הדוגמה משקופית 26: הסיכוי לכשל בכל שינוי של הכניסה, כפול מספר השינויים בשנייה.",
        "N = 10     P = 5.6 x 10^-6  ->  5.6 x 10^-5 / second", "בתצוגה:", L26P, L26K,
        "מה הסיכוי לכשל בשנייה? כתבו את המספר שלפני", "x 10^-6", "P(failure)/second = N x K x 10^-6"] + binl(7),
       lambda q, p: (p[0] * p[1], 0x7F))],
     lambda p: f"{p[0] * p[1]} x 10^-6 / s")

# topic 3: many trays (slides 30, 32), the input a in the slide-36 code (slides 38-39)
LKT = "HEX3 = minutes to roll     HEX2 HEX1 = minutes to bake     HEX0 = trays"
VKT = [(a, b, n) for a in range(1, 10) for b in (10, 12, 15, 18, 20) for n in (2, 4, 6, 8)]
numq("COOKIE30K", "העוגיות משקופיות 30 ו-32: כמה מגשים", 4, VKT, lambda p: [[p[0], p[1] // 10, p[1] % 10, p[2]]], LKT,
     [(["העוגיות משקופית 30: בן לבד, בלי מקביליות - מגש אחד בכל פעם. בתצוגה:", LKT,
        "כמה דקות לוקח להכין את כל המגשים?", "t = trays x (roll + bake)"] + binl(8), lambda q, p: (p[2] * (p[0] + p[1]), 0xFF)),
      (["העוגיות משקופית 32: אליסה עוזרת עם תנור משלה, וכל אחד מכין חצי מהמגשים. בתצוגה:", LKT,
        "כמה דקות עכשיו?", "t = trays / 2 x (roll + bake)"] + binl(8), lambda q, p: (p[2] // 2 * (p[0] + p[1]), 0xFF))],
     lambda p: f"{p[2] * (p[0] + p[1])} min alone, {p[2] // 2 * (p[0] + p[1])} min with Alyssa")

L39 = "HEX3 HEX2 = the time a changes (ns)"
SC39 = "b = 0     c = 0     a: 0 -> 1"
numq("HDL39", "הקוד משקופיות 38-39: הכניסה a", 2, list(range(10, 90)), lambda p: [[p // 10, p % 10]], L39,
     [(["הקוד משקופית 36, עם ההשהיות שלו:"] + CODE36 + ["כמו בשקופית 39, הכניסה", "a", "נכנסת ישר לשער של", "n2", SC39,
        "בתצוגה:", L39, "באיזה זמן", "n2", "משתנה?", "a -> n2", "t + 2"] + binl(7), lambda q, p: (p + 2, 0x7F)),
      (["הקוד משקופית 36, עם ההשהיות שלו:"] + CODE36 + [SC39, "בתצוגה:", L39,
        "אל", "n1", "השינוי מגיע דרך המהפך (שקופית 38). באיזה זמן", "n1", "משתנה?", "a -> ab -> n1", "t + 1 + 2"] + binl(7),
       lambda q, p: (p + 3, 0x7F))],
     lambda p: f"a at {p}: n2 {p + 2}, n1 {p + 3}")

ORDER = ["SLIDE10TC", "SLIDE10HOLD", "SLIDE11FIX", "TCQ4", "OVERHEAD7", "PATHS6", "TCMIN", "TWOPATHS", "TPDMAX", "GATESMAX", "FMAX", "HOLDOK", "SLACK", "EXAMPLE", "EXAMPLE3", "BUFFERS",
         "SKEW14", "SKEW15", "SYNC26", "SKEW13", "ASYNC17", "SLIDE26P", "APERTURE", "SKEWSETUP", "SKEWMAX", "SKEWFIX", "SKEWSLACK", "SKEWCHECK", "SYNC", "SYNCLAT", "RESOLVE", "MTBFGROW", "MTBF",
         "COOKIE32", "COOKIE33", "HDL36", "COOKIE30K", "HDL39", "LATENCY", "SPATIAL", "BOTH", "PIPECLK", "PIPESPLIT", "NTOKENS", "RETIME", "PIPESIM", "PIPELAT", "HDLDELAY", "HDLFIRST", "TBDELAY"]
TOPICS = [(40, "זמני התקנה והחזקה", 16), (40, "חלון הדגימה, הטיית שעון ומסנכרנים", 17), (40, "מקביליות והשהיות בקוד", 17)]
DESC = {"TCQ4": "שקופית 4: כמה זמן היציאה של הדלגלג עלולה להשתנות",
        "OVERHEAD7": "שקופית 7: התקורה של האוגרים לעומת הלוגיקה",
        "PATHS6": "שקופית 6: איזה מסלול בודקים בכל אילוץ",
        "SKEW13": "שקופית 13: ההטיה במקרה הגרוע, ואיזה אילוץ בסכנה",
        "ASYNC17": "שקופית 17: לחצן אסינכרוני ואילוץ ההחזקה",
        "SLIDE26P": "שקופית 26: הסיכוי לכשל בשנייה",
        "COOKIE30K": "העוגיות משקופיות 30 ו-32: כמה זמן לכמה מגשים",
        "HDL39": "הקוד משקופיות 38-39: מתי n1 ו-n2 משתנים כשהכניסה הראשונה משתנה",
        "SLIDE10HOLD": "המעגל משקופית 10: אילוץ ההחזקה במסלול הקצר",
        "SLIDE10TC": "המעגל משקופית 10: ההשהיה של המסלול הארוך וזמן המחזור",
        "SLIDE11FIX": "התיקון משקופית 11: מאגר במסלול הקצר",
        "SKEW14": "שקופית 14: זמן המחזור כשהשעון השני מקדים",
        "SKEW15": "שקופית 15: אילוץ ההחזקה כשהשעון השני מאחר",
        "SYNC26": "המסנכרן משקופיות 22 ו-26: זמן המחזור וזמן ההתייצבות",
        "COOKIE32": "העוגיות משקופית 32: אחזור וקצב של בן ואליסה",
        "COOKIE33": "העוגיות משקופית 33: מתי כל מגש יוצא מהתנור",
        "HDL36": "הקוד משקופית 36: מתי האותות משתנים",
        "TCMIN": "זמן המחזור המינימלי של מסלול",
        "TPDMAX": "ההשהיה המותרת ללוגיקה בזמן מחזור נתון",
        "FMAX": "זמן המחזור והתדר המקסימלי",
        "APERTURE": "חלון הדגימה, והאם שינוי של הנתון מסוכן",
        "SYNCLAT": "כמה זמן לוקח לסנכרן",
        "BOTH": "מקביליות מרחבית וזמנית יחד",
        "HOLDOK": "אילוץ ההחזקה, וה-tcd המינימלי",
        "SLACK": "האם המעגל עומד בזמן, ובכמה",
        "EXAMPLE": "הדוגמה מהשקופית: שני שערים בטור - התקנה והחזקה",
        "BUFFERS": "כמה מאגרים לתקן הפרת החזקה",
        "SKEWSETUP": "זמן המחזור והחזקה עם הטיית שעון",
        "SKEWMAX": "כמה הטיה אילוץ ההחזקה מרשה",
        "SKEWSLACK": "כמה הטיה אילוץ ההתקנה מרשה",
        "SYNC": "מסנכרן: מה היציאה מעתיקה, כמה דלגלגים, האם מספיק",
        "RESOLVE": "זמן ההתייצבות במסנכרן",
        "LATENCY": "עוגיות: זמן אחזור וקצב, עם צנרת ובלי",
        "SPATIAL": "מקביליות מרחבית: קצב ואחזור",
        "PIPECLK": "צנרת: זמן מחזור וזמן אחזור",
        "PIPESIM": "צנרת על הלוח: השלבים אחרי עליית שעון - כמה שלבים, כמה אסימונים",
        "HDLDELAY": "השהיות בקוד: מתי היציאה משתנה",
        "TWOPATHS": "שני מסלולים: מי קובע את זמן המחזור",
        "GATESMAX": "כמה שערים בטור נכנסים במחזור",
        "EXAMPLE3": "הדוגמה מהשקופית עם יותר שערים: התקנה, החזקה, ה-tcd המינימלי",
        "SKEWFIX": "כמה מאגרים לתקן הפרת החזקה בגלל הטיה",
        "SKEWCHECK": "הטיה לשני הכיוונים: התקנה, החזקה, ההטיה המותרת",
        "MTBFGROW": "כמה עוזר עוד דלגלג במסנכרן",
        "MTBF": "הזמן הממוצע בין כשלים",
        "PIPESPLIT": "חלוקת מעגל לשלבים שווים: זמן מחזור ואחזור",
        "NTOKENS": "כמה מחזורים וננו-שניות לכמה אסימונים בצנרת",
        "RETIME": "איפה לשים אוגר צנרת בשרשרת שערים",
        "PIPELAT": "צנרת נסתרת על הלוח: שלבים ואחזור בננו-שניות",
        "HDLFIRST": "המסלול הקצר והארוך בקוד מהשקופית",
        "TBDELAY": "השהיות בקוד בדיקה: מתי כל אות משתנה"}
W = C.order(W, ORDER)
if __name__ == "__main__":
    C.main(W, TOPICS, DESC, "תזמון, מסנכרנים ומקביליות - מהקל אל הקשה, ואי אפשר בלי הלוח")
