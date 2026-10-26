# Week 4 boards and secrets for ex8..ex10 (instructor only).  python gen_w4.py [--compile]
# Writes, for week4 ex8 (critical path), ex9 (glitches), ex10 (case / casez):
#   C:/DE10/solutions/week4/exN/board/board.v + board.qpf + board.qsf   (the hidden board source)
#   C:/DE10/week4/exN/tools/secrets.txt   (question pools + hashes of the right answers - no answers in clear)
#   C:/DE10/week4/exN/tools/puzzles.txt   (what the student may see: delays, casez code, keys of the casez bits)
#   C:/DE10/solutions/week4/exN/ANSWERS.md + key.json
# --compile: Quartus 13.0sp1 builds every board and copies board.sof into the repo.
# Fixed seed: running it again gives the same boards and secrets.
import hashlib, json, os, random, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SOL = "C:/DE10/solutions/week4"
REPO = "C:/DE10/week4"
QBIN = "C:/altera/13.0sp1/quartus/bin64"
rng = random.Random(20261006)

def H(s):
    return hashlib.sha256(("DE10w2|" + s).encode("ascii")).hexdigest()[:10]

SEG = ["1000000", "1111001", "0100100", "0110000", "0011001", "0010010", "0000010", "1111000",
       "0000000", "0010000", "0001000", "0000011", "1000110", "0100001", "0000110", "0001110"]
LIB = """
// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(input [3:0] x, output reg [6:0] seg);
	always @(*) case (x)
""" + "".join(f"\t\t4'h{i:X}: seg = 7'b{s};\n" for i, s in enumerate(SEG)) + """\t\tdefault: seg = 7'b1111111;
	endcase
endmodule

// One pulse of one clock every 0.1 s (50 MHz): the "tick" of the slow-motion circuits
module tick10(input clk, output reg t);
	reg [22:0] c = 23'd0;
	always @(posedge clk) begin
		t <= (c == 23'd4999999);
		c <= (c == 23'd4999999) ? 23'd0 : c + 23'd1;
	end
endmodule

// A gate output in slow motion: y follows x d ticks later (d = 1..15), pulses included
module dly(input clk, input t, input x, input [3:0] d, output y);
	reg [14:0] h = 15'd0;
	always @(posedge clk) if (t) h <= {h[13:0], x};
	assign y = h[d - 4'd1];
endmodule

// Stopwatch: ticks since the last input change, at the first and at the last change of y; n = changes of y
module watch(input clk, input t, input changed, input y, output reg [6:0] first, output reg [6:0] last, output reg [3:0] n);
	reg [6:0] c = 7'd0;
	reg yp = 1'b0;
	always @(posedge clk) if (t) begin
		yp <= y;
		if (changed) begin c <= 7'd0; first <= 7'd0; last <= 7'd0; n <= 4'd0; end
		else begin
			if (c != 7'd99) c <= c + 7'd1;
			if (y != yp) begin
				if (n == 4'd0) first <= c;
				last <= c;
				if (n != 4'd15) n <= n + 4'd1;
			end
		end
	end
endmodule

// 0..99 on two digits
module dec2(input [6:0] v, output [6:0] tens, output [6:0] ones);
	hex7seg ht(.x(v / 7'd10), .seg(tens));
	hex7seg ho(.x(v % 7'd10), .seg(ones));
endmodule
"""
PORTS = """	input        CLOCK_50,
	input  [9:0] SW,
	input  [3:0] KEY,
	output [9:0] LEDR,
	output [7:0] LEDG,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3"""

top = open("C:/DE10/top.qsf", encoding="utf-8").read().splitlines()
pins = [l for l in top if re.search(r"-to (SW|KEY|LEDR|LEDG|HEX|CLOCK_50)", l)]

def write(path, text, nl="\n"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline=nl) as f:
        f.write(text)

def board(ex, title, body):
    v = f"// week 4 {ex} board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.\n" \
        f"// {title}\nmodule board(\n{PORTS}\n\t);\n{body}endmodule\n{LIB}"
    d = f"{SOL}/{ex}/board"
    write(f"{d}/board.v", v)
    write(f"{d}/board.qpf", 'QUARTUS_VERSION = "13.0"\nPROJECT_REVISION = "board"\n')
    q = ['# week 4 ' + ex + ' board - DE1, Quartus II 13.0sp1',
         'set_global_assignment -name FAMILY "Cyclone II"',
         'set_global_assignment -name DEVICE EP2C20F484C7',
         'set_global_assignment -name TOP_LEVEL_ENTITY board',
         'set_global_assignment -name VERILOG_FILE board.v',
         'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files',
         'set_global_assignment -name RESERVE_ALL_UNUSED_PINS "AS INPUT TRI-STATED"',
         'set_global_assignment -name STRATIX_DEVICE_IO_STANDARD "3.3-V LVTTL"'] + pins
    write(f"{d}/board.qsf", "\n".join(q) + "\n")
    write(f"{d}/board.sdc", "create_clock -name CLOCK_50 -period 20.000 [get_ports CLOCK_50]\n")

