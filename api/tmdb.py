"""Provides helper functions for interacting with the TMDB API."""

import requests

from config import (
    TMDB_API_KEY,
    TMDB_BASE
)


# Send a request to the TMDB API
def tmdb_request(endpoint, params=None):

    if params is None:
        params = {}

    params["api_key"] = TMDB_API_KEY

    url = f"{TMDB_BASE}/{endpoint}"

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as error:

        print(
            "TMDB Error:",
            error
        )

        return {}


# Fetch trending movies
def get_trending():

    return tmdb_request(
        "trending/movie/day"
    ).get(
        "results",
        []
    )


# Fetch top-rated movies
def get_top_rated():

    return tmdb_request(
        "movie/top_rated"
    ).get(
        "results",
        []
    )


# Fetch upcoming movies
def get_upcoming():

    return tmdb_request(
        "movie/upcoming"
    ).get(
        "results",
        []
    )


# Fetch currently playing movies
def get_now_playing():

    return tmdb_request(
        "movie/now_playing"
    ).get(
        "results",
        []
    )


# Convert IMDb ID to TMDB movie details
def imdb_to_tmdb(imdb_id):

    data = tmdb_request(
        f"find/{imdb_id}",
        {
            "external_source": "imdb_id"
        }
    )

    movies = data.get(
        "movie_results",
        []
    )

    if movies:
        return movies[0]

    return None


# Fetch recommended movies
def get_recommendations(movie_id):

    return tmdb_request(
        f"movie/{movie_id}/recommendations"
    ).get(
        "results",
        []
    )


# Fetch the official YouTube trailer
def get_trailer(movie_id):

    videos = tmdb_request(
        f"movie/{movie_id}/videos"
    ).get(
        "results",
        []
    )

    for video in videos:

        if (
            video["site"] == "YouTube"
            and
            video["type"] == "Trailer"
        ):

            return (
                f"https://www.youtube.com/watch?v={video['key']}"
            )

    return None


# Fetch movie streaming providers available in India
def get_watch_providers(movie_id):

    data = tmdb_request(
        f"movie/{movie_id}/watch/providers"
    )

    try:

        return data["results"]["IN"]["flatrate"]

    except KeyError:

        return []