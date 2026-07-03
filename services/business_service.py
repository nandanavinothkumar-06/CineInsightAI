"""
Business Intelligence Analytics
"""

from collections import Counter


def business_dashboard(predictions):

    total = len(predictions)

    sentiments = [

        p.prediction

        for p in predictions

    ]

    emotions = [

        getattr(p, "emotion", "Unknown")

        for p in predictions

    ]

    confidences = [

        p.confidence

        for p in predictions

    ]

    positive = sentiments.count("positive")

    negative = sentiments.count("negative")

    average_confidence = round(

        sum(confidences) /

        len(confidences),

        2

    ) if confidences else 0

    emotion_counter = Counter(emotions)

    most_common_emotion = (

        emotion_counter.most_common(1)[0][0]

        if emotions else "N/A"

    )

    return {

        "total_reviews": total,

        "positive_reviews": positive,

        "negative_reviews": negative,

        "positive_percentage":

            round(

                positive / total * 100,

                2

            ) if total else 0,

        "negative_percentage":

            round(

                negative / total * 100,

                2

            ) if total else 0,

        "average_confidence":

            average_confidence,

        "most_common_emotion":

            most_common_emotion

    }