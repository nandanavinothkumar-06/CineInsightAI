"""
Explainable AI Service
"""

import numpy as np


def explain_classical_model(model, vectorizer, review, top_n=10):

    processed = review

    vector = vectorizer.transform([processed])

    feature_names = np.array(
        vectorizer.get_feature_names_out()
    )

    nonzero = vector.nonzero()[1]

    features = []

    try:

        coef = model.coef_[0]

    except Exception:

        return {

            "positive": [],

            "negative": []

        }

    for idx in nonzero:

        features.append(

            (

                feature_names[idx],

                coef[idx]

            )

        )

    positive = sorted(

        [

            x for x in features

            if x[1] > 0

        ],

        key=lambda x: x[1],

        reverse=True

    )[:top_n]

    negative = sorted(

        [

            x for x in features

            if x[1] < 0

        ],

        key=lambda x: x[1]

    )[:top_n]

    return {

        "positive": positive,

        "negative": negative

    }