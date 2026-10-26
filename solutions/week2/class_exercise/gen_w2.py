# -*- coding: utf-8 -*-
# Week 2 class exercise (lecture 2, Harris ch. 1: number systems, addition, signed numbers, extension, gates, CMOS).
# Same engine as lecture 3 (C:/DE10/solutions/class_exercise/gen.py, imported): one board design, steps, PC link,
# Hebrew screens. Instructor only.
#   python gen_w2.py                 simulate every question (iverilog) and write the student files
#   python gen_w2.py --compile       also compile with Quartus and copy sof/Qnn.sof to C:/DE10/week2/class_exercise
#   python gen_w2.py --only Q05      one question
#   python gen_w2.py --id <ID>       a student's answers and codes;  --answers <ID> = the student in the guide
import argparse, itertools, os, random, sys
sys.path.insert(0, "C:/DE10/solutions/class_exercise")
import gen as G

HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
G.LECTURE = "2"
G.PREFIX = "w2|"				# other codes / variants than lecture 3
G.REPO = "C:/DE10/solutions/de1/week2"	# the DE1 build, not the repo week
G.HERE = HERE					# build/, answers and the guide go here
G.EXPLAIN_FILE = f"{HERE}/explain_w2.py"
Q, HOLD = G.Q, G.HOLD
rng = random.Random(202)

def hexd(d):					# the 4 outputs of one 7-segment digit
    return [("H", (d, b)) for b in range(4)]
def bitsof(v, n):
    return [(v >> b) & 1 for b in range(n)]
def const(vals):				# a display with no real input: one dummy input (SW9), the same in both rows
    return [[x, x] for x in vals]
DIG = ["0 = all down    1 = SW0    2 = SW1    3 = SW1+SW0    4 = SW2",
       "5 = SW2+SW0    6 = SW2+SW1    7 = SW2+SW1+SW0    8 = SW3    9 = SW3+SW0"]
BIN4 = ["8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
ROWS3 = ["SW9 SW8 SW7:   000   001   010   011   100   101   110   111      (0 = down, 1 = up)"]
POS4 = ["1st -> SW0     2nd -> SW1     3rd -> SW2     4th -> SW3"]
def tw(v, n=4):				# two's complement bits of v in n bits
    return v & ((1 << n) - 1)
def sval(v):				# 4-bit two's complement value
    return v - 16 if v & 8 else v

W = []
# ================================================================ topic 1: number systems
# Q01 decimal -> binary
V = list(range(20, 100))
W.append(Q(id="Q01", name="DEC2BIN", title="מעשרוני לבינארי", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v // 10, 4) + bitsof(v % 10, 4)),
    answer=lambda v: (v, 0x7F), describe=lambda v: f"the number {v} = {v:07b}",
    B=["the number = HEX1 HEX0 (decimal)     answer: SW6..SW0"], L=[], F=[],
    steps=[(["בלוח מוצג מספר עשרוני, בשתי הספרות הימניות של התצוגה.",
             "האם הוא אי-זוגי? (מספר אי-זוגי = הביט הימני שלו 1)",
             "אי-זוגי - הרימו:", "SW0", "זוגי - השאירו למטה."], lambda q, v: (v & 1, 0x1)),
           (["שיטה 1: מה החזקה הגדולה ביותר של 2 שנכנסת במספר?",
             "64 = SW6     32 = SW5     16 = SW4     8 = SW3",
             "הרימו רק את המתג שלה."], lambda q, v: (1 << (v.bit_length() - 1), 0x7F)),
           (["המספר כולו בבינארי: הורידו את החזקה, ומהשארית - שוב החזקה הגדולה שנכנסת, וכך הלאה.",
             "64 = SW6   32 = SW5   16 = SW4   8 = SW3   4 = SW2   2 = SW1   1 = SW0",
             "הרימו את המתגים של כל החזקות שהשתמשתם בהן."], lambda q, v: (v, 0x7F))]))

# Q02 hex -> binary
V = list(range(0x10, 0x100))
W.append(Q(id="Q02", name="HEX2BIN", title="מהקסדצימלי לבינארי", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v >> 4, 4) + bitsof(v & 15, 4)),
    answer=lambda v: (v, 0xFF), describe=lambda v: f"0x{v:02X} = {v:08b}",
    B=["the number = HEX1 HEX0 (hex)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח מוצג מספר הקסדצימלי בשתי ספרות.", "כתבו בבינארי (4 ביטים) את הספרה הימנית:", "HEX0"] + BIN4 +
            ["A = 10   B = 11   C = 12   D = 13   E = 14   F = 15"], lambda q, v: (v & 15, 0xF)),
           (["עכשיו את הספרה השמאלית, בבינארי:", "HEX1"] + BIN4 +
            ["A = 10   B = 11   C = 12   D = 13   E = 14   F = 15"], lambda q, v: (v >> 4, 0xF)),
           (["כל המספר: שתי ספרות הקס = 8 ביטים (בייט). הספרה השמאלית על ארבעת המתגים העליונים:",
             "HEX1 -> SW7 SW6 SW5 SW4      HEX0 -> SW3 SW2 SW1 SW0"], lambda q, v: (v, 0xFF))]))

# Q03 binary -> decimal
V = rng.sample(range(256), 256)
W.append(Q(id="Q03", name="BIN2DEC", title="מבינארי לעשרוני", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 8)), answer=lambda v: (v % 10, 0xF),
    describe=lambda v: f"{v:08b} = {v}",
    B=["the number = LEDG7..LEDG0 (LEDG0 = 1, LEDG1 = 2, LEDG2 = 4 ... LEDG7 = 128)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בנורות הירוקות מוצג מספר בינארי. חברו את הערכים של הנורות הדולקות.",
             "מה ספרת המאות של המספר העשרוני? (0, 1 או 2)", "0 = all down     1 = SW0     2 = SW1"],
            lambda q, v: (v // 100, 0x3)),
           (["מה ספרת העשרות שלו?"] + DIG, lambda q, v: ((v // 10) % 10, 0xF)),
           (["ומה ספרת האחדות?"] + DIG, lambda q, v: (v % 10, 0xF))]))

# Q04 how many bits / hex digits
V = rng.sample(range(100, 1000), 256)
NB = ["7 = SW2+SW1+SW0     8 = SW3     9 = SW3+SW0     10 = SW3+SW1"]
W.append(Q(id="Q04", name="BITS", title="כמה ביטים צריך?", inputs=[9], flat=True,
    outs=hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v // 100, 4) + bitsof((v // 10) % 10, 4) + bitsof(v % 10, 4)),
    answer=lambda v: ((v.bit_length() + 3) // 4, 0x3),
    describe=lambda v: f"{v} needs {v.bit_length()} bits, {(v.bit_length() + 3) // 4} hex digits",
    B=["the number = HEX2 HEX1 HEX0 (decimal)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מוצג מספר עשרוני בשלוש ספרות.", "כמה ביטים צריך כדי לכתוב אותו בבינארי?",
             "כמה ביטים מספיקים לכל גודל:",
             "7 bits -> 127      8 bits -> 255      9 bits -> 511      10 bits -> 1023",
             "שימו את מספר הביטים:"] + NB, lambda q, v: (v.bit_length(), 0xF)),
           (["כמה ספרות הקס צריך? כל ספרת הקס היא 4 ביטים.", "2 = SW1     3 = SW1 + SW0"],
            lambda q, v: ((v.bit_length() + 3) // 4, 0x3))]))

# ================================================================ topic 2: addition, signed numbers, extension
# Q05 a hidden adder: S = A + K, carry
V = list(range(1, 16))
def add_tab(k):
    s = [(a + k) & 15 for a in range(16)]
    c = [(a + k) >> 4 for a in range(16)]
    return [[(x >> b) & 1 for x in s] for b in range(4)] + [c]
W.append(Q(id="Q05", name="ADDER", title="מחבר עם מספר מוסתר", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, [9, 8, 7, 6]], variants=V,
    tables=add_tab, answer=lambda k: ((15 + k) & 15, 0xF), describe=lambda k: f"K = {k}",
    B=["A = SW9 SW8 SW7 SW6 (HEX0)     sum = LEDG3..LEDG0     carry = LEDG4     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הלוח מחבר לכניסה מספר מוסתר, ומראה את הסכום (4 ביטים) ואת הנשא.",
             "שימו את ארבעת מתגי הכניסה למטה:", "SW9 SW8 SW7 SW6 = 0000",
             "עכשיו הנורות מראות 0 ועוד המספר המוסתר - כלומר את המספר עצמו. העתיקו אותו:",
             "SW3..SW0 = LEDG3..LEDG0"], lambda q, k: (k, 0xF)),
           (["גלישה: כשהסכום גדול מ-15 הוא לא נכנס ב-4 ביטים, ונורת הנשא נדלקת:", "LEDG4",
             "מה הכניסה הקטנה ביותר שמדליקה אותה? שימו אותה:", "SW3..SW0"] + BIN4,
            lambda q, k: (16 - k, 0xF)),
           (["הרימו את ארבעת מתגי הכניסה:", "SW9 SW8 SW7 SW6 = 1111",
             "מה מראות ארבע נורות הסכום? העתיקו:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, k: ((15 + k) & 15, 0xF))]))

# Q06 sign / magnitude
V = [v for v in range(16) if v != 8]
def sm_val(v):
    return -(v & 7) if v & 8 else v & 7
BITS4 = [("H", (3, 0)), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))]	# 4 bits as 0 / 1 on HEX3..HEX0
SMLEG = ["the number = HEX3 HEX2 HEX1 HEX0  (also on LEDG3..LEDG0)", "HEX3 = the sign bit     HEX2 HEX1 HEX0 = the magnitude"]
SMEX = ["1101 = -5     0101 = +5"]
W.append(Q(id="Q06", name="SIGNMAG", title="סימן וגודל", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)] + BITS4, hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 4) + [(v >> 3) & 1, (v >> 2) & 1, (v >> 1) & 1, v & 1]),
    answer=lambda v: (tw(sm_val(v)), 0xF),
    describe=lambda v: f"{v:04b} = {sm_val(v)} -> two's complement {tw(sm_val(v)):04b}",
    B=["the number = HEX3..HEX0 (HEX3 = sign, HEX2..HEX0 = magnitude)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר בשיטת סימן וגודל, 4 ביטים. הספרה השמאלית היא ביט הסימן, ושלוש הימניות הן הגודל:"] + SMLEG +
            ["סימן 1 = שלילי, סימן 0 = חיובי. למשל:"] + SMEX +
            ["האם המספר שבתצוגה שלילי?", "שלילי - הרימו:", "SW0", "חיובי - השאירו למטה."],
            lambda q, v: ((v >> 3) & 1, 0x1)),
           (["מה הגודל של המספר (שלוש הספרות הימניות בתצוגה)? שימו אותו:"] + SMLEG + SMEX +
            ["4 = SW2     2 = SW1     1 = SW0"], lambda q, v: (v & 7, 0x7)),
           (["כתבו את אותו מספר בשיטה אחרת: משלים ל-2, ב-4 ביטים."] + SMLEG +
            ["מספר חיובי - אותם ביטים בדיוק. למשל:", "+5 = 0101",
             "מספר שלילי - כתבו את הגודל ב-4 ביטים, הפכו את כל הביטים, ואז הוסיפו 1. למשל מינוס 5:",
             "magnitude 0101  ->  flip 1010  ->  + 1  =  1011",
             "SW3..SW0"] + BIN4, lambda q, v: (tw(sm_val(v)), 0xF))]))

