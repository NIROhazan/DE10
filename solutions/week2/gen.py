# Week 2 boards and secrets (instructor only).  python gen.py
# Writes, for week2 ex1..ex6:
#   C:/DE10/solutions/week2/exN/board/board.v + board.qpf + board.qsf   (the hidden board source)
#   C:/DE10/week2/exN/tools/secrets.txt   (question pools + hashes of the right answers - no answers in clear)
#   C:/DE10/solutions/week2/exN/ANSWERS.md (the puzzle tables)
# Fixed seed: running it again gives the same boards and secrets.
import hashlib, os, random, re

SOL = "C:/DE10/solutions/week2"
REPO = "C:/DE10/week2"
rng = random.Random(20261006)

def H(s):
    return hashlib.sha256(("DE10w2|" + s).encode("ascii")).hexdigest()[:10]

SEG = ["1000000", "1111001", "0100100", "0110000", "0011001", "0010010", "0000010", "1111000",
       "0000000", "0010000", "0001000", "0000011", "1000110", "0100001", "0000110", "0001110"]
HEX7 = """
// Hex digit to 7-segment, active low, seg[6:0] = g f e d c b a
module hex7seg(input [3:0] x, output reg [6:0] seg);
	always @(*) case (x)
""" + "".join(f"\t\t4'h{i:X}: seg = 7'b{s};\n" for i, s in enumerate(SEG)) + """\t\tdefault: seg = 7'b1111111;
	endcase
endmodule
"""
PORTS = """	input  [9:0] SW,
	input  [3:0] KEY,
	output [9:0] LEDR,
	output [7:0] LEDG,
	output [6:0] HEX0,
	output [6:0] HEX1,
	output [6:0] HEX2,
	output [6:0] HEX3"""
BLANK = "7'b1111111"
DASH = "7'b0111111"

top = open("C:/DE10/top.qsf", encoding="utf-8").read().splitlines()
pins = [l for l in top if re.search(r"-to (SW|KEY|LEDR|LEDG|HEX)", l)]

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

def board(ex, title, body):
    v = f"// {ex} board - Terasic DE1 (Cyclone II EP2C20F484C7). Instructor source: students get only board.sof.\n" \
        f"// {title}\nmodule board(\n{PORTS}\n\t);\n{body}endmodule\n{HEX7}"
    d = f"{SOL}/{ex}/board"
    write(f"{d}/board.v", v)
    write(f"{d}/board.qpf", 'QUARTUS_VERSION = "13.0"\nPROJECT_REVISION = "board"\n')
    q = ['# ' + ex + ' board - DE1, Quartus II 13.0sp1',
         'set_global_assignment -name FAMILY "Cyclone II"',
         'set_global_assignment -name DEVICE EP2C20F484C7',
         'set_global_assignment -name TOP_LEVEL_ENTITY board',
         'set_global_assignment -name VERILOG_FILE board.v',
         'set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files',
         'set_global_assignment -name RESERVE_ALL_UNUSED_PINS "AS INPUT TRI-STATED"',
         'set_global_assignment -name STRATIX_DEVICE_IO_STANDARD "3.3-V LVTTL"'] + pins
    write(f"{d}/board.qsf", "\n".join(q) + "\n")

import json
def secrets(ex, pools, ok):
    key = {}
    for item, ans in ok:
        key.setdefault(item, ans)        # the first spelling is the one to show
    write(f"{SOL}/{ex}/key.json", json.dumps(key, indent=0))
    lines = [f"# {ex}: question pools, and hashes of the right answers (made by the instructor's gen.py - do not edit)"]
    for name, items in pools.items():
        lines.append(f"pool {name} " + " ".join(items))
    hs = sorted(set(H(f"w2-{ex}|{item}|{ans}") for item, ans in ok))	# w2-ex5 = the label run.ps1 uses
    for i in range(0, len(hs), 8):
        lines.append("ok " + " ".join(hs[i:i + 8]))
    write(f"{REPO}/{ex}/tools/secrets.txt", "\n".join(lines) + "\n")

