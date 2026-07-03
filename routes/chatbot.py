from flask import (
    Blueprint,
    render_template,
    request
)

from database import Prediction

from api.omdb import (
    search_movies,
    movie_details
)

chatbot_bp = Blueprint(
    "chatbot",
    __name__
)

@chatbot_bp.route("/chatbot")
def chatbot():
    return render_template(
        "chatbot.html"
    )

@chatbot_bp.route(
    "/ask",
    methods=["POST"]
)
def ask():

    movie = request.form["movie"]

    response = search_movies(movie)

    if response.get("Response") == "False":

        return render_template(
            "chatbot.html",
            error=response.get("Error")
        )

    movies = response.get(
        "Search",
        []
    )

    movies = sorted(
        movies,
        key=lambda x: x.get(
            "Year",
            "0"
        ),
        reverse=True
    )

    return render_template(
        "chatbot.html",
        movies=movies
    )

@chatbot_bp.route(
    "/movie/<imdb_id>"
)
def movie_details(imdb_id):

    movie = movie_details(imdb_id)

    title = movie.get(
        "Title",
        ""
    )

    reviews = Prediction.query.filter(
        Prediction.movie_name.ilike(
            f"%{title}%"
        )
    ).all()

    positive = len(
        [
            r
            for r in reviews
            if r.prediction == "positive"
        ]
    )

    negative = len(
        [
            r
            for r in reviews
            if r.prediction == "negative"
        ]
    )

    total_reviews = positive + negative

    community_rating = round(
        (
            positive /
            total_reviews
        ) * 5,
        1
    ) if total_reviews > 0 else 0

    return render_template(
        "chatbot.html",
        movie=movie,
        positive=positive,
        negative=negative,
        community_rating=community_rating
    )