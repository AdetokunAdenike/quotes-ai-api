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
    # Load local .env only in development (safe to leave even in production)
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)

    # Check if PipeOps/Postgres environment vars exist
    pg_user = os.getenv("PGUSER")
    pg_password = os.getenv("PGPASSWORD")
    pg_host = os.getenv("PGHOST")
    pg_port = os.getenv("PGPORT", "5432")
    pg_db = os.getenv("PGDATABASE")

    if pg_user and pg_password and pg_host and pg_db:
        database_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    else:
        # Fallback to SQLite for local development
        sqlite_path = os.path.join(app.instance_path, 'quotes.db')
        database_url = f"sqlite:///{sqlite_path}"

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

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Create tables if not already existing
    with app.app_context():
        from .models import Quote
        db.create_all()

    return app
