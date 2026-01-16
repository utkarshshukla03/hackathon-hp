import pandas as pd


def clean_and_merge(raw_df: pd.DataFrame, std_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merges raw purchase order data with standardized item data
    and performs basic data cleaning.

    Parameters
    ----------
    raw_df : pd.DataFrame
        Raw purchase order data.
    std_df : pd.DataFrame
        Standardized item mapping.

    Returns
    -------
    pd.DataFrame
        Cleaned and merged dataframe ready for analytics.
    """

    # -----------------------------
    # Ensure category exists (backward compatible)
    # -----------------------------
    if "category" not in std_df.columns:
        std_df["category"] = "UNKNOWN"

    # -----------------------------
    # Merge on po_id
    # -----------------------------
    df = raw_df.merge(
        std_df[
            [
                "po_id",
                "item_code",
                "canonical_item_name",
                "confidence_score",
                "category",  # NEW (future-ready metadata)
            ]
        ],
        on="po_id",
        how="inner",
        validate="many_to_one"
    )

    # -----------------------------
    # Drop invalid price rows
    # -----------------------------
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df[df["unit_price"] > 0]

    # -----------------------------
    # Clean quantity (validated for future use)
    # -----------------------------
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df = df[df["quantity"].notna()]

    # -----------------------------
    # Parse and validate dates
    # -----------------------------
    df["po_date"] = pd.to_datetime(df["po_date"], errors="coerce")
    df = df[df["po_date"].notna()]

    # -----------------------------
    # Trim whitespace in key string fields
    # -----------------------------
    text_cols = [
        "item_code",
        "canonical_item_name",
        "category",      # NEW
        "region",
        "department",
        "supplier",
        "unit",
    ]

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # -----------------------------
    # Final sanity checks
    # -----------------------------
    required_cols = [
        "po_id",
        "item_code",
        "canonical_item_name",
        "category",      # NEW
        "unit_price",
        "po_date",
        "region",
        "supplier",
    ]

    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(
            f"Post-cleaning dataframe missing columns: {sorted(missing)}"
        )

    return df
