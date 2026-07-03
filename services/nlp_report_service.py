"""
Creates a final NLP summary.
"""

def create_nlp_report(

    prediction,

    confidence,

    emotion,

    statistics,

    keywords,

    consensus

):

    if confidence >= 95:

        confidence_level = "Very High"

    elif confidence >= 80:

        confidence_level = "High"

    else:

        confidence_level = "Moderate"

    if statistics["words"] < 15:

        review_type = "Short"

    elif statistics["words"] < 40:

        review_type = "Medium"

    else:

        review_type = "Detailed"

    return {

        "prediction": prediction,

        "confidence": confidence,

        "confidence_level": confidence_level,

        "emotion": emotion,

        "review_type": review_type,

        "keywords": len(keywords),

        "agreement": consensus["percentage"],

        "language_quality":

            "Excellent"

            if statistics["unique_words"] > 10

            else "Basic"

    }