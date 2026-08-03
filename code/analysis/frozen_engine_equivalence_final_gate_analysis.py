from __future__ import annotations

import hashlib
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "frozen_engine_equivalence"
FIG_OUT = ROOT / "figures" / "manuscript_png"
CORE = ROOT / "code" / "fixed_engine_core" / "core"
sys.path.insert(0, str(CORE))

import adversary_ladder as AL  # noqa: E402
import t3_confirmatory as TC  # noqa: E402


DT = AL.DT
MSPD = AL.MSPD
SMOOTH = AL.SMOOTH
LOOK = AL.LOOK
VOTE_INT = AL.VOTE_INT
FRAMES = 1800
N_AGENTS = 50
COHERENCE = 1.0
MC = 8
Q_DIRS = [4, 8, 16]
TRAJS = ["circle", "square", "zigzag", "lemniscate"]
TRS = [0.25, 0.35]
DELAYS = [12, 34]
RADIUS = 0.5


def make_dirs(m: int) -> tuple[np.ndarray, np.ndarray]:
    if m == 8:
        return AL.DIRS.copy(), AL.DA.copy()
    angles = np.linspace(0.0, 2.0 * math.pi, m, endpoint=False)
    dirs = np.column_stack([np.cos(angles), np.sin(angles)]).astype(float)
    deg = np.degrees(angles) % 360.0
    return dirs, deg


def unit(v: np.ndarray, fallback: np.ndarray | None = None) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n > 1e-12:
        return v / n
    return np.array([1.0, 0.0]) if fallback is None else fallback.copy()


def wrap_pi(x: float) -> float:
    return math.atan2(math.sin(x), math.cos(x))


def circular_abs_delta(a: float, b: float) -> float:
    return abs(wrap_pi(a - b))


def angle_to_bin(angles_deg: np.ndarray, dir_degrees: np.ndarray) -> np.ndarray:
    a = angles_deg % 360.0
    d = np.abs(dir_degrees[None, :] - a[:, None])
    d = np.minimum(d, 360.0 - d)
    return np.argmin(d, axis=1)


def heading_to_cell(theta_rad: float, m: int) -> int:
    angle = theta_rad % (2.0 * math.pi)
    return int(np.floor((angle + math.pi / m) / (2.0 * math.pi / m))) % m


def boundary_margin_norm(theta_rad: float, m: int) -> float:
    cell = heading_to_cell(theta_rad, m)
    center = 2.0 * math.pi * cell / m
    half_width = math.pi / m
    dist = circular_abs_delta(theta_rad, center)
    return float(np.clip(max(0.0, half_width - dist) / half_width, 0.0, 1.0))


def stable_seed(q_dirs: int, traj: str, tr: float, delay: int, rep: int) -> int:
    key = f"{q_dirs}|{traj}|{tr:.4f}|{delay}|{rep}".encode("utf-8")
    return 210_000_000 + int(hashlib.sha256(key).hexdigest()[:10], 16) % 80_000_000


def make_path(traj: str):
    if traj == "circle":
        return AL.Circle()
    if traj == "square":
        return AL.Square()
    if traj == "zigzag":
        return AL.Zigzag()
    if traj == "lemniscate":
        return AL.Lemniscate()
    raise ValueError(traj)


def frame_at(path, arc: float) -> tuple[np.ndarray, np.ndarray]:
    eps = 0.05
    tangent = unit(path.at(arc + eps) - path.at(arc - eps))
    normal = np.array([-tangent[1], tangent[0]])
    return tangent, normal


def second_projection_lemniscate(path, p: np.ndarray):
    pts = path.pts
    d = np.linalg.norm(pts - p, axis=1)
    i1 = int(np.argmin(d))
    idx = np.arange(len(pts))
    circ_dist = np.minimum(np.abs(idx - i1), len(pts) - np.abs(idx - i1))
    masked = d.copy()
    masked[circ_dist < 35] = np.inf
    i2 = int(np.argmin(masked))
    t1, _ = frame_at(path, float(path.arcs[i1]))
    t2, _ = frame_at(path, float(path.arcs[i2]))
    arc_sep = float(abs(path.arcs[i1] - path.arcs[i2]))
    arc_sep = min(arc_sep, path.circ - arc_sep)
    return {
        "d1": float(d[i1]),
        "d2": float(d[i2]),
        "arc_sep": arc_sep,
        "tangent_disagreement": float(1.0 - abs(np.clip(float(t1 @ t2), -1.0, 1.0))),
    }


