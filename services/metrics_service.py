import json
import os

from config import MODEL_DIR

METRICS_FILE = os.path.join(
    MODEL_DIR,
    "metrics.json"
)


def load_metrics():
    with open(METRICS_FILE, "r") as f:
        return json.load(f)


def get_best_model(metrics):
    return max(
        metrics,
        key=lambda model: metrics[model]["accuracy"]
    )