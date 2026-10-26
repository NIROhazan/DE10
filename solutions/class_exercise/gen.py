# Class exercise (lecture 3, Harris ch. 2, slides 1 and 3-106) - boards, keys and questions. Instructor only.
#
#   python gen.py                 build every question and simulate it in iverilog
#   python gen.py --compile       also compile with Quartus 13.0sp1 and copy Qnn.sof to C:/DE10/solutions/de1/week3/sof
#   python gen.py --only Q05      one question (with or without --compile)
#   python gen.py --id 316009489  a student's login number, every step's answer (switches) and code
#
# Every question is the same hardware (ce.v), in small STEPS. Step 0 = login, the last step = the question itself.
#   LOGIN   the student sets their login number (10 bits, from the ID) on SW9..0 and presses KEY3. The board shows
#           the code of step 0 (a receipt) until the first switch moves - the PC checks it, so a wrong login is caught.
#   PLAY    a hidden puzzle: every output (LED) is a table over the input switches. Each table entry is
#           0, 1 or HOLD (keep the last value - that is how the memory boxes of Q01-Q02 work).
#   ANSWER  KEY3 (LEDG7 on, LEDG2..0 = the step). The answer of the CURRENT step is set on the switches; while KEY2 is
#           held the board shows that step's code if it is right, otherwise "Err". Releasing KEY2 after a right answer
#           moves the board to the next step. KEY1 shows the last code the board gave.
# The PC knows neither the answers nor the codes. Code of step k = 3 hidden hex digits + a public check digit over
# them, the login number and k - so the PC can say PASS / FAIL for every step, and catches a code of another step.
# Hidden digits: mix(secret, k) in logic; secret = 16 bits of HMAC(key, "Qnn|login") in a ROM.
# The variant of a question is picked by the login number: var = pub * nsec + sec, where pub (public, MD5)
# picks what is printed on the screen and sec (secret, HMAC) picks what is hidden in the board.
import argparse, hashlib, hmac, itertools, os, random, re, secrets, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
REPO = "C:/DE10/solutions/de1/week3"	# the DE1 build; C:/DE10/week3 is the DE10-Lite port (de10/port.py)
QBIN = "C:/altera/13.0sp1/quartus/bin64"
IVL = "C:/iverilog/bin"
HOLD = 2

# ---------------------------------------------------------------- key, login number, codes
kf = f"{HERE}/key.txt"
if not os.path.exists(kf):
    open(kf, "w").write(secrets.token_hex(16) + "\n")
KEY = open(kf).read().strip().encode("ascii")

def login_of(sid):
    b = hashlib.md5(("DE10ce|" + sid).encode("ascii")).digest()
    return (b[0] + 256 * b[1]) % 1024

def pub_of(qid, s, npub):
    return hashlib.md5(f"DE10ce|{qid}|{s}".encode("ascii")).digest()[0] % npub if npub > 1 else 0

def mac(msg):
    return hmac.new(KEY, msg.encode("ascii"), hashlib.sha256).digest()

LECTURE = "3"		# the lecture number in the instructor guide
PREFIX = ""		# "" = lecture 3; another lecture sets its own (gen_w2.py: "w2|") - codes and variants differ
def secret_of(qid, s):
    return int.from_bytes(mac(f"{PREFIX}{qid}|{s}")[0:2], "big")

K1 = [int.from_bytes(mac(f"K1|{k}")[0:2], "big") for k in range(8)]
K2 = [int.from_bytes(mac(f"K2|{k}")[0:2], "big") for k in range(8)]

def mix(sec, k):
    x = sec ^ K1[k]
    x = (x + (((x << 5) | (x >> 11)) & 0xFFFF)) & 0xFFFF
    x = x ^ (x >> 7)
    return (x + K2[k]) & 0xFFFF

def check_digit(d3, d2, d1, s, k):
    return (d3 + 3 * d2 + 5 * d1 + 7 + 9 * (s & 15) + 11 * ((s >> 4) & 15) + 13 * (s >> 8) + 15 * k) % 16

def code_of(qid, s, k):
    x = mix(secret_of(qid, s), k)
    d3, d2, d1 = x >> 12, (x >> 8) & 15, (x >> 4) & 15
    return (d3, d2, d1, check_digit(d3, d2, d1, s, k))

def code_str(qid, s, k):
    return "".join(f"{d:X}" for d in code_of(qid, s, k))

def var_of(q, s):
    sec = int.from_bytes(mac(f"{PREFIX}{q.id}|{s}")[2:4], "big") % q.nsec
    return pub_of(q.id, s, q.npub) * q.nsec + sec

# ---------------------------------------------------------------- Boolean helpers
def bits(r, n):
    return [(r >> (n - 1 - i)) & 1 for i in range(n)]		# MSB first: A, B, C, ...

def parse(expr):
    toks = re.findall(r"[A-Z]|[()+'01*]", expr.replace(" ", ""))
    pos = 0
    def peek():
        return toks[pos] if pos < len(toks) else ""
    def take():
        nonlocal pos
        pos += 1
        return toks[pos - 1]
    def p_or():
        a = p_and()
        while peek() == "+":
            take(); b = p_and(); a = (lambda x, y: lambda e: x(e) | y(e))(a, b)
        return a
    def p_and():
        a = p_not()
        while peek() and (peek() in "(01*" or peek().isalpha()):
            if peek() == "*":
                take()
            b = p_not(); a = (lambda x, y: lambda e: x(e) & y(e))(a, b)
        return a
    def p_not():
        a = p_atom()
        while peek() == "'":
            take(); a = (lambda x: lambda e: 1 - x(e))(a)
        return a
    def p_atom():
        t = take()
        if t == "(":
            a = p_or()
            assert take() == ")", expr
            return a
        if t in "01":
            return (lambda v: lambda e: v)(int(t))
        return lambda e, t=t: e[t]
    f = p_or()
    assert pos == len(toks), expr
    return f

def table_of(expr, names):
    f = parse(expr)
    n = len(names)
    return [f(dict(zip(names, bits(r, n)))) for r in range(1 << n)]

def min_sop(tt, n):
    """(terms, literals) of the minimal SOP: fewest implicants, then fewest literals."""
    ones = frozenset(r for r in range(1 << n) if tt[r])
    if not ones:
        return (0, 0)
    imps = []
    for lits in itertools.product((None, 0, 1), repeat=n):
        rs = frozenset(r for r in range(1 << n) if all(l is None or bits(r, n)[i] == l for i, l in enumerate(lits)))
        if rs <= ones:
            imps.append((rs, sum(l is not None for l in lits)))
    primes = [(rs, c) for rs, c in imps if not any(rs < r2 for r2, _ in imps)]
    for k in range(1, len(primes) + 1):
        best = None
        for combo in itertools.combinations(primes, k):
            if frozenset().union(*[rs for rs, _ in combo]) == ones:
                lit = sum(c for _, c in combo)
                best = lit if best is None else min(best, lit)
        if best is not None:
            return (k, best)

def depends(tt, n, i):
    return any(tt[r] != tt[r ^ (1 << (n - 1 - i))] for r in range(1 << n))

# ---------------------------------------------------------------- a question
class Q:
    """id, name, title; inputs = switch numbers MSB first; outs = ('R', i) / ('G', i) per output;
    hexes = 4 entries for HEX3..HEX0: None, a letter, or a list of switch numbers (one hex digit);
    variants[var] = params; tables(params) -> per output a list of 0/1/HOLD per row;
    answer(params) -> (want, mask) on SW9..0; text: B (board), L (question), F (answer format), P[pub]."""
    def __init__(self, **kw):
        self.npub, self.seq, self.P, self.sb = 1, False, {}, 0
        self.__dict__.update(kw)
        self.n = len(self.inputs) + self.sb		# sb state bits (a clocked question) = the row's high bits
        if self.sb:
            assert sorted(i for k, i in self.outs if k == "N") == list(range(self.sb)), self.id
        self.vb = max(1, (len(self.variants) - 1).bit_length()) if (self.sb or kw.get("small")) else 8	# variant bits of the table ROM
        assert 2 * len(self.outs) * (1 << (self.vb + self.n)) <= 140000, self.id
        if self.npub == 1:
            self.nsec = len(self.variants)
        assert len(self.variants) == self.npub * self.nsec <= 256, self.id
        assert len(self.outs) <= 24

def legend(names, inputs):
    return ", ".join(f"{a} = SW{s}" for a, s in zip(names, inputs))

def perms_sample(rng, items, k):
    allp = list(itertools.permutations(items))
    return [list(p) for p in (allp if k >= len(allp) else rng.sample(allp, k))]

QS = []
rng = random.Random(20261006)
ABC, ABCD = ["A", "B", "C"], ["A", "B", "C", "D"]
IN2, IN3, IN4 = [1, 0], [2, 1, 0], [3, 2, 1, 0]
HX2 = [None, None, [1], [0]]
HX3 = [None, [2], [1], [0]]
HX4 = [[3], [2], [1], [0]]
COMB2 = [[(t >> (3 - r)) & 1 for r in range(4)] for t in range(1, 15)]
ROWS2 = "rows A B = 00, 01, 10, 11"

# ---- Q01: memory or not (slides 4-7)
SEQ = {"SR, A sets, B resets": [HOLD, 0, 1, HOLD], "SR, B sets, A resets": [HOLD, 1, 0, HOLD],
       "D latch, B enables, D = A": [HOLD, 0, HOLD, 1], "D latch, A enables, D = B": [HOLD, HOLD, 0, 1],
       "C-element": [0, HOLD, HOLD, 1], "inverted C-element": [1, HOLD, HOLD, 0],
       "D latch, B' enables, D = A": [0, HOLD, 1, HOLD], "D latch, A' enables, D = B": [0, 1, HOLD, HOLD]}
v01 = []
for _ in range(256):
    pos = rng.sample(range(8), rng.choice([3, 4, 5]))
    v01.append([("seq", rng.choice(list(SEQ))) if i in pos else ("comb", rng.choice(COMB2)) for i in range(8)])
QS.append(Q(id="Q01", name="SEQ", title="Combinational or sequential? (8 black boxes)", inputs=IN2, seq=True,
    outs=[("R", i) for i in range(8)], hexes=HX2, variants=v01,
    tables=lambda p: [SEQ[t] if k == "seq" else t for k, t in p],
    answer=lambda p: (sum(1 << i for i, (k, _) in enumerate(p) if k == "seq"), 0xFF),
    describe=lambda p: "; ".join(f"box{i}: {t if k == 'seq' else 'comb ' + ''.join(map(str, t))}" for i, (k, t) in enumerate(p)),
    B=["Inputs: A = SW1, B = SW0 (HEX1, HEX0). Box i = LEDRi (8 boxes, all get the same A and B).",
       "Change ONE switch at a time - two at once pass through a row in between."],
    L=["Some boxes are combinational (the output depends only on A and B now), some are sequential",
       "(they remember: the same A, B can give a different output, depending on what came before).",
       "Find which boxes are sequential. Try different ORDERS of A, B - not only the four rows."],
    F=["SWi = 1 if box i is sequential, 0 if combinational (SW7..SW0)."]))

# ---- Q02: the latch (slides 6-7)
v02 = [(s, r) for s in range(4) for r in range(4) if s != r]
QS.append(Q(id="Q02", name="LATCH", title="A box with memory: what sets it, what resets it?", inputs=IN2, seq=True,
    outs=[("R", 0)], hexes=HX2, variants=v02,
    tables=lambda p: [[1 if r == p[0] else 0 if r == p[1] else HOLD for r in range(4)]],
    answer=lambda p: ((p[0] << 2) | p[1], 0xF),
    describe=lambda p: f"set at AB={p[0]:02b}, reset at AB={p[1]:02b}",
    B=["Inputs: A = SW1, B = SW0 (HEX1, HEX0). The box = LEDR0. It starts at 0."],
    L=["One input row (A B) sets the box to 1, one row resets it to 0, the other two rows keep (hold)",
       "the last value. Find the set row and the reset row."],
    F=["SW3 SW2 = A B of the SET row,  SW1 SW0 = A B of the RESET row."]))

# ---- Q03: maxterms, POS (slides 9-13)
QS.append(Q(id="Q03", name="PI", title="Maxterms: write F as a product of sums, F = PI(...)", inputs=IN2,
    outs=[("R", 0)], hexes=HX2, variants=COMB2,
    tables=lambda p: [p], answer=lambda p: (sum(1 << r for r in range(4) if p[r] == 0), 0xF),
    describe=lambda p: "F rows 00..11 = " + "".join(map(str, p)),
    B=["Inputs: A = SW1, B = SW0 (HEX1, HEX0). F = LEDR0."],
    L=["F is hidden in the board. Find its truth table and write F in canonical POS: F = PI(...)."],
    F=["SWi = 1 if maxterm i is in PI(...), row i = A B in binary (SW3..SW0)."]))

# ---- Q04: minterms, SOP (slides 9-16)
v04 = [[1 if r in ones else 0 for r in range(8)] for k in (3, 4, 5) for ones in itertools.combinations(range(8), k)]
QS.append(Q(id="Q04", name="SIGMA", title="Minterms: write F as a sum of products, F = SIGMA(...)", inputs=IN3,
    outs=[("R", 0)], hexes=HX3, variants=v04,
    tables=lambda p: [p], answer=lambda p: (sum(1 << r for r in range(8) if p[r]), 0xFF),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p)),
    B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). F = LEDR0."],
    L=["F is hidden in the board. Find its truth table and write F in canonical SOP: F = SIGMA(...)."],
    F=["SWi = 1 if minterm i is in SIGMA(...), row i = A B C in binary (SW7..SW0)."]))

# ---- Q05, Q06: which LED is a minterm / a maxterm (slide 10)
def term(kind):
    vs = sorted(rng.sample(range(3), {"min": 3, "max": 3, "p2": 2, "s2": 2, "lit": 1}[kind]))	# alphabetical (slide 62)
    pol = [rng.randint(0, 1) for _ in vs]
    lit = lambda r, i: bits(r, 3)[vs[i]] ^ pol[i]
    if kind in ("min", "p2", "lit"):
        tt = [int(all(lit(r, i) for i in range(len(vs)))) for r in range(8)]
    else:
        tt = [int(any(lit(r, i) for i in range(len(vs)))) for r in range(8)]
    name = (" " if kind in ("min", "p2", "lit") else " + ").join(ABC[v] + ("'" if p else "") for v, p in zip(vs, pol))
    return (kind, tt, name if kind in ("min", "p2", "lit") else "(" + name + ")")
v05 = []
for _ in range(256):
    nmin, nmax = rng.randint(1, 3), rng.randint(1, 3)
    kinds = ["min"] * nmin + ["max"] * nmax + [rng.choice(["p2", "s2", "lit"]) for _ in range(8 - nmin - nmax)]
    rng.shuffle(kinds)
    v05.append([term(k) for k in kinds])
for qid, kind, word in (("Q05", "min", "minterm"), ("Q06", "max", "maxterm")):
    QS.append(Q(id=qid, name=word.upper(), title=f"Which LEDs are {word}s?", inputs=IN3,
        outs=[("R", i) for i in range(8)], hexes=HX3, variants=v05,
        tables=lambda p: [t[1] for t in p],
        answer=lambda p, kind=kind: (sum(1 << i for i, t in enumerate(p) if t[0] == kind), 0xFF),
        describe=lambda p: ";  ".join(f"LEDR{i} = {t[2]}" for i, t in enumerate(p)),
        B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). LEDR7..LEDR0 = 8 hidden terms."],
        L=["Each LED is one term over A, B, C: a product (AND of literals) or a sum (OR of literals),",
           "with 1, 2 or 3 literals. Find the LEDs that are " + word + "s.",
           "Hint: how many rows of the truth table light a minterm? how many rows turn a maxterm off?"],
        F=[f"SWi = 1 if LEDRi is a {word} (SW7..SW0)."]))

# ---- Q07: from a story to an equation (slides 14, 17-21)
STORIES = [
    (["You can Eat delicious food (E) if you Make it yourself (M), or you have a personal Chef (C)",
      "who is Talented (T) and not eXpensive (X)."], "MCTX",
     "M + CTX'", ["(M + C)TX'", "M + CTX", "M + C + TX'"]),
    (["The alarm sounds (Y) when the Door is open (D) and the system is Armed (A),",
      "or when there is Smoke (S) and it is not a Test (T)."], "DAST",
     "DA + ST'", ["DA + ST", "D(A + S)T'", "DA + S + T'"]),
    (["You pass (P) if you did the Homework (H) and the Exam (E) or the Lab (L),",
      "unless you Cheated (C)."], "HELC",
     "H(E + L)C'", ["HE + LC'", "H(E + L) + C'", "HELC'"]),
    (["The light (Y) is on when it is Dark (D) and someone Moves (M), or when the Switch (S) is on -",
      "but never when the Battery (B) is low."], "DMSB",
     "(DM + S)B'", ["DM + SB'", "DM + S + B'", "(D + M)SB'"]),
    (["You can Enter (E) with a Hat (H) and Shoes (S), or with a Hat and a Ticket (T),",
      "or if you are a VIP (V)."], "HSTV",
     "HS + HT + V", ["HST + V", "(H + V)(S + T)", "H + S + T + V"]),
    (["The fan (F) runs when it is Hot (H) and the window is not Open (O),",
      "or when a Kid (K) presses the Button (B)."], "HOKB",
     "HO' + KB", ["HO' + K + B", "HO'KB", "(H + O')(K + B)"]),
]
P24 = [list(p) for p in itertools.permutations(range(4))]
v07 = []
for st in STORIES:
    names = list(st[1])
    cands = [table_of(e, names) for e in [st[2]] + st[3]]
    assert len({tuple(c) for c in cands}) == 4, st[2]
    v07 += [(st, perm, cands) for perm in P24]
QS.append(Q(id="Q07", name="STORY", title="From a story to an equation", inputs=IN4,
    outs=[("R", i) for i in range(4)], hexes=HX4, variants=v07, npub=len(STORIES), nsec=24,
    tables=lambda p: [p[2][p[1][j]] for j in range(4)],
    answer=lambda p: (1 << p[1].index(0), 0xF),
    describe=lambda p: ";  ".join(f"LEDR{j} = {([p[0][2]] + p[0][3])[p[1][j]]}" for j in range(4)),
    B=["Inputs: SW3 SW2 SW1 SW0 = the four letters of your story, in the order given (HEX3..HEX0).",
       "LEDR3..LEDR0 = four circuits built by four students from the same story."],
    L=["Write the Boolean equation of the story (on paper). Only ONE LED implements it exactly."],
    P={i: st[0] + ["Letters: " + legend(list(st[1]), IN4)] for i, st in enumerate(STORIES)},
    F=["SWi = 1 for the LED that implements your story (one switch, SW3..SW0)."]))

# ---- Q08: which inputs do not matter (slides 20-21: E = HS + H)
v08 = []
while len(v08) < 256:
    used = sorted(rng.sample(range(4), rng.choice([2, 3])))
    tt = [rng.randint(0, 1) for _ in range(16)]
    tt = [tt[sum(bits(r, 4)[u] << i for i, u in enumerate(used))] for r in range(16)]
    if all(depends(tt, 4, u) for u in used) and tt not in [v[1] for v in v08]:
        v08.append((used, tt))
QS.append(Q(id="Q08", name="MATTER", title="Which inputs does the guard really look at?", inputs=IN4,
    outs=[("R", 0)], hexes=HX4, variants=v08,
    tables=lambda p: [p[1]], answer=lambda p: (sum(1 << (3 - u) for u in p[0]), 0xF),
    describe=lambda p: "uses " + "".join("HSTV"[u] for u in p[0]) + ", table " + "".join(map(str, p[1])),
    B=["Inputs: Hat H = SW3, Shoes S = SW2, Ticket T = SW1, VIP V = SW0 (HEX3..HEX0). Enter E = LEDR0."],
    L=["Like E = HS + H in the lecture: the guard's rule mentions all four, but some of them never change E.",
       "Find the inputs that DO matter (changing them alone changes E in at least one situation)."],
    F=["SW3 = H, SW2 = S, SW1 = T, SW0 = V: 1 if that input matters, 0 if E never depends on it."]))

# ---- Q09, Q10: perfect induction - the theorem lab (slides 23-44)
THMS = [("A(A + B)", "A", "T9 covering"), ("BC + BC'", "B", "T10 combining"),
        ("AB + A'C + BC", "AB + A'C", "T11 consensus"), ("(AB)'", "A' + B'", "T12 De Morgan"),
        ("(A + B)'", "A' + B'", "?"), ("A + BC", "(A + B)(A + C)", "T8' distributivity"),
        ("A + BC", "(A + B)C", "?"), ("A + A'B", "A + B", "simplification")]
TT = [(table_of(l, ABC), table_of(r, ABC)) for l, r, _ in THMS]
assert len(set((tuple(a), tuple(b)) for a, b in TT)) == 8
TRUE = [a == b for a, b in TT]
def pair_tables(perm):
    return [[TT[perm[r >> 3]][side][r & 7] for r in range(64)] for side in (0, 1)]
HX_PAIR = [[9, 8, 7], [2], [1], [0]]
B_PAIR = ["Pair k = SW9 SW8 SW7 (HEX3). Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0).",
          "LEDR1 = the LEFT side, LEDR0 = the RIGHT side of statement k (k = 0..7)."]
