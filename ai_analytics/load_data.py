import pandas as pd
from pathlib import Path


# -----------------------------
# File paths (DO NOT CHANGE)
# -----------------------------
RAW_PO_PATH = Path("data/raw/purchase_orders_raw.csv")
STD_ITEMS_PATH = Path("data/processed/standardized_items.csv")


# -----------------------------
# Expected schemas (LOCKED)
# -----------------------------
RAW_PO_COLUMNS = [
    "po_id",
    "item_description",
    "unit_price",
    "quantity",
    "unit",
    "po_date",
    "region",
    "department",
    "supplier",
]

STD_ITEMS_COLUMNS = [
    "po_id",
    "item_code",
    "canonical_item_name",
    "confidence_score",
]


# -----------------------------
# Internal helpers
# -----------------------------
def _check_file_exists(path: Path):
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path.as_posix()}"
        )


def _check_schema(df: pd.DataFrame, expected_cols: list, file_name: str):
    missing = set(expected_cols) - set(df.columns)
    extra = set(df.columns) - set(expected_cols)

    if missing:
        raise ValueError(
            f"{file_name} is missing columns: {sorted(missing)}"
        )

    # Extra columns are allowed but warned
    if extra:
        print(
            f"Warning: {file_name} has extra columns "
            f"that will be ignored: {sorted(extra)}"
        )


# -----------------------------
# Public API
# -----------------------------
def load_data():
    """
    Loads and validates input CSV files.

    Returns
    -------
    raw_df : pd.DataFrame
        Raw purchase order data.
    std_df : pd.DataFrame
        Standardized item mapping.
    """

    # Check files exist
    _check_file_exists(RAW_PO_PATH)
    _check_file_exists(STD_ITEMS_PATH)

    # Load CSVs
    raw_df = pd.read_csv(RAW_PO_PATH)
    std_df = pd.read_csv(STD_ITEMS_PATH)

    # Validate schemas
    _check_schema(raw_df, RAW_PO_COLUMNS, "purchase_orders_raw.csv")
    _check_schema(std_df, STD_ITEMS_COLUMNS, "standardized_items.csv")

    # Return only expected columns (order preserved)
    raw_df = raw_df[RAW_PO_COLUMNS]
    std_df = std_df[STD_ITEMS_COLUMNS]

    return raw_df, std_df
