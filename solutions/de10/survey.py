# -*- coding: utf-8 -*-
import re, sys
from load import load

week = int(sys.argv[1])
G, W = load(week)
kinds = {}
for q in W:
    ks = sorted({k for k, _ in q.outs})
    r = sorted(i for k, i in q.outs if k == "R")
    g = sorted(i for k, i in q.outs if k == "G")
    text = " ".join(q.B + [l for ls, _ in q.steps for l in ls])
    keys = sorted(set(re.findall(r"KEY\d", text)))
    leds = sorted(set(re.findall(r"LED[RG]\d+", text)))
    flags = []
    if set(r) & set(g): flags.append("R&G-OVERLAP")
    if r and g: flags.append("R+G")
    if q.sb: flags.append(f"clocked sb={q.sb}")
    if "KEY0" in text or "KEY2" in text or "KEY3" in text: flags.append("keys:" + ",".join(keys))
    print(f"{q.id} {q.name:10} outs={''.join(ks):6} R={r} G={g} vb={q.vb} n={q.n} ns={q.ns} {' '.join(flags)}")
