from __future__ import annotations

import hashlib
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "final_structural_audit"
sys.path.insert(0, str(SCRIPT_DIR))

import crn_pairing_interaction_repair as R  # noqa: E402


Q_DIRS = R.Q_DIRS
TRAJS = R.TRAJS
TRS = R.TRS
DELAYS = R.DELAYS
MC = R.MC
N_VOTES = R.N_VOTES
N_AGENTS = R.N_AGENTS


def child_seed(label: str, traj: str, tr: float, delay: int, rep: int) -> int:
    key = f"stream-separated|{label}|{traj}|{tr:.4f}|{delay}|{rep}".encode("utf-8")
    return 410_000_000 + int(hashlib.sha256(key).hexdigest()[:10], 16) % 80_000_000


@dataclass(frozen=True)
class StreamSeparatedSchedule:
    tr: float
    active_noise: np.ndarray
    sluggish_u: np.ndarray
    other_noise: np.ndarray
    honest_troll_noise: np.ndarray

    @classmethod
    def make(cls, traj: str, tr: float, delay: int, rep: int) -> "StreamSeparatedSchedule":
        na, ns, no, nt = R.counts_for_tr(tr)
        honest_rng = np.random.default_rng(child_seed("honest_agents", traj, tr, delay, rep))
        troll_rng = np.random.default_rng(child_seed("honest_trolls", traj, tr, delay, rep))
        return cls(
            tr=tr,
            active_noise=honest_rng.uniform(-3.0, 3.0, size=(N_VOTES, max(na, 1))),
            sluggish_u=honest_rng.uniform(0.2, 0.5, size=(N_VOTES, max(ns, 1))),
            other_noise=honest_rng.uniform(-30.0, 30.0, size=(N_VOTES, max(no, 1))),
            honest_troll_noise=troll_rng.uniform(-3.0, 3.0, size=(N_VOTES, max(nt, 1))),
        )

    def honest_block(self, vote_round: int, iang: float, pang: float, dir_degrees: np.ndarray) -> tuple[np.ndarray, int]:
        na, ns, no, nt = R.counts_for_tr(self.tr)
        angs = np.empty(na + ns + no, dtype=float)
        i = 0
        if na > 0:
            angs[i : i + na] = iang + self.active_noise[vote_round, :na]
            i += na
        diff = iang - pang
        if diff > 180.0:
            diff -= 360.0
        if diff < -180.0:
            diff += 360.0
        if ns > 0:
            angs[i : i + ns] = pang + diff * (1.0 - self.sluggish_u[vote_round, :ns])
            i += ns
        if no > 0:
            angs[i : i + no] = iang + self.other_noise[vote_round, :no]
            i += no
        return R.A.angle_to_bin(angs[:i], dir_degrees), nt

    def honest_trolls(self, vote_round: int, iang: float, nt: int, dir_degrees: np.ndarray) -> np.ndarray:
        if nt <= 0:
            return np.array([], dtype=int)
        return R.A.angle_to_bin(iang + self.honest_troll_noise[vote_round, :nt], dir_degrees)


