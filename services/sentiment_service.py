"""Provides sentiment prediction services for text, CSV, and PDF reviews."""

import os
import pickle
import numpy as np

from PyPDF2 import PdfReader
from transformers import pipeline

from database import db, Prediction
from preprocessing import preprocess

from config import MODEL_DIR

from services.nlp_pipeline import pipeline_steps
from services.statistics_service import text_statistics
from services.keyword_service import extract_keywords
from services.frequency_service import word_frequency
from services.explain_service import explain_prediction
from services.nlp_report_service import create_nlp_report
from services.xai_service import explain_classical_model
from services.confidence_service import confidence_dashboard
from services.reliability_service import prediction_reliability
from services.business_service import business_dashboard
from services.insight_service import ai_insights
from services.emotion_service import emotion_predict
from services.report_service import generate_report


# ==========================================================
# Load Classical Machine Learning Models
# ==========================================================

with open(
    os.path.join(MODEL_DIR, "lr.pkl"),
    "rb"
) as file:
    lr_model = pickle.load(file)

with open(
    os.path.join(MODEL_DIR, "nb.pkl"),
    "rb"
) as file:
    nb_model = pickle.load(file)

with open(
    os.path.join(MODEL_DIR, "svc.pkl"),
    "rb"
) as file:
    svc_model = pickle.load(file)

with open(
    os.path.join(MODEL_DIR, "tfidf.pkl"),
    "rb"
) as file:
    tfidf = pickle.load(file)


# ==========================================================
# Load Deep Learning Model (BERT)
# ==========================================================

bert = pipeline(
    "text-classification",
    model="textattack/bert-base-uncased-imdb"
)


# ==========================================================
# Helper
# ==========================================================

def vectorize(text):
    """
    Preprocess and convert text into TF-IDF vector.
    """

    processed = preprocess(text)

    return tfidf.transform(
        [processed]
    )


# ==========================================================
# BERT Prediction
# ==========================================================

def bert_predict(text):

    result = bert(
        str(text),
        truncation=True,
        max_length=512
    )[0]

    label_map = {

        "LABEL_0": "negative",

        "LABEL_1": "positive"

    }

    prediction = label_map[
        result["label"]
    ]

    confidence = round(
        result["score"] * 100,
        2
    )

    return prediction, confidence


# ==========================================================
# Logistic Regression
# ==========================================================

def lr_predict(text):

    vector = vectorize(text)

    prediction = lr_model.predict(
        vector
    )[0]

    confidence = round(

        max(

            lr_model.predict_proba(
                vector
            )[0]

        ) * 100,

        2

    )

    return prediction, confidence


# ==========================================================
# Naive Bayes
# ==========================================================

def nb_predict(text):

    vector = vectorize(text)

    prediction = nb_model.predict(
        vector
    )[0]

    confidence = round(

        max(

            nb_model.predict_proba(
                vector
            )[0]

        ) * 100,

        2

    )

    return prediction, confidence


# ==========================================================
# Linear SVC
# ==========================================================

def svc_predict(text):

    vector = vectorize(text)

    prediction = svc_model.predict(vector)[0]

    score = svc_model.decision_function(vector)[0]

    confidence = round(
        100 / (1 + np.exp(-abs(score))),
        2
    )

    return prediction, confidence


# ==========================================================
# Predict using every model
# ==========================================================

def all_model_predictions(text):

    bert_pred, bert_conf = bert_predict(text)

    lr_pred, lr_conf = lr_predict(text)

    nb_pred, nb_conf = nb_predict(text)

    svc_pred, svc_conf = svc_predict(text)

    predictions = {

        "BERT": {

            "prediction": bert_pred,

            "confidence": bert_conf

        },

        "Logistic Regression": {

            "prediction": lr_pred,

            "confidence": lr_conf

        },

        "Naive Bayes": {

            "prediction": nb_pred,

            "confidence": nb_conf

        },

        "Linear SVC": {

            "prediction": svc_pred,

            "confidence": svc_conf

        }

    }

    return predictions

# ==========================================================
# Aspect Keywords
# ==========================================================

ASPECT_KEYWORDS = {

    "Acting": [
        "acting",
        "actor",
        "actors",
        "performance",
        "performances",
        "cast"
    ],

    "Story": [
        "story",
        "plot",
        "screenplay",
        "script"
    ],

    "Music": [
        "music",
        "soundtrack",
        "songs",
        "background score",
        "bgm"
    ],

    "Ending": [
        "ending",
        "climax",
        "finale"
    ],

    "Visuals": [
        "visual",
        "visuals",
        "cinematography",
        "cgi",
        "effects",
        "vfx"
    ]
}


# ==========================================================
# Aspect Based Sentiment Analysis
# ==========================================================

def aspect_analysis(review):

    result = {}

    sentences = review.split(".")

    for aspect, keywords in ASPECT_KEYWORDS.items():

        result[aspect] = {

            "sentiment": "Not Mentioned",

            "confidence": "-"

        }

        for sentence in sentences:

            sentence_lower = sentence.lower()

            if any(

                keyword in sentence_lower

                for keyword in keywords

            ):

                prediction, confidence = bert_predict(
                    sentence
                )

                result[aspect] = {

                    "sentiment": prediction,

                    "confidence": confidence,

                    "sentence": sentence.strip()

                }

                break

    return result


# ==========================================================
# Model Consensus Engine
# ==========================================================

