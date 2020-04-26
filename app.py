import os
from datetime import datetime
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)


# Script to create a table



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    added_builder = db.relationship(
        'Builder', backref='contributor', lazy=True)
    added_instrument = db.relationship(
        'Instrument', backref='contributor', lazy=True)

    def __repr__(self):
        return f"User('{self.username})"


class Builder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    instruments_built = db.relationship(
        'Instrument', backref='instrument_builder', lazy=True)

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
    

instruments = [
    {
        'contributor': 'Guillermo Brachetta',
        'instrument_maker': 'Vaudry',
        'location': 'Amsterdam'
    },
    {
        'contributor': 'Menno van Delft',
        'instrument_maker': 'Ruckers',
        'location': 'Paris'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/builders')
def builders():
    return render_template('builders.html')


@app.route('/instruments')
def instrument():
    return render_template('instruments.html', instruments=instruments, title='Instruments')


@app.route('/contributors')
def contributors():
    return render_template('contributors.html')


if __name__ == "__main__":
    app.run(debug=True)