def path_flags(traj: str, path, pos: np.ndarray, delayed_arc: float) -> dict[str, float]:
    if traj == "circle":
        return {"path_event": 0.0, "endpoint_wrap": 0.0, "branch_event": 0.0}
    _, arc = path.closest(pos)
    if traj == "square":
        corners = np.asarray([10.0, 30.0, 50.0, 70.0])
        return {
            "path_event": float(np.min(np.abs(corners - arc)) <= RADIUS),
            "endpoint_wrap": 0.0,
            "branch_event": 0.0,
        }
    if traj == "zigzag":
        corners = np.asarray(path.cum[1:-1], dtype=float)
        dist = float(np.min(np.abs(corners - arc))) if len(corners) else math.inf
        return {
            "path_event": float(dist <= RADIUS),
            "endpoint_wrap": float(delayed_arc >= path.circ - LOOK),
            "branch_event": 0.0,
        }
    if traj == "lemniscate":
        sec = second_projection_lemniscate(path, pos)
        event = (
            sec["d2"] - sec["d1"] <= 0.75
            and sec["arc_sep"] >= 5.0
            and sec["tangent_disagreement"] >= 0.25
        )
        return {"path_event": float(event), "endpoint_wrap": 0.0, "branch_event": float(event)}
    raise ValueError(traj)


def honest_block_q(iang: float, pang: float, tr: float, rng: np.random.Generator, dir_degrees: np.ndarray) -> tuple[np.ndarray, int]:
    sc = (1.0 - tr) / 0.95
    na = round(N_AGENTS * 0.70 * sc)
    ns = round(N_AGENTS * 0.20 * sc)
    nt = round(N_AGENTS * tr)
    no = max(0, N_AGENTS - na - ns - nt)
    angs = np.empty(na + ns + no, dtype=float)
    i = 0
    angs[i : i + na] = iang + rng.uniform(-3.0, 3.0, na)
    i += na
    diff = iang - pang
    if diff > 180.0:
        diff -= 360.0
    if diff < -180.0:
        diff += 360.0
    if ns > 0:
        angs[i : i + ns] = pang + diff * (1.0 - rng.uniform(0.2, 0.5, ns))
        i += ns
    if no > 0:
        angs[i : i + no] = iang + rng.uniform(-30.0, 30.0, no)
        i += no
    return angle_to_bin(angs[:i], dir_degrees), nt