# Q07 two's complement
V = list(range(16))
W.append(Q(id="Q07", name="TWOS", title="משלים ל-2", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (tw(-sval(v)), 0xF),
    describe=lambda v: f"{v:04b} = {sval(v)}",
    B=["the number = LEDG3..LEDG0 (two's complement, 4 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בנורות מספר במשלים ל-2 (4 ביטים). הנורה השמאלית 1 = שלילי.",
             "שלילי - הרימו:", "SW0", "חיובי - השאירו למטה."], lambda q, v: ((v >> 3) & 1, 0x1)),
           (["מה הערך המוחלט שלו?", "שלילי - הפכו את כל הביטים והוסיפו 1. חיובי - הוא כמו שהוא.",
             "SW3..SW0"] + BIN4, lambda q, v: (abs(sval(v)), 0xF)),
           (["הפכו את הסימן שלו (הפכו את כל הביטים והוסיפו 1), ב-4 ביטים:", "SW3..SW0"],
            lambda q, v: (tw(-sval(v)), 0xF))]))

# Q08 a signed decimal -> two's complement (4 and 8 bits)
V = list(range(-8, 8))
W.append(Q(id="Q08", name="NEGATIVE", title="מספר שלילי בבינארי", inputs=[9], flat=True,
    outs=[("M", 1)] + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const([1 if v < 0 else 0] + bitsof(abs(v), 4)), answer=lambda v: (tw(v, 8), 0xFF),
    describe=lambda v: f"{v} = {tw(v):04b} = {tw(v, 8):08b}",
    B=["the number = HEX1 HEX0 (decimal, a minus on HEX1 if negative)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח מספר עשרוני עם סימן. כתבו אותו במשלים ל-2, ב-4 ביטים:",
             "שלילי: כתבו את הערך המוחלט, הפכו את כל הביטים והוסיפו 1.", "SW3..SW0"] + BIN4,
            lambda q, v: (tw(v), 0xF)),
           (["ועכשיו ב-8 ביטים: העתיקו את 4 הביטים, ומלאו את 4 העליונים בביט הסימן (הביט השמאלי):",
             "SW7..SW0"], lambda q, v: (tw(v, 8), 0xFF))]))

# Q09 subtraction: A - B = A + (-B)
V = [(a, b) for a in range(8) for b in range(8)]
W.append(Q(id="Q09", name="SUBTRACT", title="חיסור במשלים ל-2", inputs=[9], flat=True,
    outs=hexd(3) + [("M", 2)] + hexd(1), hexes=[None, None, None, None], variants=V,
    tables=lambda p: const(bitsof(p[0], 4) + [1] + bitsof(p[1], 4)), answer=lambda p: (tw(p[0] - p[1]), 0xF),
    describe=lambda p: f"{p[0]} - {p[1]} = {p[0] - p[1]} = {tw(p[0] - p[1]):04b}",
    B=["the exercise = HEX3 - HEX1     answer: SW3..SW0 (two's complement, 4 bits)"], L=[], F=[],
    steps=[(["בלוח תרגיל חיסור. חיסור = חיבור של המספר הנגדי.",
             "מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.", "במשלים ל-2 מוצאים את הנגדי כך: הופכים את כל הביטים (0 ל-1 ו-1 ל-0), ואז מוסיפים 1.",
             "שלב 1: כתבו את המספר הנגדי למספר הימני (הפכו את כל הביטים והוסיפו 1), ב-4 ביטים:",
             "SW3..SW0"] + BIN4, lambda q, p: (tw(-p[1]), 0xF)),
           (["שלב 2: חברו את המספר השמאלי ואת התוצאה של שלב 1. שמרו רק 4 ביטים (הנשא נזרק):",
             "SW3..SW0"], lambda q, p: (tw(p[0] - p[1]), 0xF))]))

# Q10 sign / zero extension
V = list(range(16))
W.append(Q(id="Q10", name="EXTEND", title="הרחבת סימן והרחבה באפסים", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (v, 0xFF),
    describe=lambda v: f"{v:04b} -> sign {tw(sval(v), 8):08b}, zero {v:08b}",
    B=["the number = LEDG3..LEDG0 (4 bits)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בנורות מספר של 4 ביטים. הרחבת סימן ל-8 ביטים:",
             "העתיקו את 4 הביטים למתגים התחתונים, ומלאו את 4 העליונים בביט השמאלי (ביט הסימן):",
             "SW7..SW0"], lambda q, v: (tw(sval(v), 8), 0xFF)),
           (["הרחבה באפסים ל-8 ביטים: 4 הביטים למטה, ו-4 העליונים תמיד 0:", "SW7..SW0"],
            lambda q, v: (v, 0xFF))]))

# ================================================================ topic 3: gates and CMOS
GATES2 = G.GATES
W.append(Q(id="Q11", name="GATE2", title="איזה שער מוסתר בלוח?", inputs=[9, 8], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=list(range(6)),
    tables=lambda p: [GATES2[p][1]], answer=lambda p: (p, 0x7), describe=lambda p: GATES2[p][0],
    B=["A = SW9     B = SW8     Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער של שתי כניסות. נסו את 4 המצבים ורשמו בכל אחד אם הנורה דולקת:",
             "SW9 SW8:   down-down,   down-up,   up-down,   up-up",
             "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4,
            lambda q, p: (sum(GATES2[p][1][r] << r for r in range(4)), 0xF)),
           (["איזה שער זה? הרימו את המתגים שלו:",
             "AND = all down   OR = SW0   XOR = SW1   NAND = SW1+SW0   NOR = SW2   XNOR = SW2+SW0"],
            lambda q, p: (p, 0x7))]))

GATES3 = [("AND3", lambda a, b, c: a & b & c), ("OR3", lambda a, b, c: a | b | c),
          ("XOR3", lambda a, b, c: a ^ b ^ c), ("NAND3", lambda a, b, c: 1 - (a & b & c)),
          ("NOR3", lambda a, b, c: 1 - (a | b | c)), ("XNOR3", lambda a, b, c: 1 - (a ^ b ^ c))]
T3 = [[f(*G.bits(r, 3)) for r in range(8)] for _, f in GATES3]
W.append(Q(id="Q12", name="GATE3", title="שער של שלוש כניסות", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(6)),
    tables=lambda p: [T3[p]], answer=lambda p: (p, 0x7), describe=lambda p: GATES3[p][0],
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער של שלוש כניסות. חצי ראשון: החזיקו למטה:", "SW9 = down",
             "נסו 4 מצבים ורשמו אם הנורה דולקת:", "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
             "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4, lambda q, p: (sum(T3[p][r] << r for r in range(4)), 0xF)),
           (["חצי שני: אותו דבר, אבל החזיקו למעלה:", "SW9 = up",
             "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
             "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4, lambda q, p: (sum(T3[p][4 + r] << r for r in range(4)), 0xF)),
           (["איזה שער זה? זוגיות: שער שנותן 1 כשמספר ה-1 בכניסות אי-זוגי.",
             "AND3 = all down   OR3 = SW0   XOR3 (odd) = SW1   NAND3 = SW1+SW0   NOR3 = SW2   XNOR3 (even) = SW2+SW0"],
            lambda q, p: (p, 0x7))]))

CMOS = [("NAND2", lambda a, b, c: 1 - (a & b), 1, 4), ("NOR2", lambda a, b, c: 1 - (a | b), 0, 4),
        ("NAND3", lambda a, b, c: 1 - (a & b & c), 1, 6), ("NOR3", lambda a, b, c: 1 - (a | b | c), 0, 6),
        ("AND2", lambda a, b, c: a & b, 1, 6), ("OR2", lambda a, b, c: a | b, 0, 6)]
TC = [[f(*G.bits(r, 3)) for r in range(8)] for _, f, _, _ in CMOS]
W.append(Q(id="Q13", name="CMOS", title="שער מטרנזיסטורים", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(6)),
    tables=lambda p: [TC[p]], answer=lambda p: (CMOS[p][3], 0xF), describe=lambda p: CMOS[p][0],
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער אחד. עברו על 8 המצבים וזהו אותו:"] + ROWS3 +
            ["(gates with 2 inputs use only A and B)",
             "NAND2 = all down   NOR2 = SW0   NAND3 = SW1   NOR3 = SW1+SW0   AND2 = SW2   OR2 = SW2+SW0"],
            lambda q, p: (p, 0x7)),
           (["בשער הזה, הטרנזיסטורים מסוג", "nMOS", "(הרשת שמחוברת לאדמה) - בטור או במקביל?",
             "NAND: nMOS in series     NOR: nMOS in parallel     AND, OR: like their first stage",
             "בטור - הרימו:", "SW0", "במקביל - השאירו למטה."], lambda q, p: (CMOS[p][2], 0x1)),
           (["והטרנזיסטורים מסוג", "pMOS", "(הרשת שמחוברת למתח)? הם תמיד הפוכים לרשת התחתונה.",
             "בטור - הרימו:", "SW0", "במקביל - השאירו למטה."], lambda q, p: (1 - CMOS[p][2], 0x1)),
           (["כמה טרנזיסטורים יש בשער כולו? לכל כניסה זוג אחד; לשער", "AND / OR",
             "מוסיפים עוד מהפך של שני טרנזיסטורים.", "4 = SW2     6 = SW2 + SW1"],
            lambda q, p: (CMOS[p][3], 0xF))]))