QS.append(Q(id="Q09", name="EQUAL", title="Perfect induction: which statements are true?", inputs=[9, 8, 7, 2, 1, 0],
    outs=[("R", 1), ("R", 0)], hexes=HX_PAIR, variants=perms_sample(rng, range(8), 256),
    tables=pair_tables, answer=lambda p: (sum(1 << k for k in range(8) if TRUE[p[k]]), 0xFF),
    describe=lambda p: ";  ".join(f"k{k}: {THMS[p[k]][0]} = {THMS[p[k]][1]}" for k in range(8)),
    B=B_PAIR,
    L=["The board holds 8 statements LEFT = RIGHT. Some are theorems, some are false.",
       "Prove or refute each one by perfect induction: check every row."],
    F=["SWk = 1 if statement k is TRUE (LEFT = RIGHT in all 8 rows), SW7..SW0."]))
ASK10 = [(0, 4), (1, 6), (2, 4), (3, 6), (5, 4), (7, 6), (3, 4), (5, 6)]
v10 = [(x, y, perm) for x, y in ASK10 for perm in perms_sample(rng, range(8), 32)]
QS.append(Q(id="Q10", name="WHERE", title="Perfect induction: find two statements on the board", inputs=[9, 8, 7, 2, 1, 0],
    outs=[("R", 1), ("R", 0)], hexes=HX_PAIR, variants=v10, npub=8, nsec=32,
    tables=lambda p: pair_tables(p[2]),
    answer=lambda p: (p[2].index(p[0]) | (p[2].index(p[1]) << 3), 0x3F),
    describe=lambda p: f"X at k={p[2].index(p[0])}, Y at k={p[2].index(p[1])}",
    B=B_PAIR,
    L=["These 8 statements are on the board, in a hidden order (pair k = 0..7):"] +
      [f"   {i}:  {l} = {r}" for i, (l, r, _) in enumerate(THMS)] +
      ["Write both sides of a statement as truth tables (on paper), then find it on the board."],
    P={i: [f"Find X = statement {x} ({THMS[x][0]} = {THMS[x][1]}) and Y = statement {y} ({THMS[y][0]} = {THMS[y][1]})."]
       for i, (x, y) in enumerate(ASK10)},
    F=["SW2 SW1 SW0 = the pair number k of X,  SW5 SW4 SW3 = the pair number k of Y."]))

# ---- Q11: minimal SOP (slides 45-48)
v11 = [tt for tt in ([(t >> r) & 1 for r in range(8)] for t in range(256))
       if 2 <= sum(tt) <= 6 and min_sop(tt, 3) != (1, 1)]		# all 232 of them
QS.append(Q(id="Q11", name="MINSOP", title="Simplify: the minimal sum of products", inputs=IN3,
    outs=[("R", 0)], hexes=HX3, variants=v11,
    tables=lambda p: [p], answer=lambda p: (min_sop(p, 3)[0] | (min_sop(p, 3)[1] << 4), 0xF7),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p)) + f", min SOP (terms, literals) = {min_sop(p, 3)}",
    B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). F = LEDR0."],
    L=["F is hidden in the board. Find it, then simplify it with the theorems to a minimal SOP",
       "(fewest implicants, and each implicant with the fewest literals)."],
    F=["SW2 SW1 SW0 = number of implicants (terms),  SW7 SW6 SW5 SW4 = number of literals (SW3 = 0)."]))

# ---- Q12: the hidden literal (slides 50-61)
LITS = ["A", "A'", "B", "B'", "C", "C'"]
EXPR12 = ["(A + B)(A' + ?) + BC", "A'B + ?C + A'BC'", "(AB + C)? + A'B'",
          "A'? + BC' + AB'C", "(A + ?)(B' + C) + A'BC'", "AB + A'? + B'C'"]
v12 = []
for e in EXPR12:
    tts = [table_of(e.replace("?", "(" + l + ")"), ABC) for l in LITS]
    assert len({tuple(t) for t in tts}) == 6, e
    v12 += [(e, i, tts[i]) for i in range(6)]
QS.append(Q(id="Q12", name="LITERAL", title="The hidden literal, then simplify", inputs=IN3,
    outs=[("R", 0)], hexes=HX3, variants=v12, npub=len(EXPR12), nsec=6,
    tables=lambda p: [p[2]], answer=lambda p: (p[1] | (min_sop(p[2], 3)[1] << 4), 0xF7),
    describe=lambda p: f"? = {LITS[p[1]]}, min SOP literals {min_sop(p[2], 3)[1]}",
    B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). Y = LEDR0."],
    L=["The board computes the expression below. One literal (?) is hidden: it is A, A', B, B', C or C'.",
       "Find it, then simplify Y to a minimal SOP and count its literals."],
    P={i: [f"Y = {e}"] for i, e in enumerate(EXPR12)},
    F=["SW2 SW1 SW0 = the hidden literal: 0 = A, 1 = A', 2 = B, 3 = B', 4 = C, 5 = C'.",
       "SW7 SW6 SW5 SW4 = number of literals in the minimal SOP of Y (SW3 = 0)."]))

# ---- candidates on LEDs: Q13 common errors (70-73), Q14 De Morgan (68-69, 89-92), Q15 multiply / factor (59-67)
def cand_question(qid, name, title, sets, names, ncand, nsec, L, F, B):
    inputs = IN3 if len(names) == 3 else IN4
    v = []
    for e, cands in sets:
        assert len(cands) == ncand, e
        ref = table_of(e, names)
        tts = [table_of(c, names) for c in cands]
        good = [t == ref for t in tts]
        assert any(good) and good.count(False) >= 2, (e, good)
        v += [(e, cands, tts, good, perm) for perm in perms_sample(rng, range(ncand), nsec)]
    return Q(id=qid, name=name, title=title, inputs=inputs, outs=[("R", j) for j in range(ncand)],
        hexes=HX3 if len(names) == 3 else HX4, variants=v, npub=len(sets), nsec=nsec,
        tables=lambda p: [p[2][p[4][j]] for j in range(ncand)],
        answer=lambda p: (sum(1 << j for j in range(ncand) if p[3][p[4][j]] == (qid != "Q13")), (1 << ncand) - 1),
        describe=lambda p: ";  ".join(f"LEDR{j} = {p[1][p[4][j]]}{'' if p[3][p[4][j]] else ' (wrong)'}" for j in range(ncand)),
        B=B, L=L, P={i: [f"Y = {e}"] for i, (e, _) in enumerate(sets)}, F=F)
QS.append(cand_question("Q13", "ERRORS", "Common errors: which simplifications are wrong?",
    [("A'BC + A'", ["A'", "A'B + A'", "A'BC", "A' + BC", "A' + B"]),
     ("AB + AB'", ["A", "A(B + B')", "B", "A + B'", "AB'"]),
     ("(A + BC)'", ["A'(B' + C')", "A'B' + A'C'", "A' + B'C'", "A'BC", "A'B'C'"]),
     ("(A + B)(A + C)", ["A + BC", "A + AC + AB + BC", "AB + AC", "(A + B)C", "A + BC'"]),
     ("AB + A'C + BC", ["AB + A'C", "AB + A'C + ABC", "AB + BC", "A'C + BC", "AB + C"]),
     ("A + A'B", ["A + B", "A + B + AB", "B", "AB", "A'B"])],
    ABC, 5, 40,
    ["Five students simplified the expression below. Their results are LEDR4..LEDR0.",
     "Some are right, some made a common error (lost a bar, De Morgan on a mix, a wrong step)."],
    ["SWi = 1 if LEDRi is WRONG (not equal to Y in some row), SW4..SW0."],
    ["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). LEDR4..LEDR0 = the five results."]))
QS.append(cand_question("Q14", "DEMORGAN", "De Morgan: which results are right?",
    [("((A + BD)C)'", ["A'B' + A'D' + C'", "A'(B' + D') + C'", "A'B'D' + C'", "A'(B' + D')C'"]),
     ("((A + B')C)'", ["A'B + C'", "A'B' + C'", "A'BC'", "(A' + B)C'"]),
     ("(A'B + CD')'", ["(A + B')(C' + D)", "AC' + AD + B'C' + B'D", "(A' + B)(C' + D)", "AB' + C'D"]),
     ("((A + B)(C + D)')'", ["A'B' + C + D", "A'B' + C'D'", "(A' + B')(C + D)", "A'B'CD"]),
     ("(A(B' + C) + D)'", ["(A' + BC')D'", "A'D' + BC'D'", "(A' + B'C')D'", "A' + BC' + D'"]),
     ("((AB)' + C)'", ["ABC'", "A'B'C'", "(A + B)C'", "A' + B' + C'"])],
    ABCD, 4, 24,
    ["Apply De Morgan to the expression below (from the outside in). LEDR3..LEDR0 are four answers."],
    ["SWi = 1 if LEDRi is RIGHT (equal to Y in all 16 rows), SW3..SW0."],
    ["Inputs: A = SW3, B = SW2, C = SW1, D = SW0 (HEX3..HEX0). LEDR3..LEDR0 = the four answers."]))
QS.append(cand_question("Q15", "MULTIPLY", "Multiplying out (SOP) and factoring (POS)",
    [("(A + C + D)(A + B)", ["A + BC + BD", "A + B(C + D)", "AB + AC + AD", "A + BCD", "AC + BD", "A + B + CD"]),
     ("(A + BC)(A + D)", ["A + BCD", "A + AD + ABC + BCD", "A + BC + D", "AD + BC", "A + BD + CD", "ABCD"]),
     ("A + B'CD", ["(A + B')(A + C)(A + D)", "(A + B')(A + CD)", "(A + B')(C + D)", "A(B' + C + D)",
                   "A + B' + C + D", "(A + B)(A + C)(A + D)"]),
     ("AB + C'D", ["(A + C')(A + D)(B + C')(B + D)", "(AB + C')(AB + D)", "(A + C')(B + D)", "(A + B)(C' + D)",
                   "(A + C')(A + D)(B + C')", "(A' + C)(B + D)"]),
     ("(A + B)(C + D)", ["AC + AD + BC + BD", "A(C + D) + B(C + D)", "AB + CD", "AC + BD", "A + B + C + D",
                         "AC + AD + BC"]),
     ("A + B(C' + D)", ["A + BC' + BD", "(A + B)(A + C' + D)", "(A + B)(C' + D)", "AB + C' + D", "A + BC'D",
                        "(A + B)(A + C)(A + D)"])],
    ABCD, 6, 40,
    ["Multiply out (to SOP) or factor (to POS) the expression below. LEDR5..LEDR0 are six answers."],
    ["SWi = 1 if LEDRi is RIGHT (equal to Y in all 16 rows), SW5..SW0."],
    ["Inputs: A = SW3, B = SW2, C = SW1, D = SW0 (HEX3..HEX0). LEDR5..LEDR0 = the six answers."]))

# ---- Q16, Q17: priority circuit, active-low inputs (slides 80-82)
v16, seen = [], set()
while len(v16) < 256:
    order, pol = rng.sample(range(4), 4), rng.randint(0, 15)
    if (tuple(order), pol) not in seen:
        seen.add((tuple(order), pol)); v16.append((order, pol))
def prio_tables(p):
    order, pol = p
    out = [[0] * 16 for _ in range(4)]
    for r in range(16):
        act = [((r >> i) & 1) ^ ((pol >> i) & 1) for i in range(4)]		# A_i = SW i
        for i in order:
            if act[i]:
                out[i][r] = 1
                break
    return out
B_PRIO = ["Inputs: A3 = SW3, A2 = SW2, A1 = SW1, A0 = SW0 (HEX3..HEX0). Outputs: Yi = LEDRi.",
          "Like the lecture's priority circuit: Yi = 1 when Ai is active and no input of higher priority is."]
QS.append(Q(id="Q16", name="PRIORITY", title="Priority circuit: the order", inputs=IN4,
    outs=[("R", i) for i in range(4)], hexes=HX4, variants=v16, tables=prio_tables,
    answer=lambda p: (sum(p[0][t] << (2 * t) for t in range(4)), 0xFF),
    describe=lambda p: f"order (high->low) A{p[0][0]} A{p[0][1]} A{p[0][2]} A{p[0][3]}, active-low mask {p[1]:04b}",
    B=B_PRIO,
    L=["The priority order is hidden (it is not A3 > A2 > A1 > A0). Some inputs may be active LOW",
       "(active when the switch is DOWN). Find the order, from the highest priority to the lowest."],
    F=["SW1 SW0 = number (0-3) of the HIGHEST input,  SW3 SW2 = the second,",
       "SW5 SW4 = the third,  SW7 SW6 = the LOWEST."]))
QS.append(Q(id="Q17", name="ACTIVELOW", title="Priority circuit: active-low inputs", inputs=IN4,
    outs=[("R", i) for i in range(4)], hexes=HX4, variants=v16, tables=prio_tables,
    answer=lambda p: (p[1], 0xF), describe=lambda p: f"active-low mask {p[1]:04b}, order {p[0]}",
    B=B_PRIO,
    L=["Some inputs are active LOW: they count as active when the switch is DOWN (0) - like KEY0..KEY3",
       "on the board. With all switches down, something already lights. Find the active-low inputs."],
    F=["SWi = 1 if Ai is active low, 0 if active high (SW3..SW0)."]))

# ---- Q18, Q19: two-level NAND / NOR (slides 83-87)
def gate2(t, l1, l2, r):
    x = [bits(r, 3)[l // 2] ^ (l & 1) for l in (l1, l2)]
    return 1 - (x[0] & x[1]) if t else 1 - (x[0] | x[1])		# t = 1 NAND, 0 NOR
def nn_tables(p):
    g, ty = p
    n = [[gate2(t, a, b, r) for r in range(8)] for t, a, b in g]
    y = [1 - (n[0][r] & n[1][r] & n[2][r]) if ty else 1 - (n[0][r] | n[1][r] | n[2][r]) for r in range(8)]
    return n + [y]
def rand_nn():
    while True:
        g = []
        for _ in range(3):
            v1, v2 = rng.sample(range(3), 2)
            g.append((rng.randint(0, 1), 2 * v1 + rng.randint(0, 1), 2 * v2 + rng.randint(0, 1)))
        p = (g, rng.randint(0, 1))
        n = nn_tables(p)
        if any(len({n[0][r], n[1][r], n[2][r]}) > 1 for r in range(8)) and len({tuple(x) for x in n[:3]}) == 3:
            return p
LITNAME = ["A", "A'", "B", "B'", "C", "C'"]
desc_nn = lambda p: "; ".join(f"n{i + 1} = {'NAND' if t else 'NOR'}({LITNAME[a]}, {LITNAME[b]})" for i, (t, a, b) in enumerate(p[0])) + \
    f"; Y = {'NAND' if p[1] else 'NOR'}(n1, n2, n3)"
B_NN = ["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0).",
        "First level: n1 = LEDR3, n2 = LEDR2, n3 = LEDR1 - each a 2-input NAND or NOR of literals (A, A', B, ...).",
        "Second level: Y = LEDR0 = a 3-input NAND or NOR of n1, n2, n3."]
v18 = [rand_nn() for _ in range(256)]
QS.append(Q(id="Q18", name="NANDNOR", title="Two-level logic: NAND or NOR?", inputs=IN3,
    outs=[("R", 3), ("R", 2), ("R", 1), ("R", 0)], hexes=HX3, variants=v18, tables=nn_tables,
    answer=lambda p: ((p[0][0][0] << 3) | (p[0][1][0] << 2) | (p[0][2][0] << 1) | p[1], 0xF),
    describe=desc_nn, B=B_NN,
    L=["Find the type of every gate. A NAND of literals is a sum (x' + y'); a NOR is a product (x'y').",
       "For Y, look at what it does when n1, n2, n3 are not all equal."],
    F=["SW3 = n1, SW2 = n2, SW1 = n3, SW0 = Y:  1 = NAND, 0 = NOR."]))
v19 = [(k, rand_nn()) for k in range(3) for _ in range(85)]
QS.append(Q(id="Q19", name="NODE", title="Two-level logic: the inputs of one gate", inputs=IN3,
    outs=[("R", 3), ("R", 2), ("R", 1), ("R", 0)], hexes=HX3, variants=v19, npub=3, nsec=85,
    tables=lambda p: nn_tables(p[1]),
    answer=lambda p: ((1 << (5 - p[1][0][p[0]][1])) | (1 << (5 - p[1][0][p[0]][2])), 0x3F),
    describe=lambda p: f"node n{p[0] + 1}: " + desc_nn(p[1]), B=B_NN,
    L=["Find which two literals go into your gate (and so whether it is a NAND or a NOR)."],
    P={k: [f"Your gate: n{k + 1} (LEDR{3 - k})."] for k in range(3)},
    F=["Two switches up: SW5 = A, SW4 = A', SW3 = B, SW2 = B', SW1 = C, SW0 = C'."]))

# ---- Q20: multilevel - find the gates (slides 79, 94-97)
GN = ["AND", "OR", "NAND", "NOR"]
def g2(t, a, b):
    return [a & b, a | b, 1 - (a & b), 1 - (a | b)][t]
def ml_tables(p):
    out = [[], [], []]
    for r in range(16):
        A, B, C, D = bits(r, 4)
        n1 = g2(p[0], A, B); n2 = g2(p[1], n1, C); y = g2(p[2], n2, D)
        out[0].append(n1); out[1].append(n2); out[2].append(y)
    return out
QS.append(Q(id="Q20", name="GATES", title="A multilevel circuit: find the gates", inputs=IN4,
    outs=[("R", 2), ("R", 1), ("R", 0)], hexes=HX4, variants=[list(t) for t in itertools.product(range(4), repeat=3)],
    tables=ml_tables, answer=lambda p: ((p[0] << 4) | (p[1] << 2) | p[2], 0x3F),
    describe=lambda p: f"n1 = {GN[p[0]]}(A, B); n2 = {GN[p[1]]}(n1, C); Y = {GN[p[2]]}(n2, D)",
    B=["Inputs: A = SW3, B = SW2, C = SW1, D = SW0 (HEX3..HEX0).",
       "The circuit: n1 = G1(A, B) on LEDR2,  n2 = G2(n1, C) on LEDR1,  Y = G3(n2, D) on LEDR0."],
    L=["Each gate G1, G2, G3 is an AND, OR, NAND or NOR (2 inputs). Find all three."],
    F=["Codes: 0 = AND, 1 = OR, 2 = NAND, 3 = NOR.  SW5 SW4 = G1,  SW3 SW2 = G2,  SW1 SW0 = G3."]))

# ---- Q21: bubble pushing - which circuit is on the board? (slides 88-97)
def rand_circuit():
    v1 = rng.sample(range(4), 2); v2 = rng.sample(range(4), 2)
    return ([(v, rng.randint(0, 1)) for v in v1], [(v, rng.randint(0, 1)) for v in v2],
            rng.randint(2, 3), rng.randint(2, 3), rng.randint(0, 3), rng.randint(0, 1), rng.randint(0, 1))
def circ_tt(c):
    l1, l2, t1, t2, t3, b1, b2 = c
    out = []
    for r in range(16):
        x = bits(r, 4)
        n1 = g2(t1, *[x[v] ^ p for v, p in l1]); n2 = g2(t2, *[x[v] ^ p for v, p in l2])
        out.append(g2(t3, n1 ^ b1, n2 ^ b2))
    return out
def circ_txt(c):
    l1, l2, t1, t2, t3, b1, b2 = c
    lit = lambda vp: ABCD[vp[0]] + ("'" if vp[1] else "")
    return (f"n1 = {GN[t1]}({lit(l1[0])}, {lit(l1[1])});  n2 = {GN[t2]}({lit(l2[0])}, {lit(l2[1])});  "
            f"Y = {GN[t3]}(n1{chr(39) if b1 else ''}, n2{chr(39) if b2 else ''})")
SETS21 = []
for _ in range(8):
    cs, tts = [], []
    while len(cs) < 8:
        c = rand_circuit(); t = circ_tt(c)
        if t not in tts and 3 <= sum(t) <= 13:
            cs.append(c); tts.append(t)
    SETS21.append((cs, tts))
QS.append(Q(id="Q21", name="BUBBLES", title="Bubble pushing: which circuit is in the board?", inputs=IN4,
    outs=[("R", 0)], hexes=HX4, variants=[(i, k) for i in range(8) for k in range(8)], npub=8, nsec=8,
    tables=lambda p: [SETS21[p[0]][1][p[1]]], answer=lambda p: (p[1], 0x7),
    describe=lambda p: f"circuit {p[1]}: " + circ_txt(SETS21[p[0]][0][p[1]]),
    B=["Inputs: A = SW3, B = SW2, C = SW1, D = SW0 (HEX3..HEX0). Y = LEDR0."],
    L=["The board holds ONE of the eight circuits below (n1' = a bubble on that input of the last gate).",
       "Push the bubbles, write each Y as an SOP, and find the one in the board."],
    P={i: [f"  {k}: {circ_txt(c)}" for k, c in enumerate(cs)] for i, (cs, _) in enumerate(SETS21)},
    F=["SW2 SW1 SW0 = the number of the circuit (0-7)."]))

# ---- Q22, Q23: the multiplexer as a lookup table (slides 98-102)
DN = ["0", "1", "C", "C'"]
def mux_tt(d):
    return [[0, 1, r & 1, 1 - (r & 1)][d[3 - (r >> 1)]] for r in range(8)]		# d = (D3, D2, D1, D0)
QS.append(Q(id="Q22", name="MUXDATA", title="A 4:1 mux: what is on its data inputs?", inputs=IN3,
    outs=[("R", 0)], hexes=HX3, variants=[list(t) for t in itertools.product(range(4), repeat=4)],
    tables=lambda p: [mux_tt(p)], answer=lambda p: ((p[0] << 6) | (p[1] << 4) | (p[2] << 2) | p[3], 0xFF),
    describe=lambda p: "D3 D2 D1 D0 = " + " ".join(DN[x] for x in p),
    B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). Y = LEDR0.",
       "A 4:1 mux: S1 = A, S0 = B select D0..D3 (AB = 00 -> D0 ... 11 -> D3). Each Di is 0, 1, C or C'."],
    L=["Find what is wired to every data input."],
    F=["Codes: 0 = '0', 1 = '1', 2 = C, 3 = C'.  SW7 SW6 = D3,  SW5 SW4 = D2,  SW3 SW2 = D1,  SW1 SW0 = D0."]))
