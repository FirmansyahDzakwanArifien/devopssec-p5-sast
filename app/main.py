"""
SecureVault — Aplikasi manajemen catatan sederhana berbasis Flask.
Entry point utama aplikasi.
"""

from flask import Flask
from app.routes import auth_bp, notes_bp
from app.config import DevelopmentConfig


def create_app(config=None):
    """Application factory pattern."""
    app = Flask(__name__)

    if config is None:
        app.config.from_object(DevelopmentConfig)
    else:
        app.config.from_object(config)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notes_bp, url_prefix="/notes")

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="0.0.0.0", port=5000, debug=True)
