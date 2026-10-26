# -*- coding: utf-8 -*-
# The class exercises of weeks 3-11 on the Terasic DE10-Lite (MAX 10 10M50DAF484C7G). Instructor only.
#
#   py port.py 5                    simulate every question of week 5 and write the student files into C:/DE10/week5
#   py port.py 5 --compile          also compile with Quartus Prime 25.1 and copy sof/Qnn.sof into C:/DE10/week5/sof
#   py port.py 5 --only Q13 [Q14]   only these questions
#   py port.py 5 --id <ID>          a student's login number, every step's answer and the codes (the same as gen_wN.py --id)
#
# The questions, variants, answers and codes come unchanged from the DE1 generators (class_exercise/gen.py for week 3,
# weekN/class_exercise/gen_wN.py for the others, same key.txt) - so answers.bat / verify.bat keep working.
# The board design is the DE1 core (module ce from gen.py, simulated as before) inside a DE10 top level:
#   KEY0 = check the answer (the DE1's KEY2), KEY1 = the DE1's KEY1;
#   the DE10 has no green LEDs: LEDGi -> LEDRi. A question with red and green outputs moves the green ones up
#   (LEDGi -> LEDR(i + off)) when both fit in 10 LEDs, otherwise a free switch picks the page (0 = red, 1 = green);
#   HEX0..HEX3 as on the DE1 (decimal points off), HEX4 and HEX5 blank.
# The screen texts get the same changes (LEDG -> LEDR, green -> red, the moved LEDs, the page switch).
import argparse, os, re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from load import load

ROOT = "C:/DE10"
QBIN = "C:/altera_standard/25.1std/quartus/bin64"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

# ---------------------------------------------------------------- where every output goes on the DE10
def layout(q):
    """-> (led, page_sw): led[j] = the LEDR index of output j (R / G outputs only); page_sw = None or the switch that
    picks the page (then page[j] = 0 for the red outputs, 1 for the green ones)."""
    r = [(j, i) for j, (k, i) in enumerate(q.outs) if k == "R"]
    g = [(j, i) for j, (k, i) in enumerate(q.outs) if k == "G"]
    led, page = {}, {}
    if not (r and g):
        for j, i in r + g:
            led[j] = i
        return led, page, None, 0
    rmax, gmin, gmax = max(i for _, i in r), min(i for _, i in g), max(i for _, i in g)
    off = 9 - gmax
    if gmin + off > rmax:			# both fit: the green ones go to the top LEDs
        for j, i in r:
            led[j] = i
        for j, i in g:
            led[j] = i + off
        return led, page, None, off
    used = set(q.inputs)
    for k in range(1, q.ns):			# the answer switches of every variant
        for p in q.variants:
            used |= {b for b in range(10) if G.step_answer(q, p, k)[1] >> b & 1}
    free = [b for b in range(9, -1, -1) if b not in used]
    if q.inputs == [9] and all(len(set(t)) == 1 for t in q.tables(q.variants[0])):
        free = [9] + free			# SW9 only picks a page of constant data anyway
    assert free, f"{q.id} {q.name}: no switch is free for the page"
    for j, i in r:
        led[j], page[j] = i, 0
    for j, i in g:
        led[j], page[j] = i, 1
    return led, page, free[0], 0

# ---------------------------------------------------------------- the screen texts
GROUP = re.compile(r"LED([RG])(\d)(?:\.\.LED([RG])(\d))?")
HE_GREEN = [("ירוקות", "אדומות"), ("ירוקים", "אדומים"), ("ירוקה", "אדומה"), ("ירוק", "אדום")]

def fix_line(l, q, off, psw):
    def sub(m):
        kind, a, b = m.group(1), int(m.group(2)), m.group(4)
        def idx(k, i):
            return i + off if k == "G" else i
        s = f"LEDR{idx(kind, a)}" + (f"..LEDR{idx(m.group(3), int(b))}" if b else "")
        if psw is not None:
            s += f" (SW{psw} = {1 if kind == 'G' else 0})"
        return s
    l = GROUP.sub(sub, l)
    l = l.replace("(green)", "(red)")
    for a, b in HE_GREEN:
        l = l.replace(a, b)
    return l

