"""
t3_closure_probe.py
===================
Closure diagnostic for the T3 manuscript.

Purpose
-------
Tests whether the high-delay harm band is best explained by:
  H_phase: projected local relief reverses sign, or
  H_cost : local relief remains, but jitter/tail/mistiming costs dominate.

This script intentionally reuses the existing engine definitions in adversary_ladder.py
and mirrors t3_confirmatory.py's sim_u logic. It does NOT replace the engine.

Outputs
-------
  results/t3_closure_probe_summary.csv
  results/t3_closure_probe_summary.json

Key signs
---------
  gap_h_minus_t3 > 0  : T3 improves RMSE vs honest counterfactual
  energy_relief > 0   : local T3 command perturbation reduces signed-error energy
  abs_relief > 0      : local T3 command perturbation reduces absolute error
  vel_oppose > 0      : local T3 command perturbation opposes cross-track velocity
                       This is diagnostic only; RMSE is more directly tied to energy_relief/abs_relief.
  raw_cos_vel < 0     : raw minority-only vector is anti-parallel to current velocity

Recommended use
---------------
  python t3_closure_probe.py quick
  python t3_closure_probe.py full

Optional examples
-----------------
  python t3_closure_probe.py custom --trajs circle --trs 0.30 --delays 0,8,18,26,34,44,56,68 --mc 30
  python t3_closure_probe.py custom --trajs circle,lemniscate --trs 0.30 --delays 26,34,44,56 --mc 50
"""
from __future__ import annotations

import argparse, copy, csv, json, math, os, sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np

# Put the current script directory first, so it imports the user's local engine.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import adversary_ladder as AL
from adversary_ladder import Circle, Square, Lemniscate, Zigzag

TRAJ_CTORS = {
    "circle": Circle,
    "square": Square,
    "lemniscate": Lemniscate,
    "zigzag": Zigzag,
}
MODE_IDX = {"honest":0, "T3pub":2}
TRAJ_IDX = {"circle":0, "square":1, "lemniscate":2, "zigzag":3}


def seed_base(traj_name: str, mode: str, tr: float, ctrl_delay_f: int, coh: float = 1.0, agg: str = "mean", t3_obs_delay: int = 1) -> int:
    """Same deterministic seed convention as t3_confirmatory.py."""
    return (TRAJ_IDX[traj_name]*10_000_000 + MODE_IDX[mode]*1_000_000
            + int(round(tr*100))*10_000 + int(ctrl_delay_f)*100
            + int(round(coh*100)) + (0 if agg=='mean' else 5000)
            + t3_obs_delay*70_000)


def tangent_normal(traj, arc: float, eps: float = 0.15) -> Tuple[np.ndarray, np.ndarray]:
    p1 = traj.at(arc + eps)
    p0 = traj.at(arc - eps)
    t = p1 - p0
    n = np.linalg.norm(t)
    if n < 1e-12:
        t = np.array([1.0, 0.0])
    else:
        t = t / n
    return t, np.array([-t[1], t[0]])


def signed_error_and_normal(traj, pos: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray, float]:
    """Signed cross-track error and local normal.

    For circle, use the radial signed error. For polygonal/discrete trajectories,
    use the normal of the local path tangent estimated from traj.at(arc±eps).
    """
    cp, arc = traj.closest(pos)
    if isinstance(traj, Circle):
        r = np.linalg.norm(pos)
        nvec = pos / r if r > 1e-12 else np.array([1.0, 0.0])
        return float(r - traj.R), nvec, cp, arc
    _, nvec = tangent_normal(traj, arc)
    return float(np.dot(pos - cp, nvec)), nvec, cp, arc