def secrets(ex, pools, ok):
    key = {}
    for item, ans in ok:
        key.setdefault(item, ans)
    write(f"{SOL}/{ex}/key.json", json.dumps(key, indent=0))
    lines = [f"# {ex}: question pools, and hashes of the right answers (made by the instructor's gen_w4.py - do not edit)"]
    for name, items in pools.items():
        lines.append(f"pool {name} " + " ".join(items))
    hs = sorted(set(H(f"w4-{ex}|{item}|{ans}") for item, ans in ok))
    for i in range(0, len(hs), 8):
        lines.append("ok " + " ".join(hs[i:i + 8]))
    write(f"{REPO}/{ex}/tools/secrets.txt", "\n".join(lines) + "\n", "\r\n")

# ---------------------------------------------------------------- SOP keys: truth table + cost
def sop_key(terms, vars_):
    """terms: list of dicts var->1/0. Key = hex truth table (row i: vars_[0] is the MSB) + ' terms/literals'."""
    n = len(vars_); tt = 0
    for i in range(2 ** n):
        val = {v: (i >> (n - 1 - k)) & 1 for k, v in enumerate(vars_)}
        if any(all(val[v] == b for v, b in t.items()) for t in terms):
            tt |= 1 << i
    lits = sum(len(t) for t in terms)
    return f"{tt:0{max(1, (2 ** n) // 4)}X} {len(terms)}/{lits}"

def term_str(t):
    return "".join(v + ("" if b else "'") for v, b in sorted(t.items()))

# ================================================================= ex8: critical path
# n1 = A AND B,  n2 = NOT C,  n3 = n1 OR n2,  Y = n3 AND D.  Every gate of a type has the same hidden delay.
P8 = []
while len(P8) < 8:
    a, o, n = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
    if len({a, o, n}) < 3 or 2 * a == n + a:       # all different; and the two long paths differ
        continue
    if (a, o, n) in P8:
        continue
    P8.append((a, o, n))
case8 = "".join(f"\t\t\t3'd{p}: begin dA = 4'd{a}; dO = 4'd{o}; dN = 4'd{n}; end\n" for p, (a, o, n) in enumerate(P8))
board("ex8", "Critical path: n1 = A AND B, n2 = NOT C, n3 = n1 OR n2, Y = n3 AND D in slow motion (1 tick = 0.1 s). "
      "Puzzle SW9..7 picks the hidden gate delays. HEX3..2 = ticks to the LAST change of Y, HEX1..0 = to the FIRST.", f"""
	wire clk = CLOCK_50;
	wire t;
	tick10 tk(.clk(clk), .t(t));

	// the inputs, sampled every tick: {{puzzle, D, C, B, A}}
	wire [6:0] now = {{SW[9:7], SW[3:0]}};
	reg  [6:0] in = 7'd0;
	always @(posedge clk) if (t) in <= now;
	wire changed = (now != in);
	wire A = in[0], B = in[1], C = in[2], D = in[3];
	wire [2:0] p = in[6:4];

	reg [3:0] dA, dO, dN;
	always @(*) begin
		case (p)
{case8}			default: begin dA = 4'd1; dO = 4'd1; dN = 4'd1; end
		endcase
	end

	wire n1, n2, n3, Y;
	dly g1(.clk(clk), .t(t), .x(A & B),   .d(dA), .y(n1));
	dly g2(.clk(clk), .t(t), .x(~C),      .d(dN), .y(n2));
	dly g3(.clk(clk), .t(t), .x(n1 | n2), .d(dO), .y(n3));
	dly g4(.clk(clk), .t(t), .x(n3 & D),  .d(dA), .y(Y));

	wire [6:0] first, last;
	wire [3:0] n;
	watch w(.clk(clk), .t(t), .changed(changed), .y(Y), .first(first), .last(last), .n(n));

	assign LEDG = {{7'b0, Y}};
	assign LEDR = {{6'b0, n}};
	dec2 dl(.v(last), .tens(HEX3), .ones(HEX2));
	dec2 df(.v(first), .tens(HEX1), .ones(HEX0));
""")
ok8 = []
for p, (a, o, n) in enumerate(P8):
    ok8.append((f"gates{p}", f"{a} {o} {n}"))
    tpd = max(2 * a + o, n + o + a); tcd = a
    ok8.append((f"tpd{p}", f"{tpd} {tcd}"))