def fix_texts(q, off, psw):
    q.B = [fix_line(l, q, off, psw) for l in q.B]
    if psw is not None:				# say once, in the board line, what the page switch does
        q.B = [l + f"     SW{psw} = which LEDs (0 / 1)" for l in q.B]
    q.steps = [([fix_line(l, q, off, psw) for l in lines], f) for lines, f in q.steps]
    if q.P:
        q.P = {k: [fix_line(l, q, off, psw) for l in v] for k, v in q.P.items()}

# ---------------------------------------------------------------- the DE10 top level
def top_v(q, led, page, psw):
    rows = []
    for b in range(10):
        js = [j for j in led if led[j] == b]
        if not js:
            rows.append("1'b0")
            continue
        def val(j):
            k, i = q.outs[j]
            return f"core_LEDR[{i}]" if k == "R" else f"core_LEDG[{i}]"
        if psw is None:
            rows.append(val(js[0]))
        else:
            p0 = [j for j in js if page[j] == 0]
            p1 = [j for j in js if page[j] == 1]
            rows.append(f"(SW[{psw}] ? {val(p1[0]) if p1 else chr(49) + chr(39) + 'b0'} : {val(p0[0]) if p0 else chr(49) + chr(39) + 'b0'})")
    ledr = ", ".join(rows[::-1])
    return f"""// Class exercise {q.id} ({q.name}) - Terasic DE10-Lite (MAX 10 10M50DAF484C7G).
// Generated by C:/DE10/solutions/de10/port.py - students get only the .sof.
// The DE1 core (module ce, ce.v) with the DE10's keys, LEDs and displays:
//   KEY0 = check the answer (the core's KEY2), KEY1 = the core's KEY1; no green LEDs - see port.py for the LEDs.
module de10_top(
	input        MAX10_CLK1_50,
	input  [1:0] KEY,
	input  [9:0] SW,
	output [9:0] LEDR,
	output [7:0] HEX0,
	output [7:0] HEX1,
	output [7:0] HEX2,
	output [7:0] HEX3,
	output [7:0] HEX4,
	output [7:0] HEX5
	);
	wire [9:0] core_LEDR;
	wire [7:0] core_LEDG;
	wire [6:0] h0, h1, h2, h3;
	ce core(.CLOCK_50(MAX10_CLK1_50), .SW(SW), .KEY({{1'b1, KEY[0], KEY[1], 1'b1}}),
		.LEDR(core_LEDR), .LEDG(core_LEDG), .HEX0(h0), .HEX1(h1), .HEX2(h2), .HEX3(h3));
	assign LEDR = {{{ledr}}};
	assign HEX0 = {{1'b1, h0}};
	assign HEX1 = {{1'b1, h1}};
	assign HEX2 = {{1'b1, h2}};
	assign HEX3 = {{1'b1, h3}};
	assign HEX4 = 8'hFF;
	assign HEX5 = 8'hFF;
endmodule
"""

def top_tb(q, led, page, psw):
    """The DE10 top level against its core: every LED and display, for random switches, in every core state."""
    lines = ["`timescale 1ns/1ns", "module tbtop;", "\treg clk = 0; always #10 clk = ~clk;",
             "\treg [9:0] SW = 0; reg [1:0] KEY = 2'b11;",
             "\twire [9:0] LEDR; wire [7:0] HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;",
             "\tde10_top dut(.MAX10_CLK1_50(clk), .KEY(KEY), .SW(SW), .LEDR(LEDR), .HEX0(HEX0), .HEX1(HEX1), .HEX2(HEX2), .HEX3(HEX3), .HEX4(HEX4), .HEX5(HEX5));",
             "\tinteger i, b, fails = 0; reg want;",
             "\tinitial begin",
             f"\t\tdut.core.sp.src = 14'h{(1 << 13) | (1 << 10) | 5:04X};",
             "\t\tfor (i = 0; i < 400; i = i + 1) begin",
             "\t\t\tSW = $random; KEY[0] = (i % 37) != 5; repeat (3) @(posedge clk);"]
    for b in range(10):
        js = [j for j in led if led[j] == b]
        want = "1'b0"
        def val(j):
            k, i = q.outs[j]
            return f"dut.core.LEDR[{i}]" if k == "R" else f"dut.core.LEDG[{i}]"
        if js and psw is None:
            want = val(js[0])
        elif js:
            p0 = [val(j) for j in js if page[j] == 0] or ["1'b0"]
            p1 = [val(j) for j in js if page[j] == 1] or ["1'b0"]
            want = f"(SW[{psw}] ? {p1[0]} : {p0[0]})"
        lines.append(f"\t\t\tif (LEDR[{b}] !== {want}) begin fails = fails + 1; if (fails < 5) $display(\"FAIL LEDR{b} at %0d\", i); end")
    lines.append("\t\t\tif ({HEX3[6:0], HEX2[6:0], HEX1[6:0], HEX0[6:0]} !== {dut.core.HEX3, dut.core.HEX2, dut.core.HEX1, dut.core.HEX0}"
                 " || {HEX5, HEX4, HEX3[7], HEX2[7], HEX1[7], HEX0[7]} !== 20'hFFFFF) begin fails = fails + 1; if (fails < 5) $display(\"FAIL HEX at %0d\", i); end")
    # every output that the core drives must reach the board (a green or red output with no LED would be lost)
    lines += ["\t\tend", "\t\t$display(\"top: %0d fails\", fails);", "\t\t$finish;", "\tend", "endmodule"]
    return "\n".join(lines) + "\n"

