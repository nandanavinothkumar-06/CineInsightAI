"""
Prediction Reliability Service
"""

def prediction_reliability(

    predictions,

    consensus,

    confidence_dashboard

):

    agreement = consensus["percentage"]

    average = confidence_dashboard["average"]

    spread = confidence_dashboard["spread"]

    score = 0

    # Agreement

    if agreement == 100:

        score += 50

    elif agreement >= 75:

        score += 35

    elif agreement >= 50:

        score += 20

    # Confidence

    if average >= 95:

        score += 40

    elif average >= 85:

        score += 30

    elif average >= 70:

        score += 20

    else:

        score += 10

    # Confidence Spread

    if spread <= 10:

        score += 10

    elif spread <= 20:

        score += 7

    elif spread <= 40:

        score += 5

    else:

        score += 2

    # Rating

    if score >= 95:

        reliability = "Excellent"

        stars = 5

        risk = "Very Low"

    elif score >= 80:

        reliability = "Very High"

        stars = 4

        risk = "Low"

    elif score >= 60:

        reliability = "High"

        stars = 3

        risk = "Moderate"

    elif score >= 40:

        reliability = "Medium"

        stars = 2

        risk = "High"

    else:

        reliability = "Low"

        stars = 1

        risk = "Very High"

    return {

        "score": score,

        "stars": stars,

        "reliability": reliability,

        "risk": risk,

        "agreement": agreement,

        "spread": spread,

        "average": average

    }