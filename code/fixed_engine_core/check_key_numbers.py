"""Check the key manuscript numbers from included T3 closure outputs.

Run from the repository root:
    python code/check_key_numbers.py
"""
from __future__ import annotations
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
rows = json.loads((ROOT / 'data' / 'processed' / 't3_closure_probe_summary.json').read_text())

n = len(rows)
benefit = sum(r['gap_h_minus_t3'] > 0 for r in rows)
harm = n - benefit
classes = Counter(r['mechanism_class'] for r in rows)
d26 = [r for r in rows if r['delay'] == 26]
traj_counts = {tn: (sum(r['gap_h_minus_t3'] > 0 for r in rows if r['traj'] == tn),
                   sum(1 for r in rows if r['traj'] == tn))
               for tn in sorted(set(r['traj'] for r in rows))}

print('Cells:', n)
print('Benefit cells:', benefit)
print('Harm/non-benefit cells:', harm)
print('Mechanism classes:', dict(classes))
print('Design latency d=26 benefits:', sum(r['gap_h_minus_t3'] > 0 for r in d26), '/', len(d26))
print('Trajectory benefit counts:', traj_counts)

assert n == 96, n
assert benefit == 78, benefit
assert harm == 18, harm
assert classes['harm_cost_dominance'] == 15, classes
assert classes['harm_with_local_reversal'] == 1, classes
assert sum(r['gap_h_minus_t3'] > 0 for r in d26) == 12, d26
assert traj_counts['circle'] == (17, 24), traj_counts
assert traj_counts['square'] == (23, 24), traj_counts
assert traj_counts['lemniscate'] == (16, 24), traj_counts
assert traj_counts['zigzag'] == (22, 24), traj_counts
print('All key checks passed.')
