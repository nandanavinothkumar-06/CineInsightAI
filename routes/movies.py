from flask import (
    Blueprint,
    render_template
)

from services.movie_service import (
    get_trending_movies,
    get_top_rated_movies,
    get_upcoming_movies,
    get_now_playing_movies,
    get_movie_recommendations,
    get_movie_trailer,
    get_movie_providers
)

movies_bp = Blueprint(
    "movies",
    __name__,
    url_prefix=""
)


@movies_bp.route("/trending")
def trending():

    movies = get_trending_movies()

    return render_template(
        "trending.html",
        title="Trending Movies",
        movies=movies
    )


@movies_bp.route("/top_rated")
def top_rated():

    movies = get_top_rated_movies()

    return render_template(
        "trending.html",
        title="Top Rated Movies",
        movies=movies
    )


@movies_bp.route("/upcoming")
def upcoming():

    movies = get_upcoming_movies()

    return render_template(
        "trending.html",
        title="Upcoming Movies",
        movies=movies
    )


@movies_bp.route("/now_playing")
def now_playing():

    movies = get_now_playing_movies()

    return render_template(
        "trending.html",
        title="Now Playing",
        movies=movies
    )


@movies_bp.route("/recommend/<int:id>")
def recommend(id):

    movies = get_movie_recommendations(id)

    return render_template(
        "recommend.html",
        movies=movies
    )


@movies_bp.route("/trailer/<int:id>")
def trailer(id):

    trailer_url = get_movie_trailer(id)

    return render_template(
        "trailer.html",
        trailer_url=trailer_url
    )


@movies_bp.route("/providers/<int:id>")
def providers(id):

    providers = get_movie_providers(id)

    return render_template(
        "providers.html",
        providers=providers
    )