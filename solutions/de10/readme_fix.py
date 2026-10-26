# -*- coding: utf-8 -*-
# py readme_fix.py <week>   the question table of C:/DE10/weekN/README.md from the generator (TOPICS, DESC)
import re, sys
from load import load

week = int(sys.argv[1])
f = f"C:/DE10/week{week}/README.md"
t = open(f, encoding="utf-8").read()
if week == 3:
    t = t.replace("4 נורות ירוקות", "4 נורות אדומות").replace("LEDG0", "LEDR0")
else:
    G, W = load(week)
    m = sys.modules[f"gen_w{week}"]
    rows, k = [], 1
    for ti, (mins, name, n) in enumerate(m.TOPICS, 1):
        for j in range(n):
            q = W[k - 1 + j]
            rows.append(f"| {f'**{ti}. {name}**' if j == 0 else ''} | {q.id} | {m.DESC[q.name]} |")
        k += n
    lines = t.splitlines()
    head = next(i for i, l in enumerate(lines) if l.startswith("| נושא"))
    end = head + 2
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    lines[head + 2:end] = rows
    t = "\n".join(lines) + "\n"
open(f, "w", encoding="utf-8", newline="\n").write(t)
print(f"week {week}: README written")
