from flask import Flask

from database import db
from config import DATABASE

from routes.prediction import prediction_bp
from routes.history import history_bp
from routes.movies import movies_bp
from routes.chatbot import chatbot_bp
from routes.dashboard import dashboard_bp

# Flask App
app = Flask(__name__)

app.register_blueprint(prediction_bp)
app.register_blueprint(history_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(dashboard_bp)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{DATABASE}"

db.init_app(app)

with app.app_context():
    db.create_all()

# Run App

if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False
    )