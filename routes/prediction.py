from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    current_app
)

import os
import pandas as pd

from config import REPORT_DIR

from services.sentiment_service import (
    predict_text,
    predict_pdf,
    predict_csv
)

prediction_bp = Blueprint(
    "prediction",
    __name__
)

@prediction_bp.route("/")
def home():

    return render_template(
        "index.html"
    )

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():

    result = predict_text(
        request.form["review"],
        request.form.get(
            "movie_name",
            ""
        )
    )

    return render_template(
        "index.html",
        **result
    )

@prediction_bp.route(
    "/csv",
    methods=["POST"]
)
def csv_prediction():

    file = request.files["csv"]

    df = pd.read_csv(file)

    df = predict_csv(df)

    output = os.path.join(
        REPORT_DIR,
        "output.csv"
    )

    df.to_csv(
        output,
        index=False
    )

    current_app.config["CSV_DF"] = df

    return send_file(
        output,
        as_attachment=True
    )

@prediction_bp.route(
    "/pdf",
    methods=["POST"]
)
def pdf_prediction():

    result = predict_pdf(
        request.files["pdf"]
    )

    return render_template(
        "index.html",
        **result
    )

@prediction_bp.route(
    "/download_report"
)
def download_report():

    path = os.path.join(
        REPORT_DIR,
        "report.pdf"
    )

    if not os.path.exists(path):

        return """
        <h2>
        Report not generated yet.
        </h2>
        """

    return send_file(
        path,
        as_attachment=True
    )