def model_consensus(predictions):

    prediction_list = [

        model["prediction"]

        for model in predictions.values()

    ]

    positive = prediction_list.count("positive")

    negative = prediction_list.count("negative")

    total = len(prediction_list)

    if positive >= negative:

        final_prediction = "positive"

        agreement = positive

    else:

        final_prediction = "negative"

        agreement = negative

    agreement_percentage = round(

        agreement / total * 100,

        2

    )

    return {

        "prediction": final_prediction,

        "agreement": agreement,

        "total": total,

        "percentage": agreement_percentage

    }


# ==========================================================
# Highest Confidence Model
# ==========================================================

def highest_confidence_model(predictions):

    best_model = max(

        predictions,

        key=lambda model: predictions[model]["confidence"]

    )

    return {

        "model": best_model,

        "prediction": predictions[best_model]["prediction"],

        "confidence": predictions[best_model]["confidence"]

    }


# ==========================================================
# Classical ML Summary
# ==========================================================

def classical_summary(predictions):

    return {

        "Logistic Regression": predictions["Logistic Regression"],

        "Naive Bayes": predictions["Naive Bayes"],

        "Linear SVC": predictions["Linear SVC"]

    }


# ==========================================================
# Deep Learning Summary
# ==========================================================

def bert_summary(predictions):

    return predictions["BERT"]

# ==========================================================
# Predict Single Review
# ==========================================================

def predict_text(review, movie_name=""):

    nlp_pipeline = pipeline_steps(review)
    statistics = text_statistics(review)
    keywords = extract_keywords(review)
    frequency = word_frequency(review)
    explanation = explain_prediction(review)

    # -----------------------------
    # Multi-model predictions
    # -----------------------------

    predictions = all_model_predictions(review)

    consensus = model_consensus(predictions)

    best_model = highest_confidence_model(predictions)

    confidence_data = confidence_dashboard(predictions)

    reliability = prediction_reliability(

        predictions,

        consensus,

        confidence_data

    )

    processed = preprocess(review)

    lr_xai = explain_classical_model(

        lr_model,

        tfidf,

        processed

    )

    history = Prediction.query.all()

    business = business_dashboard(history)

    insights = ai_insights(

        business,

        reliability,

        confidence_data

    )

    # -----------------------------
    # Emotion Detection
    # -----------------------------

    emotion = emotion_predict(review)

    # -----------------------------
    # Aspect Analysis
    # -----------------------------

    aspect_result = aspect_analysis(
        review
    )

    # -----------------------------
    # Final Prediction (BERT)
    # -----------------------------

    final_prediction = predictions[
        "BERT"
    ]["prediction"]

    final_confidence = predictions[
        "BERT"
    ]["confidence"]

    # -----------------------------
    # Save Prediction
    # -----------------------------

    save_prediction(

        movie_name,

        review,

        final_prediction,

        final_confidence

    )

    # -----------------------------
    # Generate PDF Report
    # -----------------------------

    generate_report(

        review,

        final_prediction,

        final_confidence,

        emotion

    )

    nlp_report = create_nlp_report(

        final_prediction,

        final_confidence,

        emotion,

        statistics,

        keywords,

        consensus

    )

    # -----------------------------
    # Return Everything
    # -----------------------------

    return {

        "review": review,

        "prediction": final_prediction,

        "confidence": final_confidence,

        "emotion": emotion,

        "aspect_result": aspect_result,

        "predictions": predictions,

        "consensus": consensus,

        "best_model": best_model,

        "nlp_pipeline": nlp_pipeline,

        "text_statistics": statistics,

        "keywords": keywords,

        "word_frequency": frequency,

        "explanation": explanation,

        "nlp_report": nlp_report,

        "lr_xai": lr_xai,

        "confidence_dashboard": confidence_data,

        "reliability": reliability,

        "business_dashboard": business,

        "insights": insights,

        "classical_models":

            classical_summary(
                predictions
            ),

        "bert":

            bert_summary(
                predictions
            )

    }


# ==========================================================
# Predict PDF
# ==========================================================

def predict_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return predict_text(
        text[:1000]
    )

# ==========================================================
# Predict CSV Reviews
# ==========================================================

def predict_csv(df):

    sentiments = []
    confidences = []
    emotions = []

    acting = []
    story = []
    music = []
    ending = []
    visuals = []

    for text in df["review"]:

        review = str(text)

        predictions = all_model_predictions(review)

        bert_result = predictions["BERT"]

        emotion = emotion_predict(review)

        aspect = aspect_analysis(review)

        sentiments.append(
            bert_result["prediction"]
        )

        confidences.append(
            bert_result["confidence"]
        )

        emotions.append(
            emotion
        )

        acting.append(
            aspect["Acting"]["sentiment"]
        )

        story.append(
            aspect["Story"]["sentiment"]
        )

        music.append(
            aspect["Music"]["sentiment"]
        )

        ending.append(
            aspect["Ending"]["sentiment"]
        )

        visuals.append(
            aspect["Visuals"]["sentiment"]
        )

    df["prediction"] = sentiments
    df["confidence"] = confidences
    df["emotion"] = emotions

    df["acting_sentiment"] = acting
    df["story_sentiment"] = story
    df["music_sentiment"] = music
    df["ending_sentiment"] = ending
    df["visuals_sentiment"] = visuals

    return df


# ==========================================================
# Save Prediction
# ==========================================================

def save_prediction(

    movie_name,

    review,

    prediction,

    confidence

):

    row = Prediction(

        movie_name=movie_name,

        review=review,

        prediction=prediction,

        confidence=confidence

    )

    db.session.add(row)

    db.session.commit()

    return row