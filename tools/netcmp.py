"""Parse a KiCad kicadsexpr netlist; compare two netlists by node sets."""
import re, sys
from collections import defaultdict

def tok(s):
    return re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', s)

def parse(s):
    t = tok(s); i = 0
    def rd():
        nonlocal i
        if t[i] == '(':
            i += 1; L = []
            while t[i] != ')':
                L.append(rd())
            i += 1; return L
        v = t[i]; i += 1
        return v[1:-1] if v.startswith('"') else v
    return rd()

def find(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]

def load(path):
    root = parse(open(path).read())
    comps = {}
    for c in find(find(root, 'components')[0], 'comp'):
        ref = find(c, 'ref')[0][1]
        sp = find(c, 'sheetpath')
        name = find(sp[0], 'names')[0][1] if sp else ''
        comps[ref] = name
    nets = []
    for n in find(find(root, 'nets')[0], 'net'):
        name = find(n, 'name')[0][1]
        nodes = frozenset((find(x, 'ref')[0][1], find(x, 'pin')[0][1]) for x in find(n, 'node'))
        nets.append((name, nodes))
    return comps, nets

if __name__ == '__main__':
    ca, na = load(sys.argv[1]); cb, nb = load(sys.argv[2])
    ca = {k for k in ca if not k.startswith('#')}; cb = {k for k in cb if not k.startswith('#')}
    print('components only in A:', sorted(ca - cb)); print('components only in B:', sorted(cb - ca))
    # drop power-symbol nodes
    def clean(nets):
        out = {}
        for name, nodes in nets:
            nd = frozenset(x for x in nodes if not x[0].startswith('#'))
            if nd: out[nd] = name
        return out
    A, B = clean(na), clean(nb)
    onlyA = [ (A[k], sorted(k)) for k in A if k not in B]
    onlyB = [ (B[k], sorted(k)) for k in B if k not in A]
    print(f'nets A={len(A)} B={len(B)} onlyA={len(onlyA)} onlyB={len(onlyB)}')
    # node -> net maps for a readable diff
    def n2n(D):
        m = {}
        for k, name in D.items():
            for x in k: m[x] = (name, k)
        return m
    mA, mB = n2n(A), n2n(B)
    for name, k in sorted(onlyA):
        print('A:', name, k)
        for x in k:
            if x in mB: print('     B has', x, 'in', mB[x][0], sorted(mB[x][1])[:8])
    for name, k in sorted(onlyB):
        print('B:', name, k)
    # names of rails should match
    same = not onlyA and not onlyB and ca == cb
    print("PASS: identical connections" if same else "FAIL: connections differ")
    sys.exit(0 if same else 1)
