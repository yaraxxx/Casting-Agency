import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
import json


database_path = 'postgres://yarasaleh@localhost:5432/agency'
db = SQLAlchemy()



'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Movies
a persistent movies entity, extends the base SQLAlchemy Model
    -> insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, releaseDate=req_Date)
            movie.insert()
    -> delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, releaseDate=req_Date)
            movie.delete()
    -> update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'The Great Gatsby'
            movie.update()

'''
class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer(),primary_key=True)
    title  = Column(String(180),nullable=False)
    releaseDate = Column(DateTime(),default=datetime.datetime.utcnow)

    def movie_dict(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'releaseDate': self.releaseDate
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.movie_dict())




'''
Actors
a persistent movies entity, extends the base SQLAlchemy Model
 - id
 - name
 - Age
 - Gender
'''
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer(),primary_key=True)
    name  = Column(String(180),nullable=False)
    Age = Column(Integer(), nullable=False)
    gender = Column(String(10),nullable=False)

    def actor_dict(self):
        return {
            'id' : self.id,
            'title' : self.name,
            'age': self.age,
            'gender' : self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.actor_dict())
