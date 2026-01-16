import pandas as pd

# -----------------------------
# Volatility threshold
# -----------------------------
VOLATILITY_THRESHOLD = 0.15  # 15% coefficient of variation


def add_trend_labels(agg_df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns price stability trends based on volatility.

    Trend interpretation:
    - UP     : High price volatility (unstable pricing)
    - STABLE : Low price volatility (stable pricing)

    Parameters
    ----------
    agg_df : pd.DataFrame
        Aggregated cost dataframe.

    Returns
    -------
    pd.DataFrame
        Aggregated dataframe with trend_direction column.
    """

    required_cols = [
        "item_code",
        "avg_price",
        "price_std",
    ]

    missing = set(required_cols) - set(agg_df.columns)
    if missing:
        raise ValueError(
            f"Trend analysis input missing columns: {sorted(missing)}"
        )

    trend_map = {}

    # -----------------------------
    # Compute volatility per item
    # -----------------------------
    for item_code, group in agg_df.groupby("item_code"):
        mean_price = group["avg_price"].mean()
        std_price = group["price_std"].mean()

        # Safety checks
        if mean_price == 0 or pd.isna(mean_price) or pd.isna(std_price):
            trend_map[item_code] = "STABLE"
            continue

        coefficient_of_variation = std_price / mean_price

        if coefficient_of_variation > VOLATILITY_THRESHOLD:
            trend_map[item_code] = "UP"
        else:
            trend_map[item_code] = "STABLE"

    # -----------------------------
    # Assign labels
    # -----------------------------
    agg_df["trend_direction"] = agg_df["item_code"].map(trend_map)

    return agg_df
