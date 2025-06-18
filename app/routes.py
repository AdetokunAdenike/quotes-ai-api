import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, session
from . import db, get_openrouter_client
from .models import Quote

# Initialize Blueprint
quote_bp = Blueprint("quote", __name__)

@quote_bp.before_app_request
def assign_session_id():
    if "id" not in session:
        session["id"] = str(uuid.uuid4())

@quote_bp.route("/", methods=["GET"])
def home():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return render_template("index.html", quotes=quotes, current_year=datetime.utcnow().year)

@quote_bp.route("/dashboard", methods=["GET"])
def dashboard():
    quotes = Quote.query.filter_by(session_id=session["id"]).order_by(Quote.created_at.desc()).all()
    return render_template("index.html", quotes=quotes, current_year=datetime.utcnow().year)

@quote_bp.route("/generate", methods=["POST"])
def generate_quote():
    data = request.get_json()
    theme = data.get("theme", "motivation")

    try:
        client = get_openrouter_client()

        response = client.chat.completions.create(
            model="mistralai/mistral-small-3.1-24b-instruct",
            temperature=0.9,
            messages=[
                {"role": "system", "content": "You are a wise and inspiring assistant that gives short motivational quotes."},
                {"role": "user", "content": f"Give a short motivational quote about {theme}. Do not say 'here is a quote'. Just return the quote only."}
            ]
        )

        ai_quote = response.choices[0].message.content.strip()

        new_quote = Quote(
            theme=theme,
            quote=ai_quote,
            session_id=session["id"]
        )
        db.session.add(new_quote)
        db.session.commit()

        return jsonify({"theme": theme, "quote": ai_quote})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@quote_bp.route("/quotes", methods=["GET"])
def get_quotes():
    quotes = Quote.query.order_by(Quote.created_at.desc()).all()
    return jsonify([
        {
            "id": q.id,
            "theme": q.theme,
            "quote": q.quote,
            "created_at": q.created_at.isoformat()
        }
        for q in quotes
    ])
