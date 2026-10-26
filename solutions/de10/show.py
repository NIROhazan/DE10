# -*- coding: utf-8 -*-
# py show.py <week> <Qnn> ...   the definition of questions (inputs, outputs, texts)
import sys
from load import load

G, W = load(int(sys.argv[1]))
by = {q.id: q for q in W}
for qid in sys.argv[2:]:
    q = by[qid]
    print(f"##### {q.id} {q.name} inputs={q.inputs} outs={q.outs} hexes={q.hexes} n={q.n} vb={q.vb}")
    for l in q.B:
        print("B:", l)
    for k, (ls, _) in enumerate(q.steps, 1):
        for l in ls:
            print(f"S{k}:", l)
        p = q.variants[0]
        print(f"   answer v0: {G.step_answer(q, p, k)}")
    print("   describe v0:", q.describe(q.variants[0]))
