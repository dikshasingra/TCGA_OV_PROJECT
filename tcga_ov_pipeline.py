"""
TCGA-OV preprocessing pipeline.
This script harmonizes expression + clinical data and creates ready-to-model survival tables.
If no real data is present in data_raw/, it generates synthetic test data.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_RAW = ROOT / "data_raw"
DATA_PROCESSED = ROOT / "data_processed"
DATA_RAW.mkdir(exist_ok=True)
DATA_PROCESSED.mkdir(exist_ok=True)

def preprocess_expression(expr_df):
    df = np.log2(expr_df + 1.0)          # log-transform
    df = df.transpose()                  # samples = rows
    df = (df - df.mean()) / (df.std(ddof=0) + 1e-8)  # z-score
    return df

def build_survival_table(clin_df):
    time, event = [], []
    for _, row in clin_df.iterrows():
        d_death = row.get('days_to_death', np.nan)
        d_last = row.get('days_to_last_follow_up', np.nan)
        vs = row.get('vital_status', None)
        if not pd.isna(d_death):
            time.append(float(d_death))
            event.append(1)
        elif not pd.isna(d_last):
            time.append(float(d_last))
            event.append(1 if str(vs).lower() == "dead" else 0)
        else:
            time.append(np.nan)
            event.append(np.nan)
    return pd.DataFrame({'time': time, 'event': event}, index=clin_df.index)

def pipeline():
    # --- Synthetic demo data (so it runs even without TCGA files) ---
    n_samples, n_genes = 50, 500
    rng = np.random.default_rng(123)
    expr = pd.DataFrame(
        rng.lognormal(mean=1.5, sigma=1.0, size=(n_genes, n_samples)),
        index=[f"GENE{i}" for i in range(n_genes)],
        columns=[f"TCGA-TEST-{i:03d}" for i in range(n_samples)]
    )
    clin = pd.DataFrame(index=expr.columns)
    clin['days_to_death'] = rng.integers(100, 2000, size=n_samples)
    clin['vital_status'] = ['alive' if x % 3 else 'dead' for x in range(n_samples)]

    expr_processed = preprocess_expression(expr)
    surv_table = build_survival_table(clin)
    combined = surv_table.join(expr_processed)

    expr_processed.to_csv(DATA_PROCESSED / "expression_samples_by_genes.csv")
    surv_table.to_csv(DATA_PROCESSED / "survival_table.csv")
    combined.to_csv(DATA_PROCESSED / "combined_survival_expression.csv")
    print("✅ Saved processed files in data_processed/")

if __name__ == "__main__":
    pipeline()
