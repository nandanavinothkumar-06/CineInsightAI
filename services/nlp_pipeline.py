import re
import string
import nltk

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()


def lowercase_text(text):
    return text.lower()


def remove_punctuation(text):
    return text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )


def tokenize(text):
    return word_tokenize(text)


def remove_stopwords(tokens):

    return [

        word

        for word in tokens

        if word not in stop_words

    ]


def lemmatize(tokens):

    return [

        lemmatizer.lemmatize(word)

        for word in tokens

    ]


def pipeline_steps(text):

    lower = lowercase_text(text)

    no_punctuation = remove_punctuation(lower)

    tokens = tokenize(no_punctuation)

    filtered = remove_stopwords(tokens)

    lemmas = lemmatize(filtered)

    return {

        "original": text,

        "lowercase": lower,

        "no_punctuation": no_punctuation,

        "tokens": tokens,

        "filtered": filtered,

        "lemmatized": lemmas,

        "processed_text": " ".join(lemmas)

    }