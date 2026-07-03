"""Provides movie-related services using the TMDB API."""

from api.tmdb import (
    get_now_playing,
    get_recommendations,
    get_top_rated,
    get_trailer,
    get_trending,
    get_upcoming,
    get_watch_providers,
)


# Fetch trending movies
def get_trending_movies():
    return get_trending()


# Fetch top-rated movies
def get_top_rated_movies():
    return get_top_rated()


# Fetch upcoming movies
def get_upcoming_movies():
    return get_upcoming()


# Fetch currently playing movies
def get_now_playing_movies():
    return get_now_playing()


# Fetch movie recommendations
def get_movie_recommendations(movie_id):
    return get_recommendations(movie_id)


# Fetch movie trailer
def get_movie_trailer(movie_id):
    return get_trailer(movie_id)


# Fetch movie streaming providers
def get_movie_providers(movie_id):
    return get_watch_providers(movie_id)