secrets("ex8", {"p": [str(p) for p in range(8)]}, ok8)
write(f"{SOL}/ex8/ANSWERS.md", "# week 4 ex8 - critical path: hidden delays (ticks)\n\n"
      "Circuit: n1 = A AND B, n2 = NOT C, n3 = n1 OR n2, Y = n3 AND D.  Paths: A/B: AND+OR+AND, C: NOT+OR+AND, D: AND.\n\n"
      "| puzzle | AND | OR | NOT | tpd (critical) | tcd (D) | critical inputs |\n|---|---|---|---|---|---|---|\n" +
      "".join(f"| {p} | {a} | {o} | {n} | {max(2*a+o, n+o+a)} | {a} | {'A B' if 2*a+o > n+o+a else 'C'} |\n" for p, (a, o, n) in enumerate(P8)) +
      "\nMeasure AND: flip D with n3 = 1 (A=B=1 or C=0).  A/B path: B=1 (or A=1), C=1, D=1, flip A.  C path: A or B = 0, D=1, flip C.\n"
      "The paper questions (Q3, Q4) are computed in tools/questions.ps1: `answers.bat w4-ex8 <ID>`.\n")

# ================================================================= ex9: glitches
# Y = L1 V' + V L2 (+ L1 L2 when SW6 is up).  The NOT of V is a real gate (slow); L1 / L2 come in both polarities (free).
P9 = []; seen = set()
while len(P9) < 8:
    V = rng.randrange(3)
    others = [i for i in range(3) if i != V]
    rng.shuffle(others)
    l1, l2 = others
    s1, s2 = rng.randrange(2), rng.randrange(2)      # 1 = the literal is the variable itself, 0 = its NOT
    dn, da, do = rng.randint(2, 6), rng.randint(2, 5), rng.randint(1, 4)
    k = (V, l1, l2, s1, s2)
    if k in seen:
        continue
    seen.add(k); P9.append(dict(V=V, l1=l1, l2=l2, s1=s1, s2=s2, dn=dn, da=da, do=do))
VN = "ABC"
case9 = ""
for p, z in enumerate(P9):
    case9 += (f"\t\t\t3'd{p}: begin v = in[{z['V']}]; l1 = {'' if z['s1'] else '~'}in[{z['l1']}]; l2 = {'' if z['s2'] else '~'}in[{z['l2']}]; "
              f"dN = 4'd{z['dn']}; dA = 4'd{z['da']}; dO = 4'd{z['do']}; end\n")
board("ex9", "Glitches: a hidden Y = L1 V' + V L2 in slow motion (1 tick = 0.1 s), puzzle SW9..7; SW6 up adds the term L1 L2. "
      "HEX3..2 = ticks to the LAST change of Y, HEX1..0 = to the FIRST, LEDR3..0 = how many times Y changed.", f"""
	wire clk = CLOCK_50;
	wire t;
	tick10 tk(.clk(clk), .t(t));

	// the inputs, sampled every tick: {{puzzle, fix, C, B, A}}
	wire [6:0] now = {{SW[9:6], SW[2:0]}};
	reg  [6:0] in = 7'd0;
	always @(posedge clk) if (t) in <= now;
	wire changed = (now != in);
	wire fix = in[3];
	wire [2:0] p = in[6:4];

	reg v, l1, l2;
	reg [3:0] dN, dA, dO;
	always @(*) begin
		case (p)
{case9}			default: begin v = 1'b0; l1 = 1'b0; l2 = 1'b0; dN = 4'd1; dA = 4'd1; dO = 4'd1; end
		endcase
	end

	wire vn, n1, n2, n3, Y;
	dly g0(.clk(clk), .t(t), .x(~v),            .d(dN), .y(vn));
	dly g1(.clk(clk), .t(t), .x(l1 & vn),       .d(dA), .y(n1));
	dly g2(.clk(clk), .t(t), .x(v & l2),        .d(dA), .y(n2));
	dly g3(.clk(clk), .t(t), .x(l1 & l2 & fix), .d(dA), .y(n3));
	dly g4(.clk(clk), .t(t), .x(n1 | n2 | n3),  .d(dO), .y(Y));

	wire [6:0] first, last;
	wire [3:0] n;
	watch w(.clk(clk), .t(t), .changed(changed), .y(Y), .first(first), .last(last), .n(n));

	assign LEDG = {{7'b0, Y}};
	assign LEDR = {{6'b0, n}};
	dec2 dl(.v(last), .tens(HEX3), .ones(HEX2));
	dec2 df(.v(first), .tens(HEX1), .ones(HEX0));
""")
ok9 = []; md9 = ""
for p, z in enumerate(P9):
    Vv, L1v, L2v = VN[z['V']], VN[z['l1']], VN[z['l2']]
    t1 = {L1v: z['s1'], Vv: 0}; t2 = {Vv: 1, L2v: z['s2']}; cons = {L1v: z['s1'], L2v: z['s2']}
    ok9.append((f"sop{p}", sop_key([t1, t2], "ABC")))
    ok9.append((f"fix{p}", sop_key([cons], "ABC")))
    before = {Vv: 1, L1v: z['s1'], L2v: z['s2']}
    ok9.append((f"glitch{p}", f"{z['V']} {before['A']}{before['B']}{before['C']}"))
    md9 += (f"| {p} | Y = {term_str(t1)} + {term_str(t2)} | SW{z['V']} ({Vv}) falls from ABC = {before['A']}{before['B']}{before['C']} | "
            f"{term_str(cons)} | {z['dn']} {z['da']} {z['do']} | {z['da'] + z['do']} -> {z['dn'] + z['da'] + z['do']} |\n")
