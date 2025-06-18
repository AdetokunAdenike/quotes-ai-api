import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from openai import OpenAI

db = SQLAlchemy()
migrate = Migrate()

def get_openrouter_client():
    """Returns a new OpenAI client instance for OpenRouter."""
    return OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Use single DATABASE_URL environment variable
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("Missing DATABASE_URL; deployment will fail.")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY") or os.getenv("PGPASSWORD") or "fallback_dev_key"

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprint
    from .routes import quote_bp
    app.register_blueprint(quote_bp)

    # Create tables
    with app.app_context():
        from .models import Quote
        # db.create_all()

    return app
