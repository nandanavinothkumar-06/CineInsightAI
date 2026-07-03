"""Stores application configuration constants."""

import os

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)

IMAGE_DIR = os.path.join(
    BASE_DIR,
    "static",
    "images"
)

DATABASE = os.path.join(
    BASE_DIR,
    "instance",
    "sentiment.db"
)

# TMDB API configuration
TMDB_API_KEY = "cef376856f785389188252671b9d2ad4"
TMDB_BASE = "https://api.themoviedb.org/3"

# OMDb API configuration
OMDB_API_KEY = "d1565103"
OMDB_BASE = "https://www.omdbapi.com/"

# SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE}"