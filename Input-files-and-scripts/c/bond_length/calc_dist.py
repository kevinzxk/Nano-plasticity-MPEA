#!/usr/bin/env python3
import os, re, math

def read_coords(fname):
    """Extract list of (id,x,y,z) from LAMMPS format file"""
    atoms = []
    with open(fname) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('ITEM:'):
                continue
            parts = line.split()
            if len(parts) != 5:
                continue
            idx, typ, x, y, z = parts
            atoms.append((int(idx), float(x), float(y), float(z)))
    return atoms

def all_pairs(atoms):
    """Generate (id1,id2,dist) for all distinct atom pairs"""
    for i in range(len(atoms)):
        for j in range(i+1, len(atoms)):
            id1, x1, y1, z1 = atoms[i]
            id2, x2, y2, z2 = atoms[j]
            d = math.sqrt((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)
            yield id1, id2, d

# ---------- Main Loop ----------
for idx in range(11):               # 0..10
    inp = f'bond_length.{idx}'
    out = f'bond_length.{idx}.dist'
    if not os.path.isfile(inp):
        print(f'Warning: {inp} does not exist, skipping')
        continue
    atoms = read_coords(inp)
    with open(out, 'w') as f:
        f.write('id1\tid2\tdistance\n')
        for id1, id2, d in all_pairs(atoms):
            f.write(f'{id1}\t{id2}\t{d:.6f}\n')
    print(f'Completed: {inp} -> {out}')