SEL23 = [(0, 1, 2), (0, 2, 1), (1, 2, 0)]		# (S1, S0, the data variable X)
def mux23(p):
    (s1, s0, x), tt = SEL23[p[0]], p[1]
    codes = []
    for sel in (3, 2, 1, 0):
        vals = []
        for xv in (0, 1):
            r = sum(b << (2 - v) for v, b in ((s1, sel >> 1), (s0, sel & 1), (x, xv)))
            vals.append(tt[r])
        codes.append({(0, 0): 0, (1, 1): 1, (0, 1): 2, (1, 0): 3}[tuple(vals)])
    return codes		# D3, D2, D1, D0
v23 = []
for k in range(3):
    pool = [tt for tt in ([(t >> r) & 1 for r in range(8)] for t in range(256)) if 2 <= sum(tt) <= 6]
    v23 += [(k, tt) for tt in rng.sample(pool, 85)]
QS.append(Q(id="Q23", name="MUXLOGIC", title="Logic using a mux: build F with your select lines", inputs=IN3,
    outs=[("R", 0)], hexes=HX3, variants=v23, npub=3, nsec=85,
    tables=lambda p: [p[1]], answer=lambda p: (sum(c << (6 - 2 * i) for i, c in enumerate(mux23(p))), 0xFF),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p[1])) + ", D3..D0 = " + " ".join(
        ["0", "1", ABC[SEL23[p[0]][2]], ABC[SEL23[p[0]][2]] + "'"][c] for c in mux23(p)),
    B=["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0). F = LEDR0 (hidden)."],
    L=["Find F, then build it from ONE 4:1 mux: your select lines are given below, and every data",
       "input D0..D3 is 0, 1, X or X' (X = the variable that is not a select line)."],
    P={k: [f"Your mux: S1 = {ABC[s1]}, S0 = {ABC[s0]}, X = {ABC[x]}  ({ABC[s1]}{ABC[s0]} = 00 -> D0 ... 11 -> D3)."]
       for k, (s1, s0, x) in enumerate(SEL23)},
    F=["Codes: 0 = '0', 1 = '1', 2 = X, 3 = X'.  SW7 SW6 = D3,  SW5 SW4 = D2,  SW3 SW2 = D1,  SW1 SW0 = D0."]))

# ---- Q24, Q25: the decoder (slides 103-106)
ROWS24 = [(5, 2), (0, 7), (3, 6), (1, 4), (6, 1), (2, 5), (7, 0), (4, 3)]
def dec_tables(perm):
    return [[0 if perm[r] == j else 1 for r in range(8)] for j in range(8)]
B_DEC = ["Inputs: A = SW2, B = SW1, C = SW0 (HEX2 HEX1 HEX0).",
         "A 3:8 decoder with ACTIVE-LOW outputs on LEDR7..LEDR0 - wired in a hidden order."]
QS.append(Q(id="Q24", name="DECODER", title="A 3:8 decoder: which LED is which output?", inputs=IN3,
    outs=[("R", j) for j in range(8)], hexes=HX3,
    variants=[(r1, r2, perm) for r1, r2 in ROWS24 for perm in perms_sample(rng, range(8), 32)], npub=8, nsec=32,
    tables=lambda p: dec_tables(p[2]), answer=lambda p: (p[2][p[0]] | (p[2][p[1]] << 3), 0x3F),
    describe=lambda p: "row -> LED: " + " ".join(f"{r}->{p[2][r]}" for r in range(8)),
    B=B_DEC,
    L=["One-hot, active low: for each input row exactly one LED is OFF. Find the LEDs of your two rows."],
    P={i: [f"Your rows: minterm {r1} (A B C = {r1:03b}) and minterm {r2} (A B C = {r2:03b})."] for i, (r1, r2) in enumerate(ROWS24)},
    F=["SW2 SW1 SW0 = the LED number (0-7) of your FIRST minterm,  SW5 SW4 SW3 = the LED number of the SECOND."]))
v25 = []
for _ in range(256):
    v25.append((rng.sample(range(8), 8), sorted(rng.sample(range(8), rng.randint(2, 5)))))
QS.append(Q(id="Q25", name="DECOR", title="Logic using a decoder: which outputs go into the gate?", inputs=IN3,
    outs=[("R", j) for j in range(8)] + [("G", 0)], hexes=HX3, variants=v25,
    tables=lambda p: dec_tables(p[0]) + [[1 if r in p[1] else 0 for r in range(8)]],
    answer=lambda p: (sum(1 << p[0][r] for r in p[1]), 0xFF),
    describe=lambda p: f"Y = SIGMA{tuple(p[1])}, row -> LED: " + " ".join(f"{r}->{p[0][r]}" for r in range(8)),
    B=B_DEC + ["Y = LEDG0 = a gate fed by some of the decoder outputs (OR of minterms, with active-low outputs)."],
    L=["Find which decoder outputs (LEDs) are wired into the gate that makes Y."],
    F=["SWi = 1 if the output on LEDRi goes into the gate (SW7..SW0)."]))

# ---- NEW ORDER (easy -> hard, in steps). The first-format questions above keep old ids o01..o25 (C:/DE10/week3/class_exercise/old);
# each one gets a new Qnn when it is converted to steps.
for q in QS:
    q.id = "o" + q.id[1:]
    q.flat = False
GATES = [("AND", [0, 0, 0, 1]), ("OR", [0, 1, 1, 1]), ("XOR", [0, 1, 1, 0]),
         ("NAND", [1, 1, 1, 0]), ("NOR", [1, 0, 0, 0]), ("XNOR", [1, 0, 0, 1])]
NEW = []
QBY_O01_VARIANTS = [q for q in QS if q.id == "o01"][0].variants		# Q20 shares it (redrawn in place below)
NEW.append(Q(id="Q01", name="GATE", title="Which gate is hidden in the board?", inputs=[9, 8], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=list(range(6)),
    tables=lambda p: [GATES[p][1]], answer=lambda p: (p, 0x7),
    describe=lambda p: f"gate {GATES[p][0]}",
    B=["A = SW9, B = SW8 (HEX3, HEX2).  Y = LEDG0 (green).  Your answer goes on SW3..SW0."], L=[], F=[]))
# Q02: a hidden F of three inputs - its truth table in two halves, then minterms (SIGMA) and maxterms (PI)
V02 = [[1 if r in ones else 0 for r in range(8)] for k in (3, 4, 5) for ones in itertools.combinations(range(8), k)]
NEW.append(Q(id="Q02", name="SIGMA", title="Minterms and maxterms of a hidden F", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=V02,
    tables=lambda p: [p], answer=lambda p: (8 - sum(p), 0xF),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p)),
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  F = LEDG0 (green).  Your answer goes on SW3..SW0."], L=[], F=[]))
# Q03: four green lights, each one term of A B C: one minterm, one maxterm, two others (a 2-literal product,
# a 2-literal sum or one literal - on in 2, off in 2, on in 4 rows, so only the minterm is on in exactly one row
# and only the maxterm is off in exactly one row). Own RNG, so nothing else changes.
_r03 = random.Random(103)
def term03(kind):
    vs = sorted(_r03.sample(range(3), {"min": 3, "max": 3, "p2": 2, "s2": 2, "lit": 1}[kind]))
    pol = [_r03.randint(0, 1) for _ in vs]
    lit = lambda r, i: bits(r, 3)[vs[i]] ^ pol[i]
    if kind in ("min", "p2", "lit"):
        return (kind, [int(all(lit(r, i) for i in range(len(vs)))) for r in range(8)])
    return (kind, [int(any(lit(r, i) for i in range(len(vs)))) for r in range(8)])
V03 = []
while len(V03) < 256:
    kinds = ["min", "max", _r03.choice(["p2", "s2", "lit"]), _r03.choice(["p2", "s2", "lit"])]
    _r03.shuffle(kinds)
    v = [term03(k) for k in kinds]
    if v not in V03:
        V03.append(v)
NEW.append(Q(id="Q03", name="TERMS", title="Which light is a minterm, which a maxterm?", inputs=[9, 8, 7], flat=True,
    outs=[("G", j) for j in range(4)], hexes=[[9], [8], [7], None], variants=V03,
    tables=lambda p: [t for _, t in p], answer=lambda p: (1 << [k for k, _ in p].index("max"), 0xF),
    describe=lambda p: ", ".join(f"LEDG{j} {k} {''.join(map(str, t))}" for j, (k, t) in enumerate(p)),
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  4 terms = LEDG3..LEDG0 (green).  Your answer goes on SW3..SW0."],
    L=[], F=[]))
# Q04: F of A B C that depends on exactly two of them - one input never matters (slides 20-21: E = HS + H).
# u = the unused input (0 = A, 1 = B, 2 = C), f = a 2-input function of the other two that needs both.
F2 = [t for t in ([(n >> r) & 1 for r in range(4)] for n in range(16))
      if any(t[r] != t[r ^ 2] for r in range(4)) and any(t[r] != t[r ^ 1] for r in range(4))]
def f04(p):
    u, f = p
    x, y = [i for i in range(3) if i != u]
    return [f[(bits(r, 3)[x] << 1) | bits(r, 3)[y]] for r in range(8)]
def matters04(p, i):
    t, m = f04(p), 1 << (2 - i)
    return int(any(t[r] != t[r ^ m] for r in range(8)))
V04 = [(u, f) for u in range(3) for f in F2]
NEW.append(Q(id="Q04", name="MATTER", title="Which input does not matter?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=V04,
    tables=lambda p: [f04(p)], answer=lambda p: (1 << (2 - p[0]), 0x7),
    describe=lambda p: f"unused {ABC[p[0]]}, F rows 000..111 = " + "".join(map(str, f04(p))),
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  F = LEDG0 (green).  Your answer goes on SW3..SW0."],
    L=[], F=[]))
# Q05: a hidden 4:1 mux - S1 S0 = SW9 SW8 pick D0..D3, each D is '0', '1', C or C' (C = SW7). p = (D3, D2, D1, D0).
NEW.append(Q(id="Q05", name="MUX", title="What is wired into the multiplexer?", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=[list(t) for t in itertools.product(range(4), repeat=4)],
    tables=lambda p: [mux_tt(p)], answer=lambda p: (p[0], 0x3),
    describe=lambda p: "D3 D2 D1 D0 = " + " ".join(DN[x] for x in p),
    B=["Select S1 = SW9, S0 = SW8.  Input C = SW7.  (HEX3 HEX2 HEX1)   Y = LEDG0 (green).   Your answer goes on SW3..SW0.",
       "A 4:1 mux: S1 S0 = 00 sends D0 to Y,  01 sends D1,  10 sends D2,  11 sends D3."],
    L=[], F=[]))
# Q06: a hidden 2:4 decoder - A B = SW9 SW8, the 4 outputs on LEDG3..LEDG0 in a hidden order (perm[row] = the LED).
# The last step: logic using a decoder - which two outputs go into the OR for F = SIGMA(m1, m2) (printed, by pub).
PAIRS06 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
_r06 = random.Random(106)
V06 = [(pr, perm) for pr in PAIRS06 for perm in _r06.sample([list(t) for t in itertools.permutations(range(4))], 24)]
NEW.append(Q(id="Q06", name="DECODER", title="A decoder: which light is which output?", inputs=[9, 8], flat=True,
    outs=[("G", j) for j in range(4)], hexes=[[9], [8], None, None], variants=V06, npub=6, nsec=24,
    tables=lambda p: [[1 if p[1][r] == j else 0 for r in range(4)] for j in range(4)],
    answer=lambda p: ((1 << p[1][p[0][0]]) | (1 << p[1][p[0][1]]), 0xF),
    describe=lambda p: f"F = SIGMA{p[0]}, row -> LED: " + " ".join(f"{r:02b}->LEDG{p[1][r]}" for r in range(4)),
    B=["A = SW9, B = SW8 (HEX3 HEX2).  The decoder's 4 outputs = LEDG3..LEDG0 - in a hidden order.  Answer on SW3..SW0."],
    P={i: [f"Your function for the last step:  F = SIGMA({a}, {b})  - F = 1 when A B = {a:02b} or {b:02b}."]
       for i, (a, b) in enumerate(PAIRS06)},
    L=[], F=[]))
# Q07: a priority circuit, active high, 4 inputs A3..A0 = SW9..SW6, outputs Yi = LEDGi, hidden order (24 variants).
NEW.append(Q(id="Q07", name="PRIORITY", title="A priority circuit: who wins?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", i) for i in range(4)], hexes=[[9], [8], [7], [6]], variants=[(list(o), 0) for o in itertools.permutations(range(4))],
    tables=prio_tables, answer=lambda p: (1 << p[0][3], 0xF),
    describe=lambda p: "order high -> low: " + " ".join(f"A{i}" for i in p[0]),
    B=["Inputs A3 = SW9, A2 = SW8, A1 = SW7, A0 = SW6 (HEX3..HEX0).  Outputs Y3..Y0 = LEDG3..LEDG0.  Answer on SW3..SW0.",
       "Yi = 1 when Ai is up and no STRONGER input is up. The order of strength is hidden."],
    L=[], F=[]))

# Q08: perfect induction over A B - 4 statements LEFT = RIGHT in a hidden order; pair k = SW9 SW8, A B = SW7 SW6.
THM08 = [("A + AB", "A", "covering"), ("A + A'B", "A + B", "simplification"),
         ("(AB)'", "A' + B'", "De Morgan"), ("(A + B)'", "A' + B'", "a false 'De Morgan'")]
TT08 = [(table_of(l, ["A", "B"]), table_of(r, ["A", "B"])) for l, r, _ in THM08]
assert len({(tuple(a), tuple(b)) for a, b in TT08}) == 4
def tables08(p):
    perm = p[1]
    return [[TT08[perm[r >> 2]][side][r & 3] for r in range(16)] for side in (0, 1)]
V08 = [(x, list(perm)) for x in range(4) for perm in itertools.permutations(range(4))]
NEW.append(Q(id="Q08", name="THEOREMS", title="Perfect induction: which statements are true?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9, 8], None, [7], [6]], variants=V08, npub=4, nsec=24,
    tables=tables08, answer=lambda p: (p[1].index(p[0]), 0x3),
    describe=lambda p: "pairs k0..k3 = " + ", ".join(f"{THM08[i][0]} = {THM08[i][1]}" for i in p[1]),
    B=["Statement number = SW9 SW8 (HEX3).  A = SW7, B = SW6 (HEX1 HEX0).  LEFT = LEDG1, RIGHT = LEDG0.  Answer on SW3..SW0.",
       "The board holds 4 statements LEFT = RIGHT, in a hidden order:   " + "     ".join(f"{l} = {r}" for l, r, _ in THM08)],
    P={i: [f"Your statement for the last step:  {THM08[i][0]} = {THM08[i][1]}"] for i in range(4)},
    L=[], F=[]))

# Q09: from a story to an equation - 4 students' circuits on LEDG3..0, one is right (6 stories x 24 orders).
STORIES09 = [
    ("You go to the Park (P) if it is NOT Raining (R) and you have Sandwiches (S) or Drinks (D).", "RSD",
     "R'(S + D)", ["R'S + D", "R'SD", "R + S + D"]),
    ("The alarm (Y) rings when the Door (D) is open and the system is Armed (A), or when there is Smoke (S).", "DAS",
     "DA + S", ["D(A + S)", "DAS", "D + A + S"]),
    ("The light (L) is on when it is Dark (D) and someone Moves (M) - but never when the Battery (B) is low.", "DMB",
     "DMB'", ["DM + B'", "DMB", "(D + M)B'"]),
    ("You Enter (E) with a Hat (H) and Shoes (S), or with a Hat and no Shoes (S').", "HSX",
     "HS + HS'", ["HS", "H + S", "S"]),
    ("The fan (F) runs when it is Hot (H) and the window is not Open (O), or when a Kid (K) presses the button.", "HOK",
     "HO' + K", ["HO'K", "H(O' + K)", "H + O' + K"]),
    ("You Win (W) if you get a Million (M) or a Notepad (N) - but only if you Play (P).", "MNP",
     "(M + N)P", ["M + NP", "MNP", "M + N + P"]),
]
V09 = []
for st in STORIES09:
    names = list(st[1])
    cands = [table_of(e, names) for e in [st[2]] + st[3]]
    assert len({tuple(c) for c in cands}) == 4, st[2]
    V09 += [(st, list(perm), cands) for perm in itertools.permutations(range(4))]
def letters09(st):
    return [c for c in st[1] if c != "X"]
NEW.append(Q(id="Q09", name="STORY", title="From a story to an equation", inputs=[9, 8, 7], flat=True,
    outs=[("G", j) for j in range(4)], hexes=[[9], [8], [7], None], variants=V09, npub=6, nsec=24,
    tables=lambda p: [p[2][p[1][j]] for j in range(4)], answer=lambda p: (1 << p[1].index(0), 0xF),
    describe=lambda p: "; ".join(f"LEDG{j} = {([p[0][2]] + p[0][3])[p[1][j]]}" for j in range(4)),
    B=["Your three letters are on SW9 SW8 SW7, in the order shown below (HEX3 HEX2 HEX1).  4 students' circuits = LEDG3..LEDG0.",
       "Answer on SW3..SW0."],
    P={i: [st[0], "Letters:  " + ",  ".join(f"{c} = SW{9 - k}" for k, c in enumerate(st[1]) if c != "X")
           + ("   (SW7 is not used)" if "X" in st[1] else "")] for i, st in enumerate(STORIES09)},
    L=[], F=[]))

# Q10: De Morgan - a printed expression with an outer bar, 4 answers on LEDG3..0, one is right (6 x 24).
DM10 = [("((A + B')C)'", ["A'B + C'", "A'B' + C'", "A'BC'", "(A' + B)C'"]),
        ("(A'B + C)'", ["(A + B')C'", "(A' + B)C'", "AB'C'", "A + B' + C'"]),
        ("(AB + C)'", ["(A' + B')C'", "A'B'C'", "(A' + B')C", "A' + B'C'"]),
        ("((A + B)C')'", ["A'B' + C", "A'B' + C'", "A' + B' + C", "(A' + B')C"]),
        ("(A + B + C)'", ["A'B'C'", "A' + B' + C'", "A'B'C", "A'B' + C'"]),
        ("(A(B + C'))'", ["A' + B'C", "A' + B'C'", "A'(B' + C)", "A' + B + C'"])]
V10 = []
for e, cands in DM10:
    ref = table_of(e, ABC)
    tts = [table_of(c, ABC) for c in cands]
    assert tts[0] == ref and all(t != ref for t in tts[1:]) and len({tuple(t) for t in tts}) == 4, e
    V10 += [(e, list(perm), tts) for perm in itertools.permutations(range(4))]
NEW.append(Q(id="Q10", name="DEMORGAN", title="De Morgan: which answer is right?", inputs=[9, 8, 7], flat=True,
    outs=[("G", j) for j in range(4)], hexes=[[9], [8], [7], None], variants=V10, npub=6, nsec=24,
    tables=lambda p: [p[2][p[1][j]] for j in range(4)], answer=lambda p: (1 << p[1].index(0), 0xF),
    describe=lambda p: "; ".join(f"LEDG{j} = {[c for e, c in DM10 if e == p[0]][0][p[1][j]]}" for j in range(4)),
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  4 students' answers = LEDG3..LEDG0.  Answer on SW3..SW0."],
    P={i: [f"Your expression:   Y = {e}"] for i, (e, _) in enumerate(DM10)},
    L=[], F=[]))
