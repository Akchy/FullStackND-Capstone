import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
from sqlalchemy.exc import SQLAlchemyError
from datetime import *
from auth.auth import AuthError, requires_auth
from database.models import *


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

  # Routes
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({
            "status": 200,
            "message": "Hello World",
        })

  #### Movies ####
    '''
    Returns the list of all the movies
    '''
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies_query = Movie.query.all()
        movies_list = list(map(Movie.details, movies_query))
        if(len(movies_list) == 0):
            abort(404)
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Movies successfully fetched",
            "data": {
                "movies": movies_list
            }
        })

    '''
    Fetch movie from 'movie_id' and return details
    '''
    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movies_query = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if(movies_query is None):
            abort(404)

        movie = Movie.details(movies_query)

        return jsonify({
            "status": 200,
            "success": True,
            "message": "Movies successfully fetched",
            "data": {
                "movie": movie
            }
        })

    '''
    Create a new movie
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if(body is None):
            abort(422)
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if(title is None or release_date is None):
            abort(422)

        try:
            new_movie = Movie(
                title=title, release_date=release_date)
            Movie.insert(new_movie)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Movie successfully created",
                "data": {
                    "movie": Movie.details(new_movie)
                }
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    Update movie present in the database with id = movie_id
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        body = request.get_json()

        if(body is None):
            abort(422)

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if(movie is None):
            abort(404)

        try:
            if(body is not None):
                setattr(movie, 'title', title)
            if(release_date is not None):
                setattr(movie, 'release_date', release_date)
            Movie.update(movie)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Movie successfully updated",
                "data": {
                    "movie": Movie.details(movie)
                }
            })
        except Exception as e:
            print(e)
            abort(422)
    '''
    Delete a movie with id = movie_id
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if(movie is None):
            abort(404)

        try:
            Movie.delete(movie)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Movie successfully deleted"
            })
        except Exception as e:
            print(e)
            abort(422)

  #### ACTORS ####
    '''
    Returns details of all the actors
    '''
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors_list = list(map(Actor.details, Actor.query.all()))
        if(len(actors_list) == 0):
            abort(404)
        return jsonify({
            "status": 200,
            "success": True,
            "message": "Actors successfully fetched",
            "data": {
                "actors": actors_list
            }
        })

    '''
    Returns the detail of the actor with id = movie_id
    '''
    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if(actor is None):
            abort(404)

        return jsonify({
            "status": 200,
            "success": True,
            "message": "Actors successfully fetched",
            "data": {
                "actor": Actor.details(actor)
            }
        })

    '''
    Create a new actor
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):

        body = request.get_json()
        if(body is None):
            abort(422)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie = body.get('movie', None)

        if(name is None or age is None or gender is None):
            abort(422)
        try:
            if(movie is not None):
                movie_query = Movie.query.filter(
                    Movie.id == movie).one_or_none()
                if(movie_query is None):
                    abort(404)
            else:
                new_actor = Actor(name=name, age=age,
                                  gender=gender, movie=movie)

            Actor.insert(new_actor)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Actor successfully created",
                "data": {
                    "actor": Actor.details(new_actor)
                }
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    Update actor present in the database with id = movie_id
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):

        body = request.get_json()
        if(body is None):
            abort(422)

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movie = body.get('movie', None)

        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if(actor is None):
            abort(404)

        try:
            if(name is not None):
                setattr(actor, 'name', name)
            if(age is not None):
                setattr(actor, 'age', age)
            if(gender is not None):
                setattr(actor, 'gender', gender)
            if(movie is not None):
                setattr(actor, 'movie', movie)

            Actor.update(actor)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Actor successfully created",
                "data": {
                    "actor": Actor.details(actor)
                }
            })
        except Exception as e:
            print(e)
            abort(422)

    '''
    Delete an actor with id = actor_id
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        if(actor is None):
            abort(404)
        try:
            Actor.delete(actor)
            return jsonify({
                "status": 200,
                "success": True,
                "message": "Actor successfully deleted"
            })
        except Exception as e:
            print(e)
            abort(422)

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
    def auth_error(e):
        print(e)
        return jsonify(e.error), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0', port=8080, debug=True)
    app.run()
