# AI Standardization Module

This module is owned by AI ML Engineer 1.

Its purpose is to convert messy purchase order item descriptions into
standardized canonical items with stable item codes and confidence scores.

This module is completely independent from UI and analytics logic.

---

## What this module does

Input  
Raw purchase order lines with free text item descriptions

Output  
Standardized items with  
canonical item name  
stable item code  
confidence score  

Same items written differently will always map to the same item code.

---

## Folder structure

ai_standardization  
text_cleaning.py  
attribute_extraction.py  
embeddings.py  
clustering.py  
item_code_generator.py  
run_standardization.py  

Input data location  
data raw purchase_orders_raw.csv  

Output data location  
data processed standardized_items.csv  

---

## Input schema

purchase_orders_raw.csv must contain at least

po_id  
item_description  

Other columns are ignored by this module.

---

## Output schema

standardized_items.csv contains

po_id  
item_description  
canonical_item_name  
item_code  
confidence_score  

Confidence score ranges from 0.75 to 0.95.

---

## How the pipeline works

Step 1  
Clean and normalize item descriptions  
Expand abbreviations and normalize text  

Step 2  
Extract attributes like diameter length and material  

Step 3  
Generate sentence embeddings using a transformer model  

Step 4  
Cluster similar items using cosine similarity  

Step 5  
Assign canonical item name and generate stable item codes  

Step 6  
Compute confidence score based on cluster size  

---

## How to run

From project root directory

python ai_standardization/run_standardization.py

---

## Success criteria

Script runs without error  
standardized_items.csv is created  
Same item written differently maps to same item code  
Confidence score is populated  

---

## What this module does not do

No UI logic  
No price analytics  
No anomaly detection  
No APIs  

This separation is intentional to enable parallel work.

---

## Owner

AI ML Engineer 1

This module is complete once standardized_items.csv is generated successfully.
