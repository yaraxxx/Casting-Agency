#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import sys

from models import db_drop_and_create_all, setup_db, Movies, Actors

from auth import AuthError, requires_auth




def create_app(test_config=None):
    #----------------------------------------------------------------------------#
    # App Config.
    #----------------------------------------------------------------------------#
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, DELETE, PATCH, OPTIONS')
        return response



    '''
    uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START THE DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()

    def get_movies_list():
        movies_list = []
        movies = Movies.query.all()
        for movie in movies:
            movies_list.append(movie.movie_dict())
        return movies_list

    def get_actors_list():
        actors_list = []
        actors = Actors.query.all()
        for actor in actors:
            actors_list.append(actor.actor_dict())
        return actors_list

    #----------------------------------------------------------------------------#
    # ROUTES.
    #----------------------------------------------------------------------------#

    @app.route('/')
    def index():
        return 'Hi!!'


    #  Movies
    #----------------------------------------------------------------
    @app.route('/all_movies',methods=['GET'])
    @requires_auth('get:all_movies')
    def get_movies(payload):
        try:
            movies_list = get_movies_list()
            if(len(movies_list) == 0):
                abort(404)


            return jsonify({
                "success": True,
                "movies": movies_list})
        except:
            abort(404)




    @app.route('/movie',methods=['POST'])
    @requires_auth('post:movie')
    def add_movie(payload):
        try:
            body = request.get_json()
            new_movie = Movies(
                id = body.get("id"),
                title = body.get("title"),
                releaseDate = body.get("releaseDate")
            )

            new_movie.insert()
            movie = Movies.query.filter_by(id=new_movie.id).first()
            return jsonify({
                "success": True,
                "movie": [movie.movie_dict()]
            })
        except:
            # print("Movie: --------------------")
            # print(sys.exc_info())
            abort(422)






    @app.route('/movie/<int:id>',methods=['PATCH'])
    @requires_auth('patch:movie')
    def update_movie(payload,id):
        try:
            movie = Movies.query.filter_by(id=id).one_or_none()


            body = request.get_json()
            title_update = body.get('title')
            releaseDate_update = body.get('releaseDate')

            if(title_update):
                movie.title = title_update
            if(releaseDate_update):
                movie.releaseDate = releaseDate_update

            movie.update()
            return jsonify({
                "success": True,
                "movie": [movie.movie_dict()]
            })
        except:
            # print("Movie -----------------------------------")
            # print(sys.exc_info())
            if(movie is None):
                abort(404)
            else:
                abort(422)



    @app.route('/movie/<int:id>',methods=['DELETE'])
    @requires_auth('delete:movie')
    def remove_movie(payload,id):
        try:
            movie = Movies.query.filter_by(id=id).one_or_none()
            # if(movie is None):
            #     print("test1111")
            #     abort(404)

            movie.delete()

            return jsonify({
                "success": True,
                "deleted_movie": id
            })
        except:
            # print("Movie -----------------------------------")
            # print(sys.exc_info())
            abort(404)


    #  Actors
    #----------------------------------------------------------------
    @app.route('/all_actors',methods=['GET'])
    @requires_auth('get:all_actors')
    def get_actors(payload):
        try:
            actors_list = get_actors_list()
            if(len(actors_list) == 0):
                abort(404)

            return jsonify({
                "success": True,
                "actors": actors_list})
        except:
            abort(404)




    @app.route('/actor',methods=['POST'])
    @requires_auth('post:actor')
    def add_actor(payload):
        try:
            body = request.get_json()
            new_actor = Actors(
                id = body.get("id"),
                name = body.get("name"),
                Age = body.get("Age"),
                gender = body.get("gender"),
                movie_id = body.get("movie_id")
            )

            new_actor.insert()
            actor = Actors.query.filter_by(id=new_actor.id).first()
            return jsonify({
                "success": True,
                "actor": [actor.actor_dict()]
            })
        except:
            # print("Actor: --------------------")
            # print(sys.exc_info())
            abort(422)



    @app.route('/actor/<int:id>',methods=['PATCH'])
    @requires_auth('patch:actor')
    def update_actor(payload,id):
        try:
            actor = Actors.query.filter_by(id=id).one_or_none()


            body = request.get_json()
            name_update = body.get("name")
            age_update = body.get("Age")
            movie_update = body.get("movie_id")

            if(name_update):
                actor.name = name_update
            if(age_update):
                actor.Age = age_update
            if(movie_update):
                actor.movie_id = movie_update

            actor.update()
            return jsonify({
                "success": True,
                "actor": [actor.actor_dict()]
            })
        except:
            # print("Actor: --------------------")
            # print(sys.exc_info())
            if(actor is None):
                abort(404)
            else:
                abort(422)




    @app.route('/actor/<int:id>',methods=['DELETE'])
    @requires_auth('delete:actor')
    def remove_actor(payload,id):
        try:
            actor = Actors.query.filter_by(id=id).one_or_none()
            name = str(actor.name)

            actor.delete()

            return jsonify({
                "success": True,
                "deleted_actor": name
            })
        except:
            # print("Actor -----------------------------------")
            # print(sys.exc_info())
            abort(404)



    #----------------------------------------------------------------------------#
    # ERROR HANDLING.
    #----------------------------------------------------------------------------#

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error
        }), 401


    return app



APP = create_app()




# For Hyroku use:
#  run the app and specify port manually:
if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0',port=8080,debug=True)

# # Local use:
# if __name__ == '__main__':
#     APP.run(host='127.0.0.1', port=8080, debug=True)
