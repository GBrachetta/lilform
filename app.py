import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

# Script to create a table


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    added_builder = db.relationship('Builder', backref='author', lazy=True)
    added_instrument = db.relationship(
        'Instrument', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username})"


class Builder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instruments_built = db.relationship(
        'Instrument', backref='built', lazy=True)

    def __repr__(self):
        return f"Builder('{self.name}')"


class Instrument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    builder_id = db.Column(db.Integer, db.ForeignKey(
        'builder.id'), nullable=False)

    def __repr__(self):
        return f"Instrument('{self.location}')"


@app.route('/')
@app.route('/home')
def home():
    return "<h1>Home</h1>"


@app.route('/about')
def about():
    return "<h1>About</h1>"


if __name__ == "__main__":
    app.run(debug=True)