def build(q, week):
    led, page, psw, off = layout(q)
    d = G.build(q)				# the DE1 core: ce.v and the ROMs (HERE/build/Qnn of the week)
    shutil.rmtree(f"{d}/de10", ignore_errors=True)
    os.makedirs(f"{d}/de10")
    for f in ("ce.v", "seed.hex", "want.hex", "table.hex"):
        shutil.copy(f"{d}/{f}", f"{d}/de10/{f}")
    dd = f"{d}/de10"
    G.write(f"{dd}/de10_top.v", top_v(q, led, page, psw))
    G.write(f"{dd}/de10.qpf", 'QUARTUS_VERSION = "25.1"\nPROJECT_REVISION = "de10"\n')
    G.write(f"{dd}/de10.sdc", "create_clock -name MAX10_CLK1_50 -period 20 [get_ports MAX10_CLK1_50]\n")
    pins = [l for l in open(f"{ROOT}/top.qsf", encoding="utf-8").read().splitlines()
            if re.search(r"-to (MAX10_CLK1_50|SW|KEY|LEDR|HEX)", l)]
    G.write(f"{dd}/de10.qsf", "\n".join([
        f"# Class exercise week {week} {q.id} - DE10-Lite, Quartus Prime 25.1",
        'set_global_assignment -name FAMILY "MAX 10"',
        "set_global_assignment -name DEVICE 10M50DAF484C7G",
        "set_global_assignment -name TOP_LEVEL_ENTITY de10_top",
        "set_global_assignment -name VERILOG_FILE de10_top.v",
        "set_global_assignment -name VERILOG_FILE ce.v",
        "set_global_assignment -name SDC_FILE de10.sdc",
        "set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files",
        "set_global_assignment -name NUM_PARALLEL_PROCESSORS 2",
        'set_global_assignment -name INTERNAL_FLASH_UPDATE_MODE "SINGLE IMAGE WITH ERAM"',
        'set_global_assignment -name RESERVE_ALL_UNUSED_PINS_WEAK_PULLUP "AS INPUT TRI-STATED WITH WEAK PULL-UP"'] + pins) + "\n")
    return d, dd, (led, page, psw)

def simulate_top(q, d, dd, lay):
    G.write(f"{dd}/tbtop.v", top_tb(q, *lay))
    G.write(f"{dd}/stub_issp.v", G.STUB)
    r = subprocess.run([f"{G.IVL}/iverilog", "-o", "top.vvp", "tbtop.v", "de10_top.v", "ce.v", "stub_issp.v"],
                       cwd=dd, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr); return False
    r = subprocess.run([f"{G.IVL}/vvp", "-n", "top.vvp"], cwd=dd, capture_output=True, text=True)
    out = r.stdout.strip().splitlines()
    bad = [l for l in out if "FAIL" in l]
    if bad:
        print("    top:", "\n    ".join(bad))
    return any(l == "top: 0 fails" for l in out)

def compile_q(q, dd, week):
    r = subprocess.run([f"{QBIN}/quartus_sh.exe", "--flow", "compile", "de10"], cwd=dd, capture_output=True, text=True)
    open(f"{dd}/compile.log", "w", encoding="utf-8").write(r.stdout + r.stderr)
    if r.returncode:
        return f"{q.id}: COMPILE FAILED - {dd}/compile.log"
    os.makedirs(f"{ROOT}/week{week}/sof", exist_ok=True)
    shutil.copy(f"{dd}/output_files/de10.sof", f"{ROOT}/week{week}/sof/{q.id}.sof")
    return None

