import re

ITEM_KEYWORDS = [
    "pipe", "valve", "flange", "gasket", "pump",
    "bearing", "cable", "oil", "filter"
]

MATERIALS = [
    "carbon steel", "stainless steel", "mild steel", "copper"
]

def generate_insights(text):
    insights = []

    lowered = text.lower()

    # Items
    items_found = sorted({
        kw.capitalize() for kw in ITEM_KEYWORDS if kw in lowered
    })
    if items_found:
        insights.append(f"Items detected: {', '.join(items_found)}")

    # Materials
    materials_found = sorted({
        mat.title() for mat in MATERIALS if mat in lowered
    })
    if materials_found:
        insights.append(f"Materials: {', '.join(materials_found)}")

    # Sizes
    sizes = re.findall(r"\b\d+(\.\d+)?\s*(mm|inch|in)\b", lowered)
    sizes_clean = sorted({f"{s[0]} {s[1]}" for s in sizes})
    if sizes_clean:
        insights.append(f"Sizes: {', '.join(sizes_clean)}")

    # Oil grades
    oil_grade = re.findall(r"iso\s*\d+", lowered)
    if oil_grade:
        insights.append(f"Oil grade: {', '.join(sorted(set(oil_grade)))}")

    # Prices
    prices = sorted({
        int(p) for p in re.findall(r"\b\d{3,6}\b", lowered)
    })
    if len(prices) >= 2:
        insights.append(
            f"Price range mentioned: {min(prices)} to {max(prices)}"
        )
    elif prices:
        insights.append(f"Price mentioned: {prices[0]}")

    # Context
    context = []
    if "maintenance" in lowered:
        context.append("Maintenance")
    if "operation" in lowered or "operations" in lowered:
        context.append("Operations")

    if context:
        insights.append(f"Usage context: {', '.join(context)}")

    return insights
