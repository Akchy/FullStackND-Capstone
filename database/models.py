
import os
from sqlalchemy import Column, String, Integer, ARRAY, create_engine, Enum, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import *
import enum

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(String(10), nullable=False)
    actor = db.relationship('Actor', backref='Movie', lazy='dynamic')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def actor_details(self):
        return {
            'id': self.Actor.id,
            'name': self.Actorname,
            'age': self.Actor.age,
            'gender': self.Actor.gender
        }

class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)
    movie_id = Column(Integer, db.ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, age, gender, movie):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def details(self):
        return  {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }
