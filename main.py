from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from crud import movie_crud_service, user_crud_service, comment_crud_service, rating_crud_service
from schema import MovieCreate, MovieUpdate, UserInDb,UserCreate, UserBase, CommentCreate, RatingCreate
from auth import pwd_context, authenticate_user, create_access_token, get_current_user
from logger import get_logger

app = FastAPI()

logger = get_logger(__name__)

@app.post("/signup")
def signup(user: UserCreate):
    db_user = user_crud_service.get_user_by_username(username=user.username)
    logger.info('Creating user....')
    if db_user:
        logger.warning(f"user with {user.username} already exists")
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    created_user = user_crud_service.user_create(user_data=user, hashed_password=hashed_password)
    logger.info('user successfully created')
    return {"message": "User created successfully", "user": created_user}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.get('username')})
    logger.info('Access token generated')
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.get('id')}


@app.post("/movies")
def create_movie(movie_data: MovieCreate, user: dict = Depends(get_current_user)):
    # Attach the current user's ID to the movie data
    logger.info('Movie user_id data')
    movie_data.user_id = user['id']
    movie = movie_crud_service.movie_create(movie_data, user)
    logger.info('Movie created successfully')
    return {"message": "Movie created successfully", "data": movie}

@app.get("/movies")
def get_all_movies(skip: int = 0, limit: int = 5):
    movies = movie_crud_service.get_all_movies(skip, limit)
    return {"data": movies}

@app.get("/movies/{movie_id}")
def get_movies_by_id(movie_id: str):
    movie = movie_crud_service.get_movies_by_id(movie_id)
    if not movie:
        return {"message": "movie not found"}
    logger.info('Movie generated with ID')
    return {"data": movie}


@app.put("/movies/{movie_id}")
def update_movie(movie_id: str, movie_update_data: MovieUpdate, user: UserInDb = Depends(get_current_user)):
    # Fetch the movie to check ownership
    movie = movie_crud_service.get_movies_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["user_id"] != user["id"]:
        logger.warning("user not authorized")
        raise HTTPException(status_code=403, detail="Not authorized to update this movie")
    
    
    updated_movie = movie_crud_service.update_movie(movie_id, movie_update_data, user)
    logger.info('Movie Updated Successfully with movie_update_data')
    return {"message": "Movie updated successfully", "data": updated_movie}


@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: str, user: UserInDb = Depends(get_current_user)):
    # Fetch the movie to check ownership
    logger.info('User_id used for deleting')
    movie = movie_crud_service.get_movies_by_id(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["user_id"] != user["id"]:
        logger.warning("user not authorized")
        raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
    
    movie_crud_service.delete_movie(movie_id, user)
    logger.info('Movie deleted successfully')
    return {"message": "Movie deleted successfully"}


@app.post("/movies/{movie_id}/comments")
def create_comment(movie_id: str, comment_data: CommentCreate, user: UserBase = Depends(get_current_user)):
    comment = comment_crud_service.create_comment(comment_data, user, movie_id)
    logger.info(f'Comment created for {user} in {movie_id} Successfully')
    return {"message": "Comment created successfully", "data": comment}

@app.get("/movies/{movie_id}/comments")
def get_comments_by_movie(movie_id: str):
    comments = comment_crud_service.get_comments_by_movie(movie_id)
    return {"data": comments}


@app.post("/movies/{movie_id}/ratings")
def create_rating(movie_id: str, rating_data: RatingCreate, user: UserBase = Depends(get_current_user)):
    rating = rating_crud_service.create_rating(rating_data, user, movie_id)
    logger.info(f'Rating Created for {user} in {movie_id} Successfully')
    return {"message": "Rating created successfully", "data": rating}

@app.get("/movies/{movie_id}/ratings")
def get_ratings_by_movie(movie_id: str):
    ratings = rating_crud_service.get_ratings_by_movie(movie_id)
    if not ratings:
        return {"data": []}
    # Calculate the average rating
    average_rating = sum(rating["rating"] for rating in ratings) / len(ratings)
    return {"data": ratings, "average_rating": average_rating}





