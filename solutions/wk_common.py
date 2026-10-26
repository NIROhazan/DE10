# -*- coding: utf-8 -*-
# Shared by the class exercises of weeks 5-11 (gen_wN.py): the lecture-3 engine (class_exercise/gen.py), helpers for
# questions, the main loop (simulate / compile / write), and the week's folder (LESSON.bat, label.txt, lesson.txt,
# README.md). Instructor only.
#   in gen_wN.py:  import wk_common as C;  G, Q, HOLD = C.setup(N, __file__);  ... W = [...];  C.main(W, ORDER, TOPICS, DESC)
import argparse, itertools, os, random, re, shutil, sys
sys.path.insert(0, "C:/DE10/solutions/class_exercise")
import gen as G

Q, HOLD = G.Q, G.HOLD
WEEK = None

def setup(week, here_file):
    global WEEK
    WEEK = week
    here = os.path.dirname(os.path.abspath(here_file)).replace("\\", "/")
    G.LECTURE = str(week)
    G.PREFIX = f"w{week}|"
    G.REPO = f"C:/DE10/solutions/de1/week{week}"	# the DE1 build; the repo weeks are the DE10-Lite port (de10/port.py)
    G.HERE = here
    G.EXPLAIN_FILE = f"{here}/explain_w{week}.py"
    return G, Q, HOLD

# ---------------------------------------------------------------- helpers for questions
def hexd(d):					# the 4 outputs of one 7-segment digit
    return [("H", (d, b)) for b in range(4)]
def bitsof(v, n):
    return [(v >> b) & 1 for b in range(n)]
def const(vals, n=1):				# outputs that do not depend on the n row bits (a display of data)
    return [[x] * (1 << n) for x in vals]
def cnt(n, start=1):				# a count on SW3..SW0, as a ready list
    return [" ".join(f"{k} = " + ("+".join(f"SW{b}" for b in range(3, -1, -1) if k >> b & 1) or "all down")
                     for k in range(start, n + 1))]
def code(names, per=4):				# a choice among names: 0 = all down, 1 = SW0, ... (lines of `per`)
    items = [f"{nm} = " + ("+".join(f"SW{b}" for b in range(3, -1, -1) if k >> b & 1) or "all down")
             for k, nm in enumerate(names)]
    return ["     ".join(items[i:i + per]) for i in range(0, len(items), per)]
