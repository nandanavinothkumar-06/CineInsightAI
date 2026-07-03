import pandas as pd
import base64
from io import BytesIO

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import plotly.express as px

from wordcloud import WordCloud
from database import db, Prediction


def get_history_data(search="", sentiment="", movie=""):

    query = Prediction.query

    if search:
        query = query.filter(
            Prediction.review.ilike(f"%{search}%")
        )

    if sentiment:
        query = query.filter(
            Prediction.prediction == sentiment
        )

    if movie:
        query = query.filter(
            Prediction.movie_name.ilike(f"%{movie}%")
        )

    rows = query.order_by(
        Prediction.created_at.desc()
    ).all()

    total = len(rows)

    positive = len(
        [r for r in rows if r.prediction == "positive"]
    )

    negative = len(
        [r for r in rows if r.prediction == "negative"]
    )

    avg_confidence = round(
        sum(r.confidence for r in rows) / total,
        2
    ) if total else 0

    latest_date = (
        rows[0].created_at.strftime("%d-%m-%Y")
        if rows
        else "-"
    )

    most_common = (
        "Positive"
        if positive >= negative
        else "Negative"
    ) if rows else "-"

    movies = (
        db.session.query(
            Prediction.movie_name
        )
        .distinct()
        .all()
    )

    movies = [
        m[0]
        for m in movies
        if m[0]
    ]

    return {
        "rows": rows,
        "total": total,
        "positive": positive,
        "negative": negative,
        "avg_confidence": avg_confidence,
        "latest_date": latest_date,
        "most_common": most_common,
        "movies": movies
    }


def export_history_dataframe():

    rows = Prediction.query.all()

    data = []

    for r in rows:

        data.append({

            "Movie": r.movie_name,
            "Review": r.review,
            "Prediction": r.prediction,
            "Confidence": r.confidence,
            "Date": r.created_at

        })

    return pd.DataFrame(data)

def create_wordcloud(text):

    if not text.strip():
        return None

    wc = WordCloud(
        width=800,
        height=400,
        background_color="white"
    ).generate(text)

    img = BytesIO()

    plt.figure(figsize=(8, 4))
    plt.imshow(wc)
    plt.axis("off")

    plt.savefig(
        img,
        format="png",
        bbox_inches="tight"
    )

    plt.close("all")

    img.seek(0)

    return base64.b64encode(
        img.getvalue()
    ).decode()

def get_dashboard_summary(mode, csv_df):

    has_csv = csv_df is not None

    total = 0
    positive = 0
    negative = 0

    avg_confidence = 0

    positive_percentage = 0
    negative_percentage = 0

    most_common = "-"
    most_common_emotion = "-"

    dashboard_message = ""

    recent = []

    # CSV MODE

    if mode == "csv" and has_csv:

        dashboard_type = "csv"

        df = csv_df.copy()

        total = len(df)

        if "prediction" in df.columns:

            positive = (
                df["prediction"] == "positive"
            ).sum()

            negative = (
                df["prediction"] == "negative"
            ).sum()

        if (
            "confidence" in df.columns
            and not df.empty
        ):

            avg_confidence = round(
                df["confidence"].mean(),
                2
            )

        positive_percentage = round(
            (positive / total) * 100,
            2
        ) if total else 0

        negative_percentage = round(
            (negative / total) * 100,
            2
        ) if total else 0

        most_common = (
            "Positive"
            if positive >= negative
            else "Negative"
        )

        if (
            "emotion" in df.columns
            and not df.empty
        ):

            most_common_emotion = (
                df["emotion"].mode()[0]
            )

        recent = (
            df.to_dict("records")[-10:]
        )

    # DATABASE MODE

    else:

        dashboard_type = "database"

        rows = Prediction.query.all()

        total = len(rows)

        positive = len(
            [
                r
                for r in rows
                if r.prediction == "positive"
            ]
        )

        negative = len(
            [
                r
                for r in rows
                if r.prediction == "negative"
            ]
        )

        avg_confidence = round(

            sum(
                r.confidence
                for r in rows
            ) / total,

            2

        ) if total else 0

        positive_percentage = round(
            (positive / total) * 100,
            2
        ) if total else 0

        negative_percentage = round(
            (negative / total) * 100,
            2
        ) if total else 0

        most_common = (
            "Positive"
            if positive >= negative
            else "Negative"
        )

        recent = (
            Prediction.query
            .order_by(
                Prediction.created_at.desc()
            )
            .limit(10)
            .all()
        )

        df = pd.DataFrame(

            [
                {
                    "movie_name": r.movie_name,
                    "review": r.review,
                    "prediction": r.prediction,
                    "confidence": r.confidence,
                    "date": r.created_at.strftime("%Y-%m-%d")
                }
                for r in rows
            ]
        )

    if total == 0:
        dashboard_message = (
            "No reviews available yet."
        )


    return {

        "dashboard_type": dashboard_type,
        "has_csv": has_csv,
        "df": df,
        "recent": recent,
        "total": total,
        "positive": positive,
        "negative": negative,
        "avg_confidence": avg_confidence,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "most_common": most_common,
        "most_common_emotion": most_common_emotion,
        "dashboard_message": dashboard_message

    }