# ---------------------------------------------------------------- the student files
def lesson_txt(week, m, W):
    if not hasattr(m, "TOPICS"):
        return None				# weeks 3 and 4: the repo's lesson.txt already matches
    k, lt = 1, []
    for mins, name, n in m.TOPICS:
        lt.append(f"TOPIC {mins} | {name} | " + " ".join(f"Q{i:02d}" for i in range(k, k + n)))
        k += n
    assert k - 1 == len(W)
    return (f"# The lesson schedule of week {week} (lecture {week}) - read by LESSON.bat (tools\\lesson.ps1). Edit it before the lesson.\n"
            "# TOPIC <minutes> | <name, Hebrew, no English letters> | <questions, easy -> hard>.\n\n"
            "# The lesson's time starts when the student types the student ID; the TOPIC minutes add up to the lesson's\n"
            "# length and are only a recommendation (the menu lets the student open any question).\n"
            + "\n".join(lt) + "\n")

def write_student(week, m, W):
    wdir = f"{ROOT}/week{week}"
    stage = f"{HERE}/stage/week{week}"		# gen.py reads REPO/lesson.txt
    os.makedirs(f"{stage}/tools", exist_ok=True)
    lt = lesson_txt(week, m, W)
    if lt:
        G.write(f"{wdir}/lesson.txt", lt)
    shutil.copy(f"{wdir}/lesson.txt", f"{stage}/lesson.txt")
    G.REPO = stage
    txt = G.questions_txt().replace("C:/DE10/solutions/class_exercise/gen.py", "C:/DE10/solutions/de10/port.py")
    G.write(f"{wdir}/questions.txt", txt)
    G.write(f"{wdir}/QUESTIONS.md", G.questions_md())
    G.write(f"{wdir}/label.txt", f"w{week}ce\n")

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("week", type=int)
    ap.add_argument("--compile", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--id")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--nosim", action="store_true")
    a = ap.parse_args()
    week = a.week
    G, W = load(week)
    m = sys.modules.get(f"gen_w{week}")
    if a.id:
        G.show_id(a.id); sys.exit(0)
    G.HERE = f"{HERE}/build/week{week}"		# the DE1 build folders of the generators stay as they are
    lays = {}
    for q in W:
        led, page, psw, off = layout(q)
        lays[q.id] = (led, page, psw)
        fix_texts(q, off, psw)
        if psw is not None or off:
            print(f"{q.id} {q.name}: " + (f"page switch SW{psw}" if psw is not None else f"green LEDs moved up by {off}"))
    # every LEDR a screen names must be an output of that question
    for q in W:
        outs = set(lays[q.id][0].values())
        named = set()
        for l in q.B + [l for ls, _ in q.steps for l in ls]:
            for mm in re.finditer(r"LEDR(\d)(?:\.\.LEDR(\d))?", l):
                x, y = int(mm.group(1)), int(mm.group(2) or mm.group(1))
                named |= set(range(min(x, y), max(x, y) + 1))
        if named - outs:
            print(f"WARNING {q.id} {q.name}: the screen names LEDR {sorted(named - outs)}, not outputs")
    write_student(week, m, W)
    sel = [q for q in W if not a.only or q.id in a.only]
    bad, jobs = [], []
    for q in sel:
        d, dd, lay = build(q, week)
        ok = True
        if not a.nosim:
            ok = G.simulate(q, d) and simulate_top(q, d, dd, lay)
        print(f"{q.id} {q.name}: {'sim OK' if ok else 'SIM FAILED'}", flush=True)
        if not ok:
            bad.append(q.id)
        elif a.compile:
            jobs.append((q, dd))
    if jobs:
        with ThreadPoolExecutor(a.jobs) as ex:
            for q, err in zip([q for q, _ in jobs], ex.map(lambda t: compile_q(t[0], t[1], week), jobs)):
                print(err or f"{q.id}: compiled -> week{week}/sof/{q.id}.sof", flush=True)
                if err:
                    bad.append(q.id)
    print(f"week {week}: " + ("FAILED: " + " ".join(bad) if bad else "all OK"), flush=True)
    sys.exit(1 if bad else 0)
