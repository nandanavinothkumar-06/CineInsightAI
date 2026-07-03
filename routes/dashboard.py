from flask import (
    Blueprint,
    render_template,
    request
)

from services.analytics_service import (
    get_dashboard_summary,
    build_dashboard_charts
)

from services.metrics_service import (
    load_metrics,
    get_best_model
)

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)

@dashboard_bp.route("/dashboard")
def dashboard():

    mode = request.args.get(
        "mode",
        "database"
    )

    csv_df = None

    context = get_dashboard_summary(
        mode,
        csv_df
    )

    charts = build_dashboard_charts(context)

    metrics = load_metrics()

    winner = max(
        metrics,
        key=lambda x: metrics[x]["accuracy"]
    )

    #fastest_model = min(
        #metrics,
        #key=lambda x: metrics[x]["prediction_time"]
    #)

    #smallest_model = min(
        #metrics,
        #key=lambda x: metrics[x]["model_size_kb"]
    #)

    ranked_models = sorted(
        metrics.keys(),
        key=lambda x: metrics[x]["accuracy"],
        reverse=True
    )

    return render_template(
        "dashboard.html",
        **context,
        **charts,
        metrics=metrics,
        winner=winner,
        #fastest_model=fastest_model,
        #smallest_model=smallest_model,
        ranked_models=ranked_models

    )
