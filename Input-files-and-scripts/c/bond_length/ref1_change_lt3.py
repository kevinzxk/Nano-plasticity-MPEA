#!/usr/bin/env python3
import os

def read_lt3(fname):
    """返回 {(id1,id2): dist} 仅保留 dist<3 的键值"""
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

# ---------- 主程序 ----------
files = [f'bond_length.{i}.dist' for i in range(5)]
if not all(os.path.exists(f) for f in files):
    raise SystemExit('缺少前 5 个 .dist 文件！')

ref0 = read_lt3(files[0])          # 基准：文件 0
series = [read_lt3(f) for f in files[1:]]  # 文件 1-4

with open('ref1_change_lt3.txt', 'w') as fw:
    fw.write('step\tid1\tid2\tdelta_d_A\trelative_change_%\n')
    for step, data in enumerate(series, 1):   # step=1,2,3,4
        for key in ref0:
            if key not in data:
                continue
            d0, di = ref0[key], data[key]
            delta = di - d0
            rel = (delta / d0 * 100.0) if d0 else 0.0
            id1, id2 = key
            fw.write(f'{step}\t{id1}\t{id2}\t{delta:.6f}\t{rel:.2f}\n')

print('已写入 ref1_change_lt3.txt')