# Free Text Analysis Module

This module handles unstructured procurement text such as
emails, notes, PDFs, or copied content with no fixed format.

It extracts key facts and insights using lightweight NLP.

This module is independent of the structured CSV pipeline.

---

## What this module does

Input  
Free text with no headers, no order, no structure

Output  
Bullet point insights with:
• Items detected
• Materials
• Sizes
• Oil grades
• Price ranges
• Usage context

The output is factual, keyword driven, and non-robotic.

---

## Folder structure

ai_free_text/  
text_preprocessing.py  
insight_generation.py  
run_free_text_analysis.py  

---

## How it works

Step 1  
Normalize raw text

Step 2  
Extract factual signals using patterns and keywords

Step 3  
Format insights into short bullet points

No data is written to CSV.
This module only returns insights for display.

---

## Example output

• Items detected: Pipe, Valve, Oil  
• Materials: Carbon Steel, Stainless Steel  
• Sizes: 100 mm, 2 inch  
• Oil grade: ISO 68  
• Price range mentioned: 1200 to 5000  
• Usage context: Maintenance, Operations  

---

## How to run

From project root

python ai_free_text/run_free_text_analysis.py

---

## What this module does not do

• No clustering
• No standardization
• No analytics
• No database writes

This separation is intentional.

---

## Usage

Designed for:
• UI text box input
• Demo scenarios
• Unstructured procurement data

---

## Status

Feature complete and demo ready.