def simulate_stream(traj: str, q_dirs: int, tr: float, delay: int, rep: int, mode: str, schedule: StreamSeparatedSchedule):
    dirs, dir_degrees = R.A.make_dirs(q_dirs)
    path = R.A.make_path(traj)
    pos = path.start()
    vel = np.zeros(2)
    pos_hist = [pos.copy()]
    pang = 0.0
    cur_dir = np.array([1.0, 0.0])
    prev_votes: np.ndarray | None = None
    prev_agg_cell: int | None = None
    pub_hist: list[float] = []
    rows = []
    err2_post = []
    vote_round = 0

    for frame in range(R.FRAMES):
        delayed_idx = max(0, len(pos_hist) - 1 - delay)
        delayed_pos = pos_hist[delayed_idx]
        _, delayed_arc = path.closest(delayed_pos)
        cp_pre, arc_pre = path.closest(pos)
        err2_pre = float(np.sum((pos - cp_pre) ** 2))

        if frame % R.VOTE_INT == 0:
            flags = R.A.path_flags(traj, path, pos, delayed_arc)
            lookahead = path.at(delayed_arc + R.LOOK)
            idir = lookahead - delayed_pos
            n = float(np.linalg.norm(idir))
            if n > 1e-10:
                idir = idir / n
            iang = math.degrees(math.atan2(float(idir[1]), float(idir[0])))

            honest, nt = schedule.honest_block(vote_round, iang, pang, dir_degrees)
            pang = iang

            if mode == "T3" and nt > 0:
                pubprev = pub_hist[-1] if len(pub_hist) >= 1 else None
                base = iang if pubprev is None else pubprev
                nc = int(math.floor(R.COHERENCE * nt))
                nd = nt - nc
                anti = R.A.angle_to_bin(np.asarray([base + 180.0]), dir_degrees)[0]
                trolls = np.concatenate(
                    [
                        np.full(nc, anti, dtype=int),
                        np.array([], dtype=int) if nd == 0 else np.zeros(nd, dtype=int),
                    ]
                )
            elif nt > 0:
                trolls = schedule.honest_trolls(vote_round, iang, nt, dir_degrees)
            else:
                trolls = np.array([], dtype=int)

            votes = np.concatenate([honest, trolls])
            agg = dirs[votes].mean(axis=0)
            agg_norm = float(np.linalg.norm(agg))
            cur_dir = R.A.unit(agg, fallback=cur_dir)
            heading = math.atan2(float(cur_dir[1]), float(cur_dir[0]))
            agg_cell = R.A.heading_to_cell(heading, q_dirs)
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
            vote_event = float(any_vote_switch > 0.0 or agg_cell_switch > 0.0)
            rows.append(
                {
                    "paired_id": f"sscrn_{traj}_tr{tr:.2f}_d{delay}_rep{rep}_q{q_dirs}",
                    "base_condition_id": f"sscrn_{traj}_tr{tr:.2f}_d{delay}_rep{rep}",
                    "mode": mode,
                    "q_dirs": q_dirs,
                    "q_coarseness": 1.0 / q_dirs,
                    "traj": traj,
                    "tr": tr,
                    "delay": delay,
                    "rep": rep,
                    "vote_round": vote_round,
                    "frame": frame,
                    "err2_pre_vote": err2_pre,
                    "vote_bin_switch_rate": vote_switch_rate,
                    "vote_switch_chord2_mean": vote_switch_chord2_mean,
                    "agg_cell_switch": agg_cell_switch,
                    "agg_cell_jump_chord2": agg_cell_jump_chord2,
                    "agg_norm": agg_norm,
                    "path_event": path_event,
                    "endpoint_wrap": float(flags["endpoint_wrap"]),
                    "branch_event": float(flags["branch_event"]),
                    "vote_event": vote_event,
                    "vote_path_coincident": float(path_event > 0.0 and vote_event > 0.0),
                    "vote_only_event": float(vote_event > 0.0 and path_event == 0.0),
                    "path_only_event": float(path_event > 0.0 and vote_event == 0.0),
                    "quiet_event": float(path_event == 0.0 and vote_event == 0.0),
                }
            )
            prev_votes = votes.copy()
            prev_agg_cell = agg_cell
            vote_round += 1

        vel += R.SMOOTH * (cur_dir * R.MSPD - vel)
        pos = pos + vel * R.DT
        pos_hist.append(pos.copy())
        cp_post, _ = path.closest(pos)
        err2_post.append(float(np.sum((pos - cp_post) ** 2)))

    out = pd.DataFrame(rows).sort_values(["paired_id", "mode", "vote_round"]).copy()
    out["err2_pre_next_vote"] = out.groupby(["paired_id", "mode"])["err2_pre_vote"].shift(-1)
    out["err2_increment_next_vote"] = out["err2_pre_next_vote"] - out["err2_pre_vote"]
    out["positive_err2_increment_next_vote"] = out["err2_increment_next_vote"].clip(lower=0.0)
    return float(math.sqrt(np.mean(err2_post))), out


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


