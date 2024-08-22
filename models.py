from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