def simulate_mode_series(traj, traj_name: str, N: int, tr: float, seed: int, mode: str,
                         ctrl_delay_f: int, coh: float = 1.0, t3_obs_delay: int = 1,
                         agg: str = "mean") -> Dict[str, np.ndarray | float]:
    """Mirror t3_confirmatory.sim_u, but log signed errors and derivatives."""
    rng = np.random.default_rng(seed)
    pos = traj.start(); vel = np.zeros(2); ph = [pos.copy()]
    pang = 0.0; cur_dir = np.array([1.0, 0.0])
    abs_errs = np.empty(AL.FRAMES)
    signed_errs = np.empty(AL.FRAMES)
    edots = np.empty(AL.FRAMES)
    pub_hist: List[float] = []
    hon_hist: List[float] = []

    for f in range(AL.FRAMES):
        if f % AL.VOTE_INT == 0:
            di = max(0, len(ph)-1-ctrl_delay_f)
            dp = ph[di]
            _, arc = traj.closest(dp)
            lap = traj.at(arc + AL.LOOK)
            idir = lap - dp
            nn = np.linalg.norm(idir)
            idir = idir/nn if nn > 1e-10 else idir
            iang = np.degrees(np.arctan2(idir[1], idir[0]))
            honest, nt = AL._honest_block(iang, pang, tr, N, rng)
            pang = iang
            pubprev = pub_hist[-t3_obs_delay] if len(pub_hist) >= t3_obs_delay else None
            honprev = hon_hist[-t3_obs_delay] if len(hon_hist) >= t3_obs_delay else None
            if nt > 0 and mode == 'T3pub':
                src = pubprev
                base = iang if src is None else src
                nc = int(np.floor(coh * nt)); nd = nt - nc
                troll = np.concatenate([
                    np.full(nc, AL.a2d(np.array([base+180.0]))[0], int),
                    rng.integers(0, 8, nd) if nd > 0 else np.array([], int)
                ])
            elif nt > 0 and mode == 'honest':
                troll = AL.a2d(iang + rng.uniform(-3, 3, nt))
            else:
                troll = np.array([], int)
            votes = np.concatenate([honest, troll])
            hb = AL.DIRS[honest].mean(0)
            hon_hist.append(np.degrees(np.arctan2(hb[1], hb[0])) if np.linalg.norm(hb) > 1e-10 else iang)
            if agg == 'mean':
                bl = AL.DIRS[votes].mean(0)
                nb = np.linalg.norm(bl)
                cur_dir = bl/nb if nb > 1e-10 else cur_dir
            elif agg == 'majority':
                cur_dir = AL.DIRS[np.bincount(votes, minlength=8).argmax()]
            else:
                raise ValueError(f"unknown agg={agg}")
            pub_hist.append(np.degrees(np.arctan2(cur_dir[1], cur_dir[0])))

        e, nvec, cp, _ = signed_error_and_normal(traj, pos)
        signed_errs[f] = e
        edots[f] = float(np.dot(vel, nvec))
        vel += AL.SMOOTH * (cur_dir * AL.MSPD - vel)
        pos = pos + vel * AL.DT
        ph.append(pos.copy())
        cp2, _ = traj.closest(pos)
        abs_errs[f] = np.linalg.norm(pos - cp2)

    sl = slice(120, None)
    abs_e = abs_errs[sl]
    se = signed_errs[sl]
    ed = edots[sl]
    return {
        "rmse": float(np.sqrt(np.mean(abs_e**2))),
        "signed_rms": float(np.sqrt(np.mean(se**2))),
        "osc_std": float(np.std(se)),
        "edot_rms": float(np.sqrt(np.mean(np.diff(se)**2))),
        "abs_errs": abs_e,
        "signed_errs": se,
        "edots": ed,
    }