# ================================================================ more questions (ids set below, in lesson order)
# hex -> decimal
V = list(range(0x10, 0x100))
HEXV = ["A = 10   B = 11   C = 12   D = 13   E = 14   F = 15"]
W.append(Q(id="HEX2DEC", name="HEX2DEC", title="מהקסדצימלי לעשרוני", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v >> 4, 4) + bitsof(v & 15, 4)), answer=lambda v: (v % 10, 0xF),
    describe=lambda v: f"0x{v:02X} = {v}",
    B=["the number = HEX1 HEX0 (hex)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח מספר הקסדצימלי בשתי ספרות. הערך שלו:", "HEX1 x 16 + HEX0"] + HEXV +
            ["מה ספרת המאות של הערך העשרוני? (0, 1 או 2)", "0 = all down     1 = SW0     2 = SW1"],
            lambda q, v: (v // 100, 0x3)),
           (["מה ספרת העשרות שלו?", "HEX1 x 16 + HEX0"] + DIG, lambda q, v: ((v // 10) % 10, 0xF)),
           (["ומה ספרת האחדות?", "HEX1 x 16 + HEX0"] + DIG, lambda q, v: (v % 10, 0xF))]))

# estimating large powers of two
V = [n for n in range(10, 39) if n % 10 != 9]
UNIT = ["2^10 = kilo     2^20 = mega     2^30 = giga"]
PW = ["1 = SW0   2 = SW1   4 = SW2   8 = SW3   16 = SW4", "32 = SW5   64 = SW6   128 = SW7   256 = SW8"]
W.append(Q(id="POW2", name="POW2", title="חזקות גדולות של 2", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda n: const(bitsof(n // 10, 4) + bitsof(n % 10, 4)), answer=lambda n: (1 << (n % 10), 0x1FF),
    describe=lambda n: f"2^{n} = {1 << (n % 10)} {['', 'kilo', 'mega', 'giga'][n // 10]}",
    B=["N = HEX1 HEX0 (decimal)     answer: SW8..SW0"], L=[], F=[],
    steps=[(["בלוח מספר. מעריכים את 2 בחזקת המספר הזה:", "2^N = 2^(N - 10k) x 2^(10k)"] + UNIT +
            ["איזו יחידה יוצאת?", "kilo = SW0     mega = SW1     giga = SW1 + SW0"],
            lambda q, n: (n // 10, 0x3)),
           (["ומה המספר שמכפיל את היחידה? הרימו את המתג שלו:", "2^(N - 10k)"] + PW,
            lambda q, n: (1 << (n % 10), 0x1FF))]))

# ranges of N bits
W.append(Q(id="RANGES", name="RANGES", title="הטווח של N ביטים", inputs=[9], flat=True,
    outs=hexd(0), hexes=[None, None, None, None], variants=list(range(3, 9)),
    tables=lambda n: const(bitsof(n, 4)), answer=lambda n: ((1 << (n - 1)) - 1, 0xFF),
    describe=lambda n: f"N = {n}: unsigned 0..{(1 << n) - 1}, two's {-(1 << (n - 1))}..{(1 << (n - 1)) - 1}",
    B=["N = HEX0     answer: SW7..SW0 (binary)"], L=[], F=[],
    steps=[(["בלוח מספר הביטים. מה המספר הגדול ביותר בלי סימן שנכנס בכמה ביטים כאלה?",
             "כתבו אותו בבינארי:", "SW7..SW0"], lambda q, n: ((1 << n) - 1, 0xFF)),
           (["מה המספר החיובי הגדול ביותר במשלים ל-2, באותו מספר ביטים?", "SW7..SW0"],
            lambda q, n: ((1 << (n - 1)) - 1, 0xFF)),
           (["מה השלילי הקטן ביותר במשלים ל-2? כתבו את הערך המוחלט שלו:", "SW7..SW0"],
            lambda q, n: (1 << (n - 1), 0xFF)),
           (["ומה המספר הגדול ביותר בשיטת סימן וגודל, באותו מספר ביטים?", "SW7..SW0"],
            lambda q, n: ((1 << (n - 1)) - 1, 0xFF))]))

# a hidden operation on a 4-bit number
OPS = [("-A", lambda a: -a), ("NOT A", lambda a: ~a), ("A + 1", lambda a: a + 1),
       ("A - 1", lambda a: a - 1), ("2A", lambda a: 2 * a), ("A / 2", lambda a: a >> 1)]
TO = [[f(a) & 15 for a in range(16)] for _, f in OPS]
W.append(Q(id="OPS", name="OPS", title="איזו פעולה מוסתרת בלוח?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(6)),
    tables=lambda p: [[(x >> b) & 1 for x in TO[p]] for b in range(4)], answer=lambda p: (p, 0x7),
    describe=lambda p: f"Y = {OPS[p][0]}",
    B=["A = SW9 SW8 SW7 SW6 (HEX0)     Y = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הלוח עושה פעולה מוסתרת על הכניסה ומראה את התוצאה (4 ביטים) בנורות.",
             "שימו כניסה 0:", "SW9 SW8 SW7 SW6 = 0000", "העתיקו את התוצאה:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, p: (TO[p][0], 0xF)),
           (["שימו כניסה 3:", "SW9 SW8 SW7 SW6 = 0011", "העתיקו את התוצאה:", "SW3..SW0 = LEDG3..LEDG0"],
            lambda q, p: (TO[p][3], 0xF)),
           (["איזו פעולה זו? נסו עוד כניסות אם צריך.",
             "-A = all down     NOT A = SW0     A + 1 = SW1",
             "A - 1 = SW1 + SW0     2A = SW2     A / 2 = SW2 + SW0"], lambda q, p: (p, 0x7))]))

# signed overflow
V = [(a, b) for a in range(-8, 8) for b in range(-8, 8)]
def ovf(p):
    return 1 if not -8 <= p[0] + p[1] <= 7 else 0
W.append(Q(id="OVERFLOW", name="OVERFLOW", title="גלישה במספרים עם סימן", inputs=[9], flat=True,
    outs=[("M", 3)] + hexd(2) + [("M", 1)] + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda p: const([1 if p[0] < 0 else 0] + bitsof(abs(p[0]), 4) + [1 if p[1] < 0 else 0] + bitsof(abs(p[1]), 4)),
    answer=lambda p: (ovf(p), 0x1),
    describe=lambda p: f"{p[0]} + {p[1]} = {p[0] + p[1]} -> {tw(p[0] + p[1]):04b}, overflow {ovf(p)}",
    B=["A = HEX3 HEX2     B = HEX1 HEX0 (decimal, with a minus)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שני מספרים עם סימן. המספר השמאלי במשלים ל-2, ב-4 ביטים:", "SW3..SW0"] + BIN4,
            lambda q, p: (tw(p[0]), 0xF)),
           (["המספר הימני במשלים ל-2, ב-4 ביטים:", "SW3..SW0"] + BIN4, lambda q, p: (tw(p[1]), 0xF)),
           (["חברו את שני המספרים של שלבים 1 ו-2. שמרו רק 4 ביטים (הנשא נזרק):", "SW3..SW0"],
            lambda q, p: (tw(p[0] + p[1]), 0xF)),
           (["האם הייתה גלישה? ב-4 ביטים אפשר לכתוב רק מספרים ממינוס 8 עד 7.",
             "סימן לגלישה: שני מספרים עם אותו סימן, והתוצאה עם סימן הפוך.",
             "גלישה - הרימו:", "SW0", "אין גלישה - השאירו למטה."], lambda q, p: (ovf(p), 0x1))]))

# a 4-input gate
GATES4 = [("AND4", lambda x: int(x == 15)), ("OR4", lambda x: int(x != 0)), ("XOR4", lambda x: bin(x).count("1") & 1),
          ("NAND4", lambda x: int(x != 15)), ("NOR4", lambda x: int(x == 0)), ("XNOR4", lambda x: 1 - (bin(x).count("1") & 1))]
T4 = [[f(r) for r in range(16)] for _, f in GATES4]
LIT = ["הנורה דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."]
W.append(Q(id="GATE4", name="GATE4", title="שער של ארבע כניסות", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=list(range(6)),
    tables=lambda p: [T4[p]], answer=lambda p: (p, 0x7), describe=lambda p: GATES4[p][0],
    B=["A = SW9   B = SW8   C = SW7   D = SW6   Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער של ארבע כניסות. שימו את כל הכניסות למטה:", "SW9 SW8 SW7 SW6 = 0000"] + LIT,
            lambda q, p: (T4[p][0], 0x1)),
           (["עכשיו את כל הכניסות למעלה:", "SW9 SW8 SW7 SW6 = 1111"] + LIT, lambda q, p: (T4[p][15], 0x1)),
           (["עכשיו רק כניסה אחת למעלה:", "SW9 SW8 SW7 SW6 = 1000"] + LIT, lambda q, p: (T4[p][8], 0x1)),
           (["איזה שער זה? זוגיות: שער שנותן 1 כשמספר ה-1 בכניסות אי-זוגי.",
             "AND4 = all down   OR4 = SW0   XOR4 (odd) = SW1",
             "NAND4 = SW1+SW0   NOR4 = SW2   XNOR4 (even) = SW2+SW0"], lambda q, p: (p, 0x7))]))

# which transistors are ON in a CMOS NAND2 / NOR2
V = [(g, a, b) for g in range(2) for a in range(2) for b in range(2)]
TG = [[1 - (r >> 1 & r & 1) for r in range(4)], [1 - ((r >> 1) | (r & 1)) for r in range(4)]]
def onoff(p):
    return ((1 - p[1]) << 3) | ((1 - p[2]) << 2) | (p[1] << 1) | p[2]
W.append(Q(id="ONOFF", name="ONOFF", title="אילו טרנזיסטורים דולקים?", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("H", (1, 0)), ("H", (0, 0))], hexes=[[9], [8], None, None], variants=V,
    tables=lambda p: [TG[p[0]], [p[1]] * 4, [p[2]] * 4], answer=lambda p: (TG[p[0]][2 * p[1] + p[2]], 0x1),
    describe=lambda p: f"{['NAND2', 'NOR2'][p[0]]}, A = {p[1]}, B = {p[2]}: ON {onoff(p):04b}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     Y = LEDG0     the inputs to set = HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער של שתי כניסות. נסו את 4 המצבים וזהו אותו:", "SW9 SW8:   down-down,   down-up,   up-down,   up-up",
             "NAND = all down     NOR = SW0"], lambda q, p: (p[0], 0x1)),
           (["שימו את הכניסות שמוצגות בשתי הספרות הימניות:", "SW9 = HEX1     SW8 = HEX0",
             "אילו טרנזיסטורים דולקים עכשיו? דולק - הרימו את המתג שלו:",
             "pMOS: ON when gate = 0     nMOS: ON when gate = 1",
             "P1 (A) = SW3     P2 (B) = SW2     N1 (A) = SW1     N2 (B) = SW0"], lambda q, p: (onoff(p), 0xF)),
           (["האם היציאה מחוברת עכשיו למתח, דרך הטרנזיסטורים העליונים?", "מחוברת למתח - הרימו:", "SW0",
             "מחוברת לאדמה - השאירו למטה."], lambda q, p: (TG[p[0]][2 * p[1] + p[2]], 0x1))]))

