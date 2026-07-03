"""
Keyword Extraction Service
"""

from collections import Counter

from preprocessing import preprocess


def extract_keywords(text, top_n=10):

    processed = preprocess(text)

    words = processed.split()

    frequency = Counter(words)

    keywords = frequency.most_common(top_n)

    return keywords