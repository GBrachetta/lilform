from datetime import datetime
from lilform import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    added_builder = db.relationship(
        'Builder', backref='contributor', lazy=True)
    added_instrument = db.relationship(
        'Instrument', backref='contributor', lazy=True)

    def __repr__(self):
        return f"User('{self.username})"


class Builder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    biography = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instruments_built = db.relationship(
        'Instrument', backref='instrument_builder', lazy=True)

    def __repr__(self):
        return f"Builder('{self.name}')"


class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    builder_id = db.Column(db.Integer, db.ForeignKey(
        'builder.id'), nullable=False)

    def __repr__(self):
        return f"Instrument('{self.location}')"
