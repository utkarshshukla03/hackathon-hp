"""
Master Pipeline Script
Runs the complete data processing pipeline:
1. Item Standardization (AI/ML)
2. Cost Analytics Generation
3. Anomaly Detection

This script should be run whenever new purchase order data is added.
"""

import os
import sys
from pathlib import Path

# Suppress TensorFlow warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

print("=" * 70)
print("HPCL INTELLIGENT COST DATABASE - DATA PROCESSING PIPELINE")
print("=" * 70)

# Step 1: Item Standardization
print("\n[STEP 1/3] Running Item Standardization...")
print("-" * 70)
sys.path.insert(0, str(Path(__file__).parent / "ai_standardization"))
from ai_standardization.run_standardization import main as run_standardization
run_standardization()

# Step 2: Cost Analytics
print("\n[STEP 2/3] Running Cost Analytics Generation...")
print("-" * 70)
sys.path.insert(0, str(Path(__file__).parent / "ai_analytics"))
from ai_analytics.cost_aggregation import main as run_analytics
run_analytics()

# Step 3: Anomaly Detection
print("\n[STEP 3/3] Running Anomaly Detection...")
print("-" * 70)
from ai_analytics.anomaly_detection import main as run_anomaly_detection
run_anomaly_detection()

print("\n" + "=" * 70)
print("PIPELINE COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nGenerated files:")
print("  ✓ data/processed/standardized_items.csv")
print("  ✓ data/processed/cost_analytics.csv")
print("  ✓ data/processed/anomalies.csv")
print("\nYou can now run the dashboard:")
print("  streamlit run frontend/app.py")
print("=" * 70)
