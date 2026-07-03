"""Generates PDF reports for sentiment prediction results."""

import html
import os

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from config import REPORT_DIR


# Generate a PDF report for the prediction result
def generate_report(
    review,
    prediction,
    confidence,
    emotion
):

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        REPORT_DIR,
        "report.pdf"
    )

    doc = SimpleDocTemplate(
        file_path
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "CineInsight AI Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            f"Sentiment: {prediction}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Confidence: {confidence} %",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Emotion: {emotion}",
            styles["Normal"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    safe_review = html.escape(
        str(review[:3000])
    )

    elements.append(
        Paragraph(
            safe_review,
            styles["Normal"]
        )
    )

    doc.build(elements)

    print(
        "PDF created:",
        file_path
    )

    print(
        "Size:",
        os.path.getsize(file_path)
    )

    return file_path