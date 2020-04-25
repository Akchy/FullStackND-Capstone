# Casting Agency

## General Specifications

- Models will include at least…
    - Two classes with primary keys at at least two attributes each
    - [Optional but encouraged] One-to-many or many-to-many relationships between classes
- Endpoints will include at least…
    - Two GET requests
    - One POST request
    - One PATCH request
    - One DELETE request
- Roles will include at least…
    - Two roles with different permissions
    - Permissions specified for all endpoints
- Tests will include at least….
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role


## Casting Agency Specifications
- The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

- Models:

    - Movies with attributes title and release date
    - Actors with attributes name, age and gender
- Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/
- Roles:
    - Casting Assistant
        - Can view actors and movies
    - Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
- Tests:
    - One test for success behavior of each endpoint
    - One test for error behavior of each endpoint
    - At least two tests of RBAC for each role
