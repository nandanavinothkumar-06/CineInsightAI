"""
Word Frequency Analysis
"""

from collections import Counter

from preprocessing import preprocess


def word_frequency(text, top_n=10):

    processed = preprocess(text)

    words = processed.split()

    counter = Counter(words)

    return counter.most_common(top_n)