secrets("ex9", {"p": [str(p) for p in range(8)]}, ok9)
k9 = json.load(open(f"{SOL}/ex9/key.json"))
for p, z in enumerate(P9):
    Vv, L1v, L2v = VN[z['V']], VN[z['l1']], VN[z['l2']]
    k9[f"expr|sop{p}"] = term_str({L1v: z['s1'], Vv: 0}) + " + " + term_str({Vv: 1, L2v: z['s2']})
    k9[f"expr|fix{p}"] = term_str({L1v: z['s1'], L2v: z['s2']})
write(f"{SOL}/ex9/key.json", json.dumps(k9, indent=0))
write(f"{SOL}/ex9/ANSWERS.md", "# week 4 ex9 - glitches: the hidden functions\n\n"
      "| puzzle | Y (minimal SOP) | the glitch | fix term | NOT AND OR delays | first -> last |\n|---|---|---|---|---|---|\n" + md9 +
      "\nThe glitch: V falls while both other literals are 1 - V L2 turns off after AND+OR, L1 V' turns on only after NOT+AND+OR.\n"
      "V rising gives no glitch (the slow term turns off after the fast one turned on). SW6 up adds L1 L2: no glitch.\n")
# what the student may see: the delays of each puzzle (the functions stay hidden)
write(f"{REPO}/ex9/tools/puzzles.txt", "# ex9: gate delays of every puzzle, in ticks (1 tick = 0.1 s): puzzle NOT AND OR\n" +
      "".join(f"delay {p} {z['dn']} {z['da']} {z['do']}\n" for p, z in enumerate(P9)), "\r\n")

# ================================================================= ex10: case / casez
def match(pat, a):
    return all(c == '?' or int(c) == (a >> (3 - i)) & 1 for i, c in enumerate(pat))

def analyse10(lines):
    hits = [0] * len(lines); y = []; dflt = 0
    for a in range(16):
        for i, (pat, val) in enumerate(lines):
            if match(pat, a):
                hits[i] += 1; y.append(val); break
        else:
            dflt += 1; y.append(0)
    return hits, y, dflt

from kmin import analyse as kmin_analyse, fmt as kmin_fmt
def fmt_term(c):
    return kmin_fmt(c, "ABCD")
P10 = []
while len(P10) < 16:
    L = rng.choice([4, 5])
    lines = []
    for i in range(L):
        q = rng.choice([1, 2, 2, 3])
        pat = [rng.choice("01") for _ in range(4)]
        for j in rng.sample(range(4), q):
            pat[j] = '?'
        lines.append(("".join(pat), rng.randint(1, 15)))
    hits, y, dflt = analyse10(lines)
    if sum(h == 0 for h in hits) != 1 or hits[0] == 0 or not (1 <= dflt <= 6):
        continue
    if len(set(p for p, v in lines)) != L or len(set(v for p, v in lines)) != L:
        continue
    # every bit of y must be a real function (not constant) with a minimal SOP of 2..4 terms
    costs = []
    for b in range(4):
        ones = [a for a in range(16) if (y[a] >> b) & 1]
        if not ones or len(ones) == 16:
            break
        _, _, best, cov = kmin_analyse(set(ones), set(), 4, False)
        if not (2 <= best[0] <= 4):
            break
        costs.append((ones, best))
    else:
        P10.append(dict(lines=lines, y=y, dflt=dflt, shadow=hits.index(0) + 1, bits=costs))
