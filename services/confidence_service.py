"""
Confidence Analytics Service
"""

def confidence_dashboard(predictions):

    confidences = {

        model: values["confidence"]

        for model, values in predictions.items()

    }

    winner = max(

        confidences,

        key=confidences.get

    )

    average = round(

        sum(confidences.values()) /

        len(confidences),

        2

    )

    highest = max(

        confidences.values()

    )

    lowest = min(

        confidences.values()

    )

    spread = round(

        highest - lowest,

        2

    )

    if average >= 95:

        reliability = "Excellent"

    elif average >= 85:

        reliability = "Very High"

    elif average >= 70:

        reliability = "High"

    elif average >= 50:

        reliability = "Moderate"

    else:

        reliability = "Low"

    return {

        "winner": winner,

        "average": average,

        "highest": highest,

        "lowest": lowest,

        "spread": spread,

        "reliability": reliability,

        "confidences": confidences

    }