# a compound CMOS gate
CPX = [("~(AB + C)", lambda a, b, c: 1 - ((a & b) | c), 1), ("~((A + B)C)", lambda a, b, c: 1 - ((a | b) & c), 0),
       ("~(A + BC)", lambda a, b, c: 1 - (a | (b & c)), 0), ("~(A(B + C))", lambda a, b, c: 1 - (a & (b | c)), 1),
       ("~(ABC)", lambda a, b, c: 1 - (a & b & c), 1), ("~(A + B + C)", lambda a, b, c: 1 - (a | b | c), 0)]
TX = [[f(*G.bits(r, 3)) for r in range(8)] for _, f, _ in CPX]
W.append(Q(id="COMPLEX", name="COMPLEX", title="שער CMOS מורכב", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=list(range(6)),
    tables=lambda p: [TX[p]], answer=lambda p: (CPX[p][2], 0x1), describe=lambda p: f"Y = {CPX[p][0]}",
    B=["A = SW9     B = SW8     C = SW7     Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער מטרנזיסטורים, של שלוש כניסות. חצי ראשון: החזיקו למטה:", "SW9 = down",
             "נסו 4 מצבים ורשמו אם הנורה דולקת:", "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
             "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4, lambda q, p: (sum(TX[p][r] << r for r in range(4)), 0xF)),
           (["חצי שני: אותו דבר, אבל החזיקו למעלה:", "SW9 = up",
             "SW8 SW7:   down-down,   down-up,   up-down,   up-up",
             "לכל מצב שהנורה דלקה - הרימו מתג:"] + POS4, lambda q, p: (sum(TX[p][4 + r] << r for r in range(4)), 0xF)),
           (["איזה שער זה?", "~(AB + C) = all down     ~((A + B)C) = SW0     ~(A + BC) = SW1",
             "~(A(B + C)) = SW1+SW0     ~(ABC) = SW2     ~(A + B + C) = SW2+SW0"], lambda q, p: (p, 0x7)),
           (["ברשת התחתונה (לאדמה):", "nMOS:   AND = series     OR = parallel",
             "האם הטרנזיסטורים של שתי הכניסות האלה בטור?", "A, B", "בטור - הרימו:", "SW0", "במקביל - השאירו למטה."],
            lambda q, p: (CPX[p][2], 0x1))]))

# decimal -> binary, method 2 (divide by 2)
V = list(range(20, 100))
REM = ["השארית 1 - הרימו:", "SW0", "השארית 0 - השאירו למטה."]
W.append(Q(id="DIV2", name="DIV2", title="מעשרוני לבינארי בחלוקה ב-2", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v // 10, 4) + bitsof(v % 10, 4)),
    answer=lambda v: (v, 0x7F), describe=lambda v: f"the number {v} = {v:07b}",
    B=["the number = HEX1 HEX0 (decimal)     answer: SW6..SW0"], L=[], F=[],
    steps=[(["בלוח מספר עשרוני. שיטה 2: מחלקים ב-2 שוב ושוב, וכל שארית היא הביט הבא, מימין לשמאל.",
             "חלקו את המספר ב-2. מה השארית?"] + REM, lambda q, v: (v & 1, 0x1)),
           (["עכשיו חלקו ב-2 את המנה של החלוקה הראשונה. מה השארית הפעם?"] + REM,
            lambda q, v: ((v >> 1) & 1, 0x1)),
           (["המשיכו לחלק עד שהמנה 0, וכתבו את כל השאריות:",
             "1st -> SW0     2nd -> SW1     3rd -> SW2     ...     7th -> SW6"], lambda q, v: (v, 0x7F))]))

# a byte: msb, lsb, how many ones
V = rng.sample(range(256), 256)
BIT1 = ["1 - הרימו:", "SW0", "0 - השאירו למטה."]
W.append(Q(id="BYTE", name="BYTE", title="בייט: הביט המשמעותי, הפחות משמעותי וכמה אחדות", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v >> 4, 4) + bitsof(v & 15, 4)),
    answer=lambda v: (bin(v).count("1"), 0xF), describe=lambda v: f"0x{v:02X} = {v:08b}, {bin(v).count('1')} ones",
    B=["the byte = HEX1 HEX0 (hex)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח בייט בשתי ספרות הקס. מה הביט השמאלי ביותר שלו (המשמעותי ביותר)?"] + BIT1 +
            ["A = 10   B = 11   C = 12   D = 13   E = 14   F = 15"], lambda q, v: (v >> 7, 0x1)),
           (["מה הביט הימני ביותר שלו (הפחות משמעותי)?"] + BIT1, lambda q, v: (v & 1, 0x1)),
           (["כמה ביטים של 1 יש בבייט כולו? שימו את המספר:"] + BIN4, lambda q, v: (bin(v).count("1"), 0xF))]))

# binary addition, column by column
V = [(a, b) for a in range(16) for b in range(16)]
CALEG = ["A = LEDG7 LEDG6 LEDG5 LEDG4     B = LEDG3 LEDG2 LEDG1 LEDG0"]
W.append(Q(id="COLADD", name="COLADD", title="חיבור בינארי, עמודה אחרי עמודה", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=V,
    tables=lambda p: const(bitsof(p[1], 4) + bitsof(p[0], 4)), answer=lambda p: ((p[0] + p[1]) >> 4, 0x1),
    describe=lambda p: f"{p[0]:04b} + {p[1]:04b} = {p[0] + p[1]:05b}",
    B=["A = LEDG7..LEDG4     B = LEDG3..LEDG0     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בנורות הירוקות שני מספרים של 4 ביטים: הראשון בארבע הנורות השמאליות, השני בארבע הימניות."] + CALEG +
            ["חברו את העמודה הימנית (הביט הימני של כל מספר). יש נשא לעמודה הבאה?",
             "יש נשא - הרימו:", "SW0", "אין - השאירו למטה."], lambda q, p: (p[0] & p[1] & 1, 0x1)),
           (["חברו את כל העמודות. הסכום של שני מספרים של 4 ביטים יכול להיות של 5 ביטים:"] + CALEG +
            ["כתבו את כל הסכום. הביט החמישי (הנשא מהעמודה השמאלית) על המתג החמישי:",
             "SW4 = the carry     SW3..SW0 = the 4 sum bits"],
            lambda q, p: (p[0] + p[1], 0x1F)),
           (["האם הסכום לא נכנס ב-4 ביטים (גלישה = הביט החמישי 1)?"] + CALEG +
            ["גלישה - הרימו:", "SW0", "אין - השאירו למטה."], lambda q, p: ((p[0] + p[1]) >> 4, 0x1))]))

# sign / magnitude: addition does not work
V = [m | s for s in (0, 8) for m in range(1, 8)]
SMS = lambda x: (x + (x ^ 8)) & 15
XLEG = ["X = HEX3 HEX2 HEX1 HEX0  (also on LEDG3..LEDG0)     HEX3 = the sign bit"]
W.append(Q(id="SMFAIL", name="SMFAIL", title="למה חיבור לא עובד בסימן וגודל", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)] + BITS4, hexes=[None, None, None, None], variants=V,
    tables=lambda x: const(bitsof(x, 4) + [(x >> 3) & 1, (x >> 2) & 1, (x >> 1) & 1, x & 1]),
    answer=lambda x: (int(SMS(x) in (0, 8)), 0x1),
    describe=lambda x: f"{x:04b} + {x ^ 8:04b} = {SMS(x):04b}",
    B=["X = HEX3..HEX0 (sign / magnitude, HEX3 = sign)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בתצוגה מספר בשיטת סימן וגודל, 4 ביטים. הספרה השמאלית היא ביט הסימן:"] + XLEG +
            ["מספר נגדי = אותו מספר עם סימן הפוך. למשל הנגדי של 3 הוא מינוס 3, ומספר ועוד הנגדי שלו נותן 0.",
             "בסימן וגודל מוצאים את הנגדי רק בהיפוך ביט הסימן (לא כמו במשלים ל-2). למשל:",
             "1011 = -3   ->   0011 = +3",
             "כתבו את המספר הנגדי למספר שבתצוגה:", "SW3..SW0"] + BIN4,
            lambda q, x: (x ^ 8, 0xF)),
           (["עכשיו חברו שני מספרים בחיבור בינארי רגיל, עמודה אחרי עמודה:",
             "1. המספר שבתצוגה.", "2. הנגדי שלו: אותו מספר עם ביט סימן הפוך."] + XLEG +
            ["מהסכום כתבו רק את 4 הביטים הימניים (הביט החמישי נזרק). למשל:",
             "0011 + 1011 = 1110",
             "SW3..SW0"], lambda q, x: (SMS(x), 0xF)),
           (["מספר ועוד הנגדי שלו צריך לתת 0. בסימן וגודל יש שני אפסים:", "0000 = +0     1000 = -0",
             "האם הסכום שחישבתם הוא אחד משני האפסים?", "יצא 0 - הרימו:", "SW0", "לא יצא 0 - השאירו למטה."],
            lambda q, x: (int(SMS(x) in (0, 8)), 0x1))]))

