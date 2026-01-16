import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import pandas as pd

from text_cleaning import clean_text
from attribute_extraction import extract_attributes
from embeddings import generate_embeddings
from clustering import cluster_items_with_diagnostics
from item_code_generator import generate_item_code
from category_tagging import assign_category


RAW_PATH = "data/raw/purchase_orders_raw.csv"
OUT_PATH = "data/processed/standardized_items.csv"

def confidence_from_cluster(size):
    if size == 1:
        return 0.75
    if size <= 3:
        return 0.85
    return 0.95

def main():
    df = pd.read_csv(RAW_PATH)

    df["clean_text"] = df["item_description"].apply(clean_text)
    df["attributes"] = df["clean_text"].apply(extract_attributes)

    embeddings = generate_embeddings(df["clean_text"].tolist())
    labels, diagnostics = cluster_items_with_diagnostics(embeddings)
    df["cluster"] = labels


    canonical_map = {}
    confidence_map = {}

    for cluster_id, group in df.groupby("cluster"):
        canonical_name = group.iloc[0]["clean_text"]
        item_code = generate_item_code(canonical_name)
        canonical_map[cluster_id] = (canonical_name, item_code)
        confidence_map[cluster_id] = confidence_from_cluster(len(group))

    df["canonical_item_name"] = df["cluster"].apply(lambda x: canonical_map[x][0])
    df["category"] = df["canonical_item_name"].apply(assign_category)
    df["item_code"] = df["cluster"].apply(lambda x: canonical_map[x][1])
    df["confidence_score"] = df["cluster"].apply(lambda x: confidence_map[x])

    out_df = df[
        ["po_id", "item_description", "canonical_item_name", "item_code", "category", "confidence_score"]
    ]

    out_df.to_csv(OUT_PATH, index=False)

    print("Raw items", len(df))
    print("Canonical items", df["item_code"].nunique())
    print("Reduction percent", round(
        100 * (1 - df["item_code"].nunique() / len(df)), 2
    ))

    print("\nCluster diagnostics")
    for cluster_id, stats in diagnostics.items():
        print(
            "Cluster",
            cluster_id,
            "Size",
            stats["cluster_size"],
            "Avg similarity",
            stats["avg_similarity"]
        )

if __name__ == "__main__":
    main()