# ------------------------------------------------------------------ ex1: numbers, secret bytes
S = [rng.randrange(16, 256) for _ in range(64)]
case = "".join(f"\t\t6'd{p}: S = 8'h{s:02X};\n" for p, s in enumerate(S))
board("ex1", "N = SW9..0 on LEDR and in hex on HEX2..0. KEY3 held: secret byte of puzzle SW5..0 on LEDG7..0.", f"""
	wire secret = ~KEY[3];
	reg [7:0] S;
	always @(*) case (SW[5:0])
{case}		default: S = 8'h00;
	endcase
	wire [6:0] h0, h1, h2;
	hex7seg d0(.x(SW[3:0]), .seg(h0));
	hex7seg d1(.x(SW[7:4]), .seg(h1));
	hex7seg d2(.x({{2'b00, SW[9:8]}}), .seg(h2));
	assign LEDR = SW;
	assign LEDG = secret ? S : 8'h00;
	assign HEX0 = secret ? {DASH} : h0;
	assign HEX1 = secret ? {DASH} : h1;
	assign HEX2 = secret ? {DASH} : h2;
	assign HEX3 = secret ? {DASH} : {BLANK};
""")
secrets("ex1", {"Q4": [f"p{p}" for p in range(64)]},
        [(f"p{p}", f"{s:X} {s}") for p, s in enumerate(S)])
write(f"{SOL}/ex1/ANSWERS.md", "# ex1 - secret bytes (KEY3 held, puzzle = SW5..SW0)\n\n| puzzle | byte | decimal |\n|---|---|---|\n" +
      "".join(f"| {p} | {s:02X} | {s} |\n" for p, s in enumerate(S)))

# ------------------------------------------------------------------ ex2: 4-bit adder with carry in
board("ex2", "A = SW3..0 (HEX0), B = SW7..4 (HEX1), Cin = KEY0 pressed. S = A+B+Cin on HEX3 and LEDG3..0, carry out on LEDG7.", f"""
	wire [3:0] A = SW[3:0], B = SW[7:4];
	wire cin = ~KEY[0];
	wire [4:0] T = A + B + cin;
	hex7seg d0(.x(A), .seg(HEX0));
	hex7seg d1(.x(B), .seg(HEX1));
	hex7seg d3(.x(T[3:0]), .seg(HEX3));
	assign HEX2 = {BLANK};
	assign LEDR = SW;
	assign LEDG = {{T[4], 1'b0, 1'b0, cin, T[3:0]}};
""")

# ------------------------------------------------------------------ ex3: signed 4-bit adder
board("ex3", "X = SW3..0 (HEX0), Y = SW7..4 (HEX1), S = X+Y on HEX3 and LEDG3..0, LEDG6 = carry out, LEDG7 = signed overflow.", f"""
	wire [3:0] X = SW[3:0], Y = SW[7:4];
	wire [4:0] T = X + Y;
	wire V = (X[3] == Y[3]) && (T[3] != X[3]);
	hex7seg d0(.x(X), .seg(HEX0));
	hex7seg d1(.x(Y), .seg(HEX1));
	hex7seg d3(.x(T[3:0]), .seg(HEX3));
	assign HEX2 = {BLANK};
	assign LEDR = SW;
	assign LEDG = {{V, T[4], 2'b00, T[3:0]}};
""")

# ------------------------------------------------------------------ ex4: extension
board("ex4", "X = SW3..0 (HEX0). E = X extended to 8 bits on HEX3..HEX2 and LEDG7..0: sign-extension, or zero-extension while SW9 is up.", f"""
	wire [3:0] X = SW[3:0];
	wire [7:0] E = SW[9] ? {{4'b0000, X}} : {{{{4{{X[3]}}}}, X}};
	hex7seg d0(.x(X), .seg(HEX0));
	hex7seg d2(.x(E[3:0]), .seg(HEX2));
	hex7seg d3(.x(E[7:4]), .seg(HEX3));
	assign HEX1 = {BLANK};
	assign LEDR = SW;
	assign LEDG = E;
""")

# ------------------------------------------------------------------ ex5: mystery gates
def vec(f):  # truth vector over i = C*4 + B*2 + A
    return tuple(int(bool(f((i >> 0) & 1, (i >> 1) & 1, (i >> 2) & 1))) for i in range(8))
