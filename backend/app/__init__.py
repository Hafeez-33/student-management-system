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

    # Import models so SQLAlchemy metadata is registered, then create tables
    from app import models  # noqa: F401

    with app.app_context():
        db.create_all()

    from app.routes import register_routes

    register_routes(app)

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    return app