# six 2-input gates at once, in a hidden order
PERM = random.Random(77).sample(list(itertools.permutations(range(6))), 256)
LEDN = ["LEDG0 = all down     LEDG1 = SW0     LEDG2 = SW1", "LEDG3 = SW1+SW0     LEDG4 = SW2     LEDG5 = SW2+SW0"]
def ledof(p, g):				# the LED that shows gate g (G.GATES: AND OR XOR NAND NOR XNOR)
    return p.index(g)
W.append(Q(id="GATESET", name="GATESET", title="שישה שערים - מי זה מי?", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(6)], hexes=[[9], [8], None, None], variants=PERM,
    tables=lambda p: [GATES2[p[i]][1] for i in range(6)], answer=lambda p: (ledof(p, 0), 0x7),
    describe=lambda p: " ".join(f"LEDG{i}={GATES2[p[i]][0]}" for i in range(6)),
    B=["A = SW9     B = SW8     six gates = LEDG5..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שישה שערים של שתי כניסות, כל אחד בנורה ירוקה אחרת:", "A = SW9     B = SW8     LEDG0..LEDG5",
             "נסו את 4 המצבים. איזו נורה היא", "XOR", "(דולקת כשהכניסות שונות)? הרימו את המספר שלה:"] + LEDN,
            lambda q, p: (ledof(p, 2), 0x7)),
           (["איזו נורה היא", "NAND", "(כבויה רק כששתי הכניסות 1)?"] + LEDN, lambda q, p: (ledof(p, 3), 0x7)),
           (["איזו נורה היא", "NOR", "(דולקת רק כששתי הכניסות 0)?"] + LEDN, lambda q, p: (ledof(p, 4), 0x7)),
           (["ואיזו נורה היא", "AND", "(דולקת רק כששתי הכניסות 1)?"] + LEDN, lambda q, p: (ledof(p, 0), 0x7))]))

# counting in binary: the next and the previous number
V = list(range(1, 255))
LEDB = ["LEDG0 = 1   LEDG1 = 2   LEDG2 = 4   LEDG3 = 8", "LEDG4 = 16   LEDG5 = 32   LEDG6 = 64   LEDG7 = 128"]
def flips(v):					# bits that change from v to v + 1
    return bin(v ^ (v + 1)).count("1")
W.append(Q(id="BINCOUNT", name="BINCOUNT", title="ספירה בבינארי", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 8)), answer=lambda v: (v - 1, 0xFF),
    describe=lambda v: f"{v:08b}: next {v + 1:08b} ({flips(v)} bits change), previous {v - 1:08b}",
    B=["the number = LEDG7..LEDG0 (binary)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בנורות הירוקות מספר בינארי של 8 ביטים:", "LEDG7..LEDG0",
             "מה המספר הבא בספירה (המספר ועוד 1)? כתבו אותו בבינארי:", "SW7..SW0"],
            lambda q, v: (v + 1, 0xFF)),
           (["כמה ביטים משתנים מהמספר שבנורות למספר הבא?",
             "רמז: כל ה-1 בצד ימין הופכים ל-0, וה-0 הראשון משמאלם הופך ל-1.", "LEDG7..LEDG0"] + BIN4,
            lambda q, v: (flips(v), 0xF)),
           (["ועכשיו המספר הקודם (המספר שבנורות פחות 1), בבינארי:", "LEDG7..LEDG0", "SW7..SW0"],
            lambda q, v: (v - 1, 0xFF))]))

# decimal -> hex (divide by 16)
V = list(range(16, 256))
W.append(Q(id="DEC2HEX", name="DEC2HEX", title="מעשרוני להקסדצימלי", inputs=[9], flat=True,
    outs=hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v // 100, 4) + bitsof((v // 10) % 10, 4) + bitsof(v % 10, 4)),
    answer=lambda v: (v, 0xFF), describe=lambda v: f"{v} = 0x{v:02X} = {v:08b}",
    B=["the number = HEX2 HEX1 HEX0 (decimal)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בלוח מספר עשרוני בשלוש ספרות:", "HEX2 HEX1 HEX0",
             "חלקו אותו ב-16. המנה היא הספרה השמאלית בהקס. שימו אותה:", "SW3..SW0"] + BIN4 + HEXV,
            lambda q, v: (v // 16, 0xF)),
           (["השארית מהחלוקה ב-16 היא הספרה הימנית בהקס. שימו אותה:", "HEX2 HEX1 HEX0", "SW3..SW0"] + BIN4 + HEXV,
            lambda q, v: (v % 16, 0xF)),
           (["כל המספר בבינארי (בייט): הספרה השמאלית על ארבעת המתגים העליונים.", "HEX2 HEX1 HEX0",
             "left hex digit -> SW7 SW6 SW5 SW4      right hex digit -> SW3 SW2 SW1 SW0"],
            lambda q, v: (v, 0xFF))]))

# an 8-bit two's complement number -> decimal
V = list(range(-99, 100))
W.append(Q(id="SIGNED8", name="SIGNED8", title="משלים ל-2 ב-8 ביטים - לעשרוני", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(tw(v, 8), 8)), answer=lambda v: (abs(v) % 10, 0xF),
    describe=lambda v: f"{tw(v, 8):08b} = {v}",
    B=["the number = LEDG7..LEDG0 (two's complement, 8 bits)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["בנורות הירוקות מספר במשלים ל-2, ב-8 ביטים:", "LEDG7..LEDG0",
             "הנורה השמאלית 1 = שלילי. שלילי - הרימו:", "SW0", "חיובי - השאירו למטה."],
            lambda q, v: (int(v < 0), 0x1)),
           (["מה הערך המוחלט שלו, בבינארי?", "LEDG7..LEDG0",
             "שלילי - הפכו את כל 8 הביטים והוסיפו 1. חיובי - הוא כמו שהוא.", "SW7..SW0"],
            lambda q, v: (abs(v), 0xFF)),
           (["מה ספרת העשרות של הערך המוחלט שלו, בעשרוני?",
             "LEDG7..LEDG0"] + DIG, lambda q, v: (abs(v) // 10, 0xF)),
           (["ומה ספרת האחדות שלו?",
             "LEDG7..LEDG0"] + DIG, lambda q, v: (abs(v) % 10, 0xF))]))

# a hidden 4 -> 8 bit widening circuit: sign / zero extension, ones, shift left
EXTK = [("sign extension", lambda a: tw(sval(a), 8)), ("zero extension", lambda a: a),
        ("fill with ones", lambda a: 0xF0 | a), ("shift left 4", lambda a: a << 4)]
TE = [[f(a) for a in range(16)] for _, f in EXTK]
W.append(Q(id="EXTBOX", name="EXTBOX", title="איזו הרחבה מוסתרת בלוח?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, [9, 8, 7, 6]], variants=list(range(4)),
    tables=lambda p: [[(x >> b) & 1 for x in TE[p]] for b in range(8)], answer=lambda p: (p, 0x3),
    describe=lambda p: EXTK[p][0],
    B=["A = SW9 SW8 SW7 SW6 (HEX0, 4 bits)     Y = LEDG7..LEDG0 (8 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הלוח מרחיב את הכניסה מ-4 ביטים ל-8 ביטים, בשיטה מוסתרת.", "שימו כניסה:",
             "SW9 SW8 SW7 SW6 = 1101", "העתיקו את ארבע הנורות העליונות:", "SW3..SW0 = LEDG7..LEDG4"],
            lambda q, p: (TE[p][13] >> 4, 0xF)),
           (["הכניסה 1101 היא מינוס 3 במשלים ל-2 (4 ביטים).", "SW9 SW8 SW7 SW6 = 1101",
             "האם 8 הנורות הן עדיין מינוס 3 במשלים ל-2 (8 ביטים)?", "LEDG7..LEDG0",
             "כן - הרימו:", "SW0", "לא - השאירו למטה."],
            lambda q, p: (int(TE[p][13] == tw(-3, 8)), 0x1)),
           (["עכשיו כניסה חיובית:", "SW9 SW8 SW7 SW6 = 0011", "העתיקו את ארבע הנורות העליונות:",
             "SW3..SW0 = LEDG7..LEDG4"], lambda q, p: (TE[p][3] >> 4, 0xF)),
           (["איזו שיטה זו? נסו עוד כניסות אם צריך.",
             "sign extension = all down     zero extension = SW0",
             "fill with ones = SW1     shift left 4 = SW1 + SW0"], lambda q, p: (p, 0x3))]))

