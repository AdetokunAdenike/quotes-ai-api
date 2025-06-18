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
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Use PostgreSQL if DATABASE_URL is set, otherwise fall back to SQLite for local dev
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        sqlite_path = os.path.join(app.instance_path, 'quotes.db')
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_path}"

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

    # Ensure instance folder exists before using it
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Create tables
    with app.app_context():
        from .models import Quote
        db.create_all()

    return app