case10 = ""
for p, z in enumerate(P10):
    case10 += f"\t\t\t4'd{p}:\n\t\t\t\tcasez (a)\n" + "".join(f"\t\t\t\t\t4'b{pat}: y = 4'h{val:X};\n" for pat, val in z['lines']) + \
              "\t\t\t\t\tdefault: y = 4'h0;\n\t\t\t\tendcase\n"
board("ex10", "case / casez: 16 casez blocks, puzzle SW9..6 (HEX1), a = SW3..0 (HEX0), y on LEDG3..0 and HEX3.", f"""
	wire [3:0] a = SW[3:0];
	wire [3:0] p = SW[9:6];
	reg  [3:0] y;
	always @(*) begin
		y = 4'h0;
		case (p)
{case10}		endcase
	end

	assign LEDG = {{4'b0, y}};
	assign LEDR = 10'b0;
	hex7seg h3(.x(y), .seg(HEX3));
	assign HEX2 = 7'b1111111;
	hex7seg h1(.x(p), .seg(HEX1));
	hex7seg h0(.x(a), .seg(HEX0));
""")
# ex10 is read from the code, so the code is open (puzzles.txt); the answers are computed by questions.ps1,
# the bit keys (truth table + minimal cost) are listed too - a key says nothing without solving the K-map.
pz = ["# ex10: the casez blocks of the board, one per puzzle (line = pattern value), and the key of every bit of y",
      "# (key = truth table in hex, row a = 15 first ... + minimal SOP terms/literals). Made by gen_w4.py - do not edit."]
md10 = ""
for p, z in enumerate(P10):
    pz.append(f"puzzle {p} " + " ".join(f"{pat}={val:X}" for pat, val in z['lines']))
    for b, (ones, best) in enumerate(z['bits']):
        tt = sum(1 << a for a in ones)
        pz.append(f"bit {p} {b} {tt:04X} {best[0]}/{best[1]}")
    md10 += f"| {p} | " + "; ".join(f"{pat}:{val:X}" for pat, val in z['lines']) + f" | {z['dflt']} | line {z['shadow']} | " + \
            " ".join(f"y{b}:{best[0]}/{best[1]}" for b, (o, best) in enumerate(z['bits'])) + " |\n"
write(f"{REPO}/ex10/tools/puzzles.txt", "\n".join(pz) + "\n", "\r\n")
write(f"{REPO}/ex10/tools/secrets.txt", "# ex10: no hidden answers - the casez code is open (puzzles.txt)\n", "\r\n")
write(f"{SOL}/ex10/ANSWERS.md", "# week 4 ex10 - casez puzzles\n\n| puzzle | lines | default hits | never fires | minimal SOP cost of y3..y0 bits |\n|---|---|---|---|---|\n" + md10 +
      "\nPer-student questions and answers: `answers.bat w4-ex10 <ID>`.\n")
k10 = {}
for p, z in enumerate(P10):
    for b, (ones, best) in enumerate(z['bits']):
        _, _, _, cov = kmin_analyse(set(ones), set(), 4, False)
        k10[f"expr|puzzle {p} y[{b}]"] = " + ".join(fmt_term(c) for c in cov[0])
write(f"{SOL}/ex10/key.json", json.dumps(k10, indent=0))

print("ex8 delays", P8)
print("ex9", [(term_str({VN[z['l1']]: z['s1'], VN[z['V']]: 0}), term_str({VN[z['V']]: 1, VN[z['l2']]: z['s2']})) for z in P9])
print("ex10", len(P10), "puzzles")

# ================================================================= compile
if "--compile" in sys.argv:
    for ex in ("ex8", "ex9", "ex10"):
        d = f"{SOL}/{ex}/board"
        r = subprocess.run([f"{QBIN}/quartus_sh", "--flow", "compile", "board"], cwd=d, capture_output=True, text=True)
        print(ex, "compile exit", r.returncode)
        if r.returncode == 0:
            shutil.copyfile(f"{d}/output_files/board.sof", f"{REPO}/{ex}/board.sof")
