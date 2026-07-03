"""Provides emotion prediction using a pretrained transformer model."""

from transformers import pipeline


# Load the emotion classification model
emotion_model = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    top_k=None
)


# Predict the dominant emotion from text
def emotion_predict(text):

    result = emotion_model(
        str(text[:512])
    )

    emotions = result[0]

    best = max(
        emotions,
        key=lambda emotion: emotion["score"]
    )

    return best["label"]