def local_probe_on_t3_state(traj, N: int, tr: float, seed: int, ctrl_delay_f: int,
                            coh: float = 1.0, t3_obs_delay: int = 1) -> Dict[str, float]:
    """Local paired-command diagnostic on the T3 trajectory.

    At each vote update, construct the actual T3 command and a paired honest-counterfactual
    command using the same honest block and same RNG state for the counterfactual troll draw.
    Then measure whether the T3-vs-CF command perturbation locally reduces signed error,
    absolute error, or cross-track velocity.
    """
    rng = np.random.default_rng(seed)
    pos = traj.start(); vel = np.zeros(2); ph = [pos.copy()]
    pang = 0.0; cur_dir = np.array([1.0, 0.0]); cf_dir = np.array([1.0, 0.0])
    pub_hist: List[float] = []
    hon_hist: List[float] = []

    signed_errors=[]; abs_errors=[]; edots=[]
    energy_power=[]      # e * delta_v_perp; negative => local signed-error-energy reduction
    abs_power=[]         # sign(e) * delta_v_perp; negative => local abs-error reduction
    vel_power=[]         # edot * delta_v_perp; negative => local cross-track velocity damping
    delta_perps=[]; delta_norms=[]; raw_cos=[]

    for f in range(AL.FRAMES):
        if f % AL.VOTE_INT == 0:
            di = max(0, len(ph)-1-ctrl_delay_f)
            dp = ph[di]
            _, arc = traj.closest(dp)
            lap = traj.at(arc + AL.LOOK)
            idir = lap - dp
            nn = np.linalg.norm(idir)
            idir = idir/nn if nn > 1e-10 else idir
            iang = np.degrees(np.arctan2(idir[1], idir[0]))
            honest, nt = AL._honest_block(iang, pang, tr, N, rng)
            pang = iang

            # Pair the honest-counterfactual troll draw from the RNG state immediately
            # after the honest block, before the T3 troll draw consumes randomness.
            state = copy.deepcopy(rng.bit_generator.state)
            rng_cf = np.random.default_rng(); rng_cf.bit_generator.state = copy.deepcopy(state)

            pubprev = pub_hist[-t3_obs_delay] if len(pub_hist) >= t3_obs_delay else None
            if nt > 0:
                base = iang if pubprev is None else pubprev
                nc = int(np.floor(coh * nt)); nd = nt - nc
                tidx = np.concatenate([
                    np.full(nc, AL.a2d(np.array([base+180.0]))[0], int),
                    rng.integers(0, 8, nd) if nd > 0 else np.array([], int)
                ])
                cfidx = AL.a2d(iang + rng_cf.uniform(-3, 3, nt))
            else:
                tidx = np.array([], int); cfidx = np.array([], int)

            votes = np.concatenate([honest, tidx])
            votes_cf = np.concatenate([honest, cfidx])
            bl = AL.DIRS[votes].mean(0); nb = np.linalg.norm(bl)
            cur_dir = bl/nb if nb > 1e-10 else cur_dir
            blcf = AL.DIRS[votes_cf].mean(0); nbcf = np.linalg.norm(blcf)
            cf_dir = blcf/nbcf if nbcf > 1e-10 else cf_dir

            hb = AL.DIRS[honest].mean(0); hn = np.linalg.norm(hb)
            hon_hist.append(np.degrees(np.arctan2(hb[1], hb[0])) if hn > 1e-10 else iang)
            pub_hist.append(np.degrees(np.arctan2(cur_dir[1], cur_dir[0])))

            if np.linalg.norm(vel) > 1e-9 and len(tidx) > 0:
                tv = AL.DIRS[tidx].mean(0)
                tn = np.linalg.norm(tv)
                if tn > 1e-9:
                    raw_cos.append(float(np.dot(tv/tn, vel/np.linalg.norm(vel))))

        e, nvec, cp, _ = signed_error_and_normal(traj, pos)
        edot = float(np.dot(vel, nvec))
        # Difference in the next smoothing increment if current direction were T3 vs local CF.
        delta_v_next = AL.SMOOTH * AL.MSPD * (cur_dir - cf_dir)
        dvp = float(np.dot(delta_v_next, nvec))

        signed_errors.append(e)
        abs_errors.append(float(np.linalg.norm(pos - cp)))
        edots.append(edot)
        energy_power.append(e * dvp)
        abs_power.append((np.sign(e) * dvp) if abs(e) > 1e-12 else 0.0)
        vel_power.append(edot * dvp)
        delta_perps.append(dvp)
        delta_norms.append(float(np.linalg.norm(delta_v_next)))

        # Actual T3 update.
        vel += AL.SMOOTH * (cur_dir * AL.MSPD - vel)
        pos = pos + vel * AL.DT
        ph.append(pos.copy())

    sl = slice(120, None)
    se = np.asarray(signed_errors)[sl]
    ae = np.asarray(abs_errors)[sl]
    ed = np.asarray(edots)[sl]
    ep = np.asarray(energy_power)[sl]
    ap = np.asarray(abs_power)[sl]
    vp = np.asarray(vel_power)[sl]
    dp = np.asarray(delta_perps)[sl]
    dn = np.asarray(delta_norms)[sl]

    denomE = np.mean(np.abs(se * dp)) + 1e-12
    denomA = np.mean(np.abs(dp)) + 1e-12
    denomV = np.mean(np.abs(ed * dp)) + 1e-12
    return {
        "local_rmse": float(np.sqrt(np.mean(ae**2))),
        "energy_relief": float(-np.mean(ep)/denomE),
        "abs_relief": float(-np.mean(ap)/denomA),
        "vel_oppose": float(-np.mean(vp)/denomV),
        "mean_energy_power": float(np.mean(ep)),
        "mean_abs_power": float(np.mean(ap)),
        "mean_vel_power": float(np.mean(vp)),
        "delta_perp_abs": float(np.mean(np.abs(dp))),
        "delta_norm": float(np.mean(dn)),
        "raw_cos_vel": float(np.nanmean(raw_cos)) if raw_cos else float('nan'),
    }


