from text_preprocessing import normalize_free_text
from insight_generation import generate_insights

def analyze_free_text(raw_text):
    clean_text = normalize_free_text(raw_text)
    bullets = generate_insights(clean_text)

    return bullets


if __name__ == "__main__":
    sample_input = """
    CS Pipe 100mm dia ordered for maintenance.
    Stainless steel valve 2 inch purchased from ValveWorld.
    Hydraulic oil ISO 68 required for operations.
    Prices discussed around 1200 to 5000 range.
    """

    insights = analyze_free_text(sample_input)

    for point in insights:
        print("-", point)
