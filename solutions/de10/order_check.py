# -*- coding: utf-8 -*-
# Does the repo's questions.txt / lesson.txt match the generator's question order?
import re, sys
from load import load

week = int(sys.argv[1])
G, W = load(week)
gen = [q.name for q in W]
txt = open(f"C:/DE10/week{week}/questions.txt", encoding="utf-8").read()
repo = re.findall(r"^\[Q\d+\] (\S+)", txt, re.M)
lesson = open(f"C:/DE10/week{week}/lesson.txt", encoding="utf-8").read()
lq = re.findall(r"Q\d\d", "\n".join(l for l in lesson.splitlines() if l.startswith("TOPIC")))
diff = [(i + 1, a, b) for i, (a, b) in enumerate(zip(gen, repo)) if a != b]
print(f"week {week}: generator {len(gen)}, repo {len(repo)}, lesson {len(lq)} ids; differ at {len(diff)}: {diff[:4]}")
