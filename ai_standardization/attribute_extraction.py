import re

def extract_attributes(text):
    attributes = {}

    dia = re.search(r"(\d+(\.\d+)?)\s*(mm|inch|in)", text)
    if dia:
        value = float(dia.group(1))
        unit = dia.group(3)

        if unit in ["inch", "in"]:
            value = value * 25.4
            unit = "mm"

        attributes["diameter_mm"] = round(value, 2)

    length = re.search(r"(\d+(\.\d+)?)\s*(m|meter|ft)", text)
    if length:
        value = float(length.group(1))
        unit = length.group(3)

        if unit == "ft":
            value = value * 0.3048
            unit = "m"

        attributes["length_m"] = round(value, 2)

    if "carbon steel" in text:
        attributes["material"] = "carbon steel"
    elif "stainless steel" in text:
        attributes["material"] = "stainless steel"

    return attributes