def simulate_logged(traj: str, q_dirs: int, tr: float, delay: int, rep: int, seed: int, mode: str) -> tuple[float, pd.DataFrame]:
    dirs, dir_degrees = make_dirs(q_dirs)
    path = make_path(traj)
    rng = np.random.default_rng(seed)
    pos = path.start()
    vel = np.zeros(2)
    pos_hist = [pos.copy()]
    pang = 0.0
    cur_dir = np.array([1.0, 0.0])
    prev_votes: np.ndarray | None = None
    prev_agg_cell: int | None = None
    pub_hist: list[float] = []
    vote_rows: list[dict[str, float | int | str]] = []
    err2_post: list[float] = []
    vote_round = 0

    for frame in range(FRAMES):
        delayed_idx = max(0, len(pos_hist) - 1 - delay)
        delayed_pos = pos_hist[delayed_idx]
        _, delayed_arc = path.closest(delayed_pos)
        cp_pre, arc_pre = path.closest(pos)
        err2_pre = float(np.sum((pos - cp_pre) ** 2))

        if frame % VOTE_INT == 0:
            flags = path_flags(traj, path, pos, delayed_arc)
            lookahead = path.at(delayed_arc + LOOK)
            idir = lookahead - delayed_pos
            idir_norm = float(np.linalg.norm(idir))
            if idir_norm > 1e-10:
                idir = idir / idir_norm
            iang = math.degrees(math.atan2(float(idir[1]), float(idir[0])))
            if q_dirs == 8:
                honest, nt = AL._honest_block(iang, pang, tr, N_AGENTS, rng)
            else:
                honest, nt = honest_block_q(iang, pang, tr, rng, dir_degrees)
            pang = iang

            if mode == "T3" and nt > 0:
                pubprev = pub_hist[-1] if len(pub_hist) >= 1 else None
                base = iang if pubprev is None else pubprev
                nc = int(math.floor(COHERENCE * nt))
                nd = nt - nc
                anti = angle_to_bin(np.asarray([base + 180.0]), dir_degrees)[0]
                trolls = np.concatenate(
                    [
                        np.full(nc, anti, dtype=int),
                        rng.integers(0, q_dirs, nd) if nd > 0 else np.array([], dtype=int),
                    ]
                )
            elif nt > 0:
                trolls = angle_to_bin(iang + rng.uniform(-3.0, 3.0, nt), dir_degrees)
            else:
                trolls = np.array([], dtype=int)

            votes = np.concatenate([honest, trolls])
            agg = dirs[votes].mean(axis=0)
            agg_norm = float(np.linalg.norm(agg))
            cur_dir = unit(agg, fallback=cur_dir)
            heading = math.atan2(float(cur_dir[1]), float(cur_dir[0]))
            agg_cell = heading_to_cell(heading, q_dirs)
            pub_hist.append(math.degrees(heading))

            if prev_votes is None:
                vote_switch_rate = 0.0
                vote_switch_count = 0.0
                vote_switch_chord2_mean = 0.0
                any_vote_switch = 0.0
            else:
                changed = votes != prev_votes
                vote_switch_count = float(np.sum(changed))
                vote_switch_rate = float(np.mean(changed))
                jump_vec = dirs[votes] - dirs[prev_votes]
                vote_switch_chord2_mean = float(np.mean(np.sum(jump_vec * jump_vec, axis=1)))
                any_vote_switch = float(vote_switch_count > 0)

            if prev_agg_cell is None:
                agg_cell_switch = 0.0
                agg_cell_jump_chord2 = 0.0
            else:
                agg_cell_switch = float(agg_cell != prev_agg_cell)
                agg_jump = dirs[agg_cell] - dirs[prev_agg_cell]
                agg_cell_jump_chord2 = float(np.sum(agg_jump * agg_jump))

            path_event = float(flags["path_event"])
            vote_or_agg_switch = float(any_vote_switch > 0.0 or agg_cell_switch > 0.0)
            coincident = float(path_event > 0.0 and vote_or_agg_switch > 0.0)
            vote_rows.append(
                {
                    "sim_id": f"q{q_dirs}_{traj}_tr{tr:.2f}_d{delay}_rep{rep}_{mode}",
                    "paired_id": f"q{q_dirs}_{traj}_tr{tr:.2f}_d{delay}_rep{rep}",
                    "mode": mode,
                    "q_dirs": q_dirs,
                    "q_coarseness": 1.0 / q_dirs,
                    "traj": traj,
                    "tr": tr,
                    "delay": delay,
                    "rep": rep,
                    "vote_round": vote_round,
                    "frame": frame,
                    "s_current": arc_pre,
                    "s_delayed": delayed_arc,
                    "err2_pre_vote": err2_pre,
                    "vote_bin_switch_rate": vote_switch_rate,
                    "vote_bin_switch_count": vote_switch_count,
                    "vote_switch_chord2_mean": vote_switch_chord2_mean,
                    "any_vote_bin_switch": any_vote_switch,
                    "agg_cell_idx": agg_cell,
                    "agg_cell_switch": agg_cell_switch,
                    "agg_cell_jump_chord2": agg_cell_jump_chord2,
                    "agg_norm": agg_norm,
                    "agg_boundary_margin_norm": boundary_margin_norm(heading, q_dirs),
                    "agg_boundary_proximity": 1.0 - boundary_margin_norm(heading, q_dirs),
                    "path_event": path_event,
                    "endpoint_wrap": float(flags["endpoint_wrap"]),
                    "branch_event": float(flags["branch_event"]),
                    "vote_path_coincident": coincident,
                    "vote_only_event": float(vote_or_agg_switch > 0.0 and path_event == 0.0),
                    "path_only_event": float(path_event > 0.0 and vote_or_agg_switch == 0.0),
                    "quiet_event": float(path_event == 0.0 and vote_or_agg_switch == 0.0),
                }
            )
            prev_votes = votes.copy()
            prev_agg_cell = agg_cell
            vote_round += 1

        vel += SMOOTH * (cur_dir * MSPD - vel)
        pos = pos + vel * DT
        pos_hist.append(pos.copy())
        cp_post, _ = path.closest(pos)
        err2_post.append(float(np.sum((pos - cp_post) ** 2)))

    vote_df = pd.DataFrame(vote_rows)
    vote_df = vote_df.sort_values(["sim_id", "vote_round"]).copy()
    vote_df["err2_pre_next_vote"] = vote_df.groupby("sim_id")["err2_pre_vote"].shift(-1)
    vote_df["err2_increment_next_vote"] = vote_df["err2_pre_next_vote"] - vote_df["err2_pre_vote"]
    vote_df["positive_err2_increment_next_vote"] = vote_df["err2_increment_next_vote"].clip(lower=0.0)
    return float(math.sqrt(np.mean(err2_post))), vote_df


