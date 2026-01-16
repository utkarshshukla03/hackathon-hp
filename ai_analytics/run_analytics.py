from load_data import load_data
from price_cleaning import clean_and_merge
from aggregation import aggregate_costs
from trend_analysis import add_trend_labels
from anomaly_detection import detect_anomalies


def main():
    print("Starting cost analytics pipeline...")

    # -----------------------------
    # Step 1: Load data
    # -----------------------------
    print("Loading input data...")
    raw_df, std_df = load_data()

    # -----------------------------
    # Step 2: Clean & merge
    # -----------------------------
    print("Cleaning and merging data...")
    clean_df = clean_and_merge(raw_df, std_df)

    if clean_df.empty:
        raise RuntimeError("Cleaned dataframe is empty. Check input data.")

    # -----------------------------
    # Step 3: Cost aggregation
    # -----------------------------
    print("Aggregating cost data...")
    cost_df = aggregate_costs(clean_df)

    # -----------------------------
    # Step 4: Trend analysis
    # -----------------------------
    print("Adding trend labels...")
    cost_df = add_trend_labels(cost_df)

    # Overwrite cost_analytics.csv with trend column added
    cost_df.to_csv("data/processed/cost_analytics.csv", index=False)

    # -----------------------------
    # Step 5: Anomaly detection
    # -----------------------------
    print("Detecting anomalies...")
    detect_anomalies(clean_df)

    print("Pipeline completed successfully.")
    print("Outputs generated:")
    print("- data/processed/cost_analytics.csv")
    print("- data/processed/anomalies.csv")


if __name__ == "__main__":
    main()
