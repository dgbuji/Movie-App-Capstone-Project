# Movie Listing API

This project is a movie listing API built using FastAPI. It includes JWT authentication and MongoDB for storage. The API allows users to list movies, rate them, and add comments. 
Only authenticated users can add and edit movies they listed. Everyone can view comments and rating for any movie.

## Endpoints

### Movies
- `POST /movies/`: Add a new movie (authenticated)
- `GET /movies/`: Get a list of all movies
- `GET /movies/{movie_id}`: Get a specific movie
- `PUT /movies/{movie_id}`: Update a movie (authenticated and owner only)
- `DELETE /movies/{movie_id}`: Delete a movie (authenticated and owner only)

### Comments
- `POST /comments/`: Add a comment to a movie (authenticated)
- `GET /comments/{movie_id}`: View comments for a movie
- `POST /comments/{comment_id}/reply`: Reply to a comment (authenticated)

### Ratings
- `POST /ratings/{movie_id}`: Rate a movie (authenticated)
- `GET /ratings/{movie_id}`: Get ratings for a movie
