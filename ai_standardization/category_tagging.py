def assign_category(text):
    text = text.lower()

    if "pipe" in text:
        return "Pipe"
    if "valve" in text:
        return "Valve"
    if "flange" in text:
        return "Flange"
    if "gasket" in text:
        return "Gasket"
    if "bolt" in text or "nut" in text:
        return "Fasteners"
    if "pump" in text:
        return "Pump"
    if "bearing" in text:
        return "Bearing"
    if "cable" in text or "wire" in text:
        return "Electrical Cable"
    if "oil" in text or "lubricant" in text:
        return "Lubricant"
    if "helmet" in text or "safety" in text:
        return "Safety Equipment"
    if "gauge" in text or "thermocouple" in text or "sensor" in text:
        return "Instrumentation"

    return "Other"
