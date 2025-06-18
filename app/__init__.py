import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from openai import OpenAI

db = SQLAlchemy()
migrate = Migrate()
client = None  # Global OpenRouter client

def create_app():
    load_dotenv()  # Still safe to keep

    app = Flask(__name__, instance_relative_config=True)

    # DATABASE URL (PipeOps or .env should set this)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set. Please configure it in PipeOps.")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY", "fallback_dev_key")

    global client
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import quote_bp
    app.register_blueprint(quote_bp)

    # Create tables on startup (in prod this happens once, migrations are preferred later)
    with app.app_context():
        from .models import Quote
        db.create_all()

    return app