def add_event_class(df: pd.DataFrame) -> pd.DataFrame:
    conditions = [
        df["vote_path_coincident"] > 0,
        df["vote_only_event"] > 0,
        df["path_only_event"] > 0,
        df["quiet_event"] > 0,
    ]
    labels = ["vote_path_coincident", "vote_only", "path_only", "quiet"]
    df = df.copy()
    df["event_class"] = np.select(conditions, labels, default="unclassified")
    return df


def run_frozen_equivalence() -> pd.DataFrame:
    old_frames = AL.FRAMES
    AL.FRAMES = FRAMES
    rows = []
    try:
        for traj in TRAJS:
            for tr in TRS:
                for delay in DELAYS:
                    for rep in range(4):
                        seed = stable_seed(8, traj, tr, delay, rep)
                        for mode, ref_mode in [("T3", "T3pub"), ("honest", "honest")]:
                            rmse_logged, _ = simulate_logged(traj, 8, tr, delay, rep, seed, mode)
                            rmse_ref = TC.sim_u(TC.TRAJ[traj], N_AGENTS, tr, seed, ref_mode, ctrl_delay_f=delay)
                            rows.append(
                                {
                                    "traj": traj,
                                    "tr": tr,
                                    "delay": delay,
                                    "rep": rep,
                                    "mode": mode,
                                    "rmse_reference_engine": rmse_ref,
                                    "rmse_frozen_instrumented": rmse_logged,
                                    "abs_diff": abs(rmse_ref - rmse_logged),
                                }
                            )
    finally:
        AL.FRAMES = old_frames
    return pd.DataFrame(rows)


