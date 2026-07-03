"""Provides NLP text statistics."""

import re


def text_statistics(text):

    words = re.findall(r"\b\w+\b", text)

    sentences = re.split(r"[.!?]+", text)

    sentences = [
        s for s in sentences
        if s.strip()
    ]

    characters = len(text)

    word_count = len(words)

    sentence_count = len(sentences)

    unique_words = len(
        set(
            word.lower()
            for word in words
        )
    )

    avg_word_length = round(

        sum(
            len(word)
            for word in words
        ) / word_count,

        2

    ) if word_count else 0

    reading_time = round(

        word_count / 200 * 60

    )

    return {

        "characters": characters,

        "words": word_count,

        "sentences": sentence_count,

        "unique_words": unique_words,

        "avg_word_length": avg_word_length,

        "reading_time": f"{reading_time} sec"

    }