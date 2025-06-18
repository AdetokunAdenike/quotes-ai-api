import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from openai import OpenAI

db = SQLAlchemy()
migrate = Migrate()
client = None  # Global OpenRouter client

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Construct DATABASE_URL from PipeOps-provided vars
    pg_user = os.getenv("PGUSER")
    pg_password = os.getenv("PGPASSWORD")
    pg_host = os.getenv("PGHOST")
    pg_port = os.getenv("PGPORT", "5432")
    pg_db = os.getenv("PGDATABASE")

    if all([pg_user, pg_password, pg_host, pg_db]):
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        )
    else:
        raise RuntimeError("Missing Postgres environment variables; deployment will fail.")

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("SECRET_KEY") or os.getenv("POSTGRES_PASSWORD") or "fallback_dev_key"

    global client
    client = OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import quote_bp
    app.register_blueprint(quote_bp)

    with app.app_context():
        from .models import Quote
        db.create_all()

    return app
