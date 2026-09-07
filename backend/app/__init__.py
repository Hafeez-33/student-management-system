from flask import Flask, jsonify

from app.config import Config
from app.extensions import cors, db


def create_app(config_class=Config):
    """Application factory for the Flask backend."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # Allow the future Vue/Vite dev server to call this API locally
    cors.init_app(app)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
