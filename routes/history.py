import os
import pandas as pd

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    send_file
)

from database import (
    db,
    Prediction
)

from services.analytics_service import (
    get_history_data,
    export_history_dataframe
)

from config import REPORT_DIR

history_bp = Blueprint(
    "history",
    __name__
)

@history_bp.route("/history")
def history():

    search = request.args.get(
        "search",
        ""
    )

    sentiment = request.args.get(
        "sentiment",
        ""
    )

    movie = request.args.get(
        "movie",
        ""
    )

    data = get_history_data(
        search,
        sentiment,
        movie
    )

    return render_template(
        "history.html",

        rows=data["rows"],
        total=data["total"],
        avg_confidence=data["avg_confidence"],
        latest_date=data["latest_date"],
        most_common=data["most_common"],

        search=search,
        sentiment=sentiment,
        movie=movie,

        movies=data["movies"]
    )

@history_bp.route("/delete_prediction/<int:id>")
def delete_prediction(id):

    row = Prediction.query.get_or_404(
        id
    )

    db.session.delete(row)

    db.session.commit()

    return redirect(
    url_for("history.history")
)

@history_bp.route("/export_history")
def export_history():

    df = export_history_dataframe()

    os.makedirs(
        "reports",
        exist_ok=True
    )

    path = os.path.join(
        REPORT_DIR,
        "history.csv"
    )

    df.to_csv(
        path,
        index=False
    )

    return send_file(
        path,
        as_attachment=True
    )
