"""Provides helper functions for interacting with the OMDb API."""

import requests

from config import (
    OMDB_API_KEY,
    OMDB_BASE
)


# Send a request to the OMDb API
def omdb_request(params):

    params["apikey"] = OMDB_API_KEY

    try:

        response = requests.get(
            OMDB_BASE,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as error:

        print(
            "OMDb Error:",
            error
        )

        return {}


# Search movies by title
def search_movies(movie_name):

    return omdb_request(
        {
            "s": movie_name
        }
    )


# Fetch detailed movie information using IMDb ID
def movie_details(imdb_id):

    return omdb_request(
        {
            "i": imdb_id,
            "plot": "full"
        }
    )