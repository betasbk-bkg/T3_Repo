"""
t3_closure_bootstrap.py
=======================
Raw-run bootstrap check for selected T3 closure cells.

This script imports `t3_closure_probe.py` and reuses its engine-level functions.
It is intended to be placed in the same folder as:
  - adversary_ladder.py
  - t3_closure_probe.py

Why this script exists
----------------------
`t3_closure_probe_summary.json` stores cell-level means, so it cannot provide
proper bootstrap confidence intervals for the closure variables. This script
regenerates per-run data for selected cells and bootstraps the closure variables.

Usage examples
--------------
  python t3_closure_bootstrap.py quick
  python t3_closure_bootstrap.py boundary --mc 50 --boot 2000
  python t3_closure_bootstrap.py custom --trajs circle --trs 0.20,0.30 --delays 34,44,56 --mc 50 --boot 2000
  python t3_closure_bootstrap.py full --mc 50 --boot 1000

Outputs
-------
  results/t3_closure_bootstrap_summary.csv
  results/t3_closure_bootstrap_summary.json

Key CIs
-------
  gap_h_minus_t3_ci
  energy_relief_ci
  abs_relief_ci
  osc_change_pct_ci
  edot_change_pct_ci
  tail_delta_ci

Interpretation
--------------
For cost-dominance closure, key harm cells should show:
  gap_h_minus_t3 < 0,
  energy_relief > 0 or abs_relief > 0,
  and increased osc/edot/tail cost.
"""
from __future__ import annotations

import argparse, csv, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import t3_closure_probe as CP


def parse_csv_list(s: str, cast=str):
    if s is None or s == '': return []
    return [cast(x.strip()) for x in s.split(',') if x.strip()]


def percentile_ci(x, lo=2.5, hi=97.5):
    return [float(np.percentile(x, lo)), float(np.percentile(x, hi))]


def mean_key(rows, idx, key):
    vals = [rows[i][key] for i in idx]
    return float(np.nanmean(vals))


def collect_per_run(traj_name: str, tr: float, delay: int, mc: int, N: int = 50, coh: float = 1.0):
    h_seed0 = CP.seed_base(traj_name, 'honest', tr, delay, coh=coh)
    t_seed0 = CP.seed_base(traj_name, 'T3pub', tr, delay, coh=coh)
    h_rows=[]; t_rows=[]; p_rows=[]
    for i in range(mc):
        h = CP.simulate_mode_series(CP.TRAJ_CTORS[traj_name](), traj_name, N, tr, h_seed0 + i*31, 'honest', delay, coh=coh)
        t = CP.simulate_mode_series(CP.TRAJ_CTORS[traj_name](), traj_name, N, tr, t_seed0 + i*31, 'T3pub', delay, coh=coh)
        p = CP.local_probe_on_t3_state(CP.TRAJ_CTORS[traj_name](), N, tr, t_seed0 + i*31, delay, coh=coh)
        h_rows.append(h); t_rows.append(t); p_rows.append(p)
    return h_rows, t_rows, p_rows