def run_dataset():
    sim_rows = []
    event_parts = []
    for traj in TRAJS:
        for tr in TRS:
            for delay in DELAYS:
                for rep in range(MC):
                    schedule = StreamSeparatedSchedule.make(traj, tr, delay, rep)
                    for q_dirs in Q_DIRS:
                        rmse_t3, ev_t3 = simulate_stream(traj, q_dirs, tr, delay, rep, "T3", schedule)
                        rmse_h, ev_h = simulate_stream(traj, q_dirs, tr, delay, rep, "honest", schedule)
                        t3 = add_event_class(ev_t3[ev_t3["mode"] == "T3"].copy())
                        h = ev_h[ev_h["mode"] == "honest"][
                            ["paired_id", "vote_round", "err2_increment_next_vote", "positive_err2_increment_next_vote"]
                        ].rename(
                            columns={
                                "err2_increment_next_vote": "err2_increment_next_vote_honest",
                                "positive_err2_increment_next_vote": "positive_err2_increment_next_vote_honest",
                            }
                        )
                        merged = t3.merge(h, on=["paired_id", "vote_round"], how="left")
                        merged["counterfactual_event_cost_sscrn"] = (
                            merged["err2_increment_next_vote"] - merged["err2_increment_next_vote_honest"]
                        )
                        merged["positive_counterfactual_event_cost_sscrn"] = merged["counterfactual_event_cost_sscrn"].clip(lower=0.0)
                        event_parts.append(merged)
                        sim_rows.append(
                            {
                                "base_condition_id": f"sscrn_{traj}_tr{tr:.2f}_d{delay}_rep{rep}",
                                "paired_id": f"sscrn_{traj}_tr{tr:.2f}_d{delay}_rep{rep}_q{q_dirs}",
                                "q_dirs": q_dirs,
                                "traj": traj,
                                "tr": tr,
                                "delay": delay,
                                "rep": rep,
                                "rmse_t3": rmse_t3,
                                "rmse_honest": rmse_h,
                                "rmse_gap_t3_minus_honest": rmse_t3 - rmse_h,
                            }
                        )
    events = pd.concat(event_parts, ignore_index=True)
    sim = pd.DataFrame(sim_rows)
    per_sim = (
        events.groupby(["q_dirs", "traj", "tr", "delay", "rep", "paired_id", "base_condition_id"], as_index=False)
        .agg(
            vote_bin_switch_rate=("vote_bin_switch_rate", "mean"),
            vote_switch_chord2_mean=("vote_switch_chord2_mean", "mean"),
            agg_cell_switch_rate=("agg_cell_switch", "mean"),
            agg_cell_jump_chord2_mean=("agg_cell_jump_chord2", "mean"),
            path_event_rate=("path_event", "mean"),
            endpoint_wrap_rate=("endpoint_wrap", "mean"),
            branch_event_rate=("branch_event", "mean"),
            vote_path_coincident_rate=("vote_path_coincident", "mean"),
            positive_err2_increment_t3=("positive_err2_increment_next_vote", "mean"),
            counterfactual_event_cost_sscrn=("counterfactual_event_cost_sscrn", "mean"),
            positive_counterfactual_event_cost_sscrn=("positive_counterfactual_event_cost_sscrn", "mean"),
        )
    ).merge(sim, on=["q_dirs", "traj", "tr", "delay", "rep", "paired_id", "base_condition_id"], how="left")
    return sim, per_sim, events


def summarize(per_sim: pd.DataFrame):
    metrics = [
        "vote_bin_switch_rate",
        "vote_switch_chord2_mean",
        "agg_cell_switch_rate",
        "agg_cell_jump_chord2_mean",
        "path_event_rate",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_sscrn",
        "positive_counterfactual_event_cost_sscrn",
        "rmse_gap_t3_minus_honest",
    ]
    qsum = per_sim.groupby("q_dirs", as_index=False)[metrics].mean()
    qsum["q_coarseness"] = 1.0 / qsum["q_dirs"]
    return qsum


def directional_tests(qsum: pd.DataFrame):
    qs = qsum.sort_values("q_coarseness")
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_sscrn",
        "positive_counterfactual_event_cost_sscrn",
    ]
    rows = []
    for metric in metrics:
        rho = R.spearman(qs["q_coarseness"], qs[metric])
        fine = float(qs.iloc[0][metric])
        coarse = float(qs.iloc[-1][metric])
        rows.append(
            {
                "test": f"q_coarseness_to_{metric}",
                "expected": "positive",
                "spearman": rho,
                "fine_16_value": fine,
                "coarse_4_value": coarse,
                "coarse_minus_fine": coarse - fine,
                "pass": bool(rho > 0 and coarse > fine),
            }
        )
    return pd.DataFrame(rows)