G = {
    "BUF": vec(lambda a, b, c: a), "NOT": vec(lambda a, b, c: 1 - a),
    "AND": vec(lambda a, b, c: a & b), "OR": vec(lambda a, b, c: a | b),
    "NAND": vec(lambda a, b, c: 1 - (a & b)), "NOR": vec(lambda a, b, c: 1 - (a | b)),
    "XOR": vec(lambda a, b, c: a ^ b), "XNOR": vec(lambda a, b, c: 1 - (a ^ b)),
    "AND3": vec(lambda a, b, c: a & b & c), "OR3": vec(lambda a, b, c: a | b | c),
    "NAND3": vec(lambda a, b, c: 1 - (a & b & c)), "NOR3": vec(lambda a, b, c: 1 - (a | b | c)),
    "XOR3": vec(lambda a, b, c: a ^ b ^ c), "XNOR3": vec(lambda a, b, c: 1 - (a ^ b ^ c)),
}
three = {"AND3", "OR3", "NAND3", "NOR3", "XOR3", "XNOR3"}
names = list(G)
def comp(x, y): return all(a != b for a, b in zip(G[x], G[y]))
P18 = []
while len(P18) < 16:
    pick = rng.sample(names, 8)
    pairs = [(i, j) for i in range(8) for j in range(i + 1, 8) if comp(pick[i], pick[j])]
    n3 = sum(g in three for g in pick)
    if len(pairs) == 1 and 2 <= n3 <= 4 and pick not in P18:
        P18.append(pick)
rows = ""
for p, pick in enumerate(P18):
    for i in range(8):
        led = "".join(str(G[pick[k]][i]) for k in range(7, -1, -1))
        rows += f"\t\t7'd{p * 8 + i}: L = 8'b{led};\n"
board("ex5", "A = SW0, B = SW1, C = SW2, puzzle = SW9..SW6 (HEX0). LEDG7..0 = eight hidden gates of the puzzle.", f"""
	reg [7:0] L;
	always @(*) case ({{SW[9:6], SW[2:0]}})
{rows}		default: L = 8'h00;
	endcase
	hex7seg d0(.x(SW[9:6]), .seg(HEX0));
	assign HEX1 = {BLANK};
	assign HEX2 = {BLANK};
	assign HEX3 = {BLANK};
	assign LEDR = SW;
	assign LEDG = L;
""")
ok = []
two_items, three_items, pair_items, find_items = [], [], [], []
for p, pick in enumerate(P18):
    for k, g in enumerate(pick):
        (three_items if g in three else two_items).append(f"p{p}k{k}")
    i, j = [(i, j) for i in range(8) for j in range(i + 1, 8) if comp(pick[i], pick[j])][0]
    pair_items.append(f"p{p}")
    ok.append((f"pair{p}", f"{i} {j} {pick[i]} {pick[j]}"))
    ok.append((f"pair{p}", f"{j} {i} {pick[j]} {pick[i]}"))
    ok.append((f"all{p}", " ".join(pick[k] for k in range(7, -1, -1))))
for g in names:
    for k in range(8):
        ps = [p for p in range(16) if P18[p][k] == g]
        if len(ps) == 1:
            find_items.append(f"{g}@{k}")
            ok.append((f"find{g}@{k}", str(ps[0])))
# answers of two LEDs (Q1, Q2) are checked one LED at a time: item pXkY -> name
for p, pick in enumerate(P18):
    for k, g in enumerate(pick):
        ok.append((f"p{p}k{k}", g))
secrets("ex5", {"two": two_items, "three": three_items, "all": [f"p{p}" for p in range(16)],
                 "pair": pair_items, "find": find_items}, ok)
md = "# ex5 - mystery gates (A = SW0, B = SW1, C = SW2, puzzle = SW9..SW6)\n\n| puzzle | LEDG7 | LEDG6 | LEDG5 | LEDG4 | LEDG3 | LEDG2 | LEDG1 | LEDG0 |\n|---|---|---|---|---|---|---|---|---|\n"
for p, pick in enumerate(P18):
    md += f"| {p} | " + " | ".join(pick[k] for k in range(7, -1, -1)) + " |\n"
write(f"{SOL}/ex5/ANSWERS.md", md)

# ------------------------------------------------------------------ ex6: CMOS gate detective
IN = "ABC"
def gate19(kind, ins):
    x = lambda a, b, c, n: (a, b, c)[IN.index(n)]
    if kind == "NOT":   f = lambda a, b, c: 1 - x(a, b, c, ins[0])
    if kind == "NAND2": f = lambda a, b, c: 1 - (x(a, b, c, ins[0]) & x(a, b, c, ins[1]))
    if kind == "NOR2":  f = lambda a, b, c: 1 - (x(a, b, c, ins[0]) | x(a, b, c, ins[1]))
    if kind == "AND2":  f = lambda a, b, c: x(a, b, c, ins[0]) & x(a, b, c, ins[1])
    if kind == "OR2":   f = lambda a, b, c: x(a, b, c, ins[0]) | x(a, b, c, ins[1])
    if kind == "NAND3": f = lambda a, b, c: 1 - (a & b & c)
    if kind == "NOR3":  f = lambda a, b, c: 1 - (a | b | c)
    # AOI21 / OAI21: ins[0] is the lone input, ins[1] ins[2] the pair
    if kind == "AOI21": f = lambda a, b, c: 1 - ((x(a, b, c, ins[1]) & x(a, b, c, ins[2])) | x(a, b, c, ins[0]))
    if kind == "OAI21": f = lambda a, b, c: 1 - ((x(a, b, c, ins[1]) | x(a, b, c, ins[2])) & x(a, b, c, ins[0]))
    return vec(f)