# Q11 / Q12: a printed expression (by pub), 4 students' results on LEDG3..0 - 2 right, 2 wrong (6 x 24).
def cand4(qid, name, title, sets, want_wrong, intro):
    v = []
    for e, cands in sets:
        ref = table_of(e, ABC)
        tts = [table_of(c, ABC) for c in cands]
        good = [t == ref for t in tts]
        assert good.count(True) == 2 and len({tuple(t) for t in tts}) >= 3, (e, good)
        v += [(e, list(perm), tts, good, cands) for perm in itertools.permutations(range(4))]
    return Q(id=qid, name=name, title=title, inputs=[9, 8, 7], flat=True,
        outs=[("G", j) for j in range(4)], hexes=[[9], [8], [7], None], variants=v, npub=len(sets), nsec=24,
        tables=lambda p: [p[2][p[1][j]] for j in range(4)],
        answer=lambda p: (sum(1 << j for j in range(4) if p[3][p[1][j]] != want_wrong), 0xF),
        describe=lambda p: "; ".join(f"LEDG{j} = {p[4][p[1][j]]}{'' if p[3][p[1][j]] else ' (wrong)'}" for j in range(4)),
        B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  4 students' results = LEDG3..LEDG0.  Answer on SW3..SW0."],
        P={i: [f"{intro}   Y = {e}"] for i, (e, _) in enumerate(sets)}, L=[], F=[])
NEW.append(cand4("Q11", "ERRORS", "Common errors: which simplifications are wrong?",
    [("A'BC + A'", ["A'", "A'B + A'", "A'BC", "A' + BC"]),
     ("AB + AB'", ["A", "A(B + B')", "B", "AB'"]),
     ("(A + BC)'", ["A'(B' + C')", "A'B' + A'C'", "A' + B'C'", "A'BC"]),
     ("(A + B)(A + C)", ["A + BC", "AA + AC + AB + BC", "AB + AC", "(A + B)C"]),
     ("AB + A'C + BC", ["AB + A'C", "AB + A'C + ABC", "AB + BC", "A'C + BC"]),
     ("A + A'B", ["A + B", "A + B + AB", "AB", "A'B"])],
    True, "Four students simplified your expression:"))
NEW.append(cand4("Q12", "MULTIPLY", "Multiplying out and factoring: which answers are right?",
    [("(A + B')(A + C)", ["A + B'C", "AA + AC + AB' + B'C", "AB' + AC", "A + B' + C"]),
     ("A(B + C')", ["AB + AC'", "A(C' + B)", "AB + A + C'", "(A + B)(A + C')"]),
     ("A + BC", ["(A + B)(A + C)", "(A + C)(A + B)", "(A + B)C", "A(B + C)"]),
     ("A + B'C'", ["(A + B')(A + C')", "(A + C')(A + B')", "(A + B')C'", "(A' + B')(A' + C')"]),
     ("(A' + B)(C + B)", ["A'C + B", "A'C + A'B + BC + B", "A'B + C", "A'C + B'"]),
     ("AB + C", ["(A + C)(B + C)", "(C + A)(C + B)", "(A + B)C", "A(B + C)"])],
    False, "Four students multiplied out (SOP) or factored (POS) your expression:"))

# Q13: minimal SOP of a hidden F (3 inputs) - only functions whose minimal SOP has at most 7 literals.
V13 = [tt for tt in ([(t >> r) & 1 for r in range(8)] for t in range(256))
       if 2 <= sum(tt) <= 5 and min_sop(tt, 3) != (1, 1) and min_sop(tt, 3)[1] <= 7]
NEW.append(Q(id="Q13", name="MINSOP", title="The minimal sum of products", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=V13,
    tables=lambda p: [p], answer=lambda p: (min_sop(p, 3)[1], 0xF),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p)) + f", min SOP (terms, literals) = {min_sop(p, 3)}",
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  F = LEDG0 (green).  Answer on SW3..SW0."], L=[], F=[]))

# Q14: two-level NAND-NAND or NOR-NOR: n1 = LEDG2, n2 = LEDG1 (2-input gates of literals), Y = LEDG0 = the same gate of n1, n2.
_r14 = random.Random(114)
def nn14_tables(p):
    t, g = p			# t = 1 NAND, 0 NOR;  g = [(l1, l2), (l3, l4)] literal codes 0 A 1 A' 2 B 3 B' 4 C 5 C'
    n = [[gate2(t, a, b, r) for r in range(8)] for a, b in g]
    y = [1 - (n[0][r] & n[1][r]) if t else 1 - (n[0][r] | n[1][r]) for r in range(8)]
    return n + [y]
V14 = []
while len(V14) < 256:
    t = _r14.randint(0, 1)
    g = []
    for _ in range(2):
        v1, v2 = sorted(_r14.sample(range(3), 2))
        g.append((2 * v1 + _r14.randint(0, 1), 2 * v2 + _r14.randint(0, 1)))
    p = (t, g)
    nt = nn14_tables(p)
    if nt[0] != nt[1] and len(set(nt[2])) == 2 and p not in V14:
        V14.append(p)
NEW.append(Q(id="Q14", name="NANDNOR", title="Two-level logic: NAND-NAND or NOR-NOR", inputs=[9, 8, 7], flat=True,
    outs=[("G", 2), ("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=V14,
    tables=nn14_tables, answer=lambda p: ((1 << (5 - p[1][0][0])) | (1 << (5 - p[1][0][1])), 0x3F),
    describe=lambda p: f"{'NAND' if p[0] else 'NOR'}-{'NAND' if p[0] else 'NOR'}: n1 = ({LITNAME[p[1][0][0]]}, {LITNAME[p[1][0][1]]}), "
                       f"n2 = ({LITNAME[p[1][1][0]]}, {LITNAME[p[1][1][1]]})",
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  n1 = LEDG2, n2 = LEDG1 (first level), Y = LEDG0 (second level).",
       "All three gates are NAND, or all three are NOR. Each first-level gate has 2 inputs: letters or their NOTs (A, A', B, ...)."],
    L=[], F=[]))

# Q15: multilevel - n1 = G1(A, B) on LEDG2, n2 = G2(n1, C) on LEDG1, Y = G3(n2, D) on LEDG0; A B C D = SW9..SW6.
NEW.append(Q(id="Q15", name="GATES", title="A multilevel circuit: find the gates", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 2), ("G", 1), ("G", 0)], hexes=[[9], [8], [7], [6]], variants=[list(t) for t in itertools.product(range(4), repeat=3)],
    tables=ml_tables, answer=lambda p: (p[2], 0x3),
    describe=lambda p: f"n1 = {GN[p[0]]}(A, B); n2 = {GN[p[1]]}(n1, C); Y = {GN[p[2]]}(n2, D)",
    B=["A = SW9, B = SW8, C = SW7, D = SW6 (HEX3..HEX0).  Answer on SW1 SW0.",
       "The circuit:  n1 = G1(A, B) on LEDG2   ->   n2 = G2(n1, C) on LEDG1   ->   Y = G3(n2, D) on LEDG0."],
    L=[], F=[]))
# Q16: logic using a mux - a hidden F, built from a 4:1 mux with personal select lines (SEL23, mux23: D3..D0 codes).
_r16 = random.Random(116)
_pool16 = [tt for tt in ([(t >> r) & 1 for r in range(8)] for t in range(256)) if 2 <= sum(tt) <= 6]
V16 = [(k, tt) for k in range(3) for tt in _r16.sample(_pool16, 85)]
NEW.append(Q(id="Q16", name="MUXLOGIC", title="Build F from a multiplexer", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=V16, npub=3, nsec=85,
    tables=lambda p: [p[1]], answer=lambda p: (mux23(p)[0], 0x3),
    describe=lambda p: "F rows 000..111 = " + "".join(map(str, p[1])) + ", D3..D0 = " + " ".join(
        ["0", "1", ABC[SEL23[p[0]][2]], ABC[SEL23[p[0]][2]] + "'"][c] for c in mux23(p)),
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  F = LEDG0 (green).  Answer on SW1 SW0."],
    P={k: [f"Your mux: S1 = {ABC[s1]}, S0 = {ABC[s0]}, and X = {ABC[x]} goes to the data inputs.   "
           f"{ABC[s1]}{ABC[s0]} = 00 -> D0,  01 -> D1,  10 -> D2,  11 -> D3."] for k, (s1, s0, x) in enumerate(SEL23)},
    L=[], F=[]))

# Q17: the hidden literal - a printed expression with one ?, the board computes it with ? = A, A', B, B', C or C'.
for _e in EXPR12:
    for _l in LITS:
        assert min_sop(table_of(_e.replace("?", "(" + _l + ")"), ABC), 3)[1] <= 7, (_e, _l)
NEW.append(Q(id="Q17", name="LITERAL", title="The hidden literal", inputs=[9, 8, 7], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], None], variants=v12, npub=len(EXPR12), nsec=6,
    tables=lambda p: [p[2]], answer=lambda p: (min_sop(p[2], 3)[1], 0xF),
    describe=lambda p: f"? = {LITS[p[1]]}, min SOP literals {min_sop(p[2], 3)[1]}",
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  Y = LEDG0 (green).  Answer on SW3..SW0."],
    P={i: [f"Your expression:   Y = {e}      - one literal is hidden: ? is A, A', B, B', C or C'."] for i, e in enumerate(EXPR12)},
    L=[], F=[]))

# Q18: bubble pushing - the board holds one of 4 printed circuits (SETS21: 8 sets, the first 4 circuits of each).
NEW.append(Q(id="Q18", name="BUBBLES", title="Bubble pushing: which circuit is in the board?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=[(i, k) for i in range(8) for k in range(4)], npub=8, nsec=4,
    tables=lambda p: [SETS21[p[0]][1][p[1]]], answer=lambda p: (p[1], 0x3),
    describe=lambda p: f"circuit {p[1]}: " + circ_txt(SETS21[p[0]][0][p[1]]),
    B=["A = SW9, B = SW8, C = SW7, D = SW6 (HEX3..HEX0).  Y = LEDG0 (green).  Answer on SW1 SW0.",
       "n1' means a bubble (NOT) on that input of the last gate."],
    P={i: ["The board holds ONE of these circuits:"] + [f"  {k}: {circ_txt(c)}" for k, c in enumerate(cs[:4])]
       for i, (cs, _) in enumerate(SETS21)},
    L=[], F=[]))

# Q19: one box with memory - one row sets it, one row resets it, the other two rows hold (12 variants).
NEW.append(Q(id="Q19", name="LATCH", title="A box with memory: what turns it on, what turns it off?", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=v02,
    tables=lambda p: [[1 if r == p[0] else 0 if r == p[1] else HOLD for r in range(4)]], answer=lambda p: (p[1], 0x3),
    describe=lambda p: f"ON at AB={p[0]:02b}, OFF at AB={p[1]:02b}",
    B=["A = SW9, B = SW8 (HEX3 HEX2).  The box = LEDG0 (green).  Answer on SW1 SW0.",
       "Move ONE switch at a time - two at once pass through a row in between."],
    L=[], F=[]))

# Q20: 8 boxes - which have memory? (the o01 puzzles, now on LEDG7..0 with A B = SW9 SW8 and the answer on SW7..SW0)
NEW.append(Q(id="Q20", name="SEQ", title="Combinational or sequential? (8 boxes)", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", i) for i in range(8)], hexes=[[9], [8], None, None], variants=QBY_O01_VARIANTS,
    tables=lambda p: [SEQ[t] if k == "seq" else t for k, t in p],
    answer=lambda p: (sum(1 << i for i, (k, _) in enumerate(p) if k == "seq"), 0xFF),
    describe=lambda p: "; ".join(f"box{i}: {t if k == 'seq' else 'comb ' + ''.join(map(str, t))}" for i, (k, t) in enumerate(p)),
    B=["A = SW9, B = SW8 (HEX3 HEX2).  Box i = LEDGi (8 boxes, all get the same A and B).  Answer on SW7..SW0.",
       "Move ONE switch at a time - two at once pass through a row in between."],
    L=[], F=[]))
# ================= the second round, Q21-Q30: each topic one step further (more inputs, more candidates)
_r2 = random.Random(121)
def perms_n(n, k):
    allp = [list(t) for t in itertools.permutations(range(n))]
    return allp if k >= len(allp) else _r2.sample(allp, k)
def cands_q(qid, name, title, sets, names, inputs, ncand, nsec, want_right, intro, hexes):
    v = []
    for e, cands in sets:
        ref = table_of(e, names)
        tts = [table_of(c, names) for c in cands]
        good = [t == ref for t in tts]
        assert any(good) and not all(good), (e, good)
        v += [(e, perm, tts, good, cands) for perm in perms_n(ncand, nsec)]
    return Q(id=qid, name=name, title=title, inputs=inputs, flat=True,
        outs=[("G", j) for j in range(ncand)], hexes=hexes, variants=v, npub=len(sets), nsec=nsec,
        tables=lambda p: [p[2][p[1][j]] for j in range(ncand)],
        answer=lambda p: (sum(1 << j for j in range(ncand) if p[3][p[1][j]] == want_right), (1 << ncand) - 1),
        describe=lambda p: "; ".join(f"LEDG{j} = {p[4][p[1][j]]}{'' if p[3][p[1][j]] else ' (wrong)'}" for j in range(ncand)),
        B=[("A = SW9, B = SW8, C = SW7, D = SW6 (HEX3..HEX0)." if len(names) == 4 else "A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).")
           + f"  {ncand} students' results = LEDG{ncand - 1}..LEDG0.  Answer on SW{ncand - 1}..SW0."],
        P={i: [f"{intro}   Y = {e}"] for i, (e, _) in enumerate(sets)}, L=[], F=[])

# Q21: SIGMA / PI of a hidden F of FOUR inputs
V21 = []
while len(V21) < 256:
    tt = [_r2.randint(0, 1) for _ in range(16)]
    if 5 <= sum(tt) <= 10 and tt not in V21:
        V21.append(tt)
NEW.append(Q(id="Q21", name="SIGMA4", title="Minterms and maxterms - four inputs", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=V21,
    tables=lambda p: [p], answer=lambda p: (16 - sum(p), 0xF),
    describe=lambda p: "F rows 0000..1111 = " + "".join(map(str, p)),
    B=["A = SW9, B = SW8, C = SW7, D = SW6 (HEX3..HEX0).  F = LEDG0 (green).  Answer on SW3..SW0."], L=[], F=[]))

# Q22: a 3:8 decoder, outputs on LEDG7..0 in a hidden order; the last step: the LED of a personal minterm
V22 = [(m, perm) for m in range(8) for perm in perms_n(8, 32)]
NEW.append(Q(id="Q22", name="DEC38", title="A 3:8 decoder: which light is which output?", inputs=[9, 8, 7], flat=True,
    outs=[("G", j) for j in range(8)], hexes=[[9], [8], [7], None], variants=V22, npub=8, nsec=32,
    tables=lambda p: [[1 if p[1][r] == j else 0 for r in range(8)] for j in range(8)],
    answer=lambda p: (p[1][p[0]], 0x7),
    describe=lambda p: "row -> LED: " + " ".join(f"{r:03b}->{p[1][r]}" for r in range(8)) + f"; minterm {p[0]}",
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  The decoder's 8 outputs = LEDG7..LEDG0, in a hidden order.  Answer on SW2..SW0."],
    P={m: [f"Your minterm for the last step:  m{m}  (A B C = {m:03b})."] for m in range(8)}, L=[], F=[]))

# Q23: the theorem lab with the 8 statements over A B C (THMS): statement k = SW9 SW8 SW7, A B C = SW6 SW5 SW4
def tables23(p):
    perm = p[1]
    return [[TT[perm[r >> 3]][side][r & 7] for r in range(64)] for side in (0, 1)]
V23 = [(x, perm) for x in range(8) for perm in perms_n(8, 32)]
NEW.append(Q(id="Q23", name="THEOREMS8", title="Perfect induction: 8 statements of A B C", inputs=[9, 8, 7, 6, 5, 4], flat=True,
    outs=[("G", 1), ("G", 0)], hexes=[[9, 8, 7], [6], [5], [4]], variants=V23, npub=8, nsec=32,
    tables=tables23, answer=lambda p: (p[1].index(p[0]), 0x7),
    describe=lambda p: "k0..k7 = " + ", ".join(f"{THMS[i][0]} = {THMS[i][1]}" for i in p[1]),
    B=["Statement number = SW9 SW8 SW7 (HEX3: 0-7).  A = SW6, B = SW5, C = SW4 (HEX2 HEX1 HEX0).",
       "LEFT side = LEDG1, RIGHT side = LEDG0.  Answer on SW3..SW0."],
    P={x: [f"Your statement for the last step:  {THMS[x][0]} = {THMS[x][1]}"] for x in range(8)}, L=[], F=[]))

# Q24: a story with FOUR letters (STORIES), 4 circuits on LEDG3..0
V24 = []
for st in STORIES:
    names = list(st[1])
    cands = [table_of(e, names) for e in [st[2]] + st[3]]
    V24 += [(st, perm, cands) for perm in perms_n(4, 24)]
NEW.append(Q(id="Q24", name="STORY4", title="From a story to an equation - four letters", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", j) for j in range(4)], hexes=[[9], [8], [7], [6]], variants=V24, npub=len(STORIES), nsec=24,
    tables=lambda p: [p[2][p[1][j]] for j in range(4)], answer=lambda p: (1 << p[1].index(0), 0xF),
    describe=lambda p: "; ".join(f"LEDG{j} = {([p[0][2]] + p[0][3])[p[1][j]]}" for j in range(4)),
    B=["Your four letters are on SW9 SW8 SW7 SW6, in the order shown below (HEX3..HEX0).  4 circuits = LEDG3..LEDG0.  Answer on SW3..SW0."],
    P={i: st[0] + ["Letters:  " + ",  ".join(f"{c} = SW{9 - k}" for k, c in enumerate(st[1]))] for i, st in enumerate(STORIES)},
    L=[], F=[]))

def sets_of(oid):
    o = QBY_OLD[oid]
    return [(o.variants[i * o.nsec][0], o.variants[i * o.nsec][1]) for i in range(o.npub)]
QBY_OLD = {q.id: q for q in QS}
NEW.append(cands_q("Q25", "DEMORGAN4", "De Morgan with four letters: which answers are right?", sets_of("o14"), ABCD,
    [9, 8, 7, 6], 4, 24, True, "Apply De Morgan to your expression:", [[9], [8], [7], [6]]))
NEW.append(cands_q("Q26", "MULTIPLY4", "Multiplying out and factoring - six answers", sets_of("o15"), ABCD,
    [9, 8, 7, 6], 6, 40, True, "Six students multiplied out (SOP) or factored (POS) your expression:", [[9], [8], [7], [6]]))
NEW.append(cands_q("Q27", "ERRORS5", "Common errors - five simplifications", sets_of("o13"), ABC,
    [9, 8, 7], 5, 40, False, "Five students simplified your expression:", [[9], [8], [7], None]))

# Q28: two-level with THREE first-level gates, each NAND or NOR (mixed), and Y = NAND3 or NOR3 (v18)
NEW.append(Q(id="Q28", name="NANDNOR3", title="Two-level logic: three gates, NAND or NOR each", inputs=[9, 8, 7], flat=True,
    outs=[("G", 3), ("G", 2), ("G", 1), ("G", 0)], hexes=[[9], [8], [7], None], variants=v18, tables=nn_tables,
    answer=lambda p: ((p[0][0][0] << 3) | (p[0][1][0] << 2) | (p[0][2][0] << 1) | p[1], 0xF),
    describe=desc_nn,
    B=["A = SW9, B = SW8, C = SW7 (HEX3 HEX2 HEX1).  First level: n1 = LEDG3, n2 = LEDG2, n3 = LEDG1 (2-input NAND or NOR",
       "of letters or their NOTs).  Second level: Y = LEDG0 = a 3-input NAND or NOR of n1, n2, n3.  Answer on SW3..SW0."],
    L=[], F=[]))

# Q29: bubble pushing with all EIGHT printed circuits of a set
NEW.append(Q(id="Q29", name="BUBBLES8", title="Bubble pushing: which of eight circuits?", inputs=[9, 8, 7, 6], flat=True,
    outs=[("G", 0)], hexes=[[9], [8], [7], [6]], variants=[(i, k) for i in range(8) for k in range(8)], npub=8, nsec=8,
    tables=lambda p: [SETS21[p[0]][1][p[1]]], answer=lambda p: (p[1], 0x7),
    describe=lambda p: f"circuit {p[1]}: " + circ_txt(SETS21[p[0]][0][p[1]]),
    B=["A = SW9, B = SW8, C = SW7, D = SW6 (HEX3..HEX0).  Y = LEDG0 (green).  Answer on SW2..SW0.",
       "n1' means a bubble (NOT) on that input of the last gate."],
    P={i: ["The board holds ONE of these circuits:"] + [f"  {k}: {circ_txt(c)}" for k, c in enumerate(cs)] for i, (cs, _) in enumerate(SETS21)},
    L=[], F=[]))

# Q30: a D latch - which input is the enable, and is it active at 1 or at 0?
DL30 = ["D latch, A enables, D = B", "D latch, B enables, D = A", "D latch, A' enables, D = B", "D latch, B' enables, D = A"]
NEW.append(Q(id="Q30", name="DLATCH", title="A D latch: which input is the enable?", inputs=[9, 8], flat=True, seq=True,
    outs=[("G", 0)], hexes=[[9], [8], None, None], variants=list(range(4)),
    tables=lambda p: [SEQ[DL30[p]]], answer=lambda p: (0 if p >= 2 else 1, 0x1),
    describe=lambda p: DL30[p],
    B=["A = SW9, B = SW8 (HEX3 HEX2).  The box = LEDG0 (green).  Answer on SW1 SW0.",
       "Move ONE switch at a time - two at once pass through a row in between."],
    L=[], F=[]))