def summarize_cell(traj_name: str, tr: float, delay: int, mc: int, N: int = 50, coh: float = 1.0) -> Dict[str, float | str | int]:
    traj_h = TRAJ_CTORS[traj_name]()
    traj_t = TRAJ_CTORS[traj_name]()
    h_seed0 = seed_base(traj_name, 'honest', tr, delay, coh=coh)
    t_seed0 = seed_base(traj_name, 'T3pub', tr, delay, coh=coh)

    h_rows=[]; t_rows=[]; p_rows=[]
    h_abs_pool=[]; t_abs_pool=[]
    for i in range(mc):
        h = simulate_mode_series(TRAJ_CTORS[traj_name](), traj_name, N, tr, h_seed0 + i*31, 'honest', delay, coh=coh)
        t = simulate_mode_series(TRAJ_CTORS[traj_name](), traj_name, N, tr, t_seed0 + i*31, 'T3pub', delay, coh=coh)
        p = local_probe_on_t3_state(TRAJ_CTORS[traj_name](), N, tr, t_seed0 + i*31, delay, coh=coh)
        h_rows.append(h); t_rows.append(t); p_rows.append(p)
        h_abs_pool.append(np.abs(h['signed_errs']))
        t_abs_pool.append(np.abs(t['signed_errs']))

    # pooled tail threshold from the honest counterfactual for this cell
    h_abs = np.concatenate(h_abs_pool)
    t_abs = np.concatenate(t_abs_pool)
    q95 = float(np.percentile(h_abs, 95))
    h_tail = float(np.mean(h_abs > q95))
    t_tail = float(np.mean(t_abs > q95))
    h_tail_mse_share = float(np.mean((h_abs[h_abs > q95]**2)) / (np.mean(h_abs**2)+1e-12)) if np.any(h_abs > q95) else 0.0
    t_tail_mse_share = float(np.mean((t_abs[t_abs > q95]**2)) / (np.mean(t_abs**2)+1e-12)) if np.any(t_abs > q95) else 0.0

    def mean(rows, key): return float(np.nanmean([r[key] for r in rows]))
    out = {
        "traj": traj_name, "tr": tr, "delay": delay, "mc": mc,
        "rmse_honest": mean(h_rows, 'rmse'),
        "rmse_t3": mean(t_rows, 'rmse'),
        "gap_h_minus_t3": mean(h_rows, 'rmse') - mean(t_rows, 'rmse'),
        "osc_honest": mean(h_rows, 'osc_std'),
        "osc_t3": mean(t_rows, 'osc_std'),
        "osc_change_pct": (mean(t_rows, 'osc_std') - mean(h_rows, 'osc_std')) / (mean(h_rows, 'osc_std')+1e-12) * 100,
        "edot_honest": mean(h_rows, 'edot_rms'),
        "edot_t3": mean(t_rows, 'edot_rms'),
        "edot_change_pct": (mean(t_rows, 'edot_rms') - mean(h_rows, 'edot_rms')) / (mean(h_rows, 'edot_rms')+1e-12) * 100,
        "tail_q95_honest": q95,
        "tail_rate_honest": h_tail,
        "tail_rate_t3": t_tail,
        "tail_delta": t_tail - h_tail,
        "tail_mse_share_honest": h_tail_mse_share,
        "tail_mse_share_t3": t_tail_mse_share,
        "energy_relief": mean(p_rows, 'energy_relief'),
        "abs_relief": mean(p_rows, 'abs_relief'),
        "vel_oppose": mean(p_rows, 'vel_oppose'),
        "delta_perp_abs": mean(p_rows, 'delta_perp_abs'),
        "delta_norm": mean(p_rows, 'delta_norm'),
        "raw_cos_vel": mean(p_rows, 'raw_cos_vel'),
    }
    # Mechanism classification. Conservative thresholds avoid overclaiming near zero.
    gap = out['gap_h_minus_t3']
    relief = out['energy_relief']
    vopp = out['vel_oppose']
    taild = out['tail_delta']
    if gap > 0:
        cls = 'benefit'
    elif relief < -0.05 or out['abs_relief'] < -0.02:
        cls = 'harm_with_local_reversal'
    elif taild > 0.03 or out['osc_change_pct'] > 10 or out['edot_change_pct'] > 10:
        cls = 'harm_cost_dominance'
    else:
        cls = 'harm_or_neutral_unclear'
    out['mechanism_class'] = cls
    return out