# single-input gates: NOT or buffer, and their transistors
V = list(range(16))
LEDS4 = ["LEDG0 -> SW0     LEDG1 -> SW1     LEDG2 -> SW2     LEDG3 -> SW3"]
W.append(Q(id="NOTBUF", name="NOTBUF", title="מהפך או חוצץ?", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9], None, None, None], variants=V,
    tables=lambda m: [[(m >> i) & 1, 1 - ((m >> i) & 1)] for i in range(4)],
    answer=lambda m: (16 - 2 * bin(m).count("1"), 0x1F),
    describe=lambda m: " ".join(f"LEDG{i}={'NOT' if m >> i & 1 else 'BUF'}" for i in range(4)),
    B=["A = SW9 (HEX3)     four gates = LEDG3..LEDG0     answer: SW4..SW0"], L=[], F=[],
    steps=[(["בלוח ארבעה שערים של כניסה אחת, כולם מקבלים את אותה כניסה:", "A = SW9     LEDG0..LEDG3",
             "כל שער הוא מהפך או חוצץ:", "NOT: Y = not A     BUF: Y = A",
             "שימו את הכניסה למטה:", "SW9 = down", "איזו נורה דולקת - הרימו את המתג שלה:"] + LEDS4,
            lambda q, m: (m, 0xF)),
           (["עכשיו הכניסה למעלה:", "SW9 = up", "איזו נורה דולקת - הרימו את המתג שלה:"] + LEDS4,
            lambda q, m: (~m & 15, 0xF)),
           (["כמה טרנזיסטורים בארבעת השערים יחד?",
             "NOT = 2 transistors     BUF = two NOTs = 4 transistors",
             "השערים: מהפך = נורה שדולקת כשהכניסה למטה.", "A = SW9     LEDG0..LEDG3",
             "8 = SW3     10 = SW3+SW1     12 = SW3+SW2     14 = SW3+SW2+SW1     16 = SW4"],
            lambda q, m: (16 - 2 * bin(m).count("1"), 0x1F))]))

# parity: XOR / XNOR of a hidden subset of four inputs
V = [(s, inv) for inv in range(2) for s in range(16) if bin(s).count("1") >= 2]
def par(p, r):
    return (bin(r & p[0]).count("1") & 1) ^ p[1]
def parkind(p):
    return 3 * p[1] + bin(p[0]).count("1") - 2
PAR = ["XOR2 = all down     XOR3 = SW0     XOR4 = SW1", "XNOR2 = SW1+SW0     XNOR3 = SW2     XNOR4 = SW2+SW0"]
W.append(Q(id="PARITY", name="PARITY", title="זוגיות: אילו כניסות מחוברות?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=V,
    tables=lambda p: [[par(p, r) for r in range(16)]], answer=lambda p: (parkind(p), 0x7),
    describe=lambda p: f"{['XOR', 'XNOR'][p[1]]} of inputs {p[0]:04b} (A B C D)",
    B=["A = SW9   B = SW8   C = SW7   D = SW6   Y = LEDG0 (green)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח שער זוגיות של חלק מארבע הכניסות (השאר לא מחוברות):", "XOR or XNOR", "A = SW9   B = SW8   C = SW7   D = SW6   Y = LEDG0",
             "שימו את כל הכניסות למטה:", "SW9 SW8 SW7 SW6 = 0000"] + LIT,
            lambda q, p: (par(p, 0), 0x1)),
           (["אילו כניסות מחוברות? מהמצב שכולן למטה, הרימו כל פעם כניסה אחת בלבד.",
             "A = SW9   B = SW8   C = SW7   D = SW6   Y = LEDG0",
             "הנורה השתנתה = הכניסה מחוברת. הרימו את המתג שלה:", "A -> SW3     B -> SW2     C -> SW1     D -> SW0"],
            lambda q, p: (p[0], 0xF)),
           (["איזה שער זה? הספרה = מספר הכניסות המחוברות.",
             "XOR: Y = 1 when an odd number of its inputs are 1     XNOR: even",
             "A = SW9   B = SW8   C = SW7   D = SW6   Y = LEDG0"] + PAR,
            lambda q, p: (parkind(p), 0x7))]))

# ================================================================ easy questions from the slides (first in each topic)
# slide 17: powers of two
V = list(range(9))
W.append(Q(id="SPOW", name="SPOW", title="חזקות של 2 מהשקף", inputs=[9], flat=True,
    outs=hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda n: const(bitsof(n, 4)), answer=lambda n: ((1 << n) % 10, 0xF),
    describe=lambda n: f"2^{n} = {1 << n} = {1 << n:09b}",
    B=["N = HEX0     answer: SW8..SW0"], L=[], F=[],
    steps=[(["טבלת החזקות של 2 מהשקף: 1, 2, 4, 8, 16 ... בתצוגה מספר:", "N = HEX0",
             "מה זה 2 בחזקת המספר הזה? הרימו את המתג שלו:"] + PW, lambda q, n: (1 << n, 0x1FF)),
           (["מה ספרת האחדות של 2 בחזקת המספר הזה, בעשרוני?", "N = HEX0"] + DIG,
            lambda q, n: ((1 << n) % 10, 0xF))]))

# slide 18: binary -> decimal, like 10011 = 19
V = [v for v in range(1, 32) if v != 19]
LED5 = ["LEDG4 = 16   LEDG3 = 8   LEDG2 = 4   LEDG1 = 2   LEDG0 = 1"]
W.append(Q(id="SBIN5", name="SBIN5", title="מבינארי לעשרוני כמו בשקף", inputs=[9], flat=True,
    outs=[("G", i) for i in range(5)], hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v, 5)), answer=lambda v: (v % 10, 0xF),
    describe=lambda v: f"{v:05b} = {v}",
    B=["the number = LEDG4..LEDG0 (binary, 5 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: ממירים מבינארי לעשרוני בחיבור המשקלות של הביטים הדולקים:",
             "10011 = 16 + 2 + 1 = 19",
             "בנורות הירוקות מספר בינארי של 5 ביטים:"] + LED5 +
            ["מה ספרת העשרות שלו בעשרוני?", "0 = all down     1 = SW0     2 = SW1     3 = SW1+SW0"],
            lambda q, v: (v // 10, 0x3)),
           (["ומה ספרת האחדות שלו?"] + LED5 + DIG, lambda q, v: (v % 10, 0xF))]))

# slide 25: hex -> binary, like 4AF = 0100 1010 1111
V = [v for v in rng.sample(range(0x100, 0x1000), 257) if v != 0x4AF][:256]
W.append(Q(id="SHEX3", name="SHEX3", title="מהקסדצימלי לבינארי כמו בשקף", inputs=[9], flat=True,
    outs=hexd(2) + hexd(1) + hexd(0), hexes=[None, None, None, None], variants=V,
    tables=lambda v: const(bitsof(v >> 8, 4) + bitsof((v >> 4) & 15, 4) + bitsof(v & 15, 4)),
    answer=lambda v: (v >> 8, 0xF), describe=lambda v: f"0x{v:03X} = {v >> 8:04b} {(v >> 4) & 15:04b} {v & 15:04b}",
    B=["the number = HEX2 HEX1 HEX0 (hex)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: כל ספרת הקס היא 4 ביטים:", "4AF = 0100 1010 1111",
             "בתצוגה מספר הקסדצימלי של 3 ספרות. כתבו בבינארי את הספרה הימנית:", "HEX0"] + BIN4 + HEXV,
            lambda q, v: (v & 15, 0xF)),
           (["עכשיו את הספרה האמצעית, בבינארי:", "HEX1"] + BIN4 + HEXV, lambda q, v: ((v >> 4) & 15, 0xF)),
           (["ועכשיו את הספרה השמאלית, בבינארי:", "HEX2"] + BIN4 + HEXV, lambda q, v: (v >> 8, 0xF))]))

# slides 32-33, 43-44: the slides' 4-bit additions (and the same with the numbers swapped)
SADD = [(0b1011, 0b0011), (0b1001, 0b0101), (0b1011, 0b0110), (0b0110, 0b1010), (0b1110, 0b0011)]
V = SADD + [(b, a) for a, b in SADD]
W.append(Q(id="SADD", name="SADD", title="החיבורים מהשקפים", inputs=[9], flat=True,
    outs=[("G", i) for i in range(8)], hexes=[None, None, None, None], variants=V, small=True,
    tables=lambda p: const(bitsof(p[1], 4) + bitsof(p[0], 4)), answer=lambda p: ((p[0] + p[1]) >> 4, 0x1),
    describe=lambda p: f"{p[0]:04b} + {p[1]:04b} = {p[0] + p[1]:05b}",
    B=["A = LEDG7..LEDG4     B = LEDG3..LEDG0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בנורות אחד מתרגילי החיבור של 4 ביטים מהשקפים:"] + CALEG +
            ["חברו עמודה אחרי עמודה מימין, עם נשא לעמודה הבאה, כמו בשקף.",
             "כתבו רק את 4 הביטים של הסכום (בלי הנשא האחרון):", "SW3..SW0"] + BIN4,
            lambda q, p: ((p[0] + p[1]) & 15, 0xF)),
           (["האם יצא נשא מהעמודה השמאלית (הסכום לא נכנס ב-4 ביטים = גלישה)?"] + CALEG +
            ["יש נשא - הרימו:", "SW0", "אין - השאירו למטה."], lambda q, p: ((p[0] + p[1]) >> 4, 0x1))]))

# slide 37: sign / magnitude, like +6 = 0110, -6 = 1110
V = [v for v in range(-7, 8) if v not in (0, 6, -6)]
W.append(Q(id="SSM", name="SSM", title="סימן וגודל כמו בשקף", inputs=[9], flat=True,
    outs=[("M", 1)] + hexd(0), hexes=[None, None, None, None], variants=V, small=True,
    tables=lambda v: const([1 if v < 0 else 0] + bitsof(abs(v), 4)),
    answer=lambda v: ((8 if v < 0 else 0) | abs(v), 0xF),
    describe=lambda v: f"{v} = {(8 if v < 0 else 0) | abs(v):04b} (sign / magnitude)",
    B=["the number = HEX1 HEX0 (decimal, a minus on HEX1 if negative)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: בשיטת סימן וגודל, 4 ביטים:", "+6 = 0110     -6 = 1110",
             "בתצוגה מספר עשרוני עם סימן:", "HEX1 HEX0",
             "מה הגודל שלו (בלי הסימן), ב-3 ביטים?", "4 = SW2     2 = SW1     1 = SW0"],
            lambda q, v: (abs(v), 0x7)),
           (["עכשיו כל המספר בסימן וגודל: הוסיפו את ביט הסימן משמאל (1 = שלילי, 0 = חיובי).", "HEX1 HEX0",
             "SW3 = the sign bit     SW2 SW1 SW0 = the magnitude"],
            lambda q, v: ((8 if v < 0 else 0) | abs(v), 0xF))]))