def run_dataset() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sim_rows = []
    event_rows = []
    for q in Q_DIRS:
        for traj in TRAJS:
            for tr in TRS:
                for delay in DELAYS:
                    for rep in range(MC):
                        seed = stable_seed(q, traj, tr, delay, rep)
                        rmse_t3, t3_events = simulate_logged(traj, q, tr, delay, rep, seed, "T3")
                        rmse_hon, hon_events = simulate_logged(traj, q, tr, delay, rep, seed, "honest")
                        t3 = add_event_class(t3_events[t3_events["mode"] == "T3"].copy())
                        hon = hon_events[hon_events["mode"] == "honest"][
                            ["paired_id", "vote_round", "err2_increment_next_vote", "positive_err2_increment_next_vote"]
                        ].rename(
                            columns={
                                "err2_increment_next_vote": "err2_increment_next_vote_honest",
                                "positive_err2_increment_next_vote": "positive_err2_increment_next_vote_honest",
                            }
                        )
                        merged = t3.merge(hon, on=["paired_id", "vote_round"], how="left")
                        merged["counterfactual_event_cost"] = (
                            merged["err2_increment_next_vote"] - merged["err2_increment_next_vote_honest"]
                        )
                        merged["positive_counterfactual_event_cost"] = merged["counterfactual_event_cost"].clip(lower=0.0)
                        event_rows.append(merged)
                        sim_rows.append(
                            {
                                "q_dirs": q,
                                "traj": traj,
                                "tr": tr,
                                "delay": delay,
                                "rep": rep,
                                "paired_id": f"q{q}_{traj}_tr{tr:.2f}_d{delay}_rep{rep}",
                                "rmse_t3": rmse_t3,
                                "rmse_honest": rmse_hon,
                                "rmse_gap_t3_minus_honest": rmse_t3 - rmse_hon,
                            }
                        )
    events = pd.concat(event_rows, ignore_index=True)
    sim = pd.DataFrame(sim_rows)
    per_sim = (
        events.groupby(["q_dirs", "traj", "tr", "delay", "rep", "paired_id"], as_index=False)
        .agg(
            vote_bin_switch_rate=("vote_bin_switch_rate", "mean"),
            vote_switch_chord2_mean=("vote_switch_chord2_mean", "mean"),
            agg_cell_switch_rate=("agg_cell_switch", "mean"),
            agg_cell_jump_chord2_mean=("agg_cell_jump_chord2", "mean"),
            agg_boundary_proximity_mean=("agg_boundary_proximity", "mean"),
            path_event_rate=("path_event", "mean"),
            endpoint_wrap_rate=("endpoint_wrap", "mean"),
            branch_event_rate=("branch_event", "mean"),
            vote_path_coincident_rate=("vote_path_coincident", "mean"),
            positive_err2_increment_t3=("positive_err2_increment_next_vote", "mean"),
            positive_err2_increment_honest=("positive_err2_increment_next_vote_honest", "mean"),
            counterfactual_event_cost_mean=("counterfactual_event_cost", "mean"),
            positive_counterfactual_event_cost=("positive_counterfactual_event_cost", "mean"),
        )
    )
    per_sim = per_sim.merge(sim, on=["q_dirs", "traj", "tr", "delay", "rep", "paired_id"], how="left")
    return sim, per_sim, events


def q_summary(per_sim: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "vote_bin_switch_rate",
        "vote_switch_chord2_mean",
        "agg_cell_switch_rate",
        "agg_cell_jump_chord2_mean",
        "agg_boundary_proximity_mean",
        "path_event_rate",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_mean",
        "positive_counterfactual_event_cost",
        "rmse_t3",
        "rmse_honest",
        "rmse_gap_t3_minus_honest",
    ]
    out = per_sim.groupby("q_dirs", as_index=False)[cols].mean()
    out["q_coarseness"] = 1.0 / out["q_dirs"]
    return out


def event_class_summary(events: pd.DataFrame) -> pd.DataFrame:
    return (
        events.groupby(["q_dirs", "traj", "event_class"], as_index=False)
        .agg(
            rows=("event_class", "size"),
            vote_switch_chord2_mean=("vote_switch_chord2_mean", "mean"),
            agg_cell_jump_chord2_mean=("agg_cell_jump_chord2", "mean"),
            boundary_proximity=("agg_boundary_proximity", "mean"),
            positive_err2_increment_t3=("positive_err2_increment_next_vote", "mean"),
            positive_err2_increment_honest=("positive_err2_increment_next_vote_honest", "mean"),
            counterfactual_event_cost=("counterfactual_event_cost", "mean"),
            positive_counterfactual_event_cost=("positive_counterfactual_event_cost", "mean"),
        )
    )


def spearman(x: pd.Series, y: pd.Series) -> float:
    xr = x.rank(method="average")
    yr = y.rank(method="average")
    if xr.nunique() <= 1 or yr.nunique() <= 1:
        return float("nan")
    return float(np.corrcoef(xr, yr)[0, 1])


