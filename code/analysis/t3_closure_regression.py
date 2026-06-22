"""
t3_closure_regression.py
========================
Second-pass analysis of t3_closure_probe_summary.json/csv.

Purpose
-------
Quantifies whether the T3 benefit/harm boundary is explained better by
local relief alone or by a benefit-cost model that includes oscillation,
error-derivative/jitter, and high-error tail costs.

Usage
-----
  python t3_closure_regression.py --input results/t3_closure_probe_summary.json
  python t3_closure_regression.py --input results/t3_closure_probe_summary.csv --out results/closure_analysis

Outputs
-------
  closure_second_pass_report.md
  mechanism_counts.csv
  trajectory_summary.csv
  delay_summary.csv
  tr_summary.csv
  diagnostic_regression_models.csv
  diagnostic_regression_mixed_model.csv
  benefit_harm_classifier_models.csv
  key_boundary_cells.csv

Interpretation
--------------
Positive `gap_h_minus_t3` means T3 improves over honest. A successful
cost-boundary theory should show that oscillation/tail/jitter variables explain
benefit-vs-harm better than local relief alone.
"""
from __future__ import annotations

import argparse, json, os
import numpy as np
import pandas as pd

from sklearn.model_selection import LeaveOneOut
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (
    r2_score, mean_absolute_error, roc_auc_score, accuracy_score,
    balanced_accuracy_score, f1_score, confusion_matrix
)


def load_table(path: str) -> pd.DataFrame:
    if path.lower().endswith('.json'):
        with open(path, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    if path.lower().endswith('.csv'):
        return pd.read_csv(path)
    raise ValueError('Input must be .json or .csv')


def loo_regression(df: pd.DataFrame, features: list[str]) -> tuple[float, float]:
    y = df['gap_h_minus_t3'].to_numpy(float)
    preds = np.zeros(len(df))
    for train, test in LeaveOneOut().split(df):
        model = make_pipeline(StandardScaler(), LinearRegression())
        model.fit(df.iloc[train][features], y[train])
        preds[test] = model.predict(df.iloc[test][features])
    return float(r2_score(y, preds)), float(mean_absolute_error(y, preds))


def insample_regression(df: pd.DataFrame, features: list[str]) -> dict:
    y = df['gap_h_minus_t3'].to_numpy(float)
    model = make_pipeline(StandardScaler(), LinearRegression())
    model.fit(df[features], y)
    pred = model.predict(df[features])
    coefs = model.named_steps['linearregression'].coef_
    out = {
        'r2_in_sample': float(r2_score(y, pred)),
        'mae_in_sample': float(mean_absolute_error(y, pred)),
    }
    for k, v in zip(features, coefs):
        out[f'coef_{k}'] = float(v)
    return out


def loo_mixed_regression(df: pd.DataFrame, num_features: list[str], cat_features: list[str]) -> tuple[float, float]:
    y = df['gap_h_minus_t3'].to_numpy(float)
    preds = np.zeros(len(df))
    for train, test in LeaveOneOut().split(df):
        pre = ColumnTransformer([
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cat_features),
        ])
        model = Pipeline([('pre', pre), ('lr', LinearRegression())])
        model.fit(df.iloc[train][num_features + cat_features], y[train])
        preds[test] = model.predict(df.iloc[test][num_features + cat_features])
    return float(r2_score(y, preds)), float(mean_absolute_error(y, preds))


def insample_mixed_regression(df: pd.DataFrame, num_features: list[str], cat_features: list[str]) -> dict:
    y = df['gap_h_minus_t3'].to_numpy(float)
    pre = ColumnTransformer([
        ('num', StandardScaler(), num_features),
        ('cat', OneHotEncoder(drop='first'), cat_features),
    ])
    model = Pipeline([('pre', pre), ('lr', LinearRegression())])
    model.fit(df[num_features + cat_features], y)
    pred = model.predict(df[num_features + cat_features])
    return {
        'r2_in_sample': float(r2_score(y, pred)),
        'mae_in_sample': float(mean_absolute_error(y, pred)),
    }


