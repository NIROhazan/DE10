"""Exact minimal SOP / POS (fewest terms, then literals) for n <= 4, like check.ps1's Get-MinCost.
Also all prime implicants and all minimal covers."""
from itertools import product, combinations

def cubes(n):
    for c in product('01-', repeat=n):
        yield ''.join(c)

def covers(c, b):
    return all(x == '-' or x == y for x, y in zip(c, b))

def analyse(ones, dcs, n, pos=False):
    rows = [format(i, f'0{n}b') for i in range(2 ** n)]
    want = [r for i, r in enumerate(rows) if (i in ones) != pos and i not in dcs]
    off = [r for i, r in enumerate(rows) if (i in ones) == pos and i not in dcs]
    ok = [c for c in cubes(n) if not any(covers(c, r) for r in off) and any(covers(c, r) for r in want)]
    # prime: no other ok cube strictly contains it
    def contains(a, b):  # a contains b
        return a != b and all(x == '-' or x == y for x, y in zip(a, b))
    primes = [c for c in ok if not any(contains(o, c) for o in ok)]
    best = None; covers_found = []
    for t in range(1, len(primes) + 1):
        for comb in combinations(primes, t):
            if all(any(covers(c, r) for c in comb) for r in want):
                lits = sum(n - c.count('-') for c in comb)
                if best is None or lits < best[1]:
                    best = (t, lits); covers_found = [comb]
                elif lits == best[1]:
                    covers_found.append(comb)
        if best:
            break
    ess = [p for p in primes if any(covers(p, r) and sum(covers(q, r) for q in primes) == 1 for r in want)]
    return primes, ess, best, covers_found

def fmt(c, vars_, pos=False):
    lits = [(v if (b == '1') != pos else v + "'") for v, b in zip(vars_, c) if b != '-']
    if pos:
        return '(' + ' + '.join(lits) + ')' if len(lits) > 1 else lits[0]
    return ''.join(lits) or '1'

def report(name, ones, dcs, n):
    vars_ = 'ABCD'[:n]
    print(f'== {name}: ones {sorted(ones)} dc {sorted(dcs)}')
    for pos in (False, True):
        primes, ess, best, cov = analyse(set(ones), set(dcs), n, pos)
        k = 'POS' if pos else 'SOP'
        print(f'  {k} primes {[fmt(p, vars_, pos) for p in primes]}  essential {[fmt(p, vars_, pos) for p in ess]}  best {best}')
        for c in cov:
            print('     ', (' ' if pos else ' + ').join(fmt(p, vars_, pos) for p in c))

if __name__ == '__main__':
    report('ex4 wrap', [0, 2, 3, 7], [], 3)
    report('ex5 cyclic', [0, 1, 2, 5, 6, 7], [], 3)
    report('ex6 octet', [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 14], [], 4)
    seg = {  # Harris sevenseg abc_defg for digits 0..9
        0: '1111110', 1: '0110000', 2: '1101101', 3: '1111001', 4: '0110011',
        5: '1011011', 6: '1011111', 7: '1110000', 8: '1111111', 9: '1110011'}
    for i, s in enumerate('abcdefg'):
        report(f'ex7 segment {s}', [d for d in range(10) if seg[d][i] == '1'], range(10, 16), 4)
        report(f'ex7 segment {s} NO X', [d for d in range(10) if seg[d][i] == '1'], [], 4)