QS = QS + NEW
QBY = {q.id: q for q in QS}
for q in QS:
    if q.npub > 1:
        assert set(q.P) == set(range(q.npub)), q.id

# ---------------------------------------------------------------- steps (new format - only these are rebuilt)
# A step = (lines on the screen, fn(params) -> (want, mask)); step 0 (login) is added by the runner and the board.
# Questions without steps keep the first format (one answer, no steps): their sof files were built by gen_v1.py.bak
# and are NOT rebuilt here; their codes are old_code_str().
def run_seq(q, p, seq):
    """LEDR outputs after the input rows in seq (outputs start at 0); seq must leave no output depending on the start."""
    tabs, st = q.tables(p), [None] * len(q.outs)
    for r in seq:
        for j in range(len(q.outs)):
            if tabs[j][r] != HOLD:
                st[j] = tabs[j][r]
    assert None not in st, (q.id, seq)
    return sum(st[j] << i for j, (k, i) in enumerate(q.outs))

# One switch at a time (Gray code): flipping two switches together always passes through a row in between,
# and a box with memory reacts to it. The long paths visit all four rows, so their end does not depend on the start.
S01A, S01B = [0, 1, 3, 2, 0], [0, 2, 3, 1, 0]
# Q01 variants (own RNG, so no other question changes): box 0 has no memory, box 1 is an SR latch (it holds at 00,
# so 00 -> 01 -> 00 and 00 -> 10 -> 00 end differently), 3-5 boxes with memory, at least 2 differ after the long paths.
_r01 = random.Random(101)
_q01 = QBY["o01"]
SR2 = ["SR, A sets, B resets", "SR, B sets, A resets"]
for _v in range(len(_q01.variants)):
    while True:
        _pos = [1] + _r01.sample([2, 3, 4, 5, 6, 7], _r01.choice([2, 3, 4]))
        _p = [("comb", _r01.choice(COMB2))] + [("seq", _r01.choice(SR2))] + \
             [("seq", _r01.choice(list(SEQ))) if i in _pos else ("comb", _r01.choice(COMB2)) for i in range(2, 8)]
        if bin(run_seq(_q01, _p, S01A) ^ run_seq(_q01, _p, S01B)).count("1") >= 2:
            break
    _q01.variants[_v] = _p
def box0_table(q, p):
    return sum(q.tables(p)[0][r] << r for r in range(4))
def run_box(q, p, seq, j):
    """Output j after the rows in seq; it must not depend on the start."""
    t, v = q.tables(p)[j], None
    for r in seq:
        if t[r] != HOLD:
            v = t[r]
    assert v is not None, (q.id, seq, j)
    return v
def box1_moves(q, p):
    return (run_box(q, p, [0, 1, 0], 1) << 1) | run_box(q, p, [0, 2, 0], 1)
# Every step: GOAL, what to do, ANSWER. run.ps1 adds the same answer recipe under every step.
def prio_win(p, ins):
    """Q07: the strongest of the inputs that are up."""
    for i in p[0]:
        if i in ins:
            return i