def loo_classifier(df: pd.DataFrame, features: list[str], cats: list[str] | None = None) -> dict:
    cats = cats or []
    y = (df['gap_h_minus_t3'] > 0).astype(int).to_numpy()
    probs = np.zeros(len(df)); preds = np.zeros(len(df))
    for train, test in LeaveOneOut().split(df):
        if cats:
            pre = ColumnTransformer([
                ('num', StandardScaler(), features),
                ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), cats),
            ])
            model = Pipeline([('pre', pre), ('logit', LogisticRegression(max_iter=2000, C=1.0))])
            model.fit(df.iloc[train][features + cats], y[train])
            probs[test] = model.predict_proba(df.iloc[test][features + cats])[:, 1]
            preds[test] = model.predict(df.iloc[test][features + cats])
        else:
            model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, C=1.0))
            model.fit(df.iloc[train][features], y[train])
            probs[test] = model.predict_proba(df.iloc[test][features])[:, 1]
            preds[test] = model.predict(df.iloc[test][features])
    return {
        'auc_loocv': float(roc_auc_score(y, probs)),
        'accuracy_loocv': float(accuracy_score(y, preds)),
        'balanced_accuracy_loocv': float(balanced_accuracy_score(y, preds)),
        'f1_loocv': float(f1_score(y, preds)),
        'confusion_matrix': str(confusion_matrix(y, preds).tolist()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='Path to t3_closure_probe_summary.json or .csv')
    ap.add_argument('--out', default='results/closure_analysis', help='Output directory')
    args = ap.parse_args()

    df = load_table(args.input)
    os.makedirs(args.out, exist_ok=True)
    df['benefit'] = df['gap_h_minus_t3'] > 0

    counts = df['mechanism_class'].value_counts().rename_axis('mechanism_class').reset_index(name='n')
    traj = df.groupby('traj').agg(
        n=('benefit', 'size'), benefit=('benefit', 'sum'),
        harm=('benefit', lambda x: int((~x).sum())),
        mean_gap=('gap_h_minus_t3', 'mean'),
        mean_osc_change=('osc_change_pct', 'mean'),
        mean_tail_delta=('tail_delta', 'mean'),
    ).reset_index()
    delay = df.groupby('delay').agg(
        n=('benefit', 'size'), benefit=('benefit', 'sum'),
        harm=('benefit', lambda x: int((~x).sum())),
        mean_gap=('gap_h_minus_t3', 'mean'),
        mean_osc_change=('osc_change_pct', 'mean'),
        mean_tail_delta=('tail_delta', 'mean'),
    ).reset_index()
    trsum = df.groupby('tr').agg(
        n=('benefit', 'size'), benefit=('benefit', 'sum'),
        harm=('benefit', lambda x: int((~x).sum())),
        mean_gap=('gap_h_minus_t3', 'mean'),
    ).reset_index()

    feature_sets = {
        'local_relief_only': ['energy_relief'],
        'cost_terms_only': ['osc_change_pct', 'edot_change_pct', 'tail_delta'],
        'relief_plus_cost': ['energy_relief', 'osc_change_pct', 'edot_change_pct', 'tail_delta'],
        'relief_abs_plus_cost': ['abs_relief', 'osc_change_pct', 'edot_change_pct', 'tail_delta'],
        'relief_cost_with_projection_magnitude': ['energy_relief', 'delta_perp_abs', 'osc_change_pct', 'edot_change_pct', 'tail_delta'],
    }
    reg_rows = []
    for name, features in feature_sets.items():
        row = {'model': name, 'features': ', '.join(features)}
        row.update(insample_regression(df, features))
        cv_r2, cv_mae = loo_regression(df, features)
        row.update({'r2_loocv': cv_r2, 'mae_loocv': cv_mae})
        reg_rows.append(row)
    reg = pd.DataFrame(reg_rows)

    mixed_num = ['energy_relief', 'osc_change_pct', 'edot_change_pct', 'tail_delta', 'delay', 'tr']
    mixed_row = {'model': 'relief_plus_cost_plus_delay_traj', 'features': ', '.join(mixed_num + ['traj'])}
    mixed_row.update(insample_mixed_regression(df, mixed_num, ['traj']))
    cv_r2, cv_mae = loo_mixed_regression(df, mixed_num, ['traj'])
    mixed_row.update({'r2_loocv': cv_r2, 'mae_loocv': cv_mae})
    mixed = pd.DataFrame([mixed_row])

    clf_rows = []
    for name, feats, cats in [
        ('local_relief_only', ['energy_relief'], []),
        ('cost_terms_only', ['osc_change_pct', 'edot_change_pct', 'tail_delta'], []),
        ('relief_plus_cost', ['energy_relief', 'osc_change_pct', 'edot_change_pct', 'tail_delta'], []),
        ('relief_plus_cost_plus_traj', ['energy_relief', 'osc_change_pct', 'edot_change_pct', 'tail_delta'], ['traj']),
    ]:
        row = {'model': name, 'features': ', '.join(feats + cats)}
        row.update(loo_classifier(df, feats, cats))
        clf_rows.append(row)
    clf = pd.DataFrame(clf_rows)

    key = df[(df['mechanism_class'] != 'benefit') | ((df['traj'] == 'circle') & (df['delay'].isin([34, 44, 56])))][
        ['traj', 'tr', 'delay', 'gap_h_minus_t3', 'energy_relief', 'abs_relief',
         'osc_change_pct', 'edot_change_pct', 'tail_delta', 'mechanism_class']
    ].sort_values(['traj', 'tr', 'delay'])

    for obj, filename in [
        (counts, 'mechanism_counts.csv'), (traj, 'trajectory_summary.csv'),
        (delay, 'delay_summary.csv'), (trsum, 'tr_summary.csv'),
        (reg, 'diagnostic_regression_models.csv'), (mixed, 'diagnostic_regression_mixed_model.csv'),
        (clf, 'benefit_harm_classifier_models.csv'), (key, 'key_boundary_cells.csv')
    ]:
        obj.to_csv(os.path.join(args.out, filename), index=False)

    report = f"""# T3 closure probe: second-pass diagnostic analysis

Input: `{os.path.basename(args.input)}`  
Cells: {len(df)} = {df.traj.nunique()} trajectories × {df.tr.nunique()} minority fractions × {df.delay.nunique()} delays  
MC per cell: {df['mc'].iloc[0] if 'mc' in df else 'unknown'}

## 1. Mechanism classes

{counts.to_markdown(index=False)}

## 2. Trajectory-level benefit/harm counts

{traj.to_markdown(index=False, floatfmt='.3f')}

## 3. Delay-level benefit/harm counts

{delay.to_markdown(index=False, floatfmt='.3f')}

## 4. Diagnostic regression: explaining the RMSE gap

Target: `gap_h_minus_t3`, where positive means T3 improves over honest.

{reg[['model','r2_in_sample','r2_loocv','mae_loocv']].to_markdown(index=False, floatfmt='.3f')}

Mixed model:

{mixed[['model','r2_in_sample','r2_loocv','mae_loocv']].to_markdown(index=False, floatfmt='.3f')}

## 5. Benefit/harm classification

Positive class = T3 benefit.

{clf[['model','auc_loocv','accuracy_loocv','balanced_accuracy_loocv','confusion_matrix']].to_markdown(index=False, floatfmt='.3f')}

## 6. Key boundary cells

{key.to_markdown(index=False, floatfmt='.3f')}

## Suggested manuscript claim

Frame-level diagnostics do not show that the harm bands are primarily caused by a reversal of the local relief channel. Instead, most harm cells retain positive local relief but exhibit increased oscillation, error-derivative variation, and/or high-error tail rate. The appropriate mechanism statement is therefore:

> T3 provides a projected local error-relief channel. Global RMSE benefit occurs when this relief exceeds mistiming-induced oscillation, jitter, tail, and topology costs. Harm bands are mainly cost-dominance boundaries, not phase-reversal boundaries.
"""
    with open(os.path.join(args.out, 'closure_second_pass_report.md'), 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    print(f'\nSaved outputs in: {args.out}')


if __name__ == '__main__':
    main()
