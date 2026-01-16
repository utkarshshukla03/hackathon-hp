import pandas as pd
from pathlib import Path


# -----------------------------
# Output path (LOCKED)
# -----------------------------
OUTPUT_PATH = Path("data/processed/anomalies.csv")

# -----------------------------
# Detection thresholds
# -----------------------------
STD_MULTIPLIER = 2.5
ABSOLUTE_THRESHOLD_RATIO = 0.20  # 20% deviation


def detect_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detects price anomalies at PO level.

    Strategy:
    - If price variance exists: use std-based rule
    - If no variance: use absolute deviation rule

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and merged purchase order dataframe.

    Returns
    -------
    pd.DataFrame
        Anomalies dataframe.
    """

    required_cols = [
        "po_id",
        "item_code",
        "unit_price",
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(
            f"Anomaly detection input missing columns: {sorted(missing)}"
        )

    anomaly_records = []

    # -----------------------------
    # Process per item_code
    # -----------------------------
    for item_code, group in df.groupby("item_code"):
        median_price = group["unit_price"].median()
        std_price = group["unit_price"].std()

        # Safety guard
        if pd.isna(median_price):
            continue

        for _, row in group.iterrows():
            deviation = abs(row["unit_price"] - median_price)

            # Case 1: Standard deviation available
            if std_price and not pd.isna(std_price) and std_price > 0:
                threshold = STD_MULTIPLIER * std_price
                is_anomaly = deviation > threshold
                reason = (
                    f"Deviation exceeds {STD_MULTIPLIER}× standard deviation"
                )

            # Case 2: No variance fallback
            else:
                threshold = ABSOLUTE_THRESHOLD_RATIO * median_price
                is_anomaly = deviation > threshold
                reason = (
                    f"Deviation exceeds "
                    f"{int(ABSOLUTE_THRESHOLD_RATIO*100)}% of median price"
                )

            if is_anomaly:
                anomaly_records.append({
                    "po_id": row["po_id"],
                    "item_code": item_code,
                    "unit_price": row["unit_price"],
                    "expected_price": median_price,
                    "anomaly_flag": True,
                    "anomaly_reason": reason,
                })

    anomaly_df = pd.DataFrame(anomaly_records)

    # Ensure columns exist even if empty
    if anomaly_df.empty:
        anomaly_df = pd.DataFrame(columns=[
            "po_id", "item_code", "unit_price", "expected_price",
            "anomaly_flag", "anomaly_reason"
        ])

    # -----------------------------
    # Save output
    # -----------------------------
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    anomaly_df.to_csv(OUTPUT_PATH, index=False)

    return anomaly_df
