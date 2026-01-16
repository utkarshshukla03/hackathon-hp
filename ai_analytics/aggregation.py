import pandas as pd
from pathlib import Path


# -----------------------------
# Output path (LOCKED)
# -----------------------------
OUTPUT_PATH = Path("data/processed/cost_analytics.csv")


def aggregate_costs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates cost data at item, region, and supplier level.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned and merged purchase order dataframe.

    Returns
    -------
    pd.DataFrame
        Aggregated cost analytics dataframe.
    """

    # -----------------------------
    # Required columns check
    # -----------------------------
    required_cols = [
        "item_code",
        "canonical_item_name",
        "region",
        "supplier",
        "unit_price",
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(
            f"Aggregation input missing columns: {sorted(missing)}"
        )

    # -----------------------------
    # Perform aggregation
    # -----------------------------
    agg_df = (
        df.groupby(
            ["item_code", "canonical_item_name", "region", "supplier"],
            as_index=False
        )
        .agg(
            avg_price=("unit_price", "mean"),
            median_price=("unit_price", "median"),
            min_price=("unit_price", "min"),
            max_price=("unit_price", "max"),
            price_std=("unit_price", "std"),
        )
    )

    # -----------------------------
    # Handle single-observation std
    # -----------------------------
    agg_df["price_std"] = agg_df["price_std"].fillna(0.0)

    # -----------------------------
    # Save output
    # -----------------------------
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    agg_df.to_csv(OUTPUT_PATH, index=False)

    return agg_df