def summarize_bootstrap_cell(traj_name: str, tr: float, delay: int, mc: int, boot: int, N: int = 50, coh: float = 1.0, seed: int = 20260617):
    rng = np.random.default_rng(seed + hash((traj_name, tr, delay)) % 100000)
    h_rows, t_rows, p_rows = collect_per_run(traj_name, tr, delay, mc, N=N, coh=coh)
    n = mc

    boot_vals = {k: np.empty(boot) for k in [
        'gap_h_minus_t3', 'energy_relief', 'abs_relief', 'osc_change_pct',
        'edot_change_pct', 'tail_delta', 'raw_cos_vel'
    ]}

    for b in range(boot):
        ih = rng.integers(0, n, n)
        it = rng.integers(0, n, n)
        ip = rng.integers(0, n, n)

        rmse_h = mean_key(h_rows, ih, 'rmse')
        rmse_t = mean_key(t_rows, it, 'rmse')
        osc_h = mean_key(h_rows, ih, 'osc_std')
        osc_t = mean_key(t_rows, it, 'osc_std')
        edot_h = mean_key(h_rows, ih, 'edot_rms')
        edot_t = mean_key(t_rows, it, 'edot_rms')
        relief = mean_key(p_rows, ip, 'energy_relief')
        abs_relief = mean_key(p_rows, ip, 'abs_relief')
        raw_cos = mean_key(p_rows, ip, 'raw_cos_vel')

        h_abs = np.concatenate([np.abs(h_rows[i]['signed_errs']) for i in ih])
        t_abs = np.concatenate([np.abs(t_rows[i]['signed_errs']) for i in it])
        q95 = np.percentile(h_abs, 95)
        tail_delta = float(np.mean(t_abs > q95) - np.mean(h_abs > q95))

        boot_vals['gap_h_minus_t3'][b] = rmse_h - rmse_t
        boot_vals['energy_relief'][b] = relief
        boot_vals['abs_relief'][b] = abs_relief
        boot_vals['osc_change_pct'][b] = (osc_t - osc_h) / (osc_h + 1e-12) * 100
        boot_vals['edot_change_pct'][b] = (edot_t - edot_h) / (edot_h + 1e-12) * 100
        boot_vals['tail_delta'][b] = tail_delta
        boot_vals['raw_cos_vel'][b] = raw_cos

    row = {'traj': traj_name, 'tr': tr, 'delay': delay, 'mc': mc, 'boot': boot}
    for k, arr in boot_vals.items():
        row[k] = float(np.mean(arr))
        row[k + '_ci_lo'], row[k + '_ci_hi'] = percentile_ci(arr)

    # Conservative classification from bootstrap means + CI signs.
    gap = row['gap_h_minus_t3']; relief = row['energy_relief']; abs_rel = row['abs_relief']
    cost_flag = (row['osc_change_pct'] > 10) or (row['edot_change_pct'] > 10) or (row['tail_delta'] > 0.03)
    if gap > 0:
        cls = 'benefit'
    elif relief < -0.05 or abs_rel < -0.02:
        cls = 'harm_with_local_reversal'
    elif cost_flag:
        cls = 'harm_cost_dominance'
    else:
        cls = 'harm_or_neutral_unclear'
    row['mechanism_class_mean'] = cls
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', nargs='?', default='quick', choices=['quick','boundary','full','custom'])
    ap.add_argument('--trajs', default=None)
    ap.add_argument('--trs', default=None)
    ap.add_argument('--delays', default=None)
    ap.add_argument('--mc', type=int, default=None)
    ap.add_argument('--boot', type=int, default=1000)
    ap.add_argument('--N', type=int, default=50)
    args = ap.parse_args()

    if args.mode == 'quick':
        trajs = ['circle'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.30] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [26, 34, 44, 56] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 20 if args.mc is None else args.mc
    elif args.mode == 'boundary':
        trajs = ['circle','lemniscate'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.20, 0.30, 0.40] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [0, 8, 18, 34, 44, 56] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 50 if args.mc is None else args.mc
    elif args.mode == 'full':
        trajs = ['circle','square','lemniscate','zigzag'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.20, 0.30, 0.40] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [0,8,18,26,34,44,56,68] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 50 if args.mc is None else args.mc
    else:
        trajs = ['circle'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.30] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [26,34,44,56] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 30 if args.mc is None else args.mc

    rows=[]; total=len(trajs)*len(trs)*len(delays); k=0
    print(f'[closure_bootstrap] mode={args.mode} cells={total} mc={mc} boot={args.boot}')
    for tn in trajs:
        for tr in trs:
            for d in delays:
                k += 1
                row = summarize_bootstrap_cell(tn, tr, d, mc=mc, boot=args.boot, N=args.N)
                rows.append(row)
                print(f"[{k:03d}/{total}] {tn:10} tr={tr:.2f} d={d:2d} "
                      f"gap={row['gap_h_minus_t3']:+.3f} [{row['gap_h_minus_t3_ci_lo']:+.3f},{row['gap_h_minus_t3_ci_hi']:+.3f}] "
                      f"relief={row['energy_relief']:+.3f} [{row['energy_relief_ci_lo']:+.3f},{row['energy_relief_ci_hi']:+.3f}] "
                      f"osc%={row['osc_change_pct']:+.1f} tailΔ={row['tail_delta']:+.3f} "
                      f"class={row['mechanism_class_mean']}")

    outdir = os.path.join(HERE, 'results')
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, 't3_closure_bootstrap_summary.csv')
    json_path = os.path.join(outdir, 't3_closure_bootstrap_summary.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    print(f'\nsaved:\n  {csv_path}\n  {json_path}')


if __name__ == '__main__':
    main()
