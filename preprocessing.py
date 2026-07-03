"""Provides text preprocessing utilities for sentiment analysis."""

import re
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Load stop words and lemmatizer
stop_words = set(
    stopwords.words("english")
)

lemmatizer = WordNetLemmatizer()


# Clean and preprocess review text
def preprocess(text):

    text = str(text).lower()

    text = re.sub(
        r"<.*?>",
        "",
        text
    )

    text = re.sub(
        r"http\S+|www\S+",
        "",
        text
    )

    text = re.sub(
        r"\d+",
        "",
        text
    )

    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )

    text = re.sub(
        r"[^a-zA-Z\s]",
        "",
        text
    )

    text = text.encode(
        "ascii",
        "ignore"
    ).decode("ascii")

    text = " ".join(
        text.split()
    )

    words = word_tokenize(text)

    words = [
        lemmatizer.lemmatize(
            word,
            pos="v"
        )
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)