STEPS = {
    "Q01": [
        (["GOAL: meet the board. A gate is hidden in it: inputs A = SW9, B = SW8, output Y = LEDG0.",
          "Put A B = 0 0 (SW9 and SW8 down). Is the green light LEDG0 on?",
          "ANSWER: SW0 up if LEDG0 is on, SW0 down if it is off."],
         lambda q, p: (GATES[p][1][0], 0x1)),
        (["GOAL: the whole truth table of the gate.",
          "Try A B = 00, 01, 10, 11 (SW9 SW8) and write Y for each row.",
          "ANSWER: SW0 = Y at 00,  SW1 = Y at 01,  SW2 = Y at 10,  SW3 = Y at 11."],
         lambda q, p: (sum(GATES[p][1][r] << r for r in range(4)), 0xF)),
        (["GOAL: name the gate. Compare your truth table with what each gate does.",
          "ANSWER - first put SW3 SW2 SW1 SW0 all DOWN, then raise only the switches of your gate:",
          "   AND = (all down)    OR = SW0    XOR = SW1    NAND = SW1 + SW0    NOR = SW2    XNOR = SW2 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q02": [
        (["GOAL: meet F. It has three inputs: A = SW9, B = SW8, C = SW7. F = LEDG0.",
          "Put A B C = 0 0 0 (SW9, SW8, SW7 down). Is LEDG0 on?",
          "ANSWER: SW0 up if LEDG0 is on, SW0 down if it is off."],
         lambda q, p: (p[0], 0x1)),
        (["GOAL: the first half of the truth table - the 4 rows where A = 0. Keep SW9 DOWN.",
          "1. Set SW8 SW7 like this, and write down LEDG0 (on = 1) for each row:",
          "      row 000: SW8 down, SW7 down      row 001: SW8 down, SW7 up",
          "      row 010: SW8 up,   SW7 down      row 011: SW8 up,   SW7 up",
          "2. Copy the 4 lights to the right switches (up = 1):",
          "ANSWER: SW0 = row 000,  SW1 = row 001,  SW2 = row 010,  SW3 = row 011."],
         lambda q, p: (sum(p[r] << r for r in range(4)), 0xF)),
        (["GOAL: the second half - the 4 rows where A = 1. Keep SW9 UP.",
          "1. Set SW8 SW7 like this, and write down LEDG0 (on = 1) for each row:",
          "      row 100: SW8 down, SW7 down      row 101: SW8 down, SW7 up",
          "      row 110: SW8 up,   SW7 down      row 111: SW8 up,   SW7 up",
          "2. Copy the 4 lights to the right switches (up = 1):",
          "ANSWER: SW0 = row 100,  SW1 = row 101,  SW2 = row 110,  SW3 = row 111."],
         lambda q, p: (sum(p[4 + r] << r for r in range(4)), 0xF)),
        (["GOAL: minterms. A row where F = 1 is a MINTERM: F = SIGMA(those row numbers).",
          "Count the rows of your table where F = 1.",
          "ANSWER: the number on the switches:   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p), 0xF)),
        (["GOAL: maxterms. A row where F = 0 is a MAXTERM: F = PI(those row numbers).",
          "Count the rows of your table where F = 0.",
          "ANSWER: the number on the switches:   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q03": [
        (["GOAL: meet the 4 green lights. Each one is a TERM of A B C, like  A B'  or  A + C.",
          "Put A B C = 1 1 1 (SW9, SW8, SW7 up).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(t[7] << j for j, (_, t) in enumerate(p)), 0xF)),
        (["GOAL: ONE table of all 4 lights. Copy it to paper, go over the 8 rows once (0 = down, 1 = up),",
          "and mark the lights that are on in each row:",
          "   row (SW9 SW8 SW7)    LEDG3  LEDG2  LEDG1  LEDG0",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in the LEDG0 column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[0][1]), 0xF)),
        (["GOAL: the MINTERM - all three letters ANDed, like  A B' C. It is ON in only ONE row.",
          "In your table, find the column with a single 1.",
          "ANSWER: one switch up - SWi for that light (LEDGi)."],
         lambda q, p: (1 << [k for k, _ in p].index("min"), 0xF)),
        (["GOAL: the MAXTERM - all three letters ORed, like  A + B' + C. It is OFF in only ONE row.",
          "In your table, find the column with a single 0.",
          "ANSWER: one switch up - SWi for that light (LEDGi)."],
         lambda q, p: q.answer(p)),
    ],
    "Q04": [
        (["GOAL: the truth table of F. Copy it to paper, go over the 8 rows once (0 = down, 1 = up),",
          "and write F (LEDG0 on = 1) in each row:",
          "   row (SW9 SW8 SW7)    F",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in the F column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(f04(p)), 0xF)),
        (["GOAL: does A matter? Look at pairs of rows that differ ONLY in A (the first digit):",
          "   000 - 100      001 - 101      010 - 110      011 - 111",
          "If F is different in at least one pair, A matters.",
          "ANSWER: SW0 up if A matters, SW0 down if F is the same in all 4 pairs."],
         lambda q, p: (matters04(p, 0), 0x1)),
        (["GOAL: does B matter? Pairs that differ ONLY in B (the middle digit):",
          "   000 - 010      001 - 011      100 - 110      101 - 111",
          "ANSWER: SW0 up if B matters, SW0 down if F is the same in all 4 pairs."],
         lambda q, p: (matters04(p, 1), 0x1)),
        (["GOAL: one input never changes F - find it. (Check C too: pairs 000-001, 010-011, 100-101, 110-111.)",
          "ANSWER: raise ONE switch for the input that does NOT matter:   A = SW2    B = SW1    C = SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q05": [
        (["GOAL: meet the mux. Put S1 S0 = 0 0 (SW9, SW8 down) - now Y shows D0.",
          "Look at Y with C = 0 (SW7 down), then with C = 1 (SW7 up).",
          "ANSWER: SW0 = Y with C = 0,   SW1 = Y with C = 1   (up = on)."],
         lambda q, p: ((mux_tt(p)[1] << 1) | mux_tt(p)[0], 0x3)),
        (["GOAL: what is on D0? Put S1 S0 = 0 0 (SW9 down, SW8 down) - now Y shows D0.",
          "Look at Y with C = 0 (SW7 down) and with C = 1 (SW7 up):",
          "   Y 0 and 0 -> '0'     Y 1 and 1 -> '1'     Y = C (0 then 1) -> C     Y = opposite of C (1 then 0) -> C'",
          "ANSWER: '0' = all down    '1' = SW0    C = SW1    C' = SW1 + SW0"],
         lambda q, p: (p[3], 0x3)),
        (["GOAL: what is on D1? Put S1 S0 = 0 1 (SW9 down, SW8 up) - now Y shows D1.",
          "Look at Y with C = 0 (SW7 down) and with C = 1 (SW7 up):",
          "   Y 0 and 0 -> '0'     Y 1 and 1 -> '1'     Y = C (0 then 1) -> C     Y = opposite of C (1 then 0) -> C'",
          "ANSWER: '0' = all down    '1' = SW0    C = SW1    C' = SW1 + SW0"],
         lambda q, p: (p[2], 0x3)),
        (["GOAL: what is on D2? Put S1 S0 = 1 0 (SW9 up, SW8 down) - now Y shows D2.",
          "Look at Y with C = 0 (SW7 down) and with C = 1 (SW7 up):",
          "   Y 0 and 0 -> '0'     Y 1 and 1 -> '1'     Y = C (0 then 1) -> C     Y = opposite of C (1 then 0) -> C'",
          "ANSWER: '0' = all down    '1' = SW0    C = SW1    C' = SW1 + SW0"],
         lambda q, p: (p[1], 0x3)),
        (["GOAL: what is on D3? Put S1 S0 = 1 1 (SW9 up, SW8 up) - now Y shows D3.",
          "Look at Y with C = 0 (SW7 down) and with C = 1 (SW7 up):",
          "   Y 0 and 0 -> '0'     Y 1 and 1 -> '1'     Y = C (0 then 1) -> C     Y = opposite of C (1 then 0) -> C'",
          "ANSWER: '0' = all down    '1' = SW0    C = SW1    C' = SW1 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q06": [
        (["GOAL: meet the decoder. For every input row exactly ONE output is on (one-hot).",
          "Put A B = 0 0 (SW9 down, SW8 down). Which green light is on?",
          "ANSWER: one switch up - SWi for the light LEDGi that is on.   Write it down: row 00 -> LEDG?"],
         lambda q, p: (1 << p[1][0], 0xF)),
        (["GOAL: the output of row 01.",
          "Put A B = 0 1 (SW9 down, SW8 up). Which green light is on?",
          "ANSWER: one switch up - SWi for the light LEDGi that is on.   Write it down: row 01 -> LEDG?"],
         lambda q, p: (1 << p[1][1], 0xF)),
        (["GOAL: the output of row 10.",
          "Put A B = 1 0 (SW9 up, SW8 down). Which green light is on?",
          "ANSWER: one switch up - SWi for the light LEDGi that is on.   Write it down: row 10 -> LEDG?"],
         lambda q, p: (1 << p[1][2], 0xF)),
        (["GOAL: the output of row 11.",
          "Put A B = 1 1 (SW9 up, SW8 up). Which green light is on?",
          "ANSWER: one switch up - SWi for the light LEDGi that is on.   Write it down: row 11 -> LEDG?"],
         lambda q, p: (1 << p[1][3], 0xF)),
        (["GOAL: logic using a decoder. F = SIGMA(...) = an OR of the decoder outputs of its rows (see above).",
          "Look at your notes: which light belongs to each row of F?",
          "ANSWER: raise the TWO switches of those lights (SWi for LEDGi)."],
         lambda q, p: q.answer(p)),
    ],
    "Q07": [
        (["GOAL: meet the priority circuit. Raise ONLY SW9 (A3) - all of SW9..SW6 others down.",
          "One input alone always wins. Which light is on?",
          "ANSWER: one switch up - SWi for the light LEDGi that is on."],
         lambda q, p: (1 << 3, 0xF)),
        (["GOAL: two inputs together. Raise SW9 AND SW8 (A3 and A2). Only the stronger one lights its Y.",
          "Which light is on now?",
          "ANSWER: one switch up - SWi for that light."],
         lambda q, p: (1 << prio_win(p, [3, 2]), 0xF)),
        (["GOAL: the STRONGEST input. Raise all four: SW9, SW8, SW7, SW6.",
          "The light that is on belongs to the strongest input.",
          "ANSWER: one switch up - SWi for that light."],
         lambda q, p: (1 << p[0][0], 0xF)),
        (["GOAL: the WEAKEST input - it wins only when it is alone.",
          "From all four up: lower the winner's switch, see who wins next, lower it too ... the last one is the weakest.",
          "ANSWER: one switch up for the weakest input:   A3 = SW3   A2 = SW2   A1 = SW1   A0 = SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q08": [
        (["GOAL: is statement 0 true?  SW9, SW8 down = statement 0.  LEDG1 = its LEFT side, LEDG0 = its RIGHT side.",
          "Set SW7 SW6 = down down,  down up,  up down,  up up.",
          "In each one: are LEDG1 and LEDG0 the SAME (both on or both off)?",
          "ANSWER: SW0 up if they were the same in all 4.  SW0 down if they were different even once."],
         lambda q, p: (int(TT08[p[1][0]][0] == TT08[p[1][0]][1]), 0x1)),
        (["GOAL: the same check as step 1, for all 4 statements. Copy this table to paper:",
          "   statement   SW9 SW8      same in all 4?",
          "       0       down down        ?",
          "       1       down up          ?",
          "       2       up down          ?",
          "       3       up up            ?",
          "For each line: set SW9 SW8, move SW7 SW6 through down down, down up, up down, up up, and watch",
          "LEDG1 and LEDG0. The same (both on or both off) every time = yes. Different even once = no.",
          "ANSWER: raise the switch of every 'yes':  statement 0 = SW0,  1 = SW1,  2 = SW2,  3 = SW3."],
         lambda q, p: (sum(1 << k for k in range(4) if TT08[p[1][k]][0] == TT08[p[1][k]][1]), 0xF)),
        (["GOAL: where is YOUR statement (at the top)? Fill this table on paper from YOUR statement:",
          "   A B (SW7 SW6)    LEFT   RIGHT",
          "   0 0", "   0 1", "   1 0", "   1 1",
          "Now find the statement number whose LEDG1 (LEFT) and LEDG0 (RIGHT) show exactly your table.",
          "ANSWER: that number:   0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q09": [
        (["GOAL: meet the 4 circuits. First write the story as an equation, on paper.",
          "Put all three letters to 1 (SW9, SW8, SW7 up).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][7] << j for j in range(4)), 0xF)),
        (["GOAL: use YOUR equation. What is it when the letters are 1, 0, 1 (SW9 up, SW8 down, SW7 up)?",
          "Work it out on paper, from the equation.",
          "ANSWER: SW0 up if your equation gives 1, SW0 down if it gives 0."],
         lambda q, p: (p[2][0][5], 0x1)),
        (["GOAL: which circuit is your equation? Fill this table from your equation (paper), then compare it",
          "with each light on the board, row by row:",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: one switch up - SWi for the light that matches in all 8 rows."],
         lambda q, p: q.answer(p)),
    ],
    "Q10": [
        (["GOAL: De Morgan on paper. Remove the outer bar of your Y (outside in: (XY)' = X' + Y', (X + Y)' = X'Y').",
          "Then fill the table of Y from your result:",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in your Y column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[2][0]), 0xF)),
        (["GOAL: meet the 4 answers on the board. Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(4)), 0xF)),
        (["GOAL: the right answer. Compare each light with your table, row by row (all 8 rows).",
          "ANSWER: one switch up - SWi for the light that matches your Y in all 8 rows."],
         lambda q, p: q.answer(p)),
    ],
    "Q11": [
        (["GOAL: your own answer first. Work on YOUR expression (above) on paper, then fill its table:",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in your Y column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[2][[i for i, g in enumerate(p[3]) if g][0]]), 0xF)),
        (["GOAL: meet the 4 results on the board. Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(4)), 0xF)),
        (["GOAL: find the mistakes. Compare each light with your table, row by row (all 8 rows).",
          "ANSWER: SWi up for every light that is WRONG (different from your Y in some row) - two lights."],
         lambda q, p: q.answer(p)),
    ],
    "Q12": [
        (["GOAL: your own answer first. Work on YOUR expression (above) on paper, then fill its table:",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in your Y column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[2][[i for i, g in enumerate(p[3]) if g][0]]), 0xF)),
        (["GOAL: meet the 4 results on the board. Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(4)), 0xF)),
        (["GOAL: find the right answers. Compare each light with your table, row by row (all 8 rows).",
          "ANSWER: SWi up for every light that is RIGHT (equal to your Y in all 8 rows) - two lights."],
         lambda q, p: q.answer(p)),
    ],
    "Q13": [
        (["GOAL: the truth table of F. Copy it to paper, go over the 8 rows once (0 = down, 1 = up), write F (LEDG0):",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in the F column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p), 0xF)),
        (["GOAL: the minimal SOP. Write F as SIGMA of its minterms, then join minterms that differ in one letter",
          "(T10: XY + XY' = X), until no more joins - the fewest terms, each with the fewest letters.",
          "ANSWER: how many TERMS (products) does it have?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (min_sop(p, 3)[0], 0xF)),
        (["GOAL: count the letters. In your minimal SOP, count every letter of every term (A'B + C = 3 letters).",
          "ANSWER: how many LITERALS?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q14": [
        (["GOAL: meet the circuit. Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SW2 = n1 (LEDG2),  SW1 = n2 (LEDG1),  SW0 = Y (LEDG0)   (up = on)."],
         lambda q, p: (sum(t[0] << (2 - j) for j, t in enumerate(nn14_tables(p))), 0x7)),
        (["GOAL: NAND or NOR? Go over the 8 rows and watch n1 (LEDG2).",
          "A 2-input NAND is OFF in only 2 rows (both inputs 1).  A 2-input NOR is ON in only 2 rows (both inputs 0).",
          "ANSWER: SW0 up if n1 is a NAND, SW0 down if it is a NOR."],
         lambda q, p: (p[0], 0x1)),
        (["GOAL: the inputs of n1. Look at the 2 special rows of n1 (NAND: where it is off, NOR: where it is on).",
          "In those rows two letters stay the same - they are n1's inputs. NAND: a letter that is 1 there is X, 0 there is X'.",
          "NOR: a letter that is 0 there is X, 1 there is X'.",
          "ANSWER: two switches up:   SW5 = A   SW4 = A'   SW3 = B   SW2 = B'   SW1 = C   SW0 = C'"],
         lambda q, p: q.answer(p)),
    ],
    "Q15": [
        (["GOAL: meet the circuit. Put A B C D = 0 0 0 0 (SW9..SW6 down).",
          "ANSWER: copy the lights - SW2 = n1 (LEDG2),  SW1 = n2 (LEDG1),  SW0 = Y (LEDG0)   (up = on)."],
         lambda q, p: (sum(t[0] << (2 - j) for j, t in enumerate(ml_tables(p))), 0x7)),
        (["GOAL: G1. n1 (LEDG2) depends only on A and B: try A B = 00, 01, 10, 11 (SW9 SW8).",
          "AND: 1 only if both inputs are 1.  OR: 0 only if both are 0.  NAND: 0 only if both are 1.  NOR: 1 only if both are 0.",
          "ANSWER (on SW1 SW0):   AND = both down   OR = SW0   NAND = SW1   NOR = SW1 + SW0"],
         lambda q, p: (p[0], 0x3)),
        (["GOAL: G2. Its inputs are n1 (LEDG2) and C (SW7); its output is n2 (LEDG1). Try all four n1, C pairs.",
          "AND: 1 only if both inputs are 1.  OR: 0 only if both are 0.  NAND: 0 only if both are 1.  NOR: 1 only if both are 0.",
          "ANSWER (on SW1 SW0):   AND = both down   OR = SW0   NAND = SW1   NOR = SW1 + SW0"],
         lambda q, p: (p[1], 0x3)),
        (["GOAL: G3. Its inputs are n2 (LEDG1) and D (SW6); its output is Y (LEDG0). Try all four n2, D pairs.",
          "AND: 1 only if both inputs are 1.  OR: 0 only if both are 0.  NAND: 0 only if both are 1.  NOR: 1 only if both are 0.",
          "ANSWER (on SW1 SW0):   AND = both down   OR = SW0   NAND = SW1   NOR = SW1 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q16": [
        (["GOAL: the truth table of F. Copy it to paper, go over the 8 rows once (0 = down, 1 = up), write F (LEDG0):",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[1]), 0x7)),
        (["GOAL: D0. Look at the 2 rows of your table where your S1 S0 = 0 0 (one with X = 0, one with X = 1).",
          "F there is 0 and 0 -> D0 = '0'.   1 and 1 -> '1'.   0 then 1 (follows X) -> X.   1 then 0 -> X'.",
          "ANSWER (on SW1 SW0):   '0' = both down   '1' = SW0   X = SW1   X' = SW1 + SW0"],
         lambda q, p: (mux23(p)[3], 0x3)),
        (["GOAL: D1. Look at the 2 rows of your table where your S1 S0 = 0 1 (one with X = 0, one with X = 1).",
          "F there is 0 and 0 -> D1 = '0'.   1 and 1 -> '1'.   0 then 1 (follows X) -> X.   1 then 0 -> X'.",
          "ANSWER (on SW1 SW0):   '0' = both down   '1' = SW0   X = SW1   X' = SW1 + SW0"],
         lambda q, p: (mux23(p)[2], 0x3)),
        (["GOAL: D2. Look at the 2 rows of your table where your S1 S0 = 1 0 (one with X = 0, one with X = 1).",
          "F there is 0 and 0 -> D2 = '0'.   1 and 1 -> '1'.   0 then 1 (follows X) -> X.   1 then 0 -> X'.",
          "ANSWER (on SW1 SW0):   '0' = both down   '1' = SW0   X = SW1   X' = SW1 + SW0"],
         lambda q, p: (mux23(p)[1], 0x3)),
        (["GOAL: D3. Look at the 2 rows of your table where your S1 S0 = 1 1 (one with X = 0, one with X = 1).",
          "F there is 0 and 0 -> D3 = '0'.   1 and 1 -> '1'.   0 then 1 (follows X) -> X.   1 then 0 -> X'.",
          "ANSWER (on SW1 SW0):   '0' = both down   '1' = SW0   X = SW1   X' = SW1 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q17": [
        (["GOAL: the truth table of the board's Y. Copy it to paper, go over the 8 rows once, write Y (LEDG0):",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[2]), 0xF)),
        (["GOAL: find the hidden literal. Try ? = A in your expression: work out its table on paper and compare with",
          "the board's table. Not the same? Try A', then B, B', C, C' - only one of them matches.",
          "ANSWER:   A = SW0   A' = SW1   B = SW1+SW0   B' = SW2   C = SW2+SW0   C' = SW2+SW1"],
         lambda q, p: (p[1] + 1, 0x7)),
        (["GOAL: simplify Y (with the right literal) to a minimal SOP and count its letters (A'B + C = 3).",
          "ANSWER: how many LITERALS?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q18": [
        (["GOAL: two quick looks at the board. Put A B C D = 0 0 0 0 (all down), then 1 1 1 1 (all up).",
          "ANSWER: SW0 = Y (LEDG0) at 0000,   SW1 = Y at 1111   (up = on)."],
         lambda q, p: ((SETS21[p[0]][1][p[1]][15] << 1) | SETS21[p[0]][1][p[1]][0], 0x3)),
        (["GOAL: which circuit? Push the bubbles of each circuit above to an SOP (paper), or just work out",
          "its Y in a few rows (start with 0000 and 1111). Compare with the board until only one circuit fits.",
          "ANSWER: its number:   0 = both down   1 = SW0   2 = SW1   3 = SW1 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q19": [
        (["GOAL: meet the box. Start at A B = 0 0, then ONE switch at a time: SW8 up (01), SW9 up (11),",
          "SW8 down (10), SW9 down (00). Watch LEDG0 the whole time.",
          "ANSWER: SW0 up if LEDG0 changed at least once on the way."],
         lambda q, p: (1, 0x1)),
        (["GOAL: the row that turns the box ON. The box stays as it is in most rows - only ONE row switches it on.",
          "Find it: when the light goes on, which row are you in?",
          "ANSWER: that row A B on SW1 SW0:   00 = both down   01 = SW0   10 = SW1   11 = SW1 + SW0"],
         lambda q, p: (p[0], 0x3)),
        (["GOAL: the row that turns the box OFF. (In the other two rows the box just remembers.)",
          "ANSWER: that row A B on SW1 SW0:   00 = both down   01 = SW0   10 = SW1   11 = SW1 + SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q20": [
        (["GOAL: read ONE box. Box 0 = LEDG0 (it has no memory).",
          "Try the four rows of A B (SW9 SW8) and write LEDG0 for each row.",
          "ANSWER: SW3 = LEDG0 at A B = 11,  SW2 = at 10,  SW1 = at 01,  SW0 = at 00."],
         lambda q, p: (box0_table(q, p), 0xF)),
        (["GOAL: a box that REMEMBERS. Box 1 = LEDG1.",
          "1. A B = 00. Raise SW8, then lower it (back to 00). Write LEDG1.",
          "2. Raise SW9, then lower it (back to 00). Write LEDG1.",
          "Both times A B = 00 - but LEDG1 is different: the box remembers what came before.",
          "ANSWER: SW1 = LEDG1 after move 1,  SW0 = LEDG1 after move 2."],
         lambda q, p: (box1_moves(q, p), 0x3)),
        (["GOAL: which other boxes remember? Test all 8 on two long paths, one switch at a time:",
          "Path 1 from 00: SW8 up, SW9 up, SW8 down, SW9 down. Write LEDG7..LEDG0.",
          "Path 2 from 00: SW9 up, SW8 up, SW9 down, SW8 down. Write LEDG7..LEDG0.",
          "ANSWER: SWi up for every box whose light is different at the end of the two paths."],
         lambda q, p: (run_seq(q, p, S01A) ^ run_seq(q, p, S01B), 0xFF)),
        (["GOAL: ALL boxes with memory. Some remember only in another row, not at 00.",
          "For every row of A B, arrive at it from both neighbours (one switch at a time)",
          "and watch whether a light depends on where you came from.",
          "ANSWER: SWi up for every box with memory (SW7..SW0)."],
         lambda q, p: q.answer(p)),
    ],
    "Q21": [
        (["WHAT YOU DO: look at the green light LEDG0 for 4 positions of the switches, and write on/off.",
          "(16 positions in all - this is round 1 of 4.)",
          "1. Put SW9 DOWN and SW8 DOWN. Do not touch them in this round.",
          "2. SW7 down, SW6 down  - is the green light on?   write: position 1 = on / off",
          "3. SW7 down, SW6 UP    - is it on?                position 2",
          "4. SW7 UP,   SW6 down  - is it on?                position 3",
          "5. SW7 UP,   SW6 UP    - is it on?                position 4",
          "ANSWER: for every position that was ON, raise one switch:",
          "   position 1 -> SW0      position 2 -> SW1      position 3 -> SW2      position 4 -> SW3"],
         lambda q, p: (sum(p[0 + r] << r for r in range(4)), 0xF)),
        (["ROUND 2 of 4 - the same as round 1, only SW9 and SW8 are different.",
          "1. Put SW9 DOWN and SW8 UP. Do not touch them in this round.",
          "2. SW7 down, SW6 down  - is the green light on?   write: position 1 = on / off",
          "3. SW7 down, SW6 UP    - is it on?                position 2",
          "4. SW7 UP,   SW6 down  - is it on?                position 3",
          "5. SW7 UP,   SW6 UP    - is it on?                position 4",
          "ANSWER: for every position that was ON, raise one switch:",
          "   position 1 -> SW0      position 2 -> SW1      position 3 -> SW2      position 4 -> SW3"],
         lambda q, p: (sum(p[4 + r] << r for r in range(4)), 0xF)),
        (["ROUND 3 of 4 - the same as round 1, only SW9 and SW8 are different.",
          "1. Put SW9 UP and SW8 DOWN. Do not touch them in this round.",
          "2. SW7 down, SW6 down  - is the green light on?   write: position 1 = on / off",
          "3. SW7 down, SW6 UP    - is it on?                position 2",
          "4. SW7 UP,   SW6 down  - is it on?                position 3",
          "5. SW7 UP,   SW6 UP    - is it on?                position 4",
          "ANSWER: for every position that was ON, raise one switch:",
          "   position 1 -> SW0      position 2 -> SW1      position 3 -> SW2      position 4 -> SW3"],
         lambda q, p: (sum(p[8 + r] << r for r in range(4)), 0xF)),
        (["ROUND 4 of 4 - the same as round 1, only SW9 and SW8 are different.",
          "1. Put SW9 UP and SW8 UP. Do not touch them in this round.",
          "2. SW7 down, SW6 down  - is the green light on?   write: position 1 = on / off",
          "3. SW7 down, SW6 UP    - is it on?                position 2",
          "4. SW7 UP,   SW6 down  - is it on?                position 3",
          "5. SW7 UP,   SW6 UP    - is it on?                position 4",
          "ANSWER: for every position that was ON, raise one switch:",
          "   position 1 -> SW0      position 2 -> SW1      position 3 -> SW2      position 4 -> SW3"],
         lambda q, p: (sum(p[12 + r] << r for r in range(4)), 0xF)),
        (["HOW MANY TIMES WAS THE LIGHT ON? Count the ON positions you wrote in rounds 1-4 (16 positions in all).",
          "(A position where F is on is called a MINTERM.)",
          "ANSWER: put that number on the switches:",
          "   1 = SW0          2 = SW1          3 = SW1+SW0       4 = SW2           5 = SW2+SW0       6 = SW2+SW1",
          "   7 = SW2+SW1+SW0  8 = SW3          9 = SW3+SW0      10 = SW3+SW1      11 = SW3+SW1+SW0  12 = SW3+SW2"],
         lambda q, p: (sum(p), 0xF)),
        (["HOW MANY TIMES WAS THE LIGHT OFF? That is 16 minus your answer before.",
          "(A position where F is off is called a MAXTERM.)",
          "ANSWER: put that number on the switches:",
          "   1 = SW0          2 = SW1          3 = SW1+SW0       4 = SW2           5 = SW2+SW0       6 = SW2+SW1",
          "   7 = SW2+SW1+SW0  8 = SW3          9 = SW3+SW0      10 = SW3+SW1      11 = SW3+SW1+SW0  12 = SW3+SW2"],
         lambda q, p: q.answer(p)),
    ],
    "Q22": [
        (["GOAL: meet the decoder. Put A B C = 0 0 0 (SW9, SW8, SW7 down). Exactly one green light is on.",
          "ANSWER: its number in binary: SW2 = 4, SW1 = 2, SW0 = 1 - raise the ones that add up to it (0 = all down)   (LEDG5 = SW2 + SW0)."],
         lambda q, p: (p[1][0], 0x7)),
        (["GOAL: one more. Put A B C = 1 1 1 (all three up). Which light is on now?",
          "ANSWER: its number in binary: SW2 = 4, SW1 = 2, SW0 = 1 - raise the ones that add up to it (0 = all down)."],
         lambda q, p: (p[1][7], 0x7)),
        (["GOAL: your minterm (above). Put its row on SW9 SW8 SW7 and see which light is on.",
          "ANSWER: its number in binary: SW2 = 4, SW1 = 2, SW0 = 1 - raise the ones that add up to it (0 = all down)."],
         lambda q, p: q.answer(p)),
    ],
    "Q23": [
        (["WHAT YOU DO: check statement 0 - are its two lights ALWAYS the same?",
          "(Each statement is like  A(A + B) = A.  LEDG1 = its left side, LEDG0 = its right side.",
          " A statement is TRUE when the two lights are equal - both on, or both off - in every position.)",
          "1. Put SW9, SW8, SW7 DOWN. This chooses statement 0. Do not touch them.",
          "2. Set SW6 SW5 SW4 to each of these 8 positions. Each time look: LEDG1 and LEDG0 - equal?",
          "     a. down down down          e. up down down",
          "     b. down down up            f. up down up",
          "     c. down up down            g. up up down",
          "     d. down up up              h. up up up",
          "ANSWER: equal in ALL 8 positions -> raise SW0.   Different even once -> leave SW0 DOWN."],
         lambda q, p: (int(TRUE[p[1][0]]), 0x1)),
        (["WHAT YOU DO: the same check for all 8 statements, and count how many are true.",
          "1. Set the statement number on SW9 SW8 SW7:",
          "   statement 0 = SW9 SW8 SW7 down down down    1 = down down up    2 = down up down    3 = down up up",
          "             4 = up down down                  5 = up down up      6 = up up down      7 = up up up",
          "2. For each statement do the 8 positions of A B C, as in step 1, and write: true / false.",
          "ANSWER: how many statements are true? Put the number:",
          "   0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(TRUE), 0xF)),
        (["WHAT YOU DO: find where YOUR statement (at the top of the screen) is on the board.",
          "1. On paper, fill this table for YOUR statement - what its LEFT side gives, and what its RIGHT side gives:",
          "   A B C  (SW6 SW5 SW4)    LEFT   RIGHT",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "2. On the board, try statement numbers (SW9 SW8 SW7, as in step 2). For each one compare LEDG1 with",
          "   your LEFT column and LEDG0 with your RIGHT column, in the 8 positions of SW6 SW5 SW4.",
          "3. The statement where BOTH lights match your table in all 8 positions is yours.",
          "ANSWER: its number:",
          "   0 = all down   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: q.answer(p)),
    ],
    "Q24": [
        (["GOAL: meet the 4 circuits. Write the story as an equation (paper). Put all four letters to 1 (SW9..SW6 up).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][15] << j for j in range(4)), 0xF)),
        (["GOAL: use YOUR equation: what is it when the letters are 1, 0, 1, 0 (SW9 up, SW8 down, SW7 up, SW6 down)?",
          "ANSWER: SW0 up if your equation gives 1, SW0 down if it gives 0."],
         lambda q, p: (p[2][0][10], 0x1)),
        (["GOAL: which circuit is your equation? Compare each light with your equation in all 16 rows",
          "(rows where they differ rule a light out - start with the rows you already know).",
          "ANSWER: one switch up - SWi for the light that matches in every row."],
         lambda q, p: q.answer(p)),
    ],
    "Q25": [
        (["GOAL: meet the 4 answers. Put A B C D = 0 0 0 0 (SW9..SW6 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(4)), 0xF)),
        (["GOAL: and at A B C D = 1 1 1 1 (SW9..SW6 up).",
          "ANSWER: copy the lights (SW3..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][15] << j for j in range(4)), 0xF)),
        (["GOAL: De Morgan on paper (outside in), then compare each light with your result row by row.",
          "ANSWER: SWi up for every light that is RIGHT (equal to Y in all 16 rows) - one or two lights."],
         lambda q, p: q.answer(p)),
    ],
    "Q26": [
        (["GOAL: meet the 6 answers (LEDG5..LEDG0). Put A B C D = 0 0 0 0 (SW9..SW6 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW5..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(6)), 0x3F)),
        (["GOAL: and at A B C D = 1 1 1 1 (SW9..SW6 up).",
          "ANSWER: copy the lights (SW5..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][15] << j for j in range(6)), 0x3F)),
        (["GOAL: multiply out or factor your expression on paper, then compare each light with it row by row.",
          "ANSWER: SWi up for every light that is RIGHT (equal to Y in all 16 rows) - two lights."],
         lambda q, p: q.answer(p)),
    ],
    "Q27": [
        (["GOAL: your own answer first. Simplify YOUR expression (above) on paper, then fill its table:",
          "   row (SW9 SW8 SW7)    Y",
          "   0 0 0",
          "   0 0 1",
          "   0 1 0",
          "   0 1 1",
          "   1 0 0",
          "   1 0 1",
          "   1 1 0",
          "   1 1 1",
          "ANSWER: how many 1s in your Y column?   1 = SW0   2 = SW1   3 = SW1+SW0   4 = SW2   5 = SW2+SW0   6 = SW2+SW1   7 = SW2+SW1+SW0"],
         lambda q, p: (sum(p[2][[i for i, g in enumerate(p[3]) if g][0]]), 0xF)),
        (["GOAL: meet the 5 results (LEDG4..LEDG0). Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SWi up if LEDGi is on (SW4..SW0)."],
         lambda q, p: (sum(p[2][p[1][j]][0] << j for j in range(5)), 0x1F)),
        (["GOAL: find the mistakes. Compare each light with your table, row by row.",
          "ANSWER: SWi up for every light that is WRONG (different from your Y in some row)."],
         lambda q, p: q.answer(p)),
    ],
    "Q28": [
        (["GOAL: meet the circuit. Put A B C = 0 0 0 (SW9, SW8, SW7 down).",
          "ANSWER: copy the lights - SW3 = n1 (LEDG3), SW2 = n2, SW1 = n3, SW0 = Y (LEDG0)."],
         lambda q, p: (sum(t[0] << (3 - j) for j, t in enumerate(nn_tables(p))), 0xF)),
        (["GOAL: n1 (LEDG3): NAND or NOR? Go over the 8 rows.",
          "A 2-input NAND is OFF in only 2 rows (both inputs 1).  A 2-input NOR is ON in only 2 rows (both inputs 0).",
          "ANSWER: SW0 up if n1 is a NAND, SW0 down if it is a NOR."],
         lambda q, p: (p[0][0][0], 0x1)),
        (["GOAL: every gate. n2 and n3 the same way. For Y (3 inputs n1 n2 n3): watch a row where n1, n2, n3 are",
          "NOT all equal - a NAND gives 1 there, a NOR gives 0.",
          "ANSWER: SW3 = n1,  SW2 = n2,  SW1 = n3,  SW0 = Y:   up = NAND,  down = NOR."],
         lambda q, p: q.answer(p)),
    ],
    "Q29": [
        (["GOAL: two quick looks. Put A B C D = 0 0 0 0 (all down), then 1 1 1 1 (all up).",
          "ANSWER: SW0 = Y (LEDG0) at 0000,   SW1 = Y at 1111   (up = on)."],
         lambda q, p: ((SETS21[p[0]][1][p[1]][15] << 1) | SETS21[p[0]][1][p[1]][0], 0x3)),
        (["GOAL: which circuit? Work out each circuit's Y in a few rows (paper; bubble pushing helps),",
          "and compare with the board, until only one circuit is left.",
          "ANSWER: its number in binary: SW2 = 4, SW1 = 2, SW0 = 1 - raise the ones that add up to it (0 = all down)."],
         lambda q, p: q.answer(p)),
    ],
    "Q30": [
        (["GOAL: a D latch: when its ENABLE is active it copies its DATA input, otherwise it remembers.",
          "One of A, B is the enable, the other is the data. Walk 00 -> 01 -> 11 -> 10 -> 00 (one switch at a time).",
          "ANSWER: SW0 up if LEDG0 changed at least once on the way."],
         lambda q, p: (1, 0x1)),
        (["GOAL: which input is the ENABLE? Set one input, then move the OTHER one up and down and watch the box.",
          "The enable is the input that, in one of its positions, makes the box FOLLOW the other one; in its other position the box stays.",
          "ANSWER: SW1 up if A (SW9) is the enable,  SW0 up if B (SW8) is the enable - one switch."],
         lambda q, p: (2 if p in (0, 2) else 1, 0x3)),
        (["GOAL: is the enable active when it is 1 (up) or when it is 0 (down)?",
          "ANSWER: SW0 up if the box follows the data while the enable is UP,  SW0 down if while it is DOWN."],
         lambda q, p: q.answer(p)),
    ],
    "o01": [
        (["GOAL: read ONE box. Box 0 = LEDR0 (it has no memory).",
          "Try the four rows of A B (SW1 SW0) and write LEDR0 for each row.",
          "ANSWER: SW3 = LEDR0 at A B = 11,  SW2 = at 10,  SW1 = at 01,  SW0 = at 00."],
         lambda q, p: (box0_table(q, p), 0xF)),
        (["GOAL: a box that REMEMBERS. Box 1 = LEDR1.",
          "1. A B = 00. Raise SW0, then lower it (back to 00). Write LEDR1.",
          "2. Raise SW1, then lower it (back to 00). Write LEDR1.",
          "Both times A B = 00 - but LEDR1 is different: the box remembers what came before.",
          "ANSWER: SW1 = LEDR1 after move 1,  SW0 = LEDR1 after move 2."],
         lambda q, p: (box1_moves(q, p), 0x3)),
        (["GOAL: which other boxes remember? Test all 8 the same way, on two long paths.",
          "Path 1 from 00, one switch at a time: SW0 up, SW1 up, SW0 down, SW1 down. Write LEDR7..LEDR0.",
          "Path 2 from 00: SW1 up, SW0 up, SW1 down, SW0 down. Write LEDR7..LEDR0.",
          "ANSWER: SWi up for every box whose light is different at the end of the two paths."],
         lambda q, p: (run_seq(q, p, S01A) ^ run_seq(q, p, S01B), 0xFF)),
        (["GOAL: ALL boxes with memory. Some remember only in another row, not at 00.",
          "For every row of A B, arrive at it from both neighbours (one switch at a time)",
          "and watch whether a light depends on where you came from.",
          "ANSWER: SWi up for every box with memory (SW7..SW0)."],
         lambda q, p: q.answer(p)),
    ],
}
for q in QS:
    q.steps = STEPS.get(q.id, [])
    q.ns = len(q.steps) + 1 if q.steps else 0		# with the login step
    q.flat = getattr(q, "flat", False)
    assert q.ns <= 8

# The names follow the LESSON order (tools/lesson.txt): topic 1 = Q01-Q12, topic 2 = Q13-Q22, topic 3 = Q23-Q38
# (each topic opens with the easy slide questions of w3_easy.py, see below), so "TOPIC 1 QUESTION 9" is Q09. The questions above were written under their first names (by difficulty);
# RENAME maps first name -> lesson name. Codes and variants follow the new name (HMAC of the name).
RENAME = {
    "Q01": "Q01", "Q02": "Q02", "Q03": "Q03", "Q04": "Q04", "Q21": "Q05", "Q08": "Q06", "Q23": "Q07", "Q13": "Q08", "Q17": "Q09",
    "Q09": "Q10", "Q10": "Q11", "Q11": "Q12", "Q12": "Q13", "Q24": "Q14", "Q25": "Q15", "Q27": "Q16", "Q26": "Q17",
    "Q05": "Q18", "Q06": "Q19", "Q07": "Q20", "Q16": "Q21", "Q22": "Q22", "Q14": "Q23", "Q15": "Q24", "Q18": "Q25",
    "Q28": "Q26", "Q29": "Q27", "Q19": "Q28", "Q30": "Q29", "Q20": "Q30"}
assert sorted(RENAME.values()) == [f"Q{i:02d}" for i in range(1, 31)]
for q in NEW:
    q.id = RENAME[q.id]
NEW.sort(key=lambda q: q.id)
QS = [q for q in QS if not q.id.startswith("Q")] + NEW
QBY = {q.id: q for q in QS}
# Hebrew screens (he_text.py): replaces title / B / P / step texts, never the answers
exec(open(f"{HERE}/he_text.py", encoding="utf-8").read())
apply_hebrew(NEW)
# The easy questions (w3_easy.py, the slides' own circuits, Hebrew steps written there) open each lesson topic; the 30
# above follow them in their topic (Q01-Q09, Q10-Q17, Q18-Q30), and all get new lesson ids Q01.. in this order.
exec(open(f"{HERE}/w3_easy.py", encoding="utf-8").read())
NEW = [q for t, rg in enumerate([range(1, 10), range(10, 18), range(18, 31)])
       for q in EASY_W3[t] + [QBY[f"Q{i:02d}"] for i in rg]]
for _i, q in enumerate(NEW, 1):
    q.id = f"Q{_i:02d}"
QS = [q for q in QS if not q.id.startswith("Q")] + NEW
QBY = {q.id: q for q in QS}

def step_answer(q, p, k):
    return q.steps[k - 1][1](q, p)

def old_code_str(qid, s):
    """The first format (no steps): 3 hidden digits + check digit over them and the login."""
    h = mac(f"{qid}|{s}")
    c = ((h[0] << 8) | h[1]) >> 4
    d3, d2, d1 = c >> 8, (c >> 4) & 15, c & 15
    d0 = (d3 + 3 * d2 + 5 * d1 + 7 + 9 * (s & 15) + 11 * ((s >> 4) & 15) + 13 * (s >> 8)) % 16
    return f"{d3:X}{d2:X}{d1:X}{d0:X}"

def final_code(q, s):
    return code_str(q.id, s, q.ns - 1) if q.ns else old_code_str(q.id, s)

# ---------------------------------------------------------------- checks on the puzzles themselves
def check_question(q):
    """Every answer (each step and the last) must follow from what the student can see (the tables + the printed
    text), and the printed text alone must not give the last answer (several answers for every printed text)."""
    seen, per_pub = {}, {}
    for v, p in enumerate(q.variants):
        pub = v // q.nsec
        wants = [q.answer(p)] + [step_answer(q, p, k) for k in range(1, q.ns)]
        for want, mask in wants:
            assert want & ~mask == 0 and mask < 1024, (q.id, v)
        sig = (pub, tuple(tuple(t) for t in q.tables(p)))
        assert seen.setdefault(sig, wants) == wants, f"{q.id}: variant {v} - same board, different answer"
        per_pub.setdefault(pub, set()).add(wants[0][0])
        for t in q.tables(p):
            assert len(t) == 1 << q.n and all(x in (0, 1, HOLD) for x in t), q.id
    worst = min(len(s) for s in per_pub.values())
    assert worst >= 2, f"{q.id}: the printed text gives the answer"
    return worst

# ---------------------------------------------------------------- hardware (steps)
SEG = [0x40, 0x79, 0x24, 0x30, 0x19, 0x12, 0x02, 0x78, 0x00, 0x10, 0x08, 0x03, 0x46, 0x21, 0x06, 0x0E]
CH = {"L": 0b1000111, "A": 0b0001000, "n": 0b0101011, "S": 0b0010010, "E": 0b0000110, "r": 0b0101111, "P": 0b0001100, None: 0x7F}

def verilog(q):
    n, no = q.n, len(q.outs)
    row = ", ".join(f"sw[{s}]" for s in q.inputs)
    clocked, stdecl = "", ""
    if q.sb:
        row = "st, " + row
        stdecl = f"\treg [{q.sb - 1}:0] st;\t\t\t\t// the state (a clocked question)\n"
        nxt = ", ".join(f"q[{[j for j, (k, i) in enumerate(q.outs) if k == 'N' and i == b][0]}]" for b in range(q.sb - 1, -1, -1))
        clocked = f"""
	// the state register: KEY1 = one clock edge, KEY0 = reset; the table gives the next state (outputs N)
	wire press1 = k2[1] & ~k1[1];
	wire press0 = k2[0] & ~k1[0];
	initial st = {q.sb}'d0;
	always @(posedge CLOCK_50)
		if (!go || settle != 4'd15 || press0) st <= {q.sb}'d0;
		else if (press1) st <= {{{nxt}}};
"""
    leds = [f"\t\t\t{'LEDR' if kind == 'R' else 'LEDG'}[{i}] = q[{j}];" for j, (kind, i) in enumerate(q.outs) if kind in "RG"]
    for d, h in zip((3, 2, 1, 0), ("HEX3", "HEX2", "HEX1", "HEX0")):
        hb = {i[1]: j for j, (kind, i) in enumerate(q.outs) if kind == "H" and i[0] == d}
        mj = [j for j, (kind, i) in enumerate(q.outs) if kind == "M" and i == d]
        if hb:
            leds.append(f"\t\t\t{h} = seg({{" + ", ".join(f"q[{hb[b]}]" if b in hb else "1'b0" for b in (3, 2, 1, 0)) + "});")
        elif mj:
            leds.append(f"\t\t\t{h} = q[{mj[0]}] ? 7'h3F : 7'h7F;")
    hexes = []
    for h, spec in zip(("HEX3", "HEX2", "HEX1", "HEX0"), q.hexes):
        if isinstance(spec, list):
            d = ", ".join(f"sw[{s}]" for s in spec)
            pad = 4 - len(spec)
            hexes.append(f"\t\t\t{h} = seg({{{str(pad) + chr(39) + 'b0, ' if pad else ''}{d}}});")
        elif spec:
            hexes.append(f"\t\t\t{h} = 7'h{CH[spec]:02X};")
    kcase = "".join(f"\t\t\t3'd{k}: begin c1 = 16'h{K1[k]:04X}; c2 = 16'h{K2[k]:04X}; end\n" for k in range(8))
    return f"""// Class exercise {q.id} ({q.name}) - Terasic DE1 (Cyclone II EP2C20F484C7), in steps.
// Generated by C:/DE10/solutions/class_exercise/gen.py - students get only the .sof.
// The PC talks to the board over the USB cable (In-System Sources and Probes, quartus_stp):
//   source = {{go, start step[2:0], login[9:0]}} written by run.ps1 - no login on the switches;
//   probe  = {{done, step[2:0], code[15:0]}} read by run.ps1 - the code is 0 until the last step is solved.
// The student puts the answer on the switches and presses KEY2: PASS (next step) or Err, for one second.
module ce(
	input            CLOCK_50,
	input      [9:0] SW,
	input      [3:0] KEY,
	output reg [9:0] LEDR,
	output reg [7:0] LEDG,
	output reg [6:0] HEX0,
	output reg [6:0] HEX1,
	output reg [6:0] HEX2,
	output reg [6:0] HEX3
	);
	localparam N = {n}, NO = {no}, NS = {q.ns};
	parameter FLASH = 26'd50_000_000;		// PASS / Err stay one second

	reg [9:0] sw = 10'd0;
	reg [3:0] k1 = 4'hF, k2 = 4'hF;
	always @(posedge CLOCK_50) begin sw <= SW; k1 <= KEY; k2 <= k1; end
	wire press2 = k2[2] & ~k1[2];		// KEY2 pressed (the keys are active low)

	// ---- the link to the PC
	wire [13:0] src;
	reg  [19:0] probe = 20'd0;
	altsource_probe #(.sld_auto_instance_index("YES"), .sld_instance_index(0), .instance_id("CE"),
		.probe_width(20), .source_width(14), .source_initial_value("0"), .enable_metastability("NO"))
		sp(.probe(probe), .source(src));
	reg [13:0] s1 = 14'd0, s2 = 14'd0;
	always @(posedge CLOCK_50) begin s1 <= src; s2 <= s1; end
	wire       go    = s2[13];
	wire [2:0] start = s2[12:10];
	wire [9:0] seed  = s2[9:0];

	// per login number: {{secret[15:0], variant[7:0]}}
	reg [23:0] srom [0:1023];
	initial $readmemh("seed.hex", srom);
	reg [23:0] sq = 24'd0;
	always @(posedge CLOCK_50) sq <= srom[seed];
	wire [7:0]  vr     = sq[7:0];
	wire [15:0] secret = sq[23:8];

	reg [2:0] step = 3'd0;
	reg       done = 1'b0;
	// per variant and step: {{mask[9:0], answer[9:0]}}
	reg [19:0] wrom [0:2047];
	initial $readmemh("want.hex", wrom);
	reg [19:0] wq = 20'd0;
	always @(posedge CLOCK_50) wq <= wrom[{{vr, step}}];
	wire ok = ((sw ^ wq[9:0]) & wq[19:10]) == 10'd0;

	// the code of this step: 3 hidden digits mixed from the secret, then the public check digit
	reg [15:0] c1, c2;
	always @(*)
		case (step)
{kcase}		endcase
	wire [15:0] x1 = secret ^ c1;
	wire [15:0] x2 = x1 + {{x1[10:0], x1[15:11]}};
	wire [15:0] x3 = x2 ^ {{7'd0, x2[15:7]}};
	wire [15:0] x4 = x3 + c2;
	wire [3:0]  chk = x4[15:12] + 4'd3 * x4[11:8] + 4'd5 * x4[7:4] + 4'd7 + 4'd9 * seed[3:0] + 4'd11 * seed[7:4]
	                + 4'd13 * {{2'b00, seed[9:8]}} + 4'd15 * {{1'b0, step}};
	wire [15:0] code = {{x4[15:4], chk}};

	// per variant and input row: 2 bits per output, 00 = 0, 01 = 1, 10 = hold
{stdecl}	wire [N-1:0] row = {{{row}}};
	reg [2*NO-1:0] trom [0:(1 << ({q.vb} + N)) - 1];
	initial $readmemh("table.hex", trom);
	reg [2*NO-1:0] tq = {{2*NO{{1'b0}}}};
	always @(posedge CLOCK_50) tq <= trom[{{{"vr" if q.vb == 8 else f"vr[{q.vb - 1}:0]"}, row}}];

	reg [3:0] settle = 4'd0;			// the ROMs need a few clocks after the PC sends the login
	always @(posedge CLOCK_50)
		if (!go) settle <= 4'd0;
		else if (settle != 4'd15) settle <= settle + 4'd1;

	// steps: KEY2 = check the switches. Right: PASS and the next step (the last one: done, the code).
	reg [25:0] flash = 26'd0;
	reg        good  = 1'b0;			// what the flash shows: PASS or Err
	reg [15:0] last  = 16'd0;
	always @(posedge CLOCK_50) begin
		if (flash != 26'd0) flash <= flash - 26'd1;
		if (!go) begin step <= 3'd0; done <= 1'b0; last <= 16'd0; flash <= 26'd0; end
		else if (settle == 4'd8) step <= start;
		else if (settle == 4'd15 && press2 && !done) begin
			flash <= FLASH; good <= ok;
			if (ok) begin
				if (step == NS - 1) begin done <= 1'b1; last <= code; end
				else step <= step + 3'd1;
			end
		end
		probe <= {{done, step, last}};
	end

	reg [NO-1:0] q = {{NO{{1'b0}}}};
	integer j;
	always @(posedge CLOCK_50)
		if (settle < 4'd4) q <= {{NO{{1'b0}}}};
		else for (j = 0; j < NO; j = j + 1) if (!tq[2*j+1]) q[j] <= tq[2*j];
{clocked}
	function [6:0] seg(input [3:0] x);
		case (x)
{''.join(f"			4'h{i:X}: seg = 7'h{s:02X};{chr(10)}" for i, s in enumerate(SEG))}		endcase
	endfunction
	localparam [6:0] BL = 7'h7F, DA = 7'h3F, CP = 7'h{CH['P']:02X}, CA = 7'h{CH['A']:02X}, CS = 7'h{CH['S']:02X},
	                 CE = 7'h{CH['E']:02X}, CR = 7'h{CH['r']:02X}, CD = 7'h21, CO = 7'h23, CN = 7'h{CH['n']:02X};

	always @(*) begin
		LEDR = sw; LEDG = 8'd0;
		HEX3 = BL; HEX2 = BL; HEX1 = BL; HEX0 = BL;
		if (!go || settle != 4'd15) begin
			HEX3 = DA; HEX2 = DA; HEX1 = DA; HEX0 = DA;		// ---- waiting for the PC
		end else if (flash != 26'd0) begin
			if (good) begin HEX3 = CP; HEX2 = CA; HEX1 = CS; HEX0 = CS; end	// PASS
			else begin HEX3 = CE; HEX2 = CR; HEX1 = CR; end			// Err
		end else if (done) begin
			HEX3 = CD; HEX2 = CO; HEX1 = CN; HEX0 = CE;			// donE
		end else begin
{chr(10).join(leds)}
{chr(10).join(hexes)}
		end
	end
endmodule
"""

def seed_rom(q):
    return "".join(f"{(secret_of(q.id, s) << 8) | var_of(q, s):06X}\n" for s in range(1024))

def want_rom(q):
    lines = []
    for v in range(256):
        for k in range(8):
            want, mask = step_answer(q, q.variants[v], k) if (v < len(q.variants) and 1 <= k < q.ns) else (0, 0x3FF)
            lines.append(f"{(mask << 10) | want:05X}")
    return "\n".join(lines) + "\n"

def table_rom(q):
    no, w = len(q.outs), (2 * len(q.outs) + 3) // 4
    lines = []
    for v in range(1 << q.vb):
        tabs = q.tables(q.variants[v]) if v < len(q.variants) else [[0] * (1 << q.n)] * no
        for r in range(1 << q.n):
            lines.append(f"{sum(tabs[j][r] << (2 * j) for j in range(no)):0{w}X}")
    return "\n".join(lines) + "\n"

def pins():
    top = open("C:/DE10/top.qsf", encoding="utf-8").read().splitlines()
    return [l for l in top if re.search(r"-to (CLOCK_50|SW|KEY|LEDR|LEDG|HEX)", l)]

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def build(q):
    d = f"{HERE}/build/{q.id}"
    for f in ("seed.hex", "table.hex", "want.hex"):
        if os.path.exists(f"{d}/{f}"):
            os.remove(f"{d}/{f}")
    write(f"{d}/ce.v", verilog(q))
    write(f"{d}/seed.hex", seed_rom(q))
    write(f"{d}/want.hex", want_rom(q))
    write(f"{d}/table.hex", table_rom(q))
    write(f"{d}/ce.qpf", 'QUARTUS_VERSION = "13.0"\nPROJECT_REVISION = "ce"\n')
    write(f"{d}/ce.sdc", "create_clock -name CLOCK_50 -period 20 [get_ports CLOCK_50]\n")
    write(f"{d}/ce.qsf", "\n".join([
        f"# Class exercise {q.id} - DE1, Quartus II 13.0sp1",
        'set_global_assignment -name FAMILY "Cyclone II"',
        "set_global_assignment -name DEVICE EP2C20F484C7",
        "set_global_assignment -name TOP_LEVEL_ENTITY ce",
        "set_global_assignment -name VERILOG_FILE ce.v",
        "set_global_assignment -name SDC_FILE ce.sdc",
        "set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files",
        'set_global_assignment -name RESERVE_ALL_UNUSED_PINS "AS INPUT TRI-STATED"',
        'set_global_assignment -name STRATIX_DEVICE_IO_STANDARD "3.3-V LVTTL"'] + pins()) + "\n")
    return d

# ---------------------------------------------------------------- simulation (iverilog)
def play_hex(q, sw, st=None):
    out = []
    for d, spec in zip((3, 2, 1, 0), q.hexes):
        hb = {i[1]: j for j, (kind, i) in enumerate(q.outs) if kind == "H" and i[0] == d}
        mj = [j for j, (kind, i) in enumerate(q.outs) if kind == "M" and i == d]
        if hb:
            out.append(SEG[sum(st[hb[b]] << b for b in hb)])
            continue
        if mj:
            out.append(0x3F if st[mj[0]] else 0x7F)
            continue
        if isinstance(spec, list):
            out.append(SEG[sum(((sw >> s) & 1) << (len(spec) - 1 - i) for i, s in enumerate(spec))])
        else:
            out.append(CH[spec])
    return out

def sw_of_row(q, r, extra=0):
    sw = extra
    for i, s in enumerate(q.inputs):
        sw = (sw & ~(1 << s)) | (((r >> (len(q.inputs) - 1 - i)) & 1) << s)
    return sw

STUB = """// iverilog stand-in for Quartus' altsource_probe: the testbench drives src and reads probe
module altsource_probe #(parameter sld_auto_instance_index = "YES", parameter sld_instance_index = 0,
	parameter instance_id = "CE", parameter probe_width = 20, parameter source_width = 14,
	parameter source_initial_value = "0", parameter enable_metastability = "NO")
	(input [probe_width-1:0] probe, output [source_width-1:0] source);
	reg [source_width-1:0] src = 0;
	assign source = src;
endmodule
"""

def testbench(q, seeds):
    lines = ["`timescale 1ns/1ns", "module tb;", "\treg clk = 0; always #10 clk = ~clk;",
             "\treg [9:0] SW = 0; reg [3:0] KEY = 4'hF;",
             "\twire [9:0] LEDR; wire [7:0] LEDG; wire [6:0] HEX0, HEX1, HEX2, HEX3;",
             "\tce #(.FLASH(26'd30)) dut(.CLOCK_50(clk), .SW(SW), .KEY(KEY), .LEDR(LEDR), .LEDG(LEDG), .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3));",
             "\tinteger fails = 0, checks = 0;",
             "\ttask chk(input [9:0] r, input [7:0] g, input [27:0] h, input [19:0] p, input [8*24:1] what);",
             "\t\tbegin checks = checks + 1;",
             "\t\tif (LEDR !== r || LEDG !== g || {HEX3, HEX2, HEX1, HEX0} !== h || dut.probe !== p) begin fails = fails + 1;",
             "\t\t\tif (fails < 10) $display(\"FAIL %0s: LEDR %b/%b LEDG %b/%b HEX %h/%h probe %h/%h\", what, LEDR, r, LEDG, g, {HEX3, HEX2, HEX1, HEX0}, h, dut.probe, p); end",
             "\t\tend endtask",
             "\ttask press2; begin KEY[2] = 0; repeat (4) @(posedge clk); KEY[2] = 1; repeat (4) @(posedge clk); end endtask",
             "\ttask pressk(input integer k); begin KEY[k] = 0; repeat (4) @(posedge clk); KEY[k] = 1; repeat (4) @(posedge clk); end endtask",
             "\tinitial begin"]
    hexv = lambda h: (h[0] << 21) | (h[1] << 14) | (h[2] << 7) | h[3]
    def chk(r, g, h, p, what):
        lines.append(f"\t\tchk(10'h{r:03X}, 8'h{g:02X}, 28'h{hexv(h):07X}, 20'h{p:05X}, \"{what}\");")
    PASS = [CH["P"], CH["A"], CH["S"], CH["S"]]
    ERR = [CH["E"], CH["r"], CH["r"], 0x7F]
    DONE = [0x21, 0x23, CH["n"], CH["E"]]
    DASH = [0x3F] * 4
    trng = random.Random(hash(q.id) & 0xFFFF)
    for si, s in enumerate(seeds):
        p = q.variants[var_of(q, s)]
        tabs = q.tables(p)
        first = 1 + si % (q.ns - 1)			# resume: the PC sends a later start step
        lines.append(f"\t\t// login {s}, start at step {first}")
        lines.append("\t\tSW = 10'h000; repeat (4) @(posedge clk);")
        chk(0, 0, DASH, 0, f"waiting {s}")
        lines.append(f"\t\tdut.sp.src = 14'h{(1 << 13) | (first << 10) | s:04X}; repeat (24) @(posedge clk);")
        # while the PC sends the login the switches are all down (row 0): a memory box already reacts to that row
        st = [tabs[j][0] if tabs[j][0] != HOLD else 0 for j in range(len(q.outs))]
        rows = list(range(1 << q.n)) + [trng.randrange(1 << q.n) for _ in range(8)] if not q.seq else \
            [trng.randrange(1 << q.n) for _ in range(60)]
        ni, cur, inb, swc = len(q.inputs), 0, 0, 0
        if q.sb:
            rows = [("clk" if x < 5 else "rst" if x == 5 else "sw") for x in (trng.randrange(12) for _ in range(70))]
        for r in rows:
            if q.sb:			# a clocked question: switches, KEY1 (clock) or KEY0 (reset); outputs follow the state
                if r == "sw":
                    inb = trng.randrange(1 << ni)
                    swc = sw_of_row(q, inb, trng.randrange(1024))
                    lines.append(f"\t\tSW = 10'h{swc:03X}; repeat (3) @(posedge clk);")
                elif r == "clk":
                    cur = sum(tabs[j][(cur << ni) | inb] << i for j, (k, i) in enumerate(q.outs) if k == "N")
                    lines.append("\t\tpressk(1);")
                else:
                    cur = 0
                    lines.append("\t\tpressk(0);")
                r = (cur << ni) | inb
                sw = swc
            else:
                sw = sw_of_row(q, r, trng.randrange(1024))
            for j in range(len(q.outs)):
                if tabs[j][r] != HOLD:
                    st[j] = tabs[j][r]
            ledr = sw
            for j, (k, i) in enumerate(q.outs):
                if k == "R":
                    ledr = (ledr & ~(1 << i)) | (st[j] << i)
            ledg = sum(st[j] << i for j, (k, i) in enumerate(q.outs) if k == "G")
            lines.append(f"\t\tSW = 10'h{sw:03X}; repeat (5) @(posedge clk);")
            chk(ledr, ledg, play_hex(q, sw, st), first << 16, f"play {s} row {r}")
        if q.sb:			# back to reset before the steps (the state does not matter for them)
            lines.append("\t\tpressk(0);")
        for k in range(first, q.ns):
            want, mask = step_answer(q, p, k)
            good = want | (trng.randrange(1024) & ~mask)
            bad = good ^ (mask & -mask)
            final = k == q.ns - 1
            lines.append(f"\t\tSW = 10'h{bad:03X}; repeat (5) @(posedge clk); press2;")
            chk(bad, 0, ERR, k << 16, f"err {s} step {k}")
            lines.append("\t\trepeat (40) @(posedge clk);")
            lines.append(f"\t\tSW = 10'h{good:03X}; repeat (5) @(posedge clk); press2;")
            c = code_of(q.id, s, k)
            cv = (c[0] << 12) | (c[1] << 8) | (c[2] << 4) | c[3]
            pr = (1 << 19) | (k << 16) | cv if final else (k + 1) << 16
            lines.append("\t\trepeat (2) @(posedge clk);")
            chk(good, 0, PASS, pr, f"pass {s} step {k}")
            lines.append("\t\trepeat (40) @(posedge clk);")
            if final:
                chk(good, 0, DONE, pr, f"done {s}")
        lines.append("\t\tdut.sp.src = 14'h0000; repeat (6) @(posedge clk);")
    lines += ["\t\t$display(\"%0s: %0d checks, %0d fails\", \"" + q.id + "\", checks, fails);", "\t\t$finish;", "\tend", "endmodule"]
    return "\n".join(lines) + "\n"

def simulate(q, d):
    seeds, pubs = [], set()
    srng = random.Random(7)
    while len(seeds) < 6 or (len(pubs) < q.npub and len(seeds) < 12):
        s = srng.randrange(1024)
        p = pub_of(q.id, s, q.npub)
        if len(seeds) < 6 or p not in pubs:
            seeds.append(s); pubs.add(p)
    write(f"{d}/tb.v", testbench(q, seeds))
    write(f"{d}/stub_issp.v", STUB)
    r = subprocess.run([f"{IVL}/iverilog", "-o", "sim.vvp", "tb.v", "ce.v", "stub_issp.v"], cwd=d, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr); return False
    r = subprocess.run([f"{IVL}/vvp", "-n", "sim.vvp"], cwd=d, capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    print("   ", "\n    ".join(l for l in out if "FAIL" in l or "checks" in l))
    return any(re.search(r"checks, 0 fails", l) for l in out)

def compile_q(q, d):
    r = subprocess.run([f"{QBIN}/quartus_sh.exe", "--flow", "compile", "ce"], cwd=d, capture_output=True, text=True)
    open(f"{d}/compile.log", "w").write(r.stdout + r.stderr)
    if r.returncode:
        print(f"    {q.id}: COMPILE FAILED - {d}/compile.log"); return False
    rpt = open(f"{d}/output_files/ce.fit.summary").read()
    le = re.search(r"Total logic elements : ([\d,]+)", rpt).group(1)
    mem = re.search(r"Total memory bits : ([\d,]+)", rpt).group(1)
    os.makedirs(f"{REPO}/sof", exist_ok=True)
    shutil.copy(f"{d}/output_files/ce.sof", f"{REPO}/sof/{q.id}.sof")
    print(f"    {q.id}: compiled, {le} LEs, {mem} memory bits -> sof/{q.id}.sof")
    return True

# ---------------------------------------------------------------- the student's files
# ---------------------------------------------------------------- switch positions as bits on the screens
_BIT = {"down": "0", "up": "1"}
def bitwords(line):
    """The teacher's rule: a switch position is written as a bit - down = 0, up = 1 (00, 01, SW9 = 1, all 0 ...).
    Only switch positions change; the legend '(0 = down, 1 = up)' and words like 'Up / Down' (arrow keys) stay."""
    b = lambda w: _BIT[w.lower()]
    line = re.sub(r"\b(down|up)-(down|up)\b", lambda m: b(m.group(1)) + b(m.group(2)), line, flags=re.I)
    line = re.sub(r"(=\s*)((?:(?:down|up)\s+){1,3}(?:down|up))\b",
                  lambda m: m.group(1) + "".join(b(w) for w in m.group(2).split()), line, flags=re.I)
    line = re.sub(r"\b(all|both) (down|up)\b", lambda m: m.group(1) + " " + b(m.group(2)), line, flags=re.I)
    line = re.sub(r"\b(SW\d\.\.SW\d)\s+(down|up)\b", lambda m: m.group(1) + " = all " + b(m.group(2)), line, flags=re.I)
    line = re.sub(r"\b(SW[\di]+)\s*=\s*(down|up)\b", lambda m: m.group(1) + " = " + b(m.group(2)), line, flags=re.I)
    line = re.sub(r"\b(SW[\di]+),?\s+(down|up)\b(?!\s*/)", lambda m: m.group(1) + " = " + b(m.group(2)), line, flags=re.I)
    return line

def questions_txt():
    out = ["# Class exercise - the questions (written by C:/DE10/solutions/class_exercise/gen.py, do not edit).",
           "# [Qnn] NAME | title | npub n [| steps n];  B: board;  Pk: printed for login numbers with pub = k;",
           "# with steps: Sk: the screen of step k (step 0 = login, in run.ps1);  without: L: question, F: answer format", ""]
    for q in [q for q in QS if q.id.startswith("Q")]:
        out.append(f"[{q.id}] {q.name} | {q.title} | npub {q.npub}" + (f" | steps {q.ns}" if q.ns else "") + (" | flat" if q.flat else ""))
        out += [f"B: {bitwords(l)}" for l in q.B]
        for k in sorted(q.P):
            out += [f"P{k}: {bitwords(l)}" for l in q.P[k]]
        if q.ns:
            for k, (lines, _) in enumerate(q.steps, 1):
                out += [f"S{k}: {bitwords(l)}" for l in lines]
        else:
            out += [f"L: {l}" for l in q.L] + [f"F: {l}" for l in q.F]
        out.append("")
    return "\n".join(out)

BAT = """@echo off
rem ============================================================
rem  Class exercise - {id}: {title}
rem  Programs the board with this question, tells you your login
rem  number and the question. The board checks your answer and
rem  shows a code - type it here, it goes into moodle.txt.
rem ============================================================
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "tools{bs}run.ps1" -Only {id}
echo.
pause
"""

def sw_up(want, mask):
    up = [f"SW{i}" for i in range(9, -1, -1) if mask >> i & 1 and want >> i & 1]
    return " + ".join(up) if up else "all down"

def questions_md(sid=None):
    """class_exercise/QUESTIONS.md: every question by lesson topic - what the board holds, the switches, the personal data,
    and every step in full (no answers). Written on every run, so it always matches the screens.
    With sid: the instructor's copy with the answers of that student (QUESTIONS_ANSWERS.md in this folder)."""
    import re as _re
    topics = []
    for l in open(f"{REPO}/lesson.txt", encoding="utf-8").read().splitlines():
        m = _re.match(r"^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$", l)
        if m:
            topics.append((m.group(1), m.group(2), m.group(3).split()))
    he = lambda t: any("\u0590" <= c <= "\u05ff" for c in t)
    fmt = lambda t: t if he(t) else f"`{t}`"
    s_ = login_of(sid) if sid else None
    if sid:
        out = ["# פירוט השאלות לפי נושא - עם התשובות (למרצה בלבד)", "",
               f"התשובות של הסטודנט `{sid}` (מספר כניסה {s_}). לכל סטודנט מספרים אחרים - לסטודנט אחר:",
               "`python gen.py --answers <ID>`  או  `answers.bat ce <ID>`.", ""]
    else:
        out = ["# פירוט השאלות לפי נושא", "",
               "נוצר אוטומטית מ-`gen.py` - כל שאלה כפי שהיא מופיעה על המסך, בלי התשובות. מסודר לפי הנושאים של השיעור (`lesson.txt`).", ""]
    for i, (mins, name, qids) in enumerate(topics, 1):
        out += [f"## נושא {i} - {name}", "", f"{mins} דקות, {len(qids)} שאלות: {qids[0]}-{qids[-1]}", ""]
        for qid in qids:
            q = QBY[qid]
            data = [l for l in q.B if he(l)]
            legend = [l for l in q.B if not he(l)]
            out += [f"### {q.id} - {q.title}", ""]
            if data:
                out.append("- **על הלוח:** " + " ".join(data))
            out.append("- **מתגים ונורות:** " + " ; ".join(f"`{l}`" for l in legend))
            p_ = q.variants[var_of(q, s_)] if sid else None
            if q.P:
                ex = q.P[pub_of(q.id, s_, q.npub)] if sid else q.P[0]
                out.append(("- **הנתון האישי שלו:** " if sid else "- **נתון אישי** (לכל סטודנט אחר, לפי מספר הסטודנט), למשל: ")
                           + " ; ".join(fmt(l) for l in ex))
            if sid:
                out.append(f"- **מה מוסתר בלוח:** `{q.describe(p_)}`")
            out.append(f"- **שלבים:** {q.ns - 1}")
            out.append("")
            for k, (lines, _) in enumerate(q.steps, 1):
                out.append(f"**שלב {k}**")
                out.append("")
                for l in lines:
                    out.append("- (הנתון האישי של הסטודנט)" if l == "@P" else f"- {fmt(l.strip())}")
                if sid:
                    w_, m_ = step_answer(q, p_, k)
                    out.append(f"- **התשובה:** `{sw_up(w_, m_)}`")
                out.append("")
    return "\n".join(out) + "\n"

EXPLAIN_FILE = f"{HERE}/explain.py"		# gen_w2.py points it to explain_w2.py
def answers_guide(sid):
    """The instructor's guide (instructor_guide/guide.html, never given to students): a table of the questions with the
    part of lecture 3 and the slides they cover, then every question - what it teaches, what the board holds, and for each
    step the task, how the right answer is found, and the answer of student sid as an example."""
    import html as _h, re as _re
    ns = {}
    exec(open(EXPLAIN_FILE, encoding="utf-8").read(), ns)
    TEACH, EXPLAIN, SLIDES, NOT_COVERED = ns["TEACH"], ns["EXPLAIN"], ns["SLIDES"], ns["NOT_COVERED"]
    s_ = login_of(sid)
    topics = []
    for l in open(f"{REPO}/lesson.txt", encoding="utf-8").read().splitlines():
        m = _re.match(r"^\s*TOPIC\s+([\d.]+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*$", l)
        if m:
            topics.append((m.group(1), m.group(2), m.group(3).split()))
    he = lambda t: any("\u0590" <= c <= "\u05ff" for c in t)
    esc = _h.escape
    show = lambda t: esc(t) if he(t) else f'<code dir="ltr">{esc(t)}</code>'
    o = ['<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>מדריך למרצה - תרגיל כיתה, הרצאה ' + LECTURE + '</title>',
         '<style>body{font-family:Arial,sans-serif;max-width:1100px;margin:24px auto;padding:0 16px;line-height:1.5;color:#222}'
         'h1{font-size:26px}h2{margin-top:36px;border-bottom:2px solid #36c;padding-bottom:4px}h3{margin-top:28px;color:#235}'
         'table{border-collapse:collapse;width:100%;margin:12px 0}td,th{border:1px solid #bbb;padding:5px 8px;vertical-align:top}'
         'th{background:#e8eef8}code{background:#f2f2f2;padding:1px 4px;border-radius:3px;font-size:92%;unicode-bidi:embed}'
         '.step{border:1px solid #ddd;border-radius:6px;padding:8px 12px;margin:10px 0;background:#fcfcfc}'
         '.ans{background:#eaf7ea;border-right:4px solid #3a3;padding:6px 10px;margin-top:6px}'
         '.how{background:#fff7e0;border-right:4px solid #e90;padding:6px 10px;margin-top:6px}'
         '.small{color:#666;font-size:90%}</style></head><body>',
         '<h1>מדריך למרצה - תרגיל הכיתה של הרצאה ' + LECTURE + '</h1>',
         f'<p class="small">נוצר אוטומטית מ-<code>gen.py</code>. לא מגיע לסטודנטים. התשובות לדוגמה הן של הסטודנט '
         f'<code>{esc(sid)}</code> (מספר כניסה {s_}); לכל סטודנט מספרים אחרים - לסטודנט אחר: '
         f'<code>python gen.py --answers &lt;ID&gt;</code> או <code>answers.bat ce &lt;ID&gt;</code>.</p>',
         '<h2>אילו שאלות מכסות איזה חלק בהרצאה</h2>',
         '<table><tr><th>נושא בשיעור</th><th>שאלה</th><th>שם</th><th>החלק בהרצאה ' + LECTURE + '</th><th>שקופיות</th></tr>']
    for i, (mins, name, qids) in enumerate(topics, 1):
        for j, qid in enumerate(qids):
            q = QBY[qid]
            part, sl = SLIDES[q.name]
            cell = f'<td rowspan="{len(qids)}">{i}. {esc(name)}<br><span class="small">{mins} דקות</span></td>' if j == 0 else ""
            o.append(f'<tr>{cell}<td><a href="#{q.id}">{q.id}</a></td><td>{esc(q.title)}</td><td>{esc(part)}</td>'
                     f'<td dir="ltr" style="text-align:right">{sl}</td></tr>')
    o.append('</table>')
    o.append('<p><b>שקופיות בטווח (1, 3-106) שאין להן שאלה ישירה:</b></p><ul>')
    o += [f'<li><span dir="ltr">{a}</span> - {esc(b)}</li>' for a, b in NOT_COVERED]
    o.append('</ul>')
    for i, (mins, name, qids) in enumerate(topics, 1):
        o.append(f'<h2>נושא {i}: {esc(name)}</h2>')
        for qid in qids:
            q = QBY[qid]
            p_ = q.variants[var_of(q, s_)]
            ex = EXPLAIN[q.name]
            assert len(ex) == q.ns - 1, (q.name, len(ex), q.ns - 1)
            part, sl = SLIDES[q.name]
            o.append(f'<h3 id="{q.id}">{q.id} - {esc(q.title)}</h3>')
            o.append(f'<p><b>מה השאלה מלמדת:</b> {esc(TEACH[q.name])}<br>'
                     f'<b>בהרצאה:</b> {esc(part)}, שקופיות <span dir="ltr">{sl}</span><br>'
                     f'<b>מתגים ונורות:</b> ' + " ".join(show(l) for l in q.B) + '</p>')
            mine = q.P.get(pub_of(q.id, s_, q.npub), []) if q.P else []
            if mine:
                o.append('<p><b>הנתון האישי של הסטודנט לדוגמה:</b> ' + " ".join(show(l) for l in mine) + '</p>')
            o.append(f'<p><b>מה מוסתר בלוח שלו:</b> <code dir="ltr">{esc(q.describe(p_))}</code></p>')
            for k, (lines, _) in enumerate(q.steps, 1):
                task = [l for l in lines if l != "@P"]
                w_, m_ = step_answer(q, p_, k)
                o.append(f'<div class="step"><b>שלב {k}</b><br>' + "<br>".join(show(l) for l in task) +
                         f'<div class="how"><b>איך מגיעים לתשובה:</b> {esc(ex[k - 1])}</div>'
                         f'<div class="ans"><b>התשובה של הסטודנט לדוגמה:</b> <code dir="ltr">{esc(sw_up(w_, m_))}</code></div></div>')
    o.append('</body></html>')
    return "\n".join(o) + "\n"

def write_repo():
    """The student folder gets the questions file only: questions open through LESSON.bat, never one by one
    (no Qnn BATs; run.ps1 refuses to run without the lesson). Instructor: question.bat <Qnn> in this folder."""
    write(f"{REPO}/questions.txt", questions_txt())
    write(f"{REPO}/QUESTIONS.md", questions_md())
    for f in os.listdir(REPO):
        if re.match(r"Q\d\d_.*\.bat$", f):
            os.remove(f"{REPO}/{f}")

def answers_md():
    out = ["# Class exercise - answer key (instructor only)", "",
           "Per student: `python gen.py --id <ID>` (login number, every answer as switches, every code).",
           "Codes: `C:/DE10/solutions/verify.bat <folder>` (lines `ce-Qnn: XXXX` in moodle.txt).", ""]
    for q in QS:
        out += [f"## {q.id} {q.name} - {q.title}", "", f"{len(q.variants)} variants (npub {q.npub} x nsec {q.nsec}); "
                f"fewest different answers per printed text: {check_question(q)}."
                + (f" In {q.ns} steps (0 = login)." if q.ns else " One step (first format)."), ""]
        if q.ns:
            out += [f"- step {k}: " + " ".join(lines) for k, (lines, _) in enumerate(q.steps, 1)]
        else:
            out += [f"- answer: {l}" for l in q.F]
        out.append(f"- example variant 0: {q.describe(q.variants[0])} -> SW = {q.answer(q.variants[0])[0]:010b}")
        out.append("")
    return "\n".join(out)

def show_id(sid):
    s = login_of(sid)
    print(f"ID {sid}: login number {s} = SW9..0 {s:010b} (hex {s:03X})")
    for q in QS:
        p = q.variants[var_of(q, s)]
        if q.ns:
            print(f"{q.id} {q.name:9} in steps - final code {final_code(q, s)}   (step 0 receipt {code_str(q.id, s, 0)})")
            for k in range(1, q.ns):
                want, mask = step_answer(q, p, k)
                print(f"      step {k}: answer {want:010b} (mask {mask:03X})  code {code_str(q.id, s, k)}")
        else:
            want, mask = q.answer(p)
            sw = " ".join(f"SW{i}" for i in range(9, -1, -1) if want >> i & 1) or "(all down)"
            print(f"{q.id} {q.name:9} code {final_code(q, s)}  answer {want:010b} (mask {mask:03X}) up: {sw}")
        print(f"      {q.describe(p)}")

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--id")
    ap.add_argument("--nosim", action="store_true")
    ap.add_argument("--answers", default="316009489", help="the student whose answers go into QUESTIONS_ANSWERS.md")
    a = ap.parse_args()
    if a.id:
        show_id(a.id); sys.exit(0)
    for q in QS:
        check_question(q)
    sel = [QBY[a.only]] if a.only else [q for q in QS if q.id.startswith("Q")]
    bad = []
    for q in sel:
        if not q.ns:
            print(f"{q.id}: first format (no steps) - its sof stays as built by gen_v1.py.bak"); continue
        d = build(q)
        print(f"{q.id} {q.name}: {len(q.variants)} variants, {q.ns} steps")
        if not a.nosim and not simulate(q, d):
            bad.append(q.id); continue
        if a.compile and not compile_q(q, d):
            bad.append(q.id)
    write_repo()
    write(f"{HERE}/ANSWERS.md", answers_md())
    write(f"{HERE}/QUESTIONS_ANSWERS.md", questions_md(a.answers))
    write(f"{HERE}/instructor_guide/guide.html", answers_guide(a.answers))
    print("FAILED: " + " ".join(bad) if bad else "all OK")
    sys.exit(1 if bad else 0)