COUNT = {"NOT": 2, "NAND2": 4, "NOR2": 4, "NAND3": 6, "NOR3": 6, "AND2": 6, "OR2": 6, "AOI21": 6, "OAI21": 6}
UP = {"NAND2": "PARALLEL", "NAND3": "PARALLEL", "NOR2": "SERIES", "NOR3": "SERIES"}
DOWN = {"NAND2": "SERIES", "NAND3": "SERIES", "NOR2": "PARALLEL", "NOR3": "PARALLEL"}
kinds = ["NOT", "NAND2", "NOR2", "NAND3", "NOR3", "AND2", "OR2", "AOI21", "OAI21",
         "NAND2", "NOR2", "NAND3", "NOR3", "AOI21", "OAI21", "OR2"]
rng.shuffle(kinds)
P19 = []
for kind in kinds:
    if kind == "NOT": ins = rng.choice(IN)
    elif kind in ("NAND3", "NOR3"): ins = "ABC"
    elif kind in ("AOI21", "OAI21"): l = rng.choice(IN); ins = l + "".join(c for c in IN if c != l)
    else: ins = "".join(sorted(rng.sample(IN, 2)))
    P19.append((kind, ins))
rows = ""
for p, (kind, ins) in enumerate(P19):
    v = gate19(kind, ins)
    for i in range(8):
        rows += f"\t\t7'd{p * 8 + i}: Y = 1'b{v[i]};\n"
board("ex6", "A = SW0, B = SW1, C = SW2, puzzle = SW9..SW6 (HEX0). Y of the hidden CMOS gate on LEDG0 and HEX3.", f"""
	reg Y;
	always @(*) case ({{SW[9:6], SW[2:0]}})
{rows}		default: Y = 1'b0;
	endcase
	hex7seg d0(.x(SW[9:6]), .seg(HEX0));
	hex7seg d3(.x({{3'b000, Y}}), .seg(HEX3));
	assign HEX1 = {BLANK};
	assign HEX2 = {BLANK};
	assign LEDR = SW;
	assign LEDG = {{7'b0000000, Y}};
""")
ok = []
pools = {"name": [], "cmos": [], "inputs": [], "count": [], "aoi": []}
for p, (kind, ins) in enumerate(P19):
    it = f"p{p}"
    ok.append((f"name{p}", kind))
    ok.append((f"count{p}", str(COUNT[kind])))
    if kind not in ("AOI21", "OAI21"): pools["name"].append(it)
    pools["count"].append(it)
    if kind in UP:
        pools["cmos"].append(it); ok.append((f"cmos{p}", f"{kind} {UP[kind]} {DOWN[kind]} {COUNT[kind]}"))
    if kind in ("NAND2", "NOR2", "AND2", "OR2"):
        pools["inputs"].append(it); ok.append((f"inputs{p}", f"{kind} {ins[0]} {ins[1]}")); ok.append((f"inputs{p}", f"{kind} {ins[1]} {ins[0]}"))
    if kind in ("AOI21", "OAI21"):
        pools["aoi"].append(it); ok.append((f"aoi{p}", f"{kind} {ins[0]}"))
secrets("ex6", pools, ok)
md = "# ex6 - CMOS gates (A = SW0, B = SW1, C = SW2, puzzle = SW9..SW6)\n\n| puzzle | gate | inputs | transistors | pull-up | pull-down |\n|---|---|---|---|---|---|\n"
for p, (kind, ins) in enumerate(P19):
    shown = f"lone {ins[0]}, pair {ins[1]}{ins[2]}" if kind in ("AOI21", "OAI21") else ins
    md += f"| {p} | {kind} | {shown} | {COUNT[kind]} | {UP.get(kind, '-')} | {DOWN.get(kind, '-')} |\n"
write(f"{SOL}/ex6/ANSWERS.md", md)
print("ok")
