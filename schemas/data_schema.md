# Intelligent Cost Database - Data Schema

## Overview
This document defines the data structure for the HPCL Intelligent Cost Database procurement transformation system.

---

## 1. purchase_orders_raw.csv
**Purpose**: Raw procurement order data from source systems (unstructured, messy)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| po_id | String | Unique Purchase Order Identifier | PO-2024-001 |
| item_description | String | Free-text item description (messy) | "Hydraulic Oil ISO VG 46" / "industrial lubricant oil" |
| unit_price | Float | Price per unit | 425.50 |
| quantity | Integer | Quantity ordered | 500 |
| unit | String | Unit of measurement | liter, piece, meter, sheet |
| po_date | Date | Purchase order date (YYYY-MM-DD) | 2024-01-15 |
| region | String | Geographical region | North, East, West, South |
| department | String | Department placing order | Operations, Maintenance, Production, Installation, Assembly |
| supplier | String | Supplier name | SyntheticTech Industries |

**Key Characteristics**:
- Item descriptions are **inconsistent** (same item written multiple ways)
- Serves as input for standardization pipeline
- May contain data quality issues

---

## 2. standardized_items.csv
**Purpose**: Standardized item mappings with confidence scores

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| po_id | String | Reference to original PO | PO-2024-001 |
| item_description | String | Original messy description | "industrial lubricant oil grade 46" |
| canonical_item_name | String | Standardized item name | Hydraulic Oil ISO VG 46 |
| item_code | String | Unique standardized code | HYD-OIL-46-001 |
| confidence_score | Float | AI confidence (0-1) | 0.98 |

**Key Characteristics**:
- Maps raw items to canonical forms
- Confidence scores indicate standardization quality
- Enables deduplication of procurement items

---

## 3. cost_analytics.csv
**Purpose**: Aggregated cost insights and trend analysis

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| item_code | String | Standardized item code | HYD-OIL-46-001 |
| canonical_item_name | String | Standard item name | Hydraulic Oil ISO VG 46 |
| region | String | Geographical region | North |
| supplier | String | Supplier name | SyntheticTech Industries |
| avg_price | Float | Average price across orders | 425.75 |
| median_price | Float | Median price | 427.00 |
| price_std | Float | Standard deviation | 4.25 |
| min_price | Float | Minimum price observed | 420.00 |
| max_price | Float | Maximum price observed | 432.00 |
| trend_direction | String | Price trend direction | up, down, stable |

**Trend Categories**:
- **up**: Price increasing over time (cost pressure)
- **down**: Price decreasing over time (savings opportunity)
- **stable**: Price stable (consistent supplier)

**Use Cases**:
- Identify cost trends by supplier/region
- Detect price variations
- Benchmark supplier performance

---

## 4. anomalies.csv
**Purpose**: Flagged abnormal pricing events

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| po_id | String | Purchase Order ID | PO-2024-026 |
| item_code | String | Standardized item code | STEEL-PIPE-4-002 |
| unit_price | Float | Actual price paid | 2800.00 |
| expected_price | Float | Expected price (baseline) | 1825.00 |
| anomaly_flag | String | Anomaly present? | yes, no |
| anomaly_reason | String | Human-readable reason | Price 53.4% above average |

**Anomaly Detection Rules**:
- Price deviation > 15% from regional average
- Unusual supplier pricing
- Quantity-based discount misses
- Outlier detection

**Severity Levels** (in reason):
- **CRITICAL**: >40% deviation
- **HIGH**: 20-40% deviation
- **MEDIUM**: 15-20% deviation

---

## Data Flow

```
purchase_orders_raw.csv
    ↓
[Standardization Pipeline]
    ↓
standardized_items.csv
    ↓
[Analytics & Aggregation]
    ↓
cost_analytics.csv
anomalies.csv
    ↓
[Visualization in Streamlit Dashboard]
```

---

## Data Quality Notes

1. **Completeness**: All fields required, no nulls
2. **Consistency**: Item codes follow pattern: [CATEGORY]-[DESCRIPTOR]-[SEQUENCE]
3. **Accuracy**: Dates in ISO 8601 format (YYYY-MM-DD)
4. **Uniqueness**: po_id is unique in raw data; may repeat in processed views
5. **Validation**: All prices > 0, quantities > 0

---

## Future Extensions

- Version control on cost_analytics (time-series)
- Supplier rating scores
- Historical anomaly tracking
- Invoice-level granularity

