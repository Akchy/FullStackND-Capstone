# Casting Agenct

## Udacity Full Stack Nano Degree

The project imitates a casting agency.

There are two models: actor and movie.

To test the application, you may run `test_app.py` file which runs a series of unit test cases.
You might also use POSTMAN to test the endpoints and the token can be found in the `.env` file.

You can register and login into the api using [https://udacity-coffee-shop-ashwin.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=f3r5vgCSMONSjyGwB1Y7dXZFuQMmlfyS&redirect_uri=https://localhost:8001/login](https://udacity-coffee-shop-ashwin.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=f3r5vgCSMONSjyGwB1Y7dXZFuQMmlfyS&redirect_uri=https://localhost:8001/login) however, you won't be able to use the APIs since permissions need to be manually assignes.

The API is hosted on: https://casting-agency-udacity-fsnd.herokuapp.com/

## Endpoints

- GET '/movies'
This endpoint fetches all the movies in the database

- GET '/movies/<int:movie_id>'
This endpoint fetches the movie from the database with  id == movie_id

- POST '/movies'
This endpoint creates a new movie in the database

- DELETE '/movies/int:movie_id'
This endpoint will delete the movie from the database with  id == movie_id

- PATCH '/movies/patch/int:movie_id'
This endpoint will update the movie from the database with  id == movie_id

- GET '/actors'
This endpoint fetches all the actors in the databse

- GET '/actors/<int:actor_id>
This endpoint fetches the actor from the database with  id == actor_id

- POST '/actors'
This endpoint creates a new actor in the database

- DELETE '/actors/int:actor_id'
This endpoint will delete the actor from the database with  id == actor_id

- PATCH '/actors/int:actor_id'
This endpoint will update the actor from the database with  id == actor_id