def contrast_ci(per_sim: pd.DataFrame):
    rng = np.random.default_rng(20260731)
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_sscrn",
        "positive_counterfactual_event_cost_sscrn",
    ]
    wide = per_sim.pivot_table(index=["traj", "tr", "delay", "rep"], columns="q_dirs", values=metrics, aggfunc="mean")
    rows = []
    for metric in metrics:
        diff = (wide[(metric, 4)] - wide[(metric, 16)]).dropna().to_numpy()
        lo, hi = R.bootstrap_ci(diff, rng)
        rows.append(
            {
                "contrast": "q4_minus_q16_stream_separated_crn",
                "metric": metric,
                "mean": float(np.mean(diff)),
                "ci95_low": lo,
                "ci95_high": hi,
                "n_clusters": int(len(diff)),
                "fraction_positive": float(np.mean(diff > 0.0)),
            }
        )
    return pd.DataFrame(rows)


def event_summary(events: pd.DataFrame):
    return (
        events.groupby(["q_dirs", "traj", "event_class"], as_index=False)
        .agg(
            rows=("event_class", "size"),
            vote_switch_chord2_mean=("vote_switch_chord2_mean", "mean"),
            agg_cell_jump_chord2_mean=("agg_cell_jump_chord2", "mean"),
            positive_err2_increment_t3=("positive_err2_increment_next_vote", "mean"),
            counterfactual_event_cost_sscrn=("counterfactual_event_cost_sscrn", "mean"),
            positive_counterfactual_event_cost_sscrn=("positive_counterfactual_event_cost_sscrn", "mean"),
        )
    )


def condition_consistency(per_sim: pd.DataFrame):
    metrics = [
        "vote_switch_chord2_mean",
        "agg_cell_jump_chord2_mean",
        "vote_path_coincident_rate",
        "positive_err2_increment_t3",
        "counterfactual_event_cost_sscrn",
        "positive_counterfactual_event_cost_sscrn",
    ]
    wide = per_sim.pivot_table(index=["traj", "tr", "delay", "rep"], columns="q_dirs", values=metrics, aggfunc="mean")
    rows = []
    for metric in metrics:
        base = (wide[(metric, 4)] - wide[(metric, 16)]).dropna().reset_index(name="q4_minus_q16")
        groups = [("overall", base)]
        groups.extend((f"traj={k}", g) for k, g in base.groupby("traj"))
        groups.extend((f"delay={k}", g) for k, g in base.groupby("delay"))
        groups.extend((f"tr={k}", g) for k, g in base.groupby("tr"))
        for label, group in groups:
            rows.append(
                {
                    "metric": metric,
                    "group": label,
                    "n": int(len(group)),
                    "mean_q4_minus_q16": float(group["q4_minus_q16"].mean()),
                    "fraction_q4_gt_q16": float((group["q4_minus_q16"] > 0.0).mean()),
                }
            )
    return pd.DataFrame(rows)


def ols_beta(df: pd.DataFrame):
    work = df.dropna(subset=["counterfactual_event_cost_sscrn"]).copy()
    q = work["q_coarseness"].to_numpy(float)
    vote = work["vote_event"].to_numpy(float)
    path = work["path_event"].to_numpy(float)
    X = np.column_stack([np.ones(len(work)), q, vote, path, q * vote, q * path, vote * path])
    names = ["intercept", "q_coarseness", "vote_event", "path_event", "q_x_vote", "q_x_path", "vote_x_path"]
    y = work["counterfactual_event_cost_sscrn"].to_numpy(float)
    return np.linalg.lstsq(X, y, rcond=None)[0], names


