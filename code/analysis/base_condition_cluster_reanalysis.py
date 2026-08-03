from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "base_condition_cluster_reanalysis"
SRC = ROOT / "data" / "final_structural_audit" / "sscrn_vote_events_with_counterfactual.csv"


OUTCOME = "counterfactual_event_cost_sscrn"
BASE_TERMS = ["intercept", "q_coarseness", "vote_event", "path_event", "q_x_vote", "q_x_path", "vote_x_path"]


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    work = df.dropna(subset=[OUTCOME]).copy()
    work["vote_event"] = work["vote_event"].astype(float)
    work["path_event"] = work["path_event"].astype(float)
    work["delay"] = work["delay"].astype(int)
    work["tr"] = work["tr"].astype(float)
    return work


def design_matrix(df: pd.DataFrame, adjusted: bool) -> tuple[np.ndarray, list[str]]:
    q = df["q_coarseness"].to_numpy(float)
    vote = df["vote_event"].to_numpy(float)
    path = df["path_event"].to_numpy(float)
    cols = [
        np.ones(len(df)),
        q,
        vote,
        path,
        q * vote,
        q * path,
        vote * path,
    ]
    names = BASE_TERMS.copy()

    if adjusted:
        traj_d = pd.get_dummies(df["traj"], prefix="traj", drop_first=True, dtype=float)
        delay_d = pd.get_dummies(df["delay"], prefix="delay", drop_first=True, dtype=float)
        tr_d = pd.get_dummies(df["tr"], prefix="tr", drop_first=True, dtype=float)
        for frame in [traj_d, delay_d, tr_d]:
            for col in frame.columns:
                cols.append(frame[col].to_numpy(float))
                names.append(str(col))

    return np.column_stack(cols), names


def ols_beta(df: pd.DataFrame, adjusted: bool) -> tuple[np.ndarray, list[str]]:
    X, names = design_matrix(df, adjusted)
    y = df[OUTCOME].to_numpy(float)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return beta, names


def cluster_bootstrap(df: pd.DataFrame, cluster_col: str, adjusted: bool, draws: int = 2000) -> tuple[pd.DataFrame, pd.DataFrame]:
    beta, names = ols_beta(df, adjusted)
    clusters = df[cluster_col].drop_duplicates().to_numpy()
    grouped = {k: g for k, g in df.groupby(cluster_col, sort=False)}
    rng = np.random.default_rng(20260731)
    boot = np.empty((draws, len(beta)))
    for i in range(draws):
        sampled = rng.choice(clusters, size=len(clusters), replace=True)
        sample = pd.concat([grouped[c] for c in sampled], ignore_index=True)
        boot[i, :] = ols_beta(sample, adjusted)[0]
    rows = []
    for j, name in enumerate(names):
        rows.append(
            {
                "model": "adjusted" if adjusted else "base",
                "cluster": cluster_col,
                "term": name,
                "estimate": float(beta[j]),
                "ci95_low": float(np.percentile(boot[:, j], 2.5)),
                "ci95_high": float(np.percentile(boot[:, j], 97.5)),
                "excludes_zero": bool(np.percentile(boot[:, j], 2.5) > 0 or np.percentile(boot[:, j], 97.5) < 0),
            }
        )
    return pd.DataFrame(rows), pd.DataFrame(boot, columns=names)


def compare_cluster_levels(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cluster_col in ["paired_id", "base_condition_id"]:
        for adjusted in [False, True]:
            model, _ = cluster_bootstrap(df, cluster_col, adjusted, draws=1000)
            rows.append(model[model["term"].isin(BASE_TERMS)])
    return pd.concat(rows, ignore_index=True)


def event_class_sparsity(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["q_dirs", "traj", "event_class"], as_index=False)
        .agg(
            rows=("event_class", "size"),
            base_conditions=("base_condition_id", "nunique"),
            mean_cost=(OUTCOME, "mean"),
            positive_tail=("positive_counterfactual_event_cost_sscrn", "mean"),
        )
        .sort_values(["event_class", "q_dirs", "traj"])
    )


def write_route_verdict(all_models: pd.DataFrame, sparsity: pd.DataFrame) -> None:
    final = all_models[
        (all_models["cluster"] == "base_condition_id")
        & (all_models["model"] == "adjusted")
        & (all_models["term"].isin(["q_x_vote", "vote_x_path", "q_x_path", "path_event"]))
    ].copy()
    qxv = final[final["term"] == "q_x_vote"].iloc[0]
    vxp = final[final["term"] == "vote_x_path"].iloc[0]
    survives = bool(qxv["excludes_zero"] and vxp["excludes_zero"])
    sparse_min = int(sparsity["rows"].min())
    pd.DataFrame(
        [
            {
                "verdict": "BASE_CONDITION_CLUSTER_REPAIR_SURVIVES" if survives else "BASE_CONDITION_CLUSTER_REPAIR_WEAKENS_INTERACTION",
                "adjusted_base_cluster_q_x_vote_estimate": float(qxv["estimate"]),
                "adjusted_base_cluster_q_x_vote_ci_low": float(qxv["ci95_low"]),
                "adjusted_base_cluster_q_x_vote_ci_high": float(qxv["ci95_high"]),
                "adjusted_base_cluster_vote_x_path_estimate": float(vxp["estimate"]),
                "adjusted_base_cluster_vote_x_path_ci_low": float(vxp["ci95_low"]),
                "adjusted_base_cluster_vote_x_path_ci_high": float(vxp["ci95_high"]),
                "minimum_event_class_rows": sparse_min,
                "note": "base_condition_id clustered bootstrap; covariate adjusted; not validation",
            }
        ]
    ).to_csv(OUT / "base_cluster_route_verdict.csv", index=False)


def main() -> None:
    df = prepare(pd.read_csv(SRC))
    all_models = compare_cluster_levels(df)
    sparsity = event_class_sparsity(df)

    # Full 2000-draw final tables for the corrected cluster level.
    base_model, base_boot = cluster_bootstrap(df, "base_condition_id", adjusted=False, draws=2000)
    adj_model, adj_boot = cluster_bootstrap(df, "base_condition_id", adjusted=True, draws=2000)

    all_models.to_csv(OUT / "cluster_level_model_comparison.csv", index=False)
    base_model.to_csv(OUT / "base_condition_cluster_base_model.csv", index=False)
    adj_model.to_csv(OUT / "base_condition_cluster_adjusted_model.csv", index=False)
    base_boot.to_csv(OUT / "base_condition_cluster_base_bootstrap_draws.csv", index=False)
    adj_boot.to_csv(OUT / "base_condition_cluster_adjusted_bootstrap_draws.csv", index=False)
    sparsity.to_csv(OUT / "event_class_sparsity_by_q_traj.csv", index=False)
    write_route_verdict(adj_model, sparsity)


if __name__ == "__main__":
    main()
