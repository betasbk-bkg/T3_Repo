from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "data" / "final_structural_audit" / "sscrn_per_sim_metrics.csv"
OUT = ROOT / "data" / "final_structural_audit" / "table17_pairwise_q_contrasts_v41.csv"

METRICS = [
    ("mean vote-jump chord2 per vote opportunity", "vote_switch_chord2_mean"),
    ("aggregate jump chord2", "agg_cell_jump_chord2_mean"),
    ("path/vote co-occurrence", "vote_path_coincident_rate"),
    ("positive intervention error-squared increment", "positive_err2_increment_t3"),
    ("mean counterfactual event cost", "counterfactual_event_cost_sscrn"),
    ("mean positive-part counterfactual cost", "positive_counterfactual_event_cost_sscrn"),
]
CONTRASTS = [("q4_minus_q8", 4, 8), ("q8_minus_q16", 8, 16), ("q4_minus_q16", 4, 16)]


def main() -> None:
    df = pd.read_csv(SRC)
    clusters = np.array(sorted(df["base_condition_id"].unique()))
    q_index = {4: 0, 8: 1, 16: 2}
    draws = 2000
    seed = 20260802
    rng = np.random.default_rng(seed)
    sample_idx = rng.integers(0, len(clusters), size=(draws, len(clusters)))
    rows = []
    for label, col in METRICS:
        mat = df.pivot(index="base_condition_id", columns="q_dirs", values=col).loc[clusters, [4, 8, 16]].to_numpy(float)
        full = mat.mean(axis=0)
        boot_means = mat[sample_idx].mean(axis=1)
        for contrast, qa, qb in CONTRASTS:
            vals = boot_means[:, q_index[qa]] - boot_means[:, q_index[qb]]
            rows.append(
                {
                    "Metric": label,
                    "Contrast": contrast,
                    "Mean": float(full[q_index[qa]] - full[q_index[qb]]),
                    "95% CI low": float(np.percentile(vals, 2.5)),
                    "95% CI high": float(np.percentile(vals, 97.5)),
                    "n_clusters": int(len(clusters)),
                    "bootstrap_draws": draws,
                    "seed": seed,
                }
            )
    pd.DataFrame(rows).to_csv(OUT, index=False)


if __name__ == "__main__":
    main()