def parse_csv_list(s: str, cast=str):
    if s is None or s == '': return []
    return [cast(x.strip()) for x in s.split(',') if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', nargs='?', default='quick', choices=['quick','full','custom'])
    ap.add_argument('--trajs', default=None, help='comma list, e.g. circle,square,lemniscate,zigzag')
    ap.add_argument('--trs', default=None, help='comma list, e.g. 0.20,0.30,0.40')
    ap.add_argument('--delays', default=None, help='comma list, e.g. 0,8,18,26,34,44,56,68')
    ap.add_argument('--mc', type=int, default=None)
    ap.add_argument('--N', type=int, default=50)
    args = ap.parse_args()

    if args.mode == 'quick':
        trajs = ['circle'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.30] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [0,8,18,26,34,44,56,68] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 10 if args.mc is None else args.mc
    elif args.mode == 'full':
        trajs = ['circle','square','lemniscate','zigzag'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.20,0.30,0.40] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [0,8,18,26,34,44,56,68] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 50 if args.mc is None else args.mc
    else:
        trajs = ['circle'] if args.trajs is None else parse_csv_list(args.trajs)
        trs = [0.30] if args.trs is None else parse_csv_list(args.trs, float)
        delays = [0,8,18,26,34,44,56,68] if args.delays is None else parse_csv_list(args.delays, int)
        mc = 20 if args.mc is None else args.mc

    outdir = os.path.join(HERE, 'results')
    os.makedirs(outdir, exist_ok=True)
    rows=[]
    total = len(trajs)*len(trs)*len(delays)
    k=0
    print(f"[closure_probe] mode={args.mode} trajs={trajs} trs={trs} delays={delays} mc={mc} cells={total}")
    for tn in trajs:
        for tr in trs:
            for d in delays:
                k += 1
                row = summarize_cell(tn, tr, d, mc, N=args.N)
                rows.append(row)
                print(f"[{k:03d}/{total}] {tn:10} tr={tr:.2f} d={d:2d} gap={row['gap_h_minus_t3']:+.3f} "
                      f"relief={row['energy_relief']:+.3f} vopp={row['vel_oppose']:+.3f} "
                      f"osc%={row['osc_change_pct']:+.1f} edot%={row['edot_change_pct']:+.1f} "
                      f"tailΔ={row['tail_delta']:+.3f} class={row['mechanism_class']}")

    csv_path = os.path.join(outdir, 't3_closure_probe_summary.csv')
    json_path = os.path.join(outdir, 't3_closure_probe_summary.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader(); writer.writerows(rows)
    print(f"\nsaved:\n  {csv_path}\n  {json_path}")

if __name__ == '__main__':
    main()