# slides 41-42: reversing the sign (invert the bits, add 1)
V = [v for v in range(1, 16) if v not in (3, 8)]
W.append(Q(id="SREV", name="SREV", title="היפוך סימן כמו בשקף", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=V, small=True,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (tw(-sval(v)), 0xF),
    describe=lambda v: f"{v:04b} = {sval(v)} -> flip {~v & 15:04b} -> {tw(-sval(v)):04b} = {-sval(v)}",
    B=["the number = LEDG3..LEDG0 (two's complement, 4 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: היפוך הסימן של 3 = הופכים את כל הביטים ומוסיפים 1:",
             "0011  ->  1100  ->  + 1  =  1101 = -3",
             "בנורות מספר במשלים ל-2, 4 ביטים:", "LEDG3..LEDG0",
             "שלב 1: הפכו את כל הביטים שלו (0 ל-1, 1 ל-0):", "SW3..SW0"],
            lambda q, v: (~v & 15, 0xF)),
           (["שלב 2: הוסיפו 1 לתוצאה של שלב 1, ושמרו 4 ביטים. זה המספר עם הסימן ההפוך:", "SW3..SW0"] + BIN4,
            lambda q, v: (tw(-sval(v)), 0xF))]))

# slides 53-54: the six 2-input gates, in the slides' order; the inputs to set are shown on HEX1 HEX0
GLED = ["AND = LEDG0   OR = LEDG1   XOR = LEDG2   NAND = LEDG3   NOR = LEDG4   XNOR = LEDG5"]
GSW = ["AND -> SW0   OR -> SW1   XOR -> SW2   NAND -> SW3   NOR -> SW4   XNOR -> SW5"]
def gates_at(r):
    return sum(GATES2[g][1][r] << g for g in range(6))
W.append(Q(id="SGATES", name="SGATES", title="ששת השערים מהשקף", inputs=[9, 8], flat=True,
    outs=[("G", i) for i in range(6)] + [("H", (1, 0)), ("H", (0, 0))], hexes=[[9], [8], None, None],
    variants=list(range(4)), small=True,
    tables=lambda r: [GATES2[g][1] for g in range(6)] + [[r >> 1] * 4, [r & 1] * 4],
    answer=lambda r: (gates_at(3 - r), 0x3F), describe=lambda r: f"A B = {r >> 1}{r & 1}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     the inputs to set = HEX1 HEX0     answer: SW5..SW0"], L=[], F=[],
    steps=[(["בלוח ששת השערים של שתי כניסות מהשקף, כל אחד בנורה:"] + GLED +
            ["שימו את הכניסות שמוצגות בשתי הספרות הימניות:", "SW9 = HEX1     SW8 = HEX0",
             "אילו שערים נותנים 1? בדקו בטבלאות מהשקף ובנורות, והרימו את המתגים שלהם:"] + GSW,
            lambda q, r: (gates_at(r), 0x3F)),
           (["עכשיו הפכו את שתי הכניסות:", "SW9 = not HEX1     SW8 = not HEX0"] + GLED +
            ["אילו שערים נותנים 1 עכשיו? הרימו את המתגים שלהם:"] + GSW,
            lambda q, r: (gates_at(3 - r), 0x3F))]))

# slide 66: the CMOS NAND gate and its table of transistors
W.append(Q(id="SNAND", name="SNAND", title="שער הנאנד מהשקף", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("H", (1, 0)), ("H", (0, 0))], hexes=[[9], [8], None, None], variants=list(range(4)), small=True,
    tables=lambda r: [TG[0], [r >> 1] * 4, [r & 1] * 4], answer=lambda r: (onoff((0, r >> 1, r & 1)), 0xF),
    describe=lambda r: f"A B = {r >> 1}{r & 1}: Y = {TG[0][r]}, ON {onoff((0, r >> 1, r & 1)):04b}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     Y = LEDG0     the inputs to set = HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השער מטרנזיסטורים מהשקף:", "NAND", "A = SW9     B = SW8     Y = LEDG0",
             "שימו את הכניסות שמוצגות בשתי הספרות הימניות:", "SW9 = HEX1     SW8 = HEX0",
             "הנורה דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."], lambda q, r: (TG[0][r], 0x1)),
           (["באותן כניסות, אילו טרנזיסטורים דולקים? כמו בטבלה שבשקף. דולק - הרימו את המתג שלו:",
             "SW9 = HEX1     SW8 = HEX0",
             "pMOS: ON when gate = 0     nMOS: ON when gate = 1",
             "P1 (A) = SW3     P2 (B) = SW2     N1 (A) = SW1     N2 (B) = SW0"],
            lambda q, r: (onoff((0, r >> 1, r & 1)), 0xF))]))

# slide 68: the CMOS NOR3 gate (three pMOS in series, three nMOS in parallel)
NOR3T = [1 if r == 0 else 0 for r in range(8)]
W.append(Q(id="SNOR3", name="SNOR3", title="שער נור של שלוש כניסות מהשקף", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))], hexes=[None, None, None, None],
    variants=list(range(8)), small=True,
    tables=lambda r: [NOR3T, [r >> 2] * 8, [(r >> 1) & 1] * 8, [r & 1] * 8],
    answer=lambda r: (bin(r).count("1"), 0x3),
    describe=lambda r: f"A B C = {r:03b}: Y = {NOR3T[r]}, {bin(r).count('1')} nMOS ON",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0     the inputs to set = HEX2 HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השער מטרנזיסטורים מהשקף:", "NOR3", "A = SW9   B = SW8   C = SW7   Y = LEDG0",
             "שימו את הכניסות שמוצגות בשלוש הספרות הימניות:", "SW9 = HEX2     SW8 = HEX1     SW7 = HEX0",
             "הנורה דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."], lambda q, r: (NOR3T[r], 0x1)),
           (["למטה בשקף שלושה טרנזיסטורים במקביל, אחד לכל כניסה:", "nMOS: ON when gate = 1",
             "SW9 = HEX2     SW8 = HEX1     SW7 = HEX0",
             "כמה מהם דולקים באותן כניסות?", "0 = all down     1 = SW0     2 = SW1     3 = SW1+SW0"],
            lambda q, r: (bin(r).count("1"), 0x3))]))

# ================================================================ more easy questions from the slides (after the first ones)
# slide 16: counting in binary
W.append(Q(id="SCOUNT", name="SCOUNT", title="ספירה בבינארי כמו בשקף", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=list(range(14)), small=True,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (v + 2, 0xF),
    describe=lambda v: f"{v:04b} -> {v + 1:04b} -> {v + 2:04b}",
    B=["the number = LEDG3..LEDG0 (binary, 4 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["הספירה בבינארי מהשקף:", "0, 1, 10, 11, 100, 101, 110, 111 ...",
             "בנורות הירוקות מספר בינארי של 4 ביטים:", "the number = LEDG3..LEDG0",
             "מה המספר הבא בספירה (המספר ועוד 1)? כתבו אותו בבינארי:", "SW3..SW0"] + BIN4,
            lambda q, v: (v + 1, 0xF)),
           (["ומה המספר שבא אחריו (המספר שבנורות ועוד 2)? כתבו אותו בבינארי:", "the number = LEDG3..LEDG0",
             "SW3..SW0"] + BIN4, lambda q, v: (v + 2, 0xF))]))

# slide 21: N bits - the largest number and how many values (example: 3 bits = 8 values, 0..7)
PWV = ["4 = SW2     8 = SW3     16 = SW4     32 = SW5", "64 = SW6     128 = SW7     256 = SW8"]
BITSW = ["1st bit = SW0     2nd bit = SW1     3rd bit = SW2     ...     8th bit = SW7"]
W.append(Q(id="SRANGE", name="SRANGE", title="כמה ערכים בכמה ביטים, כמו בשקף", inputs=[9], flat=True,
    outs=hexd(0), hexes=[None, None, None, None], variants=[2, 4, 5, 6, 7, 8], small=True,
    tables=lambda n: const(bitsof(n, 4)), answer=lambda n: (1 << n, 0x1FF),
    describe=lambda n: f"N = {n}: {1 << n} values, 0..{(1 << n) - 1}",
    B=["N = HEX0 (the number of bits)     answer: SW8..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: מספר בינארי של 3 ביטים:", "3 bits:   8 values,   range 0..7 = 000..111",
             "בתצוגה מספר הביטים:", "N = HEX0",
             "מה המספר הגדול ביותר שנכנס בכמה ביטים כאלה? כתבו אותו בבינארי:"] + BITSW,
            lambda q, n: ((1 << n) - 1, 0xFF)),
           (["כמה ערכים שונים אפשר לכתוב בכמה ביטים כאלה?", "N = HEX0", "3 bits -> 8 values",
             "הרימו את המתג של התשובה:"] + PWV, lambda q, n: (1 << n, 0x1FF))]))

# slide 23: the table of hex digits (decimal 10..15 -> a letter -> binary)
LETS = ["A = all down     B = SW0     C = SW1", "D = SW1+SW0     E = SW2     F = SW2+SW0"]
W.append(Q(id="SHEXDIG", name="SHEXDIG", title="טבלת ספרות ההקס מהשקף", inputs=[9], flat=True,
    outs=hexd(1) + hexd(0), hexes=[None, None, None, None], variants=list(range(10, 16)), small=True,
    tables=lambda v: const(bitsof(1, 4) + bitsof(v - 10, 4)), answer=lambda v: (v, 0xF),
    describe=lambda v: f"{v} = 0x{v:X} = {v:04b}",
    B=["the number = HEX1 HEX0 (decimal)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["טבלת ספרות ההקס מהשקף: מ-10 עד 15 הספרות הן אותיות:",
             "A = 10   B = 11   C = 12   D = 13   E = 14   F = 15",
             "בתצוגה מספר עשרוני:", "the number = HEX1 HEX0",
             "איזו ספרת הקס הוא? הרימו את המתגים שלה:"] + LETS, lambda q, v: (v - 10, 0x7)),
           (["כתבו את אותה ספרה בבינארי, כמו בעמודה הימנית של הטבלה בשקף:", "the number = HEX1 HEX0",
             "A = 10   B = 11   C = 12   D = 13   E = 14   F = 15", "SW3..SW0"] + BIN4,
            lambda q, v: (v, 0xF))]))

