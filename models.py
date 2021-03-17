import os
from sqlalchemy import Column, String, Integer, Enum
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
# from app import app

database_name = "capstone"
database_path = os.environ.get('DATABASE_URL')

db = SQLAlchemy()

# setup_db(app)


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


class Game(db.Model):
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    rating = db.Column(db.Integer)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def full(self):
        return {
            "id": self.id,
            "title": self.title,
            "completed": self.completed,
            "rating": self.rating
        }

    def short(self):
        return {
            "id": self.id,
            "title": self.title
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Character(db.Model):
    __tablename__ = 'Character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fighting = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    good = db.Column(db.Boolean, nullable=False, default=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)

    def full(self):
        return {
            "id": self.id,
            "name": self.name,
            "fighting": self.fighting,
            "intelligence": self.intelligence,
            "good": self.good,
            "game_id": self.game_id
        }

    def short(self):
        return {
            "id": self.id,
            "title": self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