def directional_tests(qsum: pd.DataFrame) -> pd.DataFrame:
    qs = qsum.sort_values("q_coarseness")
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_mean",
    ]
    rows = []
    for metric in metrics:
        rho = spearman(qs["q_coarseness"], qs[metric])
        fine = float(qs.iloc[0][metric])
        coarse = float(qs.iloc[-1][metric])
        rows.append(
            {
                "test": f"q_coarseness_to_{metric}",
                "expected": "positive",
                "spearman": rho,
                "fine_16_value": fine,
                "coarse_4_value": coarse,
                "pass": bool(rho > 0 and coarse > fine),
                "coarse_minus_fine": coarse - fine,
            }
        )
    return pd.DataFrame(rows)


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator, b: int = 2000) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan"), float("nan")
    draws = np.empty(b)
    n = len(values)
    for i in range(b):
        draws[i] = float(np.mean(values[rng.integers(0, n, n)]))
    return float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def bootstrap_tables(per_sim: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(20260731)
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_mean",
        "positive_counterfactual_event_cost",
    ]
    ci_rows = []
    for q, group in per_sim.groupby("q_dirs"):
        for metric in metrics:
            vals = group[metric].dropna().to_numpy()
            lo, hi = bootstrap_ci(vals, rng)
            ci_rows.append(
                {
                    "q_dirs": q,
                    "metric": metric,
                    "mean": float(np.mean(vals)),
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "n_clusters": int(len(vals)),
                }
            )
    ci = pd.DataFrame(ci_rows)

    wide = per_sim.pivot_table(
        index=["traj", "tr", "delay", "rep"],
        columns="q_dirs",
        values=metrics,
        aggfunc="mean",
    )
    contrast_rows = []
    for metric in metrics:
        vals = (wide[(metric, 4)] - wide[(metric, 16)]).dropna().to_numpy()
        lo, hi = bootstrap_ci(vals, rng)
        contrast_rows.append(
            {
                "contrast": "q4_minus_q16",
                "metric": metric,
                "mean": float(np.mean(vals)),
                "ci95_low": lo,
                "ci95_high": hi,
                "n_paired_clusters": int(len(vals)),
                "fraction_positive": float(np.mean(vals > 0.0)),
            }
        )
    contrast = pd.DataFrame(contrast_rows)
    return ci, contrast


def condition_consistency(per_sim: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_mean",
    ]
    wide = per_sim.pivot_table(
        index=["traj", "tr", "delay", "rep"],
        columns="q_dirs",
        values=metrics,
        aggfunc="mean",
    )
    rows = []
    for metric in metrics:
        diff = (wide[(metric, 4)] - wide[(metric, 16)]).dropna()
        base = diff.reset_index(name="q4_minus_q16")
        for keys, group in [("overall", base)]:
            rows.append(
                {
                    "metric": metric,
                    "group": keys,
                    "n": int(len(group)),
                    "mean_q4_minus_q16": float(group["q4_minus_q16"].mean()),
                    "fraction_q4_gt_q16": float((group["q4_minus_q16"] > 0).mean()),
                }
            )
        for traj, group in base.groupby("traj"):
            rows.append(
                {
                    "metric": metric,
                    "group": f"traj={traj}",
                    "n": int(len(group)),
                    "mean_q4_minus_q16": float(group["q4_minus_q16"].mean()),
                    "fraction_q4_gt_q16": float((group["q4_minus_q16"] > 0).mean()),
                }
            )
        for delay, group in base.groupby("delay"):
            rows.append(
                {
                    "metric": metric,
                    "group": f"delay={delay}",
                    "n": int(len(group)),
                    "mean_q4_minus_q16": float(group["q4_minus_q16"].mean()),
                    "fraction_q4_gt_q16": float((group["q4_minus_q16"] > 0).mean()),
                }
            )
        for tr, group in base.groupby("tr"):
            rows.append(
                {
                    "metric": metric,
                    "group": f"tr={tr}",
                    "n": int(len(group)),
                    "mean_q4_minus_q16": float(group["q4_minus_q16"].mean()),
                    "fraction_q4_gt_q16": float((group["q4_minus_q16"] > 0).mean()),
                }
            )
    return pd.DataFrame(rows)


def q_event_interaction(events: pd.DataFrame) -> pd.DataFrame:
    table = (
        events.groupby(["q_dirs", "event_class"], as_index=False)
        .agg(
            rows=("event_class", "size"),
            counterfactual_event_cost=("counterfactual_event_cost", "mean"),
            positive_counterfactual_event_cost=("positive_counterfactual_event_cost", "mean"),
            positive_err2_increment_t3=("positive_err2_increment_next_vote", "mean"),
        )
    )
    wide = table.pivot(index="event_class", columns="q_dirs", values="counterfactual_event_cost")
    contrasts = []
    for event_class, row in wide.iterrows():
        if 4 in row.index and 16 in row.index:
            contrasts.append(
                {
                    "event_class": event_class,
                    "counterfactual_q4_minus_q16": float(row[4] - row[16]),
                }
            )
    contrast = pd.DataFrame(contrasts)
    return table.merge(contrast, on="event_class", how="left")


def plot_outputs(qsum: pd.DataFrame, event_interaction: pd.DataFrame) -> None:
    fig_dir = FIG_OUT
    fig_dir.mkdir(parents=True, exist_ok=True)
    q = qsum.sort_values("q_dirs")
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    axes[0, 0].plot(q["q_dirs"], q["vote_bin_switch_rate"], marker="o", label="frequency")
    axes[0, 0].plot(q["q_dirs"], q["vote_switch_chord2_mean"], marker="o", label="magnitude burden")
    axes[0, 0].set_title("Frequency-magnitude trade-off")
    axes[0, 0].legend(frameon=False)
    axes[0, 1].plot(q["q_dirs"], q["agg_cell_jump_chord2_mean"], marker="o", color="#b45309")
    axes[0, 1].set_title("Aggregate jump burden")
    axes[1, 0].plot(q["q_dirs"], q["vote_path_coincident_rate"], marker="o", color="#047857")
    axes[1, 0].set_title("Path/vote co-occurrence")
    sub = event_interaction[event_interaction["q_dirs"].isin(Q_DIRS)]
    for ev, group in sub.groupby("event_class"):
        axes[1, 1].plot(group["q_dirs"], group["counterfactual_event_cost"], marker="o", label=ev)
    axes[1, 1].set_title("Counterfactual event cost")
    axes[1, 1].legend(frameon=False, fontsize=8)
    for ax in axes.ravel():
        ax.set_xlabel("quantizer directions")
        ax.grid(alpha=0.25)
        ax.set_xticks(Q_DIRS)
    fig.suptitle("Fixed-engine final gate: quantizer trade-off and event interaction", fontweight="bold")
    plt.savefig(fig_dir / "fixed_engine_final_gate_tradeoff_interaction.png", dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    equivalence = run_frozen_equivalence()
    equivalence.to_csv(OUT / "frozen_engine_equivalence.csv", index=False)

    sim, per_sim, events = run_dataset()
    qsum = q_summary(per_sim)
    esum = event_class_summary(events)
    tests = directional_tests(qsum)
    ci, contrast_ci = bootstrap_tables(per_sim)
    consistency = condition_consistency(per_sim)
    interaction = q_event_interaction(events)
    plot_outputs(qsum, interaction)

    sim.to_csv(OUT / "final_gate_sim_summary.csv", index=False)
    per_sim.to_csv(OUT / "final_gate_per_sim_metrics.csv", index=False)
    events.to_csv(OUT / "final_gate_vote_events_with_counterfactual.csv", index=False)
    qsum.to_csv(OUT / "final_gate_q_summary.csv", index=False)
    esum.to_csv(OUT / "final_gate_event_class_summary.csv", index=False)
    tests.to_csv(OUT / "final_gate_directional_tests.csv", index=False)
    ci.to_csv(OUT / "final_gate_cluster_bootstrap_ci.csv", index=False)
    contrast_ci.to_csv(OUT / "final_gate_coarse_fine_contrast_ci.csv", index=False)
    consistency.to_csv(OUT / "final_gate_condition_consistency.csv", index=False)
    interaction.to_csv(OUT / "final_gate_q_event_interaction.csv", index=False)

    eq_pass = bool(equivalence["abs_diff"].max() < 1e-10)
    strict_pass = int(tests["pass"].sum())
    verdict = "FROZEN_ENGINE_FINAL_GATE_PARTIAL_PASS"
    if eq_pass and strict_pass >= 3:
        verdict = "FROZEN_ENGINE_FINAL_GATE_TECHNICALLY_STRENGTHENED"
    pd.DataFrame(
        [
            {
                "verdict": verdict,
                "frozen_equivalence_pass": eq_pass,
                "max_equivalence_abs_diff": float(equivalence["abs_diff"].max()),
                "directional_pass_count": strict_pass,
                "directional_total": int(len(tests)),
                "note": "not validation; not global RMSE closure",
            }
        ]
    ).to_csv(OUT / "final_gate_route_verdict.csv", index=False)


if __name__ == "__main__":
    main()