# slide 40: the msb of a two's complement number weighs -8
W4 = ["LEDG3 = -8     LEDG2 = 4     LEDG1 = 2     LEDG0 = 1"]
W.append(Q(id="SMSBW", name="SMSBW", title="משקל הביט השמאלי במשלים ל-2", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None],
    variants=[v for v in range(16) if v not in (7, 8)], small=True,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (abs(sval(v)), 0xF),
    describe=lambda v: f"{v:04b} = {-8 * (v >> 3)} + {v & 7} = {sval(v)}",
    B=["the number = LEDG3..LEDG0 (two's complement, 4 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["מהשקף: במשלים ל-2 המשקל של הביט השמאלי שלילי:",
             "0111 = +7 (most positive)     1000 = -8 (most negative)",
             "בנורות הירוקות מספר במשלים ל-2, 4 ביטים:"] + W4 +
            ["האם הנורה של מינוס 8 דולקת?", "דולקת - הרימו:", "SW0", "כבויה - השאירו למטה."],
            lambda q, v: (v >> 3, 0x1)),
           (["מה הערך של שלוש הנורות הימניות (בלי הנורה של מינוס 8)?"] + W4 + DIG,
            lambda q, v: (v & 7, 0xF)),
           (["הערך של המספר = מינוס 8 אם הנורה השמאלית דולקת, ועוד הערך של שלוש הימניות.",
             "מה הערך המוחלט של המספר?"] + W4 + DIG, lambda q, v: (abs(sval(v)), 0xF))]))

# slide 45: the same 4 bits in sign / magnitude and in two's complement
W.append(Q(id="SCMP", name="SCMP", title="אותם ביטים בשתי שיטות, כמו בשקף", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None], variants=list(range(8, 16)), small=True,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (16 - v, 0xF),
    describe=lambda v: f"{v:04b}: sign / magnitude -{v & 7}, two's complement -{16 - v}",
    B=["the bits = LEDG3..LEDG0 (4 bits)     answer: SW3..SW0"], L=[], F=[],
    steps=[(["השוואת השיטות מהשקף: אותם 4 ביטים הם מספר אחר בכל שיטה.",
             "בנורות הירוקות 4 ביטים, והביט השמאלי 1 (שלילי בשתי השיטות):", "the bits = LEDG3..LEDG0",
             "בשיטת סימן וגודל: הביט השמאלי = הסימן, שלושת הימניים = הגודל.",
             "מה הערך המוחלט של המספר בסימן וגודל?"] + DIG, lambda q, v: (v & 7, 0xF)),
           (["ועכשיו אותם ביטים במשלים ל-2. מה הערך המוחלט?", "the bits = LEDG3..LEDG0",
             "הפכו את כל הביטים והוסיפו 1."] + DIG, lambda q, v: (16 - v, 0xF))]))

# slide 49: zero extension changes the value of a negative number (1011 = -5 -> 0000 1011 = 11)
W.append(Q(id="SZEXT", name="SZEXT", title="הרחבה באפסים משנה את הערך", inputs=[9], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[None, None, None, None],
    variants=[v for v in range(8, 16) if v != 11], small=True,
    tables=lambda v: const(bitsof(v, 4)), answer=lambda v: (v % 10, 0xF),
    describe=lambda v: f"{v:04b} = {sval(v)} -> 0000 {v:04b} = {v}",
    B=["the number = LEDG3..LEDG0 (two's complement, 4 bits)     answer: SW7..SW0"], L=[], F=[],
    steps=[(["הדוגמה מהשקף: הרחבה באפסים של מספר שלילי:", "1011 = -5   ->   0000 1011 = 11",
             "בנורות הירוקות מספר שלילי במשלים ל-2, 4 ביטים:", "the number = LEDG3..LEDG0",
             "הרחיבו אותו באפסים ל-8 ביטים: 4 הביטים העליונים 0.",
             "SW7 SW6 SW5 SW4 = the upper 4 bits     SW3 SW2 SW1 SW0 = the lower 4 bits"],
            lambda q, v: (v, 0xFF)),
           (["אחרי ההרחבה באפסים המספר חיובי. ספרת העשרות של הערך העשרוני שלו היא 1.",
             "the number = 0000 LEDG3 LEDG2 LEDG1 LEDG0",
             "מה ספרת האחדות שלו?"] + DIG, lambda q, v: (v % 10, 0xF))]))

# slide 55: the 3-input XOR = odd parity
XOR3T = [bin(r).count("1") & 1 for r in range(8)]
X3LEG = ["A = SW9   B = SW8   C = SW7   Y = LEDG0"]
X3SET = ["SW9 = HEX2     SW8 = HEX1     SW7 = HEX0"]
W.append(Q(id="SXOR3", name="SXOR3", title="שער זוגיות של שלוש כניסות מהשקף", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0), ("H", (2, 0)), ("H", (1, 0)), ("H", (0, 0))], hexes=[None, None, None, None],
    variants=list(range(8)), small=True,
    tables=lambda r: [XOR3T, [r >> 2] * 8, [(r >> 1) & 1] * 8, [r & 1] * 8],
    answer=lambda r: (XOR3T[r], 0x1),
    describe=lambda r: f"A B C = {r:03b}: {bin(r).count('1')} ones, Y = {XOR3T[r]}",
    B=["A = SW9   B = SW8   C = SW7   Y = LEDG0     the inputs to set = HEX2 HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השער של שלוש כניסות מהשקף:", "XOR3:   Y = 1 when an odd number of inputs are 1"] + X3LEG +
            ["שימו את הכניסות שמוצגות בשלוש הספרות הימניות:"] + X3SET +
            ["כמה כניסות למעלה?", "0 = all down     1 = SW0     2 = SW1     3 = SW1+SW0"],
            lambda q, r: (bin(r).count("1"), 0x3)),
           (["באותן כניסות: מה היציאה?", "XOR3:   Y = 1 when an odd number of inputs are 1"] + X3LEG + X3SET + LIT,
            lambda q, r: (XOR3T[r], 0x1))]))

# slide 65: the CMOS NOT gate and its table (P1, N1)
W.append(Q(id="SNOT", name="SNOT", title="שער המהפך מטרנזיסטורים מהשקף", inputs=[9], flat=True,
    outs=[("G", 0), ("H", (0, 0))], hexes=[[9], None, None, None], variants=[0, 1], small=True,
    tables=lambda r: [[1, 0], [r] * 2], answer=lambda r: (1 if r else 2, 0x3),
    describe=lambda r: f"A = {r}: Y = {1 - r}, {'N1' if r else 'P1'} ON",
    B=["A = SW9 (HEX3)     Y = LEDG0     the input to set = HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השער מטרנזיסטורים מהשקף:", "NOT:   P1 = pMOS (to VDD)     N1 = nMOS (to GND)",
             "A = SW9     Y = LEDG0", "שימו את הכניסה שמוצגת בספרה הימנית:", "SW9 = HEX0"] + LIT,
            lambda q, r: (1 - r, 0x1)),
           (["באותה כניסה, איזה טרנזיסטור דולק? כמו בטבלה שבשקף. הרימו את המתג שלו:", "SW9 = HEX0",
             "pMOS: ON when gate = 0     nMOS: ON when gate = 1", "P1 = SW1     N1 = SW0"],
            lambda q, r: (1 if r else 2, 0x3))]))

# slide 69: AND2 = NAND2 followed by NOT
TAND = [(r >> 1) & r & 1 for r in range(4)]
A2LEG = ["A = SW9     B = SW8     Y = LEDG0"]
A2SET = ["SW9 = HEX1     SW8 = HEX0"]
W.append(Q(id="SAND2", name="SAND2", title="שער וגם מטרנזיסטורים מהשקף", inputs=[9, 8], flat=True,
    outs=[("G", 0), ("H", (1, 0)), ("H", (0, 0))], hexes=[[9], [8], None, None], variants=list(range(4)), small=True,
    tables=lambda r: [TAND, [r >> 1] * 4, [r & 1] * 4], answer=lambda r: (TAND[r], 0x1),
    describe=lambda r: f"A B = {r >> 1}{r & 1}: NAND = {1 - TAND[r]}, Y = {TAND[r]}",
    B=["A = SW9 (HEX3)     B = SW8 (HEX2)     Y = LEDG0     the inputs to set = HEX1 HEX0     answer: SW3..SW0"], L=[], F=[],
    steps=[(["בלוח השער מהשקף, בשני שלבים:", "AND2 = NAND2 -> NOT"] + A2LEG +
            ["שימו את הכניסות שמוצגות בשתי הספרות הימניות:"] + A2SET +
            ["מה היציאה של השלב הראשון?", "NAND2:   0 only when A = B = 1", "1 - הרימו:", "SW0", "0 - השאירו למטה."],
            lambda q, r: (1 - TAND[r], 0x1)),
           (["והיציאה של השער כולו, אחרי המהפך?", "AND2 = NAND2 -> NOT"] + A2LEG + A2SET + LIT,
            lambda q, r: (TAND[r], 0x1))]))

ORDER = ["SPOW", "SBIN5", "SHEX3", "SCOUNT", "SRANGE", "SHEXDIG",
         "DEC2BIN", "DIV2", "HEX2BIN", "BIN2DEC", "BINCOUNT", "BYTE", "HEX2DEC", "DEC2HEX", "BITS", "POW2",
         "SADD", "SSM", "SREV", "SMSBW", "SCMP", "SZEXT",
         "ADDER", "COLADD", "SIGNMAG", "SMFAIL", "TWOS", "NEGATIVE", "SIGNED8", "RANGES", "OPS", "SUBTRACT", "OVERFLOW",
         "EXTEND", "EXTBOX",
         "SGATES", "SNAND", "SNOR3", "SXOR3", "SNOT", "SAND2",
         "NOTBUF", "GATE2", "GATESET", "GATE3", "GATE4", "PARITY", "ONOFF", "CMOS", "COMPLEX"]
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
    G.write(f"{HERE}/instructor_guide/guide.html", G.answers_guide(a.answers))
    print("FAILED: " + " ".join(bad) if bad else "all OK")
    sys.exit(1 if bad else 0)