def build_dashboard_charts(context):

    df = context["df"]
    dashboard_type = context["dashboard_type"]
    positive = context["positive"]
    negative = context["negative"]

# Generate all dashboard charts and word clouds

    # Default values

    pie_graph = ""
    hist_graph = ""
    line_graph = ""
    trend_graph = ""
    monthly_graph = ""
    movie_graph = ""
    box_graph = ""

    keyword_graph = ""
    emotion_graph = ""
    aspect_graph = ""
    gauge_graph = ""

    positive_wordcloud = None
    negative_wordcloud = None

    # PIE CHART

    pie = px.pie(
        names=[
            "Positive",
            "Negative"
        ],
        values=[
            positive,
            negative
        ],
        title="Sentiment Distribution"
    )

    pie_graph = pie.to_html(
        full_html=False
    )

    # HISTOGRAM

    if (
        not df.empty
        and "confidence" in df.columns
    ):

        hist = px.histogram(
            df,
            x="confidence",
            nbins=20,
            title="Confidence Distribution"
        )

        hist_graph = hist.to_html(
            full_html=False
        )

    # DATABASE ONLY

    if (
        dashboard_type == "database"
        and not df.empty
    ):
        # Timeline

        timeline = (
            df.groupby("date")
            .size()
            .reset_index(name="count")
        )

        line = px.line(
            timeline,
            x="date",
            y="count",
            markers=True,
            title="Reviews Over Time"
        )

        line_graph = line.to_html(
            full_html=False
        )

        # Sentiment Trend

        sentiment_trend = (
            df.groupby(
                [
                    "date",
                    "prediction"
                ]
            )
            .size()
            .reset_index(name="count")
        )

        trend = px.line(
            sentiment_trend,
            x="date",
            y="count",
            color="prediction",
            markers=True,
            title="Sentiment Trend"
        )

        trend_graph = trend.to_html(
            full_html=False
        )

        # Monthly
        df["month"] = pd.to_datetime(
            df["date"]
        ).dt.strftime("%Y-%m")

        monthly = (
            df.groupby("month")
            .size()
            .reset_index(name="count")
        )

        monthly_fig = px.bar(
            monthly,
            x="month",
            y="count",
            title="Monthly Prediction Count"
        )

        monthly_graph = monthly_fig.to_html(
            full_html=False
        )

        # Top Movies

        if "movie_name" in df.columns:

            movies = (
                df["movie_name"]
                .fillna("")
            )

            movies = movies[
                movies != ""
            ]

            if not movies.empty:

                top_movies = (
                    movies.value_counts()
                    .head(10)
                )

                movie_fig = px.bar(
                    x=top_movies.index,
                    y=top_movies.values,
                    title="Top Reviewed Movies"
                )

                movie_graph = movie_fig.to_html(
                    full_html=False
                )
    # BOX PLOT

    if (
        not df.empty
        and "prediction" in df.columns
    ):

        box = px.box(
            df,
            x="prediction",
            y="confidence",
            title="Confidence by Sentiment"
        )

        box_graph = box.to_html(
            full_html=False
        )

    # WORD CLOUDS

    if (
        not df.empty
        and "review" in df.columns
    ):

        positive_text = " ".join(
            df[
                df["prediction"] == "positive"
            ]["review"]
            .astype(str)
        )

        negative_text = " ".join(
            df[
                df["prediction"] == "negative"
            ]["review"]
            .astype(str)
        )

        positive_wordcloud = create_wordcloud(
            positive_text
        )

        negative_wordcloud = create_wordcloud(
            negative_text
        )

    # Return Everything

    return {

        "pie_graph": pie_graph,
        "hist_graph": hist_graph,
        "line_graph": line_graph,
        "trend_graph": trend_graph,
        "monthly_graph": monthly_graph,
        "movie_graph": movie_graph,
        "box_graph": box_graph,
        "keyword_graph": keyword_graph,
        "emotion_graph": emotion_graph,
        "aspect_graph": aspect_graph,
        "gauge_graph": gauge_graph,
        "positive_wordcloud": positive_wordcloud,
        "negative_wordcloud": negative_wordcloud

    }