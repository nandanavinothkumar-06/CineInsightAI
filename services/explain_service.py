"""
Explainable NLP Service
"""

from preprocessing import preprocess

POSITIVE_WORDS = {

    "good","great","excellent","awesome","love","loved",
    "amazing","fantastic","wonderful","best","beautiful",
    "super","favorite","perfect","enjoy","liked","brilliant"

}

NEGATIVE_WORDS = {

    "bad","worst","boring","poor","hate","terrible",
    "awful","disappointing","slow","waste","weak",
    "predictable","confusing","ugly","dislike"

}


def explain_prediction(text):

    processed = preprocess(text)

    words = processed.split()

    positive = []

    negative = []

    neutral = []

    for word in words:

        if word in POSITIVE_WORDS:

            positive.append(word)

        elif word in NEGATIVE_WORDS:

            negative.append(word)

        else:

            neutral.append(word)

    return {

        "positive": list(set(positive)),

        "negative": list(set(negative)),

        "neutral": list(set(neutral))

    }