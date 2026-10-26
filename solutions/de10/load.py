# -*- coding: utf-8 -*-
# Loads the questions of one week from its DE1 generator, without running its main.
#   G, W = load(week)   G = the lecture-3 engine (class_exercise/gen.py), W = the questions Q01.. in order
import importlib.util, sys

sys.path.insert(0, "C:/DE10/solutions/class_exercise")
sys.path.insert(0, "C:/DE10/solutions")

def load(week):
    import gen as G
    if week == 3:
        W = [q for q in G.QS if q.id.startswith("Q")]
        G.QS, G.QBY = W, {q.id: q for q in W}
        for q in W:
            q.ns = len(q.steps) + 1
        return G, W
    path = f"C:/DE10/solutions/week{week}/class_exercise/gen_w{week}.py"
    spec = importlib.util.spec_from_file_location(f"gen_w{week}", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return G, m.W