BIN4 = ["8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
BIN5 = ["16 = SW4     8 = SW3     4 = SW2     2 = SW1     1 = SW0"]
UP0 = lambda yes, no: [yes + " - הרימו:", "SW0", no + " - השאירו למטה."]
CLK = ["KEY1 = clock (one rising edge per press)     KEY0 = reset"]

def run(q, p, actions, start=0):
    """A clocked question: the state after actions from start; actions = ints (switch rows) or 'c' (KEY1) / 'r' (KEY0)."""
    tabs, ni, cur, inb = q.tables(p), len(q.inputs), start, 0
    for a in actions:
        if a == "c":
            cur = sum(tabs[j][(cur << ni) | inb] << i for j, (k, i) in enumerate(q.outs) if k == "N")
        elif a == "r":
            cur = 0
        else:
            inb = a
    return cur
def outs_at(q, p, state, inb):			# the visible outputs (non-N, no HOLD) at a state and input row
    tabs, ni = q.tables(p), len(q.inputs)
    return {o: tabs[j][(state << ni) | inb] for j, o in enumerate(q.outs) if o[0] != "N"}
def fsm_tables(q_outs, sb, ni, nxt, out):
    """Tables of a clocked question: nxt(state, inb) -> next state, out(state, inb) -> {out: bit}; outs in q_outs order."""
    t = []
    for kind, i in q_outs:
        col = []
        for r in range(1 << (sb + ni)):
            s_, inb = r >> ni, r & ((1 << ni) - 1)
            col.append((nxt(s_, inb) >> i) & 1 if kind == "N" else out(s_, inb)[(kind, i)])
        t.append(col)
    return t
def nouts(sb):
    return [("N", i) for i in range(sb)]

# ---------------------------------------------------------------- numbers shown on the display (one or two pages)
def digs(n):					# the outputs of the n left digits (HEX3 first)
    return [o for d in (3, 2, 1, 0)[:n] for o in hexd(d)]
def show(pages):				# pages = [[d3, d2, ...]] or two of them (SW9 down / up) -> the tables
    n = len(pages[0])
    cols = []
    for k, d in enumerate((3, 2, 1, 0)[:n]):
        for b in range(4):
            cols.append([(pg[k] >> b) & 1 for pg in (pages if len(pages) == 2 else pages * 2)])
    return cols
def numq(W, id_, title, n, variants, pages, legend, steps, describe, pages2=False):
    """A question whose data are numbers on the display (SW9 = page 2 when pages2); the answer = the last step's."""
    W.append(Q(id=id_, name=id_, title=title, inputs=[9], flat=True, outs=digs(n), hexes=[None, None, None, None],
               variants=variants, tables=lambda p: show(pages(p)), answer=lambda p: steps[-1][1](None, p),
               describe=describe, B=[legend + ("     SW9 = page 2" if pages2 else "") + "     answer: SW8..SW0"], L=[], F=[],
               steps=steps))
def rv(seed, k, f):				# up to k distinct variants from a generator f(rng) (None = skip)
    r, out = random.Random(seed), []
    for _ in range(20000):
        v = f(r)
        if v is not None and v not in out:
            out.append(v)
            if len(out) == k:
                break
    return out
def binl(n):					# the switch list of an n-bit binary answer
    items = [f"{1 << b} = SW{b}" for b in range(n - 1, -1, -1)]
    return ["   ".join(items[i:i + 6]) for i in range(0, len(items), 6)]

# ---------------------------------------------------------------- checks, main
def check_lang(W):				# a line is Hebrew or English, never both
    bad = []
    for q in W:
        q.ns = len(q.steps) + 1
        for lines, _ in q.steps:
            for l in lines:
                he = any("\u0590" <= c <= "\u05ff" for c in l)
                lat = any(c.isascii() and c.isalpha() for c in l)
                if he and lat:
                    bad.append(f"{q.name}: {l}")
    assert not bad, "mixed lines:\n" + "\n".join(bad)

def order(W, ORDER):
    by = {q.name: q for q in W}
    assert sorted(by) == sorted(ORDER), sorted(set(by) ^ set(ORDER))
    W = [by[n] for n in ORDER]
    for i, q in enumerate(W):
        q.id = f"Q{i + 1:02d}"
    check_lang(W)
    G.QS = W
    G.QBY = {q.id: q for q in W}
    return W

def student_folder(W, TOPICS, DESC, TITLE):
    """The week's folder C:/DE10/week<N> (the tools are shared in C:/DE10/tools): LESSON.bat, label.txt, lesson.txt, README.md."""
    dst = G.REPO
    os.makedirs(dst, exist_ok=True)
    shutil.copy("C:/DE10/week2/LESSON.bat", f"{dst}/LESSON.bat")
    G.write(f"{dst}/label.txt", f"w{WEEK}ce\n")
    k, lt, rows = 1, [], []
    for t, (mins, name, n) in enumerate(TOPICS, 1):
        ids = [f"Q{i:02d}" for i in range(k, k + n)]
        lt.append(f"TOPIC {mins} | {name} | {' '.join(ids)}")
        for j, qid in enumerate(ids):
            rows.append(f"| {f'**{t}. {name}**' if j == 0 else ''} | {qid} | {DESC[G.QBY[qid].name]} |")
        k += n
    assert k - 1 == len(W), "TOPICS do not add up"
    G.write(f"{dst}/lesson.txt",
            f"# The lesson schedule of week {WEEK} (lecture {WEEK}) - read by LESSON.bat (tools\\lesson.ps1). Edit it before the lesson.\n"
            "# TOPIC <minutes> | <name, Hebrew, no English letters> | <questions, easy -> hard>.\n\n"
            "# The lesson's time starts when the student types the student ID; the TOPIC minutes add up to the lesson's\n"
            "# length and are only a recommendation (the menu lets the student open any question).\n"
            + "\n".join(lt) + "\n")
    clocked = any(q.sb for q in W)
    G.write(f"{dst}/README.md",
            f"# תרגיל כיתה - שבוע {WEEK} (הרצאה {WEEK}): {TITLE}\n\n"
            "דאבל-קליק על `LESSON.bat`. איך עובדים: [README הראשי](../README.md). פירוט מלא של כל שאלה: [`QUESTIONS.md`](QUESTIONS.md).\n\n"
            + ("בשאלות עם שעון: **`KEY1`** = עליית שעון אחת בכל לחיצה, **`KEY0`** = איפוס.\n\n" if clocked else "")
            + f"## השאלות\n\n| נושא (כל אחד {TOPICS[0][0]} דקות) | שאלה | מה |\n|---|---|---|\n" + "\n".join(rows) + "\n")

def main(W, TOPICS, DESC, TITLE):
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
    student_folder(W, TOPICS, DESC, TITLE)
    sel = [G.QBY[a.only]] if a.only else W
    bad = []
    for q in sel:
        d = G.build(q)
        print(f"{q.id} {q.name}: {len(q.variants)} variants, {q.ns} steps", flush=True)
        if not a.nosim and not G.simulate(q, d):
            bad.append(q.id); continue
        if a.compile and not G.compile_q(q, d):
            bad.append(q.id)
        sys.stdout.flush()
    G.write(f"{G.REPO}/questions.txt", G.questions_txt())
    G.write(f"{G.REPO}/QUESTIONS.md", G.questions_md())
    G.write(f"{G.HERE}/QUESTIONS_ANSWERS.md", G.questions_md(a.answers))
    G.write(f"{G.HERE}/instructor_guide/guide.html", G.answers_guide(a.answers))
    print("FAILED: " + " ".join(bad) if bad else "all OK", flush=True)
    sys.exit(1 if bad else 0)
