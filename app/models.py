from . import db
from datetime import datetime

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(120), nullable=False)
    quote = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(120), nullable=True)