def interaction_bootstrap(events: pd.DataFrame, b: int = 1000):
    work = events.dropna(subset=["counterfactual_event_cost_sscrn"]).copy()
    beta, names = ols_beta(work)
    clusters = work["paired_id"].drop_duplicates().to_numpy()
    grouped = {k: g for k, g in work.groupby("paired_id", sort=False)}
    rng = np.random.default_rng(20260731)
    draws = np.empty((b, len(beta)))
    for i in range(b):
        sampled = rng.choice(clusters, size=len(clusters), replace=True)
        sample = pd.concat([grouped[c] for c in sampled], ignore_index=True)
        draws[i, :] = ols_beta(sample)[0]
    rows = []
    for j, name in enumerate(names):
        rows.append(
            {
                "term": name,
                "estimate": float(beta[j]),
                "ci95_low": float(np.percentile(draws[:, j], 2.5)),
                "ci95_high": float(np.percentile(draws[:, j], 97.5)),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(draws, columns=names)


def plot_outputs(qsum: pd.DataFrame, events: pd.DataFrame):
    fig_dir = OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    q = qsum.sort_values("q_dirs")
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    axes[0, 0].plot(q["q_dirs"], q["vote_bin_switch_rate"], marker="o", label="frequency")
    axes[0, 0].plot(q["q_dirs"], q["vote_switch_chord2_mean"], marker="o", label="magnitude")
    axes[0, 0].legend(frameon=False)
    axes[0, 0].set_title("Stream-separated CRN trade-off")
    axes[0, 1].plot(q["q_dirs"], q["counterfactual_event_cost_sscrn"], marker="o")
    axes[0, 1].set_title("Mean CRN event cost")
    axes[1, 0].plot(q["q_dirs"], q["positive_counterfactual_event_cost_sscrn"], marker="o")
    axes[1, 0].set_title("Positive CRN cost tail")
    agg = events.groupby(["q_dirs", "event_class"], as_index=False)["counterfactual_event_cost_sscrn"].mean()
    for ev, group in agg.groupby("event_class"):
        axes[1, 1].plot(group["q_dirs"], group["counterfactual_event_cost_sscrn"], marker="o", label=ev)
    axes[1, 1].legend(frameon=False, fontsize=8)
    axes[1, 1].set_title("Event-class interaction")
    for ax in axes.ravel():
        ax.set_xticks(Q_DIRS)
        ax.set_xlabel("quantizer directions")
        ax.grid(alpha=0.25)
    fig.suptitle("Stream-separated CRN final gate", fontweight="bold")
    plt.savefig(fig_dir / "stream_separated_crn_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def main():
    sim, per_sim, events = run_dataset()
    qsum = summarize(per_sim)
    tests = directional_tests(qsum)
    contrasts = contrast_ci(per_sim)
    esum = event_summary(events)
    consistency = condition_consistency(per_sim)
    model, draws = interaction_bootstrap(events)
    plot_outputs(qsum, events)

    sim.to_csv(OUT / "sscrn_sim_summary.csv", index=False)
    per_sim.to_csv(OUT / "sscrn_per_sim_metrics.csv", index=False)
    events.to_csv(OUT / "sscrn_vote_events_with_counterfactual.csv", index=False)
    qsum.to_csv(OUT / "sscrn_q_summary.csv", index=False)
    tests.to_csv(OUT / "sscrn_directional_tests.csv", index=False)
    contrasts.to_csv(OUT / "sscrn_coarse_fine_contrast_ci.csv", index=False)
    esum.to_csv(OUT / "sscrn_event_class_summary.csv", index=False)
    consistency.to_csv(OUT / "sscrn_condition_consistency.csv", index=False)
    model.to_csv(OUT / "sscrn_interaction_model_cluster_bootstrap.csv", index=False)
    draws.to_csv(OUT / "sscrn_interaction_model_bootstrap_draws.csv", index=False)

    c = contrasts.set_index("metric")
    pd.DataFrame(
        [
            {
                "verdict": "STREAM_SEPARATED_CRN_GATE_COMPLETED",
                "directional_pass_count": int(tests["pass"].sum()),
                "directional_total": int(len(tests)),
                "primary_vote_burden_q4_minus_q16": float(c.loc["vote_switch_chord2_mean", "mean"]),
                "primary_vote_burden_ci_low": float(c.loc["vote_switch_chord2_mean", "ci95_low"]),
                "primary_vote_burden_ci_high": float(c.loc["vote_switch_chord2_mean", "ci95_high"]),
                "mean_counterfactual_q4_minus_q16": float(c.loc["counterfactual_event_cost_sscrn", "mean"]),
                "mean_counterfactual_ci_low": float(c.loc["counterfactual_event_cost_sscrn", "ci95_low"]),
                "mean_counterfactual_ci_high": float(c.loc["counterfactual_event_cost_sscrn", "ci95_high"]),
                "positive_counterfactual_tail_q4_minus_q16": float(c.loc["positive_counterfactual_event_cost_sscrn", "mean"]),
                "positive_counterfactual_tail_ci_low": float(c.loc["positive_counterfactual_event_cost_sscrn", "ci95_low"]),
                "positive_counterfactual_tail_ci_high": float(c.loc["positive_counterfactual_event_cost_sscrn", "ci95_high"]),
                "note": "stream-separated CRN; not validation; not global RMSE closure",
            }
        ]
    ).to_csv(OUT / "sscrn_route_verdict.csv", index=False)


if __name__ == "__main__":
    main()
