#!/usr/bin/env python3
import os

def read_lt3(fname):
    """Return {(id1,id2): dist} keeping only key-value pairs with dist<3"""
    data = {}
    with open(fname) as f:
        for line in f:
            if line.startswith('id1'):
                continue
            id1, id2, d = line.split()
            key = tuple(sorted(map(int, (id1, id2))))
            dist = float(d)
            if dist < 3.0:
                data[key] = dist
    return data

# ---------- Main Program ----------
files = [f'bond_length.{i}.dist' for i in range(5)]
if not all(os.path.exists(f) for f in files):
    raise SystemExit('Missing the first 5 .dist files!')

series = [read_lt3(f) for f in files]   # List with length=5

with open('step_change_lt3.txt', 'w') as fw:
    fw.write('step\tid1\tid2\tdelta_d_A\trelative_change_%\n')
    for step in range(4):               # 0→1, 1→2, 2→3, 3→4
        prev, curr = series[step], series[step+1]
        for key in prev:
            if key not in curr:
                continue
            d_prev, d_curr = prev[key], curr[key]
            delta = d_curr - d_prev
            rel = (delta / d_prev * 100.0) if d_prev else 0.0
            id1, id2 = key
            fw.write(f'{step+1}\t{id1}\t{id2}\t{delta:.6f}\t{rel:.2f}\n')

print('Written to step_change_lt3.txt')